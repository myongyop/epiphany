# Rust Microscope GUI Makefile

.PHONY: help install build run release clean test deps

help:
	@echo "🦀 Rust Microscope GUI Project"
	@echo ""
	@echo "Available commands:"
	@echo "  deps     - Install system dependencies"
	@echo "  build    - Debug build"
	@echo "  release  - Release build"
	@echo "  run      - Run application (debug)"
	@echo "  run-rel  - Run application (release)"
	@echo "  test     - Run tests"
	@echo "  clean    - Clean build files"
	@echo "  install  - Install to system"

deps:
	@echo "🔧 Installing system dependencies..."
	./install_deps.sh

build:
	@echo "🔨 Building debug version..."
	cargo build

release:
	@echo "🚀 Building release version..."
	cargo build --release

run:
	@echo "▶️  Running application (debug)..."
	RUST_LOG=info cargo run

run-rel:
	@echo "▶️  Running application (release)..."
	RUST_LOG=info cargo run --release

test:
	@echo "🧪 Running tests..."
	cargo test

clean:
	@echo "🧹 Cleaning build files..."
	cargo clean

install: release
	@echo "📦 Installing to system..."
	sudo cp target/release/microscope-gui-rust /usr/local/bin/
	@echo "✅ Installation complete! Run with 'microscope-gui-rust' command."

# Developer commands
dev: build run

check:
	@echo "🔍 Checking code..."
	cargo check
	cargo clippy -- -D warnings
	cargo fmt --check

format:
	@echo "🎨 Formatting code..."
	cargo fmt

# Cross-compilation (optional)
build-windows:
	@echo "🪟 Building for Windows..."
	cargo build --release --target x86_64-pc-windows-gnu

build-macos:
	@echo "🍎 Building for macOS..."
	cargo build --release --target x86_64-apple-darwin