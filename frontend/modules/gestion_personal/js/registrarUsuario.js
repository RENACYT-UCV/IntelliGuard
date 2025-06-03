document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registerForm');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        registrarUsuario();
    });
});

function registrarUsuario() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const rol = document.getElementById('rol').value;
    const jwtToken = getCookie('jwt');
    const apiUrl = API_URL + '/registro';


    const usuarioData = {
        usuario: username,
        contraseña: password,
        idRol: rol
    };
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + jwtToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(usuarioData)
    })
    .then(response => {
        handleUnauthorized(response);
        if (!response.ok) {
            throw new Error('Error en la solicitud: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        console.log('Respuesta del servidor:', data);
        document.getElementById('message').innerHTML = '<div class="alert alert-success">Usuario registrado exitosamente</div>';
        document.getElementById('registerForm').reset();
    })
    .catch(error => {
        console.error('Error al registrar el usuario:', error);
        document.getElementById('message').innerHTML = '<div class="alert alert-danger">Error al registrar el usuario</div>';
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
