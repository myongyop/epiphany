#!/usr/bin/env python3
"""
Display captured microscope images as ASCII art
"""

import cv2
import numpy as np

def image_to_ascii(image_path, width=80, height=60):
    """Convert image to ASCII art"""
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Cannot read image: {image_path}")
        return
    
    print(f"Original image size: {img.shape[1]}x{img.shape[0]}")
    print(f"Image type: {img.dtype}")
    print(f"Pixel value range: {img.min()} ~ {img.max()}")
    
    # Resize image
    resized = cv2.resize(img, (width, height))
    
    # Convert to grayscale
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    
    # ASCII character set (from dark to bright)
    ascii_chars = " .:-=+*#%@"
    
    print(f"\nMicroscope image ASCII preview ({width}x{height}):")
    print("=" * width)
    
    # Convert each pixel to ASCII character
    for row in gray:
        line = ""
        for pixel in row:
            # Convert pixel value to ASCII character index
            char_index = min(len(ascii_chars) - 1, int(pixel) * len(ascii_chars) // 256)
            line += ascii_chars[char_index]
        print(line)
    
    print("=" * width)
    
    # Image statistics
    print(f"\nImage statistics:")
    print(f"Average brightness: {gray.mean():.1f}")
    print(f"Standard deviation: {gray.std():.1f}")
    print(f"Minimum value: {gray.min()}")
    print(f"Maximum value: {gray.max()}")

def main():
    print("=== Microscope Image ASCII Viewer ===")
    image_path = "microscope_capture.jpg"
    
    # Display as ASCII art
    image_to_ascii(image_path, width=100, height=75)
    
    print(f"\nOriginal image file: {image_path}")
    print("To view the image, open it with an image viewer!")

if __name__ == "__main__":
    main()