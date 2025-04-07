// Very simple sidebar toggle implementation
console.log('Sidebar script loaded');

// Global variables for direct access
var sidebarToggle;
var sidebar;

// Function to toggle sidebar visibility
function toggleSidebar() {
    console.log('Toggle clicked');
    if (sidebar && sidebarToggle) {
        if (sidebar.classList.contains('open')) {
            sidebar.classList.remove('open');
            sidebarToggle.classList.remove('open');
        } else {
            sidebar.classList.add('open');
            sidebarToggle.classList.add('open');
        }
    }
}

// Initialize elements and attach events
function init() {
    console.log('Initializing sidebar');
    
    // Get elements
    sidebarToggle = document.querySelector('.sidebar-toggle');
    sidebar = document.querySelector('.sidebar');
    
    // Log what we found
    console.log('Sidebar toggle found:', !!sidebarToggle);
    console.log('Sidebar found:', !!sidebar);
    
    // Attach event if elements exist
    if (sidebarToggle && sidebar) {
        console.log('Attaching click event');
        sidebarToggle.onclick = toggleSidebar;
    } else {
        console.log('Elements not found, will retry');
        setTimeout(init, 500);
    }
}

// Try to initialize as soon as possible
init();

// Also try when window loads
window.onload = init;
