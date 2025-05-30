function login() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
        fetch(API_URL + '/login/administrador', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ usuario: username, contraseña: password })
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Error al iniciar sesión. Por favor, verifica tus credenciales.');
            }
        })
        .then(data => {
            saveAuth(data.access_token, username);
            window.location.href = 'pages/menu.html';
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

