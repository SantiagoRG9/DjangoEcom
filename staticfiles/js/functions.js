var vents = {
    items : {
        cli: '',
        date_joined: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        products: []
    },
    list: function () {
        $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.products,
            columns: [
                {"data" : "id"},
                {"data" : "name"},
                {"data" : "cat.name"},
                {"data" : "pvp"},
                {"data" : "cant"},
                {"data" : "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat><i class="fas fa-trash-alt"></i></a>';
                        
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2)
                        
                    }
                },
            ]
        })
    }
};

$(document).ready( function () {
    $('#myTable').DataTable({
        responsive: true,
        autoWidth: false
    });
});

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

   
    $('#datetimepicker1').datetimepicker();

    $("input[name='iva']").TouchSpin({
        min: 0,
        max: 100,
        step: 0.1,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    });

    $('input[name="search"]').autocomplete({
        source: function (request, response){
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action' : 'search_products',
                    'term' : request.term
                },
                dataType: 'json',
            }).done(function(data){
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown){

            })
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            console.clear()
            ui.item.cant = 1;
            ui.item.subtotal = 0.00;
            vents.items.products.push(ui.item);
            console.log(vents.items);
            $(this).val('');
        }
    });
})

