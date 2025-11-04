#!/usr/bin/env python3
"""
Admin interface for editing existing projects
Run: python3 _dev/admin-edit-server.py
Opens: http://localhost:5001/admin/edit
"""

from flask import Flask, request, jsonify, send_from_directory
import os
import json
import shutil
from pathlib import Path
import unicodedata
from PIL import Image
import re
import webbrowser
from threading import Timer
import markdown
from markdownify import markdownify as md

# Get project root
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
os.chdir(project_root)

app = Flask(__name__)

def clean_slug(text):
    """Generate URL-friendly slug from project name"""
    slug = text.lower()
    slug = slug.replace(' / ', '-').replace('/', '-')
    slug = slug.replace(',', '').replace(':', '').replace('&', 'and')
    slug = slug.replace(' ', '-').replace('(', '').replace(')', '')
    slug = slug.replace('ü', 'u').replace('ß', 'ss')
    slug = slug.replace("'", '').replace("'", '')
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    return slug

def generate_cover_from_first_image(source_path, dest_path, target_width=900, target_height=600):
    """Generate a 3:2 aspect ratio cover image from source"""
    try:
        with Image.open(source_path) as img:
            img_width, img_height = img.size
            target_ratio = target_width / target_height
            img_ratio = img_width / img_height
            
            if img_ratio > target_ratio:
                new_height = img_height
                new_width = int(new_height * target_ratio)
                left = (img_width - new_width) // 2
                top = 0
                right = left + new_width
                bottom = img_height
            else:
                new_width = img_width
                new_height = int(new_width / target_ratio)
                left = 0
                top = (img_height - new_height) // 2
                right = img_width
                bottom = top + new_height
            
            cropped = img.crop((left, top, right, bottom))
            resized = cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            if img.mode == 'RGBA':
                rgb_img = Image.new('RGB', resized.size, (255, 255, 255))
                rgb_img.paste(resized, mask=resized.split()[3])
                rgb_img.save(dest_path, 'JPEG', quality=90, optimize=True)
            else:
                resized.save(dest_path, quality=90, optimize=True)
            
            return True
    except Exception as e:
        print(f"Error generating cover: {e}")
        return False

def parse_project_html(html_path):
    """Parse existing project HTML to extract content"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(f.read(), 'html.parser')
            
            # Extract title
            title_elem = soup.select_one('h1.page-title')
            title = title_elem.get_text().strip() if title_elem else ''
            
            # Extract properties
            properties = {}
            for row in soup.select('.property-row'):
                th = row.select_one('th')
                td = row.select_one('td')
                if th and td:
                    key = th.get_text().strip().lower().replace('i did', 'role')
                    if key == 'for':
                        properties['collaborator'] = td.get_text().strip()
                    elif key == 'year':
                        properties['year'] = td.get_text().strip()
                    elif key == 'official site':
                        link = td.select_one('a')
                        properties['official_site'] = link['href'] if link else ''
                    elif key == 'role':
                        tags = [tag.get_text().strip() for tag in td.select('.tag')]
                        properties['role'] = ', '.join(tags)
            
            # Extract description and convert HTML back to Markdown
            description_elem = soup.select_one('.page-body')
            description = ''
            if description_elem:
                # Find all content before the images
                content_parts = []
                for child in description_elem.children:
                    # Stop at images or hr
                    if child.name in ['hr', 'div']:
                        break
                    if child.name == 'p':
                        # Convert paragraph HTML to Markdown
                        content_parts.append(md(str(child)).strip())
                    elif child.name in ['ul', 'ol']:
                        # Convert lists to Markdown
                        content_parts.append(md(str(child)).strip())
                    elif child.name and child.get_text().strip():
                        # Other block elements
                        content_parts.append(md(str(child)).strip())
                
                description = '\n\n'.join(content_parts) if content_parts else ''
            
            # Extract acknowledgment and convert HTML to Markdown - always populate so user can edit
            acknowledgment = ''
            ack_h3 = soup.find('h3', string='Acknowledgment')
            if ack_h3:
                # Get all content after the h3 until the next hr or end of page-body
                ack_parts = []
                for sibling in ack_h3.next_siblings:
                    if sibling.name == 'p':
                        # Convert paragraph HTML to Markdown
                        ack_markdown = md(str(sibling)).strip()
                        ack_parts.append(ack_markdown)
                    elif sibling.name in ['ul', 'ol']:
                        # Convert lists to Markdown
                        ack_markdown = md(str(sibling)).strip()
                        ack_parts.append(ack_markdown)
                    elif sibling.name in ['h3', 'hr']:
                        break
                
                if ack_parts:
                    acknowledgment = '\n\n'.join(ack_parts)
                    print(f"DEBUG: Found acknowledgment (Markdown): {acknowledgment[:100]}...")
            
            return {
                'title': title,
                'description': description.strip(),
                'acknowledgment': acknowledgment,
                **properties
            }
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return {}

@app.route('/')
@app.route('/admin/edit')
def admin_edit_interface():
    """Serve admin edit interface"""
    admin_dir = os.path.join(project_root, '_dev', 'admin')
    return send_from_directory(admin_dir, 'edit.html')

@app.route('/admin/<path:filename>')
def admin_static(filename):
    """Serve admin static files"""
    admin_dir = os.path.join(project_root, '_dev', 'admin')
    return send_from_directory(admin_dir, filename)

@app.route('/styles.css')
def serve_styles():
    """Serve main styles.css for preview"""
    return send_from_directory(project_root, 'styles.css')

@app.route('/index.html')
def serve_main_site():
    """Serve main site for back link"""
    return send_from_directory(project_root, 'index.html')

@app.route('/projects/<slug>/')
@app.route('/projects/<slug>/index.html')
def serve_project(slug):
    """Serve project detail pages"""
    project_dir = os.path.join(project_root, 'projects', slug)
    return send_from_directory(project_dir, 'index.html')

@app.route('/projects/<slug>/images/<filename>')
def serve_project_image(slug, filename):
    """Serve project images"""
    images_dir = os.path.join(project_root, 'projects', slug, 'images')
    return send_from_directory(images_dir, filename)

@app.route('/api/serve-local-image', methods=['POST'])
def serve_local_image():
    """Serve a local image for preview (base64 encoded)"""
    try:
        data = request.json
        image_path = data.get('path')
        
        if not image_path or not os.path.exists(image_path):
            return jsonify({'error': 'Image not found'}), 404
        
        # Read image and convert to base64
        with open(image_path, 'rb') as f:
            import base64
            image_data = base64.b64encode(f.read()).decode('utf-8')
            
        # Detect mime type
        ext = os.path.splitext(image_path)[1].lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        mime_type = mime_types.get(ext, 'image/jpeg')
        
        return jsonify({
            'data': f'data:{mime_type};base64,{image_data}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/browse-images', methods=['POST'])
def browse_images():
    """List images in specified folder"""
    try:
        data = request.json
        path = data.get('path', '')
        
        if not path or not os.path.exists(path):
            return jsonify({'error': 'Folder not found'}), 404
        
        # Get all image files
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
        image_files = []
        
        for file in os.listdir(path):
            if file.lower().endswith(image_extensions):
                full_path = os.path.join(path, file)
                if os.path.isfile(full_path):
                    image_files.append({
                        'name': file,
                        'path': full_path
                    })
        
        # Sort naturally
        def natural_sort_key(item):
            return [int(text) if text.isdigit() else text.lower()
                    for text in re.split('([0-9]+)', item['name'])]
        
        image_files.sort(key=natural_sort_key)
        
        return jsonify({'images': image_files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/list-projects', methods=['GET'])
def list_projects():
    """Get list of all projects"""
    try:
        with open('projects-data.json', 'r', encoding='utf-8') as f:
            projects = json.load(f)
        
        # Filter out CV entry and return list
        project_list = [
            {
                'slug': p['slug'],
                'name': p['name'],
                'year': p['year'],
                'collaborator': p.get('collaborator', '')
            }
            for p in projects
            if not p.get('isCV', False)
        ]
        
        # Sort alphabetically by name
        project_list.sort(key=lambda x: x['name'].lower())
        
        return jsonify({'projects': project_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/load-project/<slug>', methods=['GET'])
def load_project(slug):
    """Load project data for editing"""
    try:
        # Get project from projects-data.json
        with open('projects-data.json', 'r', encoding='utf-8') as f:
            projects = json.load(f)
        
        project = next((p for p in projects if p['slug'] == slug), None)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        # Parse HTML content
        html_path = os.path.join('projects', slug, 'index.html')
        if not os.path.exists(html_path):
            return jsonify({'error': 'Project HTML not found'}), 404
        
        content = parse_project_html(html_path)
        
        # Get images from images folder
        images_dir = os.path.join('projects', slug, 'images')
        images = []
        if os.path.exists(images_dir):
            image_files = sorted(
                [f for f in os.listdir(images_dir) if f.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')) and not f.startswith('cover')],
                key=lambda x: int(x.split('_')[0]) if '_' in x else 0
            )
            for img_file in image_files:
                images.append({
                    'name': img_file,
                    'path': os.path.join(images_dir, img_file)
                })
        
        return jsonify({
            'slug': slug,
            'name': project['name'],
            'year': project['year'],
            'collaborator': project.get('collaborator', ''),
            'official_site': project.get('link', ''),
            'role': project.get('role', ''),
            'description': content.get('description', ''),
            'acknowledgment': content.get('acknowledgment', ''),
            'images': images
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete-project/<slug>', methods=['DELETE'])
def delete_project(slug):
    """Delete a project"""
    try:
        project_dir = os.path.join('projects', slug)
        
        # Check if project exists
        if not os.path.exists(project_dir):
            return jsonify({'error': 'Project not found'}), 404
        
        # Remove project directory and all contents
        shutil.rmtree(project_dir)
        print(f"Deleted project folder: {project_dir}")
        
        # Update projects-data.json
        with open('projects-data.json', 'r', encoding='utf-8') as f:
            projects = json.load(f)
        
        # Remove project from list
        projects = [p for p in projects if p['slug'] != slug]
        
        with open('projects-data.json', 'w', encoding='utf-8') as f:
            json.dump(projects, f, indent=2, ensure_ascii=False)
        
        print(f"Removed {slug} from projects-data.json")
        
        return jsonify({
            'success': True,
            'message': f'Project "{slug}" deleted successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/update-project/<slug>', methods=['POST'])
def update_project(slug):
    """Update existing project"""
    try:
        data = request.json
        
        # Validate required fields
        required = ['name', 'year', 'collaborator', 'role']
        for field in required:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if slug needs to change
        project_name = f"{data['name']}, {data['year']}"
        new_slug = clean_slug(project_name)
        
        old_project_dir = os.path.join('projects', slug)
        new_project_dir = os.path.join('projects', new_slug)
        
        # If slug changed, rename directory
        if slug != new_slug and os.path.exists(old_project_dir):
            if os.path.exists(new_project_dir):
                return jsonify({'error': 'A project with this name/year already exists'}), 400
            os.rename(old_project_dir, new_project_dir)
            slug = new_slug
        
        project_dir = new_project_dir if slug == new_slug else old_project_dir
        images_dir = os.path.join(project_dir, 'images')
        
        # Handle images if provided
        if 'images' in data and data['images']:
            os.makedirs(images_dir, exist_ok=True)
            
            # Check if we're reordering existing images or loading new ones
            images_are_from_project = all(
                img_data['path'].startswith(images_dir) 
                for img_data in data['images']
            )
            
            if images_are_from_project:
                # Reordering existing images - rename in place
                # First, rename all to temp names to avoid conflicts
                temp_mapping = []
                for idx, img_data in enumerate(data['images'], start=1):
                    src_path = img_data['path']
                    ext = os.path.splitext(src_path)[1]
                    temp_name = f"temp_{idx:02d}_image{ext}"
                    temp_path = os.path.join(images_dir, temp_name)
                    
                    if os.path.exists(src_path):
                        os.rename(src_path, temp_path)
                        temp_mapping.append((temp_path, f"{idx:02d}_image{ext}"))
                
                # Then rename temp files to final names
                numbered_images = []
                for temp_path, final_name in temp_mapping:
                    final_path = os.path.join(images_dir, final_name)
                    os.rename(temp_path, final_path)
                    numbered_images.append(final_name)
            else:
                # Loading new images - copy from external source
                # Clear old numbered images
                if os.path.exists(images_dir):
                    for f in os.listdir(images_dir):
                        if f.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
                            os.remove(os.path.join(images_dir, f))
                
                # Copy new images
                numbered_images = []
                for idx, img_data in enumerate(data['images'], start=1):
                    src_path = img_data['path']
                    ext = os.path.splitext(src_path)[1]
                    dest_name = f"{idx:02d}_image{ext}"
                    dest_path = os.path.join(images_dir, dest_name)
                    
                    shutil.copy2(src_path, dest_path)
                    numbered_images.append(dest_name)
            
            # Regenerate cover from first image
            if numbered_images:
                first_image_path = os.path.join(images_dir, numbered_images[0])
                cover_ext = os.path.splitext(numbered_images[0])[1]
                cover_path = os.path.join(images_dir, f"cover{cover_ext}")
                
                if not generate_cover_from_first_image(first_image_path, cover_path):
                    shutil.copy2(first_image_path, cover_path)
        else:
            # Use existing images
            numbered_images = sorted(
                [f for f in os.listdir(images_dir) if f.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')) and not f.startswith('cover')]
            ) if os.path.exists(images_dir) else []
        
        # Generate HTML
        html_content = generate_html(data, numbered_images)
        html_path = os.path.join(project_dir, 'index.html')
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Update projects-data.json
        with open('projects-data.json', 'r', encoding='utf-8') as f:
            projects = json.load(f)
        
        # Find and update the project
        cover_ext = os.path.splitext(numbered_images[0])[1] if numbered_images else '.jpg'
        updated_project = {
            'name': project_name,
            'year': str(data['year']),
            'collaborator': data['collaborator'],
            'link': data.get('official_site', ''),
            'role': data['role'],
            'slug': slug,
            'image': f'projects/{slug}/images/cover{cover_ext}',
            'hasDetailPage': True
        }
        
        # Replace old project
        projects = [updated_project if p['slug'] in [slug, new_slug] else p for p in projects]
        
        # Sort by year descending
        projects.sort(key=lambda x: int(x['year']) if x['year'].isdigit() else 0, reverse=True)
        
        with open('projects-data.json', 'w', encoding='utf-8') as f:
            json.dump(projects, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            'success': True,
            'slug': slug,
            'url': f'/projects/{slug}/'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_html(data, images):
    """Generate project HTML"""
    name = data['name']
    year = data['year']
    collaborator = data['collaborator']
    official_site = data.get('official_site', '')
    role = data.get('role', '')
    description = data.get('description', '')
    acknowledgment = data.get('acknowledgment', '')
    
    # Generate role tags
    roles = [r.strip() for r in role.split(',')]
    role_tags_html = ' '.join([f'<span class="tag">{r}</span>' for r in roles if r])
    
    # Generate official site row if present
    official_site_row = ''
    if official_site:
        site_text = official_site.replace('https://', '').replace('http://', '').replace('www.', '')
        if len(site_text) > 50:
            site_text = 'View Project'
        official_site_row = f"""
                <tr class="property-row">
                    <th><span class="icon">🔗</span>Official Site</th>
                    <td><a href="{official_site}" target="_blank" class="url-value">{site_text}</a></td>
                </tr>"""
    
    # Generate role row
    role_row = ''
    if role_tags_html:
        role_row = f"""
                <tr class="property-row">
                    <th><span class="icon">📋</span>I did</th>
                    <td>{role_tags_html}</td>
                </tr>"""
    
    # Generate description HTML from Markdown
    description_html = ''
    if description:
        # Parse Markdown to HTML
        md = markdown.Markdown(extensions=['extra', 'nl2br'])
        html = md.convert(description)
        # Indent for template
        lines = html.split('\n')
        description_html = '\n'.join([f'        {line}' if line else '' for line in lines])
    
    # Generate images HTML
    images_html = ''
    if len(images) > 0:
        if len(images) == 1:
            images_html = f"""
        <div class="image-full">
            <img src="images/{images[0]}" alt="{name}, {year}" loading="lazy">
        </div>"""
        elif len(images) >= 2:
            images_html = f"""
        <div class="image-grid">
            <div class="image-column">
                <img src="images/{images[0]}" alt="{name}, {year}" loading="lazy">
            </div>
            <div class="image-column">
                <img src="images/{images[1]}" alt="{name}, {year}" loading="lazy">
            </div>
        </div>"""
            
            for img in images[2:]:
                images_html += f"""
        <div class="image-full">
            <img src="images/{img}" alt="{name}, {year}" loading="lazy">
        </div>"""
    
    # Generate acknowledgment section
    acknowledgment_html = ''
    is_rlh = 'rafael lozano-hemmer' in collaborator.lower()
    
    if is_rlh:
        acknowledgment_html = """
        <hr>
        <h3>Acknowledgment</h3>
        <p>This artwork by Rafael Lozano-Hemmer is the result of the combined efforts of a talented and diverse group of professionals. Each person has contributed unique skills and expertise to the creation of this piece. For more information about the team and their roles, please visit our <a href="https://www.lozano-hemmer.com/" target="_blank" class="url-value">official website</a>.</p>"""
    elif acknowledgment:
        # Parse Markdown for acknowledgment too
        md = markdown.Markdown(extensions=['extra', 'nl2br'])
        ack_html = md.convert(acknowledgment)
        lines = ack_html.split('\n')
        ack_content = '\n'.join([f'        {line}' if line else '' for line in lines])
        acknowledgment_html = f"""
        <hr>
        <h3>Acknowledgment</h3>
{ack_content}"""
    
    # Generate full HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}, {year} - Stephan Schulz</title>
    <link rel="stylesheet" href="../../styles.css">
</head>
<body>
    <main class="container">
        <div class="breadcrumb">
            <a href="../../index.html">Stephan Schulz</a> / 
            <a href="../../index.html">Projects and Artworks</a> / 
            {name}, {year}
        </div>

        <header>
            <h1 class="page-title">{name}, {year}</h1>
            
            <table class="properties">
                <tbody>
                    <tr class="property-row">
                        <th><span class="icon">👤</span>for</th>
                        <td>{collaborator}</td>
                    </tr>
                    <tr class="property-row">
                        <th><span class="icon">#</span>Year</th>
                        <td>{year}</td>
                    </tr>{official_site_row}{role_row}
                </tbody>
            </table>
        </header>

        <hr class="properties-divider">

        <div class="page-body">
{description_html}
            
{images_html}
{acknowledgment_html}
        </div>
    </main>
</body>
</html>"""
    
    return html

def open_browser():
    """Open browser to admin interface"""
    webbrowser.open('http://localhost:5001/admin/edit')

if __name__ == '__main__':
    print("=" * 60)
    print("✏️  Project Edit Interface")
    print("=" * 60)
    print("\nStarting server at http://localhost:5001/admin/edit")
    print("\nPress Ctrl+C to stop the server\n")
    
    # Open browser after a short delay
    Timer(1.5, open_browser).start()
    
    app.run(debug=True, port=5001, use_reloader=False)

