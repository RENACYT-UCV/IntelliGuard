document.addEventListener("DOMContentLoaded", function() {
    // Obtener datos del usuario desde localStorage
    const user = JSON.parse(localStorage.getItem('user'));
    const usernameSpan = document.querySelector('.username');
    const rolSpan = document.querySelector('.rol');

    if (user && user.codigo) {
        usernameSpan.textContent = "Estudiante código: " + user.codigo;
        rolSpan.textContent = "Rol: Estudiante";
    } else {
        usernameSpan.textContent = "No autenticado";
        rolSpan.textContent = "";
    }

    // Función para cerrar sesión
    window.logout = function() {
        localStorage.removeItem('user');
        window.location.href = '../index.html';
    };
});
