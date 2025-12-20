// =================== AUTH LOGIC ===================

// Chuyển đổi form
function toggleForm(formType) {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    if (formType === 'register') {
        loginForm.classList.add('hidden-form');
        registerForm.classList.remove('hidden-form');
    } else {
        registerForm.classList.add('hidden-form');
        loginForm.classList.remove('hidden-form');
    }
}

// Ẩn / hiện mật khẩu
function togglePasswordVisibility(inputId, btn) {
    const input = document.getElementById(inputId);
    const icon = btn.querySelector('i');

    if (input.type === "password") {
        input.type = "text";
        icon.classList.replace('ri-eye-off-line', 'ri-eye-line');
    } else {
        input.type = "password";
        icon.classList.replace('ri-eye-line', 'ri-eye-off-line');
    }
}

// Điền nhanh tài khoản demo
function fillLogin(user, pass) {
    document.getElementById('username').value = user;
    document.getElementById('password').value = pass;
}

// Toast
function showToast(message) {
    const toast = document.getElementById('toast');
    const msg = document.getElementById('toast-message');
    msg.innerText = message;
    toast.classList.remove('hidden');
    setTimeout(() => toast.classList.add('hidden'), 3000);
}

// Đăng ký
function handleRegister(e) {
    e.preventDefault();

    const user = {
        username: document.getElementById('reg-email').value,
        password: document.getElementById('reg-password').value,
        name:
            document.getElementById('reg-lastname').value +
            " " +
            document.getElementById('reg-firstname').value,
        role: document.querySelector('input[name="reg-role"]:checked').value
    };

    localStorage.setItem('registeredUser', JSON.stringify(user));
    showToast("Đăng ký thành công!");
    toggleForm('login');
}

// Đăng nhập
function handleLogin(e) {
    e.preventDefault();

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();

    const demoTeacher = { user: "Kim Vũ", pass: "123456", role: "teacher" };
    const demoStudent = { user: "Nguyễn Văn A", pass: "233484", role: "student" };
    const regUser = JSON.parse(localStorage.getItem('registeredUser'));

    let user = null;

    if (username === demoTeacher.user && password === demoTeacher.pass)
→        user = demoTeacher;
    else if (username === demoStudent.user && password === demoStudent.pass)
        user = demoStudent;
    else if (regUser && username === regUser.username && password === regUser.password)
        user = regUser;

    if (!user) {
        showToast("Sai tài khoản hoặc mật khẩu!");
        return;
    }

    localStorage.setItem('currentUser', JSON.stringify(user));
    window.location.href =
        user.role === "teacher" ? "dashboardGV.html" : "dashboardSV.html";
}
