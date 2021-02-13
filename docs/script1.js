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



    $('#example tfoot th').each(function () {
        var title = $(this).text();
        $(this).html('<input type="text" placeholder="Search ' + title + '" />');
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
            },
            {
                "data": "Website",

                "render": function (data, type, full, meta) {
                    return '<a target="_blank" href="https://www.oea.org.lb/Arabic/Memberdetails.aspx?pageid=112&id=' + data + '">Details</a>'
                }

                        }
        ],
        initComplete: function () {
            // Apply the search
            this.api().columns().every(function () {
                var that = this;

                $('input', this.footer()).on('keyup change clear', function () {
                    if (that.search() !== this.value) {
                        that
                            .search(this.value)
                            .draw();
                    }
                });
            });
        },
        processing: true,
        language: {
            processing: "<img src='https://media1.giphy.com/media/feN0YJbVs0fwA/giphy.gif'>"
        }
    });
    hideLoader();
})
