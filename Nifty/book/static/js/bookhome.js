$(document).ready(function(){
    // 当滚动超过300px时显示返回顶部按钮
    $(window).scroll(function(){
      if ($(this).scrollTop() > 50) {
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