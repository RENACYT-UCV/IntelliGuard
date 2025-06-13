function login() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    fetch(API_URL + '/ia/login/administrador', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ usuario: username, contraseña: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.access_token) {
            saveAuth(data.access_token, username);
            window.location.href = 'dashboardadmin.html';
        } else {
            document.getElementById('error-message').style.display = 'block';
        }
    })
    .catch(error => {
        document.getElementById('error-message').style.display = 'block';
    });
}

function agregarDigito(digit) {
    var password = document.getElementById('password');
    if (password.value.length < 6) {
        password.value += digit;
    }
}

function eliminarDigito() {
    var password = document.getElementById('password');
    password.value = password.value.slice(0, -1);
}

function limpiarDigitos() {
    var password = document.getElementById('password');
    password.value = '';
}

