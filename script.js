// Projects Gallery with Dynamic Loading
let allProjects = [];
let displayedProjects = [];
let currentSort = 'year';
const PROJECTS_PER_PAGE = 16;
let currentPage = 1;

document.addEventListener('DOMContentLoaded', function() {
    loadProjects();
    initializeUI();
});

// Load projects from JSON
async function loadProjects() {
    try {
        const response = await fetch('projects-data.json');
        allProjects = await response.json();
        displayProjects();
    } catch (error) {
        console.error('Error loading projects:', error);
        // Fallback to manual data if JSON fails
        loadFallbackProjects();
    }
}

// Fallback data (the 8 projects we have images for)
function loadFallbackProjects() {
    allProjects = [
        { name: 'Pulsos del agua, 2025', year: '2025', collaborator: 'Nelson Vergara', image: 'assets/projects/pulsos-del-agua.jpg', slug: 'pulsos-del-agua-2025' },
        { name: 'Transparency Display, 2024', year: '2024', collaborator: 'Rafael Lozano-Hemmer', image: 'assets/projects/transparency-display.png', slug: 'transparency-display-2024' },
        { name: 'Pulse Agglomerate, 2024', year: '2024', collaborator: 'Rafael Lozano-Hemmer', image: 'assets/projects/pulse-agglomerate.jpg', slug: 'pulse-agglomerate-2024' },
        { name: 'Climate Parliament, 2024', year: '2024', collaborator: 'Rafael Lozano-Hemmer', image: 'assets/projects/climate-parliament.jpg', slug: 'climate-parliament-2024' },
        { name: 'Pulse Voronoi, 2024', year: '2024', collaborator: 'Rafael Lozano-Hemmer', image: 'assets/projects/pulse-voronoi.jpg', slug: 'pulse-voronoi-2024' },
        { name: 'Kristallstimmen, 2024', year: '2024', collaborator: 'Rafael Lozano-Hemmer', image: 'assets/projects/kristallstimmen.jpg', slug: 'kristallstimmen-2024' },
        { name: 'Dark Ride, 2024', year: '2024', collaborator: 'Rafael Lozano-Hemmer', image: 'assets/projects/dark-ride.jpg', slug: 'dark-ride-2024' },
        { name: 'Collider, 2023', year: '2023', collaborator: 'Rafael Lozano-Hemmer', image: 'assets/projects/collider.jpg', slug: 'collider-2023' }
    ];
    displayProjects();
}

// Display projects
function displayProjects() {
    const grid = document.getElementById('projects-grid');
    const loadMoreContainer = document.getElementById('load-more-container');
    
    // Sort projects
    let sortedProjects = [...allProjects];
    if (currentSort === 'year') {
        sortedProjects.sort((a, b) => {
            const yearA = parseInt(a.year) || 0;
            const yearB = parseInt(b.year) || 0;
            return yearB - yearA;
        });
    } else if (currentSort === 'alpha') {
        sortedProjects.sort((a, b) => a.name.localeCompare(b.name));
    }
    
    // Get projects to display
    const projectsToShow = sortedProjects.slice(0, currentPage * PROJECTS_PER_PAGE);
    displayedProjects = projectsToShow;
    
    // Clear grid
    grid.innerHTML = '';
    
    // Create project cards
    projectsToShow.forEach((project, index) => {
        const card = createProjectCard(project, index);
        grid.appendChild(card);
    });
    
    // Show/hide load more button
    if (projectsToShow.length < sortedProjects.length) {
        loadMoreContainer.classList.remove('hidden');
    } else {
        loadMoreContainer.classList.add('hidden');
    }
}

// Create a project card element
function createProjectCard(project, index) {
    const card = document.createElement('div');
    card.className = 'project-card';
    card.style.animationDelay = `${(index % PROJECTS_PER_PAGE) * 0.05}s`;
    
    // Make card clickable - prioritize detail pages over external links
    card.style.cursor = 'pointer';
    card.addEventListener('click', () => {
        if (project.isCV) {
            // CV links directly to cv.html
            window.location.href = 'cv.html';
        } else if (project.hasDetailPage) {
            // Go to project folder (contains index.html)
            window.location.href = `projects/${project.slug}/`;
        } else if (project.link) {
            // Fallback to external link if no detail page
            window.open(project.link, '_blank');
        }
    });
    
    // Create image container
    const imageDiv = document.createElement('div');
    imageDiv.className = 'project-image';
    
    const img = document.createElement('img');
    img.src = project.image;
    img.alt = project.name;
    img.loading = 'lazy';
    
    // Handle image load errors
    img.onerror = function() {
        this.style.display = 'none';
        imageDiv.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
    };
    
    imageDiv.appendChild(img);
    
    // Create info container
    const infoDiv = document.createElement('div');
    infoDiv.className = 'project-info';
    
    const title = document.createElement('h3');
    title.className = 'project-title';
    title.textContent = project.name;
    
    const collaborator = document.createElement('p');
    collaborator.className = 'project-collaborator';
    collaborator.textContent = project.collaborator;
    
    infoDiv.appendChild(title);
    infoDiv.appendChild(collaborator);
    
    card.appendChild(imageDiv);
    card.appendChild(infoDiv);
    
    return card;
}

// Initialize UI controls
function initializeUI() {
    const viewButtons = document.querySelectorAll('.view-btn');
    const loadMoreBtn = document.getElementById('load-more-btn');
    
    // Handle view button clicks
    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            viewButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            const view = this.getAttribute('data-view');
            currentSort = view;
            currentPage = 1; // Reset to first page
            displayProjects();
        });
    });
    
    // Handle load more button
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', function() {
            currentPage++;
            displayProjects();
            
            // Smooth scroll to new content
            setTimeout(() => {
                const lastVisibleCard = document.querySelectorAll('.project-card')[(currentPage - 1) * PROJECTS_PER_PAGE];
                if (lastVisibleCard) {
                    lastVisibleCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }
            }, 100);
        });
    }
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#' || href === '#about') {
                e.preventDefault();
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Press '1' for Year view
        if (e.key === '1' && !e.metaKey && !e.ctrlKey) {
            const yearBtn = document.querySelector('[data-view="year"]');
            if (yearBtn) yearBtn.click();
        }
        
        // Press '2' for Alphabetical view
        if (e.key === '2' && !e.metaKey && !e.ctrlKey) {
            const alphaBtn = document.querySelector('[data-view="alpha"]');
            if (alphaBtn) alphaBtn.click();
        }
    });
}

// Optional: Infinite scroll (uncomment to enable)
/*
window.addEventListener('scroll', function() {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 500) {
        const loadMoreBtn = document.getElementById('load-more-btn');
        if (loadMoreBtn && !loadMoreBtn.disabled && !document.getElementById('load-more-container').classList.contains('hidden')) {
            loadMoreBtn.click();
        }
    }
});
*/
