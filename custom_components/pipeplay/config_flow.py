"""Config flow for PipePlay integration."""
import logging
import aiohttp
import asyncio
from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME

CONF_API_KEY = "api_key"
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

DOMAIN = "pipeplay"

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_HOST, default="localhost"): str,
    vol.Required(CONF_PORT, default=8080): int,
    vol.Optional(CONF_NAME, default="PipePlay Player"): str,
    vol.Optional(CONF_API_KEY, default=""): str,
})


class PipePlayConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for PipePlay."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self.discovery_info = {}

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                api_key = user_input.get(CONF_API_KEY) or None
                await self._test_connection(user_input[CONF_HOST], user_input[CONF_PORT], api_key)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Create a unique ID based on host and port
                await self.async_set_unique_id(f"{user_input[CONF_HOST]}:{user_input[CONF_PORT]}")
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_zeroconf(self, discovery_info: Dict[str, Any]) -> FlowResult:
        """Handle zeroconf discovery."""
        host = discovery_info.get("host")
        port = discovery_info.get("port", 8080)
        name = discovery_info.get("name", "PipePlay Player")
        
        # Set unique ID based on host and port
        await self.async_set_unique_id(f"{host}:{port}")
        self._abort_if_unique_id_configured()
        
        # Store discovery info
        self.discovery_info = {
            CONF_HOST: host,
            CONF_PORT: port,
            CONF_NAME: name,
        }
        
        # Set context for the discovered device
        self.context["title_placeholders"] = {"name": name, "host": host}
        
        try:
            await self._test_connection(host, port)
        except (CannotConnect, Exception):
            return self.async_abort(reason="cannot_connect")
        
        return await self.async_step_discovery_confirm()

    async def async_step_discovery_confirm(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Confirm discovery."""
        if user_input is not None:
            return self.async_create_entry(
                title=self.discovery_info[CONF_NAME],
                data=self.discovery_info,
            )

        return self.async_show_form(
            step_id="discovery_confirm",
            description_placeholders={
                "name": self.discovery_info[CONF_NAME],
                "host": self.discovery_info[CONF_HOST],
                "port": self.discovery_info[CONF_PORT],
            },
        )

    async def _test_connection(self, host: str, port: int, api_key: Optional[str] = None) -> bool:
        """Test if we can connect to the PipePlay service."""
        session = async_get_clientsession(self.hass)
        
        # First check if authentication is required
        try:
            async with asyncio.timeout(10):
                async with session.get(f"http://{host}:{port}/api/auth/info") as response:
                    if response.status == 200:
                        auth_info = await response.json()
                        auth_required = auth_info.get("auth_required", False)
                    else:
                        auth_required = False
        except Exception:
            auth_required = False
        
        # Prepare headers
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        # Test actual connection
        try:
            async with asyncio.timeout(10):
                async with session.get(f"http://{host}:{port}/api/status", headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("service") == "pipeplay"
                    elif response.status == 401:
                        if auth_required and not api_key:
                            raise InvalidAuth("API key required but not provided")
                        elif api_key:
                            raise InvalidAuth("Invalid API key")
                        else:
                            raise CannotConnect("Authentication failed")
        except InvalidAuth:
            raise
        except Exception as err:
            _LOGGER.debug("Connection test failed: %s", err)
            raise CannotConnect from err
        
        raise CannotConnect


class CannotConnect(Exception):
    """Error to indicate we cannot connect."""


class InvalidAuth(Exception):
    """Error to indicate authentication failure."""