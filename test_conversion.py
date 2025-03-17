from resolume_gui import adjust_composition

# Test with the sample file
input_file = "test files/UpscaleComp.avc"
output_file = "test files/UpscaleComp_converted.avc"

# Use a resolution factor of 2.0 (e.g., 1080p to 4K)
resolution_factor = 2.0
framerate_factor = 2.4  # e.g., 25fps to 60fps

# Run the conversion
summary = adjust_composition(
    input_file,
    output_file,
    resolution_factor=resolution_factor,
    framerate_factor=framerate_factor
)

print(summary)