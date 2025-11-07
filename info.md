# PipePlay PipeWire Media Player

A Home Assistant integration for PipePlay, a PipeWire-based media player designed for seamless integration with Home Assistant.

## What is PipePlay?

PipePlay is a lightweight media player that uses PipeWire for audio playback and provides a clean integration with Home Assistant. It's designed to be simple, efficient, and provide full media player functionality without unnecessary complexity.

## Key Features

### Automatic Discovery
PipePlay services are automatically discovered on your network using Zeroconf/mDNS, making setup effortless.

### Full Media Player Support
- Play/Pause/Stop controls
- Volume control and muting
- Seek to specific positions
- Media metadata display (title, artist, album, duration)
- Support for multiple audio formats (MP3, FLAC, WAV, OGG, M4A, AAC)

### Real-time Updates
Live status updates via HTTP API ensure your Home Assistant interface always reflects the current player state.

### PipeWire Integration
Uses modern PipeWire audio system for robust, low-latency audio playback with seamless integration into Linux audio ecosystems.

## Installation Requirements

### PipePlay Service
You need to install and run the PipePlay service on a machine with:
- Linux with PipeWire/PulseAudio
- Python 3.9+
- libmpv for media playback

### Network Requirements
- PipePlay service and Home Assistant must be on the same network for automatic discovery
- Default API port 8080 must be accessible

## Quick Start

1. Install PipePlay service on your target machine
2. Install this integration through HACS
3. Restart Home Assistant
4. Look for discovered PipePlay devices in Settings → Devices & Services

## Use Cases

- **Multi-room Audio**: Run PipePlay instances on different machines for whole-home audio
- **Dedicated Audio Zones**: Create dedicated media players for specific areas
- **Integration with Automations**: Control music playback based on presence, time, or other conditions
- **Voice Control**: Use with voice assistants through Home Assistant

## Documentation

For detailed setup instructions, configuration options, and troubleshooting, see the [full documentation](https://github.com/coagentpai/pipeplay-ha).