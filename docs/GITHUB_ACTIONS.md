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
    branches: [ main ]
  pull_request:
    branches: [ main ]
  # Allow manual triggering
  workflow_dispatch:
```

### Permissions

The workflow specifies required permissions:

```yaml
permissions:
  contents: read
  packages: read
  # Add other permissions as needed
```

### Environment

The workflow runs on a Windows environment with CMD shell:

```yaml
jobs:
  build:
    runs-on: windows-latest
    
    defaults:
      run:
        shell: cmd
```

### Steps

1. **Checkout Repository**: Fetches the latest code from the repository
2. **Set up Python**: Installs Python 3.10 and configures pip caching
3. **Create Virtual Environment**: Sets up a Python virtual environment
4. **Install Dependencies**: Installs required packages from requirements.txt and Pillow
5. **Run Windows Build Script**: Executes the build_windows.py script
6. **Test Application**: Performs basic smoke tests on the built application
   - Verifies the executable exists without attempting to run it
   - Lists directory contents for verification
7. **Check Test Data Files**: Checks if test data files exist without attempting to run conversion
   - This test is non-blocking (workflow continues even if it fails)
8. **List Build Output**: Lists the files in the build output directory
9. **Create ZIP Archive**: Creates a ZIP archive of the build output for release
10. **Create GitHub Release** (for tagged commits): Creates a GitHub Release with the built application
11. **Upload as Workflow Artifact** (for non-tagged commits): Attempts to upload the build as a workflow artifact
12. **Build Completion Message**: Displays a message indicating the build completed successfully
## Downloading the Built Application

The workflow makes the built application available for download in two ways:

### 1. GitHub Releases (Recommended)

When you create and push a tag, the workflow will automatically create a GitHub Release with the built application:

```bash
# Create a tag
git tag v1.1.3

# Push the tag to GitHub
git push origin v1.1.3
```

After pushing a tag, the workflow will:
1. Build the application
2. Create a ZIP archive of the build output
3. Create a GitHub Release with the tag name
4. Upload the ZIP archive to the release

You can then download the built application from the Releases page on GitHub.

### 2. Workflow Artifacts (Fallback)

For regular commits that don't have tags, the workflow will attempt to upload the build as a workflow artifact. However, this method may not work reliably due to compatibility issues with the upload-artifact action.

If it works, you can access the artifact by:
1. Going to the Actions tab in your repository
2. Clicking on the workflow run
3. Scrolling down to the Artifacts section
4. Downloading the "windows-build" artifact
5. Extract the ZIP file to access the application

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

### Action Versions

The workflow uses specific versions of GitHub Actions:

- `actions/checkout@v3` - For checking out the repository
- `actions/setup-python@v4` - For setting up Python

Note: We previously attempted to use `actions/upload-artifact` (v1, v2, and v3) but encountered compatibility issues. The artifact upload functionality has been temporarily disabled.

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

## Automated Testing

The workflow includes automated testing steps to verify that the built application works correctly:

### Basic Smoke Test

This test verifies that the application executable exists and can be launched:

```yaml
- name: Test application (Basic smoke test)
  run: |
    echo "Running basic smoke test on the built application..."
    if exist "dist\windows\Resolume Composition Converter\Resolume Composition Converter.exe" (
      echo "Application executable exists. Testing with --version parameter..."
      dist\windows\Resolume Composition Converter\Resolume Composition Converter.exe --version
      if %ERRORLEVEL% EQU 0 (
        echo "Application started successfully!"
      ) else (
        echo "Application failed to start with error code %ERRORLEVEL%"
        exit /b 1
      )
    ) else (
      echo "Application executable not found!"
      exit /b 1
    )
```

### File Conversion Test

This test attempts to convert a sample file using command-line parameters:

```yaml
- name: Test file conversion (if test files exist)
  run: |
    echo "Testing file conversion functionality..."
    if exist "test-data\UpscaleComp.avc" (
      if exist "dist\windows\Resolume Composition Converter\Resolume Composition Converter.exe" (
        echo "Running conversion test with sample file..."
        dist\windows\Resolume Composition Converter\Resolume Composition Converter.exe --cli --input "test-data\UpscaleComp.avc" --output "test-data\UpscaleComp_test_output.avc" --width 1920 --height 1080
        if %ERRORLEVEL% EQU 0 (
          echo "Conversion test passed!"
        ) else (
          echo "Conversion test failed with error code %ERRORLEVEL%"
          echo "This is a non-blocking test, continuing workflow..."
        )
      )
    ) else (
      echo "Test data file not found, skipping conversion test."
    )
  continue-on-error: true
```

Note: The file conversion test is configured with `continue-on-error: true`, which means the workflow will continue even if this test fails. This is useful for non-critical tests that shouldn't block the build process.

## Troubleshooting

If the workflow fails, check the following:

1. **Dependencies**: Ensure all required dependencies are listed in requirements.txt
2. **Build Script**: Verify that build/windows/build_windows.py works correctly locally
3. **File Paths**: Check that all file paths in the workflow and build script are correct
4. **Python Version**: Make sure the application is compatible with the Python version used in the workflow
5. **Command-Line Arguments**: If the tests are failing, check if the application supports the command-line arguments used in the tests

## Future Improvements

Potential improvements to the workflow:

1. **Release Integration**: Automatically create GitHub releases with the built artifacts
2. **Version Tagging**: Automatically update version numbers and create tags
3. **Cross-Platform Builds**: Add macOS and Linux build jobs
4. **Enhanced Testing**:
   - Add more comprehensive automated tests
   - Implement UI testing with tools like PyAutoGUI or Selenium
   - Add unit tests for core functionality
   - Create a test matrix for different Windows versions
5. **Code Signing**: Implement code signing for the Windows executable
6. **Test Reporting**: Generate and publish test reports
7. **Code Coverage**: Add code coverage reporting for tests
8. **Performance Testing**: Add performance benchmarks to ensure the application meets performance requirements