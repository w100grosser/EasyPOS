var items = {};
var token = $('input[name="csrfmiddlewaretoken"]').attr("value");
var total = 0;
$(document).ready(function() {
    var pageURL = $(location).attr("href");
    $("#bar").focus();
    var listc = 0;
    // $(document).on('keypress',function(e){
    //     alert(e.which);
    // })
    $(document).on("keypress", function(e) {
        if (e.which == 113) {
            var pageURL = $(location).attr("href");
            var window1 = window.open(pageURL);
            window1.focus();
        }
    });
    shortcut.add("F2", function() {
        Submit();
        $("#bar").focus();
    });
    $(document).on("click", function(e) {
        if (pageURL.includes('buy')) {} else {
            $("#bar").focus();
        }

    });
    $("#omak").click(function() {
        var username = "response_msg";
    });
    $("#sub-btn").click(function() {
        Submit();
        $("#bar").focus();
    });

    $("#newsell-btn").click(function() {
        var window1 = window.open(pageURL);
        window1.focus();
    });
    $("#newbuy-btn").click(function() {
        BuySubmit();
        $('#bar').focus();
    });
    $(document).on("click", "#ll", function() {
        var barl = $(this).val();
        Ndecrease(barl.toString());
    });
    $(document).on("click", "#lm", function() {
        var barm = $(this).val();
        Nincrease(barm.toString());
    });
    $("#bar").on("keypress", function(e) {
        if (e.which == 13) {
            var bar = $(this).val();
            $(this).val("");
            adddata(bar.toString());
        }
    });
    $("#amount").click(function() {
        $("#amount").focus();
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
        success: function(data) {
            if (data.bar != "0") {
                if (Object.keys(items).includes(data.bar)) {
                    Nincrease(data.bar);
                } else {
                    total = total + data.price;
                    $("#total").text(total.toFixed(2));
                    fillrow(data.bar, data.name, 1, data.price);

                    items[data.bar] = {
                        name: data.name,
                        bar: data.bar,
                        price: data.price,
                        Ni: 1,
                    };
                }
            }
        },
    });
}

function Nincrease(barm) {
    items[barm].Ni = items[barm].Ni + 1;
    total = total + items[barm].price;
    $("#total").text(total.toFixed(2));

    fillrow(items[barm].bar, items[barm].name, items[barm].Ni, items[barm].price);
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
        fillrow(items[barl].bar, items[barl].name, items[barl].Ni, items[barl].price);
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
            success: function(data) {
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

function BuySubmit() {
    if (Object.keys(items).length > 0) {
        amount = $('#amount').val();
        $.ajax({
            url: 'ajax/submit_receipt_buy/',
            type: "POST",
            data: {
                itemsl: JSON.stringify(items),
                amountl: amount
            },

            headers: { 'X-CSRFToken': token },
            dataType: 'json',
            success: function(data) {
                    if (data.success == 1) {
                        $('#result').text('Success');
                    } else {
                        $('#result').text('Fail');
                    }
                }
                // contentType: "application/json; charset=UTF-8",
        });
        items = {};
        $('#list  > tbody').html('');
    }
}

function fillrow(bar, name, Ni, price) {
    if (Object.keys(items).includes(bar)) {
        $("#t" + bar).html(

            '<td>' +
            name +
            "</td><td>" +
            bar +
            '</td><td>' +
            price +
            '</td><td><button class="button1" value=' +
            bar +
            ' type="button" id = "ll">Less</button>' + Ni + '<button class="button1" value=' +
            bar +
            ' type="button" id = "lm">More</button></td><td>' +
            price * Ni +
            "</td></tr>")
    } else {
        $("#list  > tbody").append(
            '<tr  id = "t' +
            bar +
            '"><td>' +
            name +
            "</td><td>" +
            bar +
            '</td><td>' +
            price +
            '</td><td><button class="button1" value=' +
            bar +
            ' type="button" id = "ll">Less</button>' + Ni + '<button class="button1" value=' +
            bar +
            ' type="button" id = "lm">More</button></td><td>' +
            price * Ni +
            "</td></tr>")
    }
}