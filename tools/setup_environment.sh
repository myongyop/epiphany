#!/bin/bash

# USB Microscope Development Environment Setup Script

echo "Setting up USB microscope development environment..."

# System update
echo "Updating system packages..."
sudo apt update

# Install essential packages
echo "Installing essential packages..."
sudo apt install -y \
    wireshark \
    libusb-1.0-0-dev \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    virtualbox \
    virtualbox-ext-pack

# Install Python packages
echo "Installing Python packages..."
pip3 install --user \
    pyusb \
    opencv-python \
    numpy \
    pillow \
    tkinter \
    matplotlib

# Load usbmon module
echo "Loading usbmon module..."
sudo modprobe usbmon

# Setup Wireshark user group
echo "Setting up Wireshark permissions..."
sudo usermod -a -G wireshark $USER

# Create udev rules for USB device permissions
echo "Setting up USB device permissions..."
sudo tee /etc/udev/rules.d/99-usb-microscope.rules > /dev/null << 'EOF'
# USB microscope device permissions
# Replace with actual Vendor ID and Product ID
SUBSYSTEM=="usb", ATTR{idVendor}=="1234", ATTR{idProduct}=="5678", MODE="0666", GROUP="plugdev"
EOF

# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger

echo "Setup complete!"
echo "Note: Please logout and login again to apply Wireshark permissions."
echo "Update the udev rules with the actual Vendor ID and Product ID of your USB microscope."