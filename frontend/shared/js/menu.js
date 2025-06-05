import { SessionManager, ROLES } from '../utils/sessionManager.js';

document.addEventListener("DOMContentLoaded", function () {
    if (!SessionManager.validateSession()) return;

    // Actualizar el contenido del elemento <span> con el nombre de usuario
    document.querySelector('.username').textContent = "Usuario: " + SessionManager.getUsername();
    document.querySelector('.rol').textContent = "Rol: " + SessionManager.getRole();

    // Obtener los contenedores de las tarjetas según el rol del usuario
    const contenedorPersonal = document.querySelector('.content-Personal');
    const contenedorAdministrador = document.querySelector('.content-Administrador');

    // Función para mostrar u ocultar los contenedores según el rol del usuario
    function mostrarContenedorSegunRol() {
        if (SessionManager.isPersonal()) {
            contenedorPersonal.style.display = 'block';
            contenedorAdministrador.style.display = 'none';
        } else if (SessionManager.isAdmin()) {
            contenedorPersonal.style.display = 'none';
            contenedorAdministrador.style.display = 'block';
        }
    }

    // Llamar a la función para mostrar u ocultar los contenedores al cargar la página
    mostrarContenedorSegunRol();
}); 