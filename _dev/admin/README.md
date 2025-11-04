# Project Admin Interface

A local web-based interface for adding new projects to your portfolio site.

## Features

- **Live Preview**: See how your project will look as you type
- **Image Management**: Select images from a folder and reorder them with drag-and-drop
- **Auto-Generation**: Automatically creates numbered images (01_image.jpg, 02_image.png, etc.) and cover images
- **File Creation**: Generates all necessary files (HTML, images, updates projects-data.json)
- **Notion-style UI**: Clean interface matching your site's aesthetic

## Requirements

Install Flask if you haven't already:

```bash
pip install flask
# or
python3 -m pip install flask
```

Existing dependencies (already installed):
- Pillow (for image processing)
- Python 3.9+

## Usage

### 1. Start the Admin Server

From your project root:

```bash
python3 _dev/admin-server.py
```

The admin interface will automatically open in your browser at http://localhost:5000/admin

### 2. Fill in Project Details

Required fields:
- **Project Name**: e.g., "Dark Ride"
- **Year**: e.g., "2024"
- **Collaborator/For**: e.g., "Rafael Lozano-Hemmer"
- **I Did/Role**: e.g., "Hardware, Software" (comma-separated)

Optional fields:
- **Official Site**: Project URL
- **Description**: Main project text (use double line breaks for paragraphs)
- **Acknowledgment**: Custom acknowledgment (auto-added for Rafael Lozano-Hemmer projects)

### 3. Load Images

1. Paste the full path to your images folder
   - Example: `/Users/yourname/Desktop/project-images`
2. Click "Load Images"
3. Drag to reorder (the order determines 01_image, 02_image, etc.)
4. Remove unwanted images with the × button

### 4. Create Project

1. Review the live preview on the right
2. Click "Create Project"
3. Wait for confirmation
4. You'll be redirected to your new project page!

## What Happens When You Submit

The system automatically:

1. **Generates slug**: Creates URL-friendly name (e.g., "dark-ride-2024")
2. **Creates folders**: `projects/dark-ride-2024/` and `projects/dark-ride-2024/images/`
3. **Copies images**: From your source folder to project folder
4. **Renames images**: To 01_image.jpg, 02_image.png, etc. based on order
5. **Generates cover**: Creates cover.jpg (900×600, 3:2 ratio) from first image
6. **Creates HTML**: Generates projects/dark-ride-2024/index.html
7. **Updates index**: Adds project to projects-data.json
8. **Sorts projects**: Automatically sorts by year (newest first)

## Tips

- **Image Order**: The first image becomes the cover, so choose wisely!
- **Rafael Lozano-Hemmer**: Projects for him get a special acknowledgment footer automatically
- **Paragraphs**: Use double line breaks in the description for new paragraphs
- **Tags**: Separate multiple roles with commas (e.g., "Hardware, Software, Animation")
- **Preview**: The preview updates in real-time as you type

## Troubleshooting

### Images don't load
- Make sure you paste the **full absolute path** to the folder
- Check that the folder contains .jpg, .png, or .gif files
- On Mac: Right-click folder → Get Info → copy path

### Can't start server
```bash
# Install Flask
python3 -m pip install flask

# If port 5000 is busy, edit admin-server.py and change:
app.run(debug=True, port=5000)
# to a different port like 5001
```

### Images show as broken in preview
- This is normal! File:// URLs work in the preview
- Images will display correctly on the actual site

## File Structure Created

```
projects/
  your-project-2024/
    index.html              ← Project detail page
    images/
      cover.jpg             ← Auto-generated (900×600)
      01_image.jpg          ← First image
      02_image.png          ← Second image
      03_image.jpg          ← Third image
      ...
```

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## Security Note

This admin interface runs **locally only** and is not meant to be deployed to a web server. It has direct filesystem access and is designed for your development environment only.

