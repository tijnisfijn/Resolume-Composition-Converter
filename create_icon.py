from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Create a 1024x1024 image with a gradient background
    img = Image.new('RGBA', (1024, 1024), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Create a gradient background (blue to purple)
    for y in range(1024):
        r = int(94 * (1 - y/1024) + 79 * (y/1024))
        g = int(95 * (1 - y/1024) + 70 * (y/1024))
        b = int(236 * (1 - y/1024) + 220 * (y/1024))
        draw.line([(0, y), (1024, y)], fill=(r, g, b, 255))
    
    # Try to load a font, fall back to default if not available
    try:
        # Try to use a system font
        font = ImageFont.truetype("Arial Bold.ttf", 300)
    except IOError:
        try:
            # Try another common font
            font = ImageFont.truetype("Arial.ttf", 300)
        except IOError:
            # Fall back to default
            font = ImageFont.load_default().font_variant(size=300)
    
    # Add text "RCC" (Resolume Composition Converter)
    text = "RCC"
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
    position = ((1024 - text_width) // 2, (1024 - text_height) // 2)
    
    # Draw text with a slight shadow for depth
    draw.text((position[0]+10, position[1]+10), text, font=font, fill=(0, 0, 0, 100))
    draw.text(position, text, font=font, fill=(255, 255, 255, 255))
    
    # Save as .icns for macOS
    if not os.path.exists('icons'):
        os.makedirs('icons')
    
    # Save as PNG first
    img.save('icons/app_icon.png')
    print("Icon created as icons/app_icon.png")
    print("To convert to .icns format, use the iconutil command on macOS")
    
    # Instructions for converting to .icns
    print("\nTo convert to .icns, follow these steps:")
    print("1. Create iconset directory: mkdir -p icons/app_icon.iconset")
    print("2. Create different sizes:")
    print("   sips -z 16 16 icons/app_icon.png --out icons/app_icon.iconset/icon_16x16.png")
    print("   sips -z 32 32 icons/app_icon.png --out icons/app_icon.iconset/icon_16x16@2x.png")
    print("   sips -z 32 32 icons/app_icon.png --out icons/app_icon.iconset/icon_32x32.png")
    print("   sips -z 64 64 icons/app_icon.png --out icons/app_icon.iconset/icon_32x32@2x.png")
    print("   sips -z 128 128 icons/app_icon.png --out icons/app_icon.iconset/icon_128x128.png")
    print("   sips -z 256 256 icons/app_icon.png --out icons/app_icon.iconset/icon_128x128@2x.png")
    print("   sips -z 256 256 icons/app_icon.png --out icons/app_icon.iconset/icon_256x256.png")
    print("   sips -z 512 512 icons/app_icon.png --out icons/app_icon.iconset/icon_256x256@2x.png")
    print("   sips -z 512 512 icons/app_icon.png --out icons/app_icon.iconset/icon_512x512.png")
    print("   cp icons/app_icon.png icons/app_icon.iconset/icon_512x512@2x.png")
    print("3. Convert to .icns: iconutil -c icns icons/app_icon.iconset")
    print("4. Update the spec file with the path to the .icns file")

if __name__ == "__main__":
    create_icon()