// Get the Carousel element by its ID.
var carouselElement = document.getElementById('carouselExampleFade');

var slideColors = ['#1100ff', '#ffffff', '#ffffff'];

// Listen for the event when the slide transition is completed.
carouselElement.addEventListener('slid.bs.carousel', function (event) {
  var currentIndex = event.to;
  var newColor = slideColors[currentIndex] || '#1100ff';

  // Change the color of all target elements (links within elements with class "auth-links").
  document.querySelectorAll('.auth-links a').forEach(function(link) {
    link.style.color = newColor;
  });
});

$(document).ready(function(){
  // Initializes all controls of the rating class, display only, no editing allowed.
  $('.rating').rating({
    displayOnly: true,
    showCaption: false,  // Hide the text of the scoring instructions
    step: 0.1
  });
  $('.kv-svg-heart').rating({
    theme: 'krajee-svg',
    filledStar: '<span class="krajee-icon krajee-icon-heart"></span>',
    emptyStar: '<span class="krajee-icon krajee-icon-heart"></span>',
    starCaptions: function (rating) {
        return rating == 1 ? 'One heart' : rating + ' hearts';
    },
    containerClass: 'is-heart'
});
});

document.addEventListener("DOMContentLoaded", function() {
  const cards = document.querySelectorAll('.card');
  
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('show');
        // Once the animation is triggered you can stop watching the element
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });
  
  cards.forEach(card => {
    observer.observe(card);
  });
});

$(document).ready(function(){
  // Show back to top button when scrolling over 300px
  $(window).scroll(function(){
    if ($(this).scrollTop() > 300) {
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