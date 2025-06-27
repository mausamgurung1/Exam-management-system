// register.js
document.getElementById("registrationForm").addEventListener("submit", function(e) {
    const password1 = document.querySelector('input[name="password1"]').value;
    const password2 = document.querySelector('input[name="password2"]').value;
  
    if (password1 !== password2) {
      e.preventDefault();
      alert("Passwords do not match!");
    }
  });
  