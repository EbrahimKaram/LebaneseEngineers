var data_global = [];
$(document).ready(function () {



    d3.csv("all_engineers.csv", function (data) {

        data_global = data;
        columns = d3.keys(data[0]);
        $('#example').DataTable({
            data: d3.values(data),
            deferRender: true,
            scrollY: 200,
            scrollCollapse: true,
            scroller: true
        });
        return data;
    });



});
//https://stackoverflow.com/questions/29256675/integrate-datatables-plugin-with-the-help-of-d3-js


//d3.keys(data[0])
