# PipePlay Home Assistant Integration

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]

_Integration to add PipePlay PipeWire media players to Home Assistant._

**This integration will set up the following platforms.**

| Platform        | Description                         |
| --------------- | ----------------------------------- |
| `media_player` | PipePlay PipeWire media player      |

## Features

- **Automatic Discovery**: Uses Zeroconf to automatically discover PipePlay players on your network
- **Full Media Player Integration**: Complete Home Assistant media player entity with all controls
- **Real-time State Updates**: Live status updates via HTTP API polling
- **Configuration Flow**: Easy setup through the Home Assistant UI

## Installation

### HACS (Recommended)

1. Make sure [HACS](https://hacs.xyz/) is installed
2. Go to HACS → Integrations
3. Click the three dots in the top right corner and select "Custom repositories"
4. Add `https://github.com/coagentpai/pipeplay-ha` as an Integration repository
5. Search for "PipePlay" in HACS and install
6. Restart Home Assistant

### Manual Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`)
2. If you do not have a `custom_components` directory (folder) there, you need to create it
3. In the `custom_components` directory (folder) create a new folder called `pipeplay`
4. Download _all_ the files from the `custom_components/pipeplay/` directory (folder) in this repository
5. Place the files you downloaded in the new directory (folder) you created
6. Restart Home Assistant

## Configuration

### PipePlay Service Setup

First, you need to have a PipePlay service running. Download and install PipePlay:

```bash
git clone https://github.com/coagentpai/pipeplay
cd pipeplay
pip install -e .
```

Start the PipePlay service:

```bash
pipeplay --daemon
```

The service will start with automatic discovery enabled by default.

### Home Assistant Integration

#### Automatic Discovery

If your PipePlay service is running with discovery enabled (default), it should appear automatically in Home Assistant:

1. Go to **Settings** → **Devices & Services**
2. Look for "PipePlay Player Found" in discovered devices
3. Click "Configure" to add the device

#### Manual Setup

If automatic discovery doesn't work:

1. Go to **Settings** → **Devices & Services** → **Add Integration**
2. Search for "PipePlay PipeWire Media Player"
3. Enter the connection details:
   - **Host**: IP address of your PipePlay service (e.g., `192.168.1.100`)
   - **Port**: API port (default: `8080`)
   - **Name**: Friendly name for the player
   - **API Key**: Required if authentication is enabled (leave empty if not using auth)

## Usage

Once configured, the media player will appear as a standard Home Assistant media player entity with these capabilities:

- **Playback Controls**: Play, pause, stop
- **Volume Control**: Set volume level and mute/unmute
- **Seek**: Jump to specific position in media
- **Media Information**: Display title, artist, album, duration, and position
- **Play Media**: Play files from URLs or local paths

### Playing Media

You can play media through:

- Home Assistant UI
- Automations and scripts
- REST API
- Service calls

Example service call:
```yaml
service: media_player.play_media
target:
  entity_id: media_player.pipeplay_player
data:
  media_content_type: music
  media_content_id: /path/to/your/music.mp3
```

## Troubleshooting

### Player Not Discovered

1. Ensure both PipePlay service and Home Assistant are on the same network
2. Check that the PipePlay API server is running (default port 8080)
3. Verify discovery is enabled in PipePlay configuration
4. Try manual setup with the player's IP address

### Connection Issues

1. Check firewall settings on the PipePlay host
2. Verify the API port is accessible: `curl http://PLAYER_IP:8080/api/status`
3. Check PipePlay logs for any errors
4. Ensure PipeWire/PulseAudio is running on the PipePlay host

### Authentication Issues

1. **"Authentication failed - check your API key"**: 
   - Verify the API key is correct in the integration configuration
   - Check if authentication is enabled on the PipePlay service
   - Look for the generated API key in PipePlay logs or config file
2. **Connection works without API key but fails with key**:
   - Authentication may be disabled on the PipePlay service
   - Remove the API key from the integration config if auth is not needed

### State Not Updating

1. Check network connectivity between Home Assistant and PipePlay
2. Verify the PipePlay service is running and responding
3. Check Home Assistant logs for any error messages

## Development

### API Endpoints

The integration communicates with PipePlay via HTTP API:

- `GET /api/status` - Current player status
- `POST /api/command` - Send control commands
- `GET /api/info` - Service information
- `GET /api/auth/info` - Authentication requirements
- `GET /health` - Health check

#### Authentication

When authentication is enabled on the PipePlay service, all API requests (except `/health` and `/api/auth/info`) require an `Authorization: Bearer <api_key>` header. The integration automatically handles this when an API key is configured.

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

- [GitHub Issues](https://github.com/coagentpai/pipeplay-ha/issues)
- [Home Assistant Community](https://community.home-assistant.io/)
- [PipePlay Documentation](https://github.com/coagentpai/pipeplay-ha)

---

[pipeplay-integration]: https://github.com/coagentpai/pipeplay-ha
[commits-shield]: https://img.shields.io/badge/commits-active-brightgreen.svg?style=for-the-badge
[commits]: https://github.com/coagentpai/pipeplay-ha/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/badge/release-v1.0.0-blue.svg?style=for-the-badge
[releases]: https://github.com/coagentpai/pipeplay-ha/releases