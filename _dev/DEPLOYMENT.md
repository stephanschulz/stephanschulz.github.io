# Deployment Guide

This guide will help you deploy your personal website to GitHub Pages.

## Prerequisites

- Git installed on your computer
- GitHub account
- Repository access rights

## Step-by-Step Deployment

### 1. Prepare Your Content

Before deploying, customize your site:

- [ ] Add your profile picture as `assets/avatar.jpg` (600x600px recommended)
- [ ] Update the About section with your bio
- [ ] Add/modify your projects
- [ ] Update contact information
- [ ] Change social media links
- [ ] Review all content for accuracy

### 2. Create GitHub Repository

**Option A: User/Organization Site** (Recommended)
- Repository name: `stephanschulz.github.io`
- URL will be: `https://stephanschulz.github.io`

**Option B: Project Site**
- Repository name: Any name (e.g., `portfolio`, `website`)
- URL will be: `https://stephanschulz.github.io/repository-name`

### 3. Initialize Git Repository

Open Terminal and run:

```bash
cd /Users/stephanschulz/Documents/cursor_ai/websites/stephanschulz
git init
git add .
git commit -m "Initial commit: Personal portfolio website"
```

### 4. Connect to GitHub

```bash
# For user site:
git remote add origin https://github.com/stephanschulz/stephanschulz.github.io.git

# OR for project site:
# git remote add origin https://github.com/stephanschulz/YOUR-REPO-NAME.git

git branch -M main
git push -u origin main
```

### 5. Configure GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Scroll to **Pages** section (left sidebar)
4. Under "Build and deployment":
   - **Source**: Select "GitHub Actions"
   - The workflow file is already configured in `.github/workflows/deploy.yml`
5. Click **Save**

### 6. Wait for Deployment

- GitHub Actions will automatically build and deploy your site
- Check the **Actions** tab to monitor progress
- Deployment usually takes 1-2 minutes
- You'll see a green checkmark when complete

### 7. Access Your Site

Your site will be live at:
- User site: `https://stephanschulz.github.io/`
- Project site: `https://stephanschulz.github.io/repository-name/`

## Making Updates

After initial deployment, any changes pushed to the `main` branch will automatically trigger a new deployment:

```bash
# Make your changes to files
git add .
git commit -m "Update: description of changes"
git push
```

The site will update automatically within 1-2 minutes.

## Troubleshooting

### Site Not Loading

1. **Check GitHub Actions**: Go to the Actions tab and verify the workflow completed successfully
2. **Verify Pages Settings**: Ensure GitHub Pages is enabled in Settings > Pages
3. **Check Branch**: Make sure you're deploying from the correct branch (usually `main`)
4. **Wait**: Sometimes it takes up to 10 minutes for the first deployment

### Images Not Displaying

1. Check that image paths are correct (case-sensitive)
2. Ensure images are committed to the repository
3. Verify images are in the `assets/` folder
4. Check file extensions match (`.jpg`, `.png`, etc.)

### Custom Domain (Optional)

To use a custom domain:

1. Add a file named `CNAME` to your repository root
2. Inside the file, add your domain: `yourdomain.com`
3. Configure DNS settings with your domain provider:
   - Add A records pointing to GitHub's IPs:
     - 185.199.108.153
     - 185.199.109.153
     - 185.199.110.153
     - 185.199.111.153
   - Or add a CNAME record pointing to: `stephanschulz.github.io`

### Workflow Permissions

If deployment fails with permissions error:

1. Go to **Settings** > **Actions** > **General**
2. Under "Workflow permissions"
3. Select "Read and write permissions"
4. Check "Allow GitHub Actions to create and approve pull requests"
5. Save changes and re-run the workflow

## Advanced Configuration

### Adding Analytics

To add Google Analytics or other tracking:

1. Get your tracking code
2. Add it to the `<head>` section of `index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### SEO Optimization

The site already includes basic SEO meta tags. For enhanced SEO:

1. Add a `sitemap.xml`
2. Create a `robots.txt`
3. Add Open Graph meta tags for social sharing
4. Include structured data (Schema.org)

### Performance Optimization

For faster loading:

1. Compress images before uploading
2. Use WebP format for images
3. Minify CSS and JavaScript (optional)
4. Enable caching headers (via GitHub Pages by default)

## Need Help?

- **GitHub Pages Documentation**: https://docs.github.com/en/pages
- **GitHub Actions Help**: https://docs.github.com/en/actions
- **HTML/CSS/JS Resources**: https://developer.mozilla.org/

---

Good luck with your deployment! 🚀

