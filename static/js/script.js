// script.js

// Assuming ratings is defined in the template

if (typeof ratings !== 'undefined') {
    // Feedback Distribution Chart
    const feedbackChart = document.getElementById('feedbackChart');
    if (feedbackChart) {
        const ctx = feedbackChart.getContext('2d');
        const ratingCounts = {};
        ratings.forEach(r => {
            ratingCounts[r] = (ratingCounts[r] || 0) + 1;
        });
        const labels = Object.keys(ratingCounts).sort();
        const data = labels.map(l => ratingCounts[l]);
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Number of Feedbacks',
                    data: data,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Bar Chart (perhaps same as above or different)
    const barChart = document.getElementById('barChart');
    if (barChart) {
        const ctx = barChart.getContext('2d');
        // Similar to feedbackChart
        const ratingCounts = {};
        ratings.forEach(r => {
            ratingCounts[r] = (ratingCounts[r] || 0) + 1;
        });
        const labels = Object.keys(ratingCounts).sort();
        const data = labels.map(l => ratingCounts[l]);
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Ratings',
                    data: data,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }]
            }
        });
    }

    // Pie Chart
    const pieChart = document.getElementById('pieChart');
    if (pieChart) {
        const ctx = pieChart.getContext('2d');
        const ratingCounts = {};
        ratings.forEach(r => {
            ratingCounts[r] = (ratingCounts[r] || 0) + 1;
        });
        const labels = Object.keys(ratingCounts).sort();
        const data = labels.map(l => ratingCounts[l]);
        
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 205, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 205, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)'
                    ],
                    borderWidth: 1
                }]
            }
        });
    }
}

// Chatbot
function sendMessage() {
    const input = document.getElementById('chatInput').value;
    const reply = document.getElementById('chatReply');
    if (input.trim() === '') return;
    
    // Simple response, in real app use AI
    reply.innerText = 'This is a placeholder response. Integrate with AI API.';
}