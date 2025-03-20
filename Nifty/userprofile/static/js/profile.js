$(document).ready(function(){
  $('#searchInput-favorite').on('keyup', function(){
      var query = $(this).val().toLowerCase().trim();
      // Iterate through each collection card
      $('.favorite-item').each(function(){
          // Get all the text in the card
          var cardText = $(this).text().toLowerCase();
          // Show the entire card (and its outer links) if it contains the query string in the card text, otherwise hide it
          if(cardText.indexOf(query) !== -1){
              $(this).closest('a').show();
          } else {
              $(this).closest('a').hide();
          }
      });
  });
});

$(document).ready(function(){
  $("#searchInput-reviews").on("keyup", function(){
      var query = $(this).val().toLowerCase().trim();
      
      $(".review-card").each(function(){
          // Get the entire card text content
          var text = $(this).text().toLowerCase();
          // If it contains the query keyword, show the card; otherwise hide it
          if(text.indexOf(query) !== -1){
              $(this).show();
          } else {
              $(this).hide();
          }
      });
  });
});

document.addEventListener("DOMContentLoaded", function() {
  // Get the hash value of the current URL
  var hash = window.location.hash;
  // If the hash value is #list-settings, then the tab is automatically activated
  if (hash === "#settings") {
    var triggerEl = document.getElementById('list-settings-list');
    if (triggerEl) {
      var tab = new bootstrap.Tab(triggerEl);
      tab.show();
    }
  }
});

$(document).ready(function(){
  var csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

  $('.delete-icon').on('click', function(event){
      // Prevent events from bubbling up to the parent link
      event.stopPropagation();
      // Blocking default behavior (e.g., blocking link jumps)
      event.preventDefault();
      var $card = $(this).closest('.favorite-item');
      var category = $card.data('category');
      var itemSelf = $card.data('item-self');

      

      $.ajax({
          url: "delete_favorite/",
          type: "POST",
          data: {
              category: category,
              item_self: itemSelf,
          },
          headers: { "X-CSRFToken": csrftoken },
          success: function(response) {
            if(response.success) {
              // Update quantity: find the count for the corresponding category <span>
              var $countSpan = $('#count-' + category);
              var currentCount = parseInt($countSpan.text(), 10);
              if (!isNaN(currentCount) && currentCount > 0) {
                  $countSpan.text(currentCount - 1);
              }
              $card.fadeOut(function(){
                  $(this).remove();
              });
            } else {
                alert("delete fail: " + response.message);
            }
          },
          error: function(xhr, status, error) {
              alert("error: " + error);
          }
      });
  });
});

$(document).ready(function(){
  // Bind events to each toggle button
  $('.toggle-delete-btn').on('click', function(){
      // Find the current category and extract the category by the id of the button.
      var btnId = $(this).attr('id'); // "toggle-delete-book"
      
      var category = btnId.replace("toggle-delete-", "");
      
      // Toggles the show-hide of all delete buttons for the current category
      $('.favorite-item[data-category="' + category + '"] .delete-icon').toggleClass('d-none');

      // Disable or enable links based on whether or not the delete button is displayed
      $('.favorite-item[data-category="' + category + '"]').each(function(){
        var $link = $(this).closest('a');
        // Disable links if at least one of the delete buttons in the current favorite item is not hidden
        if ($(this).find('.delete-icon').hasClass('d-none')) {
            $link.removeClass('disabled-link');
        } else {
            $link.addClass('disabled-link');
        }
    });
  });
});

$(document).ready(function(){
  var csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
  // Toggle delete button show/hide
  window.toggleDelete = function(reviewId) {
      var $card = $('#review-' + reviewId);
      var $deleteBtn = $card.find('.delete-btn');
      $deleteBtn.toggleClass('d-none');
  };

  // Delete comments and remove cards
  window.deleteReview = function(reviewId) {
      
      $.ajax({
          url: "delete_review/",
          type: "POST",
          data: {
              review_id: reviewId,
          },
          headers: { "X-CSRFToken": csrftoken },
          success: function(response) {
              if(response.success) {
                  $('#review-' + reviewId).fadeOut(function(){
                      $(this).remove();
                      // Update the total number of comments
                      var $countSpan = $('#review-count');
                      var currentCount = parseInt($countSpan.text(), 10);
                      if (!isNaN(currentCount) && currentCount > 0) {
                          $countSpan.text(currentCount - 1);
                      }
                  });
              } else {
                  alert("delete fail: " + response.message);
              }
          },
          error: function(xhr, status, error) {
              alert("error: " + error);
          }
      });
  };
});


function followUser(targetUserId) {
    var csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    $.ajax({
        url: "follow_user/",
        type: "POST",
        data: {
            target_user_id: targetUserId
        },
        headers: { "X-CSRFToken": csrftoken },
        success: function(response) {
            if(response.success) {
                if(response.action === 'followed') {
                    $('#follow-btn').removeClass('btn-outline-primary').addClass('btn-success').text("Following");
                } else {
                $('#follow-btn').removeClass('btn-success').addClass('btn-outline-primary').text("Follow");
                }
                // Update the number of followers and fans
                $('#follower-count').html('<strong>' + response.user_follower_num + '</strong> Follower');
            } else {
                alert("Operation failed: " + response.message);
            }
        },
        error: function(xhr, status, error) {
            alert("Request error: " + error);
        }
    });
}
