const API_URL = 'http://localhost:3000'; // ejemplo

// Lógica de login
function login() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  fetch(API_URL + '/login/administrador', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ usuario: username, contraseña: password })
  })
    .then(response => {
      if (response.ok) return response.json();
      else throw new Error('Credenciales inválidas');
    })
    .then(data => {
      saveAuth(data.access_token, username);
      window.location.href = 'pages/menu.html';
    })
    .catch(error => {
      document.getElementById('error-message').style.display = 'block';
    });
}

function agregarDigito(digit) {
  const passwordField = document.getElementById('password');

  if (passwordField.value.length < 6) {
    passwordField.value += digit;
    actualizarIndicadores(passwordField.value.length);
  }
}

function eliminarDigito() {
  const passwordField = document.getElementById('password');
  passwordField.value = passwordField.value.slice(0, -1);
  actualizarIndicadores(passwordField.value.length);
}

function limpiarDigitos() {
  const passwordField = document.getElementById('password');
  passwordField.value = '';
  actualizarIndicadores(0);
}

function actualizarIndicadores(longitud) {
  for (let i = 1; i <= 6; i++) {
    const dot = document.getElementById(`dot-${i}`);
    if (i <= longitud) {
      dot.classList.add('active');
    } else {
      dot.classList.remove('active');
    }
  }
}

function validTokenSession() {
  const currentPage = window.location.pathname;
  if (currentPage !== '/index.html' && currentPage !== '/') {
    const jwtCookie = getCookie('jwt');
    const usernameCookie = getCookie('username');
    if (!jwtCookie || !usernameCookie) {
      logout();
    }
  }
}

function handleUnauthorized(response) {
  if ([401, 403, 422].includes(response.status)) {
    logout();
  }
}

function logout() {
  document.cookie = 'jwt=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 UTC; Secure; SameSite=Strict';
  document.cookie = 'username=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 UTC; Secure; SameSite=Strict';
  window.location.href = '../index.html';
}

function saveAuth(token, username) {
  document.cookie = `jwt=${token}; Path=/; Secure; SameSite=Strict`;
  document.cookie = `username=${username}; Path=/; Secure; SameSite=Strict`;
}

function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith(name + '=')) {
      return cookie.substring(name.length + 1);
    }
  }
  return null;
}

function menu() {
  window.location.href = '../pages/menu.html';
}

// ✅ AQUÍ VAN LAS ASIGNACIONES AL FINAL
window.agregarDigito = agregarDigito;
window.eliminarDigito = eliminarDigito;
window.limpiarDigitos = limpiarDigitos;
window.login = login;
