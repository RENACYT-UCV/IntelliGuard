export function saveAuth(token, usuario) {
  localStorage.setItem('token', token);
  localStorage.setItem('usuario', usuario);
  localStorage.setItem('role', 'Administrador');
}

export function getToken() {
  return localStorage.getItem('token');
}

export function clearAuth() {
  localStorage.removeItem('token');
  localStorage.removeItem('usuario');
  localStorage.removeItem('role');
}

export function isAuthenticated() {
  return !!getToken();
}

// Redirigir si no está autenticado
export function checkAuth() {
  if (!isAuthenticated()) {
    window.location.href = '/frontend/modules/login_administrador/pages/index.html';
  }
}

function validTokenSession() {
  var currentPage = window.location.pathname;
  if (currentPage !== '/index.html' && currentPage !== '/') {
    var jwtCookie = getCookie('jwt');
    var usernameCookie = getCookie('username');
    if (!jwtCookie || !usernameCookie) {
      logout()
    }
  }
}
function handleUnauthorized(response) {
  if (response.status === 403 || response.status === 401 || response.status === 422) {
    logout();
  }
}
function logout() {
  clearAuth();
  window.location.href = '/frontend/modules/login_administrador/pages/index.html';
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
  window.location.href = '/frontend/modules/login_administrador/pages/menu.html';
}

