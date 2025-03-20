// Control the back to top button
$(document).ready(function(){
  // Show back to top button when scrolling over 50px
  $(window).scroll(function(){
    if ($(this).scrollTop() > 50) {
      $('#backToTop').fadeIn();
    } else {
      $('#backToTop').fadeOut();
    }
  });
  // Smooth scrolling to the top when clicking a button
  $('#backToTop').click(function(){
    $('html, body').animate({scrollTop: 0}, 600);
    return false;
  });
});

// Control the animation
document.addEventListener('DOMContentLoaded', function() {
  var container = document.getElementById('search-page-main');
  // Determine if a URL has a query string
  if (window.location.search === '') {
    // No query parameters, first load, add animation class
    container.classList.add('animate');
  } else {
    // With query parameters, no animation is played and the final state is set directly
    container.style.opacity = 1;
    container.style.transform = 'translateY(0)';
  }
});
