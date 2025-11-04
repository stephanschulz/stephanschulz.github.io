#!/usr/bin/env python3
import json
import os
from pathlib import Path
import html

# Load projects data
with open('projects-data.json', 'r', encoding='utf-8') as f:
    projects = json.load(f)

# HTML template for project pages
template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Stephan Schulz</title>
    <link rel="stylesheet" href="../styles.css">
    <style>
        .back-link {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 14px;
            margin-bottom: 24px;
            transition: color 0.2s ease;
        }}
        .back-link:hover {{
            color: var(--text-primary);
        }}
        .project-header {{
            margin-bottom: 32px;
        }}
        .project-meta {{
            display: flex;
            gap: 16px;
            font-size: 14px;
            color: var(--text-secondary);
            margin-top: 8px;
        }}
        .project-image-large {{
            width: 100%;
            border-radius: 6px;
            margin-bottom: 32px;
        }}
        .external-link {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 24px;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--text-primary);
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        .external-link:hover {{
            background: var(--bg-hover);
            transform: translateY(-1px);
        }}
    </style>
</head>
<body>
    <main class="container">
        <a href="../index.html" class="back-link">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <path d="M8.5 1.5l-7 7 7 7V10h6.5V6H8.5V1.5z"/>
            </svg>
            Back to Projects
        </a>

        <div class="project-header">
            <h1 class="page-title">{title}</h1>
            <div class="project-meta">
                <span>Year: {year}</span>
                <span>•</span>
                <span>{collaborator}</span>
                {role_html}
            </div>
        </div>

        <img src="../{image}" alt="{title}" class="project-image-large" onerror="this.style.display='none'">

        {link_html}

        <div style="margin-top: 48px;">
            <p style="color: var(--text-secondary); font-size: 14px;">
                More details and documentation coming soon.
            </p>
        </div>
    </main>
</body>
</html>'''

# Generate a page for each project
os.makedirs('projects', exist_ok=True)
generated = 0

for project in projects:
    if not project.get('hasDetailPage'):
        continue
    
    # Prepare template variables
    role_html = f'<span>•</span><span>Role: {html.escape(project["role"])}</span>' if project.get('role') else ''
    link_html = f'''<a href="{project['link']}" target="_blank" class="external-link">
            View Official Project Page
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <path d="M3.75 2h3.5a.75.75 0 0 1 0 1.5h-3.5a.25.25 0 0 0-.25.25v8.5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25v-3.5a.75.75 0 0 1 1.5 0v3.5A1.75 1.75 0 0 1 12.25 14h-8.5A1.75 1.75 0 0 1 2 12.25v-8.5C2 2.784 2.784 2 3.75 2zm6.854-1h4.146a.25.25 0 0 1 .25.25v4.146a.25.25 0 0 1-.427.177L13.03 4.03 9.28 7.78a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042l3.75-3.75-1.543-1.543A.25.25 0 0 1 10.604 1z"/>
            </svg>
        </a>''' if project.get('link') else ''
    
    html_content = template.format(
        title=html.escape(project['name']),
        year=html.escape(project['year']),
        collaborator=html.escape(project['collaborator']),
        role_html=role_html,
        image=html.escape(project['image']),
        link_html=link_html
    )
    
    # Write file
    filename = f"projects/{project['slug']}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    generated += 1

print(f"✓ Generated {generated} project detail pages")

