#!/usr/bin/env python3
import csv
import json
import os
from pathlib import Path
import unicodedata

# Read the CSV file
projects = []
csv_path = 'notion-page/Stephan Schulz/Projects and Artworks f8c7057cd41f4367aa5303e122fd0b46.csv'
projects_dir = 'notion-page/Stephan Schulz/Projects and Artworks'

with open(csv_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['Name']
        year = row['Year']
        
        # Skip non-project entries
        if not name or not year or name in ['Acknowledgment', 'Biography and Curriculum Vitae']:
            continue
            
        # Create slug from name (without year for image matching)
        slug = name.lower()
        # Remove year from slug for image filename
        slug_no_year = slug.split(',')[0].strip()
        # Handle slashes - remove them for slug but keep spaces around them
        slug_no_year = slug_no_year.replace(' / ', '-').replace('/', '-')
        slug_no_year = slug_no_year.replace(':', '').replace('&', 'and')
        slug_no_year = slug_no_year.replace(' ', '-').replace('(', '').replace(')', '')
        slug_no_year = slug_no_year.replace('+', '-')
        slug_no_year = slug_no_year.replace('--', '-').replace('---', '-')
        slug_no_year = slug_no_year.replace('é', 'e').replace('ó', 'o').replace('ü', 'u')
        slug_no_year = slug_no_year.replace("'", '')
        
        # Full slug with year for detail pages
        slug = name.lower()
        slug = slug.replace(' / ', '-').replace('/', '-')
        slug = slug.replace(',', '').replace(':', '').replace('&', 'and')
        slug = slug.replace(' ', '-').replace('(', '').replace(')', '')
        slug = slug.replace('+', '-')
        slug = slug.replace('--', '-').replace('---', '-')
        slug = slug.replace('é', 'e').replace('ó', 'o').replace('ü', 'u')
        slug = slug.replace("'", '')
        
        # Find corresponding folder and image
        # Handle slashes in names - Notion folders use spaces instead
        name_base = name.split(',')[0].strip()
        name_base_normalized = name_base.replace(' / ', ' ')
        
        # Normalize Unicode for proper matching (macOS uses NFD, CSV uses NFC)
        name_base_norm = unicodedata.normalize('NFC', name_base)
        name_base_normalized_norm = unicodedata.normalize('NFC', name_base_normalized)
        
        folder_candidates = [
            f for f in os.listdir(projects_dir) 
            if os.path.isdir(os.path.join(projects_dir, f)) and 
            (name_base_norm in unicodedata.normalize('NFC', f) or 
             name_base_normalized_norm in unicodedata.normalize('NFC', f))
        ]
        
        image_path = None
        if folder_candidates:
            folder_path = os.path.join(projects_dir, folder_candidates[0])
            # Find first image in folder
            for ext in ['jpg', 'png', 'jpeg']:
                images = list(Path(folder_path).glob(f'*.{ext}'))
                if images:
                    image_path = f'assets/projects/{slug_no_year}.{ext}'
                    break
        
        project = {
            'name': name,
            'year': year,
            'collaborator': row['for'] if row['for'] else 'Stephan Schulz',
            'link': row['Official Site'],
            'role': row['I did'],
            'slug': slug,
            'image': image_path if image_path else f'assets/projects/{slug_no_year}.jpg',
            'hasDetailPage': bool(folder_candidates)
        }
        projects.append(project)

# Sort by year (descending)
projects.sort(key=lambda x: int(x['year']) if x['year'].isdigit() else 0, reverse=True)

# Write to JSON
with open('projects-data.json', 'w', encoding='utf-8') as f:
    json.dump(projects, f, indent=2, ensure_ascii=False)

print(f"✓ Generated {len(projects)} projects")
print(f"✓ Saved to projects-data.json")

