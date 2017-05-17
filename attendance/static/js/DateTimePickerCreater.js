function addDateTimePicker(id){
  /*Add timepicker to this field*/
  //separate max values
  var separateTime = $(id).val().split(":");
  var TimeHours = separateTime[0];
  var TimeMinutes = separateTime[1];
  var TimeSeconds = separateTime[2];
  //add timepicker with options
  $(id).datetimepicker({
    format: "HH:mm:ss",
    minDate: moment({
      h:0,
      m:0,
      s:0
    }),
    maxDate: moment({
      h:TimeHours,
      m:TimeMinutes,
      s:TimeSeconds
    })
  });
}
