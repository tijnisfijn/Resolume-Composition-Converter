# Recent Changes

This page documents the recent changes made to the Resolume Composition Converter project.

## Repository Structure Reorganization (March 2025)

We've completely reorganized the repository structure to make it cleaner, more maintainable, and easier for Windows users to build the application:

### 1. Created a Logical Directory Structure

The repository now has a clear, organized structure:
- `/` - Core application files
- `/build/mac/` - Mac-specific build files
- `/build/windows/` - Windows-specific build files
- `/dist/mac/` - Output directory for Mac builds
- `/dist/windows/` - Output directory for Windows builds

### 2. Eliminated Redundant Files and Folders

Removed over 800 redundant files, including:
- Duplicate source files in "Resolume Composition Converter - Source" folder
- Built application files in "Resolume Composition Converter" folder
- Redundant ZIP files
- Duplicate spec files and build scripts in the root directory

### 3. Updated Build Scripts for the New Structure

- Created `build/mac/build_mac.py` for macOS builds
- Updated `build/windows/build_windows.py` for Windows builds
- Both scripts now use the same core files but with platform-specific configurations

### 4. Fixed Windows Build Instructions

- Created detailed Windows build instructions in `build/windows/PC_BUILD_INSTRUCTIONS.md`
- Added clear troubleshooting steps for common issues
- Included a directory structure diagram to help users understand the organization

### 5. Updated Source Package Creation

- Modified `create_source_package.py` to create a package with the new directory structure
- Added Pillow to requirements.txt for icon creation
- Created a new source package with all necessary files

## Image Handling Fix (March 2025)

We've improved the image handling in the application:

- Fixed image handling to preserve aspect ratio for different image formats
- Added support for various image formats (.jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp)
- Square images now remain square, wide images remain wide, etc.
- Improved documentation with a new 'Image Files' section in the user manual

## Community Standards (March 2025)

We've added all the recommended GitHub community standards:

1. **Security Policy** (`SECURITY.md`)
   - Defined supported versions
   - Created a process for reporting vulnerabilities
   - Explained what reporters can expect after submitting a report

2. **Issue Templates** (`.github/ISSUE_TEMPLATE/`)
   - Created a bug report template with structured sections
   - Created a feature request template with sections for problem description, proposed solution, etc.

3. **Pull Request Template** (`.github/PULL_REQUEST_TEMPLATE.md`)
   - Added sections for description of changes, related issues, testing details, etc.