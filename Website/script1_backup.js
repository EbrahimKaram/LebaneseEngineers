var tabulate = function (data, columns) {
    var table = d3.select('body').append('table').attr("id", "example").attr("class", "display nowrap")
    var thead = table.append('thead')
    var tbody = table.append('tbody')

    thead.append('tr')
        .selectAll('th')
        .data(columns)
        .enter()
        .append('th')
        .text(function (d) {
            return d
        })

    var rows = tbody.selectAll('tr')
        .data(data)
        .enter()
        .append('tr')

    var cells = rows.selectAll('td')
        .data(function (row) {
            return columns.map(function (column) {
                return {
                    column: column,
                    value: row[column]
                }
            })
        })
        .enter()
        .append('td')
        .text(function (d) {
            return d.value
        })

    return table;
}

function hideLoader() {
    $('#loading').hide();
}

$(window).ready(hideLoader);

// Strongly recommended: Hide loader after 20 seconds, even if the page hasn't finished loading
setTimeout(hideLoader, 60 * 1000);

d3.csv("All_engineers_reduced.csv", function (data) {
    var columns = d3.keys(data[0]);
    tabulate(data, columns);
    $('#example').DataTable({
        "processing": true,
        language: {
            processing: "<img src='https://media1.giphy.com/media/feN0YJbVs0fwA/giphy.gif'>"
        }
    });
})
