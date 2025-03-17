#!/usr/bin/env python3
"""
Script to create a distribution folder with the application and documentation
"""

import os
import sys
import shutil
import subprocess

def create_distribution_folder():
    """Create a distribution folder with the application and documentation"""
    print("Creating distribution folder...")
    
    # Create distribution folder
    dist_folder = "Resolume Composition Converter"
    if os.path.exists(dist_folder):
        print(f"Removing existing distribution folder: {dist_folder}")
        try:
            shutil.rmtree(dist_folder)
        except OSError as e:
            print(f"Warning: Could not remove directory: {e}")
            print("Trying to remove files individually...")
            for root, dirs, files in os.walk(dist_folder, topdown=False):
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                    except OSError:
                        pass
                for name in dirs:
                    try:
                        os.rmdir(os.path.join(root, name))
                    except OSError:
                        pass
    
    os.makedirs(dist_folder, exist_ok=True)
    
    # Copy the application
    print("Copying application...")
    app_source = "dist/Resolume Composition Converter.app"
    app_dest = f"{dist_folder}/Resolume Composition Converter.app"
    if os.path.exists(app_source):
        shutil.copytree(app_source, app_dest)
        print(f"Application copied to: {app_dest}")
    else:
        print(f"Error: Application not found at {app_source}")
        return False
    
    # Create Documentation folder
    docs_folder = f"{dist_folder}/Documentation"
    os.makedirs(docs_folder, exist_ok=True)
    
    # Copy documentation
    print("Copying documentation...")
    
    # Copy HTML manual
    if os.path.exists("documentation/MANUAL.html"):
        shutil.copy("documentation/MANUAL.html", f"{docs_folder}/User Manual.html")
        print("HTML manual copied")
    else:
        print("Warning: HTML manual not found")
        
    # Copy macOS README
    if os.path.exists("MAC_README.txt"):
        shutil.copy("MAC_README.txt", f"{dist_folder}/MAC_README.txt")
        print("macOS README copied")
    else:
        print("Warning: macOS README not found")
        
    # Copy launch scripts
    if os.path.exists("launch_resolume_converter.command"):
        shutil.copy("launch_resolume_converter.command", f"{dist_folder}/Launch Resolume Converter.command")
        # Make it executable
        os.chmod(f"{dist_folder}/Launch Resolume Converter.command", 0o755)
        print("Launch script copied")
    else:
        print("Warning: Launch script not found")
        
    if os.path.exists("debug_launch.command"):
        shutil.copy("debug_launch.command", f"{dist_folder}/Debug Launch.command")
        # Make it executable
        os.chmod(f"{dist_folder}/Debug Launch.command", 0o755)
        print("Debug launch script copied")
    else:
        print("Warning: Debug launch script not found")
        
    # Copy shell script
    if os.path.exists("run_resolume_converter.sh"):
        shutil.copy("run_resolume_converter.sh", f"{dist_folder}/Run Resolume Converter.sh")
        # Make it executable
        os.chmod(f"{dist_folder}/Run Resolume Converter.sh", 0o755)
        print("Shell script copied")
    else:
        print("Warning: Shell script not found")
        
    # Copy launcher application
    if os.path.exists("Resolume Launcher.app"):
        shutil.copytree("Resolume Launcher.app", f"{dist_folder}/Resolume Launcher.app", dirs_exist_ok=True)
        print("Launcher application copied")
    else:
        print("Warning: Launcher application not found")
        # Try to create it if it doesn't exist
        if os.path.exists("create_launcher_app.sh"):
            print("Attempting to create launcher application...")
            try:
                subprocess.run(["bash", "create_launcher_app.sh"], check=True)
                print("Launcher application created and copied")
            except Exception as e:
                print(f"Error creating launcher application: {e}")
    
    # Copy screenshots folder
    if os.path.exists("documentation/screenshots"):
        shutil.copytree("documentation/screenshots", f"{docs_folder}/screenshots")
        print("Screenshots copied")
    else:
        # Create screenshots directory if it doesn't exist
        os.makedirs(f"{docs_folder}/screenshots", exist_ok=True)
        # Copy screenshot directly if it exists
        if os.path.exists("screenshots/app_screenshot.png"):
            shutil.copy("screenshots/app_screenshot.png", f"{docs_folder}/screenshots/app_screenshot.png")
            print("Screenshot copied")
        else:
            print("Warning: Screenshots not found")
    
    # Copy README
    if os.path.exists("README.md"):
        shutil.copy("README.md", f"{docs_folder}/README.md")
        print("README copied")
    else:
        print("Warning: README.md not found")
    
    # Copy LICENSE
    if os.path.exists("LICENSE"):
        shutil.copy("LICENSE", f"{docs_folder}/LICENSE")
        print("LICENSE copied")
    else:
        print("Warning: LICENSE not found")
    
    # Create a simple HTML index file that links to the manual
    index_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resolume Composition Converter - Documentation</title>
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
        a {{
            color: #5E5FEC;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .app-screenshot {{
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <h1>Resolume Composition Converter</h1>
    
    <div style="text-align: center;">
        <img src="screenshots/app_screenshot.png" alt="Resolume Composition Converter" class="app-screenshot">
    </div>
    
    <h2>Documentation</h2>
    <ul>
        <li><a href="User Manual.html">User Manual</a> - Detailed instructions on using the application</li>
        <li><a href="README.md">README</a> - Overview and quick start guide</li>
        <li><a href="LICENSE">License</a> - MIT License</li>
    </ul>
    
    <h2>Installation</h2>
    <p>To install the application, simply drag the "Resolume Composition Converter.app" to your Applications folder.</p>
    
    <h2>Getting Started</h2>
    <ol>
        <li>Launch the application from your Applications folder</li>
        <li>Select your input composition file (.avc)</li>
        <li>Choose an output location for the converted file</li>
        <li>Set your desired resolution and frame rate</li>
        <li>Click "Convert Composition"</li>
    </ol>
    
    <p>For more detailed instructions, please refer to the <a href="User Manual.html">User Manual</a>.</p>
</body>
</html>
"""
    
    with open(f"{docs_folder}/index.html", "w") as f:
        f.write(index_html)
    print("Documentation index created")
    
    print(f"\nDistribution folder created successfully: {dist_folder}")
    print("Contents:")
    print(f"- {dist_folder}/Resolume Composition Converter.app")
    print(f"- {dist_folder}/Documentation/")
    
    return True

def create_zip():
    """Create a ZIP archive of the distribution folder"""
    print("\nCreating ZIP archive...")
    dist_folder = "Resolume Composition Converter"
    if not os.path.exists(dist_folder):
        print(f"Error: Distribution folder not found: {dist_folder}")
        return False
    
    try:
        shutil.make_archive(dist_folder, 'zip', '.', dist_folder)
        print(f"ZIP archive created: {dist_folder}.zip")
        return True
    except Exception as e:
        print(f"Error creating ZIP archive: {e}")
        return False

def main():
    """Main function"""
    if not create_distribution_folder():
        return 1
    
    create_zip()
    
    print("\nDistribution package created successfully!")
    print("You can now distribute the folder or the ZIP archive.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())