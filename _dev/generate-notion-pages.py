#!/usr/bin/env python3
import json
import os
import shutil
from pathlib import Path
from bs4 import BeautifulSoup
import re
import unicodedata
from PIL import Image

# Get the project root directory (parent of _dev folder)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
os.chdir(project_root)

# Load projects data
with open('projects-data.json', 'r', encoding='utf-8') as f:
    projects_data = json.load(f)

# Projects will be created in individual folders
# No need for separate assets directories

notion_dir = "notion-page/Stephan Schulz/Projects and Artworks"

def clean_slug(text):
    slug = text.lower()
    slug = slug.replace(',', '').replace(':', '').replace('&', 'and')
    slug = slug.replace(' ', '-').replace('(', '').replace(')', '')
    slug = slug.replace('/', '-').replace('+', '-')
    slug = slug.replace('--', '-').replace('---', '-')
    slug = slug.replace('é', 'e').replace('ó', 'o').replace('ü', 'u')
    slug = slug.replace("'", '')
    return slug

def natural_sort_key(filename):
    """Sort files naturally (handling numbers in filenames)"""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', str(filename))]

def generate_cover_from_first_image(first_image_path, cover_path):
    """Generate cover image from first image with 3:2 aspect ratio"""
    try:
        img = Image.open(first_image_path)
        width, height = img.size
        target_ratio = 3 / 2
        current_ratio = width / height
        
        if current_ratio > target_ratio:
            new_width = int(height * target_ratio)
            left = (width - new_width) // 2
            img_cropped = img.crop((left, 0, left + new_width, height))
        else:
            new_height = int(width / target_ratio)
            top = (height - new_height) // 2
            img_cropped = img.crop((0, top, width, top + new_height))
        
        img_resized = img_cropped.resize((900, 600), Image.Resampling.LANCZOS)
        img_resized.save(cover_path, quality=90, optimize=True)
        return True
    except Exception:
        return False

def copy_project_images(project_name, slug):
    """Copy and rename images to numbered format in project folder"""
    # Find the project folder with Unicode normalization
    name_base = project_name.split(',')[0].strip()
    name_base_norm = unicodedata.normalize('NFC', name_base)
    name_base_normalized = name_base.replace(' / ', ' ')
    name_base_normalized_norm = unicodedata.normalize('NFC', name_base_normalized)
    
    folders = [f for f in os.listdir(notion_dir) 
               if os.path.isdir(os.path.join(notion_dir, f)) and 
               (name_base_norm in unicodedata.normalize('NFC', f) or 
                name_base_normalized_norm in unicodedata.normalize('NFC', f))]
    
    if not folders:
        return []
    
    folder_path = os.path.join(notion_dir, folders[0])
    
    # Create project directory structure
    project_dir = os.path.join('projects', slug)
    image_dir = os.path.join(project_dir, 'images')
    os.makedirs(image_dir, exist_ok=True)
    
    # Get all images and sort them
    image_files = []
    for ext in ['jpg', 'png', 'jpeg', 'gif', 'webp']:
        image_files.extend(Path(folder_path).glob(f'*.{ext}'))
    
    image_files.sort(key=natural_sort_key)
    
    # Copy and rename with numbered prefixes
    images = []
    for idx, img_path in enumerate(image_files, start=1):
        ext = img_path.suffix
        new_name = f"{idx:02d}_image{ext}"
        dest = os.path.join(image_dir, new_name)
        shutil.copy2(str(img_path), dest)
        images.append(f'images/{new_name}')
    
    # Generate cover image from first image
    if image_files:
        first_image_path = os.path.join(image_dir, f"01_image{image_files[0].suffix}")
        cover_ext = image_files[0].suffix
        cover_path = os.path.join(image_dir, f"cover{cover_ext}")
        
        if not generate_cover_from_first_image(first_image_path, cover_path):
            # Fallback: copy first image
            shutil.copy2(first_image_path, cover_path)
    
    return images

def parse_notion_html(project_name):
    """Extract content from Notion HTML export"""
    # Find the HTML file - handle slashes and Unicode normalization
    name_base = project_name.split(',')[0].strip()
    name_base_norm = unicodedata.normalize('NFC', name_base)
    name_base_normalized = name_base.replace(' / ', ' ')
    name_base_normalized_norm = unicodedata.normalize('NFC', name_base_normalized)
    
    html_files = [f for f in os.listdir(notion_dir) 
                  if f.endswith('.html') and 
                  (name_base_norm in unicodedata.normalize('NFC', f) or 
                   name_base_normalized_norm in unicodedata.normalize('NFC', f))]
    
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
        # Clean display of link - just show domain or "View Project"
        display_text = official_site.replace('https://', '').replace('http://', '').replace('www.', '')
        if len(display_text) > 50:
            display_text = 'View Project'
        props_html += f'''
                <tr class="property-row">
                    <th>
                        <span class="icon">🔗</span>
                        Official Site
                    </th>
                    <td><a href="{official_site}" target="_blank" class="url-value">{display_text}</a></td>
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
    
    # Build description - convert URLs to links
    description_html = ''
    import re
    url_pattern = r'(https?://[^\s]+)'
    
    for para in content['description']:
        # Convert URLs in text to clickable links
        def replace_url(match):
            url = match.group(0)
            # Clean display text - show domain
            display = url.replace('https://', '').replace('http://', '').split('/')[0]
            return f'<a href="{url}" target="_blank" class="url-value">{display}</a>'
        
        para_with_links = re.sub(url_pattern, replace_url, para)
        description_html += f'<p>{para_with_links}</p>\n        '
    
    # Build acknowledgment - add Rafael Lozano-Hemmer footer if applicable
    acknowledgment_html = ''
    if 'Rafael Lozano-Hemmer' in collaborator or 'rafael lozano-hemmer' in collaborator.lower():
        acknowledgment_html = '''
        <hr>
        <h3>Acknowledgment</h3>
        <p>This artwork by Rafael Lozano-Hemmer is the result of the combined efforts of a talented and diverse group of professionals. Each person has contributed unique skills and expertise to the creation of this piece. For more information about the team and their roles, please visit our <a href="https://www.lozano-hemmer.com/" target="_blank" class="url-value">official website</a>.</p>'''
    elif content['acknowledgment']:
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
    <link rel="stylesheet" href="../../styles.css">
</head>
<body>
    <main class="container">
        <div class="breadcrumb">
            <a href="../../index.html">Stephan Schulz</a> / 
            <a href="../../index.html">Projects and Artworks</a> / 
            {project['name']}
        </div>

        <header>
            <h1 class="page-title">{project['name']}</h1>
            {props_html}
        </header>

        <hr class="properties-divider">

        <div class="page-body">
            {description_html}
            
            {images_html}
            
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
    
    # Ensure project directory exists
    project_dir = f'projects/{slug}'
    os.makedirs(project_dir, exist_ok=True)
    
    # Write file
    with open(f'{project_dir}/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    generated += 1

print(f"✓ Generated {generated} Notion-style project pages")
print(f"✓ Images organized with numbered prefixes (01_image.jpg, etc.)")
print(f"✓ Cover images auto-generated with 3:2 aspect ratio")

