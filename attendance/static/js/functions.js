/*------------------------------------------
Author: Patrik Predny,
Title: My own JS functions, used for Hodoor
Year: 2017,
License: MIT,
------------------------------------------*/
console.info("functions.js loaded"); //let me know that tjhis is properly loaded
//CONFIGURATION VARIABLES
var debug = 0; //set true or false, true enables debugging mode
/*Functions*/
//function for console lg display, like debugg mode
var variable;
function debugLog(variable) {
    if(debug) console.debug(variable);
  return 0;
}
if(debug) console.info("You are in debugging mode");
//eof debugLog function

/*Call jQuery*/
$(document).ready(function(){
    /*Dynamically resize menu after window resize*/
    $(window).on('resize', function(){
      autoMenuResize();
    });

    /*Loader fnction only for content*/
    $('.content').ready(function(){
      $('.loader').fadeOut('fast',function(){
        $('.content').fadeIn('fast');
      });
    });
    //$('.aside').hide();

    var temp;
    $('.ext-link').append(' <i class="fa fa-external-link" aria-hidden="true"></i>');
    /* DROPDOWN MENUS - slide down */
      // Add slideDown animation to Bootstrap dropdown when expanding.
      $('#myDropdown').on('show.bs.dropdown', function() {
        $(this).find('.dropdown-menu').first().stop(true, true).slideDown('fast');
      });
      // Add slideUp animation to Bootstrap dropdown when collapsing.
      $('#myDropdown').on('hide.bs.dropdown', function() {
        $(this).find('.dropdown-menu').first().stop(true, true).slideUp('fast');
      });

    /* eof DROPDOWN MENUS */

    /* SCROLL TO TOP FUNCTIONS*/
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
    /* eof SCROLL TO TOP FUNCTIONS*/

    /* TOOLTIPS */
    //Enable tooltips
    $(function () {
      $('[data-toggle="tooltip"]').tooltip({
		  //placement: 'bottom'
	   });
    })
    //Enable POPOVERS
    $(function () {
      $('[data-toggle="popover"]').popover({
	      trigger: 'hover',
        container: 'body',
	   });
    })
    /* eof TOOLTIPS */

    /* COLLABTIVE AND CLICKABLE FUNCTIONS */
    //this function make slide-able aside blocks
    //If empty then add class panel-collapsed and hide panel-body
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
    /* eof COLLABTIVE AND CLICKABLE FUNCTIONS */

    /* Navigable links from h2 titles generator*/
    //navigable-bar
    //you can see it only on xs and sm screens,
    //navigables generates scrollable links
    //on mobile first method
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
//end of document.ready()
});


/* Auto Menu Resize function */
//automatize menu size
function autoMenuResize() {
  console.log("Menu was resized");
  //get width of my existing dropdown
  $('#myDropdown').data("width", $('#myDropdown').width());
    debugLog("Width is: "+$('#myDropdown').data("width")+'px');
  //set myDropdown width to their child
  $('#myDropdown > .dropdown-menu').css('width', $('#myDropdown').data("width") );
  $('#myDropdown').data("btn-width", ($('#myDropdown').data("width")-20)/2);
  $('#myDropdown').data("btn-width-wide", ($('#myDropdown').data("width")-20));
  //use some math to resize existing width data and write them to button blocks
  //for small buttons
  $('.dropmenu-item-btn').css('width',($('#myDropdown').data("btn-width")));
  $('.dropmenu-item-btn').css('height',($('#myDropdown').data("btn-width")));
  //for larger/wider buttons
  $('.dropmenu-item-btn-wide').css('width',($('#myDropdown').data("btn-width-wide")));
  $('.dropmenu-item-btn-wide').css('height',($('#myDropdown').data("btn-width")));
    debugLog($('#myDropdown').data("btn-width"));
}
