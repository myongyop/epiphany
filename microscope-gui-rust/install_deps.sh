#!/bin/bash

echo "🦀 Installing Rust Microscope GUI dependencies..."

# Update system packages
sudo apt update

# Install OpenCV development libraries
echo "📦 Installing OpenCV..."
sudo apt install -y \
    libopencv-dev \
    libopencv-contrib-dev \
    pkg-config \
    libclang-dev \
    clang

# Additional system libraries
echo "📦 Installing additional libraries..."
sudo apt install -y \
    libudev-dev \
    libgtk-3-dev \
    libxcb-render0-dev \
    libxcb-shape0-dev \
    libxcb-xfixes0-dev \
    libxkbcommon-dev \
    libssl-dev

# Add user to video group
echo "👤 Setting up user permissions..."
sudo usermod -a -G video $USER

echo "✅ Dependencies installation complete!"
echo "⚠️  Please logout and login again to apply video group permissions."
echo ""
echo "🚀 Build and run:"
echo "   cargo build --release"
echo "   cargo run --release"