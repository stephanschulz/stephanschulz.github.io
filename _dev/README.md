# Development Files

This folder contains scripts and documentation used for building and maintaining the website. **These files are NOT part of the deployed website.**

## Scripts

### `generate-notion-pages.py`
Main script to generate project pages from Notion export.

**Usage:**
```bash
python3 _dev/generate-notion-pages.py
```

**What it does:**
- Parses Notion HTML exports
- Generates project detail pages in `projects/{slug}/index.html`
- Copies and renames images to numbered format (`01_image.jpg`, `02_image.png`, etc.)
- Auto-generates cover images with 3:2 aspect ratio (900×600px)
- Updates `projects-data.json` with image paths

**Requirements:**
- Python 3.9+
- beautifulsoup4
- Pillow

### `generate-projects.py`
Generates `projects-data.json` from the Notion CSV export.

**Usage:**
```bash
python3 _dev/generate-projects.py
```

### `generate-project-pages.py`
Legacy script (replaced by generate-notion-pages.py).

## Documentation

- `QUICK_START.md` - Quick start guide
- `DEPLOYMENT.md` - Deployment instructions for GitHub Pages
- `CUSTOMIZATION.md` - Customization guide
- `NOTION_EXPORT_GUIDE.md` - How to export from Notion
- `IMAGES_GUIDE.md` - Image organization guide
- `PROJECT_SUMMARY.md` - Project overview
- `SITE_COMPLETE.md` - Completion checklist

## File Organization

```
stephanschulz/
├── _dev/              ← THIS FOLDER (not deployed)
│   ├── *.py           ← Build scripts
│   └── *.md           ← Documentation
├── projects/          ← Deployed
│   └── {slug}/
│       ├── index.html
│       └── images/
├── assets/            ← Deployed
├── index.html         ← Deployed
├── styles.css         ← Deployed
├── script.js          ← Deployed
└── cv.html            ← Deployed
```

## Notes

- This folder should be excluded from deployment
- Already added to `.gitignore` (if applicable)
- Run scripts from project root, not from this folder

