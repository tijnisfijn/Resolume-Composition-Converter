# GitHub Repository Setup Guide

## Repository Description
```
A desktop application for converting Resolume Arena composition files (.avc) between different resolutions and frame rates. Automatically adjusts all parameters while preserving timing and composition names. Now with media format conversion: replace media files with different formats (e.g., .MP4 with .DXV) while keeping the same base filename.
```

## Repository Topics
Add these topics to make your repository more discoverable:
```
resolume, vj, video-art, composition, resolution, frame-rate, converter, desktop-application, macos, python, electron
```

## Steps to Create and Upload to GitHub

1. **Create a new GitHub repository**:
   - Go to [GitHub](https://github.com) and sign in
   - Click the "+" icon in the top right and select "New repository"
   - Enter a repository name (e.g., "resolume-composition-converter")
   - Paste the description provided above
   - Choose "Public" visibility
   - Check "Add a README file" (GitHub will use your existing README.md)
   - Check "Add .gitignore" and select "Python"
   - Check "Choose a license" and select "MIT License"
   - Click "Create repository"

2. **Upload your code**:
   ```bash
   # Initialize git in your project directory
   git init
   
   # Add all files
   git add .
   
   # Commit the files
   git commit -m "Initial commit"
   
   # Add the remote repository
   git remote add origin https://github.com/yourusername/resolume-composition-converter.git
   
   # Push to GitHub
   git push -u origin main
   ```

3. **Create a release**:
   - Go to your repository on GitHub
   - Click on "Releases" in the right sidebar
   - Click "Create a new release"
   - Enter a tag version (e.g., "v1.0.0")
   - Enter a release title (e.g., "Initial Release")
   - Add release notes describing the features
   - Upload the `Resolume Composition Converter.zip` file
   - Check "This is a pre-release" if it's not fully stable yet
   - Click "Publish release"

## Release Notes Template

```markdown
# Resolume Composition Converter v1.0.0

Initial release of the Resolume Composition Converter.

## Features

- Convert compositions between any resolution and frame rate
- Update file paths to media files in bulk
- Preserve custom durations and timing
- Automatically adjust transform effects
- Maintain composition names across conversions
- Simple, intuitive interface with dark mode
- Drag and drop support

## Installation

1. Download the ZIP file
2. Extract the contents
3. Drag the `Resolume Composition Converter.app` to your Applications folder
4. Right-click the app and select "Open" (required only the first time you run the app)

## Known Issues

- Windows and Linux builds are still in development
- Some complex effects may require manual adjustment after conversion

## Feedback

Please report any issues or suggestions in the GitHub Issues section.