#!/usr/bin/env python3
"""
USB Microscope Basic Usage Example
"""

import sys
import os
import time

# Import driver module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from driver.microscope_driver import MicroscopeDriver

def main():
    """Basic usage example"""
    print("=== USB Microscope Basic Usage Example ===")
    
    # 1. Initialize driver
    print("\n1. Initializing driver...")
    driver = MicroscopeDriver()
    
    # 2. Connect to microscope
    print("2. Attempting to connect to microscope...")
    if not driver.connect():
        print("❌ Microscope not found.")
        print("💡 Tip: Make sure USB microscope is connected.")
        return
    
    print("✅ Microscope connected successfully!")
    
    # 3. Display device information
    print("\n3. Device Information:")
    info = driver.get_device_info()
    for key, value in info.items():
        print(f"   {key}: {value}")
    
    # 4. LED brightness control test
    print("\n4. LED brightness control test...")
    brightness_levels = [0, 64, 128, 192, 255]
    
    for brightness in brightness_levels:
        print(f"   Setting LED brightness to {brightness}...")
        driver.set_led_brightness(brightness)
        time.sleep(1)
    
    # 5. Video stream test
    print("\n5. Video stream test...")
    print("   Starting stream...")
    driver.start_video_stream()
    
    print("   Streaming for 5 seconds...")
    time.sleep(5)
    
    print("   Stopping stream...")
    driver.stop_video_stream()
    
    # 6. Frame capture test
    print("\n6. Frame capture test...")
    frame = driver.capture_frame()
    if frame is not None:
        print("   ✅ Frame capture successful!")
    else:
        print("   ⚠️  Frame capture failed (normal - not yet implemented)")
    
    # 7. Disconnect
    print("\n7. Disconnecting...")
    driver.disconnect()
    print("✅ Complete!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        sys.exit(1)