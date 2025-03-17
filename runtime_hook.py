"""
Runtime hook for PyInstaller to fix library loading issues on macOS
"""
import os
import sys

# Get the application bundle path
if getattr(sys, 'frozen', False):
    # Running from the bundled app
    bundle_dir = os.path.dirname(sys.executable)
    
    # Add the Frameworks directory to the library search path
    frameworks_dir = os.path.join(bundle_dir, '../Frameworks')
    if os.path.exists(frameworks_dir):
        os.environ['DYLD_LIBRARY_PATH'] = frameworks_dir
        
        # Also add it to the Python path
        if frameworks_dir not in sys.path:
            sys.path.insert(0, frameworks_dir)
    
    # Add the Resources directory to the library search path
    resources_dir = os.path.join(bundle_dir, '../Resources')
    if os.path.exists(resources_dir):
        if 'DYLD_LIBRARY_PATH' in os.environ:
            os.environ['DYLD_LIBRARY_PATH'] += ':' + resources_dir
        else:
            os.environ['DYLD_LIBRARY_PATH'] = resources_dir
        
        # Also add it to the Python path
        if resources_dir not in sys.path:
            sys.path.insert(0, resources_dir)