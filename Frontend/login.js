document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData();
  formData.append("email", document.getElementById("email").value);
  formData.append("password", document.getElementById("password").value);

  const res = await fetch("http://127.0.0.1:8000/login", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();
  if (res.ok) {
    alert("Login successful!");
    window.location.href = "index.html";
  } else {
    alert(data.error);
  }
});
