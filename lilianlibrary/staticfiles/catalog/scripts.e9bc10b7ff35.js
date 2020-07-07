window.addEventListener('DOMContentLoaded', event => {
    // Navbar dropdowns on mobile view retract when another is activated
    document.querySelector('#search-button').addEventListener('click', () => {
        // Menu dropdown retracts
        $('#navbarDisplayMenu').collapse('hide');
    });

    document.querySelector('#nav-button').addEventListener('click', () => {
        // Search dropdown retracts
        $('#navbarToggleSearch').collapse('hide');
    });
});
