document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const dropdownMenu = document.getElementById('dropdownMenu');

    menuToggle.addEventListener('click', function(e) {
        e.stopPropagation();
        dropdownMenu.classList.toggle('show');
    });
    
    document.addEventListener('click', function(e) {
        if (!dropdownMenu.contains(e.target) && !menuToggle.contains(e.target)) {
            dropdownMenu.classList.remove('show');
        }
    });
});
