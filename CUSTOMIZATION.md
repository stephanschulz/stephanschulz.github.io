# Customization Guide

This guide shows you how to customize every aspect of your personal website.

## Quick Customization Checklist

- [ ] Add your profile picture
- [ ] Update personal information
- [ ] Add your projects
- [ ] Update social media links
- [ ] Customize colors (optional)
- [ ] Modify page sections (optional)

## 1. Profile Picture

### Adding Your Avatar

**Location**: `assets/avatar.jpg`

1. Choose a professional photo (600x600px or larger recommended)
2. Name it `avatar.jpg`
3. Save it to the `assets/` folder
4. The site will automatically display it

**Alternative**: If no image is added, the site displays your initials "SS"

### Using a Different Image Format

If you want to use PNG or another format:

1. Save your image as `assets/avatar.png` (or .webp, .gif)
2. Update `index.html` line where the avatar is referenced:

```html
<!-- Find this line -->
<img src="assets/avatar.jpg" alt="Stephan Schulz" id="avatar-img">

<!-- Change to -->
<img src="assets/avatar.png" alt="Your Name" id="avatar-img">
```

## 2. Personal Information

### Name and Title

**File**: `index.html`

Find and replace:

```html
<!-- Sidebar header -->
<h1>Stephan Schulz</h1>

<!-- Page title -->
<h1 class="page-title">Stephan Schulz</h1>

<!-- Page subtitle -->
<p class="page-subtitle">Head of R&D at Antimodular Research</p>
```

Change to your name and title.

### About Section

**Location**: `index.html` → `#about-page`

Update your bio:

```html
<div class="content-block">
  <h2>About Me</h2>
  <p>
    [Write your bio here - 2-3 paragraphs about who you are,
    what you do, and what you're passionate about]
  </p>
</div>
```

### Skills/Focus Areas

Update the tags in the About section:

```html
<div class="tag-list">
  <span class="tag">Your Skill 1</span>
  <span class="tag">Your Skill 2</span>
  <span class="tag">Your Skill 3</span>
  <!-- Add more as needed -->
</div>
```

### Contact Information

Update location and organization:

```html
<div class="info-item">
  <span class="info-label">📍 Location</span>
  <span class="info-value">Your City, Country</span>
</div>
<div class="info-item">
  <span class="info-label">🏢 Organization</span>
  <span class="info-value">Your Company</span>
</div>
```

## 3. Projects

### Adding a New Project

**Location**: `index.html` → `#projects-page` → `.projects-grid`

Copy this template and fill in your details:

```html
<div class="project-card">
  <div class="project-header">
    <h3>Project Name</h3>
    <span class="project-lang">Tech Stack</span>
  </div>
  <p class="project-description">
    Brief description of what the project does and why it's interesting
  </p>
  <div class="project-stats">
    <span>⭐ 10</span>
    <span>🔱 2</span>
  </div>
  <a href="https://github.com/yourusername/project" target="_blank" class="project-link">
    View on GitHub →
  </a>
</div>
```

### Removing a Project

Simply delete the entire `<div class="project-card">...</div>` block for that project.

### Adding Project Images

1. Add an image to the project card:

```html
<div class="project-card">
  <img src="assets/project-screenshot.jpg" alt="Project name" style="width: 100%; border-radius: 6px; margin-bottom: 1rem;">
  <!-- rest of project card content -->
</div>
```

2. Save the screenshot to `assets/project-screenshot.jpg`

## 4. Social Media Links

### Updating Links

**Location**: `index.html` → `.sidebar-footer` and `#contact-page`

**Sidebar Links**:
```html
<div class="social-links">
  <a href="https://github.com/YOUR-USERNAME" target="_blank" title="GitHub">
    <!-- GitHub icon SVG -->
  </a>
  <a href="https://twitter.com/YOUR-HANDLE" target="_blank" title="Twitter">
    <!-- Twitter icon SVG -->
  </a>
  <a href="https://YOUR-WEBSITE.com/" target="_blank" title="Website">
    <!-- Website icon SVG -->
  </a>
</div>
```

**Contact Page Cards**:
```html
<a href="https://github.com/YOUR-USERNAME" target="_blank" class="contact-card">
  <!-- Update the href and text -->
</a>
```

### Adding New Social Links

To add LinkedIn, Instagram, etc.:

1. Get an icon from [Heroicons](https://heroicons.com/) or [Simple Icons](https://simpleicons.org/)
2. Add to sidebar:

```html
<a href="https://linkedin.com/in/YOUR-PROFILE" target="_blank" title="LinkedIn">
  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
    <!-- SVG path here -->
  </svg>
</a>
```

## 5. Experience Section

### Adding Work Experience

**Location**: `index.html` → `#experience-page` → `.timeline`

```html
<div class="timeline-item">
  <div class="timeline-marker"></div>
  <div class="timeline-content">
    <h3>Job Title</h3>
    <p class="timeline-company">Company Name</p>
    <p class="timeline-period">2020 - Present</p>
    <p class="timeline-description">
      Description of your role and accomplishments
    </p>
  </div>
</div>
```

### Achievement Badges

Update or add badges:

```html
<div class="achievement-badge">
  <span class="achievement-icon">🏆</span>
  <span>Your Achievement</span>
</div>
```

## 6. Color Customization

### Changing the Color Scheme

**File**: `styles.css`

Find the `:root` section and modify these variables:

```css
:root {
  /* Background colors */
  --bg-primary: #ffffff;          /* Main background */
  --bg-secondary: #f7f6f3;        /* Cards, sidebar */
  --bg-hover: #f1f1ef;            /* Hover states */
  
  /* Text colors */
  --text-primary: #37352f;        /* Main text */
  --text-secondary: #787774;      /* Muted text */
  
  /* Accent color */
  --accent-color: #2383e2;        /* Links, highlights */
  
  /* Borders */
  --border-color: #e9e9e7;        /* Dividers, cards */
}
```

### Pre-made Color Schemes

**Blue (Default)**:
```css
--accent-color: #2383e2;
```

**Green**:
```css
--accent-color: #0f7b6c;
```

**Purple**:
```css
--accent-color: #8b5cf6;
```

**Red/Pink**:
```css
--accent-color: #e63946;
```

### Dark Mode Colors

Modify the dark mode section:

```css
@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #191919;
    --bg-secondary: #2f2f2f;
    --bg-hover: #373737;
    --text-primary: #e3e2e0;
    --text-secondary: #9b9a97;
    --border-color: #373737;
    --sidebar-bg: #252525;
  }
}
```

## 7. Adding New Pages/Sections

### Adding a New Navigation Item

1. **Add navigation link** in sidebar (`index.html`):

```html
<a href="#blog" class="nav-item" data-page="blog">
  <span class="nav-icon">📝</span>
  <span>Blog</span>
</a>
```

2. **Add page content**:

```html
<div class="page" id="blog-page">
  <div class="page-header">
    <h1 class="page-title">Blog</h1>
    <p class="page-subtitle">My thoughts and writing</p>
  </div>
  
  <div class="content-block">
    <!-- Your blog content here -->
  </div>
</div>
```

The navigation will work automatically via JavaScript!

## 8. Typography

### Changing Fonts

To use custom fonts (Google Fonts example):

1. Add to `<head>` in `index.html`:

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

2. Update `styles.css`:

```css
:root {
  --font-body: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
```

### Font Sizes

Modify these in `styles.css`:

```css
.page-title {
  font-size: 40px;  /* Main page titles */
}

.content-block h2 {
  font-size: 24px;  /* Section headings */
}

.content-block p {
  font-size: 16px;  /* Body text */
}
```

## 9. Layout Adjustments

### Sidebar Width

**File**: `styles.css`

```css
.sidebar {
  width: 260px;  /* Change this value */
}

.main-content {
  margin-left: 260px;  /* Must match sidebar width */
}
```

### Content Width

```css
.main-content {
  max-width: 900px;  /* Increase/decrease as desired */
}
```

### Spacing

Adjust spacing variables:

```css
:root {
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;
}
```

## 10. Advanced Customizations

### Adding Animations

Enhance hover effects:

```css
.project-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.project-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 12px 32px var(--shadow);
}
```

### Adding Icons

Use emoji or SVG icons throughout:

```html
<!-- Emoji icons -->
<span class="nav-icon">🚀</span>

<!-- Or use icon libraries -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<i class="fas fa-rocket"></i>
```

### Smooth Scrolling

Already included in `script.js`, but you can modify:

```javascript
target.scrollIntoView({
  behavior: 'smooth',
  block: 'start'
});
```

## Testing Your Changes

After making changes:

1. **Save all files**
2. **Refresh your browser** (Cmd+Shift+R or Ctrl+Shift+R for hard refresh)
3. **Test on mobile**: Use browser dev tools (F12 → Toggle device toolbar)
4. **Check dark mode**: Change system preferences or use browser tools
5. **Validate**: Use https://validator.w3.org/ to check HTML

## Common Issues

### Images not showing
- Check file paths (case-sensitive)
- Ensure images are in `assets/` folder
- Clear browser cache

### Styles not updating
- Hard refresh browser (Cmd+Shift+R)
- Check CSS syntax (missing semicolons, brackets)
- Inspect element to see which styles are applied

### Navigation not working
- Check `data-page` attribute matches page `id`
- Ensure JavaScript is loading (check browser console)

---

Have fun customizing! Remember to commit your changes regularly:

```bash
git add .
git commit -m "Customize: description of changes"
git push
```

