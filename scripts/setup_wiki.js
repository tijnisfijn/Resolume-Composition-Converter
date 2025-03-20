#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Configuration
const REPO_OWNER = 'tijnisfijn';
const REPO_NAME = 'Resolume-Composition-Converter';
const WIKI_FILES = [
  { source: 'wiki-Home.md', destination: 'Home.md' },
  { source: 'wiki-Recent-Changes.md', destination: 'Recent-Changes.md' },
  { source: 'wiki-Future-Roadmap.md', destination: 'Future-Roadmap.md' },
  { source: 'wiki-Building-from-Source.md', destination: 'Building-from-Source.md' },
  { source: 'wiki-_Sidebar.md', destination: '_Sidebar.md' },
  { source: 'wiki-_Footer.md', destination: '_Footer.md' }
];

// Main function
async function setupWiki() {
  console.log('Setting up wiki for repository:', `${REPO_OWNER}/${REPO_NAME}`);
  
  // Step 1: Clone the wiki repository (will fail if it doesn't exist yet)
  const wikiRepoUrl = `https://github.com/${REPO_OWNER}/${REPO_NAME}.wiki.git`;
  const wikiDir = `${REPO_NAME}.wiki`;
  
  try {
    // Try to clone the wiki repository
    console.log(`Cloning wiki repository: ${wikiRepoUrl}`);
    execSync(`git clone ${wikiRepoUrl}`, { stdio: 'inherit' });
    console.log('Wiki repository cloned successfully.');
  } catch (error) {
    // If cloning fails, create the wiki repository
    console.log('Wiki repository does not exist yet. Creating it...');
    
    // Create the wiki directory
    if (!fs.existsSync(wikiDir)) {
      fs.mkdirSync(wikiDir);
    }
    
    // Initialize git repository
    console.log(`Initializing git repository in ${wikiDir}`);
    execSync(`cd ${wikiDir} && git init`, { stdio: 'inherit' });
    
    // Add remote
    console.log(`Adding remote: ${wikiRepoUrl}`);
    execSync(`cd ${wikiDir} && git remote add origin ${wikiRepoUrl}`, { stdio: 'inherit' });
  }
  
  // Step 2: Copy wiki files
  console.log('Copying wiki files...');
  for (const file of WIKI_FILES) {
    const sourceFile = file.source;
    const destinationFile = path.join(wikiDir, file.destination);
    
    console.log(`Copying ${sourceFile} to ${destinationFile}`);
    const content = fs.readFileSync(sourceFile, 'utf8');
    fs.writeFileSync(destinationFile, content);
  }
  
  // Step 3: Commit and push changes
  console.log('Committing and pushing changes...');
  try {
    execSync(`cd ${wikiDir} && git add .`, { stdio: 'inherit' });
    execSync(`cd ${wikiDir} && git commit -m "Add wiki pages"`, { stdio: 'inherit' });
    execSync(`cd ${wikiDir} && git push -u origin master`, { stdio: 'inherit' });
    console.log('Wiki pages pushed successfully!');
  } catch (error) {
    console.error('Error committing or pushing changes:', error.message);
    console.log('You may need to create the first wiki page manually through the GitHub web interface before pushing changes.');
  }
  
  console.log('\nWiki setup complete!');
  console.log(`Visit https://github.com/${REPO_OWNER}/${REPO_NAME}/wiki to view your wiki.`);
}

// Run the main function
setupWiki().catch(error => {
  console.error('Error setting up wiki:', error);
  process.exit(1);
});