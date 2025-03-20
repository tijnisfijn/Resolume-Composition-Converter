# Resolume Composition Converter - User Manual

## Table of Contents

1. [Introduction](#introduction)
2. [Why Use This Tool?](#why-use-this-tool)
3. [Interface Overview](#interface-overview)
4. [File Organization](#file-organization)
5. [Common Use Cases](#common-use-cases)
6. [Converting a Composition](#converting-a-composition)
7. [Supported Clip Types](#supported-clip-types)
8. [Transform Effects](#transform-effects)
9. [Understanding File Paths](#understanding-file-paths)
10. [Best Practices](#best-practices)
11. [Troubleshooting](#troubleshooting)

## Introduction

Resolume Composition Converter is a specialized tool designed to help VJs and visual artists convert their Resolume Arena compositions from one resolution and frame rate to another. This is particularly useful when upgrading from HD (1080p) to 4K, or from 25/30fps to 60fps.

The application modifies the XML structure of your .avc files to adjust all relevant parameters, ensuring your composition looks and behaves correctly at the new resolution and frame rate. It also allows you to replace media files with different formats (e.g., .MP4 with .DXV) while keeping the same base filename.

## Why Use This Tool?

### The Challenge of Changing Resolutions and Formats

Visual artists, VJs, and AV professionals who use Resolume Arena often face a common challenge: adapting their carefully crafted compositions to different technical requirements. Whether it's upgrading to higher resolutions, changing frame rates, or switching media formats, these changes traditionally require painstaking manual work to rebuild compositions from scratch.

When you manually recreate a composition at a new resolution or with different media files, you lose hours of work:
- Recreating all clip placements and layer arrangements
- Rebuilding complex effect chains and parameter settings
- Reconstructing precise timing and transitions
- Reestablishing dashboard controls and MIDI mappings
- Redoing all transformations, masks, and blend modes

### How the Resolume Composition Converter Helps

The Resolume Composition Converter eliminates this tedious process by automatically adapting your compositions to new technical specifications while preserving all your creative decisions. Here's why this tool is invaluable:

1. **Saves Countless Hours of Work**: What would take hours or even days to recreate manually can be done in minutes.

2. **Maintains Creative Integrity**: All your carefully crafted transformations, effects, timing, and layer arrangements remain intact.

3. **Enables Technical Flexibility**: As technology evolves and venue requirements change, you can easily adapt your compositions without starting over.

4. **Preserves Investment in Content Creation**: The time invested in creating complex compositions is valuable and protected.

5. **Facilitates Workflow Optimization**: With the file extension matching feature, you can easily switch between different media formats while maintaining the same composition structure.

## Interface Overview

The application interface is divided into three main sections:

### File Selection
- **Input**: Select your source .avc composition file (use the Browse button)
- **Output**: Choose where to save the converted composition (use the Browse button)
- **Old File Path**: The base path where your current media files are located (use the Browse button)
- **New File Path**: The base path where your upgraded media files are located (use the Browse button)

### Resolution & Frame Rate
- **Original Settings**: The current resolution and frame rate of your composition
- **New Settings**: The target resolution and frame rate you want to convert to

### Convert Button
- Click this button to process the composition once all settings are configured

## File Organization

### Important: Media File Organization

For the converter to work properly, you should organize your media files as follows:

1. **Original Media Files**:
   - Keep all original media files in a single folder (or a folder structure)
   - This is the folder you'll specify in the "Old File Path" field

2. **Upgraded Media Files**:
   - Create a new folder for your upgraded media files
   - This is the folder you'll specify in the "New File Path" field
   - **File names must match** between original and upgraded versions
   - Only the resolution/quality should differ, not the filename

### Example Folder Structure

```
/Videos/
  /Original_1080p/
    clip1.mp4
    clip2.mp4
    background.mp4
  /Upgraded_4K/
    clip1.mp4  (same name, but 4K version)
    clip2.mp4  (same name, but 4K version)
    background.mp4  (same name, but 4K version)
```

### Using Different File Formats

With the "Ignore file extensions" option enabled, you can replace media files with different formats:

```
/Videos/
  /Original_1080p/
    clip1.mp4
    clip2.mp4
    background.mp4
  /Upgraded_4K/
    clip1.mov  (same base name, but different format)
    clip2.mov  (same base name, but different format)
    background.mov  (same base name, but different format)
```

This is particularly useful when upgrading from standard video formats (MP4) to optimized formats like MOV that are better suited for Resolume performance.

## Common Use Cases

Here are some common scenarios where the Resolume Composition Converter proves invaluable:

### Use Case 1: Upgrading from Delivery Formats to Optimized Playback Formats
**Scenario:** A VJ receives content from a client in standard MP4 format but needs to use DXV codec for optimal Resolume performance.
**Process:**
1. Convert all MP4 files to DXV format using Resolume Alley
2. Place DXV files in a new folder
3. Launch the Resolume Composition Converter
4. Select the original composition file (.avc)
5. Set the input resolution to match the original (e.g., 1920x1080)
6. Set the output resolution to the same value (1920x1080) to maintain dimensions
7. Set both input and output frame rates to match the original (e.g., 30 fps)
8. Specify the old media folder containing MP4 files
9. Specify the new media folder containing DXV files
10. Check the "Ignore file extensions" option
11. Click "Convert Composition"
12. The composition now references the DXV files instead of MP4 files, maintaining all timing and effects

### Use Case 2: Transitioning Between Different Compression Methods While Upgrading Resolution
**Scenario:** An artist wants to switch from HAP codec files to DXV while also upgrading from HD to 4K.
**Process:**
1. Convert all .HAP.MOV files to 4K .DXV files
2. Launch the Resolume Composition Converter
3. Select the original composition file (.avc)
4. Set the input resolution to the original HD size (1920x1080)
5. Set the output resolution to 4K (3840x2160)
6. Keep the frame rate the same for both input and output (e.g., 60 fps)
7. Specify the old media folder with HAP files
8. Specify the new media folder with 4K DXV files
9. Check the "Ignore file extensions" option
10. Click "Convert Composition"
11. All clips maintain their positions, effects, and timing while using the new codec and higher resolution

### Use Case 3: Upgrading to 4K Without Replacing Media Files
**Scenario:** A VJ has upgraded their system to support 4K output and wants to convert their HD composition to 4K without replacing any media files.
**Process:**
1. Launch the Resolume Composition Converter
2. Select the original HD composition file (.avc)
3. Set the input resolution to 1920x1080
4. Set the output resolution to 3840x2160
5. Keep the frame rates the same (e.g., 30 fps)
6. Leave the media folder fields empty (no media replacement)
7. Click "Convert Composition"
8. The composition is now 4K with all transformations, effects, and timing preserved
9. Original media files will be automatically scaled up to fit the new resolution

### Use Case 4: Upgrading to 4K with Selective Media Replacement
**Scenario:** A VJ is upgrading to 4K and has created 4K versions of only their most important clips, but wants to keep using the HD versions of other clips.
**Process:**
1. Place the new 4K media files in a separate folder
2. Launch the Resolume Composition Converter
3. Select the original HD composition file (.avc)
4. Set the input resolution to 1920x1080
5. Set the output resolution to 3840x2160
6. Keep the frame rates the same
7. Specify the old media folder containing all HD files
8. Specify the new media folder containing only the 4K versions
9. Click "Convert Composition"
10. The converter will replace references to files that exist in the new folder and scale up the remaining HD files
11. All transformations, effects, and timing are preserved

### Use Case 5: Upgrading to 4K with Higher Frame Rate
**Scenario:** A performer has upgraded their hardware and wants to convert their HD 30fps composition to 4K 60fps for smoother playback.
**Process:**
1. Launch the Resolume Composition Converter
2. Select the original composition file (.avc)
3. Set the input resolution to 1920x1080
4. Set the output resolution to 3840x2160
5. Set the input frame rate to 30 fps
6. Set the output frame rate to 60 fps
7. Leave the media folder fields empty (or specify new media folders if available)
8. Click "Convert Composition"
9. The composition is now 4K 60fps with all transformations and effects preserved
10. Timing is adjusted to maintain the same playback duration despite the frame rate change

## Converting a Composition

Follow these steps to convert your composition:

1. **Select Input File**:
   - Click "Browse" next to the Input field
   - Navigate to and select your original .avc composition file

2. **Select Output Location**:
   - Click "Browse" next to the Output field
   - Choose where to save the converted composition
   - It's recommended to use a new filename to avoid confusion

3. **Set File Paths** (if your media files have moved):
   - Old File Path: Enter the base path where your original media files are located
     - Click "Browse" to select the folder containing your original media files
   - New File Path: Enter the base path where your upgraded media files are located
     - Click "Browse" to select the folder containing your upgraded media files
   - Ignore file extensions: Check this box if your upgraded media files have different extensions
     - For example, if you're replacing .MP4 files with .MOV files
     - When checked, files only need to match by base name (without extension)

4. **Set Resolution and Frame Rate**:
   - The original settings are auto-detected from the composition
   - Enter your desired new resolution and frame rate
   - Common conversions:
     - HD to 4K: 1920x1080 → 3840x2160
     - 25fps to 60fps: 25 → 60

5. **Convert**:
   - Click the "Convert Composition" button
   - Wait for the process to complete
   - A summary of changes will be displayed when finished

## Supported Clip Types

The Resolume Composition Converter supports various types of clips:

### Video Files
- Standard video files referenced in your composition
- All video parameters are scaled, including resolution, position, and anchor points
- File paths are updated to point to your upgraded media files

### Image Files
- Supports various image formats (.jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp)
- Original aspect ratio is preserved during conversion
- Square images remain square, wide images remain wide, etc.
- All transform parameters are properly scaled
- File paths are updated to point to your upgraded media files

### Generator Clips
- Built-in Resolume generators (e.g., Solid Color, Gradient, Noise)
- Position, anchor points, and other transform parameters are properly scaled
- No file path updates needed (as these don't reference external files)

### Video Router Clips
- Clips that route video from other layers/clips
- All transform parameters are properly scaled
- No file path updates needed

## Transform Effects

The converter automatically scales all transform effects found in your composition:

### What Gets Converted
- **Position X/Y**: All position parameters are scaled proportionally to the new resolution
- **Anchor X/Y/Z**: All anchor point parameters are scaled to maintain proper positioning
- **Scale**: Scale parameters remain unchanged by default (they're percentage-based)
- **Multiple Transforms**: The converter handles multiple transforms at different levels:
  - Composition-level transforms
  - Layer-level transforms
  - Clip-level transforms
  - Group transforms

### How Transforms Are Detected
- The converter scans your entire composition for all transform effects
- Each transform is processed individually, ensuring all parameters are properly scaled
- The converter tracks which transforms have been processed to avoid duplicate adjustments

### Important Notes About Transforms
- The converter focuses specifically on transform effects (position, anchor points)
- Other effects that may contain pixel-based values (like masks, crops, etc.) are not automatically converted
- After conversion, you may need to manually adjust some effects that contain pixel values

## Understanding File Paths

The file path fields are crucial for ensuring your composition can find all media files after conversion. Here's how they work:

### When to Use File Paths

You need to fill in both the "Old File Path" and "New File Path" fields when:
- You've moved your media files to a new location
- You've created upgraded versions of your media files in a different folder
- You're sharing the composition with someone who has a different folder structure
- **Note**: File paths only affect video file clips, not generators or routers

### How File Paths Work

The converter performs a text replacement in the composition file:

1. It finds all instances of the "Old File Path" in the composition
2. It replaces them with the "New File Path"

### Ignore File Extensions Option

The "Ignore file extensions" checkbox allows you to replace media files with different formats:

- When **unchecked** (default): Files must have the exact same name and extension in both locations
- When **checked**: Files only need to have the same base name, but can have different extensions

This feature is particularly useful when:
- Converting from standard formats (MP4) to optimized formats like MOV
- Upgrading image files from JPG to PNG or other formats
- Maintaining the same content but in different file formats

### Example: Standard Path Replacement

If your original composition references files like:
```
C:/Users/VJ/Videos/Original_1080p/clip1.mp4
```

And you set:
- Old File Path: `C:/Users/VJ/Videos/Original_1080p`
- New File Path: `C:/Users/VJ/Videos/Upgraded_4K`
- Ignore file extensions: **Unchecked**

The converted composition will reference:
```
C:/Users/VJ/Videos/Upgraded_4K/clip1.mp4
```

### Example: Ignore Extensions Enabled

If your original composition references files like:
```
C:/Users/VJ/Videos/Original_1080p/clip1.mp4
```

And you set:
- Old File Path: `C:/Users/VJ/Videos/Original_1080p`
- New File Path: `C:/Users/VJ/Videos/Upgraded_4K`
- Ignore file extensions: **Checked**

The converted composition will reference:
```
C:/Users/VJ/Videos/Upgraded_4K/clip1.mov
```

(Assuming clip1.mov exists in the Upgraded_4K folder)

### What Happens If You Don't Specify File Paths

If you leave the "Old File Path" and "New File Path" fields empty:

1. **Composition Resolution**: The composition will be scaled up to your target resolution (e.g., 4K)
2. **Transform Parameters**: All position, anchor points, and other transform effects will be properly scaled
3. **Media Files**: The original media files will continue to be used at their original resolution
4. **Visual Result**: Resolume will display these original media files scaled up to fit the new composition resolution

This means that if your original media is 1080p, and you convert the composition to 4K:
- The composition itself will be 4K
- All positioning and layout will be properly scaled for 4K
- But the actual media content will still be 1080p, just stretched to fill the 4K space

This can result in lower visual quality compared to using actual 4K media files, as Resolume is essentially performing real-time upscaling of your 1080p content.

For optimal visual quality:
1. Create higher resolution versions of your media files
2. Organize them in a folder structure similar to your originals
3. Specify the old and new paths in the converter
4. This way, your composition will use true high-resolution media rather than upscaled content

### Important Notes

- File paths are case-sensitive
- Use forward slashes (/) even on Windows
- Do not include a trailing slash at the end of the path
- The paths should be to the base folder containing the media, not to individual files

## Best Practices

For the best results when converting compositions:

1. **Organize Media Files Properly**:
   - Keep all media files for a composition in a single folder
   - Maintain the same filenames when creating upgraded versions
   - Use a consistent folder structure

2. **Backup Your Work**:
   - Always keep a backup of your original composition
   - Save converted compositions with a new filename (e.g., "MyComp_4K.avc")

3. **Media Preparation**:
   - Prepare all your upgraded media files before converting
   - Ensure all media files exist in both original and upgraded locations
   - Verify that filenames match exactly between locations

4. **Resolution Considerations**:
   - When upgrading resolution, use exact multiples (e.g., 2x, 4x)
   - Common conversions: 1080p→2160p (2x), 720p→2160p (3x)
   - This ensures proper scaling of all elements

5. **Frame Rate Considerations**:
   - When changing frame rate, consider using multiples (e.g., 25→50, 30→60)
   - This ensures smoother timing conversions
   - BPM-synced content will be adjusted automatically

## Troubleshooting

### Common Issues and Solutions

#### "File not found" errors in Resolume after conversion

**Cause**: The file paths in the composition don't match the actual location of your media files.

**Solution**:
1. Check that all your media files exist in the location specified by "New File Path"
2. Ensure filenames match exactly between original and upgraded versions
3. Try the conversion again with correct path information

#### Some elements appear in the wrong position

**Cause**: Custom positioning that doesn't scale properly with resolution changes.

**Solution**:
1. For best results, use exact multiples for resolution changes (2x, 3x, etc.)
2. You may need to manually adjust some positions in Resolume after conversion

#### Some effects don't scale properly

**Cause**: While the converter automatically scales all transform effects, other effects with pixel-based values (masks, crops, distortions, etc.) are not automatically converted.

**Solution**:
1. After conversion, check all effects that might contain pixel values
2. Pay special attention to:
   - Mask effects
   - Crop effects
   - Distortion effects
   - Custom effects with position parameters
3. Manually adjust these effects in Resolume to match the new resolution
4. For future compositions, consider using relative values (percentages) instead of absolute pixel values when possible

#### Timing issues after conversion

**Cause**: Frame rate conversion can affect timing, especially for complex animations.

**Solution**:
1. Use frame rate multiples when possible (25→50, 30→60)
2. Check BPM settings in Resolume after conversion
3. Manually adjust any clips that don't play correctly

#### Application crashes during conversion

**Cause**: Very large compositions or corrupted .avc files can cause issues.

**Solution**:
1. Try converting a simpler composition first to verify the application works
2. Check your original .avc file opens correctly in Resolume
3. Try breaking down large compositions into smaller ones

### Getting Help

If you encounter issues not covered in this manual:

1. Check the [GitHub repository](https://github.com/yourusername/resolume-composition-converter/issues) for known issues
2. Open a new issue with detailed information about your problem
3. Include information about your operating system, composition size, and exact error messages