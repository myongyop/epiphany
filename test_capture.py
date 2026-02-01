#!/usr/bin/env python3
"""
Microscope image capture test
"""

import sys
import os
import cv2

# Import driver module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from driver.microscope_driver import MicroscopeDriver

def main():
    print("=== Microscope Image Capture Test ===")
    
    # Initialize and connect driver
    driver = MicroscopeDriver()
    
    if not driver.connect():
        print("Microscope connection failed")
        return
    
    print("Microscope connected successfully!")
    
    # Capture frame
    print("Capturing image...")
    frame = driver.capture_frame()
    
    if frame is not None:
        print(f"Capture successful! Image size: {frame.shape}")
        
        # Save image
        filename = "microscope_capture.jpg"
        cv2.imwrite(filename, frame)
        print(f"Image saved: {filename}")
        
        # Print image information
        print(f"Image type: {frame.dtype}")
        print(f"Image range: {frame.min()} ~ {frame.max()}")
        
        # Image preview (small version as ASCII art)
        small_frame = cv2.resize(frame, (80, 60))
        gray_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
        
        print("\nMicroscope image preview (ASCII):")
        ascii_chars = " .:-=+*#%@"
        for row in gray_small[::2]:  # Every 2 rows
            line = ""
            for pixel in row[::2]:  # Every 2 pixels
                char_index = min(len(ascii_chars) - 1, int(pixel) * len(ascii_chars) // 256)
                line += ascii_chars[char_index]
            print(line)
    else:
        print("Image capture failed")
    
    # Disconnect
    driver.disconnect()

if __name__ == "__main__":
    main()