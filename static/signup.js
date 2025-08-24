document.getElementById("signup-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData();
  formData.append("name", document.getElementById("name").value);
  formData.append("email", document.getElementById("email").value);
  formData.append("password", document.getElementById("password").value);

  const res = await fetch("http://127.0.0.1:8000/signup", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();
  if (res.ok) {
    alert("Account created! Please log in.");
    window.location.href = "login.html";
  } else {
    alert(data.error);
  }
});
