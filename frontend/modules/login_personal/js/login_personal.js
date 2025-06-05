import { API_CONFIG, fetchApi } from '../../../js/config.js';

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const usuario = document.getElementById('usuario').value;
        const contraseña = document.getElementById('contraseña').value;

        try {
            const response = await fetchApi(API_CONFIG.ENDPOINTS.LOGIN_PERSONAL, {
                method: 'POST',
                body: JSON.stringify({
                    usuario,
                    contraseña
                })
            });

            // Guardar el token y el rol
            localStorage.setItem('token', response.access_token);

            // Redirigir según el rol del personal
            window.location.href = '../registro_pertencias/pages/index.html';
        } catch (error) {
            // Mostrar mensaje de error
            const errorDiv = document.getElementById('error-message');
            errorDiv.textContent = 'Error en el inicio de sesión. Por favor, verifica tus credenciales.';
            errorDiv.style.display = 'block';

            // Limpiar el campo de contraseña
            document.getElementById('contraseña').value = '';
        }
    });

    // Agregar botón para ir al login de administrador
    const adminLoginBtn = document.getElementById('adminLoginBtn');
    if (adminLoginBtn) {
        adminLoginBtn.addEventListener('click', () => {
            window.location.href = '../login_administrador/pages/index.html';
        });
    }
}); 