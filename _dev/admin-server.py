#!/usr/bin/env python3
"""
Flask-based admin server for adding new projects
Run: python3 _dev/admin-server.py
"""
from flask import Flask, request, jsonify, send_from_directory
import os
import json
import shutil
from pathlib import Path
from PIL import Image
import re
import webbrowser
from threading import Timer
import markdown

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
    slug = slug.replace('+', '-').replace("'", '')
    slug = slug.replace('--', '-').replace('---', '-')
    slug = slug.replace('é', 'e').replace('ó', 'o').replace('ü', 'u')
    return slug

def generate_cover_from_first_image(first_image_path, cover_path):
    """Generate cover image with 3:2 aspect ratio (900x600)"""
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
    except Exception as e:
        print(f"Error generating cover: {e}")
        return False

def generate_project_html(project_data, images):
    """Generate HTML for project detail page"""
    name = project_data['name']
    year = project_data['year']
    collaborator = project_data['collaborator']
    official_site = project_data.get('official_site', '')
    roles = [r.strip() for r in project_data['role'].split(',') if r.strip()]
    description = project_data.get('description', '')
    acknowledgment = project_data.get('acknowledgment', '')
    
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
    
    # Build description from Markdown
    description_html = ''
    if description:
        md = markdown.Markdown(extensions=['extra', 'nl2br'])
        description_html = md.convert(description) + '\n        '
    
    # Build images
    images_html = ''
    if images:
        if len(images) >= 2:
            images_html += f'''
        <div class="image-grid">
            <div class="image-column">
                <img src="images/{images[0]}" alt="{name}" loading="lazy">
            </div>
            <div class="image-column">
                <img src="images/{images[1]}" alt="{name}" loading="lazy">
            </div>
        </div>'''
        
        for img in images[2:]:
            images_html += f'''
        <div class="image-full">
            <img src="images/{img}" alt="{name}" loading="lazy">
        </div>'''
    
    # Build acknowledgment
    acknowledgment_html = ''
    if 'Rafael Lozano-Hemmer' in collaborator or 'rafael lozano-hemmer' in collaborator.lower():
        acknowledgment_html = '''
        <hr>
        <h3>Acknowledgment</h3>
        <p>This artwork by Rafael Lozano-Hemmer is the result of the combined efforts of a talented and diverse group of professionals. Each person has contributed unique skills and expertise to the creation of this piece. For more information about the team and their roles, please visit our <a href="https://www.lozano-hemmer.com/" target="_blank" class="url-value">official website</a>.</p>'''
    elif acknowledgment:
        # Parse acknowledgment as Markdown
        md = markdown.Markdown(extensions=['extra', 'nl2br'])
        ack_html = md.convert(acknowledgment)
        acknowledgment_html = f'''
        <hr>
        <h3>Acknowledgment</h3>
        {ack_html}'''
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Stephan Schulz</title>
    <link rel="stylesheet" href="../../styles.css">
</head>
<body>
    <main class="container">
        <div class="breadcrumb">
            <a href="../../index.html">Stephan Schulz</a> / 
            <a href="../../index.html">Projects and Artworks</a> / 
            {name}
        </div>

        <header>
            <h1 class="page-title">{name}</h1>
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

@app.route('/')
@app.route('/admin')
def admin_interface():
    """Serve admin interface"""
    admin_dir = os.path.join(project_root, '_dev', 'admin')
    return send_from_directory(admin_dir, 'index.html')

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
    data = request.json
    folder_path = data.get('path', '')
    
    if not folder_path or not os.path.exists(folder_path):
        return jsonify({'error': 'Invalid folder path'}), 400
    
    try:
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
        images = []
        
        for filename in sorted(os.listdir(folder_path)):
            if filename.lower().endswith(image_extensions):
                full_path = os.path.join(folder_path, filename)
                images.append({
                    'name': filename,
                    'path': full_path
                })
        
        return jsonify({'images': images})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/create-project', methods=['POST'])
def create_project():
    """Create new project with all files"""
    try:
        data = request.json
        
        # Validate required fields
        required = ['name', 'year', 'collaborator', 'role']
        for field in required:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Generate slug
        project_name = f"{data['name']}, {data['year']}"
        slug = clean_slug(project_name)
        
        # Create project directories
        project_dir = os.path.join('projects', slug)
        images_dir = os.path.join(project_dir, 'images')
        os.makedirs(images_dir, exist_ok=True)
        
        # Process and copy images
        image_files = data.get('images', [])
        numbered_images = []
        
        for idx, img_data in enumerate(image_files, start=1):
            src_path = img_data['path']
            ext = os.path.splitext(src_path)[1]
            dest_name = f"{idx:02d}_image{ext}"
            dest_path = os.path.join(images_dir, dest_name)
            
            shutil.copy2(src_path, dest_path)
            numbered_images.append(dest_name)
        
        # Generate cover from first image
        if numbered_images:
            first_image_path = os.path.join(images_dir, numbered_images[0])
            cover_ext = os.path.splitext(numbered_images[0])[1]
            cover_path = os.path.join(images_dir, f"cover{cover_ext}")
            
            if not generate_cover_from_first_image(first_image_path, cover_path):
                # Fallback: copy first image
                shutil.copy2(first_image_path, cover_path)
        
        # Generate HTML
        html_content = generate_project_html(data, numbered_images)
        html_path = os.path.join(project_dir, 'index.html')
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Update projects-data.json
        with open('projects-data.json', 'r', encoding='utf-8') as f:
            projects = json.load(f)
        
        cover_ext = os.path.splitext(numbered_images[0])[1] if numbered_images else '.jpg'
        new_project = {
            'name': project_name,
            'year': str(data['year']),
            'collaborator': data['collaborator'],
            'link': data.get('official_site', ''),
            'role': data['role'],
            'slug': slug,
            'image': f'projects/{slug}/images/cover{cover_ext}',
            'hasDetailPage': True
        }
        
        # Insert at the beginning (newest first)
        projects.insert(0, new_project)
        
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

def open_browser():
    """Open browser to admin interface"""
    webbrowser.open('http://localhost:5000/admin')

if __name__ == '__main__':
    print("=" * 60)
    print("🎨 Project Admin Interface")
    print("=" * 60)
    print("\nStarting server at http://localhost:5000/admin")
    print("\nPress Ctrl+C to stop the server\n")
    
    # Open browser after a short delay
    Timer(1.5, open_browser).start()
    
    app.run(debug=True, port=5000, use_reloader=False)

