$(".thing-carousel").slick({
  infinite: true,
  slidesToShow: 4,
  slidesToScroll: 4,
  prevArrow:
    '<button class="slick-prev slick-arrow"><img src="/static/images/arrow-left.svg" alt="Go left" /></button>',
  nextArrow:
    '<button class="slick-next slick-arrow"><img src="/static/images/arrow-right.svg" alt="Go right" /></button>',
  responsive: [
    {
      breakpoint: 992,
      settings: {
        slidesToShow: 3,
        slidesToScroll: 3,
      },
    },
    {
      breakpoint: 800,
      settings: {
        slidesToShow: 2,
        slidesToScroll: 2,
      },
    },
    {
      breakpoint: 450,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1,
      },
    },
  ],
});

$(document).ready(function () {
  var mb = $("#menu-button");
  mb.on("click", function (ev) {
    if (mb.hasClass("menu-open")) {
      $(document.body).removeClass("menu-open");
      mb.removeClass("menu-open").addClass("menu-closed");
      $("#menu-line-1").removeClass("disappear");
      $("#menu-line-2a").removeClass("rotate45");
      $("#menu-line-2b").removeClass("rotateminus45");
      $("#menu-line-3").removeClass("disappear");
    } else {
      $(document.body).addClass("menu-open");
      mb.removeClass("menu-closed").addClass("menu-open");
      $("#menu-line-1").addClass("disappear");
      $("#menu-line-2a").addClass("rotate45");
      $("#menu-line-2b").addClass("rotateminus45");
      $("#menu-line-3").addClass("disappear");
    }
  });
});

if (document.location.hostname === "www.thedatalab.org") {
  var script = document.createElement("script");
  script.defer = true;
  script.id = "plausible";
  script.setAttribute("data-domain", "thedatalab.org");
  script.src = "https://plausible.io/js/plausible.compat.js";
  document.head.appendChild(script);
}
