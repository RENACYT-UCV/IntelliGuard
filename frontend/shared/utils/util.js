// Función para convertir URI de datos a archivo
function dataURItoFile(dataURI, filename) {
    const binary = atob(dataURI.split(',')[1]);
    const array = Uint8Array.from(binary, byte => byte.charCodeAt(0));
    return new File([array], filename, { type: 'image/jpeg' });
}

function convertirFecha(fechaString) {
    const [fecha, hora] = fechaString.split('_');
    const [año, mes, dia] = fecha.split('-');
    const [horas, minutos, segundos] = hora.split('-');
    return new Date(`${año}-${mes}-${dia}T${horas}:${minutos}:${segundos}`);
}

function parseJwt(token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}

// Función para obtener una cookie por su nombre
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Función para establecer una cookie
function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

// Función para eliminar una cookie
function eraseCookie(name) {
    document.cookie = name + '=; Max-Age=-99999999;';
}

// Función para manejar respuestas no autorizadas
function handleUnauthorized(response) {
    if (response.status === 401) {
        window.location.href = '/frontend/modules/login_administrador/pages/index.html';
    }
    return response;
} 