# GitHub Wiki Setup Instructions

This document provides instructions for setting up the GitHub wiki for the Resolume Composition Converter project.

## Wiki Files

The following wiki content files have been created:

1. `wiki-Home.md` - The main landing page for the wiki
2. `wiki-Recent-Changes.md` - Documentation of recent changes to the project
3. `wiki-Future-Roadmap.md` - Plans for future development, including AI upscaling integration
4. `wiki-Building-from-Source.md` - Instructions for building the application from source

## Setting Up the Wiki

To set up the wiki, follow these steps:

1. Go to the GitHub repository: https://github.com/tijnisfijn/Resolume-Composition-Converter
2. Click on the "Wiki" tab in the top navigation bar
3. Click on "Create the first page" button
4. For the page title, enter "Home"
5. Copy and paste the content from `wiki-Home.md` into the page content area
6. Click "Save Page"

### Adding Additional Pages

After creating the Home page, add the remaining pages:

1. Click on "New Page" in the top-right corner
2. For each new page:
   - Enter the page title (without the "wiki-" prefix and ".md" suffix)
   - Copy and paste the content from the corresponding file
   - Click "Save Page"

### Page Titles

Use the following titles for each page:
- `wiki-Home.md` → "Home"
- `wiki-Recent-Changes.md` → "Recent Changes"
- `wiki-Future-Roadmap.md` → "Future Roadmap"
- `wiki-Building-from-Source.md` → "Building from Source"

## Sidebar Navigation

After creating all pages, you can set up the sidebar navigation:

1. Create a new page titled "_Sidebar"
2. Add the following content:

```markdown
### Wiki Navigation

* [Home](Home)
* [Recent Changes](Recent-Changes)
* [Future Roadmap](Future-Roadmap)
* [Building from Source](Building-from-Source)
```

3. Click "Save Page"

## Footer

You can also create a footer that appears on all pages:

1. Create a new page titled "_Footer"
2. Add the following content:

```markdown
[Resolume Composition Converter](https://github.com/tijnisfijn/Resolume-Composition-Converter) - A desktop application for converting Resolume Arena composition files (.avc) between different resolutions and frame rates.
```

3. Click "Save Page"

## Maintaining the Wiki

To update the wiki in the future:

1. Navigate to the page you want to edit
2. Click the "Edit" button
3. Make your changes
4. Click "Save Page"

You can also clone the wiki repository locally for more advanced editing:

```bash
git clone https://github.com/tijnisfijn/Resolume-Composition-Converter.wiki.git
```

After making changes locally, you can push them back to GitHub:

```bash
cd Resolume-Composition-Converter.wiki
git add .
git commit -m "Update wiki content"
git push origin master