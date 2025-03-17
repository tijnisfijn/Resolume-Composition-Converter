import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import xml.etree.ElementTree as ET
import os

# Try to import TkinterDnD for drag and drop functionality
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    DRAG_DROP_ENABLED = True
except ImportError:
    DRAG_DROP_ENABLED = False
    print("TkinterDnD not available. Drag and drop functionality will be disabled.")

def adjust_composition(input_file, output_file, old_path=None, new_path=None,
                       resolution_factor=2.0, framerate_factor=2.4, new_name=None):
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
    
    # Keep track of transforms we've already processed
    processed_transform_ids = set()
    
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

    # --- 4) Process each clip ---
    clips = root.findall(".//Clip")
    for clip in clips:
        clips_modified += 1  # Count all clips, including generators and routers

        # 4a) Optional path replacement (only if we actually find a VideoFormatReaderSource)
        video_source = clip.find(".//VideoFormatReaderSource")
        if video_source is not None and old_path and new_path:
            file_path = video_source.get("fileName")
            
            if file_path:
                # Extract the media folder name and filename
                # This handles both absolute and relative paths
                old_path_parts = os.path.normpath(old_path).split(os.sep)
                file_path_parts = os.path.normpath(file_path).split(os.sep)
                
                # Get the last part of old_path (usually the media folder name)
                old_media_folder = old_path_parts[-1] if old_path_parts else ""
                
                # Check if the media folder name appears in the file path
                media_folder_index = -1
                for i, part in enumerate(file_path_parts):
                    if part == old_media_folder:
                        media_folder_index = i
                        break
                
                if media_folder_index >= 0:
                    # Construct new path by replacing everything from media folder onwards
                    new_path_parts = os.path.normpath(new_path).split(os.sep)
                    new_media_folder = new_path_parts[-1] if new_path_parts else ""
                    
                    # Replace the media folder in the path
                    file_path_parts[media_folder_index] = new_media_folder
                    
                    # Reconstruct the path with the appropriate separator
                    if file_path.startswith("./"):
                        new_file_path = "./" + "/".join(file_path_parts[1:])
                    else:
                        new_file_path = "/".join(file_path_parts)
                    
                    video_source.set("fileName", new_file_path)
                    paths_updated += 1
                else:
                    # If we can't find the media folder, try a direct replacement
                    if old_path in file_path:
                        new_file_path = file_path.replace(old_path, new_path)
                        video_source.set("fileName", new_file_path)
                        paths_updated += 1
        
            # Also check PreloadData
            preload = clip.find(".//PreloadData/VideoFile")
            if preload is not None:
                file_path = preload.get("value")
                
                if file_path:
                    # Extract the media folder name and filename
                    # This handles both absolute and relative paths
                    old_path_parts = os.path.normpath(old_path).split(os.sep)
                    file_path_parts = os.path.normpath(file_path).split(os.sep)
                    
                    # Get the last part of old_path (usually the media folder name)
                    old_media_folder = old_path_parts[-1] if old_path_parts else ""
                    
                    # Check if the media folder name appears in the file path
                    media_folder_index = -1
                    for i, part in enumerate(file_path_parts):
                        if part == old_media_folder:
                            media_folder_index = i
                            break
                    
                    if media_folder_index >= 0:
                        # Construct new path by replacing everything from media folder onwards
                        new_path_parts = os.path.normpath(new_path).split(os.sep)
                        new_media_folder = new_path_parts[-1] if new_path_parts else ""
                        
                        # Replace the media folder in the path
                        file_path_parts[media_folder_index] = new_media_folder
                        
                        # Reconstruct the path with the appropriate separator
                        if file_path.startswith("./"):
                            new_file_path = "./" + "/".join(file_path_parts[1:])
                        else:
                            new_file_path = "/".join(file_path_parts)
                        
                        preload.set("value", new_file_path)
                        paths_updated += 1
                    else:
                        # If we can't find the media folder, try a direct replacement
                        if old_path in file_path:
                            new_file_path = file_path.replace(old_path, new_path)
                            preload.set("value", new_file_path)
                            paths_updated += 1

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
                        primary_source.set("width", str(int(1920 * resolution_factor)))
                        primary_source.set("height", str(int(1080 * resolution_factor)))
                else:
                    # For videos, use the standard 16:9 scaling
                    primary_source.set("width", str(int(1920 * resolution_factor)))
                    primary_source.set("height", str(int(1080 * resolution_factor)))
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

    # --- 6) Write the updated XML to the *new* .avc file ---
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

    # --- 7) Return a summary ---
    summary = (
        f"Modifications Summary:\n"
        f"Clips modified: {clips_modified}\n"
        f"Transforms adjusted: {transforms_adjusted}\n"
        f"Durations adjusted: {durations_adjusted}\n"
        f"Custom durations preserved: {custom_durations_preserved}\n"
        f"File paths updated: {paths_updated}\n"
        f"Text components found: {text_components_found}\n\n"
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
            "border": "#3f3f5a",
            "drop_highlight": "#7E7FFC"  # Slightly lighter than primary for drop highlight
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
        
        # Defaults: 1080p(25fps) -> 4K(60fps)
        self.original_width = tk.StringVar(value="1920")
        self.original_height = tk.StringVar(value="1080")
        self.original_fps = tk.StringVar(value="25")
        self.new_width = tk.StringVar(value="3840")
        self.new_height = tk.StringVar(value="2160")
        self.new_fps = tk.StringVar(value="60")
        
        # Store references to entry widgets for drag and drop
        self.entry_widgets = {}
        
        # Create app layout
        self.create_widgets()
        
        # Set up drag and drop for the whole window
        self.setup_drag_and_drop()
    
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
        # Store reference for drag and drop
        self.entry_widgets['input'] = input_entry
        
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
        # Store reference for drag and drop
        self.entry_widgets['old_path'] = old_path_entry
        
        browse_old_path_btn = ttk.Button(old_path_frame, text="Browse", command=self.browse_old_path, style='TButton')
        browse_old_path_btn.pack(side=tk.RIGHT)
        
        # New file path
        new_path_frame = ttk.Frame(file_section, style='TFrame')
        new_path_frame.pack(fill=tk.X, pady=8)
        
        new_path_label = ttk.Label(new_path_frame, text="New File Path:", style='TLabel', width=12)
        new_path_label.pack(side=tk.LEFT)
        
        new_path_entry = ttk.Entry(new_path_frame, textvariable=self.new_path, style='TEntry')
        new_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        # Store reference for drag and drop
        self.entry_widgets['new_path'] = new_path_entry
        
        browse_new_path_btn = ttk.Button(new_path_frame, text="Browse", command=self.browse_new_path, style='TButton')
        browse_new_path_btn.pack(side=tk.RIGHT)
        
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
    
    def setup_drag_and_drop(self):
        """Set up drag and drop functionality for the entry widgets"""
        # Skip if drag and drop is not available
        if not DRAG_DROP_ENABLED:
            return
            
        # Create a highlight style for drag and drop
        self.style.configure('Highlight.TEntry',
                            fieldbackground=self.colors["drop_highlight"],
                            foreground=self.colors["text"],
                            borderwidth=0,
                            padding=8)
        
        # Define the drag and drop functions
        def drop(event, target_widget_key):
            # Get the dropped data
            data = event.data
            
            # Check if it's a file or folder path (remove curly braces if present)
            if data.startswith('{') and data.endswith('}'):
                data = data[1:-1]
            
            # Handle multiple files (space-separated)
            paths = data.split(' ')
            if not paths:
                return
            
            # Get the first path
            path = paths[0]
            
            # Handle different target widgets
            if target_widget_key == 'input':
                # Only accept .avc or .xml files for input
                if path.lower().endswith(('.avc', '.xml')):
                    self.input_path.set(path)
            elif target_widget_key == 'old_path' or target_widget_key == 'new_path':
                # For path fields, check if it's a directory
                if os.path.isdir(path):
                    if target_widget_key == 'old_path':
                        self.old_path.set(path)
                    else:
                        self.new_path.set(path)
            
            # Reset the highlight
            self.entry_widgets[target_widget_key].config(style='TEntry')
        
        def drag_enter(event, target_widget_key):
            # Highlight the entry widget when dragging over it
            self.entry_widgets[target_widget_key].config(style='Highlight.TEntry')
        
        def drag_leave(event, target_widget_key):
            # Reset the highlight when dragging leaves
            self.entry_widgets[target_widget_key].config(style='TEntry')
        
        # Set up drag and drop for each entry widget
        for key, widget in self.entry_widgets.items():
            widget.drop_target_register(DND_FILES)
            widget.dnd_bind('<<Drop>>', lambda e, k=key: drop(e, k))
            widget.dnd_bind('<<DropEnter>>', lambda e, k=key: drag_enter(e, k))
            widget.dnd_bind('<<DropLeave>>', lambda e, k=key: drag_leave(e, k))
    
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
        
        if (old_path and not new_path) or (new_path and not old_path):
            messagebox.showerror("Error", "Both old path and new path must be provided together.")
            return
        
        try:
            # Extract the output filename without extension to use as the composition name
            output_basename = os.path.basename(output_file)
            output_name = os.path.splitext(output_basename)[0]
            
            summary = adjust_composition(
                input_file,
                output_file,
                old_path if old_path else None,
                new_path if new_path else None,
                resolution_factor,
                framerate_factor,
                new_name=output_name
            )
            messagebox.showinfo("Processing Complete", summary)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during processing: {str(e)}")

    def open_manual_pdf(self):
        """Open the PDF manual"""
        try:
            # Check if we're running from the bundled app
            import sys
            import os
            import subprocess
            import platform
            
            # Determine the path to the manual based on whether we're running from the app bundle
            if getattr(sys, 'frozen', False):
                # Running from the bundled app
                if platform.system() == 'Darwin':  # macOS
                    manual_path = os.path.join(os.path.dirname(sys.executable),
                                              '../Resources/MANUAL.pdf')
                else:
                    manual_path = os.path.join(os.path.dirname(sys.executable),
                                              'resources/MANUAL.pdf')
            else:
                # Running from source
                manual_path = 'MANUAL.pdf'
                
                # If the PDF doesn't exist, try to create it
                if not os.path.exists(manual_path):
                    messagebox.showinfo("Opening Manual",
                                       "The PDF manual doesn't exist yet. Opening the Markdown version instead.")
                    self.open_manual_markdown()
                    return
            
            # Open the PDF with the default application
            if platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', manual_path])
            elif platform.system() == 'Windows':  # Windows
                os.startfile(manual_path)
            else:  # Linux
                subprocess.run(['xdg-open', manual_path])
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not open the manual: {str(e)}")
            # Fallback to opening the markdown file
            self.open_manual_markdown()
    
    def open_manual_html(self):
        """Open the HTML manual"""
        try:
            # Check if we're running from the bundled app
            import sys
            import os
            import subprocess
            import platform
            
            # Determine the path to the manual based on whether we're running from the app bundle
            if getattr(sys, 'frozen', False):
                # Running from the bundled app
                if platform.system() == 'Darwin':  # macOS
                    manual_path = os.path.join(os.path.dirname(sys.executable),
                                              '../Resources/MANUAL.html')
                else:
                    manual_path = os.path.join(os.path.dirname(sys.executable),
                                              'resources/MANUAL.html')
            else:
                # Running from source
                manual_path = 'MANUAL.html'
                
                # If the HTML doesn't exist, try to create it
                if not os.path.exists(manual_path):
                    messagebox.showinfo("Opening Manual",
                                       "The HTML manual doesn't exist yet. Opening the Markdown version instead.")
                    self.open_manual_markdown()
                    return
            
            # Open the HTML with the default browser
            if platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', manual_path])
            elif platform.system() == 'Windows':  # Windows
                os.startfile(manual_path)
            else:  # Linux
                subprocess.run(['xdg-open', manual_path])
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not open the manual: {str(e)}")
            # Fallback to opening the markdown file
            self.open_manual_markdown()
    
    def open_manual_markdown(self):
        """Open the Markdown manual"""
        try:
            # Check if we're running from the bundled app
            import sys
            import os
            import subprocess
            import platform
            
            # Determine the path to the manual based on whether we're running from the app bundle
            if getattr(sys, 'frozen', False):
                # Running from the bundled app
                if platform.system() == 'Darwin':  # macOS
                    manual_path = os.path.join(os.path.dirname(sys.executable),
                                              '../Resources/MANUAL.md')
                else:
                    manual_path = os.path.join(os.path.dirname(sys.executable),
                                              'resources/MANUAL.md')
            else:
                # Running from source
                manual_path = 'MANUAL.md'
            
            # Open the Markdown file with the default application
            if platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', manual_path])
            elif platform.system() == 'Windows':  # Windows
                os.startfile(manual_path)
            else:  # Linux
                subprocess.run(['xdg-open', manual_path])
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not open the manual: {str(e)}")
            
    def show_about(self):
        """Show the About dialog"""
        messagebox.showinfo("About",
                           "Resolume Composition Converter\n\n"
                           "Version 1.0.0\n\n"
                           "A tool for converting Resolume Arena compositions to different resolutions and frame rates.\n\n"
                           "© 2025 Resolume Composition Converter")

# ----------------------
#       MAIN APP
# ----------------------
if __name__ == "__main__":
    # Initialize TkinterDnD if available
    if DRAG_DROP_ENABLED:
        root = TkinterDnD.Tk()
    else:
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
    help_menu.add_command(label="User Manual", command=app.open_manual_html)
    help_menu.add_separator()
    help_menu.add_command(label="About", command=app.show_about)
    
    # Add Help menu to menu bar
    menubar.add_cascade(label="Help", menu=help_menu)
    
    # Configure the menu bar
    root.config(menu=menubar)
    
    root.mainloop()
