// rating-star plugin
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


// 
$(document).ready(function(){
   // Retrieve the CSRF token from the meta tag in the HTML header.
    var csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    // Attach a click event handler to the button with ID "add-favorite-btn".
    $('#add-favorite-btn').on('click', function(){
      // Send an AJAX POST request to the backend view URL "add_to_favorite/"
      $.ajax({
        url: "add_to_favorite/",  // 后端视图 URL
        type: "POST",
        data: {
          category: 'tv',
          item_id: "{{ tvshow.tvshow_id }}",  // 当前书籍的 ID
        },
        headers: { "X-CSRFToken": csrftoken },
        // Handle a successful response from the server.
        success: function(response) {
          if (response.success) {
            if(response.action === 'added') {
              // Update button styling: remove "btn-outline-primary", add "btn-outline-success", and update text.
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