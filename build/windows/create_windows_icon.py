#!/usr/bin/env python3
"""
Script to create a Windows icon (.ico) file from a PNG image
"""

import os
import sys
from PIL import Image

def create_windows_icon():
    """Create a Windows icon (.ico) file from a PNG image"""
    print("Creating Windows icon...")
    
    # Get the repository root directory
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    
    # Change to the repository root directory
    os.chdir(repo_root)
    
    # Check if the PNG file exists
    png_path = "icons/app_icon.png"
    if not os.path.exists(png_path):
        print(f"Error: PNG file not found at {png_path}")
        return False
    
    # Create the ICO file
    ico_path = "icons/app_icon.ico"
    try:
        # Open the PNG image
        img = Image.open(png_path)
        
        # Create a list of sizes for the ICO file
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        
        # Create a list of images with different sizes
        img_list = []
        for size in sizes:
            resized_img = img.resize(size, Image.Resampling.LANCZOS)
            img_list.append(resized_img)
        
        # Save as ICO
        img_list[0].save(ico_path, format='ICO', sizes=[(img.width, img.height) for img in img_list])
        
        print(f"Windows icon created successfully: {ico_path}")
        return True
    except Exception as e:
        print(f"Error creating Windows icon: {e}")
        return False

def main():
    """Main function"""
    create_windows_icon()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())