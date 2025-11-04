// Project Admin Interface JavaScript

let loadedImages = [];
let draggedElement = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    updatePreview();
});

function initializeEventListeners() {
    // Load images button
    document.getElementById('load-images-btn').addEventListener('click', loadImages);
    
    // Form inputs - update preview on change
    const formInputs = document.querySelectorAll('#project-form input, #project-form textarea');
    formInputs.forEach(input => {
        input.addEventListener('input', updatePreview);
    });
    
    // Form submission
    document.getElementById('project-form').addEventListener('submit', handleSubmit);
    
    // Form reset
    document.getElementById('project-form').addEventListener('reset', () => {
        loadedImages = [];
        renderImages();
        updatePreview();
        hideMessage();
    });
}

async function loadImages() {
    const folderPath = document.getElementById('image-folder').value.trim();
    
    if (!folderPath) {
        showMessage('Please enter a folder path', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/browse-images', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ path: folderPath })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to load images');
        }
        
        loadedImages = data.images;
        await renderImages();
        updatePreview();
        showMessage(`Loaded ${loadedImages.length} images`, 'success');
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

async function renderImages() {
    const container = document.getElementById('images-container');
    
    if (loadedImages.length === 0) {
        container.innerHTML = '<p class="placeholder-text">Load images from a folder to begin</p>';
        return;
    }
    
    // Load base64 data for each image if not already loaded
    const imagesWithData = [];
    for (let index = 0; index < loadedImages.length; index++) {
        const img = loadedImages[index];
        if (!img.base64) {
            try {
                const response = await fetch('/api/serve-local-image', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ path: img.path })
                });
                const data = await response.json();
                img.base64 = data.data;
            } catch (error) {
                console.error('Failed to load image:', img.path, error);
                img.base64 = '';
            }
        }
        imagesWithData.push({ ...img, index });
    }
    
    const listHTML = imagesWithData.map((img) => `
        <div class="image-item" draggable="true" data-index="${img.index}">
            <span class="drag-handle">☰</span>
            <span class="image-number">${String(img.index + 1).padStart(2, '0')}</span>
            <img src="${img.base64 || 'data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\'/%3E'}" class="image-thumbnail" alt="${img.name}">
            <span class="image-name" title="${img.name}">${img.name}</span>
            <button type="button" class="remove-image" data-index="${img.index}">×</button>
        </div>
    `).join('');
    
    container.innerHTML = `<div class="image-list">${listHTML}</div>`;
    
    // Add drag and drop listeners
    const items = container.querySelectorAll('.image-item');
    items.forEach(item => {
        item.addEventListener('dragstart', handleDragStart);
        item.addEventListener('dragover', handleDragOver);
        item.addEventListener('drop', handleDrop);
        item.addEventListener('dragend', handleDragEnd);
    });
    
    // Add remove button listeners
    const removeButtons = container.querySelectorAll('.remove-image');
    removeButtons.forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const index = parseInt(e.target.dataset.index);
            loadedImages.splice(index, 1);
            await renderImages();
            updatePreview();
        });
    });
}

// Drag and Drop handlers
function handleDragStart(e) {
    draggedElement = e.target;
    e.target.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
}

function handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }
    e.dataTransfer.dropEffect = 'move';
    return false;
}

async function handleDrop(e) {
    if (e.stopPropagation) {
        e.stopPropagation();
    }
    
    if (draggedElement !== e.target.closest('.image-item')) {
        const draggedIndex = parseInt(draggedElement.dataset.index);
        const targetIndex = parseInt(e.target.closest('.image-item').dataset.index);
        
        // Reorder array
        const [removed] = loadedImages.splice(draggedIndex, 1);
        loadedImages.splice(targetIndex, 0, removed);
        
        await renderImages();
        updatePreview();
    }
    
    return false;
}

function handleDragEnd(e) {
    e.target.classList.remove('dragging');
}

function updatePreview() {
    const name = document.getElementById('name').value || 'Project Name';
    const year = document.getElementById('year').value || '2024';
    const collaborator = document.getElementById('collaborator').value || 'Collaborator';
    const officialSite = document.getElementById('official_site').value;
    const role = document.getElementById('role').value || '';
    const description = document.getElementById('description').value || '';
    const acknowledgment = document.getElementById('acknowledgment').value || '';
    
    // Update title and breadcrumb
    document.getElementById('preview-name').textContent = `${name}, ${year}`;
    document.getElementById('preview-title').textContent = `${name}, ${year}`;
    
    // Update properties table
    document.getElementById('preview-collaborator').textContent = collaborator;
    document.getElementById('preview-year').textContent = year;
    
    // Update/add official site row
    const propertiesTable = document.getElementById('preview-properties');
    let officialSiteRow = propertiesTable.querySelector('.official-site-row');
    
    if (officialSite) {
        const displayText = officialSite.replace('https://', '').replace('http://', '').replace('www.', '');
        const shortText = displayText.length > 50 ? 'View Project' : displayText;
        
        if (!officialSiteRow) {
            officialSiteRow = document.createElement('tr');
            officialSiteRow.className = 'property-row official-site-row';
            propertiesTable.insertBefore(officialSiteRow, propertiesTable.children[2]);
        }
        
        officialSiteRow.innerHTML = `
            <th><span class="icon">🔗</span>Official Site</th>
            <td><a href="${officialSite}" target="_blank" class="url-value">${shortText}</a></td>
        `;
    } else if (officialSiteRow) {
        officialSiteRow.remove();
    }
    
    // Update/add role row
    let roleRow = propertiesTable.querySelector('.role-row');
    
    if (role) {
        const roles = role.split(',').map(r => r.trim()).filter(r => r);
        const tagsHTML = roles.map(r => `<span class="tag">${r}</span>`).join('');
        
        if (!roleRow) {
            roleRow = document.createElement('tr');
            roleRow.className = 'property-row role-row';
            propertiesTable.appendChild(roleRow);
        }
        
        roleRow.innerHTML = `
            <th><span class="icon">📋</span>I did</th>
            <td>${tagsHTML}</td>
        `;
    } else if (roleRow) {
        roleRow.remove();
    }
    
    // Update description
    const descriptionEl = document.getElementById('preview-description');
    if (description) {
        const paragraphs = description.split('\n\n').filter(p => p.trim());
        descriptionEl.innerHTML = paragraphs.map(p => `<p>${p.trim()}</p>`).join('\n');
    } else {
        descriptionEl.innerHTML = '<p>Description will appear here...</p>';
    }
    
    // Update images
    const imagesEl = document.getElementById('preview-images');
    if (loadedImages.length > 0 && loadedImages[0].base64) {
        let imagesHTML = '';
        
        // First two images in grid
        if (loadedImages.length >= 2 && loadedImages[1].base64) {
            imagesHTML += `
                <div class="image-grid">
                    <div class="image-column">
                        <img src="${loadedImages[0].base64}" alt="${name}">
                    </div>
                    <div class="image-column">
                        <img src="${loadedImages[1].base64}" alt="${name}">
                    </div>
                </div>
            `;
        } else if (loadedImages.length === 1 && loadedImages[0].base64) {
            imagesHTML += `
                <div class="image-full">
                    <img src="${loadedImages[0].base64}" alt="${name}">
                </div>
            `;
        }
        
        // Remaining images full width
        for (let i = 2; i < loadedImages.length; i++) {
            if (loadedImages[i].base64) {
                imagesHTML += `
                    <div class="image-full">
                        <img src="${loadedImages[i].base64}" alt="${name}">
                    </div>
                `;
            }
        }
        
        imagesEl.innerHTML = imagesHTML;
    } else {
        imagesEl.innerHTML = '';
    }
    
    // Update acknowledgment
    const acknowledgmentEl = document.getElementById('preview-acknowledgment');
    const isRLH = collaborator.toLowerCase().includes('rafael lozano-hemmer');
    
    if (isRLH) {
        acknowledgmentEl.innerHTML = `
            <hr>
            <h3>Acknowledgment</h3>
            <p>This artwork by Rafael Lozano-Hemmer is the result of the combined efforts of a talented and diverse group of professionals. Each person has contributed unique skills and expertise to the creation of this piece. For more information about the team and their roles, please visit our <a href="https://www.lozano-hemmer.com/" target="_blank" class="url-value">official website</a>.</p>
        `;
    } else if (acknowledgment) {
        acknowledgmentEl.innerHTML = `
            <hr>
            <h3>Acknowledgment</h3>
            <p>${acknowledgment}</p>
        `;
    } else {
        acknowledgmentEl.innerHTML = '';
    }
}

async function handleSubmit(e) {
    e.preventDefault();
    
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoading = submitBtn.querySelector('.btn-loading');
    
    // Validate
    if (loadedImages.length === 0) {
        showMessage('Please load at least one image', 'error');
        return;
    }
    
    // Disable button and show loading
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline-flex';
    
    try {
        const formData = {
            name: document.getElementById('name').value,
            year: document.getElementById('year').value,
            collaborator: document.getElementById('collaborator').value,
            official_site: document.getElementById('official_site').value,
            role: document.getElementById('role').value,
            description: document.getElementById('description').value,
            acknowledgment: document.getElementById('acknowledgment').value,
            images: loadedImages
        };
        
        const response = await fetch('/api/create-project', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to create project');
        }
        
        showMessage('Project created successfully! Redirecting...', 'success');
        
        // Redirect after a longer delay to ensure files are written
        setTimeout(() => {
            window.location.href = data.url;
        }, 2500);
        
    } catch (error) {
        showMessage(error.message, 'error');
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
    }
}

function showMessage(message, type) {
    const messageArea = document.getElementById('message-area');
    messageArea.textContent = message;
    messageArea.className = type;
}

function hideMessage() {
    const messageArea = document.getElementById('message-area');
    messageArea.style.display = 'none';
    messageArea.className = '';
}

