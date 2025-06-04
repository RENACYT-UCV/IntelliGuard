import { API_CONFIG } from '../utils/config.js';
import { saveAuth } from '../utils/sessionManager.js';

let password = '';
const MAX_LENGTH = 6;

function updateDots() {
    for (let i = 1; i <= MAX_LENGTH; i++) {
        const dot = document.getElementById(`dot-${i}`);
        dot.classList.toggle('filled', i <= password.length);
    }
}

function agregarDigito(digito) {
    if (password.length < MAX_LENGTH) {
        password += digito;
        document.getElementById('password').value = password;
        updateDots();

        if (password.length === MAX_LENGTH) {
            document.getElementById('error-message').style.display = 'none';
        }
    }
}

function eliminarDigito() {
    if (password.length > 0) {
        password = password.slice(0, -1);
        document.getElementById('password').value = password;
        updateDots();
    }
}

function limpiarDigitos() {
    password = '';
    document.getElementById('password').value = password;
    updateDots();
}

async function login() {
    const username = document.getElementById('username').value;

    if (!username || password.length !== MAX_LENGTH) {
        document.getElementById('error-message').style.display = 'block';
        return;
    }

    try {
        const response = await fetch(API_CONFIG.AUTH.LOGIN_ADMIN, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                usuario: username,
                contraseña: password
            })
        });

        if (!response.ok) {
            throw new Error('Credenciales inválidas');
        }

        const data = await response.json();
        saveAuth(data.access_token, username);
        window.location.href = '../pages/menu.html';
    } catch (error) {
        document.getElementById('error-message').style.display = 'block';
        limpiarDigitos();
    }
}

// Exportar las funciones para uso global
window.agregarDigito = agregarDigito;
window.eliminarDigito = eliminarDigito;
window.limpiarDigitos = limpiarDigitos;
window.login = login;

