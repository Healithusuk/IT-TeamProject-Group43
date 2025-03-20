$(document).ready(function(){
    // When the document is fully loaded, bind a click event to all elements with the "filter-btn" class.
    $('.filter-btn').on('click', function(){
      // Get the filter criterion from the clicked button's "data-filter" attribute.
      var filter = $(this).attr('data-filter');
      // Remove the "active" class from all filter buttons to reset their state.
      $('.filter-btn').removeClass('active');
      $(this).addClass('active');
      
      // Loop through each element with the "results-body" class.
      $('.results-body').each(function(){
        var category = $(this).attr('data-category');
        if(filter === 'all' || category === filter) {
          $(this).show();
        } else {
          $(this).hide();
        }
      });
    });
});

// Control the back to top button
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