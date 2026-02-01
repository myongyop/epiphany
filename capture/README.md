# USB Packet Capture Files

This directory contains USB traffic files captured with Wireshark.

## File Naming Convention

- `init_sequence.pcap` - Device initialization sequence
- `video_stream.pcap` - Video streaming packets
- `control_commands.pcap` - Control command packets
- `led_control.pcap` - LED lighting control packets
- `zoom_control.pcap` - Zoom control commands
- `capture_image.pcap` - Image capture commands

## Capture Method

1. Run Wireshark (with root privileges)
2. Select usbmon interface
3. Connect microscope and test functions
4. Save packets

## Analysis Tools

```bash
# Command line analysis with tshark
tshark -r capture_file.pcap -Y "usb"

# Filter specific device only
tshark -r capture_file.pcap -Y "usb.device_address == 5"
```