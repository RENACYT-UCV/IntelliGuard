let stream = null;
let isFrontCamera = true;
let isCapturing = false;
let capturedPhotos = [];
const MAX_PHOTOS = 5;
const CAPTURE_INTERVAL = 1000; // 1 segundo entre capturas
let captureInterval = null;

// Elementos del DOM
const videoElement = document.getElementById('videoElement');
const canvas = document.getElementById('canvas');
const startCaptureBtn = document.getElementById('startCaptureBtn');
const toggleCameraBtn = document.getElementById('toggleCameraBtn');
const registrarBtn = document.getElementById('registrarBtn');
const progressBar = document.getElementById('progressBar');
const progressText = document.getElementById('progressText');
const statusText = document.getElementById('statusText');
const photoPreview = document.getElementById('photoPreview');
const codigoEstudiante = document.getElementById('codigoEstudiante');

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    initCamera();
    setupEventListeners();
});

// Inicializar cámara
async function initCamera() {
    try {
        const constraints = {
            video: {
                facingMode: isFrontCamera ? 'user' : 'environment'
            }
        };
        stream = await navigator.mediaDevices.getUserMedia(constraints);
        videoElement.srcObject = stream;
    } catch (error) {
        console.error('Error al acceder a la cámara:', error);
        statusText.textContent = 'Error al acceder a la cámara';
        statusText.className = 'text-danger';
    }
}

// Configurar event listeners
function setupEventListeners() {
    startCaptureBtn.addEventListener('click', toggleCapture);
    toggleCameraBtn.addEventListener('click', toggleCamera);
    registrarBtn.addEventListener('click', registrarEstudiante);
}

// Alternar captura
function toggleCapture() {
    if (!codigoEstudiante.value) {
        statusText.textContent = 'Por favor, ingrese el código del estudiante';
        statusText.className = 'text-danger';
        return;
    }

    isCapturing = !isCapturing;
    if (isCapturing) {
        startCapture();
    } else {
        stopCapture();
    }
}

// Iniciar captura
function startCapture() {
    if (capturedPhotos.length >= MAX_PHOTOS) {
        resetCapture();
    }
    
    startCaptureBtn.textContent = 'Detener Captura';
    startCaptureBtn.className = 'btn btn-danger';
    statusText.textContent = 'Capturando fotos...';
    statusText.className = 'text-primary';
    
    captureInterval = setInterval(() => {
        if (capturedPhotos.length < MAX_PHOTOS) {
            capturePhoto();
        } else {
            stopCapture();
        }
    }, CAPTURE_INTERVAL);
}

// Detener captura
function stopCapture() {
    if (captureInterval) {
        clearInterval(captureInterval);
        captureInterval = null;
    }
    
    startCaptureBtn.textContent = 'Iniciar Captura';
    startCaptureBtn.className = 'btn btn-primary';
    
    if (capturedPhotos.length >= MAX_PHOTOS) {
        statusText.textContent = 'Captura completada';
        statusText.className = 'text-success';
        registrarBtn.disabled = false;
    } else {
        statusText.textContent = 'Captura detenida';
        statusText.className = 'text-warning';
    }
}

// Capturar foto
function capturePhoto() {
    const context = canvas.getContext('2d');
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    context.drawImage(videoElement, 0, 0);
    
    const photoData = canvas.toDataURL('image/jpeg');
    capturedPhotos.push(photoData);
    
    // Actualizar UI
    updateProgress();
    addPhotoPreview(photoData);
}

// Actualizar barra de progreso
function updateProgress() {
    const progress = (capturedPhotos.length / MAX_PHOTOS) * 100;
    progressBar.style.width = `${progress}%`;
    progressText.textContent = `${capturedPhotos.length}/${MAX_PHOTOS}`;
}

// Agregar vista previa de foto
function addPhotoPreview(photoData) {
    const img = document.createElement('img');
    img.src = photoData;
    img.className = 'photo-thumbnail';
    photoPreview.appendChild(img);
}

// Alternar cámara
async function toggleCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    isFrontCamera = !isFrontCamera;
    await initCamera();
}

// Resetear captura
function resetCapture() {
    capturedPhotos = [];
    photoPreview.innerHTML = '';
    updateProgress();
    registrarBtn.disabled = true;
}

// Registrar estudiante
async function registrarEstudiante() {
    if (!codigoEstudiante.value || capturedPhotos.length === 0) {
        statusText.textContent = 'Faltan datos requeridos';
        statusText.className = 'text-danger';
        return;
    }

    try {
        statusText.textContent = 'Registrando estudiante...';
        statusText.className = 'text-primary';
        registrarBtn.disabled = true;

        // Enviar todas las fotos al backend
        const formData = {
            codigo_estudiante: codigoEstudiante.value,
            imagenes: capturedPhotos.map(photo => photo.split(',')[1])
        };

        const response = await fetch(API_URL + '/ia/estudiantes/registrar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('step1').style.display = 'none';
            document.getElementById('step2').style.display = 'block';
        } else {
            throw new Error(data.error || 'Error al registrar el estudiante');
        }
    } catch (error) {
        console.error('Error:', error);
        statusText.textContent = error.message;
        statusText.className = 'text-danger';
        registrarBtn.disabled = false;
    } finally {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
    }
}

// Limpiar al cerrar
window.addEventListener('beforeunload', () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
});
