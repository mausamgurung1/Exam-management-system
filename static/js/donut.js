window.onload = function () {
  fetch('/dashboard/', {
    headers: {
      'X-Requested-With': 'XMLHttpRequest'  // ensures Django returns JSON
    }
  })
  .then(response => response.json())
  .then(json => {
    if (!json.data) return;

    const subjectColors = {
      "Engineering Economics": "#4CAF50",
      "Algorithm Analysis and Design": "#2196F3",
      "Numerical Method": "#FF9800",
      "Research Methodology": "#9C27B0",
      "Computer Architecture and Design": "#F44336",
      "Operating System": "#3F51B5",
    };

    const pyramid = document.getElementById("chart-pyramid");
    pyramid.innerHTML = '';  // Clear any existing charts

    Object.entries(json.data).forEach(([subject, percentage], index) => {
      const chartWrapper = document.createElement("div");
      chartWrapper.className = "donut-chart";

      const canvas = document.createElement("canvas");
      canvas.id = `donut-${index}`;
      canvas.width = 140;
      canvas.height = 140;

      const label = document.createElement("div");
      label.className = "label";
      label.innerText = `${percentage}%`;

      const subjectName = document.createElement("p");
      subjectName.className = "subject-name";
      subjectName.innerText = subject;

      chartWrapper.appendChild(canvas);
      chartWrapper.appendChild(label);
      chartWrapper.appendChild(subjectName);
      pyramid.appendChild(chartWrapper);

      createDonutChart(`donut-${index}`, percentage, subjectColors[subject]);
    });
  });
};

// Chart.js function
function createDonutChart(id, presentPercent, subjectColor) {
  new Chart(document.getElementById(id), {
    type: 'doughnut',
    data: {
      labels: ['Present', 'Absent'],
      datasets: [{
        data: [presentPercent, 100 - presentPercent],
        backgroundColor: [subjectColor, '#e0e0e0'],
        borderWidth: 0
      }]
    },
    options: {
      cutout: '70%',
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: function(context) {
              return `${context.label}: ${context.raw}%`;
            }
          }
        }
      }
    }
  });
}
