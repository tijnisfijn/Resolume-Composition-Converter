#!/usr/bin/env python
# update_checker.py - Update checking functionality for Resolume Composition Converter

import requests
import json
import time
import os
from version import get_version, is_newer_version

# GitHub API URL for releases
GITHUB_API_URL = "https://api.github.com/repos/tijnisfijn/Resolume-Composition-Converter/releases/latest"
# How often to check for updates (in seconds) - 7 days
UPDATE_CHECK_INTERVAL = 7 * 24 * 60 * 60
# File to store last check timestamp
LAST_CHECK_FILE = "last_update_check.json"

def get_latest_version():
    """
    Query GitHub API to get the latest release version
    Returns: (version_string, download_url, release_notes) or None if error
    """
    try:
        response = requests.get(GITHUB_API_URL, timeout=5)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        version = data.get('tag_name', '').lstrip('v')  # Remove 'v' prefix if present
        download_url = data.get('html_url', '')
        release_notes = data.get('body', '')
        
        return (version, download_url, release_notes)
    except (requests.RequestException, json.JSONDecodeError, KeyError) as e:
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
        os.makedirs(os.path.dirname(LAST_CHECK_FILE), exist_ok=True)
        
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