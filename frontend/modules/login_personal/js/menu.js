import config from '../../../shared/config/config.js';

document.addEventListener('DOMContentLoaded', function () {
    // Cargar información del usuario
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const username = document.querySelector('.username');
    const rol = document.querySelector('.rol');

    if (username) {
        username.textContent = user.usuario || 'Usuario';
    }
    if (rol) {
        rol.textContent = user.rol || 'Personal';
    }
});

// Función de logout
window.logout = function () {
    // Limpiar el almacenamiento local
    localStorage.removeItem('token');
    localStorage.removeItem('user');

    // Redirigir al login
    window.location.href = '../pages/index.html';
}; 