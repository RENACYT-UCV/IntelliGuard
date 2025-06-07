function validTokenSession() {
    const currentPage = window.location.pathname;
    const publicPages = ['/index.html', '/', '/frontend/index.html', '/frontend/pages/loginEstudiante.html', '/frontend/pages/registrarEstudiante.html'];
    
    if (!publicPages.includes(currentPage)) {
        const jwtCookie = getCookie('jwt');
        const usernameCookie = getCookie('username');
        if (!jwtCookie || !usernameCookie) {
            window.location.href = '/frontend/index.html';
            return false;
        }
    }
    return true;
}

function handleUnauthorized(response) {
    if (response.status === 403 || response.status === 401 || response.status === 422) {
        logout();
    }
}

function logout() {
    document.cookie = 'jwt=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 UTC; Secure; SameSite=Strict';
    document.cookie = 'username=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 UTC; Secure; SameSite=Strict';
    window.location.href = '/frontend/index.html';
}

function saveAuth(token, username) {
    document.cookie = `jwt=${token}; path=/; Secure; SameSite=Strict`;
    document.cookie = `username=${username}; path=/; Secure; SameSite=Strict`; 
}

function getCookie(name) {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1, cookie.length); 
        }
    }
    return null;
}

function menu() {
    window.location.href = '../pages/menu.html';
}

// Agregar validación de sesión al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    validTokenSession();
});
 
  