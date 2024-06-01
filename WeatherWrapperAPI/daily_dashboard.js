document.addEventListener('DOMContentLoaded', function () {
    fetchData();
});

function fetchData() {
    // Fetch data from an API endpoint
    fetch('http://127.0.0.1:8000/api/daily/daily_dashboard')
    .then(response => response.json())
    .then(data => setupCharts(data));
}

function setupCharts(data) {
    const ctxTemp = document.getElementById('tempChart').getContext('2d');
    const tempChart = new Chart(ctxTemp, {
        type: 'line',
        data: {
            labels: data.map(day => day.datetime),
            datasets: [{
                label: 'Max Temp',
                data: data.map(day => day.tempmax),
                fill: false,
                borderColor: 'red',
                tension: 0.1
            }, {
                label: 'Min Temp',
                data: data.map(day => day.tempmin),
                fill: false,
                borderColor: 'blue',
                tension: 0.1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });

    // Setup other charts like humidity, etc.
}