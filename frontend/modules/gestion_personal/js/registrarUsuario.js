import { API_CONFIG, fetchApi } from '../../../js/config.js';

document.addEventListener('DOMContentLoaded', function () {
    validarSesionAdmin();

    const form = document.getElementById('registerForm');
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        registrarUsuario();
    });
});

function validarSesionAdmin() {
    const role = localStorage.getItem('role');
    if (role !== 'admin') {
        window.location.href = '../../login_administrador/pages/index.html';
        return;
    }
}

async function registrarUsuario() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const rol = document.getElementById('rol').value;

    if (!validarDatos(username, password, rol)) {
        return;
    }

    const usuarioData = {
        usuario: username,
        contraseña: password,
        idRol: rol
    };

    try {
        await fetchApi(API_CONFIG.ENDPOINTS.AUTH.REGISTRO, {
            method: 'POST',
            body: JSON.stringify(usuarioData)
        });

        mostrarMensajeExito('Usuario registrado exitosamente');
        document.getElementById('registerForm').reset();
        setTimeout(() => {
            window.location.href = 'gestionarUsuario.html';
        }, 2000);
    } catch (error) {
        console.error('Error al registrar el usuario:', error);
        mostrarMensajeError('Error al registrar el usuario');
    }
}

function validarDatos(username, password, rol) {
    if (!username || username.length < 3) {
        mostrarMensajeError('El nombre de usuario debe tener al menos 3 caracteres');
        return false;
    }

    if (!password || password.length < 6) {
        mostrarMensajeError('La contraseña debe tener al menos 6 caracteres');
        return false;
    }

    if (!rol) {
        mostrarMensajeError('Debe seleccionar un rol');
        return false;
    }

    return true;
}

function mostrarMensajeError(mensaje) {
    const messageDiv = document.getElementById('message');
    messageDiv.innerHTML = `<div class="alert alert-danger alert-dismissible fade show">
        ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>`;
}

function mostrarMensajeExito(mensaje) {
    const messageDiv = document.getElementById('message');
    messageDiv.innerHTML = `<div class="alert alert-success alert-dismissible fade show">
        ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>`;
}

// Funciones del teclado numérico
function agregarDigito(digit) {
    const password = document.getElementById('password');
    if (password.value.length < 6) {
        password.value += digit;
    }
}

function eliminarDigito() {
    const password = document.getElementById('password');
    password.value = password.value.slice(0, -1);
}

function limpiarDigitos() {
    const password = document.getElementById('password');
    password.value = '';
}
