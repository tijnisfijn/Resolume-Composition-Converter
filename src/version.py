#!/usr/bin/env python
# version.py - Centralized version management for Resolume Composition Converter

VERSION = "1.1.1"  # Current application version

def get_version():
    """Return the current application version"""
    return VERSION

def parse_version(version_string):
    """
    Parse a version string into a tuple for comparison
    
    Args:
        version_string: A version string in the format "MAJOR.MINOR.PATCH"
        
    Returns:
        A tuple of integers (MAJOR, MINOR, PATCH) or (0, 0, 0) if parsing fails
    """
    try:
        return tuple(map(int, version_string.split('.')))
    except (ValueError, AttributeError):
        return (0, 0, 0)  # Default for invalid versions

def is_newer_version(current, latest):
    """
    Compare versions and return True if latest is newer than current
    
    Args:
        current: Current version string
        latest: Latest version string
        
    Returns:
        True if latest is newer than current, False otherwise
    """
    current_parts = parse_version(current)
    latest_parts = parse_version(latest)
    return latest_parts > current_parts