#!/usr/bin/env python3
"""
USB Microscope Driver
Basic microscope control driver using libusb
"""

import usb.core
import usb.util
import cv2
import numpy as np
import time
import sys
from typing import Optional, Tuple

class MicroscopeDriver:
    """USB Microscope Driver Class"""
    
    def __init__(self, vendor_id: int = None, product_id: int = None):
        """
        Initialize driver
        
        Args:
            vendor_id: USB Vendor ID (hexadecimal)
            product_id: USB Product ID (hexadecimal)
        """
        self.device = None
        self.vendor_id = vendor_id or 0x05e3  # Genesys Logic
        self.product_id = product_id or 0xf12a  # Digital Microscope
        self.is_connected = False
        self.video_device_index = 4  # Microscope video device index
        self.cap = None  # OpenCV VideoCapture object
        
        # Microscope specific settings
        self.supported_resolutions = [(640, 480), (320, 240)]
        self.current_resolution = (640, 480)
        
    def connect(self) -> bool:
        """Attempt to connect to the microscope."""
        try:
            # Find USB device
            self.device = usb.core.find(
                idVendor=self.vendor_id, 
                idProduct=self.product_id
            )
            
            if self.device is None:
                print("Microscope not found.")
                return False
            
            # Print device information
            try:
                manufacturer = usb.util.get_string(self.device, self.device.iManufacturer)
                product = usb.util.get_string(self.device, self.device.iProduct)
                print(f"Connected device: {manufacturer} - {product}")
            except:
                print(f"Connected device: {self.device.idVendor:04x}:{self.device.idProduct:04x}")
            
            # Initialize OpenCV VideoCapture
            self.cap = cv2.VideoCapture(self.video_device_index)
            if not self.cap.isOpened():
                print(f"Cannot open video device {self.video_device_index}.")
                return False
            
            # Video settings
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize buffer size
            
            self.is_connected = True
            print("Microscope connected successfully!")
            return True
            
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the microscope."""
        if self.cap:
            self.cap.release()
            self.cap = None
        
        if self.device:
            try:
                usb.util.dispose_resources(self.device)
            except Exception as e:
                print(f"Error releasing USB resources: {e}")
        
        self.is_connected = False
        print("Microscope disconnected")
    
    def get_device_info(self) -> dict:
        """Return device information."""
        if not self.device:
            return {}
        
        info = {
            'vendor_id': f"0x{self.device.idVendor:04x}",
            'product_id': f"0x{self.device.idProduct:04x}",
            'bus': self.device.bus,
            'address': self.device.address,
            'class': self.device.bDeviceClass
        }
        
        try:
            info['manufacturer'] = usb.util.get_string(self.device, self.device.iManufacturer)
            info['product'] = usb.util.get_string(self.device, self.device.iProduct)
        except:
            info['manufacturer'] = "Unknown"
            info['product'] = "Unknown"
        
        return info
    
    def send_control_command(self, request: int, value: int = 0, index: int = 0, data: bytes = None) -> bool:
        """Send control command."""
        if not self.is_connected:
            print("Device not connected.")
            return False
        
        try:
            if data:
                result = self.device.ctrl_transfer(
                    bmRequestType=0x40,  # Host to device, vendor specific
                    bRequest=request,
                    wValue=value,
                    wIndex=index,
                    data_or_wLength=data
                )
            else:
                result = self.device.ctrl_transfer(
                    bmRequestType=0xC0,  # Device to host, vendor specific
                    bRequest=request,
                    wValue=value,
                    wIndex=index,
                    data_or_wLength=64
                )
            return True
        except Exception as e:
            print(f"Control command failed: {e}")
            return False
    
    def set_led_brightness(self, brightness: int) -> bool:
        """Set LED brightness (0-255)."""
        if not 0 <= brightness <= 255:
            print("Brightness must be in range 0-255.")
            return False
        
        if not self.cap:
            print("Microscope not connected.")
            return False
        
        # For UVC microscopes, try brightness adjustment through OpenCV
        try:
            # Set brightness (convert to 0.0 ~ 1.0 range)
            brightness_normalized = brightness / 255.0
            success = self.cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness_normalized)
            if success:
                print(f"LED brightness set: {brightness}")
                return True
            else:
                print("Brightness setting failed - manual adjustment may be required")
                return False
        except Exception as e:
            print(f"Error setting brightness: {e}")
            return False
    
    def capture_frame(self) -> Optional[np.ndarray]:
        """Capture a frame."""
        if not self.is_connected or not self.cap:
            print("Microscope not connected.")
            return None
        
        try:
            ret, frame = self.cap.read()
            if ret:
                return frame
            else:
                print("Frame capture failed")
                return None
        except Exception as e:
            print(f"Error capturing frame: {e}")
            return None
    
    def start_video_stream(self):
        """Start video stream."""
        if not self.is_connected:
            print("Microscope not connected.")
            return False
        
        print("Starting video stream...")
        return True
    
    def stop_video_stream(self):
        """Stop video stream."""
        print("Stopping video stream...")
        return True
    
    def get_frame_size(self) -> Tuple[int, int]:
        """Return current frame size."""
        if self.cap:
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            return (width, height)
        return (640, 480)
    
    def set_frame_size(self, width: int, height: int) -> bool:
        """Set frame size."""
        if not self.cap:
            return False
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        return True

def main():
    """Main function - basic test"""
    print("USB Microscope Driver Test")
    print("-" * 40)
    
    # Initialize driver
    driver = MicroscopeDriver()
    
    # Attempt connection
    if not driver.connect():
        print("Failed to connect to microscope.")
        sys.exit(1)
    
    # Print device information
    info = driver.get_device_info()
    print("Device Information:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # Basic test
    try:
        print("\nBasic functionality test...")
        driver.set_led_brightness(128)
        driver.start_video_stream()
        
        print("Waiting 5 seconds...")
        time.sleep(5)
        
        driver.stop_video_stream()
        
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    
    finally:
        driver.disconnect()

if __name__ == "__main__":
    main()