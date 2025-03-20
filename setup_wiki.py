#!/usr/bin/env python3
"""
Script to set up GitHub wiki pages using the GitHub API.
"""

import os
import sys
import requests
import json
import base64

# Configuration
REPO_OWNER = 'tijnisfijn'
REPO_NAME = 'Resolume-Composition-Converter'
WIKI_FILES = [
    {'source': 'wiki-Home.md', 'destination': 'Home'},
    {'source': 'wiki-Recent-Changes.md', 'destination': 'Recent-Changes'},
    {'source': 'wiki-Future-Roadmap.md', 'destination': 'Future-Roadmap'},
    {'source': 'wiki-Building-from-Source.md', 'destination': 'Building-from-Source'},
    {'source': 'wiki-_Sidebar.md', 'destination': '_Sidebar'},
    {'source': 'wiki-_Footer.md', 'destination': '_Footer'}
]

def get_github_token():
    """Get GitHub token from environment variable or prompt user."""
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        token = input("Enter your GitHub personal access token: ")
    return token

def create_wiki_page(token, page_name, content):
    """Create a wiki page using the GitHub API."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pages"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'name': page_name,
        'content': content,
        'message': f'Create {page_name} wiki page'
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"Successfully created wiki page: {page_name}")
        return True
    else:
        print(f"Failed to create wiki page: {page_name}")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def main():
    """Main function to set up wiki pages."""
    print(f"Setting up wiki for repository: {REPO_OWNER}/{REPO_NAME}")
    
    # Get GitHub token
    token = get_github_token()
    if not token:
        print("GitHub token is required to create wiki pages.")
        sys.exit(1)
    
    # Create wiki pages
    for file_info in WIKI_FILES:
        source_file = file_info['source']
        destination_page = file_info['destination']
        
        print(f"Creating wiki page: {destination_page} from {source_file}")
        
        try:
            with open(source_file, 'r') as f:
                content = f.read()
            
            success = create_wiki_page(token, destination_page, content)
            if not success:
                print(f"Failed to create wiki page: {destination_page}")
        except Exception as e:
            print(f"Error creating wiki page {destination_page}: {str(e)}")
    
    print("\nWiki setup complete!")
    print(f"Visit https://github.com/{REPO_OWNER}/{REPO_NAME}/wiki to view your wiki.")

if __name__ == "__main__":
    main()