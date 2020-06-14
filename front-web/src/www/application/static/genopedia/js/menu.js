// Responsive menu
var ww = document.body.clientWidth;

$(document).ready(function() {
		$('.navi_i ul li a').removeClass('active');
		var nav = $(location).attr('pathname');
		nav.indexOf(1);
		nav.toLowerCase();
		nav = nav.split("/")[1];
		console.log(nav);
		$('#'+nav).addClass('active');

	$(".navi_i li a").each(function() {
		if ($(this).next().length > 0) {
			$(this).addClass("parent");
		};
	})

	$(".toggleMenu").click(function(e) {
		e.preventDefault();
		$(this).toggleClass("active");
		$(".navi_i").toggle();
	});
	adjustMenu();

})

$(window).bind('resize orientationchange', function() {
	ww = document.body.clientWidth;
	adjustMenu();
});

var adjustMenu = function() {
	if (ww < 768) {
		$(".toggleMenu").css("display", "inline-block");
		if (!$(".toggleMenu").hasClass("active")) {
			$(".navi_i").hide();
		} else {
			$(".navi_i").show();
		}
		$(".navi_i li").unbind('mouseenter mouseleave');
		$(".navi_i li a.parent").unbind('click').bind('click', function(e) {
			// must be attached to anchor element to prevent bubbling
			e.preventDefault();
			$(this).parent("li").toggleClass("hover");
		});
	}
	else if (ww >= 768) {
		$(".toggleMenu").css("display", "none");
		$(".navi_i").show();
		$(".navi_i li").removeClass("hover");
		$(".navi_i li a").unbind('click');
		$(".navi_i li").unbind('mouseenter mouseleave').bind('mouseenter mouseleave', function() {
		 	// must be attached to li so that mouseleave is not triggered when hover over submenu
		 	$(this).toggleClass('hover');
		});
	}
}
// Responsive menu
