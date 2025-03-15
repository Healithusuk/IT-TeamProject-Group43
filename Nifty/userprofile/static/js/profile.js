$(document).ready(function(){
  $('#searchInput-favorite').on('keyup', function(){
      var query = $(this).val().toLowerCase().trim();
      // 遍历每个收藏卡片
      $('.favorite-item').each(function(){
          // 获取卡片中所有文本内容
          var cardText = $(this).text().toLowerCase();
          // 如果卡片文本中包含查询字符串，则显示整个卡片（及其外层链接），否则隐藏
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
          // 获取整个卡片文本内容
          var text = $(this).text().toLowerCase();
          // 如果包含查询关键字，显示卡片；否则隐藏
          if(text.indexOf(query) !== -1){
              $(this).show();
          } else {
              $(this).hide();
          }
      });
  });
});

document.addEventListener("DOMContentLoaded", function() {
  // 获取当前 URL 的 hash 值
  var hash = window.location.hash;
  // 如果 hash 值为 #list-settings，则自动激活该 tab
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
      // 阻止事件冒泡到父级链接
      event.stopPropagation();
      // 阻止默认行为（例如阻止链接跳转）
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
              // 更新数量：找到对应类别的计数 <span>
              var $countSpan = $('#count-' + category);
              var currentCount = parseInt($countSpan.text(), 10);
              if (!isNaN(currentCount) && currentCount > 0) {
                  $countSpan.text(currentCount - 1);
              }
              $card.fadeOut(function(){
                  $(this).remove();
              });
            } else {
                alert("删除失败: " + response.message);
            }
          },
          error: function(xhr, status, error) {
              alert("请求出错: " + error);
          }
      });
  });
});

$(document).ready(function(){
  // 为每个切换按钮绑定事件
  $('.toggle-delete-btn').on('click', function(){
      // 找到当前类别，通过按钮的 id 提取类别（例如：toggle-delete-book -> book）
      var btnId = $(this).attr('id'); // "toggle-delete-book"
      // 也可以通过 data 属性存储类别，简单示例直接从 id 中取出
      var category = btnId.replace("toggle-delete-", "");
      
      // 切换当前类别所有删除按钮的显示隐藏
      $('.favorite-item[data-category="' + category + '"] .delete-icon').toggleClass('d-none');

      // 根据删除按钮是否显示来禁用或启用链接
      $('.favorite-item[data-category="' + category + '"]').each(function(){
        var $link = $(this).closest('a');
        // 如果当前收藏项中至少有一个删除按钮不隐藏，则禁用链接
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
  // 切换删除按钮显示/隐藏
  window.toggleDelete = function(reviewId) {
      var $card = $('#review-' + reviewId);
      var $deleteBtn = $card.find('.delete-btn');
      $deleteBtn.toggleClass('d-none');
  };

  // 删除评论，并移除卡片
  window.deleteReview = function(reviewId) {
      // 此处替换为你的删除评论接口 URL
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
                      // 更新评论总数
                      var $countSpan = $('#review-count');
                      var currentCount = parseInt($countSpan.text(), 10);
                      if (!isNaN(currentCount) && currentCount > 0) {
                          $countSpan.text(currentCount - 1);
                      }
                  });
              } else {
                  alert("删除失败: " + response.message);
              }
          },
          error: function(xhr, status, error) {
              alert("请求出错: " + error);
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
                // 更新关注和粉丝数量
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
