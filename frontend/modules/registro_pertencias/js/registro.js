import { API_CONFIG } from '../../../js/config.js';
import { getToken } from '../utils/sessionManager.js';

let capturedImage = null;
let faceDetected = false;

async function iniciarCamara() {
    try {
        const video = document.getElementById('camera');
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (error) {
        console.error('Error al acceder a la cámara:', error);
        mostrarError('No se pudo acceder a la cámara');
    }
}

async function capturarFoto() {
    const video = document.getElementById('camera');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');

    // Capturar frame del video
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    capturedImage = canvas.toDataURL('image/jpeg');

    // Detectar rostro usando IA
    try {
        const response = await fetch(API_CONFIG.IA.DETECTAR_ROSTRO, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getToken()}`
            },
            body: JSON.stringify({ imagen: capturedImage })
        });

        const data = await response.json();
        faceDetected = data.rostro_detectado;

        if (!faceDetected) {
            mostrarError('No se detectó un rostro en la imagen');
            return false;
        }

        return true;
    } catch (error) {
        console.error('Error al detectar rostro:', error);
        mostrarError('Error al procesar la imagen');
        return false;
    }
}

async function registrarPertenencia(event) {
    event.preventDefault();

    if (!capturedImage || !faceDetected) {
        mostrarError('Debe capturar una foto del estudiante');
        return;
    }

    const formData = new FormData(document.getElementById('registroForm'));
    formData.append('foto', capturedImage);

    try {
        // Verificar identidad con IA
        const verificacionResponse = await fetch(API_CONFIG.IA.VERIFICAR_IDENTIDAD, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${getToken()}`
            },
            body: formData
        });

        const verificacionData = await verificacionResponse.json();

        if (!verificacionData.identidad_verificada) {
            mostrarError('No se pudo verificar la identidad del estudiante');
            return;
        }

        // Registrar pertenencia
        const registroResponse = await fetch(API_CONFIG.PERTENENCIAS.REGISTRAR, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${getToken()}`
            },
            body: formData
        });

        if (!registroResponse.ok) {
            throw new Error('Error al registrar la pertenencia');
        }

        const data = await registroResponse.json();

        // Generar reporte
        await generarReporte(data.id_registro);

        mostrarExito('Pertenencia registrada exitosamente');
        limpiarFormulario();
    } catch (error) {
        console.error('Error:', error);
        mostrarError('Error al registrar la pertenencia');
    }
}

async function generarReporte(idRegistro) {
    try {
        const response = await fetch(API_CONFIG.REPORTES.GENERAR_REPORTE, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getToken()}`
            },
            body: JSON.stringify({ id_registro: idRegistro })
        });

        if (!response.ok) {
            throw new Error('Error al generar el reporte');
        }

        const data = await response.json();
        const reporteUrl = data.reporte_url;

        // Mostrar enlace al reporte
        const reporteLink = document.getElementById('reporteLink');
        reporteLink.href = reporteUrl;
        reporteLink.style.display = 'block';
    } catch (error) {
        console.error('Error al generar reporte:', error);
    }
}

function limpiarFormulario() {
    document.getElementById('registroForm').reset();
    capturedImage = null;
    faceDetected = false;
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.width, canvas.height);
}

function mostrarError(mensaje) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = mensaje;
    errorDiv.style.display = 'block';
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 3000);
}

function mostrarExito(mensaje) {
    const successDiv = document.getElementById('success-message');
    successDiv.textContent = mensaje;
    successDiv.style.display = 'block';
    setTimeout(() => {
        successDiv.style.display = 'none';
    }, 3000);
}

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
    iniciarCamara();
    document.getElementById('registroForm').addEventListener('submit', registrarPertenencia);
    document.getElementById('capturarBtn').addEventListener('click', capturarFoto);
});

// Exportar funciones para uso global
window.capturarFoto = capturarFoto;
window.limpiarFormulario = limpiarFormulario; 