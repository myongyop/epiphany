#!/usr/bin/env python3
"""
USB Device Scanner
Tool to scan connected USB devices and find microscopes
"""

import usb.core
import usb.util
import sys

def scan_usb_devices():
    """Scan all connected USB devices."""
    print("Scanning connected USB devices...")
    print("-" * 60)
    
    devices = usb.core.find(find_all=True)
    
    for device in devices:
        try:
            print(f"Device found:")
            print(f"  Vendor ID:  0x{device.idVendor:04x}")
            print(f"  Product ID: 0x{device.idProduct:04x}")
            
            # Try to get manufacturer and product name
            try:
                manufacturer = usb.util.get_string(device, device.iManufacturer)
                product = usb.util.get_string(device, device.iProduct)
                print(f"  Manufacturer: {manufacturer}")
                print(f"  Product:      {product}")
            except:
                print(f"  Manufacturer: (Unknown)")
                print(f"  Product:      (Unknown)")
            
            print(f"  Bus:        {device.bus}")
            print(f"  Address:    {device.address}")
            print(f"  Class:      {device.bDeviceClass}")
            print("-" * 60)
            
        except Exception as e:
            print(f"Failed to read device info: {e}")
            print("-" * 60)

def find_microscope_candidates():
    """Find devices that are likely to be microscopes."""
    print("\nSearching for microscope candidate devices...")
    
    devices = usb.core.find(find_all=True)
    candidates = []
    
    for device in devices:
        try:
            # Look for video class devices or vendor specific devices
            if (device.bDeviceClass == 14 or  # Video class
                device.bDeviceClass == 0xFF or  # Vendor specific
                device.bDeviceClass == 0):      # Interface specific
                
                try:
                    manufacturer = usb.util.get_string(device, device.iManufacturer) or "Unknown"
                    product = usb.util.get_string(device, device.iProduct) or "Unknown"
                except:
                    manufacturer = "Unknown"
                    product = "Unknown"
                
                # Search for microscope-related keywords
                keywords = ['microscope', 'camera', 'video', 'usb', 'digital']
                if any(keyword in (manufacturer + product).lower() for keyword in keywords):
                    candidates.append({
                        'vendor_id': device.idVendor,
                        'product_id': device.idProduct,
                        'manufacturer': manufacturer,
                        'product': product,
                        'class': device.bDeviceClass
                    })
        except:
            continue
    
    if candidates:
        print("Microscope candidate devices:")
        for i, candidate in enumerate(candidates, 1):
            print(f"{i}. {candidate['manufacturer']} - {candidate['product']}")
            print(f"   ID: {candidate['vendor_id']:04x}:{candidate['product_id']:04x}")
    else:
        print("No microscope candidates found.")
        print("Please check devices manually.")

def main():
    try:
        scan_usb_devices()
        find_microscope_candidates()
    except PermissionError:
        print("Error: No permission to access USB devices.")
        print("Run with: sudo python3 usb_scanner.py")
        sys.exit(1)
    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()