/*------------------------------------------
Author: Patrik Predny,
Title: My own JS functions, used for Hodoor
Year: 2017,
License: MIT,
------------------------------------------*/
console.info("functions.js loaded");
//CONFIGURATION VARIABLES
var debug = 0; //set true or false, true enables debugging mode
var thesis = 1; //presentation in school, disable some features
//Functions
var variable;
function debugLog(variable) {
    if(debug) console.debug(variable);
  return 0;
}
if(debug) console.info("You are in debugging mode");

$(document).ready(function(){
    /*Loader fnction only for content*/
    $('.content').ready(function(){
      $('.loader').fadeOut('fast',function(){
        $('.content').fadeIn('fast');
      });
    });
    //$('.aside').hide();

    var temp;
    $('.ext-link').append(' <i class="fa fa-external-link" aria-hidden="true"></i>');
    /* __DROPDOWN MENUS__*/
      // Add slideDown animation to Bootstrap dropdown when expanding.
      $('#myDropdown').on('show.bs.dropdown', function() {
        $(this).find('.dropdown-menu').first().stop(true, true).slideDown('fast');
      });
      // Add slideUp animation to Bootstrap dropdown when collapsing.
      $('#myDropdown').on('hide.bs.dropdown', function() {
        $(this).find('.dropdown-menu').first().stop(true, true).slideUp('fast');
      });

    /* //__DROPDOWN MENUS__*/

    /* __SCROLL TO TOP FUNCTIONS__*/
    //Show me scroll option
        $('.scrollup').hide();
        $(window).scroll(function () {
            if ($(this).scrollTop() > 100) {
                $('.scrollup').fadeIn();
            } else {
                $('.scrollup').fadeOut();
            }
        });
    //Scroll mechanism
       $('.scrollup').click(function () {
        $("html, body").animate({
            scrollTop: 0
        }, 'fast');
        return false;
        });
    /* //__SCROLL TO TOP FUNCTIONS__*/

    /* __TOOLTIPS__ */
    /*Enable tooltips*/
    $(function () {
      $('[data-toggle="tooltip"]').tooltip({
		  //placement: 'bottom'
	   });
    })

	$(function () {
      $('[data-toggle="popover"]').popover({
	      trigger: 'hover',
        container: 'body',
	   });
    })
    /* //__TOOLTIPS__ */

    /* __COLLABTIVE AND CLICKABLE FUNCTIONS__ */
    /* If empty then add class panel-collapsed and hide panel-body*/
    if($('#users-at-work li').length == 0) {
      $("#working-users").addClass('panel-collapsed');
      $('#working-users').removeClass('clickable');
    }
    if($('#users-on-break li').length == 0) {
      $("#break-users").addClass('panel-collapsed');
      $('#break-users').removeClass('clickable');
    }
    if($('#users-on-trip li').length == 0) {
      $("#trip-users").addClass('panel-collapsed');
      $('#trip-users').removeClass('clickable');
    }
    /*Hide/show panel-body on click on clickable class*/
    $(document).on('click', '.clickable', function(e){
      if(!$(this).hasClass('panel-collapsed'))
      {
          $(this).parents('.panel').find('.panel-body').slideUp('fast');
          $(this).addClass('panel-collapsed');
      }
      else
      {
          $(this).parents('.panel').find('.panel-body').slideDown('fast');
          $(this).removeClass('panel-collapsed');
      }
    })
    $('.panel-collapsed').parents('.panel').find('.panel-body').hide();
    /* //__COLLABTIVE AND CLICKABLE FUNCTIONS__ */

    //Enable same height on panels
    //$('.equal-height-panels .panel').matchHeight();

    /* __Navigable links from h2 titles generator__*/
    //navigable-bar
    //you can see it only on xs and sm screens,
    //navigables generates scrollable links
    var navigables = [];
    var navigableTitles = [];
    $('.navigable').each(function(i) {
      navigables.push($(this).attr('id'));
      navigableTitles.push($(this).attr('title'));
      $('.navigable-bar').append('<li><a href="#'+navigables+'" class="navigate btn btn-sm btn-primary btn-block">' + navigableTitles + '</a></li> ');
      navigables = [];
      navigableTitles = [];
    });
    //Scrolling top navigation menu
    $(".navigate").click(function() {
      var scrollToId = $(this).attr("href");
        $('html, body').animate({
            scrollTop: $(scrollToId).offset().top -55
        }, 'fast');
    });

	//automatize menu size
    $('#myDropdown').data("width", $('#myDropdown').width());
      debugLog("Width is: "+$('#myDropdown').data("width")+'px');
    $('#myDropdown > .dropdown-menu').css('width', $('#myDropdown').data("width") );
    $('#myDropdown').data("btn-width", ($('#myDropdown').data("width")-20)/2);
    $('#myDropdown').data("btn-width-wide", ($('#myDropdown').data("width")-20));
    $('.dropmenu-item-btn').css('width',($('#myDropdown').data("btn-width")));
    $('.dropmenu-item-btn').css('height',($('#myDropdown').data("btn-width")));
    $('.dropmenu-item-btn-wide').css('width',($('#myDropdown').data("btn-width-wide")));
    $('.dropmenu-item-btn-wide').css('height',($('#myDropdown').data("btn-width")));
      debugLog($('#myDropdown').data("btn-width"));
//end of document.ready()
});
