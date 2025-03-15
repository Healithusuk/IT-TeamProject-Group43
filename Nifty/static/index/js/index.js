// 获取 Carousel 元素
var carouselElement = document.getElementById('carouselExampleFade');

// 定义一个数组，用于存储每个幻灯片对应的颜色
var slideColors = ['#1100ff', '#ffffff', '#ffffff'];

// 监听幻灯片切换完成后的事件
carouselElement.addEventListener('slid.bs.carousel', function (event) {
  // event.to 属性是新幻灯片的索引
  var currentIndex = event.to;
  // 根据索引获取对应的颜色
  var newColor = slideColors[currentIndex] || '#1100ff';

  // 修改目标元素的颜色
  document.querySelectorAll('.auth-links a').forEach(function(link) {
    link.style.color = newColor;
  });
});

$(document).ready(function(){
  // 初始化所有 rating 类的控件，只显示，不允许编辑
  $('.rating').rating({
    displayOnly: true,
    showCaption: false,  // 隐藏评分说明文字
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
        // 一旦动画触发后可以停止观察该元素
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });
  
  cards.forEach(card => {
    observer.observe(card);
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