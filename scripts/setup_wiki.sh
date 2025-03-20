#!/bin/bash

# Configuration
REPO_OWNER="tijnisfijn"
REPO_NAME="Resolume-Composition-Converter"
WIKI_REPO_URL="https://github.com/$REPO_OWNER/$REPO_NAME.wiki.git"
WIKI_DIR="${REPO_NAME}.wiki"

# Function to check if command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check if git is installed
if ! command_exists git; then
  echo "Error: git is not installed. Please install git and try again."
  exit 1
fi

# Ask for GitHub token
echo "Setting up wiki for repository: $REPO_OWNER/$REPO_NAME"
echo "Please enter your GitHub personal access token (needs repo permissions):"
read -s GITHUB_TOKEN
echo

# Clone the wiki repository
echo "Cloning wiki repository: $WIKI_REPO_URL"
if [ -d "$WIKI_DIR" ]; then
  echo "Directory $WIKI_DIR already exists. Removing it..."
  rm -rf "$WIKI_DIR"
fi

git clone "https://$GITHUB_TOKEN@github.com/$REPO_OWNER/$REPO_NAME.wiki.git" "$WIKI_DIR"
if [ $? -ne 0 ]; then
  echo "Error: Failed to clone wiki repository. Please make sure the wiki is enabled for the repository."
  exit 1
fi

# Copy wiki files
echo "Copying wiki files..."
cp wiki-Home.md "$WIKI_DIR/Home.md"
cp wiki-Recent-Changes.md "$WIKI_DIR/Recent-Changes.md"
cp wiki-Future-Roadmap.md "$WIKI_DIR/Future-Roadmap.md"
cp wiki-Building-from-Source.md "$WIKI_DIR/Building-from-Source.md"
cp wiki-_Sidebar.md "$WIKI_DIR/_Sidebar.md"
cp wiki-_Footer.md "$WIKI_DIR/_Footer.md"

# Commit and push changes
echo "Committing and pushing changes..."
cd "$WIKI_DIR"
git add .
git config user.name "GitHub Actions"
git config user.email "actions@github.com"
git commit -m "Add wiki pages"
git remote set-url origin "https://$GITHUB_TOKEN@github.com/$REPO_OWNER/$REPO_NAME.wiki.git"
git push

cd ..

echo
echo "Wiki setup complete!"
echo "Visit https://github.com/$REPO_OWNER/$REPO_NAME/wiki to view your wiki."