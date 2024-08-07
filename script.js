document.addEventListener('DOMContentLoaded', function() {
    var uptimeCtx = document.getElementById('uptimeChart').getContext('2d');
    var responseTimeCtx = document.getElementById('responseTimeChart').getContext('2d');

    var uptimeLabels = uptimeData.map(data => data.date);
    var uptimeColors = uptimeData.map(data => data.color);

    var uptimeChart = new Chart(uptimeCtx, {
        type: 'bar',
        data: {
            labels: uptimeLabels,
            datasets: [{
                label: 'Uptime',
                data: uptimeLabels.map(() => 1),
                backgroundColor: uptimeColors,
                borderWidth: 1,
                fill: false
            }]
        },
        options: {
            scales: {
                x: { type: 'time', time: { unit: 'day' } },
                y: { beginAtZero: true, display: false }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });

    var responseTimeChart = new Chart(responseTimeCtx, {
        type: 'line',
        data: {
            labels: graphData.timestamps,
            datasets: [{
                label: 'Response Time (ms)',
                data: graphData.response_times,
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                fill: true
            }]
        },
        options: {
            scales: {
                x: { type: 'time', time: { unit: 'day' }, title: { display: true, text: 'Date' } },
                y: { beginAtZero: true, title: { display: true, text: 'Response Time (ms)' } }
            }
        }
    });
});
