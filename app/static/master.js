var activeNavItem = $('.nav-link');

activeNavItem.click(function(){
  activeNavItem.removeClass('active');
  $(this).addClass('active');  
});
