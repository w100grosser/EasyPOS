var items = {};
var token = $('input[name="csrfmiddlewaretoken"]').attr("value");
var total = 0;
$(document).ready(function () {
  $("#bar").focus();
  var listc = 0;
  // $(document).on('keypress',function(e){
  //     alert(e.which);
  // })
  $(document).on("keypress", function (e) {
    if (e.which == 113) {
      var pageURL = $(location).attr("href");
      var window1 = window.open(pageURL);
      window1.focus();
    }
  });
  shortcut.add("F2", function () {
    Submit();
    $("#bar").focus();
  });
  $(document).on("click", function (e) {
    $("#bar").focus();
  });
  $("#omak").click(function () {
    var username = "response_msg";
  });
  $("#sub-btn").click(function () {
    Submit();
    $("#bar").focus();
  });

  $("#newsell-btn").click(function () {
    var pageURL = $(location).attr("href");
    var window1 = window.open(pageURL);
    window1.focus();
  });
  $(document).on("click", "#ll", function () {
    var barl = $(this).val();
    Ndecrease(barl.toString());
  });
  $(document).on("click", "#lm", function () {
    var barm = $(this).val();
    Nincrease(barm.toString());
  });
  $("#bar").on("keypress", function (e) {
    if (e.which == 13) {
      var bar = $(this).val();
      $(this).val("");
      adddata(bar.toString());
    }
  });

  // $('#bar').focus();
});

function adddata(barl) {
  $.ajax({
    url: "ajax/get_item/",
    data: {
      bar: barl,
    },
    dataType: "json",
    success: function (data) {
      if (data.bar != "0") {
        if (Object.keys(items).includes(data.bar)) {
          Nincrease(data.bar);
        } else {
          items[data.bar] = {
            name: data.name,
            bar: data.bar,
            price: data.price,
            Ni: 1,
          };
          total = total + items[data.bar].price;
          $("#total").text(total.toFixed(2));
          $("#list  > tbody").append(
            '<tr  id = "t' +
              data.bar +
              '"><td>' +
              items[data.bar].name +
              "</td><td>" +
              items[data.bar].bar +
              '</td><td  id = "l' +
              data.bar +
              '"><button class="button1" value=' +
              data.bar +
              ' type="button" id = "ll">Less</button>1<button class="button1" value=' +
              data.bar +
              ' type="button" id = "lm">More</button></td><td>' +
              items[data.bar].price +
              '</td><td id = "lt' +
              data.bar +
              '">' +
              items[data.bar].price +
              "</td></tr>"
          );
        }
      }
    },
  });
}

function Nincrease(barm) {
  items[barm].Ni = items[barm].Ni + 1;
  total = total + items[barm].price;
  $("#total").text(total.toFixed(2));
  $("#l" + items[barm].bar).html(
    '<button class="button1" value=' +
      barm +
      ' type="button" id = "ll">Less</button>' +
      items[barm].Ni +
      '<button class="button1" value=' +
      barm +
      ' type="button" id = "lm">More</button>'
  );
}

function Ndecrease(barl) {
  if (items[barl].Ni < 2) {
    if (items[barl].Ni == 1) {
      total = total - items[barl].price;
      $("#total").text(total.toFixed(2));
    }
    $("#t" + items[barl].bar).remove();
    delete items[barl];
  } else {
    items[barl].Ni = items[barl].Ni - 1;
    total = total - items[barl].price;
    $("#total").text(total.toFixed(2));
    $("#l" + items[barl].bar).html(
      '<button class="button1" value=' +
        barl +
        ' type="button" id = "ll">Less</button>' +
        items[barl].Ni +
        '<button class="button1" value=' +
        barl +
        ' type="button" id = "lm">More</button>'
    );
  }
}

function Submit() {
  if (Object.keys(items).length > 0) {
    $.ajax({
      url: "ajax/submit_receipt/",
      type: "POST",
      data: {
        itemsl: JSON.stringify(items),
      },

      headers: { "X-CSRFToken": token },
      dataType: "json",
      success: function (data) {
        if (data.success == 1) {
          $("#result").text("Success");
        } else {
          $("#result").text("Fail");
        }
      },
      // contentType: "application/json; charset=UTF-8",
    });
    items = {};
    $("#list  > tbody").html("");
    $("#total").text("");
    total = 0;
    $("#total").text(total.toFixed(2));
  }
}

function fillrow(bar, name, Ni, price){
  if(Object.keys(items).includes(bar)){
    $("#t" + bar).html(
    '<tr  id = "t' +
    bar +
    '"><td>' +
    iname +
    "</td><td>" +
    bar +
    '</td><td><button class="button1" value=' +
    bar +
    ' type="button" id = "ll">Less</button>' + Ni +  '<button class="button1" value=' +
    bar +
    ' type="button" id = "lm">More</button></td><td>' +
    price +
    '</td><td id = "lt' +
    bar +
    '">' +
    price * Ni +
    "</td></tr>")
  }else{

  }
}
