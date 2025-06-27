window.onload = function () {
  fetch('/dashboard/')
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
    pyramid.innerHTML = '';

    Object.entries(json.data).forEach(([name, percent]) => {
      const wrapper = document.createElement("div");
      wrapper.className = "donut-chart";

      const canvas = document.createElement("canvas");
      canvas.width = 140;
      canvas.height = 140;

      const label = document.createElement("div");
      label.className = "label";
      label.innerText = "0%";

      const subjectName = document.createElement("p");
      subjectName.className = "subject-name";
      subjectName.innerText = name;

      wrapper.appendChild(canvas);
      wrapper.appendChild(label);
      wrapper.appendChild(subjectName);
      pyramid.appendChild(wrapper);

      const ctx = canvas.getContext("2d");
      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      const radius = 55;
      const thickness = 12;
      const endPercent = percent / 100;
      let curPerc = 0;
      let displayedPercent = 0;
      const circ = Math.PI * 2;
      const quart = Math.PI / 2;

      function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, circ);
        ctx.strokeStyle = "#e0e0e0";
        ctx.lineWidth = thickness;
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, -quart, (circ * curPerc) - quart, false);
        ctx.strokeStyle = subjectColors[name];
        ctx.lineWidth = thickness;
        ctx.lineCap = "round";
        ctx.stroke();

        if (displayedPercent < percent) {
          displayedPercent += 1;
          label.innerText = displayedPercent + "%";
        }

        curPerc += 0.01;
        if (curPerc <= endPercent) {
          requestAnimationFrame(animate);
        }
      }

      animate();
    });
  });
};
