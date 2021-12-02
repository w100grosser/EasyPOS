$(document).ready(function () {
    var token = $('input[name="csrfmiddlewaretoken"]').attr('value');

    $('#bar').focus();
    var items = {};
    var listc = 0;
    // $(document).on('keypress',function(e){
    //     alert(e.which);
    // })
    $(document).on('keypress', function (e) {
        if (e.which == 93) {
            if (Object.keys(items).length > 0) {
                $.ajax({
                    url: 'ajax/submit_receipt/',
                    type: "POST",
                    data: {
                        itemsl: JSON.stringify(items)
                    },

                    headers: { 'X-CSRFToken': token },
                    dataType: 'json',
                    // contentType: "application/json; charset=UTF-8",
                });
            }
        }
    })
    $("#omak").click(function () {
        var username = "response_msg";
    });
    $(document).on('click', '#ll', function () {
        var name = $(this).val();
        items[name].Ni = items[name].Ni - 1;
        $('#l' + items[name].bar).html('<button class="button1" value=' + name + ' type="button" id = "ll">Less</button>' + items[name].Ni + '<button class="button1" value=' + name + ' type="button" id = "lm">More</button>');
    });
    $(document).on('click', '#lm', function () {
        var name = $(this).val();
        items[name].Ni = items[name].Ni + 1;
        $('#l' + items[name].bar).html('<button class="button1" value=' + name + ' type="button" id = "ll">Less</button>' + items[name].Ni + '<button class="button1" value=' + name + ' type="button" id = "lm">More</button>');
    });
    $("#bar").on('keypress', function (e) {
        if (e.which == 13) {
            var bar = $(this).val();
            $(this).val('');
            $.ajax({
                url: 'ajax/get_item/',
                data: {
                    'bar': bar
                },
                dataType: 'json',
                success: function (data) {
                    var in1 = 1;
                    for (var key of Object.keys(items)) {
                        if (key == data.name) {

                            items[data.name].Ni = items[data.name].Ni + 1;
                            $('#l' + bar).html('<button class="button1" value=' + data.name + ' type="button" id = "ll">Less</button>' + items[data.name].Ni + '<button class="button1" value=' + data.name + ' type="button" id = "lm">More</button>');
                            in1 = 0;
                            break;
                        }
                    } if (in1 == 1) {

                        items[data.name] = { name: data.name, bar: bar, price: data.price, Ni: 1 };
                        $("#list  > tbody").append('<tr><td>' + items[data.name].name + '</td><td>' + items[data.name].bar + '</td><td  id = "l' + bar + '"><button class="button1" value=' + data.name + ' type="button" id = "ll">Less</button>1<button class="button1" value=' + data.name + ' type="button" id = "lm">More</button></td><td>' + items[data.name].price + '</td></tr>');

                    }
                }
            });
        }
    });

    // $('#bar').focus();

});