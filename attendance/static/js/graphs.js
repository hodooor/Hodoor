$(document).ready(function () {
/*Work Time Doughnut Chart*/
    var ctx = $("#Work-Time-Chart");
    var dataWorkTime = [139.5, 15.5];
    var labelsWorkTime = ["Work Hours", "Not-work Hours"];
    var bgcolorsWorkTime = ["#009bd7","#cccccc"];

    var myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labelsWorkTime,
      datasets: [{
        backgroundColor: bgcolorsWorkTime,
        data: dataWorkTime
      }]
    }
    });

/*Assigned Time Doughnut Chart*/
    var ctx = $("#Assigned-Time-Chart");
    var dataWorkTime = [120.0, 19.5];
    var labelsWorkTime = ["Assigned Hours", "Unassigned Hours"];
    var bgcolorsWorkTime = ["#cccccc","#E74121"];

    var myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labelsWorkTime,
      datasets: [{
        backgroundColor: bgcolorsWorkTime,
        data: dataWorkTime
      }]
    }
    });
    
});




