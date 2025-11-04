# Notion to GitHub Pages Migration Guide

This guide helps you extract content from your Notion page and transfer it to your GitHub Pages site.

## Step 1: Export Your Notion Page

### Desktop Export

1. Open your Notion page: https://antimodularresearch.notion.site/Stephan-Schulz-8d0f5c2871ca4502903f411a0d34208f
2. Click the `•••` menu at the top-right corner
3. Select **Export**
4. Configure export settings:
   - **Export format**: HTML
   - **Include subpages**: ON (to get all nested content)
   - **Create folders for subpages**: ON (recommended)
5. Click **Export**
6. Download the ZIP file

### What You'll Get

The export will contain:
- HTML files for each page
- A folder with images and media
- CSS files (Notion's styling)
- Subpage structure (if you have nested pages)

## Step 2: Extract Content

### 2.1 Text Content

1. Unzip the downloaded file
2. Open the main HTML file in a web browser or text editor
3. Copy the text content you want to migrate
4. Paste into the appropriate sections in `index.html`:

**About Section** → `#about-page`
**Projects/Work** → `#projects-page`  
**Experience** → `#experience-page`
**Contact Info** → `#contact-page`

### 2.2 Images

1. Find images in the export folder (usually named something like `Stephan_Schulz_[hash]/`)
2. Copy images to the `assets/` folder in your GitHub Pages project
3. Rename images appropriately:
   - Profile photo → `avatar.jpg`
   - Project images → `project-1.jpg`, `project-2.jpg`, etc.
4. Update image references in `index.html`:

```html
<!-- Before -->
<img src="Stephan_Schulz_abc123/image.png" alt="Description">

<!-- After -->
<img src="assets/project-1.jpg" alt="Description">
```

## Step 3: Map Notion Content to HTML Structure

### Notion Page Structure → HTML Sections

| Notion Section | HTML Location | File | Element ID |
|---------------|---------------|------|-----------|
| Main Title | Page header | index.html | `.page-title` |
| About/Bio | About page | index.html | `#about-page` |
| Projects | Projects page | index.html | `#projects-page` |
| Work History | Experience page | index.html | `#experience-page` |
| Contact Info | Contact page | index.html | `#contact-page` |

### Content Mapping Examples

#### Notion Heading 1 → HTML
```html
<!-- Notion: # Large Heading -->
<h1 class="page-title">Large Heading</h1>
```

#### Notion Heading 2 → HTML
```html
<!-- Notion: ## Section Title -->
<h2>Section Title</h2>
```

#### Notion Paragraph → HTML
```html
<!-- Notion: Regular text paragraph -->
<p>Regular text paragraph</p>
```

#### Notion Bulleted List → HTML
```html
<!-- Notion: 
• Item 1
• Item 2
-->
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
</ul>
```

#### Notion Callout/Highlight → HTML
```html
<!-- Notion: Callout box -->
<div class="content-block">
  <p>Important information here</p>
</div>
```

#### Notion Tags/Labels → HTML
```html
<!-- Notion: Tags -->
<div class="tag-list">
  <span class="tag">Tag 1</span>
  <span class="tag">Tag 2</span>
</div>
```

## Step 4: Preserve Notion Aesthetics

The GitHub Pages site already includes Notion-inspired styling:

### Colors
- Background: Light beige/cream (`#f7f6f3`)
- Text: Dark gray (`#37352f`)
- Accent: Blue (`#2383e2`)
- Borders: Subtle gray (`#e9e9e7`)

### Typography
- System fonts (matching Notion)
- Clean hierarchy (40px → 24px → 16px)
- Generous spacing

### Layout
- Clean sidebar navigation
- Wide content area
- Card-based project layout
- Smooth page transitions

## Step 5: Handle Notion-Specific Features

### Databases → Project Cards

If you have a Notion database for projects:

```html
<!-- Convert each database entry to a project card -->
<div class="project-card">
  <div class="project-header">
    <h3>Project Name</h3>
    <span class="project-lang">Technology</span>
  </div>
  <p class="project-description">Description from Notion</p>
  <div class="project-stats">
    <span>⭐ Stars</span>
  </div>
  <a href="project-url" class="project-link">View Project →</a>
</div>
```

### Toggle Lists → Expandable Sections

For Notion toggle lists, you can use details/summary:

```html
<details>
  <summary>Click to expand</summary>
  <p>Hidden content here</p>
</details>
```

Add this CSS to style it like Notion:

```css
details {
  margin-bottom: 1rem;
  padding: 0.5rem;
  background: var(--bg-secondary);
  border-radius: 4px;
}

summary {
  cursor: pointer;
  font-weight: 500;
}
```

### Embeds → iframes

```html
<!-- For embedded content -->
<div class="embed-container">
  <iframe src="embed-url" frameborder="0" allowfullscreen></iframe>
</div>
```

## Step 6: Quality Check

Before deploying, verify:

- [ ] All text content is transferred
- [ ] Images are displaying correctly
- [ ] Links work (both internal and external)
- [ ] Page navigation functions properly
- [ ] Mobile responsive design looks good
- [ ] Dark mode works (if content supports it)

## Quick Content Transfer Workflow

1. **Open two windows**: 
   - Notion page (exported HTML in browser)
   - Your `index.html` in code editor

2. **Copy section by section**:
   - Select content in Notion HTML
   - Paste into appropriate section in index.html
   - Clean up HTML tags
   - Replace Notion-specific classes with site classes

3. **Download all images**:
   - Right-click → Save images from Notion export
   - Move to `assets/` folder
   - Update image paths in HTML

4. **Test locally**:
   ```bash
   python -m http.server 8000
   ```
   Visit: http://localhost:8000

5. **Deploy**:
   ```bash
   git add .
   git commit -m "Add content from Notion"
   git push
   ```

## Automation Tools (Optional)

For large Notion exports, consider these tools:

- **Notion API**: Use official API to extract content programmatically
- **notion-to-md**: Convert Notion pages to Markdown
- **Loconotion**: Generate static sites from Notion (alternative approach)

## Tips for Best Results

1. **Simplify Structure**: Notion's nested pages → Flat sections on single page
2. **Optimize Images**: Compress before adding to avoid slow load times
3. **Clean HTML**: Remove Notion's inline styles and use site CSS classes
4. **Preserve Links**: Update internal Notion links to section anchors (#about, #projects)
5. **Test Thoroughly**: Check all browsers and mobile devices

## Need Help?

If you encounter issues:

1. Check the browser console for errors
2. Validate HTML: https://validator.w3.org/
3. Test images paths (case-sensitive on GitHub Pages)
4. Review the deployed site vs. local version

---

Remember: The goal is to preserve the _feel_ of your Notion page while leveraging the benefits of a static GitHub Pages site (speed, control, custom domain, etc.)

