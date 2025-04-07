// Dark mode functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dark mode script loaded');
    
    // Get DOM elements
    const body = document.body;
    const toggleButton = document.getElementById('theme-toggle');
    
    // Exit if toggle button doesn't exist
    if (!toggleButton) {
        console.error('Theme toggle button not found');
        return;
    }
    
    const toggleIcon = toggleButton.querySelector('i');
    
    // Check if dark mode is enabled in localStorage
    const isDarkMode = localStorage.getItem('darkMode') === 'enabled';
    console.log('Dark mode from localStorage:', isDarkMode);
    
    // Set initial state
    if (isDarkMode) {
        console.log('Applying initial dark mode');
        body.classList.add('dark-mode');
        if (toggleIcon) {
            toggleIcon.classList.remove('fa-moon');
            toggleIcon.classList.add('fa-sun');
        }
    }
    
    // Add click event listener
    toggleButton.addEventListener('click', function() {
        console.log('Dark mode toggle clicked');
        
        // Toggle dark mode class on body
        body.classList.toggle('dark-mode');
        
        // Update localStorage and icon
        if (body.classList.contains('dark-mode')) {
            console.log('Switching to dark mode');
            localStorage.setItem('darkMode', 'enabled');
            if (toggleIcon) {
                toggleIcon.classList.remove('fa-moon');
                toggleIcon.classList.add('fa-sun');
            }
        } else {
            console.log('Switching to light mode');
            localStorage.setItem('darkMode', 'disabled');
            if (toggleIcon) {
                toggleIcon.classList.remove('fa-sun');
                toggleIcon.classList.add('fa-moon');
            }
        }
    });
});
