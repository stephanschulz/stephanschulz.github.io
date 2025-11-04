# Admin Edit Interface

A local web interface for editing existing projects on your portfolio website.

## Quick Start

```bash
# Start the edit server
python3 _dev/admin-edit-server.py

# Browser opens automatically to:
# http://localhost:5001/admin/edit
```

## Features

- **Select from dropdown**: All existing projects listed
- **Load project data**: Automatically fills form with current content
- **Live preview**: See changes in real-time as you type
- **Edit everything**: Text, properties, images, order
- **Reorder images**: Drag and drop to change order
- **Replace images**: Load new images from a folder
- **Remove images**: Click × to delete individual images
- **Auto-cover**: Generates new cover image from first image
- **Smart updates**: Only updates what changed

## Workflow

### 1. Select a Project

- Open the dropdown at the top
- Choose the project you want to edit
- Form automatically fills with current data
- Images load in the preview

### 2. Make Changes

**Edit Text Fields:**
- Project name, year, collaborator
- Official site URL
- Role/skills (comma-separated)
- Description (use double line breaks for paragraphs)
- Acknowledgment (leave empty for RLH projects)

**Reorder Existing Images:**
- Drag images up/down in the list
- First image becomes the cover
- Preview updates instantly

**Replace All Images:**
- Paste a folder path containing new images
- Click "Load New Images"
- New images replace existing ones
- Reorder as needed

**Remove Images:**
- Click the × button on any image
- Image is removed immediately

### 3. Save Changes

- Click "Update Project"
- Wait 2.5 seconds for files to be written
- Automatically redirects to updated page
- Check main page to see updated tile

## What Gets Updated

When you save changes:

```
projects/{slug}/
  ├── index.html          ← Regenerated with new content
  └── images/
      ├── cover.jpg       ← Regenerated (900×600, 3:2 ratio)
      ├── 01_image.jpg    ← Renumbered based on new order
      ├── 02_image.png    ← etc.
      └── ...

projects-data.json        ← Updated with new metadata
```

## Special Cases

### Changing Project Name or Year

If you change the project name or year:
- A new slug is generated
- The project folder is automatically renamed
- All references in `projects-data.json` are updated
- You'll be redirected to the new URL

### Rafael Lozano-Hemmer Projects

If the collaborator field contains "Rafael Lozano-Hemmer":
- The acknowledgment field is ignored
- A standard RLH acknowledgment is automatically added
- Links to lozano-hemmer.com

### Image Updates

**Option 1: Keep Existing Images**
- Don't load new images
- Only reorder/remove existing ones
- Cover regenerates if order changes

**Option 2: Replace All Images**
- Load new images from a folder
- All existing images are replaced
- New cover generates from first new image

## Running Both Interfaces

You can run both admin interfaces simultaneously:

```bash
# Terminal 1: Create new projects
python3 _dev/admin-server.py        # port 5000

# Terminal 2: Edit existing projects  
python3 _dev/admin-edit-server.py   # port 5001
```

Switch between them as needed!

## Requirements

- Python 3.7+
- Flask (`pip install flask`)
- Pillow (`pip install Pillow`)
- BeautifulSoup4 (`pip install beautifulsoup4`)

## Troubleshooting

**"Project not found" error:**
- Project may not be in `projects-data.json`
- Try recreating with the create interface

**Images not loading:**
- Check that image files still exist
- Verify file permissions

**Preview not updating:**
- Check browser console (F12) for errors
- Refresh the page

**Changes not saving:**
- Check terminal for error messages
- Verify all required fields are filled
- Ensure project folder exists

## Tips

- **Preview is live**: Changes appear as you type
- **First image = cover**: Order matters!
- **Comma-separated roles**: "Hardware, Software, Design"
- **Paragraphs**: Use double line breaks (Enter twice)
- **External links**: Will display domain only (not full URL)
- **Cancel button**: Clears form without saving

## Navigation

From the edit interface:
- **→ Add New Project**: Switch to create interface
- **← Back to Site**: Return to main portfolio page
- **Dropdown**: Switch to different project

## File Structure

```
_dev/
  ├── admin-edit-server.py     # Flask server (port 5001)
  └── admin/
      ├── edit.html            # Edit interface HTML
      ├── edit.js              # Edit interface JavaScript
      ├── admin.css            # Shared styles
      └── README-EDIT.md       # This file
```

---

**Happy editing!** 🎨

