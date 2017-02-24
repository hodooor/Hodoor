var tooltipData = [
	"This Month Quota - show's you a quota for this month. Which menas hours you have to spare as worktime.",
	"This Month Work Time - show's you a time that you allready spared for work in this month. Work hours is time which you spared with working. Not-work time includes time spared for breaks.",
	"this assign time",
	"terminal",
	"last mnth",
	"void",
];


var numOfTooltips = 0; 


/*--------Append all tooltips to their IDs----------*/
$(document).ready(function() {
	$('.question').each(function(i) {
		numOfTooltips++;
	});
	for(var n=0; n<=numOfTooltips; n++) {
		$('#tooltip'+n).attr('title', tooltipData[n-1]);
	}
});