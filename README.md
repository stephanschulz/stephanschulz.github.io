# Stephan Schulz - Personal Website

A modern, Notion-inspired personal portfolio website built with vanilla HTML, CSS, and JavaScript. Designed for GitHub Pages deployment.

## 🚀 Features

- **Notion-style Design**: Clean, modern interface inspired by Notion's aesthetic
- **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile devices
- **Dark Mode Support**: Automatically adapts to system color scheme preferences
- **Single Page Application**: Smooth navigation without page reloads
- **SEO Friendly**: Semantic HTML with proper meta tags
- **Fast Loading**: No frameworks, just optimized vanilla JavaScript
- **GitHub Integration**: Showcases your GitHub projects and achievements

## 📁 Project Structure

```
stephanschulz/
├── index.html          # Main HTML file with all page content
├── styles.css          # Notion-inspired styling
├── script.js           # Navigation and interactivity
├── assets/             # Images, icons, and media files
│   └── avatar.jpg      # Your profile picture (add your own)
├── .github/
│   └── workflows/
│       └── deploy.yml  # GitHub Actions deployment workflow
└── README.md           # This file
```

## 🎨 Customization

### Adding Your Avatar

1. Add your profile picture to the `assets/` folder as `avatar.jpg`
2. Recommended size: 600x600px or larger (square format)
3. The site will display initials "SS" if no image is found

### Updating Content

Edit the `index.html` file to customize:

- **About Section**: Update your bio, skills, and location
- **Projects**: Add your GitHub projects or personal work
- **Experience**: Update your work history and achievements
- **Contact**: Modify social links and contact information

### Changing Colors

Edit the CSS variables in `styles.css`:

```css
:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f7f6f3;
    --text-primary: #37352f;
    --accent-color: #2383e2;
    /* ... more variables */
}
```

## 🌐 Deployment to GitHub Pages

### Method 1: Automatic Deployment (Recommended)

1. **Create a GitHub repository**:
   ```bash
   # Repository should be named: stephanschulz.github.io
   # Or any name for project pages
   ```

2. **Push your code**:
   ```bash
   cd /Users/stephanschulz/Documents/cursor_ai/websites/stephanschulz
   git init
   git add .
   git commit -m "Initial commit: Personal website"
   git branch -M main
   git remote add origin https://github.com/stephanschulz/stephanschulz.github.io.git
   git push -u origin main
   ```

3. **Enable GitHub Pages**:
   - Go to your repository on GitHub
   - Navigate to **Settings** > **Pages**
   - Under "Build and deployment":
     - Source: Select **GitHub Actions**
   - The workflow will automatically deploy your site

4. **Access your site**:
   - User page: `https://stephanschulz.github.io/`
   - Project page: `https://stephanschulz.github.io/repository-name/`

### Method 2: Manual Deployment

1. Go to **Settings** > **Pages**
2. Under "Source", select **Deploy from a branch**
3. Choose `main` branch and `/ (root)` folder
4. Click **Save**

Your site will be live in a few minutes!

## 🔧 Local Development

To preview locally, you can use any static file server:

### Using Python:
```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

### Using Node.js:
```bash
npx http-server -p 8000
```

### Using PHP:
```bash
php -S localhost:8000
```

Then visit: `http://localhost:8000`

## 📝 Migrating from Notion

If you're migrating from a Notion page:

1. **Export from Notion**:
   - Open your Notion page
   - Click `•••` > **Export**
   - Choose **HTML** format
   - Enable **Include subpages**
   - Download the ZIP file

2. **Extract Content**:
   - Copy text content from the exported HTML
   - Save images to the `assets/` folder
   - Update `index.html` with your content

3. **Preserve Structure**:
   - Maintain the same page sections
   - Keep similar visual hierarchy
   - Use the existing CSS classes for styling

## 🎯 Page Sections

The website includes four main sections:

1. **About** (`#about`): Introduction, skills, and basic information
2. **Projects** (`#projects`): Portfolio of your work and open-source contributions
3. **Experience** (`#experience`): Work history and achievements
4. **Contact** (`#contact`): Ways to get in touch

## 🔗 Links & References

- **Live Site**: https://stephanschulz.github.io/
- **GitHub Profile**: https://github.com/stephanschulz
- **X (Twitter)**: https://twitter.com/stephanschulz3
- **Original Notion Page**: https://antimodularresearch.notion.site/Stephan-Schulz-8d0f5c2871ca4502903f411a0d34208f

## 📄 License

This project is open source and available for personal use. Feel free to fork and customize for your own portfolio!

## 🤝 Contributing

This is a personal website template. Feel free to:
- Use it as a template for your own site
- Suggest improvements via issues
- Submit pull requests for bug fixes

## 📞 Contact

- **GitHub**: [@stephanschulz](https://github.com/stephanschulz)
- **Location**: Montreal, Canada
- **Organization**: Antimodular Research

---

Built with ❤️ using vanilla HTML, CSS, and JavaScript

