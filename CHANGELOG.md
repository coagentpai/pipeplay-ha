# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-06

### Added
- Initial release of PipePlay Home Assistant integration
- Automatic discovery via Zeroconf/mDNS
- Full media player entity support with all standard controls
- Real-time state updates via HTTP API
- Configuration flow for easy setup
- Support for play, pause, stop, volume control, seek, and mute
- Media metadata display (title, artist, album, duration, position)
- Robust error handling and connection management
- HACS compatibility

### Features
- **Automatic Discovery**: PipePlay services are automatically discovered on the network
- **Media Controls**: Complete playback control including seek and volume
- **Metadata Support**: Display track information and playback position
- **Configuration UI**: Easy setup through Home Assistant's configuration flow
- **Error Recovery**: Automatic reconnection and error handling

[1.0.0]: https://github.com/coagentpai/pipeplay-ha/releases/tag/v1.0.0