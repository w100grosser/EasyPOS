var items = {};
var token = $('input[name="csrfmiddlewaretoken"]').attr('value');
var amount = 0;
$(document).ready(function() {
    $('#amount').val('0');
    $('#bar').focus();
    var listc = 0;
    // $(document).on('keypress',function(e){
    //     alert(e.which);
    // })
    $(document).on('keypress', function(e) {
        if (e.which == 93) {
            Submit();
            $('#bar').focus();
        }
    });
    // $(document).on('click', function(e) {
    //     $('#bar').focus();
    // });
    $("#omak").click(function() {
        var username = "response_msg";
    });
    $("#sub-btn").click(function() {
        Submit();
        $('#bar').focus();
    });
    $(document).on('click', '#ll', function() {
        var name = $(this).val();
        Ndecrease(name);
    });
    $(document).on('click', '#lm', function() {
        var name = $(this).val();
        Nincrease(name);
    });
    $("#bar").on('keypress', function(e) {
        if (e.which == 13) {
            var bar = $(this).val();
            $(this).val('');
            adddata(bar)
        }
    });

    // $('#bar').focus();

});

function adddata(bar) {
    $.ajax({
        url: 'ajax/get_item/',
        data: {
            'bar': bar
        },
        dataType: 'json',
        success: function(data) {
            if (data.bar != 0) {

                if (Object.keys(items).includes(data.name)) {
                    Nincrease(data.name);
                } else {
                    items[data.name] = { name: data.name, bar: bar, price: data.price, Ni: 1 };
                    $("#list  > tbody").append('<tr  id = "t' + bar + '"><td>' + items[data.name].name + '</td><td>' + items[data.name].bar + '</td><td  id = "l' + bar + '"><button class="button1" value=' + data.name + ' type="button" id = "ll">Less</button>1<button class="button1" value=' + data.name + ' type="button" id = "lm">More</button></td><td>' + items[data.name].price + '</td></tr>');

                }
            }
        }
    });
}

function Nincrease(name) {
    items[name].Ni = items[name].Ni + 1;
    $('#l' + items[name].bar).html('<button class="button1" value=' + name + ' type="button" id = "ll">Less</button>' + items[name].Ni + '<button class="button1" value=' + name + ' type="button" id = "lm">More</button>');
}

function Ndecrease(name) {
    if (items[name].Ni < 2) {
        $('#t' + items[name].bar).remove();
        delete items[name];
    } else {
        items[name].Ni = items[name].Ni - 1;
        $('#l' + items[name].bar).html('<button class="button1" value=' + name + ' type="button" id = "ll">Less</button>' + items[name].Ni + '<button class="button1" value=' + name + ' type="button" id = "lm">More</button>');
    }
}

function Submit() {
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