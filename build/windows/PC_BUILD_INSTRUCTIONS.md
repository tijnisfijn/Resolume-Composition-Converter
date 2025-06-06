# Windows Build Instructions for Resolume Composition Converter

> **Note:** As an alternative to building manually, you can now download pre-built Windows versions from GitHub Actions. See the [Automated Builds](#automated-builds) section below.

## Repository Structure

The source package has the following structure:
- `/` - Core application files
- `/build/mac/` - Mac-specific build files
- `/build/windows/` - Windows-specific build files
- `/dist/mac/` - Output directory for Mac builds
- `/dist/windows/` - Output directory for Windows builds
- `/screenshots/` - Application screenshots
- `/.github/workflows/` - GitHub Actions workflow files

## Step-by-Step Instructions

1. **Download** the "Resolume-Composition-Converter-Source.zip" file from the GitHub release page.

2. **Extract** the ZIP file to a location of your choice.
   - **IMPORTANT**: Make sure to extract directly to a folder, not to a nested directory.
   - For example, extract to `D:\Downloads\Resolume-Composition-Converter-Source\`
   - NOT to `D:\Downloads\Resolume-Composition-Converter-Source\Resolume-Composition-Converter-Source\`

3. **Navigate** to the extracted folder:
   ```
   cd "Resolume-Composition-Converter-Source"
   ```
   - Verify that you can see the `src` directory containing `resolume_gui.py`.
   - If you see another folder named "Resolume-Composition-Converter-Source" inside, navigate into that folder.

4. **Create and activate** a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

5. **Install dependencies**:
   ```
   pip install -r requirements.txt
   pip install Pillow
   ```

6. **Run** the build script:
   ```
   python build/windows/build_windows.py
   ```

## Troubleshooting

### Common Issues

1. **"script 'path\to\resolume_gui.py' not found" error**:
   - This usually happens when the source package is extracted to a nested directory
   - Make sure you're in the correct directory where the `src` folder is located
   - Run `dir src` to verify that `resolume_gui.py` is in the src directory
   - If you don't see `resolume_gui.py` in the src directory, navigate to the correct directory

2. **"Spec file not found" error**:
   - Make sure you're in the root directory of the extracted source package
   - Verify that the file `build/windows/resolume_converter_windows.spec` exists

3. **"No module named 'PIL'" error**:
   - Make sure you've installed Pillow: `pip install Pillow`

4. **"No module named 'PyInstaller'" error**:
   - Make sure you've installed the requirements: `pip install -r requirements.txt`

5. **Icon creation fails**:
   - Verify that the `icons/app_icon.png` file exists
   - Make sure Pillow is installed: `pip install Pillow`
   
6. **Nested directory issues**:
   - If you extracted the ZIP file and see a nested directory structure like:
     ```
     D:\Downloads\Resolume-Composition-Converter-Source\Resolume-Composition-Converter-Source\
     ```
   - Navigate to the innermost directory where `resolume_gui.py` is located
   - Or re-extract the ZIP file directly to a non-nested location

### Checking File Structure

If you're having issues, verify that your directory structure looks like this:
```
Resolume-Composition-Converter-Source/
├── build/
│   ├── mac/
│   │   ├── build_mac.py
│   │   └── resolume_converter.spec
│   └── windows/
│       ├── build_windows.py
│       ├── create_windows_icon.py
│       ├── PC_BUILD_INSTRUCTIONS.md
│       └── resolume_converter_windows.spec
├── dist/
│   ├── mac/
│   └── windows/
├── screenshots/
├── src/
│   ├── resolume_gui.py
│   ├── runtime_hook.py
│   ├── convert_manual_simple.py
│   ├── update_checker.py
│   └── version.py
├── scripts/
│   └── create_distribution.py
├── requirements.txt
└── other files...
```

## What the Build Script Does

The build script will:
1. Install the required dependencies
2. Install Pillow for icon creation
3. Create a Windows icon (.ico) file from the PNG icon
4. Build the application using PyInstaller with the correct spec file
5. Create HTML documentation
6. Create a distribution package

After the build is complete, you'll find the application in the `dist/windows/Resolume Composition Converter` folder.

## Automated Builds

### Using GitHub Actions (Recommended)

Instead of building manually, you can download pre-built Windows versions from GitHub Actions:

1. Go to the [Actions tab](https://github.com/tijnisfijn/Resolume-Composition-Converter/actions/workflows/build-windows.yml) in the GitHub repository
2. Click on the most recent successful workflow run
3. Scroll down to the "Artifacts" section
4. Download the "Resolume-Composition-Converter-Windows-ZIP" artifact
5. Extract the ZIP file to your desired location

This method is recommended for most users as it:
- Eliminates the need to set up a development environment
- Ensures consistent builds across different systems
- Saves time and reduces potential build errors
- Provides access to the latest builds automatically

For more information about the GitHub Actions workflow, see [GITHUB_ACTIONS.md](../../docs/GITHUB_ACTIONS.md).
