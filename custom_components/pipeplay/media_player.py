"""PipePlay media player platform."""
import asyncio
import logging
from datetime import timedelta
from typing import Any, Dict, Optional

import aiohttp
from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
    MediaType,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = 5  # seconds


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the PipePlay media player platform."""
    host = config_entry.data[CONF_HOST]
    port = config_entry.data[CONF_PORT]
    name = config_entry.data[CONF_NAME]
    
    coordinator = PipePlayUpdateCoordinator(hass, host, port)
    
    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_config_entry_first_refresh()
    
    async_add_entities([PipePlayMediaPlayer(coordinator, name)], True)


class PipePlayUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching PipePlay data."""

    def __init__(self, hass: HomeAssistant, host: str, port: int) -> None:
        """Initialize the coordinator."""
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}/api"
        
        super().__init__(
            hass,
            _LOGGER,
            name="pipeplay",
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch data from PipePlay API."""
        session = async_get_clientsession(self.hass)
        
        try:
            async with asyncio.timeout(10):
                async with session.get(f"{self.base_url}/status") as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise UpdateFailed(f"Error fetching data: {response.status}")
        except Exception as err:
            raise UpdateFailed(f"Error communicating with PipePlay: {err}")


class PipePlayMediaPlayer(CoordinatorEntity, MediaPlayerEntity):
    """Representation of a PipePlay media player."""

    def __init__(self, coordinator: PipePlayUpdateCoordinator, name: str) -> None:
        """Initialize the media player."""
        super().__init__(coordinator)
        self._name = name
        self._attr_unique_id = f"pipeplay_{coordinator.host}_{coordinator.port}"
        self._attr_device_class = "speaker"
        
        self._attr_supported_features = (
            MediaPlayerEntityFeature.PLAY
            | MediaPlayerEntityFeature.PAUSE
            | MediaPlayerEntityFeature.STOP
            | MediaPlayerEntityFeature.VOLUME_SET
            | MediaPlayerEntityFeature.VOLUME_MUTE
            | MediaPlayerEntityFeature.SEEK
            | MediaPlayerEntityFeature.PLAY_MEDIA
        )

    @property
    def name(self) -> str:
        """Return the name of the media player."""
        return self._name

    @property
    def state(self) -> str:
        """Return the current state of the media player."""
        if not self.coordinator.last_update_success:
            return MediaPlayerState.UNAVAILABLE
            
        state = self.coordinator.data.get("state", "idle")
        
        state_mapping = {
            "idle": MediaPlayerState.IDLE,
            "playing": MediaPlayerState.PLAYING,
            "paused": MediaPlayerState.PAUSED,
            "buffering": MediaPlayerState.BUFFERING,
        }
        
        return state_mapping.get(state, MediaPlayerState.IDLE)

    @property
    def volume_level(self) -> Optional[float]:
        """Return the volume level of the media player (0..1)."""
        return self.coordinator.data.get("volume_level")

    @property
    def is_volume_muted(self) -> Optional[bool]:
        """Return boolean if volume is currently muted."""
        return self.coordinator.data.get("is_muted")

    @property
    def media_content_type(self) -> Optional[str]:
        """Return the media content type."""
        return self.coordinator.data.get("media_content_type")

    @property
    def media_title(self) -> Optional[str]:
        """Return the title of current playing media."""
        return self.coordinator.data.get("media_title")

    @property
    def media_artist(self) -> Optional[str]:
        """Return the artist of current playing media."""
        return self.coordinator.data.get("media_artist")

    @property
    def media_album_name(self) -> Optional[str]:
        """Return the album name of current playing media."""
        return self.coordinator.data.get("media_album")

    @property
    def media_duration(self) -> Optional[int]:
        """Return the duration of current playing media in seconds."""
        duration = self.coordinator.data.get("media_duration")
        return int(duration) if duration and duration > 0 else None

    @property
    def media_position(self) -> Optional[int]:
        """Return the position of current playing media in seconds."""
        position = self.coordinator.data.get("media_position")
        return int(position) if position else None

    async def async_play_media(self, media_type: str, media_id: str, **kwargs) -> None:
        """Play media from a URL or file path."""
        await self._send_command("play_media", {
            "media_type": media_type,
            "media_id": media_id
        })

    async def async_media_play(self) -> None:
        """Send play command."""
        await self._send_command("play")

    async def async_media_pause(self) -> None:
        """Send pause command."""
        await self._send_command("pause")

    async def async_media_stop(self) -> None:
        """Send stop command."""
        await self._send_command("stop")

    async def async_set_volume_level(self, volume: float) -> None:
        """Set volume level, range 0..1."""
        await self._send_command("volume", {"level": volume})

    async def async_mute_volume(self, mute: bool) -> None:
        """Mute (true) or unmute (false) media player."""
        await self._send_command("mute", {"muted": mute})

    async def async_media_seek(self, position: float) -> None:
        """Send seek command."""
        await self._send_command("seek", {"position": position})

    async def _send_command(self, command: str, data: Optional[Dict[str, Any]] = None) -> None:
        """Send command to PipePlay service."""
        session = async_get_clientsession(self.hass)
        url = f"{self.coordinator.base_url}/command"
        
        payload = {"command": command}
        if data:
            payload.update(data)
        
        try:
            async with asyncio.timeout(10):
                async with session.post(url, json=payload) as response:
                    if response.status != 200:
                        _LOGGER.error("Failed to send command %s: %s", command, response.status)
                    else:
                        # Trigger immediate update
                        await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Error sending command %s: %s", command, err)