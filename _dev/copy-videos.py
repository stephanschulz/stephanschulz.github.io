#!/usr/bin/env python3
"""
Copy missing videos from notion-page export to project folders
and update HTML to include video elements
"""

import os
import shutil
import re
from pathlib import Path
from bs4 import BeautifulSoup

# Get project root
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
os.chdir(project_root)

# Video mapping: notion folder → project slug
VIDEO_MAPPING = {
    'Zeitraumlupe, 2001': {
        'slug': 'zeitraumlupe-2001',
        'video': 'notion-page/Stephan Schulz/Projects and Artworks/Zeitraumlupe, 2001/zlupe.mov'
    },
    'Embodied Light Beacons, 2022': {
        'slug': 'embodied-light-beacons-2022',
        'video': 'notion-page/Stephan Schulz/Projects and Artworks/Embodied Light Beacons, 2022/3xposeNet_small.mov'
    },
    'Feuerland, 2004': {
        'slug': 'feuerland-2004',
        'video': 'notion-page/Stephan Schulz/Projects and Artworks/Feuerland, 2004/feuerland.mov'
    },
    'Pulsos del agua, 2025': {
        'slug': 'pulsos-del-agua-2025',
        'video': 'notion-page/Stephan Schulz/Projects and Artworks/Pulsos del agua, 2025/Untitled.mov'
    },
    'Pulse Agglomerate, 2024': {
        'slug': 'pulse-agglomerate-2024',
        'video': 'notion-page/Stephan Schulz/Projects and Artworks/Pulse Agglomerate, 2024/IMG_6419-small2.mov'
    },
    'Grüßt uns\'re Berge, 2000': {
        'slug': 'grußt-unsre-berge-2000',
        'video': 'notion-page/Stephan Schulz/Projects and Artworks/Grüßt uns\'re Berge, 2000/GrAAt_unsre_Berge___greetings_to_the_mountains.mp4'
    },
    'Kristallstimmen, 2024': {
        'slug': 'kristallstimmen-2024',
        'video': 'notion-page/Stephan Schulz/Projects and Artworks/Kristallstimmen, 2024/PXL_20241122_095517448.TS.mp4'
    },
    'Password Breach, 2021': {
        'slug': 'password-breach-2021',
        'video': 'notion-page/Stephan Schulz/Projects and Artworks/Password Breach, 2021/20211128_180913.mp4'
    }
}

def get_next_number(project_folder):
    """Get the next number for a file in the images folder"""
    images_folder = os.path.join(project_folder, 'images')
    if not os.path.exists(images_folder):
        return 1
    
    # Find all numbered files
    files = os.listdir(images_folder)
    numbers = []
    for f in files:
        match = re.match(r'^(\d+)_', f)
        if match:
            numbers.append(int(match.group(1)))
    
    return max(numbers) + 1 if numbers else 1

def copy_video_and_update_html(project_name, project_data):
    """Copy video to project folder and update HTML"""
    slug = project_data['slug']
    video_path = project_data['video']
    
    project_folder = os.path.join('projects', slug)
    images_folder = os.path.join(project_folder, 'images')
    html_file = os.path.join(project_folder, 'index.html')
    
    # Check if project exists
    if not os.path.exists(project_folder):
        print(f"❌ Project folder not found: {project_folder}")
        return False
    
    # Check if video exists in notion export
    if not os.path.exists(video_path):
        print(f"❌ Video not found: {video_path}")
        return False
    
    # Get video extension
    video_ext = os.path.splitext(video_path)[1]
    
    # Get next number
    next_num = get_next_number(project_folder)
    new_video_name = f"{next_num:02d}_video{video_ext}"
    new_video_path = os.path.join(images_folder, new_video_name)
    
    # Copy video
    print(f"\n📹 {project_name}")
    print(f"   Copying: {os.path.basename(video_path)}")
    print(f"   To:      {new_video_name}")
    
    shutil.copy2(video_path, new_video_path)
    video_size_mb = os.path.getsize(new_video_path) / (1024 * 1024)
    print(f"   ✅ Copied ({video_size_mb:.2f} MB)")
    
    # Update HTML
    if not os.path.exists(html_file):
        print(f"   ⚠️  HTML file not found: {html_file}")
        return True  # Video copied but HTML not updated
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the page-body div
    page_body = soup.select_one('.page-body')
    if not page_body:
        print(f"   ⚠️  Could not find .page-body in HTML")
        return True
    
    # Create video element
    video_html = f'''
        <div class="image-full">
            <video controls loading="lazy">
                <source src="images/{new_video_name}" type="video/{video_ext[1:]}">
                Your browser does not support the video tag.
            </video>
        </div>'''
    
    # Find where to insert (before <hr> if exists, otherwise at end)
    hr_tag = page_body.find('hr')
    if hr_tag:
        # Insert before the hr
        hr_tag.insert_before(BeautifulSoup(video_html, 'html.parser'))
    else:
        # Append to page-body
        page_body.append(BeautifulSoup(video_html, 'html.parser'))
    
    # Write updated HTML
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"   ✅ HTML updated with video element")
    
    return True

def main():
    print("=" * 70)
    print("COPYING VIDEOS FROM NOTION EXPORT TO PROJECT FOLDERS")
    print("=" * 70)
    
    success_count = 0
    fail_count = 0
    
    for project_name, project_data in VIDEO_MAPPING.items():
        try:
            if copy_video_and_update_html(project_name, project_data):
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f"\n❌ Error processing {project_name}: {e}")
            fail_count += 1
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✅ Successfully processed: {success_count}")
    print(f"❌ Failed: {fail_count}")
    print("=" * 70)

if __name__ == '__main__':
    main()

