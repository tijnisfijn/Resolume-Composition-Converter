import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import xml.etree.ElementTree as ET
import os
import re
import json
import platform
import webbrowser
import threading
from version import get_version
import update_checker

# Disable drag and drop functionality since tkdnd library can't be loaded
DRAG_DROP_ENABLED = False
print("Drag and drop functionality disabled.")

def find_matching_file(old_file_path, new_directory, ignore_extensions=False):
    """
    Find a matching file in the new directory based on the old file path.
    
    Args:
        old_file_path: Path to the original file
        new_directory: Directory to search for matching files
        ignore_extensions: If True, match files with different extensions
        
    Returns:
        Path to the matching file in the new directory, or None if no match found
    """
    # Define file type categories for type checking
    video_extensions = ['.mp4', '.mov', '.avi', '.wmv', '.mkv', '.dxv', '.m4v', '.webm']
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    
    # Get the base name and extension of the old file
    old_basename = os.path.splitext(os.path.basename(old_file_path))[0]
    old_ext = os.path.splitext(old_file_path)[1].lower()
    
    # Determine original file type
    old_is_video = old_ext in video_extensions
    old_is_image = old_ext in image_extensions
    
    print(f"Looking for match for: {old_basename}{old_ext}")
    
    # Check if the new directory exists
    if not os.path.exists(new_directory) or not os.path.isdir(new_directory):
        print(f"New directory does not exist: {new_directory}")
        return None
    
    # List all files in the new directory
    new_files = os.listdir(new_directory)
    
    # First, try to find an exact match (same name, same extension)
    for new_file in new_files:
        new_basename = os.path.splitext(new_file)[0]
        new_ext = os.path.splitext(new_file)[1].lower()
        
        # Check for exact match (case insensitive)
        if new_basename.lower() == old_basename.lower():
            if new_ext.lower() == old_ext.lower():
                # Same name, same extension - exact match
                print(f"Found exact match: {new_file}")
                return os.path.join(new_directory, new_file)
            elif ignore_extensions:
                # Same name, different extension - check file types
                new_is_video = new_ext in video_extensions
                new_is_image = new_ext in image_extensions
                
                # Check if file types match (video with video, image with image)
                types_match = (old_is_video and new_is_video) or (old_is_image and new_is_image)
                
                if types_match:
                    print(f"Found match with different extension: {new_file}")
                    return os.path.join(new_directory, new_file)
                else:
                    print(f"WARNING: File types don't match. Original: {old_ext} (video={old_is_video}, image={old_is_image}), New: {new_ext} (video={new_is_video}, image={new_is_image})")
    
    # If we get here, no match was found
    print(f"No match found for {old_basename}{old_ext} in {new_directory}")
    return None

def _split_path_parts(path_str):
    return [p for p in re.split(r"[\\/]", path_str) if p and p != "."]

def _rebase_path(file_path, old_path, new_path):
    if not old_path or not new_path:
        return file_path

    if old_path in file_path:
        return file_path.replace(old_path, new_path)

    file_parts = _split_path_parts(file_path)
    old_parts = _split_path_parts(old_path)
    new_parts = _split_path_parts(new_path)

    if not old_parts:
        return file_path

    old_media_folder = old_parts[-1]
    try:
        idx = file_parts.index(old_media_folder)
    except ValueError:
        return file_path

    relative_parts = file_parts[idx + 1:]
    rebased_parts = new_parts + relative_parts
    rebased = "/".join(rebased_parts)
    if file_path.startswith("./"):
        return "./" + rebased
    return rebased

def update_file_paths(root, old_path, new_path, ignore_extensions=False):
    """
    Update file paths in the XML tree to point to files in the new directory.

    When ignore_extensions is True, match by base name and file type. If no match
    is found, fall back to rebasing the path to the new directory.
    """
    if not old_path or not new_path:
        return 0

    paths_updated = 0

    print(f"\n=== UPDATING FILE PATHS ===")
    print(f"Old path: {old_path}")
    print(f"New path: {new_path}")
    print(f"Ignore extensions: {ignore_extensions}")

    def update_value(getter, setter):
        nonlocal paths_updated
        file_path = getter()
        if not file_path:
            return

        new_file_path = None
        if ignore_extensions:
            matching_file = find_matching_file(file_path, new_path, ignore_extensions=True)
            if matching_file:
                new_file_path = matching_file
            else:
                new_file_path = _rebase_path(file_path, old_path, new_path)
        else:
            new_file_path = _rebase_path(file_path, old_path, new_path)

        if new_file_path and new_file_path != file_path:
            setter(new_file_path)
            paths_updated += 1

    # Update VideoFormatReaderSource paths
    for video_source in root.findall(".//VideoFormatReaderSource"):
        update_value(lambda: video_source.get("fileName"),
                     lambda v: video_source.set("fileName", v))

    # Update PreloadData paths
    for preload in root.findall(".//PreloadData/VideoFile"):
        update_value(lambda: preload.get("value"),
                     lambda v: preload.set("value", v))

    print(f"Updated {paths_updated} file paths")
    return paths_updated

PIXEL_LIKE_THRESHOLD = 100.0

def _is_pixel_like_value(raw_value):
    try:
        return abs(float(raw_value)) >= PIXEL_LIKE_THRESHOLD
    except (TypeError, ValueError):
        return False

def _scale_value_range_if_pixel_like(param_range, resolution_factor):
    """Scale ValueRange min/max bounds only when they look pixel-based."""
    for value_range in param_range.findall("./ValueRange"):
        min_raw = value_range.get("min")
        max_raw = value_range.get("max")
        if not _is_pixel_like_value(min_raw) and not _is_pixel_like_value(max_raw):
            continue
        try:
            if min_raw is not None:
                value_range.set("min", str(float(min_raw) * resolution_factor))
            if max_raw is not None:
                value_range.set("max", str(float(max_raw) * resolution_factor))
        except ValueError:
            continue

def _scale_all_value_ranges(param_range, resolution_factor):
    """Scale all ValueRange min/max bounds regardless of threshold."""
    for value_range in param_range.findall("./ValueRange"):
        min_raw = value_range.get("min")
        max_raw = value_range.get("max")
        try:
            if min_raw is not None:
                value_range.set("min", str(float(min_raw) * resolution_factor))
            if max_raw is not None:
                value_range.set("max", str(float(max_raw) * resolution_factor))
        except ValueError:
            continue

def _get_effect_policy_path():
    system = platform.system()
    if system == "Windows":
        base = os.getenv("LOCALAPPDATA") or os.getenv("APPDATA") or os.path.expanduser("~")
        return os.path.join(base, "Resolume Composition Converter", "effect_position_policy.json")
    if system == "Darwin":
        base = os.path.expanduser("~/Library/Application Support")
        return os.path.join(base, "Resolume Composition Converter", "effect_position_policy.json")
    base = os.getenv("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
    return os.path.join(base, "resolume-composition-converter", "effect_position_policy.json")

def load_effect_position_policy():
    path = _get_effect_policy_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass
    return {}

def save_effect_position_policy(policy):
    path = _get_effect_policy_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(policy, f, indent=2, sort_keys=True)
    except OSError as e:
        print(f"Warning: Could not save effect position policy: {e}")

def scan_unknown_position_effects(input_file, policy):
    """
    Find non-transform/non-text effects that expose position/anchor params and
    do not yet have an explicit policy entry.
    """
    tree = ET.parse(input_file)
    root = tree.getroot()

    excluded_effect_types = {
        "TransformEffect",
        "TextBlock",
        "TextEffect",
        "TextGenerator",
        "BlockTextGenerator",
    }
    always_pixel_effect_types = {
        "ScreenLayerTransform",
    }
    unknown = {}

    for render_pass in root.findall(".//RenderPass"):
        effect_type = render_pass.get("type", "")
        if (not effect_type or
            effect_type in excluded_effect_types or
            effect_type in always_pixel_effect_types or
            effect_type in policy):
            continue

        params_node = render_pass.find("./Params")
        if params_node is None:
            continue

        for param in params_node.findall(".//ParamRange"):
            if param.get("name") not in ["Position X", "Position Y", "Anchor X", "Anchor Y", "Anchor Z"]:
                continue

            current = unknown.get(effect_type)
            if current is None:
                unknown[effect_type] = {
                    "count": 1,
                    "sample_value": param.get("value", ""),
                }
            else:
                current["count"] += 1
            break

    return unknown

def adjust_composition(input_file, output_file, old_path=None, new_path=None,
                        resolution_factor=2.0, framerate_factor=2.4, new_name=None,
                        ignore_extensions=False, effect_position_policy=None):
    """
    Adjust a Resolume composition file for higher resolution and new frame rate,
    WITHOUT altering the original composition on disk.

    Key changes:
      1) CompositionInfo width/height -> scaled by resolution_factor
      2) Top-level VideoTrack (if present) -> scaled by resolution_factor
      3) Each Layer's VideoTrack -> scaled by resolution_factor
      4) Each Clip's VideoTrack (Width/Height) -> scaled by resolution_factor
      5) TransformEffect (Position X, Position Y, Anchor X, Anchor Y, Anchor Z) -> scaled by resolution_factor
      6) TIMELINE (seconds) durations -> Keep same real-time (preserve user-edited durations)
      7) BPM (beats) durations -> multiply defaultMillisecondsDuration by framerate_factor
      8) PrimarySource -> either force new resolution or remove width/height
      9) (Optional) replace old_path with new_path in file references
         - When ignore_extensions=True, only compare base filenames without extensions
           This allows replacing media files with different formats (e.g., .MP4 with .MOV)
           while keeping the same base filename.
         - Example: A composition using 'video1.mp4' can be updated to use 'video1.mov'
           when this option is enabled and the new media path contains the .dxv file.
    """

    # --- Parse the XML from the original file (in memory) ---
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    # Stats counters
    clips_modified = 0
    transforms_adjusted = 0
    transforms_processed = 0  # New counter to track the number of transforms processed
    durations_adjusted = 0
    paths_updated = 0
    custom_durations_preserved = 0
    text_components_found = 0  # New counter for text components
    position_ranges_adjusted = 0
    orig_comp_w = None
    orig_comp_h = None
    
    # Keep track of transforms we've already processed
    processed_transform_ids = set()
    effect_position_policy = effect_position_policy or {}
    
    # DEBUG: Find all text-related components
    text_blocks = root.findall(".//RenderPass[@type='TextBlock']")
    text_effects = root.findall(".//RenderPass[@type='TextEffect']")
    text_generators = root.findall(".//RenderPass[@type='TextGenerator']")
    block_text_generators = root.findall(".//RenderPass[@type='BlockTextGenerator']")
    
    print(f"DEBUG: Found {len(text_blocks)} TextBlock components")
    print(f"DEBUG: Found {len(text_effects)} TextEffect components")
    print(f"DEBUG: Found {len(text_generators)} TextGenerator components")
    print(f"DEBUG: Found {len(block_text_generators)} BlockTextGenerator components")

    # --- 1) Update the CompositionInfo resolution and name ---
    comp_info = root.find(".//CompositionInfo")
    if comp_info is not None:
        old_comp_w = int(comp_info.get("width"))
        old_comp_h = int(comp_info.get("height"))
        orig_comp_w = old_comp_w
        orig_comp_h = old_comp_h
        comp_info.set("width", str(int(old_comp_w * resolution_factor)))
        comp_info.set("height", str(int(old_comp_h * resolution_factor)))
        
        # Set the new composition name if provided, otherwise keep the existing name
        comp_name = new_name if new_name else comp_info.get("name")
        comp_info.set("name", comp_name)
        
        # Ensure the root Composition element has the same name
        root.set("name", comp_name)
            
        # Also update the Param name="Name" element to match the composition name
        name_param = root.find(".//Param[@name='Name'][@T='STRING']")
        if name_param is not None:
            name_param.set("value", comp_name)

    # --- 2) Update the top-level VideoTrack (if it exists) ---
    comp_video_params = root.find("./VideoTrack/Params")
    if comp_video_params is not None:
        comp_width_param = comp_video_params.find(".//ParamRange[@name='Width']")
        comp_height_param = comp_video_params.find(".//ParamRange[@name='Height']")
        if comp_width_param is not None:
            old_val = float(comp_width_param.get("value"))
            comp_width_param.set("value", str(int(old_val * resolution_factor)))
        if comp_height_param is not None:
            old_val = float(comp_height_param.get("value"))
            comp_height_param.set("value", str(int(old_val * resolution_factor)))
            
    # --- 2b) Update all top-level Transforms ---
    # First, let's find all transforms in the composition using a more general pattern
    all_transforms = root.findall(".//RenderPass[@type='TransformEffect']")
    print(f"Found {len(all_transforms)} total transforms in the composition using general pattern")
    
    # Now, let's find the top-level transforms
    comp_transforms = root.findall("./VideoTrack/RenderPass/RenderPass[@type='TransformEffect']")
    print(f"Found {len(comp_transforms)} transforms at composition level")
    transform_count = 0
    for comp_transform in comp_transforms:
        transform_count += 1
        transforms_processed += 1  # Increment the counter
        
        # Add this transform to the set of processed transforms
        transform_id = comp_transform.get("uniqueId", None)
        if transform_id:
            processed_transform_ids.add(transform_id)
            
        print(f"Processing composition transform {transform_count} (ID: {transform_id})")
        # Get all parameters for this transform
        params = comp_transform.findall(".//ParamRange")
        
        # Process each parameter
        for param in params:
            param_name = param.get("name")
            
            # Only process position and anchor parameters
            if param_name in ["Position X", "Position Y", "Anchor X", "Anchor Y", "Anchor Z"]:
                old_val = float(param.get("value"))
                new_val = old_val * resolution_factor
                param.set("value", str(new_val))
                transforms_adjusted += 1
                print(f"  Adjusted {param_name} from {old_val} to {new_val}")

    # --- 3) Update each Layer's VideoTrack width/height ---
    for layer in root.findall(".//Layer"):
        layer_params = layer.find(".//VideoTrack/Params")
        if layer_params is not None:
            param_width = layer_params.find(".//ParamRange[@name='Width']")
            param_height = layer_params.find(".//ParamRange[@name='Height']")
            if param_width is not None:
                w_val = float(param_width.get("value"))
                param_width.set("value", str(int(w_val * resolution_factor)))
            if param_height is not None:
                h_val = float(param_height.get("value"))
                param_height.set("value", str(int(h_val * resolution_factor)))
        
        # --- 3b) Update all Layer's Transforms ---
        layer_transforms = layer.findall(".//VideoTrack/RenderPass/RenderPass[@type='TransformEffect']")
        print(f"Found {len(layer_transforms)} transforms in layer")
        transform_count = 0
        for layer_transform in layer_transforms:
            transform_count += 1
            transforms_processed += 1  # Increment the counter
            
            # Add this transform to the set of processed transforms
            transform_id = layer_transform.get("uniqueId", None)
            if transform_id:
                processed_transform_ids.add(transform_id)
                
            print(f"Processing layer transform {transform_count} (ID: {transform_id})")
            # Get all parameters for this transform
            params = layer_transform.findall(".//ParamRange")
            
            # Process each parameter
            for param in params:
                param_name = param.get("name")
                
                # Only process position and anchor parameters
                if param_name in ["Position X", "Position Y", "Anchor X", "Anchor Y", "Anchor Z"]:
                    old_val = float(param.get("value"))
                    new_val = old_val * resolution_factor
                    param.set("value", str(new_val))
                    transforms_adjusted += 1
                    print(f"  Adjusted {param_name} from {old_val} to {new_val}")

    # --- 3c) Update each Group's VideoTrack width/height and transforms ---
    for group in root.findall(".//Group"):
        group_params = group.find(".//VideoTrack/Params")
        if group_params is not None:
            param_width = group_params.find(".//ParamRange[@name='Width']")
            param_height = group_params.find(".//ParamRange[@name='Height']")
            if param_width is not None:
                w_val = float(param_width.get("value"))
                param_width.set("value", str(int(w_val * resolution_factor)))
            if param_height is not None:
                h_val = float(param_height.get("value"))
                param_height.set("value", str(int(h_val * resolution_factor)))

        group_transforms = group.findall(".//VideoTrack/RenderPass/RenderPass[@type='TransformEffect']")
        print(f"Found {len(group_transforms)} transforms in group")
        transform_count = 0
        for group_transform in group_transforms:
            transform_count += 1
            transforms_processed += 1

            transform_id = group_transform.get("uniqueId", None)
            if transform_id:
                processed_transform_ids.add(transform_id)

            print(f"Processing group transform {transform_count} (ID: {transform_id})")
            params = group_transform.findall(".//ParamRange")
            for param in params:
                param_name = param.get("name")
                if param_name in ["Position X", "Position Y", "Anchor X", "Anchor Y", "Anchor Z"]:
                    old_val = float(param.get("value"))
                    new_val = old_val * resolution_factor
                    param.set("value", str(new_val))
                    transforms_adjusted += 1
                    print(f"  Adjusted {param_name} from {old_val} to {new_val}")

    # --- Process text components specifically ---
    for text_component_type, components in [
        ("TextBlock", text_blocks),
        ("TextEffect", text_effects),
        ("TextGenerator", text_generators),
        ("BlockTextGenerator", block_text_generators)
    ]:
        for component in components:
            text_components_found += 1
            component_id = component.get("uniqueId", "unknown")
            print(f"DEBUG: Processing {text_component_type} component (ID: {component_id})")
            
            # Find all parameters for this text component
            params = component.findall(".//Param") + component.findall(".//ParamRange")
            
            # Log all parameters for debugging
            print(f"DEBUG: Found {len(params)} parameters for {text_component_type}")
            for param in params:
                param_name = param.get("name", "unnamed")
                param_type = param.get("T", param.get("type", "unknown"))
                param_value = param.get("value", "no-value")
                print(f"DEBUG: {text_component_type} param: {param_name} (Type: {param_type}, Value: {param_value})")
                
                # Check for text-specific parameters that might need scaling
                if param_name in ["FontSize", "Size", "LineHeight", "CharacterSpacing", "LineSpacing", "Position X", "Position Y"]:
                    try:
                        old_val = float(param_value)
                        new_val = old_val * resolution_factor
                        print(f"DEBUG: Scaling text parameter {param_name} from {old_val} to {new_val}")
                        param.set("value", str(new_val))
                    except (ValueError, TypeError) as e:
                        print(f"DEBUG: Error scaling text parameter {param_name}: {e}")

                if param_name in ["Position X", "Position Y", "Anchor X", "Anchor Y", "Anchor Z"]:
                    _scale_value_range_if_pixel_like(param, resolution_factor)

    # --- Process non-transform effects that also expose position/anchor params ---
    # Covers effects like ScreenLayerTransform while avoiding double-scaling
    # TransformEffect and text blocks that are already handled above.
    excluded_effect_types = {
        "TransformEffect",
        "TextBlock",
        "TextEffect",
        "TextGenerator",
        "BlockTextGenerator",
    }
    always_pixel_effect_types = {
        "ScreenLayerTransform",
    }
    for render_pass in root.findall(".//RenderPass"):
        effect_type = render_pass.get("type", "")
        if effect_type in excluded_effect_types:
            continue

        params_node = render_pass.find("./Params")
        if params_node is None:
            continue

        for param in params_node.findall(".//ParamRange"):
            param_name = param.get("name")
            if param_name not in ["Position X", "Position Y", "Anchor X", "Anchor Y", "Anchor Z"]:
                continue

            raw_value = param.get("value")
            is_always_pixel = effect_type in always_pixel_effect_types
            policy_mode = effect_position_policy.get(effect_type)
            should_convert = (
                is_always_pixel or
                policy_mode == "convert" or
                (policy_mode is None and _is_pixel_like_value(raw_value))
            )
            if should_convert:
                try:
                    old_val = float(raw_value)
                    new_val = old_val * resolution_factor
                    param.set("value", str(new_val))
                    transforms_adjusted += 1
                    position_ranges_adjusted += 1
                    print(f"Adjusted {effect_type} {param_name} from {old_val} to {new_val}")
                except ValueError:
                    pass

            if is_always_pixel or policy_mode == "convert":
                _scale_all_value_ranges(param, resolution_factor)
            elif policy_mode != "skip":
                _scale_value_range_if_pixel_like(param, resolution_factor)

    # --- 4) Process each clip ---
    clips = root.findall(".//Clip")
    for clip in clips:
        clips_modified += 1  # Count all clips, including generators and routers

        # 4a) File path updates are handled in a single pass after clip processing

        # 4b) Update all transform effects (Position, Anchor, Scale) by resolution_factor
        transforms = clip.findall(".//VideoTrack/RenderPass/RenderPass[@type='TransformEffect']")
        print(f"Found {len(transforms)} transforms in clip")
        transform_count = 0
        
        # Check if this is an image clip
        is_image_clip = False
        video_source = clip.find(".//VideoFormatReaderSource")
        if video_source is not None:
            file_path = video_source.get("fileName", "")
            if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')):
                is_image_clip = True
                print(f"IMAGE DEBUG: Processing transforms for image clip: {file_path}")
                
                # Get clip dimensions for reference
                clip_video_params = clip.find(".//VideoTrack/Params")
                if clip_video_params is not None:
                    clip_width = clip_video_params.find(".//ParamRange[@name='Width']")
                    clip_height = clip_video_params.find(".//ParamRange[@name='Height']")
                    if clip_width is not None and clip_height is not None:
                        try:
                            width_val = float(clip_width.get("value"))
                            height_val = float(clip_height.get("value"))
                            print(f"IMAGE DEBUG: Clip dimensions: {width_val}x{height_val}")
                        except (ValueError, TypeError):
                            print("IMAGE DEBUG: Could not parse clip dimensions")
        
        for transform in transforms:
            transform_count += 1
            transforms_processed += 1  # Increment the counter
            
            # Add this transform to the set of processed transforms
            transform_id = transform.get("uniqueId", None)
            if transform_id:
                processed_transform_ids.add(transform_id)
                
            print(f"Processing clip transform {transform_count} (ID: {transform_id})")
            # Get all parameters for this transform
            params = transform.findall(".//ParamRange")
            
            # For image clips, log all transform parameters for debugging
            if is_image_clip:
                print(f"IMAGE DEBUG: Transform parameters for image clip (ID: {transform_id}):")
                for p in params:
                    p_name = p.get("name")
                    p_val = p.get("value")
                    print(f"IMAGE DEBUG:   {p_name} = {p_val}")
            
            # Process each parameter
            for param in params:
                param_name = param.get("name")
                
                # Only process position and anchor parameters
                if param_name in ["Position X", "Position Y", "Anchor X", "Anchor Y", "Anchor Z"]:
                    old_val = float(param.get("value"))
                    new_val = old_val * resolution_factor
                    param.set("value", str(new_val))
                    transforms_adjusted += 1
                    print(f"  Adjusted {param_name} from {old_val} to {new_val}")
                    
                    # For image clips, log additional information
                    if is_image_clip:
                        print(f"IMAGE DEBUG: Adjusted {param_name} for image clip from {old_val} to {new_val}")

            # For images, we should handle the Scale parameter differently
            if is_image_clip:
                scale_param = transform.find(".//ParamRange[@name='Scale']")
                if scale_param is not None:
                    try:
                        old_val = float(scale_param.get("value"))
                        print(f"IMAGE DEBUG: Found Scale parameter with value {old_val}")
                        
                        # For images, we might want to preserve the scale to maintain aspect ratio
                        # But for now, just log it without changing
                        print(f"IMAGE DEBUG: Scale parameter would change from {old_val} to {old_val * resolution_factor}")
                        
                        # Uncomment to actually change the scale
                        # new_val = old_val * resolution_factor
                        # scale_param.set("value", str(new_val))
                    except (ValueError, TypeError) as e:
                        print(f"IMAGE DEBUG: Error parsing Scale parameter: {e}")
            # If you also want to scale the "Scale" param for non-images, uncomment:
            # elif not is_image_clip:
            #     scale_param = transform.find(".//ParamRange[@name='Scale']")
            #     if scale_param is not None:
            #         old_val = float(scale_param.get("value"))
            #         new_val = old_val * resolution_factor
            #         scale_param.set("value", str(new_val))

        # 4c) Process clip durations in Timeline or BPM mode
        position_param = clip.find(".//ParamRange[@name='Position']")
        if position_param is not None:
            duration_source = position_param.find("DurationSource")
            if duration_source is not None:
                default_duration = duration_source.get("defaultDuration", "")
                custom_duration_str = duration_source.get("duration", None)

                if default_duration.endswith("s"):
                    # TIMELINE MODE: Preserve any custom duration that was set 
                    if custom_duration_str:
                        custom_durations_preserved += 1
                    durations_adjusted += 1

                elif default_duration.endswith("b"):
                    # BPM MODE: multiply defaultMillisecondsDuration by framerate_factor
                    phase_source = position_param.find("PhaseSourceTransportTimeline")
                    if phase_source is not None and phase_source.get("defaultMillisecondsDuration"):
                        try:
                            old_ms = float(phase_source.get("defaultMillisecondsDuration"))
                            new_ms = old_ms * framerate_factor
                            phase_source.set("defaultMillisecondsDuration", str(new_ms))
                            durations_adjusted += 1
                        except ValueError:
                            print("Warning: Could not convert defaultMillisecondsDuration to float.")
                else:
                    print(f"Warning: defaultDuration '{default_duration}' is not 's' or 'b'. Skipping.")
            else:
                # No DurationSource, but maybe there's a PhaseSourceTransportTimeline
                phase_source = position_param.find("PhaseSourceTransportTimeline")
                if phase_source is not None and phase_source.get("defaultMillisecondsDuration"):
                    try:
                        old_ms = float(phase_source.get("defaultMillisecondsDuration"))
                        new_ms = old_ms * framerate_factor
                        phase_source.set("defaultMillisecondsDuration", str(new_ms))
                        durations_adjusted += 1
                    except ValueError:
                        print("Warning: Could not convert defaultMillisecondsDuration to float.")

        # 4d) Update the Clip's own <VideoTrack><Params> (Width/Height)
        clip_video_params = clip.find(".//VideoTrack/Params")
        if clip_video_params is not None:
            clip_width = clip_video_params.find(".//ParamRange[@name='Width']")
            clip_height = clip_video_params.find(".//ParamRange[@name='Height']")
            if clip_width is not None:
                old_val = float(clip_width.get("value"))
                new_val = old_val * resolution_factor
                clip_width.set("value", str(int(new_val)))
            if clip_height is not None:
                old_val = float(clip_height.get("value"))
                new_val = old_val * resolution_factor
                clip_height.set("value", str(int(new_val)))

        # 4e) Update the PrimarySource resolution based on source type
        primary_source = clip.find(".//PrimarySource/VideoSource")
        if primary_source is not None:
            source_type = primary_source.get("type", "")
            if source_type == "VideoFormatReaderSource":
                # Check if this is an image file by examining the file extension
                is_image = False
                video_source = clip.find(".//VideoFormatReaderSource")
                if video_source is not None:
                    file_path = video_source.get("fileName", "")
                    if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')):
                        is_image = True
                        print(f"Detected image file: {file_path}")
                
                if is_image:
                    # For images, preserve the original aspect ratio by scaling both dimensions
                    try:
                        current_width = int(primary_source.get("width"))
                        current_height = int(primary_source.get("height"))
                        
                        # Log image details for debugging
                        print(f"IMAGE DEBUG: Processing image with dimensions {current_width}x{current_height}")
                        print(f"IMAGE DEBUG: Aspect ratio: {current_width/current_height:.2f}")
                        
                        # Check if the image has an unusual aspect ratio
                        aspect_ratio = current_width / current_height
                        if aspect_ratio > 2.0 or aspect_ratio < 0.5:
                            print(f"IMAGE DEBUG: Unusual aspect ratio detected: {aspect_ratio:.2f}")
                        
                        # Scale dimensions
                        new_width = int(current_width * resolution_factor)
                        new_height = int(current_height * resolution_factor)
                        primary_source.set("width", str(new_width))
                        primary_source.set("height", str(new_height))
                        
                        print(f"Preserving image aspect ratio: {current_width}x{current_height} -> {new_width}x{new_height}")
                    except (ValueError, TypeError) as e:
                        # If we can't parse the values, use default scaling
                        print(f"IMAGE DEBUG: Error parsing image dimensions: {e}")
                        fallback_w = orig_comp_w if orig_comp_w is not None else 1920
                        fallback_h = orig_comp_h if orig_comp_h is not None else 1080
                        primary_source.set("width", str(int(fallback_w * resolution_factor)))
                        primary_source.set("height", str(int(fallback_h * resolution_factor)))
                else:
                    # For videos, scale existing dimensions when available
                    try:
                        if "width" in primary_source.attrib and "height" in primary_source.attrib:
                            current_width = int(primary_source.get("width"))
                            current_height = int(primary_source.get("height"))
                            primary_source.set("width", str(int(current_width * resolution_factor)))
                            primary_source.set("height", str(int(current_height * resolution_factor)))
                        else:
                            raise ValueError("Missing width/height")
                    except (ValueError, TypeError):
                        fallback_w = orig_comp_w if orig_comp_w is not None else 1920
                        fallback_h = orig_comp_h if orig_comp_h is not None else 1080
                        primary_source.set("width", str(int(fallback_w * resolution_factor)))
                        primary_source.set("height", str(int(fallback_h * resolution_factor)))
            else:
                # For generator/router clips, we still want to scale the resolution
                # but we need to be careful about how we do it
                if "width" in primary_source.attrib and "height" in primary_source.attrib:
                    try:
                        current_width = int(primary_source.get("width"))
                        current_height = int(primary_source.get("height"))
                        primary_source.set("width", str(int(current_width * resolution_factor)))
                        primary_source.set("height", str(int(current_height * resolution_factor)))
                    except (ValueError, TypeError):
                        # If we can't parse the values, leave them as is
                        pass

    # --- 5) Final check for any missed transforms ---
    # Find all transforms in the composition using a general pattern
    all_transforms = root.findall(".//RenderPass[@type='TransformEffect']")
    print(f"Final check: Found {len(all_transforms)} total transforms in the composition")
    
    # Report how many transforms we've already processed
    print(f"Processed {transforms_processed} transforms so far")
    
    # Process any transforms that might have been missed
    for transform in all_transforms:
        # Check if this transform has already been processed
        transform_id = transform.get("uniqueId", None)
        if transform_id and transform_id in processed_transform_ids:
            print(f"Skipping already processed transform {transform_id}")
            continue
        
        # Add this transform to the set of processed transforms
        if transform_id:
            processed_transform_ids.add(transform_id)
            transforms_processed += 1
            print(f"Processing additional transform {transform_id}")
        
        # Get all parameters for this transform
        params = transform.findall(".//ParamRange")
        
        # Process each parameter
        for param in params:
            param_name = param.get("name")
            
            # Only process position and anchor parameters
            if param_name in ["Position X", "Position Y", "Anchor X", "Anchor Y", "Anchor Z"]:
                old_val = float(param.get("value"))
                new_val = old_val * resolution_factor
                param.set("value", str(new_val))
                transforms_adjusted += 1
                print(f"  Adjusted {param_name} from {old_val} to {new_val}")

    # --- 6) Update file paths (single deterministic pass) ---
    if old_path and new_path:
        paths_updated += update_file_paths(root, old_path, new_path, ignore_extensions)

    # --- 7) Write the updated XML to the *new* .avc file ---
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

    # --- 7) Return a summary ---
    extension_note = ""
    if ignore_extensions and paths_updated > 0:
        extension_note = "\nNote: File extensions were ignored during replacement, allowing format conversion."
        # Add more details about the extension changes
        extension_note += "\nIMPORTANT: If you're replacing MP4 files with MOV files, make sure both old and new paths are correct."
        extension_note += "\nThe application will match files with the same base name but different extensions."
    
    summary = (
        f"Modifications Summary:\n"
        f"Clips modified: {clips_modified}\n"
        f"Transforms adjusted: {transforms_adjusted}\n"
        f"Additional effect position/range adjustments: {position_ranges_adjusted}\n"
        f"Durations adjusted: {durations_adjusted}\n"
        f"Custom durations preserved: {custom_durations_preserved}\n"
        f"File paths updated: {paths_updated}\n"
        f"Text components found: {text_components_found}{extension_note}\n\n"
        f"Adjusted composition saved to: {output_file}"
    )
    return summary

# ----------------------
#    TKINTER GUI CODE
# ----------------------

# No custom ScrollableFrame class needed

class ResolumeConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resolume Composition Converter")
        self.root.geometry("850x750")  # Increased height to fit all content
        self.root.configure(bg="#1D1E2D")
        self.root.minsize(600, 500)  # Smaller minimum window size to allow more resizing
        
        # Set styles
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use clam theme as base
        
        # Define colors
        self.colors = {
            "primary": "#5E5FEC",
            "primary_hover": "#4f50d6",
            "dark_bg": "#1D1E2D",
            "card_bg": "#252636",
            "input_bg": "#333445",
            "text": "#e2e8f0",
            "text_muted": "#9CA3AF",
            "border": "#3f3f5a"
        }
        
        # Configure styles
        self.style.configure('TFrame', background=self.colors["card_bg"])
        self.style.configure('TLabel', background=self.colors["card_bg"], foreground=self.colors["text"], font=('Helvetica', 11))
        self.style.configure('Header.TLabel', background=self.colors["card_bg"], foreground=self.colors["text"], font=('Helvetica', 14, 'bold'))
        self.style.configure('Title.TLabel', background=self.colors["primary"], foreground='white', font=('Helvetica', 18, 'bold'))
        
        # Button styles
        self.style.configure('TButton',
                            background=self.colors["primary"],
                            foreground='white',
                            font=('Helvetica', 11, 'bold'),
                            borderwidth=0,
                            focusthickness=0,
                            padding=10)
        self.style.map('TButton',
                      background=[('active', self.colors["primary_hover"])],
                      relief=[('pressed', 'flat'), ('!pressed', 'flat')])
        
        # Entry styles
        self.style.configure('TEntry',
                            fieldbackground=self.colors["input_bg"],
                            foreground=self.colors["text"],
                            borderwidth=0,
                            padding=8)
        self.style.map('TEntry',
                      fieldbackground=[('focus', self.colors["input_bg"])],
                      bordercolor=[('focus', self.colors["primary"])])
        
        # Variables for input fields
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.old_path = tk.StringVar()
        self.new_path = tk.StringVar()
        self.ignore_extensions = tk.BooleanVar(value=False)  # New variable for ignore extensions checkbox
        
        # Defaults: 1080p(25fps) -> 4K(60fps)
        self.original_width = tk.StringVar(value="1920")
        self.original_height = tk.StringVar(value="1080")
        self.original_fps = tk.StringVar(value="25")
        self.new_width = tk.StringVar(value="3840")
        self.new_height = tk.StringVar(value="2160")
        self.new_fps = tk.StringVar(value="60")
        
        # Create app layout
        self.create_widgets()
        
        # Check for updates on startup (non-blocking, after a delay)
        self.root.after(2000, self.check_for_updates_silently)
        self.effect_position_policy = load_effect_position_policy()
    
    def create_widgets(self):
        # Create a main frame to hold everything
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a canvas with scrollbar for scrolling
        canvas = tk.Canvas(main_frame, bg=self.colors["dark_bg"], highlightthickness=0)
        
        # Style the scrollbar to match the interface
        self.style.configure("Custom.Vertical.TScrollbar",
                            background=self.colors["card_bg"],
                            troughcolor=self.colors["dark_bg"],
                            arrowcolor=self.colors["text"],
                            borderwidth=0)
        
        # Create the scrollbar but don't pack it yet
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview, style="Custom.Vertical.TScrollbar")
        
        # Configure the canvas
        canvas.configure(yscrollcommand=self.on_scroll)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Store scrollbar as instance variable so we can access it in on_scroll
        self.scrollbar = scrollbar
        
        # Create a frame inside the canvas to hold the content
        main_container = ttk.Frame(canvas)
        canvas_window = canvas.create_window((0, 0), window=main_container, anchor="nw")
        
        # Configure the canvas to resize with the window
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
            # Check if scrollbar is needed after resize
            self.check_scrollbar_needed(canvas)
        canvas.bind("<Configure>", on_canvas_configure)
        
        # Update the scroll region when the frame size changes
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Check if scrollbar is needed after content changes
            self.check_scrollbar_needed(canvas)
        main_container.bind("<Configure>", on_frame_configure)
        
        # Store canvas as instance variable for later use
        self.canvas = canvas
        
        # Header frame
        header_frame = ttk.Frame(main_container, style='TFrame')
        header_frame.pack(fill=tk.X)
        
        # Configure header background
        header_canvas = tk.Canvas(header_frame, bg=self.colors["primary"], height=70, highlightthickness=0)
        header_canvas.pack(fill=tk.X)
        
        # App title - centered
        title_label = ttk.Label(header_canvas, text="Resolume Composition Converter", style='Title.TLabel')
        title_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Main content frame with rounded corners effect
        content_container = ttk.Frame(main_container, style='TFrame')
        content_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Add a border around the content
        content_frame = ttk.Frame(content_container, style='TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # File Selection Section
        self.create_section_title(content_frame, "File Selection")
        
        file_section = ttk.Frame(content_frame, style='TFrame')
        file_section.pack(fill=tk.X, pady=10)
        
        # Input composition
        input_frame = ttk.Frame(file_section, style='TFrame')
        input_frame.pack(fill=tk.X, pady=8)
        
        input_label = ttk.Label(input_frame, text="Input:", style='TLabel', width=12)
        input_label.pack(side=tk.LEFT)
        
        input_entry = ttk.Entry(input_frame, textvariable=self.input_path, style='TEntry')
        input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_input_btn = ttk.Button(input_frame, text="Browse", command=self.browse_input, style='TButton')
        browse_input_btn.pack(side=tk.RIGHT)
        
        # Output composition
        output_frame = ttk.Frame(file_section, style='TFrame')
        output_frame.pack(fill=tk.X, pady=8)
        
        output_label = ttk.Label(output_frame, text="Output:", style='TLabel', width=12)
        output_label.pack(side=tk.LEFT)
        
        output_entry = ttk.Entry(output_frame, textvariable=self.output_path, style='TEntry')
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_output_btn = ttk.Button(output_frame, text="Browse", command=self.browse_output, style='TButton')
        browse_output_btn.pack(side=tk.RIGHT)
        
        # Old file path
        old_path_frame = ttk.Frame(file_section, style='TFrame')
        old_path_frame.pack(fill=tk.X, pady=8)
        
        old_path_label = ttk.Label(old_path_frame, text="Old File Path:", style='TLabel', width=12)
        old_path_label.pack(side=tk.LEFT)
        
        old_path_entry = ttk.Entry(old_path_frame, textvariable=self.old_path, style='TEntry')
        old_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_old_path_btn = ttk.Button(old_path_frame, text="Browse", command=self.browse_old_path, style='TButton')
        browse_old_path_btn.pack(side=tk.RIGHT)
        
        # New file path
        new_path_frame = ttk.Frame(file_section, style='TFrame')
        new_path_frame.pack(fill=tk.X, pady=8)
        
        new_path_label = ttk.Label(new_path_frame, text="New File Path:", style='TLabel', width=12)
        new_path_label.pack(side=tk.LEFT)
        
        new_path_entry = ttk.Entry(new_path_frame, textvariable=self.new_path, style='TEntry')
        new_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_new_path_btn = ttk.Button(new_path_frame, text="Browse", command=self.browse_new_path, style='TButton')
        browse_new_path_btn.pack(side=tk.RIGHT)
        
        # Ignore extensions checkbox
        ignore_ext_frame = ttk.Frame(file_section, style='TFrame')
        ignore_ext_frame.pack(fill=tk.X, pady=8)
        
        # Configure checkbox style
        self.style.configure('TCheckbutton',
                            background=self.colors["card_bg"],
                            foreground=self.colors["text"])
        
        # Configure hover state for checkbox to maintain text visibility
        self.style.map('TCheckbutton',
                      background=[('active', self.colors["card_bg"])],
                      foreground=[('active', self.colors["text"])])
        
        ignore_ext_checkbox = ttk.Checkbutton(
            ignore_ext_frame,
            text="Ignore file extensions when replacing media (allows replacing .MP4 with .MOV etc.)",
            variable=self.ignore_extensions,
            style='TCheckbutton'
        )
        ignore_ext_checkbox.pack(side=tk.LEFT, padx=(12, 0))
        
        # Create tooltip for the ignore extensions checkbox
        tooltip_text = ("When checked, files with the same name but different extensions will be matched.\n"
                       "This allows replacing media files with different formats (e.g., .MP4 with .MOV)\n"
                       "while keeping the same base filename.\n\n"
                       "Example: A composition using 'video1.mp4' can be updated to use 'video1.mov'\n"
                       "when this option is checked and the new media path contains the .mov file.")
        
        # Simple tooltip implementation
        def show_tooltip(event):
            # Position the tooltip to the right of the checkbox text
            # to avoid covering the text
            tooltip = tk.Toplevel(self.root)
            tooltip.wm_overrideredirect(True)
            
            # Position tooltip below the checkbox
            # This ensures it doesn't cover the checkbox text
            tooltip.wm_geometry(f"+{event.x_root+15}+{event.y_root+30}")
            tooltip.configure(bg=self.colors["dark_bg"], bd=1, relief="solid")
            
            label = tk.Label(tooltip, text=tooltip_text, justify="left",
                           bg=self.colors["dark_bg"], fg=self.colors["text"],
                           padx=5, pady=5, wraplength=400)
            label.pack()
            
            def hide_tooltip(event=None):
                tooltip.destroy()
            
            tooltip.bind("<Leave>", hide_tooltip)
            ignore_ext_checkbox.bind("<Leave>", hide_tooltip)
            # Auto-hide after 8 seconds
            self.root.after(8000, hide_tooltip)
            
        ignore_ext_checkbox.bind("<Enter>", show_tooltip)
        
        # Resolution & Frame Rate Section
        self.create_section_title(content_frame, "Resolution & Frame Rate", pady=(20, 10))
        
        # Create a simple grid layout for resolution settings
        resolution_frame = ttk.Frame(content_frame, style='TFrame')
        resolution_frame.pack(fill=tk.X, pady=10)
        
        # Create a frame for the two columns
        columns_frame = ttk.Frame(resolution_frame, style='TFrame')
        columns_frame.pack(fill=tk.X)
        
        # Left column - Original settings
        left_column = ttk.Frame(columns_frame, style='TFrame')
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right column - New settings
        right_column = ttk.Frame(columns_frame, style='TFrame')
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Original Settings
        ttk.Label(left_column, text="Original Settings", font=('Helvetica', 12, 'bold'),
                 background=self.colors["card_bg"], foreground=self.colors["text"]).pack(anchor="w", pady=(0, 10))
        
        # Original Width
        orig_width_frame = ttk.Frame(left_column, style='TFrame')
        orig_width_frame.pack(fill=tk.X, pady=5)
        ttk.Label(orig_width_frame, text="Width:", width=12, style='TLabel').pack(side=tk.LEFT)
        ttk.Entry(orig_width_frame, textvariable=self.original_width, width=15).pack(side=tk.LEFT)
        
        # Original Height
        orig_height_frame = ttk.Frame(left_column, style='TFrame')
        orig_height_frame.pack(fill=tk.X, pady=5)
        ttk.Label(orig_height_frame, text="Height:", width=12, style='TLabel').pack(side=tk.LEFT)
        ttk.Entry(orig_height_frame, textvariable=self.original_height, width=15).pack(side=tk.LEFT)
        
        # Original Frame Rate
        orig_fps_frame = ttk.Frame(left_column, style='TFrame')
        orig_fps_frame.pack(fill=tk.X, pady=5)
        ttk.Label(orig_fps_frame, text="Frame Rate:", width=12, style='TLabel').pack(side=tk.LEFT)
        ttk.Entry(orig_fps_frame, textvariable=self.original_fps, width=15).pack(side=tk.LEFT)
        
        # New Settings
        ttk.Label(right_column, text="New Settings", font=('Helvetica', 12, 'bold'),
                 background=self.colors["card_bg"], foreground=self.colors["text"]).pack(anchor="w", pady=(0, 10))
        
        # New Width
        new_width_frame = ttk.Frame(right_column, style='TFrame')
        new_width_frame.pack(fill=tk.X, pady=5)
        ttk.Label(new_width_frame, text="Width:", width=12, style='TLabel').pack(side=tk.LEFT)
        ttk.Entry(new_width_frame, textvariable=self.new_width, width=15).pack(side=tk.LEFT)
        
        # New Height
        new_height_frame = ttk.Frame(right_column, style='TFrame')
        new_height_frame.pack(fill=tk.X, pady=5)
        ttk.Label(new_height_frame, text="Height:", width=12, style='TLabel').pack(side=tk.LEFT)
        ttk.Entry(new_height_frame, textvariable=self.new_height, width=15).pack(side=tk.LEFT)
        
        # New Frame Rate
        new_fps_frame = ttk.Frame(right_column, style='TFrame')
        new_fps_frame.pack(fill=tk.X, pady=5)
        ttk.Label(new_fps_frame, text="Frame Rate:", width=12, style='TLabel').pack(side=tk.LEFT)
        ttk.Entry(new_fps_frame, textvariable=self.new_fps, width=15).pack(side=tk.LEFT)
        
        # Footer with Convert button
        footer_frame = ttk.Frame(content_frame, style='TFrame')
        footer_frame.pack(fill=tk.X, pady=20)
        
        # Center the button
        button_container = ttk.Frame(footer_frame, style='TFrame')
        button_container.pack(anchor='center')
        
        convert_button = ttk.Button(
            button_container,
            text="Convert Composition",
            command=self.convert_composition,
            style='TButton',
            padding=(20, 10)
        )
        convert_button.pack(pady=10)
    
    def on_scroll(self, *args):
        """Handle scroll events and update scrollbar"""
        # Update scrollbar position
        self.scrollbar.set(*args)
        
        # Show or hide scrollbar based on content size
        first, last = float(args[0]), float(args[1])
        if first <= 0.0 and last >= 1.0:
            # Content fits in window, hide scrollbar
            self.scrollbar.pack_forget()
        else:
            # Content doesn't fit, show scrollbar
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def check_scrollbar_needed(self, canvas):
        """Check if scrollbar is needed based on content size"""
        # Get canvas and content dimensions
        canvas_height = canvas.winfo_height()
        content_height = canvas.bbox("all")[3] if canvas.bbox("all") else 0
        
        # Show or hide scrollbar based on content size
        if content_height <= canvas_height:
            # Content fits in window, hide scrollbar
            self.scrollbar.pack_forget()
        else:
            # Content doesn't fit, show scrollbar
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Section title creation method
        
    def create_section_title(self, parent, text, **kwargs):
        """Create a section title with a horizontal line"""
        frame = ttk.Frame(parent, style='TFrame')
        frame.pack(fill=tk.X, **kwargs)
        
        # Title label
        label = ttk.Label(frame, text=text, style='Header.TLabel')
        label.pack(side=tk.LEFT, anchor='w')
        
        # Horizontal separator (line)
        separator = ttk.Separator(frame, orient='horizontal')
        separator.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(15, 0), pady=10)
        
        # Add some space after the title
        spacer = ttk.Frame(parent, height=5, style='TFrame')
        spacer.pack(fill=tk.X)
    
    def browse_input(self):
        filename = filedialog.askopenfilename(
            title="Select Input Composition",
            filetypes=[("Arena Composition", "*.avc *.xml"), ("All files", "*.*")]
        )
        if filename:
            self.input_path.set(filename)
    
    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save Output Composition",
            filetypes=[("Arena Composition", "*.avc *.xml"), ("All files", "*.*")],
            defaultextension=".avc"
        )
        if filename:
            self.output_path.set(filename)
    
    def browse_old_path(self):
        folder = filedialog.askdirectory(
            title="Select Old Media Path"
        )
        if folder:
            self.old_path.set(folder)
    
    def browse_new_path(self):
        folder = filedialog.askdirectory(
            title="Select New Media Path"
        )
        if folder:
            self.new_path.set(folder)
    
    def convert_composition(self):
        """Handle composition conversion using the original adjust_composition function"""
        input_file = self.input_path.get()
        output_file = self.output_path.get()
        old_path = self.old_path.get().strip()
        new_path = self.new_path.get().strip()
        
        # Prevent overwriting the same file
        if os.path.abspath(input_file) == os.path.abspath(output_file):
            messagebox.showerror(
                "Error",
                "Input and output files must be different.\nPlease choose a different output file."
            )
            return
        
        # Get resolution and frame rate parameters
        try:
            orig_width = float(self.original_width.get())
            orig_height = float(self.original_height.get())
            new_width = float(self.new_width.get())
            new_height = float(self.new_height.get())
            orig_framerate = float(self.original_fps.get())
            new_framerate = float(self.new_fps.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for resolution and frame rate.")
            return
        
        if orig_width == 0 or orig_height == 0 or orig_framerate == 0:
            messagebox.showerror("Error", "Original resolution and frame rate must be non-zero.")
            return
        
        # Calculate scaling factors
        resolution_factor = new_width / orig_width
        framerate_factor = new_framerate / orig_framerate
        if not input_file or not output_file:
            messagebox.showerror("Error", "Please select both an input and an output file.")
            return
        
        # When ignore_extensions is checked, both paths must be provided
        if self.ignore_extensions.get() and (not old_path or not new_path):
            messagebox.showerror("Error", "When 'Ignore file extensions' is checked, you must provide both old and new media paths.")
            return
        elif (old_path and not new_path) or (new_path and not old_path):
            messagebox.showerror("Error", "Both old path and new path must be provided together.")
            return
            return
        
        try:
            # Extract the output filename without extension to use as the composition name
            output_basename = os.path.basename(output_file)
            output_name = os.path.splitext(output_basename)[0]

            unknown_effects = scan_unknown_position_effects(input_file, self.effect_position_policy)
            if unknown_effects:
                for effect_type, info in sorted(unknown_effects.items()):
                    result = messagebox.askyesnocancel(
                        "Unknown Position Effect",
                        f"Effect '{effect_type}' has position/anchor parameters.\n"
                        f"Detected occurrences: {info['count']}\n"
                        f"Sample value: {info['sample_value']}\n\n"
                        f"Treat this effect as pixel-based and convert these parameters?"
                        f"\n\nYour choice will be remembered for future conversions."
                    )
                    if result is None:
                        return
                    self.effect_position_policy[effect_type] = "convert" if result else "skip"
                save_effect_position_policy(self.effect_position_policy)
            
            # Check if ignore_extensions is checked
            if self.ignore_extensions.get():
                print("INFO: 'Ignore file extensions' option is enabled.")
                print(f"INFO: Will look for files with the same base name in {new_path}")
                print("INFO: This allows replacing files with different extensions (e.g., .MP4 with .MOV)")
                
                # Show a message to the user
                messagebox.showinfo(
                    "Extension Matching Enabled",
                    f"The 'Ignore file extensions' option is enabled.\n\n"
                    f"Files with the same base name but different extensions will be matched.\n"
                    f"For example, 'video1.mp4' can be replaced with 'video1.mov'."
                )
            
            # Standard case - use the provided paths
            summary = adjust_composition(
                input_file,
                output_file,
                old_path,
                new_path,
                resolution_factor,
                framerate_factor,
                new_name=output_name,
                ignore_extensions=self.ignore_extensions.get(),  # Pass the checkbox value
                effect_position_policy=self.effect_position_policy
            )
            messagebox.showinfo("Processing Complete", summary)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during processing: {str(e)}")

    def open_manual_pdf(self):
        """Open the PDF manual"""
        try:
            import sys
            import os
            manual_path = self._find_manual_file("MANUAL.pdf")
            if not manual_path:
                messagebox.showinfo(
                    "Opening Manual",
                    "The PDF manual is not bundled. Opening the Markdown manual instead.",
                )
                self.open_manual_markdown()
                return
            self._open_file_with_default_app(manual_path)
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not open the manual: {str(e)}")
            self.open_manual_markdown()
    
    def open_manual_html(self):
        """Open the HTML manual"""
        try:
            manual_path = self._find_manual_file("MANUAL.html")
            if not manual_path:
                messagebox.showinfo(
                    "Opening Manual",
                    "The HTML manual is not bundled. Opening the Markdown manual instead.",
                )
                self.open_manual_markdown()
                return
            self._open_file_with_default_app(manual_path)
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not open the manual: {str(e)}")
            self.open_manual_markdown()
    
    def open_manual_markdown(self):
        """Open the Markdown manual"""
        try:
            manual_path = self._find_manual_file("MANUAL.md")
            if not manual_path:
                messagebox.showerror(
                    "Error",
                    "Could not find MANUAL.md in the installed application.",
                )
                return
            self._open_file_with_default_app(manual_path)
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not open the manual: {str(e)}")

    def _open_file_with_default_app(self, path):
        import os
        import platform
        import subprocess

        if platform.system() == 'Darwin':
            subprocess.run(['open', path], check=False)
        elif platform.system() == 'Windows':
            os.startfile(path)
        else:
            subprocess.run(['xdg-open', path], check=False)

    def _find_manual_file(self, filename):
        import os
        import sys

        candidates = []
        if getattr(sys, 'frozen', False):
            exe_dir = os.path.dirname(sys.executable)
            candidates.extend([
                os.path.join(exe_dir, filename),
                os.path.join(exe_dir, "_internal", filename),
                os.path.join(exe_dir, "resources", filename),
                os.path.join(exe_dir, "Resources", filename),
                os.path.normpath(os.path.join(exe_dir, "..", "Resources", filename)),
                os.path.normpath(os.path.join(exe_dir, "..", "resources", filename)),
            ])
        else:
            repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            candidates.extend([
                os.path.join(repo_root, filename),
                os.path.join(repo_root, "docs", filename),
                os.path.join(repo_root, "documentation", filename),
            ])

        for path in candidates:
            if os.path.exists(path):
                return path
        return None
    
    def check_for_updates(self, show_if_current=True):
        """
        Check for updates and show a dialog with the result
        Args:
            show_if_current: If True, show a message even if no update is available
        """
        # Show a "checking" message for better UX
        checking_window = tk.Toplevel(self.root)
        checking_window.title("Checking for Updates")
        checking_window.geometry("300x100")
        checking_window.resizable(False, False)
        checking_window.transient(self.root)
        checking_window.grab_set()
        
        # Center the window
        checking_window.update_idletasks()
        width = checking_window.winfo_width()
        height = checking_window.winfo_height()
        x = (checking_window.winfo_screenwidth() // 2) - (width // 2)
        y = (checking_window.winfo_screenheight() // 2) - (height // 2)
        checking_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # Add a message and progress indicator
        message = ttk.Label(checking_window, text="Checking for updates...", font=('Helvetica', 12))
        message.pack(pady=20)
        
        # Use after to allow the window to be drawn before checking
        def perform_check():
            # Check for updates
            update_available, latest_version, download_url, release_notes = update_checker.check_for_updates(force=True)
            
            # Close the checking window
            checking_window.destroy()
            
            if update_available:
                # Show update available dialog
                result = messagebox.askyesno(
                    "Update Available",
                    f"A new version ({latest_version}) is available!\n\n"
                    f"You are currently using version {get_version()}.\n\n"
                    "Would you like to download the update now?",
                    icon="info"
                )
                if result:
                    # Open the download URL in the default browser
                    webbrowser.open(download_url)
            elif show_if_current:
                # Show "up to date" message
                messagebox.showinfo(
                    "No Updates Available",
                    f"You are using the latest version ({get_version()}).",
                    icon="info"
                )
        
        checking_window.after(100, perform_check)
    
    def check_for_updates_silently(self):
        """Check for updates without showing a dialog unless an update is available"""
        # Run the check in a separate thread to avoid blocking the UI
        def check_thread():
            update_available, latest_version, download_url, release_notes = update_checker.check_for_updates()
            
            if update_available:
                # Use after to schedule the dialog on the main thread
                self.root.after(0, lambda: self._show_update_dialog(latest_version, download_url))
        
        threading.Thread(target=check_thread, daemon=True).start()
    
    def _show_update_dialog(self, latest_version, download_url):
        """Show the update available dialog"""
        result = messagebox.askyesno(
            "Update Available",
            f"A new version ({latest_version}) is available!\n\n"
            f"You are currently using version {get_version()}.\n\n"
            "Would you like to download the update now?",
            icon="info"
        )
        if result:
            webbrowser.open(download_url)

    def manage_effect_position_policy(self):
        """View/edit/reset remembered effect position conversion policy."""
        editor = tk.Toplevel(self.root)
        editor.title("Effect Position Rules")
        editor.geometry("700x420")
        editor.minsize(620, 360)
        editor.transient(self.root)
        editor.grab_set()

        container = ttk.Frame(editor, padding=12)
        container.pack(fill=tk.BOTH, expand=True)

        info = ttk.Label(
            container,
            text=(
                "These rules are remembered and reused when unknown effects expose "
                "Position/Anchor parameters."
            ),
            style='TLabel'
        )
        info.pack(anchor="w", pady=(0, 10))

        columns = ("effect", "mode")
        tree = ttk.Treeview(container, columns=columns, show="headings", height=12)
        tree.heading("effect", text="Effect Type")
        tree.heading("mode", text="Mode")
        tree.column("effect", width=420, anchor="w")
        tree.column("mode", width=180, anchor="center")
        tree.pack(fill=tk.BOTH, expand=True)

        for effect_type, mode in sorted(self.effect_position_policy.items()):
            tree.insert("", tk.END, values=(effect_type, mode))

        if not self.effect_position_policy:
            messagebox.showinfo(
                "No Saved Rules",
                "No effect position rules are saved yet.\n"
                "They will appear here after you answer prompts during conversion."
            )

        def get_selected_effect():
            selection = tree.selection()
            if not selection:
                return None, None
            item_id = selection[0]
            values = tree.item(item_id, "values")
            if not values:
                return None, None
            return item_id, values[0]

        def set_mode(mode):
            item_id, effect_type = get_selected_effect()
            if not effect_type:
                messagebox.showwarning("No Selection", "Select an effect rule first.")
                return
            self.effect_position_policy[effect_type] = mode
            tree.item(item_id, values=(effect_type, mode))

        def remove_rule():
            item_id, effect_type = get_selected_effect()
            if not effect_type:
                messagebox.showwarning("No Selection", "Select an effect rule first.")
                return
            self.effect_position_policy.pop(effect_type, None)
            tree.delete(item_id)

        def reset_all():
            if not self.effect_position_policy:
                return
            if not messagebox.askyesno(
                "Reset Rules",
                "Delete all saved effect position rules?"
            ):
                return
            self.effect_position_policy.clear()
            for item_id in tree.get_children():
                tree.delete(item_id)

        def save_and_close():
            save_effect_position_policy(self.effect_position_policy)
            editor.destroy()

        button_row = ttk.Frame(container)
        button_row.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(button_row, text="Set Convert", command=lambda: set_mode("convert"), style='TButton').pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_row, text="Set Skip", command=lambda: set_mode("skip"), style='TButton').pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_row, text="Remove Rule", command=remove_rule, style='TButton').pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_row, text="Reset All", command=reset_all, style='TButton').pack(side=tk.LEFT)

        close_row = ttk.Frame(container)
        close_row.pack(fill=tk.X, pady=(8, 0))
        ttk.Button(close_row, text="Save & Close", command=save_and_close, style='TButton').pack(side=tk.RIGHT)
        ttk.Button(close_row, text="Cancel", command=editor.destroy, style='TButton').pack(side=tk.RIGHT, padx=(0, 8))
            
    def show_about(self):
        """Show the About dialog"""
        messagebox.showinfo("About",
                           f"Resolume Composition Converter\n\n"
                           f"Version {get_version()}\n\n"
                           "A tool for converting Resolume Arena compositions to different resolutions and frame rates.\n\n"
                           "© 2025 Resolume Composition Converter")

# ----------------------
#       MAIN APP
# ----------------------
if __name__ == "__main__":
    # Initialize Tk
    root = tk.Tk()
    
    app = ResolumeConverterApp(root)
    
    # Set dark mode colors for the main window and frames
    root.configure(bg="#1D1E2D")
    
    # Make window resizable
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    # Explicitly set window to be resizable
    root.resizable(True, True)
    
    # Create menu bar
    menubar = tk.Menu(root)
    
    # Create Help menu
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="Check for Updates", command=app.check_for_updates)
    help_menu.add_command(label="User Manual", command=app.open_manual_html)
    help_menu.add_command(label="Effect Position Rules", command=app.manage_effect_position_policy)
    help_menu.add_separator()
    help_menu.add_command(label="About", command=app.show_about)
    
    # Add Help menu to menu bar
    menubar.add_cascade(label="Help", menu=help_menu)
    
    # Configure the menu bar
    root.config(menu=menubar)
    
    root.mainloop()
