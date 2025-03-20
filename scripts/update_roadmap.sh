#!/bin/bash

# Configuration
REPO_OWNER="tijnisfijn"
REPO_NAME="Resolume-Composition-Converter"
WIKI_REPO_URL="https://github.com/$REPO_OWNER/$REPO_NAME.wiki.git"
WIKI_DIR="${REPO_NAME}.wiki"

# Ask for GitHub token
echo "Updating Future Roadmap page for repository: $REPO_OWNER/$REPO_NAME"
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
  echo "Error: Failed to clone wiki repository."
  exit 1
fi

# Copy updated Future Roadmap page
echo "Updating Future Roadmap page..."
cp wiki-Future-Roadmap-Updated.md "$WIKI_DIR/Future-Roadmap.md"

# Commit and push changes
echo "Committing and pushing changes..."
cd "$WIKI_DIR"
git add Future-Roadmap.md
git config user.name "GitHub Actions"
git config user.email "actions@github.com"
git commit -m "Update Future Roadmap page to emphasize open-source collaboration"
git remote set-url origin "https://$GITHUB_TOKEN@github.com/$REPO_OWNER/$REPO_NAME.wiki.git"
git push

cd ..

echo
echo "Future Roadmap page updated successfully!"
echo "Visit https://github.com/$REPO_OWNER/$REPO_NAME/wiki/Future-Roadmap to view the updated page."