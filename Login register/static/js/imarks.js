document.addEventListener("DOMContentLoaded", () => {
  const semesterBoxes = document.querySelector('.semester-container');
  const semesterBlocks = document.querySelectorAll('.semester-block');

  // Hide all semester tables initially
  semesterBlocks.forEach(div => div.style.display = 'none');

  // Show semester boxes container on page load (should be visible by default anyway)
  semesterBoxes.style.display = 'flex';

  // Attach click event to each semester box
  semesterBoxes.querySelectorAll('.semester-box').forEach(box => {
    box.addEventListener('click', () => {
      const sem = box.getAttribute('data-sem');

      // Hide semester boxes container
      semesterBoxes.style.display = 'none';

      // Hide all semester blocks
      semesterBlocks.forEach(div => div.style.display = 'none');

      // Show selected semester block
      const selectedBlock = document.getElementById('block-' + sem);
      if (selectedBlock) {
        selectedBlock.style.display = 'block';

        // Render chart if not already rendered
        if (!selectedBlock.classList.contains('chart-rendered')) {
          renderChart(sem);
          selectedBlock.classList.add('chart-rendered');
        }
      }
    });
  });

  // Chart render function (as you already have)
  function renderChart(sem) {
    const ctx = document.getElementById('marksPieChart' + sem);
    if (!ctx) return;
    const data = chartData[sem];  // chartData comes from Django template

    new Chart(ctx, {
      type: 'pie',
      data: {
        labels: data.labels,
        datasets: [{
          data: data.data,
          backgroundColor: data.colors
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: true,
            position: 'bottom'
          }
        }
      }
    });
  }
});
