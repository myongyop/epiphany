# USB Traffic Analysis

## Microscope Information
- Product Name: Smartphone USB Digital Microscope
- Magnification: 1000x, 1600x
- Connection: USB Type-C

## Analysis Environment Setup

### 1. Wireshark USB Capture Setup

```bash
# Load usbmon module
sudo modprobe usbmon

# Run Wireshark (requires root privileges)
sudo wireshark

# Or setup for running with user privileges
sudo usermod -a -G wireshark $USER
# Logout and login required
```

### 2. VirtualBox Setup

1. Create Windows 10 VM
2. Enable USB 3.0 controller
3. Add USB filter for automatic microscope connection

### 3. Capture Procedure

1. Select usbmon interface in Wireshark
2. Connect microscope to VM
3. Run original software in Windows
4. Perform the following actions while capturing packets:
   - Microscope connection/recognition
   - Start image streaming
   - Zoom in/out control
   - LED lighting control
   - Photo capture
   - Disconnect

## Analysis Results

### USB Descriptor Information
```
# Example lsusb output
Bus 001 Device 005: ID 1234:5678 Unknown Manufacturer USB Microscope
```

### Main USB Endpoints
- EP1 IN: Video stream data
- EP2 OUT: Control commands
- EP3 IN: Status information

### Communication Protocol Patterns
(To be updated after capture)

## Next Steps
1. Perform actual USB packet capture
2. Analyze protocol patterns
3. Reverse engineer control commands