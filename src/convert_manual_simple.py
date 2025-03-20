#!/usr/bin/env python3
"""
Simple script to convert MANUAL.md to HTML format for distribution
No external dependencies required
"""

import os
import sys
import shutil

def ensure_resources_dir():
    """Ensure the Resources directory exists"""
    os.makedirs('dist/Resolume Composition Converter.app/Contents/Resources', exist_ok=True)

def copy_markdown_to_resources():
    """Copy the MANUAL.md file to the Resources directory"""
    print("Copying MANUAL.md to Resources directory...")
    try:
        shutil.copy('MANUAL.md', 'dist/Resolume Composition Converter.app/Contents/Resources/MANUAL.md')
        print("MANUAL.md copied successfully")
        return True
    except Exception as e:
        print(f"Error copying MANUAL.md: {e}")
        return False

def copy_screenshot():
    """Copy the screenshot to the Resources directory"""
    print("Copying screenshot to Resources directory...")
    try:
        # Create screenshots directory in Resources if it doesn't exist
        os.makedirs('dist/Resolume Composition Converter.app/Contents/Resources/screenshots', exist_ok=True)
        
        # Copy the screenshot
        if os.path.exists('screenshots/app_screenshot.png'):
            shutil.copy('screenshots/app_screenshot.png',
                       'dist/Resolume Composition Converter.app/Contents/Resources/screenshots/app_screenshot.png')
            print("Screenshot copied successfully")
            return True
        else:
            print("Warning: Screenshot not found at screenshots/app_screenshot.png")
            return False
    except Exception as e:
        print(f"Error copying screenshot: {e}")
        return False

def create_html_version():
    """Create a simple HTML version of the manual"""
    print("Creating HTML version of the manual...")
    try:
        # Try to import markdown module
        try:
            import markdown
            has_markdown = True
        except ImportError:
            print("Markdown module not found. Installing...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown"])
            import markdown
            has_markdown = True
    except Exception:
        print("Could not install markdown module. Creating basic HTML...")
        has_markdown = False
    
    try:
        with open('MANUAL.md', 'r') as f:
            md_content = f.read()
        
        # Create a documentation directory
        os.makedirs('documentation', exist_ok=True)
        
        if has_markdown:
            # Convert markdown to HTML using the markdown module
            html_content = markdown.markdown(md_content, extensions=['tables', 'toc'])
            
            # Add app screenshot at the top
            html_content = f"""<div style="text-align: center; margin-bottom: 30px;">
    <img src="screenshots/app_screenshot.png" alt="Resolume Composition Converter" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
</div>
{html_content}"""
            
            # Add CSS styling
            html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resolume Composition Converter - User Manual</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2, h3, h4 {{
            color: #5E5FEC;
        }}
        h1 {{
            border-bottom: 2px solid #5E5FEC;
            padding-bottom: 10px;
        }}
        h2 {{
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
        }}
        code {{
            background-color: #f5f5f5;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: monospace;
        }}
        pre {{
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        a {{
            color: #5E5FEC;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        img {{
            max-width: 100%;
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
"""
        else:
            # Create a very basic HTML version by just wrapping the markdown in pre tags
            html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Resolume Composition Converter - User Manual</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 20px;
        }}
        pre {{
            white-space: pre-wrap;
            font-family: monospace;
            line-height: 1.5;
        }}
    </style>
</head>
<body>
    <h1>Resolume Composition Converter - User Manual</h1>
    <pre>{md_content}</pre>
</body>
</html>
"""
        
        # Write the HTML to the Resources directory
        with open('dist/Resolume Composition Converter.app/Contents/Resources/MANUAL.html', 'w') as f:
            f.write(html)
        
        print("HTML version created successfully")
        return True
    except Exception as e:
        print(f"Error creating HTML version: {e}")
        return False

def main():
    """Main function"""
    # Ensure directories exist
    ensure_resources_dir()
    os.makedirs('documentation', exist_ok=True)
    
    # Copy screenshot to Resources directory
    copy_screenshot()
    
    # Create HTML version of the manual
    if not create_html_version():
        return 1
    
    # Copy HTML manual to documentation folder
    try:
        shutil.copy('dist/Resolume Composition Converter.app/Contents/Resources/MANUAL.html', 'documentation/MANUAL.html')
        # Also copy the screenshot to documentation folder
        os.makedirs('documentation/screenshots', exist_ok=True)
        if os.path.exists('screenshots/app_screenshot.png'):
            shutil.copy('screenshots/app_screenshot.png', 'documentation/screenshots/app_screenshot.png')
        print("Manual copied to documentation folder")
    except Exception as e:
        print(f"Error copying to documentation folder: {e}")
    
    print("\nManual conversion complete!")
    print("The manual is now available in HTML format in:")
    print("1. The application bundle (accessible through the Help menu)")
    print("2. The 'documentation' folder in the project directory")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())