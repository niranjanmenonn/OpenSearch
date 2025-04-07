let scale = 1;
const ZOOM_SPEED = 0.1;

function zoomIn() {
    scale += ZOOM_SPEED;
    updateZoom();
}

function zoomOut() {
    scale = Math.max(0.5, scale - ZOOM_SPEED);
    updateZoom();
}

function resetZoom() {
    scale = 1;
    updateZoom();
}

function updateZoom() {
    const image = document.getElementById('concept-map-image');
    image.style.transform = `scale(${scale})`;
}
