window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) { // When scrolling more than 50px
        navbar.classList.add('heightDecrease'); // Add class name to change navigation bar height
    } else {
        navbar.classList.remove('heightDecrease'); // Remove class name to restore
    }
  });
