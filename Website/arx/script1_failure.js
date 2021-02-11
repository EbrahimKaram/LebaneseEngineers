function hideLoader() {
    $('#loading').hide();
}

// Strongly recommended: Hide loader after 20 seconds, even if the page hasn't finished loading
setTimeout(hideLoader, 80 * 1000);

var tabulate = function (columns) {
    var table = d3.select('body').select('table');
    var thead = table.append('thead');
    var tfoot = table.append('tfoot');

    thead.append('tr')
        .selectAll('th')
        .data(columns)
        .enter()
        .append('th')
        .text(function (d) {
            return d
        });

    tfoot.append('tr')
        .selectAll('th')
        .data(columns)
        .enter()
        .append('th')
        .text(function (d) {
            return d
        });

    return table;
}



d3.csv("All_engineers_reduced.csv", function (data) {
    var columns = d3.keys(data[0]);
    tabulate(columns);
    $('#example').DataTable({
        data: data,
        columns: [
            {
                "data": "Engineer_ID"
            },
            {
                "data": "Arabic_Names"
            },
            {
                "data": "Latin_Names"
            },
            {
                "data": "Field_ID"
            },
            {
                "data": "SubField_ID"
            },
            {
                "data": "Field"
            },
            {
                "data": "SubField"
            }

        ],
        processing: true,
        language: {
            processing: "<img src='https://media1.giphy.com/media/feN0YJbVs0fwA/giphy.gif'>"
        },
        initComplete: function () {
            this.api().columns().every(function () {
                var column = this;
                var select = $('<select><option value=""></option></select>')
                    .appendTo($(column.footer()).empty())
                    .on('change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );

                        column
                            .search(val ? '^' + val + '$' : '', true, false)
                            .draw();
                    });

                column.data().unique().sort().each(function (d, j) {
                    select.append('<option value="' + d + '">' + d + '</option>')
                });
            });
        }
    });
    hideLoader();
})
