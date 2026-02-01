#!/usr/bin/env python3
"""
Microscope real-time capture and save
"""

import sys
import os
import cv2
import time
from datetime import datetime

# Import driver module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from driver.microscope_driver import MicroscopeDriver

def main():
    print("=== Microscope Real-time Capture ===")
    
    # Initialize and connect driver
    driver = MicroscopeDriver()
    
    if not driver.connect():
        print("Microscope connection failed")
        return
    
    print("Microscope connected successfully!")
    print("Commands:")
    print("  's' - Save screenshot")
    print("  'b' - Adjust brightness")
    print("  'q' - Quit")
    print("  Enter - Capture frame and display ASCII")
    
    frame_count = 0
    
    try:
        while True:
            # Wait for user input
            print(f"\n[Frame {frame_count}] Enter command (Enter/s/b/q): ", end="")
            command = input().strip().lower()
            
            if command == 'q':
                break
            elif command == 's':
                # Save screenshot
                frame = driver.capture_frame()
                if frame is not None:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"microscope_{timestamp}.jpg"
                    cv2.imwrite(filename, frame)
                    print(f"✅ Screenshot saved: {filename}")
                else:
                    print("❌ Frame capture failed")
            
            elif command == 'b':
                # Adjust brightness
                print("Enter brightness value (0-255): ", end="")
                try:
                    brightness = int(input())
                    if driver.set_led_brightness(brightness):
                        print(f"✅ Brightness set: {brightness}")
                    else:
                        print("❌ Brightness setting failed")
                except ValueError:
                    print("❌ Invalid value")
            
            else:
                # Capture frame and display ASCII
                frame = driver.capture_frame()
                if frame is not None:
                    print(f"✅ Frame capture successful! Size: {frame.shape}")
                    
                    # Small ASCII preview
                    small_frame = cv2.resize(frame, (60, 45))
                    gray_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
                    
                    print("\nMicroscope real-time preview:")
                    print("-" * 60)
                    ascii_chars = " .:-=+*#%@"
                    for row in gray_small[::2]:  # Every 2 rows
                        line = ""
                        for pixel in row[::2]:  # Every 2 pixels
                            char_index = min(len(ascii_chars) - 1, int(pixel) * len(ascii_chars) // 256)
                            line += ascii_chars[char_index]
                        print(line)
                    print("-" * 60)
                    
                    # Image statistics
                    print(f"Average brightness: {gray_small.mean():.1f}")
                    print(f"Pixel range: {frame.min()} ~ {frame.max()}")
                    
                else:
                    print("❌ Frame capture failed")
            
            frame_count += 1
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    
    finally:
        driver.disconnect()
        print("Microscope disconnected")

if __name__ == "__main__":
    main()