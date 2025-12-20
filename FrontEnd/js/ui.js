// Sidebar
function toggleSidebar() {
    document.getElementById('sidebar')?.classList.toggle('collapsed');
}

// Dropdown UI
document.addEventListener('DOMContentLoaded', () => {
    const avatar = document.getElementById('avatar-dropdown-trigger');
    const menu = document.getElementById('user-dropdown');

    avatar?.addEventListener('click', e => {
        e.stopPropagation();
        menu.classList.toggle('hidden');
    });

    document.addEventListener('click', () => {
        menu?.classList.add('hidden');
    });
});
