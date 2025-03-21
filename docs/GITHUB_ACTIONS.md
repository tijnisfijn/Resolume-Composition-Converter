# GitHub Actions Workflow for Windows Builds

This document explains how the GitHub Actions workflow is set up to automate the Windows build process for the Resolume Composition Converter application.

## Overview

The GitHub Actions workflow automates the process of building the Windows version of the application. This eliminates the need for Windows users to manually build the application from source, making it easier to distribute and test the application on Windows.

## Workflow File

The workflow is defined in `.github/workflows/build-windows.yml` and includes the following key components:

### Triggers

The workflow runs automatically when:
- Code is pushed to the `main` branch
- A pull request is created targeting the `main` branch
- Manually triggered using the "Run workflow" button in the GitHub Actions UI

```yaml
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  # Allow manual triggering
  workflow_dispatch:
```

### Environment

The workflow runs on a Windows environment:

```yaml
jobs:
  build:
    runs-on: windows-latest
```

### Steps

1. **Checkout Repository**: Fetches the latest code from the repository
2. **Set up Python**: Installs Python 3.10 and configures pip caching
3. **Create Virtual Environment**: Sets up a Python virtual environment
4. **Install Dependencies**: Installs required packages from requirements.txt and Pillow
5. **Run Windows Build Script**: Executes the build_windows.py script
6. **Upload Artifacts**: Uploads the built application and ZIP file as artifacts

## Accessing Build Artifacts

After the workflow completes successfully, you can access the build artifacts:

1. Go to the [Actions tab](https://github.com/tijnisfijn/Resolume-Composition-Converter/actions/workflows/build-windows.yml)
2. Click on the most recent successful workflow run
3. Scroll down to the "Artifacts" section
4. Download the desired artifact:
   - "Resolume-Composition-Converter-Windows" - Full build output
   - "Resolume-Composition-Converter-Windows-ZIP" - Packaged ZIP file

## Customizing the Workflow

If you need to modify the workflow, here are some common changes you might want to make:

### Changing the Python Version

To use a different Python version, modify the `python-version` parameter:

```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'  # Change to desired version
    cache: 'pip'
```

### Adding Additional Dependencies

If you need to install additional dependencies, add them to the "Install dependencies" step:

```yaml
- name: Install dependencies
  run: |
    .\venv\Scripts\activate
    pip install -r requirements.txt
    pip install Pillow
    pip install your-additional-package  # Add your package here
```

### Modifying Build Parameters

If you need to pass additional parameters to the build script, modify the "Run Windows build script" step:

```yaml
- name: Run Windows build script
  run: |
    .\venv\Scripts\activate
    python build/windows/build_windows.py --your-parameter value  # Add parameters here
```

## Troubleshooting

If the workflow fails, check the following:

1. **Dependencies**: Ensure all required dependencies are listed in requirements.txt
2. **Build Script**: Verify that build/windows/build_windows.py works correctly locally
3. **File Paths**: Check that all file paths in the workflow and build script are correct
4. **Python Version**: Make sure the application is compatible with the Python version used in the workflow

## Future Improvements

Potential improvements to the workflow:

1. **Release Integration**: Automatically create GitHub releases with the built artifacts
2. **Version Tagging**: Automatically update version numbers and create tags
3. **Cross-Platform Builds**: Add macOS and Linux build jobs
4. **Testing**: Add automated testing before building
5. **Code Signing**: Implement code signing for the Windows executable