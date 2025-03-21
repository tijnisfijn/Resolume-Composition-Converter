# GitHub Actions Workflow for Windows Builds

This document explains how the GitHub Actions workflow is set up to create releases for the Resolume Composition Converter application.

## Overview

Due to compatibility issues with GitHub Actions and the repository structure, we've implemented a simplified workflow that creates placeholder releases instead of attempting to build the application directly on GitHub's infrastructure.

## Workflow File

The workflow is defined in `.github/workflows/build-windows.yml` and includes the following key components:

### Triggers

The workflow runs automatically when:
- A tag is pushed (e.g., v1.1.2, v1.1.3)
- Manually triggered using the "Run workflow" button in the GitHub Actions UI

```yaml
on:
  push:
    tags:
      - 'v*'  # Run only on tag pushes
  # Allow manual triggering
  workflow_dispatch:
```

### Permissions

The workflow specifies required permissions:

```yaml
permissions:
  contents: write  # Needed for creating releases
  packages: read
```

### Environment

The workflow runs on a Windows environment:

```yaml
jobs:
  build:
    runs-on: windows-latest
```

### Steps

1. **Create GitHub Release**: Creates a placeholder GitHub Release for the tag
2. **Build Completion Message**: Displays a message indicating the release was created successfully

## Downloading the Application

### Building Locally (Recommended)

The recommended approach is to build the application locally using the instructions in the README and build documentation:

1. Clone the repository
2. Follow the build instructions in `build/windows/PC_BUILD_INSTRUCTIONS.md`

### GitHub Releases

When you create and push a tag, the workflow will automatically create a placeholder GitHub Release:

```bash
# Create a tag
git tag v1.1.3

# Push the tag to GitHub
git push origin v1.1.3
```

After pushing a tag, the workflow will create a GitHub Release with the tag name, but it will not contain the actual built application due to GitHub Actions limitations.

## Troubleshooting

If the workflow fails, check the following:

1. **Git Issues**: The repository contains submodules that can cause issues with GitHub Actions
2. **Permissions**: Ensure the workflow has the correct permissions to create releases
3. **Tag Format**: Make sure tags follow the format `v*` (e.g., v1.1.2, v1.1.3)

## Future Improvements

Potential improvements to the workflow:

1. **Self-Hosted Runner**: Set up a self-hosted runner that can handle the repository structure
2. **Alternative CI/CD**: Explore alternative CI/CD platforms that might work better with the repository
3. **Repository Restructuring**: Consider restructuring the repository to be more compatible with GitHub Actions