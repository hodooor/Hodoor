var tooltipData = [
	"This Month Quota - showing you a quota for this month. Which means hours you have to spare as worktime.",
	"This Month Work Time - showing you a time that you allready spared for work in this month. Work hours is time which you spared with working. Not-work time includes time spared for breaks.",
	"This Month Assigned Time - showing you a time you assigned to projects. All the time you spend with work should be assigned to projects. You can do this in sessions page.",
	"Today info panel - Each session has own ID, if you have any problem you can tell this ID to administrator. Current work hours are worked hours in this day you already have worked for. In panel's footer is shown last of your swipe.",
	"Terminal Emulator - you can use this buttons and interact with Hodoor. Same principe as with RFID Tags on hardware client terminal.",
	"Last month - this panel is showing you last month info. Working hours in last month etc.",
	
	"Duration of whole session from incomming to outgoing swipe.",
	"Clean work time. This value should be assigned to projects.",
	"Time, that was not assigned to projects. Should be 0 after end of month.",
	"Number of breaks during this session.",
	"Sum of duration of all breaks during this session.",
	"Session is open, if there is no outgoing swipe.",
	"Session is modified, if some of it's swipes were corrected.",
	
	"write next...",
];


var numOfTooltips = 0; 


/*--------Append all tooltips to their IDs----------*/
$(document).ready(function() {
	var TooltipsIds = [];
	var MinTooltipNum, MaxTooltipNum;

	$('.question').each(function(i) { //question is tooltiped by default
		numOfTooltips++;
		TooltipsIds[i] = $(this).attr('id').replace('tooltip', ''); //get only tooltip id number
	});
	MinTooltipNum = Math.min.apply(Math,TooltipsIds);
	MaxTooltipNum = Math.max.apply(Math,TooltipsIds);

	for(var n=0; n<=numOfTooltips; n++) {
		$('#tooltip'+(n+MinTooltipNum)).attr('title', tooltipData[n+MinTooltipNum-1]);
		console.log(TooltipsIds[n]);
		console.log('#tooltip'+(n+MinTooltipNum));
		console.log(tooltipData[n+MinTooltipNum-1]);		
	}
	console.log(numOfTooltips);
	console.log(MinTooltipNum);
	console.log(MaxTooltipNum);

});