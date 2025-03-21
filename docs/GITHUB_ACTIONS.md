# GitHub Actions Workflow for Windows Builds

This document explains how the GitHub Actions workflow is set up to automate the Windows build process for the Resolume Composition Converter application.

## Overview

The GitHub Actions workflow automates the process of building the Windows version of the application. This eliminates the need for Windows users to manually build the application from source, making it easier to distribute and test the application on Windows.

## Workflow File

The workflow is defined in `.github/workflows/build-windows.yml` and includes the following key components:

### Triggers

The workflow runs automatically when:
- Code is pushed to the `main` branch
- A tag is pushed (e.g., v1.1.2, v1.1.3)
- A pull request is created targeting the `main` branch
- Manually triggered using the "Run workflow" button in the GitHub Actions UI

```yaml
on:
  push:
    branches:
      - main
    tags:
      - 'v*'  # Run on tag pushes too
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

1. **Checkout Repository**: Fetches the latest code from the repository, including submodules
2. **Set up Python**: Installs Python 3.10 and configures pip
3. **Enable Debug Logging**: Enables detailed debug logging for troubleshooting
4. **Install Dependencies**: Installs required packages from requirements.txt and Pillow
5. **Run Windows Build Script**: Executes the build_windows.py script
6. **List Build Output**: Lists the files in the build output directory
7. **Create ZIP Archive**: Creates a ZIP archive of the build output
8. **Upload Artifact**: Uploads the ZIP archive as a workflow artifact (using v3 of the action)
9. **Create GitHub Release** (for tagged commits): Creates a GitHub Release with the built application

## Downloading the Built Application

The workflow makes the built application available for download in two ways:

### 1. GitHub Releases (for tagged commits)

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

### 2. Workflow Artifacts (for all commits)

For all commits (including those without tags), the workflow will upload the built application as a workflow artifact:

1. Go to the Actions tab in your repository
2. Click on the workflow run
3. Scroll down to the Artifacts section
4. Download the "Resolume-Composition-Converter-Windows" artifact

## Action Versions

The workflow uses specific versions of GitHub Actions:

- `actions/checkout@v2` - For checking out the repository
- `actions/setup-python@v2` - For setting up Python
- `actions/upload-artifact@v3` - For uploading build artifacts
- `softprops/action-gh-release@v1` - For creating GitHub Releases

## Troubleshooting

If the workflow fails, check the following:

1. **Submodule Issues**: Ensure that the submodules are properly configured
2. **Dependencies**: Ensure all required dependencies are listed in requirements.txt
3. **Build Script**: Verify that build/windows/build_windows.py works correctly locally
4. **File Paths**: Check that all file paths in the workflow and build script are correct
5. **Python Version**: Make sure the application is compatible with the Python version used in the workflow
6. **Debug Logs**: Check the debug logs for detailed information about the workflow execution

## Future Improvements

Potential improvements to the workflow:

1. **Code Signing**: Implement code signing for the Windows executable
2. **Automated Testing**: Add automated tests to verify the built application works correctly
3. **Cross-Platform Builds**: Add macOS and Linux build jobs
4. **Version Tagging**: Automatically update version numbers and create tags
5. **Release Notes**: Automatically generate release notes from commit messages