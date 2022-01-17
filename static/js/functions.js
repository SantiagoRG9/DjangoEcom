function message_error(obj) {
    $.each(obj, function(key, value){
        console.log(key);
        console.log(value);
    });
}

function submit_with_ajax(url, paramaters, callback) {
    $.confirm({
        confirmButton: 'Yes i agree',
        cancelButton: 'NO never !'
    });
    $.ajax({
        url: url, //window.location.pathname
        type: 'POST',
        data: paramaters,
        dataType: 'json',
        processData: false,
        contentType: false,
    }).done(function (data){
        if(!data.hasOwnProperty('error')){
            callback();
            return false;
        }

    message_error(data.error);

    }).fail(function (jqXHR, textStatus, errorThrown){
        alert(textStatus + ': ' + errorThrown);
    })
}

$(document).ready( function () {
   
    $('input[name="action"]').val('add')
    $('#myClientModal').modal('show');
    
})