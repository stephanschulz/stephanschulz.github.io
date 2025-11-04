# How to Add Your Project Images

Your website is ready, but you need to add the project images from your Notion page. Here's exactly how to do it:

## Quick Start

You need **8 images** from your Notion page placed in the `assets/projects/` folder.

## Step 1: Export from Notion

### Method A: Download Images Directly (Recommended)

1. Open your Notion page: https://antimodularresearch.notion.site/Stephan-Schulz-8d0f5c2871ca4502903f411a0d34208f
2. **Right-click** on each project image
3. Select **"Save Image As..."** or **"Download Image"**
4. Save with these exact names:
   - `pulsos-del-agua.jpg`
   - `transparency-display.jpg`
   - `pulse-agglomerate.jpg`
   - `climate-parliament.jpg`
   - `pulse-voronoi.jpg`
   - `kristallstimmen.jpg`
   - `dark-ride.jpg`
   - `collider.jpg`

### Method B: Export Entire Notion Page

1. Go to your Notion page
2. Click `•••` menu (top right)
3. Select **Export**
4. Choose **HTML** format
5. Enable **"Include subpages"**
6. Click **Export** and download ZIP
7. Extract the ZIP
8. Find images in the export folder (usually in a subfolder)
9. Rename them to match the list above

## Step 2: Add Images to Your Website

### Option 1: Drag and Drop

1. Open Finder and navigate to:
   ```
   /Users/stephanschulz/Documents/cursor_ai/websites/stephanschulz/assets/projects/
   ```
2. Drag all 8 downloaded images into this folder

### Option 2: Command Line

```bash
# Navigate to projects folder
cd /Users/stephanschulz/Documents/cursor_ai/websites/stephanschulz/assets/projects/

# If images are in your Downloads folder, copy them:
cp ~/Downloads/pulsos-del-agua.jpg .
cp ~/Downloads/transparency-display.jpg .
cp ~/Downloads/pulse-agglomerate.jpg .
# ... (repeat for all 8 images)
```

## Step 3: Optimize Images (Optional but Recommended)

To make your site load faster, compress images:

### Using ImageOptim (Mac - Free)
1. Download from: https://imageoptim.com/
2. Drag all images into ImageOptim
3. It will automatically compress them

### Using TinyPNG (Online - Free)
1. Go to: https://tinypng.com/
2. Upload all images (max 20 at once)
3. Download compressed versions
4. Replace original files

### Using Command Line (if you have ImageMagick)
```bash
cd /Users/stephanschulz/Documents/cursor_ai/websites/stephanschulz/assets/projects/

# Resize and compress all images
for img in *.jpg; do
    convert "$img" -resize 1200x800\> -quality 85 "${img%.jpg}-optimized.jpg"
done
```

## Image Requirements

| Property | Recommendation |
|----------|---------------|
| **Format** | JPG (for photos) or PNG (for graphics) |
| **Resolution** | Minimum 600x400px, ideal 1200x800px |
| **Aspect Ratio** | 3:2 (e.g., 1200x800, 1800x1200) |
| **File Size** | Under 500KB per image |
| **Color Space** | sRGB |

## Step 4: Test Locally

After adding images, test your site:

```bash
cd /Users/stephanschulz/Documents/cursor_ai/websites/stephanschulz
python -m http.server 8000
```

Then visit: http://localhost:8000

You should see all your project images!

## Step 5: Deploy

Once images look good locally:

```bash
cd /Users/stephanschulz/Documents/cursor_ai/websites/stephanschulz
git add assets/projects/
git commit -m "Add project images"
git push
```

Your site will update automatically in 1-2 minutes.

## Troubleshooting

### Images not showing?

**Check filenames match exactly:**
```bash
cd /Users/stephanschulz/Documents/cursor_ai/websites/stephanschulz/assets/projects/
ls -la
```

You should see:
```
pulsos-del-agua.jpg
transparency-display.jpg
pulse-agglomerate.jpg
climate-parliament.jpg
pulse-voronoi.jpg
kristallstimmen.jpg
dark-ride.jpg
collider.jpg
```

**Common issues:**
- ❌ Wrong extension (`.png` instead of `.jpg`)
- ❌ Capitalization wrong (`Pulsos` instead of `pulsos`)
- ❌ Spaces in filename
- ❌ Extra characters or numbers

**Fix filename issues:**
```bash
# Example: Rename incorrectly named file
mv "Pulsos Del Agua.jpg" pulsos-del-agua.jpg
```

### Images too large?

If images are over 1MB each, compress them:

```bash
# Check file sizes
cd assets/projects/
ls -lh

# If any file is > 1MB, compress using online tools or ImageOptim
```

### Want different images?

Edit `index.html` and update the image paths:

```html
<div class="project-image">
    <img src="assets/projects/YOUR-NEW-IMAGE.jpg" alt="Description">
</div>
```

## Quick Reference: File Structure

```
stephanschulz/
├── assets/
│   └── projects/
│       ├── pulsos-del-agua.jpg        ← Add these
│       ├── transparency-display.jpg    ← Add these
│       ├── pulse-agglomerate.jpg       ← Add these
│       ├── climate-parliament.jpg      ← Add these
│       ├── pulse-voronoi.jpg          ← Add these
│       ├── kristallstimmen.jpg        ← Add these
│       ├── dark-ride.jpg              ← Add these
│       ├── collider.jpg               ← Add these
│       └── README.md
├── index.html
├── styles.css
└── script.js
```

## Pro Tips

1. **Batch download**: If Notion doesn't let you download images easily, use browser DevTools:
   - Right-click → Inspect
   - Network tab → Refresh page
   - Filter by "img"
   - Right-click image URLs → Open in new tab → Save

2. **Maintain aspect ratio**: Crop images to 3:2 ratio before uploading for best results

3. **Use descriptive alt text**: Update the `alt` attributes in `index.html` for better accessibility

4. **WebP format**: For even better compression, convert to WebP:
   ```bash
   convert input.jpg -quality 85 output.webp
   ```

---

Need help? The website will still work with placeholder gradients if images are missing, but adding real images makes it look professional!

