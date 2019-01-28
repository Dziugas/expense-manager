google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
var chart_data = JSON.parse(document.getElementById('pie_chart_data').textContent);
var data = google.visualization.arrayToDataTable(chart_data);

var options = {
  title: 'Ependiture by expense type',
  is3D: true,
};

var chart = new google.visualization.PieChart(document.getElementById('piechart'));

chart.draw(data, options);
};