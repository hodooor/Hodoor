//setInterval(function(){ console.log("Ahoj Patričku :)"); }, 1000);
$(document).ready(function(){
	//Tooltip info in SWIPES template
  $('[data-toggle="tooltip"]').tooltip(); //enables tooltip

  //Hidding and showing All of the swipes in SWIPES template
  var rows = $('table.table tbody tr');
	$('#showAll').click(function() {
	    rows.filter('.hiddenRow').show();
    	$('#showAll').addClass("hide");	
	});
	var MaxNumOfRow = 12;
	rows.filter(function( index ) { return index < MaxNumOfRow; }).removeClass("hiddenRow"); //if rowIndex is lower than VALUE then remoce hidding

});


