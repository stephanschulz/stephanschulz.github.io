#!/usr/bin/env python3
import json
import os
import shutil
from pathlib import Path
from bs4 import BeautifulSoup
import re

# Load projects data
with open('projects-data.json', 'r', encoding='utf-8') as f:
    projects_data = json.load(f)

# Create projects directory
os.makedirs('projects', exist_ok=True)
os.makedirs('assets/project-images', exist_ok=True)

notion_dir = "notion-page/Stephan Schulz/Projects and Artworks"

def clean_slug(text):
    slug = text.lower()
    slug = slug.replace(',', '').replace(':', '').replace('&', 'and')
    slug = slug.replace(' ', '-').replace('(', '').replace(')', '')
    slug = slug.replace('/', '-').replace('+', '-')
    slug = slug.replace('--', '-').replace('é', 'e').replace('ó', 'o')
    return slug

def copy_project_images(project_name, slug):
    """Copy all images from project folder to assets"""
    # Find the project folder
    folders = [f for f in os.listdir(notion_dir) 
               if os.path.isdir(os.path.join(notion_dir, f)) and project_name.split(',')[0] in f]
    
    if not folders:
        return []
    
    folder_path = os.path.join(notion_dir, folders[0])
    image_dir = os.path.join('assets/project-images', slug)
    os.makedirs(image_dir, exist_ok=True)
    
    images = []
    for ext in ['jpg', 'png', 'jpeg', 'gif', 'webp']:
        for img_path in Path(folder_path).glob(f'*.{ext}'):
            dest = os.path.join(image_dir, img_path.name)
            shutil.copy2(str(img_path), dest)
            images.append(f'../assets/project-images/{slug}/{img_path.name}')
    
    return images

def parse_notion_html(project_name):
    """Extract content from Notion HTML export"""
    # Find the HTML file
    html_files = [f for f in os.listdir(notion_dir) 
                  if f.endswith('.html') and project_name.split(',')[0] in f]
    
    if not html_files:
        return None
    
    html_path = os.path.join(notion_dir, html_files[0])
    
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Extract properties
    properties = {}
    props_table = soup.find('table', class_='properties')
    if props_table:
        for row in props_table.find_all('tr'):
            th = row.find('th')
            td = row.find('td')
            if th and td:
                key = th.get_text().strip()
                value = td.get_text().strip()
                # Check if it's a multi-select (tags)
                tags = td.find_all('span', class_='selected-value')
                if tags:
                    value = [tag.get_text().strip() for tag in tags]
                properties[key] = value
    
    # Extract description paragraphs
    page_body = soup.find('div', class_='page-body')
    description = []
    if page_body:
        for p in page_body.find_all('p', recursive=False):
            text = p.get_text().strip()
            if text:
                description.append(text)
    
    # Extract acknowledgment
    acknowledgment = ""
    h3_tags = soup.find_all('h3')
    for h3 in h3_tags:
        if 'Acknowledgment' in h3.get_text():
            next_p = h3.find_next('p')
            if next_p:
                acknowledgment = next_p.get_text().strip()
    
    return {
        'properties': properties,
        'description': description,
        'acknowledgment': acknowledgment
    }

def generate_project_page(project, content, images):
    """Generate HTML for a project page"""
    
    # Extract properties
    props = content['properties']
    collaborator = props.get('for', project['collaborator'])
    year = props.get('Year', project['year'])
    official_site = props.get('Official Site', project.get('link', ''))
    roles = props.get('I did', [])
    if isinstance(roles, str):
        roles = [r.strip() for r in roles.split(',')]
    
    # Build properties table
    props_html = f'''
        <table class="properties">
            <tbody>
                <tr class="property-row">
                    <th>
                        <span class="icon">👤</span>
                        for
                    </th>
                    <td>{collaborator}</td>
                </tr>
                <tr class="property-row">
                    <th>
                        <span class="icon">#</span>
                        Year
                    </th>
                    <td>{year}</td>
                </tr>'''
    
    if official_site:
        props_html += f'''
                <tr class="property-row">
                    <th>
                        <span class="icon">🔗</span>
                        Official Site
                    </th>
                    <td><a href="{official_site}" target="_blank" class="url-value">{official_site}</a></td>
                </tr>'''
    
    if roles:
        roles_html = ''.join([f'<span class="tag">{role}</span>' for role in roles])
        props_html += f'''
                <tr class="property-row">
                    <th>
                        <span class="icon">📋</span>
                        I did
                    </th>
                    <td>{roles_html}</td>
                </tr>'''
    
    props_html += '''
            </tbody>
        </table>'''
    
    # Build images gallery
    images_html = ''
    if images:
        # First two images in two columns
        if len(images) >= 2:
            images_html += f'''
        <div class="image-grid">
            <div class="image-column">
                <img src="{images[0]}" alt="{project['name']}" loading="lazy">
            </div>
            <div class="image-column">
                <img src="{images[1]}" alt="{project['name']}" loading="lazy">
            </div>
        </div>'''
        
        # Remaining images full width
        for img in images[2:]:
            images_html += f'''
        <div class="image-full">
            <img src="{img}" alt="{project['name']}" loading="lazy">
        </div>'''
    
    # Build description
    description_html = ''
    for para in content['description']:
        description_html += f'<p>{para}</p>\n        '
    
    # Build acknowledgment
    acknowledgment_html = ''
    if content['acknowledgment']:
        acknowledgment_html = f'''
        <hr>
        <h3>Acknowledgment</h3>
        <p>{content['acknowledgment']}</p>'''
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project['name']} - Stephan Schulz</title>
    <link rel="stylesheet" href="../styles.css">
    <style>
        .breadcrumb {{
            font-size: 14px;
            color: var(--text-secondary);
            margin-bottom: 24px;
        }}
        .breadcrumb a {{
            color: var(--text-secondary);
            text-decoration: none;
        }}
        .breadcrumb a:hover {{
            color: var(--text-primary);
        }}
        .properties {{
            width: 100%;
            margin: 24px 0 32px 0;
            font-size: 14px;
            border: none;
        }}
        .property-row {{
            border-bottom: 1px solid var(--border-color);
        }}
        .property-row th {{
            padding: 12px 0;
            font-weight: 400;
            color: var(--text-secondary);
            width: 30%;
            vertical-align: top;
            text-align: left;
        }}
        .property-row td {{
            padding: 12px 0;
            color: var(--text-primary);
        }}
        .icon {{
            margin-right: 8px;
            opacity: 0.6;
        }}
        .url-value {{
            color: var(--accent-color);
            text-decoration: none;
        }}
        .url-value:hover {{
            text-decoration: underline;
        }}
        .tag {{
            display: inline-block;
            padding: 4px 12px;
            background: var(--bg-secondary);
            border-radius: 12px;
            font-size: 12px;
            margin-right: 8px;
            border: 1px solid var(--border-color);
        }}
        .image-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin: 32px 0;
        }}
        .image-column img,
        .image-full img {{
            width: 100%;
            border-radius: 3px;
            display: block;
        }}
        .image-full {{
            margin: 32px 0;
        }}
        hr {{
            border: none;
            border-top: 1px solid var(--border-color);
            margin: 48px 0 24px 0;
        }}
        h3 {{
            font-size: 18px;
            font-weight: 600;
            margin: 24px 0 16px 0;
        }}
        p {{
            line-height: 1.7;
            margin-bottom: 16px;
        }}
        @media (max-width: 768px) {{
            .image-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <main class="container">
        <div class="breadcrumb">
            <a href="../index.html">Stephan Schulz</a> / 
            <a href="../index.html">Projects and Artworks</a> / 
            {project['name']}
        </div>

        <header>
            <h1 class="page-title">{project['name']}</h1>
            {props_html}
        </header>

        <div class="page-body">
            {images_html}
            
            {description_html}
            
            {acknowledgment_html}
        </div>
    </main>
</body>
</html>'''

# Generate project pages
generated = 0

for project in projects_data:
    if not project.get('hasDetailPage'):
        continue
    
    slug = project['slug']
    name = project['name']
    
    # Parse Notion content
    notion_content = parse_notion_html(name)
    if not notion_content:
        print(f"⚠️  No Notion content found for: {name}")
        continue
    
    # Copy all images
    images = copy_project_images(name, slug)
    
    # Generate HTML
    html = generate_project_page(project, notion_content, images)
    
    # Write file
    with open(f'projects/{slug}.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    generated += 1

print(f"✓ Generated {generated} Notion-style project pages")
print(f"✓ Images organized in assets/project-images/")

