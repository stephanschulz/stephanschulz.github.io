# Quick Start Guide

Get your personal website live in under 10 minutes!

## ⚡ Super Quick Deployment

### Option 1: Automated Script (Easiest)

Run this command:

```bash
cd /Users/stephanschulz/Documents/cursor_ai/websites/stephanschulz
./deploy.sh
```

The script will:
- Initialize git repository
- Ask for your GitHub repository URL
- Commit and push your code
- Provide next steps

### Option 2: Manual Commands

```bash
# 1. Go to project directory
cd /Users/stephanschulz/Documents/cursor_ai/websites/stephanschulz

# 2. Initialize git
git init

# 3. Add all files
git add .

# 4. Commit
git commit -m "Initial commit: Personal website"

# 5. Add your GitHub repository
git remote add origin https://github.com/stephanschulz/stephanschulz.github.io.git

# 6. Push to GitHub
git branch -M main
git push -u origin main
```

### Option 3: GitHub Desktop (Visual)

1. Download [GitHub Desktop](https://desktop.github.com/)
2. Open GitHub Desktop
3. File → Add Local Repository
4. Select: `/Users/stephanschulz/Documents/cursor_ai/websites/stephanschulz`
5. Click "Publish repository"
6. Choose repository name: `stephanschulz.github.io`
7. Uncheck "Keep this code private"
8. Click "Publish repository"

## 🔧 Enable GitHub Pages

1. Go to: https://github.com/stephanschulz/stephanschulz.github.io
2. Click **Settings** tab
3. Click **Pages** in left sidebar
4. Under "Build and deployment":
   - **Source**: Select "GitHub Actions"
5. Done! Your site will deploy automatically

## 🌐 Access Your Site

Wait 1-2 minutes, then visit:

**https://stephanschulz.github.io/**

## ✏️ Make It Yours

### Before Deploying (Recommended)

1. **Add your photo**:
   - Save as `assets/avatar.jpg` (600x600px)

2. **Update your info** in `index.html`:
   - Name
   - Title/Job
   - Bio
   - Location
   - Social links

3. **Add your projects** in `index.html`:
   - Find the `#projects-page` section
   - Update or add project cards

### After Deploying

You can update anytime:

```bash
# Make your changes to files
# Then run:
git add .
git commit -m "Update content"
git push
```

Site updates automatically in 1-2 minutes!

## 📚 Helpful Resources

- **Full README**: See `README.md`
- **Deployment Guide**: See `DEPLOYMENT.md`
- **Customization**: See `CUSTOMIZATION.md`
- **Notion Migration**: See `NOTION_EXPORT_GUIDE.md`

## 🆘 Troubleshooting

### "Permission denied" error
```bash
# Make script executable:
chmod +x deploy.sh
```

### Can't push to GitHub
```bash
# You may need to authenticate with GitHub
# Set up SSH: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
# Or use HTTPS with Personal Access Token
```

### Site not showing up
- Wait 10 minutes (first deploy can be slow)
- Check Settings > Pages is configured correctly
- Check Actions tab for deployment status
- Make sure repository is public

### Images not loading
- Ensure images are in `assets/` folder
- Check file names (case-sensitive on GitHub)
- Hard refresh browser: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

## 💡 Pro Tips

1. **Test locally first**:
   ```bash
   python -m http.server 8000
   # Visit: http://localhost:8000
   ```

2. **Use meaningful commit messages**:
   ```bash
   git commit -m "Add new project: LivePortrait"
   git commit -m "Update about section"
   git commit -m "Fix mobile navigation"
   ```

3. **Preview before pushing**:
   - Check all links work
   - Test on mobile (browser dev tools)
   - Verify images display correctly

4. **Keep it updated**:
   - Add new projects regularly
   - Update your bio and experience
   - Fresh content = better engagement

## 🎯 What's Included

Your website includes:

✅ **Responsive design** - works on all devices  
✅ **Dark mode** - respects system preferences  
✅ **Fast loading** - no frameworks, pure HTML/CSS/JS  
✅ **SEO ready** - proper meta tags and structure  
✅ **Notion-inspired** - clean, modern aesthetic  
✅ **Auto-deploy** - push code, site updates automatically  

## 📞 Need Help?

Check these resources:

- [GitHub Pages Docs](https://docs.github.com/en/pages)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [HTML/CSS/JS Guide](https://developer.mozilla.org/en-US/docs/Learn)

---

**Ready? Let's deploy! 🚀**

```bash
./deploy.sh
```

