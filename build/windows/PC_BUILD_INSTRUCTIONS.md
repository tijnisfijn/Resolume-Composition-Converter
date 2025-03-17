# Windows Build Instructions for Resolume Composition Converter

## Important Note About File Structure

When you extract the ZIP file, you'll get a folder called "Resolume Composition Converter - Source". **All the necessary files are inside this folder**, including:
- `resolume_converter_windows.spec`
- `build_windows.py`
- `create_windows_icon.py`
- And other required files

## Step-by-Step Instructions

1. **Download** the "Resolume Composition Converter - PC Source.zip" file from the GitHub release page.

2. **Extract** the ZIP file to a location of your choice.

3. **Navigate** to the extracted "Resolume Composition Converter - Source" folder:
   ```
   cd "Resolume Composition Converter - Source"
   ```

4. **Create and activate** a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

5. **Run** the build script:
   ```
   python build_windows.py
   ```

## Troubleshooting

If you get an error like "Spec file 'resolume_converter_windows.spec' not found", it means you're running the build script from the wrong directory. Make sure you're in the "Resolume Composition Converter - Source" folder when you run the build script.

## What the Build Script Does

The build script will:
1. Install the required dependencies
2. Install Pillow for icon creation
3. Create a Windows icon (.ico) file from the PNG icon
4. Build the application using PyInstaller with the correct spec file
5. Create HTML documentation
6. Create a distribution package

After the build is complete, you'll find the application in the "Resolume Composition Converter" folder.