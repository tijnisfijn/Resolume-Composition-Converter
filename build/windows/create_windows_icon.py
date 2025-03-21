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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Script directory: {script_dir}")
    
    # Try to find the repository root directory
    repo_root = os.path.abspath(os.path.join(script_dir, "../.."))
    print(f"Repository root directory: {repo_root}")
    
    # Check if icons/app_icon.png exists in the repository root directory
    png_path = os.path.join(repo_root, "icons", "app_icon.png")
    if not os.path.exists(png_path):
        print(f"Warning: PNG file not found at {png_path}")
        
        # Try to find icons/app_icon.png in various locations
        possible_locations = [
            # Current directory
            os.getcwd(),
            # Parent directory (for nested extractions)
            os.path.dirname(os.getcwd()),
            # Explicit path based on extraction pattern
            os.path.dirname(os.path.dirname(os.getcwd()))
        ]
        
        found = False
        for location in possible_locations:
            test_path = os.path.join(location, "icons", "app_icon.png")
            print(f"Testing path: {test_path}")
            if os.path.exists(test_path):
                repo_root = location
                png_path = test_path
                print(f"Found icons/app_icon.png at: {png_path}")
                found = True
                break
        
        if not found:
            print(f"Error: PNG file not found in any of the expected locations")
            return False
    
    # Change to the repository root directory
    print(f"Changing to repository root directory: {repo_root}")
    os.chdir(repo_root)
    
    # Verify that we're in the correct directory
    print(f"Current working directory: {os.getcwd()}")
    
    # Check if the PNG file exists in the current directory
    png_path = os.path.join("icons", "app_icon.png")
    if not os.path.exists(png_path):
        print(f"Error: PNG file not found at {png_path} after changing directory")
        return False
    
    # Create the ICO file
    ico_path = os.path.join("icons", "app_icon.ico")
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