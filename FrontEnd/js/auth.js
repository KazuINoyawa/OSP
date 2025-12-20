async function handleLogin(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    });

    if (!response.ok) {
        alert("Sai tài khoản hoặc mật khẩu");
        return;
    }

    const data = await response.json();

    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user", JSON.stringify(data));

    if (data.role === "teacher") {
        window.location.href = "teacher.html";
    } else {
        window.location.href = "student.html";
    }
}
