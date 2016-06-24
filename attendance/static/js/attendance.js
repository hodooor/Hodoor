$(document).ready(function(){ //Calling jQuery when document.ready
	//===================================Tooltip=========================================
  $('[data-toggle="tooltip"]').tooltip(); //enables tooltip

  //===================================Show/Hide Swipes================================
  var SwipesBtn = $('#showAll'); //get identifier for clickable button
  var MaxNumOfRow = 12; //how many rows should be vissible
  var btnText1 = "View All Swipes";
  var btnText2 = "Hide until last " + MaxNumOfRow;
  var btnClass1 = "btn-primary";
  var btnClass2 = "btn-danger";
  var btnTitle1 = "Click to show all of swipes";
  var btnTitle2 = "Click to hide all records until last " + MaxNumOfRow;
  var rows = $('table.table tbody tr'); //get row indexes
  var rowsCount = rows.length; //get max count of table rows
  var btnState = 0; //bool, btnState if 0 then button is activated

  //calling functions after button event
  $(SwipesBtn).click(function() {
  	if(!btnState) {
			$(SwipesBtn).html(btnText2);
			$(SwipesBtn).removeClass(btnClass1);
			$(SwipesBtn).addClass(btnClass2);
			$(SwipesBtn).attr('data-original-title', btnTitle2)
			HideRows(rows);
			btnState = !btnState;
  	} else {
			$(SwipesBtn).html(btnText1);
			$(SwipesBtn).removeClass(btnClass2);
			$(SwipesBtn).addClass(btnClass1);
			$(SwipesBtn).attr('data-original-title', btnTitle1)
			UnhideRows(rows);
  		btnState = !btnState;
  	}
  });

  //Hidding/showing all of the swipes in SWIPES template
  function HideRows(rows) {
	    rows.filter('.hiddenRow').show();
  }
  function UnhideRows(rows) {
	    rows.filter('.hiddenRow').hide();
  }

	//=====================================Hidding last rows filter======================
	//hidding last rows, if rowIndex is lower than VALUE then remove hidding
	rows.filter(function( index ) { return index > rowsCount-MaxNumOfRow; }).removeClass("hiddenRow");

  //=====================================Sessions status color=========================
  $("td:contains('Complete')").each(function() {
    $(this).addClass("complete");
  });
  $("td:contains('Open')").each(function() {
    $(this).addClass("open");
  });

	//=====================================Debugging=====================================
	//console.log(rowsCount);
	//console.log(rows);

});
