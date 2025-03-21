#!/usr/bin/env python3
"""
Build script for Windows
"""

import os
import sys
import subprocess
import shutil

def main():
    """Main function"""
    print("Building Resolume Composition Converter for Windows...")
    
    # Get the repository root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Script directory: {script_dir}")
    
    # Try to find the repository root directory
    repo_root = os.path.abspath(os.path.join(script_dir, "../.."))
    print(f"Repository root directory: {repo_root}")
    
    # Check if resolume_gui.py exists in the src directory
    if os.path.exists(os.path.join(repo_root, "src", "resolume_gui.py")):
        print(f"Found resolume_gui.py in src directory")
    else:
        print(f"Warning: resolume_gui.py not found in {os.path.join(repo_root, 'src')}")
        
        # Try to find resolume_gui.py in various locations
        possible_locations = [
            # Current directory
            os.getcwd(),
            # Parent directory (for nested extractions)
            os.path.dirname(os.getcwd()),
            # Explicit path based on extraction pattern
            os.path.dirname(os.path.dirname(os.getcwd())),
            # src directory
            os.path.join(repo_root, "src")
        ]
        
        for location in possible_locations:
            test_path = os.path.join(location, "resolume_gui.py")
            print(f"Testing path: {test_path}")
            if os.path.exists(test_path):
                repo_root = os.path.dirname(location) if "src" in location else location
                print(f"Found resolume_gui.py at: {test_path}")
                break
    
    # Change to the repository root directory
    print(f"Changing to repository root directory: {repo_root}")
    os.chdir(repo_root)
    
    # Verify that we're in the correct directory
    print(f"Current working directory: {os.getcwd()}")
    print(f"Files in current directory: {os.listdir('.')}")
    
    # Check if resolume_gui.py exists in the src directory
    if os.path.exists(os.path.join(repo_root, "src", "resolume_gui.py")):
        print("Found resolume_gui.py in src directory")
    else:
        print("ERROR: resolume_gui.py not found in the src directory.")
        print("Please make sure you're in the correct directory and try again.")
        return 1
    
    # Activate virtual environment if not already activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Warning: Virtual environment not activated. It's recommended to run this script in a virtual environment.")
    
    # Install requirements
    print("\nInstalling requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    # Install Pillow for icon creation
    print("\nInstalling Pillow for icon creation...")
    subprocess.run([sys.executable, "-m", "pip", "install", "Pillow"], check=True)
    
    # Create Windows icon
    print("\nCreating Windows icon...")
    subprocess.run([sys.executable, "build/windows/create_windows_icon.py"], check=True)
    
    # Build the application
    print("\nBuilding application with PyInstaller...")
    subprocess.run([sys.executable, "-m", "PyInstaller", "build/windows/resolume_converter_windows.spec"], check=True)
    
    # Create HTML documentation
    print("\nCreating HTML documentation...")
    subprocess.run([sys.executable, os.path.join(repo_root, "src/convert_manual_simple.py")], check=True)
    
    # Create distribution package
    print("\nCreating distribution package...")
    subprocess.run([sys.executable, os.path.join(repo_root, "scripts/create_distribution.py")], check=True)
    
    # Move the built application to the dist/windows directory
    if os.path.exists("dist/Resolume Composition Converter"):
        if os.path.exists("dist/windows/Resolume Composition Converter"):
            shutil.rmtree("dist/windows/Resolume Composition Converter")
        shutil.move("dist/Resolume Composition Converter", "dist/windows/")
        print("\nMoved built application to dist/windows/")
    
    if os.path.exists("Resolume Composition Converter.zip"):
        if os.path.exists("dist/windows/Resolume Composition Converter.zip"):
            os.remove("dist/windows/Resolume Composition Converter.zip")
        shutil.move("Resolume Composition Converter.zip", "dist/windows/")
        print("Moved ZIP archive to dist/windows/")
    
    print("\nBuild completed successfully!")
    print("You can find the application in the 'dist/windows/Resolume Composition Converter' folder")
    print("or in the 'dist/windows/Resolume Composition Converter.zip' archive.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
