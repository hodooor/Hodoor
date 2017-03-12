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
    //temp = $('.ext-link').html();
    //console.log(temp);
    //$('.ext-link').html(temp + ' <i class="fa fa-external-link" aria-hidden="true"></i>');
    $('.ext-link').append(' <i class="fa fa-external-link" aria-hidden="true"></i>');
    /*This functions makes color change on form icons*/
    /*$(".focused").focus(function(){
        var idcon;
        idcon = "#"+(this).id+"-icon";
        debugLog(idcon);
        $(idcon).removeClass("icon");
        $(idcon).addClass("icon-active");
    });
    $(".focused").focusout(function(){
        var idcon;
        idcon = "#"+(this).id+"-icon";
        $(idcon).removeClass("icon-active");
        $(idcon).addClass("icon");
    });*/
    
    /*Another functions*/
    //var style = $('#mystyle[rel=stylesheet]').attr('href');
    //debugLog(style);   

    /* __DROPDOWN MENUS__*/
      // Add slideDown animation to Bootstrap dropdown when expanding.
      $('#myDropdown').on('show.bs.dropdown', function() {
        $(this).find('.dropdown-menu').first().stop(true, true).slideDown('fast');
      }); 
      /*$('#myDropdown').on('mouseover', function() {
        $(this).find('.dropdown-menu').first().stop(true, true).slideDown('fast');
      });*/

      // Add slideUp animation to Bootstrap dropdown when collapsing.
      $('#myDropdown').on('hide.bs.dropdown', function() {
        $(this).find('.dropdown-menu').first().stop(true, true).slideUp('fast');
      });
      /*$('#myDropdown').on('mouseout', function() {
        $(this).find('.dropdown-menu').first().stop(true, true).slideUp('fast');
      });*/
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
          //$(this).find('.panel-arrow').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
      } 
      else 
      {
          $(this).parents('.panel').find('.panel-body').slideDown('fast');
          $(this).removeClass('panel-collapsed');
          //$(this).find('.panel-arrow').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
      }
    })
    $('.panel-collapsed').parents('.panel').find('.panel-body').hide();
    /* //__COLLABTIVE AND CLICKABLE FUNCTIONS__ */

    //Enable same height on panels
    $('.equal-height-panels .panel').matchHeight();

    /* __MAIN USERNAME COLOR MIXER__*/
    var username = $('#main-username').text();
        debugLog("users name is: "+username+" .");
    var usercount, firstLetter;
    usercount = username.length;
        debugLog(usercount);
        debugLog(username[0]);

    var color, colorSegment1, colorSegment2;
    function ColorMixer(usernametext) {  
    colorSegment1 = '';
    //colorSegment2 = '';
      for (var i = 0; i < 6; i++ ) {
        var help = usernametext.charCodeAt(i);
        colorSegment1 += Math.round((help%10));
      };
      /*for (var i = 3; i > 0; i-- ) {
        var help = usernametext.charCodeAt(i);
        colorSegment2 += Math.round((help%10));
      };*/
      //color = "#" + colorSegment1 + colorSegment2;
      color = "#" + colorSegment1;
      return color;
    }
    
    debugLog(ColorMixer(username));

    $('#main-usericon').css("background", ColorMixer(username));
        debugLog(color);
    firstLetter = username[0];
    $('#main-usericon').html(firstLetter);
    /* //__MAIN USERNAME COLOR MIXER__*/

    /* __COLOR MIXER 2 EDITION__ */
    /*var Uls = [];
    var UlsCount = 0;
    var triplen = [];
    $('body').find('.automaticColorMixer').each(function(i) {
      Uls[i] = $(this).attr('id');
      UlsCount++;
    });

    for(var i=0; i<UlsCount; i++) {

      Uls[i] = "#"+Uls[i];
        debugLog(Uls[i]);
      triplen[i] = $(Uls[i]).children('li').length;
        debugLog("len is:"+triplen[i]);

      var userNames = [];
      var userColors =[];
      var userInitials = [];

      $(Uls[i]).children('li').each(function(i) {
        $(this).addClass('prefix_'+i); //add prefix with num to list items of ul
        userNames.push($(this).text()); //save inner text as userName var
      });
      
      for(var n=0; n<triplen[i]; n++) {
        userInitials[n] = userNames[n][0]; //double array
        userColors[n] = ColorMixer(userNames[n]); //generate colors
        $(Uls[i]).children('.prefix_'+n).prepend("<span class='usericon small text-center'></span><span class='username'>");
        $(Uls[i]).children('.prefix_'+n).children('.usericon').css("background-color", userColors[n]);
        $(Uls[i]).children('.prefix_'+n).children('.usericon').text(userInitials[n]);
        $(Uls[i]).children('.prefix_'+n).append("</span>");
      }

      userNames = [];
      userColors =[];
      userInitials = [];
    
    }
    */
    /* //__COLOR MIXER 2 EDITION__ */

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

    /* __DATA TABLES ENABLE__ */
    // $('#users-with-sessions').DataTable();
    // $('#users-without-sessions').DataTable();



//end of document.ready()
});






/*Function to change stylesheet*/
//set another style: onclick="changeStyle('css/xxx.css');"
var sheetName;
function changeStyle(sheetName) {
    $('#mystyle[rel=stylesheet]').attr('href', sheetName);
    debugLog($('#mystyle[rel=stylesheet]').attr('href'));

    return 0;
}

