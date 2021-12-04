var items = {};
var newitem = 0;
var token = $('input[name="csrfmiddlewaretoken"]').attr("value");
$(document).ready(function () {
  $("#bar").focus();
  $(document).on("keypress", function (e) {
    if (e.which == 93) {
      Submit();
    }
  });

  $("#bar").on("keypress", function (e) {
    if (e.which == 13) {
      var bar = $(this).val();
      check(bar);
    }
  });

  $("#name").on("keypress", function (e) {
    if (e.which == 13 && $("#name").val().length > 0) {
      $("#price").focus();
    }
  });

  $("#price").on("keypress", function (e) {
    if (e.which == 13) {
      Submit();
    }
  });
  $("#sub-btn").click(function () {
    Submit();
    $("#bar").focus();
  });
});

function Submit() {
  if (
    $("#bar").val().length > 0 &&
    $("#price").val().length > 0 &&
    $("#name").val().length > 0
  ) {
    item = {
      bar: $("#bar").val(),
      name: $("#name").val(),
      price: $("#price").val(),
      newiteml: newitem,
    };
    $.ajax({
      url: "ajax/change_item/",
      type: "POST",
      data: {
        itemsl: JSON.stringify(item),
      },

      headers: { "X-CSRFToken": token },
      dataType: "json",
      success: function (data) {
        if (data.success == 1) {
          $("#bar").val("");
          $("#name").val("");
          $("#price").val("");
          $("#result").text("Success");
          $("#bar").focus();
        } else {
          $("#bar").focus();
          $("#result").text("Fail!");
        }
      },
    });
  }
}
function check(bar) {
  if (bar < 1) {
    return 1;
  }
  if (bar.length > 0) {
    $.ajax({
      url: "ajax/get_item/",
      data: {
        bar: bar,
      },
      dataType: "json",
      success: function (data) {
        if (data.bar == 0) {
          $("#name").focus();
          newitem = 1;
        } else {
          $("#name").val(data.name);
          $("#price").val(data.price);
          $("#name").focus();
          newitem = 0;
        }
      },
    });
  }
}
