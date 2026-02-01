# USB Microscope Project Makefile

.PHONY: help install test clean setup scan driver gui

help:
	@echo "USB Microscope Ubuntu Driver Project"
	@echo ""
	@echo "Available commands:"
	@echo "  setup    - Setup development environment"
	@echo "  install  - Install Python dependencies"
	@echo "  scan     - Scan USB devices"
	@echo "  driver   - Run driver test"
	@echo "  gui      - Run GUI application"
	@echo "  test     - Run all tests"
	@echo "  clean    - Clean temporary files"

setup:
	@echo "Setting up development environment..."
	chmod +x tools/setup_environment.sh
	./tools/setup_environment.sh

install:
	@echo "Installing Python dependencies..."
	pip3 install --user -r requirements.txt

scan:
	@echo "Scanning USB devices..."
	python3 tools/usb_scanner.py

driver:
	@echo "Running driver test..."
	python3 driver/microscope_driver.py

gui:
	@echo "Running GUI application..."
	python3 gui/microscope_gui.py

test: scan driver
	@echo "All tests completed"

clean:
	@echo "Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.log" -delete

# Developer commands
dev-setup: setup install
	@echo "Development environment setup complete"

# USB permissions setup (requires root)
usb-permissions:
	@echo "Setting USB device permissions..."
	sudo usermod -a -G plugdev $USER
	@echo "Please logout and login again"