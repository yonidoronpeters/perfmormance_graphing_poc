$.getJSON("json/data.json", function(data) {
  var chart = c3.generate({
    data: {
        columns: [
            data.mysql
        ],
        type: 'bar'
    },
    axis: {
          x: {
              type: 'category',
              categories: data.dates
          },
          y:{
              label: 'TPS'
          }
    },
    bar: {
        width: {
            ratio: 0.5 // this makes bar width 50% of length between ticks
        }
        // or
        //width: 100 // this makes bar width 100px
    }
  });

  setTimeout(function () {
    chart.load({
        columns: [
            data.oracle
        ]
    });
  }, 500);

  setTimeout(function () {
    chart.load({
        columns: [
            data.sap
        ]
    });
  }, 1000);

  setTimeout(function () {
    chart.load({
        columns: [
            data.sqlserver
        ]
    });
  }, 1500);

  setTimeout(function () {
    chart.load({
        columns: [
            data.avg
        ],
      type: 'line'
    });
  }, 2000);
});
