$(document).ready(function(){
    $('.filter-btn').on('click', function(){
      var filter = $(this).attr('data-filter');
      // 更新按钮激活状态
      $('.filter-btn').removeClass('active');
      $(this).addClass('active');
      
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

$(document).ready(function(){
  // 当滚动超过300px时显示返回顶部按钮
  $(window).scroll(function(){
    if ($(this).scrollTop() > 300) {
      $('#backToTop').fadeIn();
    } else {
      $('#backToTop').fadeOut();
    }
  });
  
  // 点击按钮时平滑滚动到顶部
  $('#backToTop').click(function(){
    $('html, body').animate({scrollTop: 0}, 600);
    return false;
  });
});