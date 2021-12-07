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
    $('#sub-btn').click(function() {
        alert($('#date').val());
        $.ajax({
            url: "ajax/getsales/",
            type: "POST",
            data: {
                date: $('#date').val(),
                date1: $('#date1').val(),
            },
            headers: { "X-CSRFToken": token },
            dataType: "json",
            success: function(data) {
                $('#total').text(data.date)
            }
        });
    });
});