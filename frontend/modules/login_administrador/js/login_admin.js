import { API_CONFIG } from '../../../js/config.js';

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const errorMessage = document.getElementById('error-message');

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const usuario = document.getElementById('usuario').value;
        const contraseña = document.getElementById('contraseña').value;

        try {
            const response = await fetch(API_CONFIG.BASE_URL + '/admin/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ usuario, contraseña })
            });

            if (!response.ok) {
                throw new Error('Credenciales inválidas');
            }

            const data = await response.json();

            localStorage.setItem('token', data.token);
            localStorage.setItem('role', 'admin');

            window.location.href = '/modules/dashboard/index.html';
        } catch (error) {
            errorMessage.textContent = 'Usuario o contraseña incorrectos';
            errorMessage.style.display = 'block';

            document.getElementById('contraseña').value = '';
        }
    });
}); 