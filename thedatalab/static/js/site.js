$('.thing-carousel').slick({
  infinite: true,
  slidesToShow: 4,
  slidesToScroll: 4,
  prevArrow: '<button class="slick-prev slick-arrow"><img src="/static/images/arrow-left.svg" /></button>',
  nextArrow: '<button class="slick-next slick-arrow"><img src="/static/images/arrow-right.svg" /></button>'
});

$(document).ready(function() {
    var mb = $('#menu-button');
    mb.on('click', function(ev) {
        if(mb.hasClass('menu-open')) {
            $(document.body).removeClass('menu-open');
            mb.removeClass('menu-open').addClass('menu-closed');
            $('#menu-line-1').removeClass('disappear');
            $('#menu-line-2a').removeClass('rotate45');
            $('#menu-line-2b').removeClass('rotateminus45');
            $('#menu-line-3').removeClass('disappear');
        } else {
            $(document.body).addClass('menu-open');
            mb.removeClass('menu-closed').addClass('menu-open');
            $('#menu-line-1').addClass('disappear');
            $('#menu-line-2a').addClass('rotate45');
            $('#menu-line-2b').addClass('rotateminus45');
            $('#menu-line-3').addClass('disappear');
        }
        
    });
});
