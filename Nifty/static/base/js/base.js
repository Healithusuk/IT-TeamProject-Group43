window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) { // 滚动超过50px时
        navbar.classList.add('heightDecrease'); // 添加类名以改变导航栏高度
    } else {
        navbar.classList.remove('heightDecrease'); // 移除类名以恢复
    }
  });
