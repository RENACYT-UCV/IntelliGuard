import { API_CONFIG, fetchApi } from '../../../js/config.js';

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const errorMessage = document.getElementById('error-message');

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const usuario = document.getElementById('usuario').value;
        const contraseña = document.getElementById('contraseña').value;

        try {
            const response = await fetchApi(API_CONFIG.ENDPOINTS.AUTH.LOGIN_ADMIN, {
                method: 'POST',
                body: JSON.stringify({ usuario, contraseña })
            });

            localStorage.setItem('token', response.access_token);
            localStorage.setItem('role', 'admin');

            window.location.href = '../gestion_personal/pages/index.html';
        } catch (error) {
            errorMessage.textContent = 'Usuario o contraseña incorrectos';
            errorMessage.style.display = 'block';
            document.getElementById('contraseña').value = '';
        }
    });

    // Botón para volver al login de personal
    const personalLoginBtn = document.getElementById('personalLoginBtn');
    if (personalLoginBtn) {
        personalLoginBtn.addEventListener('click', () => {
            window.location.href = '../login_personal/pages/index.html';
        });
    }
}); 