#!/bin/bash

# GitHub Pages Deployment Script
# This script helps you deploy your personal website to GitHub Pages

echo "================================================"
echo "GitHub Pages Deployment Helper"
echo "================================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: Git is not installed"
    echo "Please install Git: https://git-scm.com/downloads"
    exit 1
fi

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
    echo ""
fi

# Get repository URL from user
echo "🔗 GitHub Repository Setup"
echo ""
read -p "Enter your GitHub repository URL (e.g., https://github.com/stephanschulz/stephanschulz.github.io.git): " repo_url

if [ -z "$repo_url" ]; then
    echo "❌ Error: Repository URL is required"
    exit 1
fi

# Check if remote already exists
if git remote | grep -q "^origin$"; then
    echo "⚠️  Remote 'origin' already exists"
    read -p "Do you want to update it? (y/n): " update_remote
    if [ "$update_remote" = "y" ]; then
        git remote set-url origin "$repo_url"
        echo "✅ Remote updated"
    fi
else
    git remote add origin "$repo_url"
    echo "✅ Remote added"
fi

echo ""
echo "📝 Preparing files for deployment..."

# Add all files
git add .

# Create commit
echo ""
read -p "Enter commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Update personal website"
fi

git commit -m "$commit_msg"
echo "✅ Changes committed"

# Get current branch
current_branch=$(git branch --show-current)

# Check if branch is main, if not create/switch to main
if [ "$current_branch" != "main" ]; then
    echo ""
    echo "📌 Switching to main branch..."
    git branch -M main
fi

# Push to GitHub
echo ""
echo "🚀 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo "✅ Successfully deployed to GitHub!"
    echo "================================================"
    echo ""
    echo "Next steps:"
    echo "1. Go to your repository on GitHub"
    echo "2. Navigate to Settings > Pages"
    echo "3. Under 'Build and deployment', select 'GitHub Actions'"
    echo "4. Wait 1-2 minutes for deployment"
    echo ""
    
    # Extract username and repo name from URL
    repo_name=$(echo "$repo_url" | sed -n 's#.*/\([^/]*\)\.git#\1#p')
    username=$(echo "$repo_url" | sed -n 's#.*/\([^/]*\)/[^/]*\.git#\1#p')
    
    if [ "$repo_name" = "$username.github.io" ]; then
        echo "🌐 Your site will be available at:"
        echo "   https://$username.github.io/"
    else
        echo "🌐 Your site will be available at:"
        echo "   https://$username.github.io/$repo_name/"
    fi
    echo ""
else
    echo ""
    echo "================================================"
    echo "❌ Push failed"
    echo "================================================"
    echo ""
    echo "Common solutions:"
    echo "1. Make sure you have access to the repository"
    echo "2. Check if you need to authenticate with GitHub"
    echo "3. Try: git push -u origin main --force (use carefully!)"
    echo ""
    exit 1
fi

