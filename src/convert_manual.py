#!/usr/bin/env python3
"""
Script to convert MANUAL.md to PDF and HTML formats for distribution
Requires: pandoc, wkhtmltopdf
"""

import os
import subprocess
import sys

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        subprocess.run(['pandoc', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Error: pandoc is not installed. Please install it first:")
        print("  macOS: brew install pandoc")
        print("  Windows: choco install pandoc")
        print("  Linux: sudo apt-get install pandoc")
        return False
    
    return True

def convert_to_pdf():
    """Convert MANUAL.md to PDF"""
    print("Converting MANUAL.md to PDF...")
    try:
        subprocess.run([
            'pandoc',
            'MANUAL.md',
            '-o', 'dist/Resolume Composition Converter.app/Contents/Resources/MANUAL.pdf',
            '--pdf-engine=wkhtmltopdf',
            '--variable', 'margin-top=20',
            '--variable', 'margin-right=20',
            '--variable', 'margin-bottom=20',
            '--variable', 'margin-left=20',
            '--toc'
        ], check=True)
        print("PDF created successfully: dist/Resolume Composition Converter.app/Contents/Resources/MANUAL.pdf")
    except subprocess.SubprocessError as e:
        print(f"Error creating PDF: {e}")
        return False
    
    return True

def convert_to_html():
    """Convert MANUAL.md to HTML"""
    print("Converting MANUAL.md to HTML...")
    try:
        subprocess.run([
            'pandoc',
            'MANUAL.md',
            '-o', 'dist/Resolume Composition Converter.app/Contents/Resources/MANUAL.html',
            '--standalone',
            '--toc',
            '--css=manual_style.css'
        ], check=True)
        print("HTML created successfully: dist/Resolume Composition Converter.app/Contents/Resources/MANUAL.html")
    except subprocess.SubprocessError as e:
        print(f"Error creating HTML: {e}")
        return False
    
    return True

def create_css():
    """Create a CSS file for styling the HTML manual"""
    css_content = """
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', sans-serif;
        line-height: 1.6;
        color: #333;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    h1, h2, h3, h4 {
        color: #5E5FEC;
    }
    h1 {
        border-bottom: 2px solid #5E5FEC;
        padding-bottom: 10px;
    }
    h2 {
        border-bottom: 1px solid #ddd;
        padding-bottom: 5px;
    }
    code {
        background-color: #f5f5f5;
        padding: 2px 5px;
        border-radius: 3px;
        font-family: monospace;
    }
    pre {
        background-color: #f5f5f5;
        padding: 15px;
        border-radius: 5px;
        overflow-x: auto;
    }
    a {
        color: #5E5FEC;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px 12px;
        text-align: left;
    }
    th {
        background-color: #f2f2f2;
    }
    .toc {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 30px;
    }
    """
    
    try:
        with open('manual_style.css', 'w') as f:
            f.write(css_content)
        
        # Copy to resources directory
        os.makedirs('dist/Resolume Composition Converter.app/Contents/Resources', exist_ok=True)
        with open('dist/Resolume Composition Converter.app/Contents/Resources/manual_style.css', 'w') as f:
            f.write(css_content)
            
        print("CSS file created successfully")
    except IOError as e:
        print(f"Error creating CSS file: {e}")
        return False
    
    return True

def ensure_resources_dir():
    """Ensure the Resources directory exists"""
    os.makedirs('dist/Resolume Composition Converter.app/Contents/Resources', exist_ok=True)

def main():
    """Main function"""
    if not check_dependencies():
        return 1
    
    ensure_resources_dir()
    
    if not create_css():
        return 1
    
    if not convert_to_pdf():
        return 1
    
    if not convert_to_html():
        return 1
    
    print("\nManual conversion complete!")
    print("The manual is now available in PDF and HTML formats in the application bundle.")
    print("Users can access it through the Help menu in the application.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())