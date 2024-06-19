document.addEventListener('DOMContentLoaded', function () {
    var toggleButton = document.querySelector('.category-btn');
    var maincategoriesList = document.getElementById('maincategories-list');

    toggleButton.addEventListener('click', function () {
        if (maincategoriesList.style.display === 'none' || maincategoriesList.style.display ===
            '') {
            maincategoriesList.style.display = 'flex';
        } else {
            maincategoriesList.style.display = 'none';
        }
    });
});