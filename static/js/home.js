var items = {};
var token = $('input[name="csrfmiddlewaretoken"]').attr("value");
var amount = 0;
$(document).ready(function () {
  $("#sell").click(function () {
    var username = "response_msg";
  });
  $("#buy").click(function () {
    var username = "response_msg";
  });
});

$("#addfiles").click(function () {
  $.ajax({
    url: "ajax/addfiles/",
    data: {
      bar: 0,
    },
    dataType: "json",
    success: function (data) {
      if (data.success == 0) {
      }
    },
  });
});
