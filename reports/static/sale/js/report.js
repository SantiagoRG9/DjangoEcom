function generate_report() {
    var parameters = {
        'action': 'search_report',
        'start_date': '2022-01-19',
        'end_date': '2022-01-19',
    };

    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url : window.location.pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ""
        },
        // columns: [
        //     {"data" : "id"},
        //     {"data" : "name"},
        //     {"data" : "cat.name"},
        //     {"data" : "pvp"},
        //     {"data" : "cant"},
        //     {"data" : "subtotal"},
        // ],
        columnDefs: [
            {
                targets: [-1,-2,-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                    
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

$(function name(params) {
    $('input[name="date_ranger"]').daterangepicker();

    generate_report();
})