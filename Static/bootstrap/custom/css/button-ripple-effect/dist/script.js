jQuery(document).ready(function($){
// standard on load code goes here with $ prefix
// note: the $ is setup inside the anonymous function of the ready command
	'use strict';

  	var $ripple = $('.js-ripple');

  	$ripple.on('click.ui.ripple', function(e) {

		var $this = $(this);
		var $offset = $this.parent().offset();
		var $circle = $this.find('.ripple-circle');

		var x = e.pageX - $offset.left;
		var y = e.pageY - $offset.top;

		$circle.css({
	  		top: y + 'px',
	  		left: x + 'px'
		});

		$this.addClass('is-active');

  	});

  	$ripple.on('animationend webkitAnimationEnd oanimationend MSAnimationEnd', function(e) {
		$(this).removeClass('is-active');
  	});
});