import config from '../../../shared/config/config.js';

let password = '';
const MAX_LENGTH = 6;

function updateDots() {
    for (let i = 1; i <= MAX_LENGTH; i++) {
        const dot = document.getElementById(`dot-${i}`);
        if (dot) {
            dot.classList.toggle('filled', i <= password.length);
        }
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

export async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!username || !password) {
        const errorMsg = document.getElementById('error-message');
        errorMsg.textContent = 'Por favor ingrese usuario y contraseña';
        errorMsg.style.display = 'block';
        return;
    }

    try {
        const response = await fetch(`${config.API_URL}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                usuario: username,
                contraseña: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Error en el inicio de sesión');
        }

        // Guardar el token
        localStorage.setItem('token', data.access_token);

        // Guardar el rol como 'personal' por defecto
        localStorage.setItem('role', 'personal');

        if (data.user) {
            localStorage.setItem('user', JSON.stringify({
                ...data.user,
                rol: 'personal'
            }));
        }

        // Redirigir al menú principal
        window.location.href = '../pages/menu.html';
    } catch (error) {
        console.error('Error en login:', error);
        const errorMsg = document.getElementById('error-message');
        errorMsg.textContent = error.message || 'Usuario o contraseña incorrectos';
        errorMsg.style.display = 'block';
    }
}

// Exportar las funciones para uso global
window.agregarDigito = agregarDigito;
window.eliminarDigito = eliminarDigito;
window.limpiarDigitos = limpiarDigitos;

