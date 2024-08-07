document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById("timeline");
    const ctx = canvas.getContext("2d");

    const stripeWidth = 8;
    const spacing = 1;
    
    // Fetch uptime data
    fetch('data.json')
        .then(response => response.json())
        .then(data => {
            const uptimeData = data.map(entry => {
                return {
                    color: entry.status ? "green" : "red",
                    width: stripeWidth
                };
            });

            // Draw the uptime data on the canvas
            uptimeData.forEach((data, i) => {
                ctx.fillStyle = data.color;
                const start = i * (stripeWidth + spacing);
                ctx.fillRect(start, 0, data.width, 40);
            });
        });

    const overlay = document.getElementById("overlay");
    overlay.addEventListener("mousemove", (event) => {
        console.log(event.offsetX);
    });

    var responseTimeCtx = document.getElementById('responseTimeChart').getContext('2d');

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
