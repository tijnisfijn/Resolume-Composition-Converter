#!/usr/bin/env python
# update_checker.py - Update checking functionality for Resolume Composition Converter

import json
import os
import platform
import time
import urllib.error
import urllib.request
from version import get_version, is_newer_version

# GitHub API URL for releases
GITHUB_API_URL = "https://api.github.com/repos/tijnisfijn/Resolume-Composition-Converter/releases/latest"
# How often to check for updates (in seconds) - 7 days
UPDATE_CHECK_INTERVAL = 7 * 24 * 60 * 60
# File to store last check timestamp
def _get_update_check_file():
    system = platform.system()
    if system == "Windows":
        base = os.getenv("LOCALAPPDATA") or os.getenv("APPDATA") or os.path.expanduser("~")
        return os.path.join(base, "Resolume Composition Converter", "last_update_check.json")
    if system == "Darwin":
        base = os.path.expanduser("~/Library/Application Support")
        return os.path.join(base, "Resolume Composition Converter", "last_update_check.json")
    base = os.getenv("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
    return os.path.join(base, "resolume-composition-converter", "last_update_check.json")

LAST_CHECK_FILE = _get_update_check_file()

def get_latest_version():
    """
    Query GitHub API to get the latest release version
    Returns: (version_string, download_url, release_notes) or None if error
    """
    try:
        req = urllib.request.Request(
            GITHUB_API_URL,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "Resolume-Composition-Converter",
            },
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
        version = data.get('tag_name', '').lstrip('v')  # Remove 'v' prefix if present
        download_url = data.get('html_url', '')
        release_notes = data.get('body', '')

        return (version, download_url, release_notes)
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, KeyError) as e:
        print(f"Error checking for updates: {e}")
        return None

def should_check_for_updates():
    """Determine if it's time to check for updates based on last check time"""
    try:
        with open(LAST_CHECK_FILE, 'r') as f:
            data = json.load(f)
            last_check = data.get('last_check', 0)
            return (time.time() - last_check) >= UPDATE_CHECK_INTERVAL
    except (FileNotFoundError, json.JSONDecodeError):
        return True  # If file doesn't exist or is invalid, check for updates

def update_last_check_time():
    """Update the timestamp of the last update check"""
    try:
        # Ensure the directory exists
        dir_path = os.path.dirname(LAST_CHECK_FILE)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        
        with open(LAST_CHECK_FILE, 'w') as f:
            json.dump({'last_check': time.time()}, f)
    except Exception as e:
        print(f"Error updating last check time: {e}")

def check_for_updates(force=False):
    """
    Check if a newer version is available
    
    Args:
        force: If True, check regardless of the last check time
        
    Returns: 
        (is_update_available, version, download_url, release_notes) or 
        (False, None, None, None) if error
    """
    if not force and not should_check_for_updates():
        return (False, None, None, None)
    
    update_last_check_time()
    result = get_latest_version()
    
    if result is None:
        return (False, None, None, None)
    
    latest_version, download_url, release_notes = result
    current_version = get_version()
    
    if is_newer_version(current_version, latest_version):
        return (True, latest_version, download_url, release_notes)
    
    return (False, latest_version, download_url, release_notes)
