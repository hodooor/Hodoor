/*------------------------------------------
Author: Patrik Predny,
Title: My own JS functions, used for Hodoor
Year: 2017,
License: MIT,
------------------------------------------*/

//CONFIGURATION VARIABLES
var debug = 0; //set true or false, true enables debugging mode

//Functions
var variable;
function debugLog(variable) {
    if(debug) console.log(variable);
    
    return 0;
}

/*
function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}*/

$(document).ready(function(){ 
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
      $('[data-toggle="tooltip"]').tooltip();
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