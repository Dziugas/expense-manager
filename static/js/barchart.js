google.charts.load('current', {packages: ['corechart', 'bar']});
google.charts.setOnLoadCallback(drawBasic);

  function drawBasic() {
  var chart_data_2 = JSON.parse(document.getElementById('bar_chart_data').textContent);
  var data = google.visualization.arrayToDataTable(chart_data_2);

  var options = {
    title: 'Expenditure on different dates',
    chartArea: {width: '75%'},
    hAxis: {
      title: 'EUR',
      minValue: 0
    },
    vAxis: {
      title: 'Days'
    }
  };

  var chart = new google.visualization.BarChart(document.getElementById('bar_chart_id'));
  chart.draw(data, options);
}