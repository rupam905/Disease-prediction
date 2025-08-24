document
  .querySelector(".login-box")
  .addEventListener("submit", async function (e) {
    e.preventDefault(); // Prevent form from submitting normally

    // Check which button was clicked
    const activeElement = document.activeElement;
    if (activeElement.classList.contains("login-btn")) {
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;

      const response = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        window.location.href = "/dashboard"; // Change as needed
      } else {
        alert("Login failed!");
      }
    }
  });
