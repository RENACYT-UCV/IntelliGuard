let stream = null;
let isFrontCamera = true;
let reconocimientoActivo = false;
let intentosReconocimiento = 0;
const MAX_INTENTOS = 30;
const INTERVALO_RECONOCIMIENTO = 1000; // 1 segundo entre intentos
let ultimoCodigoReconocido = null;
let ultimaConfianza = 0;

// Elementos del DOM
const videoElement = document.getElementById('videoElement');
const canvas = document.getElementById('canvas');
const toggleCameraBtn = document.getElementById('toggleCameraBtn');
const loginBtn = document.getElementById('loginBtn');
const statusText = document.getElementById('statusText');
const progressBar = document.getElementById('progressBar');
const progressContainer = document.querySelector('.progress');

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    initCamera();
    setupEventListeners();
});

// Inicializar cámara
async function initCamera() {
    try {
        const facingMode = isFrontCamera ? 'user' : 'environment';
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { facingMode },
            audio: false
        });
        videoElement.srcObject = stream;
        iniciarReconocimiento();
    } catch (error) {
        mostrarError('Error al acceder a la cámara: ' + error.message);
    }
}

// Configurar event listeners
function setupEventListeners() {
    toggleCameraBtn.addEventListener('click', alternarCamara);
    loginBtn.addEventListener('click', iniciarSesion);
    
    // Detener la cámara cuando se cierra la página
    window.addEventListener('beforeunload', () => {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
    });
}

// Alternar entre cámaras frontal y trasera
async function alternarCamara() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    isFrontCamera = !isFrontCamera;
    await initCamera();
}

// Iniciar proceso de reconocimiento facial
function iniciarReconocimiento() {
    if (!reconocimientoActivo) {
        reconocimientoActivo = true;
        intentosReconocimiento = 0;
        ultimoCodigoReconocido = null;
        ultimaConfianza = 0;
        actualizarEstado('Buscando rostro...', 'info');
        realizarReconocimiento();
    }
}

// Realizar reconocimiento facial
async function realizarReconocimiento() {
    if (!reconocimientoActivo || intentosReconocimiento >= MAX_INTENTOS) {
        if (intentosReconocimiento >= MAX_INTENTOS) {
            mostrarError('No se pudo reconocer el rostro. Por favor, intente nuevamente.');
            reconocimientoActivo = false;
        }
        return;
    }

    try {
        // Capturar frame actual
        const context = canvas.getContext('2d');
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
        
        // Convertir a base64
        const imagenBase64 = canvas.toDataURL('image/jpeg').split(',')[1];

        // Validar que la imagen no esté vacía o sea muy pequeña
        if (!imagenBase64 || imagenBase64.length < 5000) { // 5000 es un umbral seguro para evitar frames vacíos
            intentosReconocimiento++;
            setTimeout(realizarReconocimiento, INTERVALO_RECONOCIMIENTO);
            return;
        }
        
        // Enviar al backend
        const response = await fetch(API_URL + '/ia/reconocimiento/verificar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ imagen: imagenBase64 })
        });

        const data = await response.json();
        
        if (response.ok && data.codigo_estudiante) {
            ultimoCodigoReconocido = data.codigo_estudiante;
            ultimaConfianza = data.confianza;
            
            // Actualizar progreso
            const progreso = (intentosReconocimiento / MAX_INTENTOS) * 100;
            actualizarProgreso(progreso);
            
            if (data.confianza >= 60) {
                reconocimientoActivo = false;
                mostrarEstudianteReconocido(data.codigo_estudiante, data.confianza);
            } else {
                actualizarEstado(`Similitud: ${data.confianza.toFixed(1)}%`, 'info');
                intentosReconocimiento++;
                setTimeout(realizarReconocimiento, INTERVALO_RECONOCIMIENTO);
            }
        } else {
            intentosReconocimiento++;
            actualizarEstado('Buscando rostro...', 'info');
            setTimeout(realizarReconocimiento, INTERVALO_RECONOCIMIENTO);
        }
    } catch (error) {
        console.error('Error en reconocimiento:', error);
        intentosReconocimiento++;
        setTimeout(realizarReconocimiento, INTERVALO_RECONOCIMIENTO);
    }
}

// Mostrar estudiante reconocido
function mostrarEstudianteReconocido(codigo, confianza) {
    actualizarEstado(`¡Estudiante reconocido! Código: ${codigo}`, 'success');
    progressContainer.style.display = 'none';
    loginBtn.style.display = 'block';

    // Obtener el token del backend
    fetch(API_URL + '/ia/login/estudiante', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ codigo_estudiante: codigo })
    })
    .then(response => response.json())
    .then(data => {
        if (data.access_token) {
            // Guardar el token y el código en la cookie usando saveAuth
            saveAuth(data.access_token, codigo);
            // Guardar información del usuario
            localStorage.setItem('user', JSON.stringify({
                codigo: codigo,
                tipo: 'estudiante'
            }));
            // Redirigir al menú
            window.location.href = 'menu.html';
        } else {
            throw new Error('No se recibió el token de acceso');
        }
    })
    .catch(error => {
        mostrarError('Error al obtener el token: ' + error.message);
        loginBtn.disabled = false;
    });
}

// Iniciar sesión
async function iniciarSesion() {
    if (!ultimoCodigoReconocido) {
        mostrarError('No se ha reconocido ningún estudiante');
        return;
    }

    try {
        loginBtn.disabled = true;
        actualizarEstado('Iniciando sesión...', 'info');
        localStorage.setItem('user', JSON.stringify({
            codigo: ultimoCodigoReconocido,
            tipo: 'estudiante'
        }));
        window.location.href = 'menu.html';
    } catch (error) {
        mostrarError('Error al iniciar sesión: ' + error.message);
        loginBtn.disabled = false;
    }
}

// Funciones de utilidad
function actualizarEstado(mensaje, tipo) {
    statusText.textContent = mensaje;
    statusText.className = `text-${tipo === 'error' ? 'danger' : tipo === 'success' ? 'success' : 'info'}`;
}

function actualizarProgreso(porcentaje) {
    progressContainer.style.display = 'block';
    progressBar.style.width = `${porcentaje}%`;
}

function mostrarError(mensaje) {
    actualizarEstado(mensaje, 'error');
    progressContainer.style.display = 'none';
    loginBtn.style.display = 'none';
}

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
} 