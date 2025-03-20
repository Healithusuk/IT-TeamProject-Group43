// This is a jQuery function which belongs to the rating-star plugin
jQuery(document).ready(function () {
    $('#ratingwork').on('rating.change', function(event, value, caption) {
        $('#ratingwork').rating('update', value);
    });
    $("#input-21f").rating({
        starCaptions: function (val) {
            if (val < 3) {
                return val;
            } else {
                return 'high';
            }
        },
        starCaptionClasses: function (val) {
            if (val < 3) {
                return 'label label-danger';
            } else {
                return 'label label-success';
            }
        },
        hoverOnClear: false
    });
    var $inp = $('#rating-input');

    $inp.rating({
        min: 0,
        max: 5,
        step: 1,
        size: 'lg',
        showClear: false
    });
    $('#btn-rating-input').on('click', function () {
        $inp.rating('refresh', {
            showClear: true,
            disabled: !$inp.attr('disabled')
        });
    });
    $('.btn-danger').on('click', function () {
        $("#kartik").rating('destroy');
    });

    $('.btn-success').on('click', function () {
        $("#kartik").rating('create');
    });
    $inp.on('rating.change', function () {
        alert($('#rating-input').val());
    });
    $('.rb-rating').rating({
        'showCaption': true,
        'stars': '3',
        'min': '0',
        'max': '3',
        'step': '1',
        'size': 'xs',
        'starCaptions': {0: 'status:nix', 1: 'status:wackelt', 2: 'status:geht', 3: 'status:laeuft'}
    });
    $("#input-21c").rating({
        min: 0, max: 8, step: 0.5, size: "xl", stars: "8"
    });
});

// Control the back to top button
$(document).ready(function(){
    // Show back to top button when scrolling over 100px
    $(window).scroll(function(){
      if ($(this).scrollTop() > 100) {
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

// Control the favorite button change if user click it
$(document).ready(function(){
  // Get the CSRF token from the meta tag in the HTML head
  var csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
  // Attach a click event handler to the "add-favorite-btn" button
  $('#add-favorite-btn').on('click', function(){
    $.ajax({
      url: "add_to_favorite/",  
      type: "POST",
      data: {
        category: 'book',
        item_id: "{{ book.book_id }}",  
      },
      headers: { "X-CSRFToken": csrftoken },
      success: function(response) {
        if (response.success) {
          if(response.action === 'added') {
            // Modify button style: remove btn-outline-primary, add btn-outline-success
            $('#add-favorite-btn').removeClass('btn-outline-primary').addClass('btn-outline-success').text("Added to Favorites❤️");;
          } else {
            $('#add-favorite-btn').removeClass('btn-outline-success').addClass('btn-outline-primary').text("Add to Favorites🤍");;
          }
        }
      },
      error: function(xhr, status, error) {
      }
    });
  });
});
