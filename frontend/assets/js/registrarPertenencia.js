function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
}

const API_URL = "https://intelliguard-ia-o65o.onrender.com"; // URL del backend desplegado

// Variables globales
let stream = null;
let capturedImage = null;
let data = { estudiante: null, objeto: null };

// Elementos del DOM
const video = document.getElementById('video');
const captureBtn = document.getElementById('captureBtn');
const retakeBtn = document.getElementById('retakeBtn');
const preview = document.getElementById('preview');
const previewContainer = document.querySelector('.preview-container');
const cameraContainer = document.querySelector('.camera-container');
const codigoInput = document.getElementById('codigoEstudiante');
const tipoInput = document.getElementById('tipoObjeto');
const descInput = document.getElementById('descripcion');
const nombreInput = document.getElementById('nombreEstudiante');
const carreraInput = document.getElementById('carreraEstudiante');
const planInput = document.getElementById('planEstudiante');

// Elementos opcionales (para mostrar información y resultados)
let registroInfo = null;
let registroResult = null;
let responseMessage = null;
let successIcon = null;
let errorIcon = null;

// Inicialización
document.addEventListener('DOMContentLoaded', async function() {
    // Inicializar elementos opcionales si existen
    registroInfo = document.querySelector('.registro-info');
    registroResult = document.querySelector('.registro-result');
    if (registroResult) {
        responseMessage = registroResult.querySelector('.response-message');
        successIcon = registroResult.querySelector('.success-icon');
        errorIcon = registroResult.querySelector('.error-icon');
    }

    await inicializarCamara();
    inicializarCodigoEstudiante();
    inicializarEventListeners();
    validarDatosIniciales();
});

// Funciones de inicialización
async function inicializarCamara() {
    try {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            throw new Error('Tu navegador no soporta el acceso a la cámara');
        }

        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                width: { ideal: 1280 },
                height: { ideal: 720 }
            } 
        });
        video.srcObject = stream;
        video.style.display = 'block';
        captureBtn.style.display = 'block';
    } catch (err) {
        console.error('Error al iniciar la cámara:', err);
        alert('Error al acceder a la cámara: ' + err.message);
        cameraContainer.innerHTML = `
            <div class="camera-error">
                <i class="fas fa-exclamation-circle"></i>
                <p>Error al acceder a la cámara: ${err.message}</p>
                <button onclick="inicializarCamara()" class="btn btn-primary">Reintentar</button>
            </div>
        `;
    }
}

function inicializarCodigoEstudiante() {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user && user.codigo) {
        codigoInput.value = user.codigo;
        codigoInput.readOnly = true;
        if (nombreInput) nombreInput.value = user.nombre || '';
        if (carreraInput) carreraInput.value = user.carrera || '';
        if (planInput) planInput.value = user.planEstudiante || '';
        // Los campos de nombre, carrera y plan quedan editables
    } else {
        codigoInput.readOnly = false;
        codigoInput.value = '';
        if (nombreInput) nombreInput.value = '';
        if (carreraInput) carreraInput.value = '';
        if (planInput) planInput.value = '';
    }
}

function inicializarEventListeners() {
    // Eventos de la cámara
    captureBtn.addEventListener('click', capturarImagen);
    retakeBtn.addEventListener('click', volverACapturar);
    
    // Eventos de formulario
    document.getElementById('registroForm').addEventListener('submit', manejarEnvioFormulario);
    
    // Eventos de comunicación entre ventanas
    window.addEventListener('message', manejoDeVentanas);
}

// Funciones de manejo de cámara
function capturarImagen() {
    if (!stream) return;
    
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    
    capturedImage = canvas.toDataURL('image/jpeg').split(',')[1];
    preview.src = 'data:image/jpeg;base64,' + capturedImage;
    
    // Cambiar visibilidad de contenedores
    cameraContainer.style.display = 'none';
    previewContainer.style.display = 'block';
}

function volverACapturar() {
    previewContainer.style.display = 'none';
    cameraContainer.style.display = 'block';
    capturedImage = null;
}

// Funciones de validación
function validarCodigoEstudiante(event) {
    const codigo = event.target.value;
    if (!codigo) {
        alert('El código de estudiante es requerido');
        return false;
    }
    return true;
}

function validarDatosIniciales() {
    const storedData = JSON.parse(localStorage.getItem('data')) || {};
    if (!storedData.estudiante && !storedData.objeto) {
        window.open('identificar-estudiante.html', '_blank');
    } else {
        data = storedData;
        mostrarDatos(data);
    }
}

// Funciones de manejo de datos
function manejoDeVentanas(event) {
    const { type, payload } = event.data;
    switch(type) {
        case 'EstudianteData':
            data.estudiante = payload;
            mostrarDatos(data);
            abrirVentanaIdentificarObjeto();
            break;
        case 'ObjetoData':
            data.objeto = payload;
            mostrarDatos(data);
            registrarPertenencia();
            break;
    }
}

async function manejarEnvioFormulario(e) {
    e.preventDefault();
    
    if (!capturedImage) {
        alert('Por favor, capture una imagen del objeto');
        return;
    }
    
    if (!validarCodigoEstudiante({ target: codigoInput })) {
        return;
    }
    if (!nombreInput.value.trim()) {
        alert('Por favor, ingrese el nombre del estudiante');
        return;
    }
    if (!carreraInput.value.trim()) {
        alert('Por favor, ingrese la carrera del estudiante');
        return;
    }
    if (!planInput.value.trim()) {
        alert('Por favor, ingrese el plan del estudiante');
        return;
    }
    
    // Construir el payload JSON
    const payload = {
        codigo_estudiante: codigoInput.value,
        tipo_objeto: tipoInput.value,
        descripcion: descInput.value,
        imagen: 'data:image/jpeg;base64,' + capturedImage
    };
    
    try {
        const response = await fetch(API_URL + '/ia/pertenencias/registrar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + getCookie('jwt')
            },
            body: JSON.stringify(payload)
        });
        
        const result = await response.json();
        if (response.ok) {
            mostrarIconoResultado(true, "Pertenencia registrada exitosamente");
            limpiarFormulario();
        } else {
            throw new Error(result.message || 'Error al registrar pertenencia');
        }
    } catch (error) {
        mostrarIconoResultado(false, error.message);
    }
}

function registrarPertenencia() {
    if (!data.objeto || !data.estudiante) {
        mostrarIconoResultado(false, "Faltan datos necesarios para el registro");
        return;
    }

    const formData = new FormData();
    formData.append('file', dataURItoFile(data.objeto.imgUri, 'photo.jpg'));
    formData.append('idEstudiante', data.estudiante.id);
    formData.append('idObjeto', data.objeto.idObjeto);

    if (data.objeto.tipoRegistro === "coincidencias") {
        formData.append('codigoPertenencia', data.objeto.codigoPertenencia);
        fetchRegistrarIngresoPertenecia(formData)
            .then(data => mostrarIconoResultado(true, data.message))
            .catch(error => handleErrorResponse(error));
    } else {
        fetchRegistrarPertenencia(formData)
            .then(data => mostrarIconoResultado(true, "Pertenencia registrada exitosamente"))
            .catch(error => handleErrorResponse(error));
    }
}

// Funciones de utilidad
function limpiarFormulario() {
    document.getElementById('registroForm').reset();
    previewContainer.style.display = 'none';
    cameraContainer.style.display = 'block';
    capturedImage = null;
}

function mostrarDatos(data) {
    if (!registroInfo) return; // Si no existe el contenedor, no mostramos nada
    
    let content = `<h2>Información del Registro</h2><br>`;
    
    if (data.estudiante) {
        content += `
            <div class="info-row">
                <div class="info-label">Código Estudiante:</div>
                <div class="info-value">${data.estudiante.codigo}</div>
            </div>
            <div class="info-row">
                <div class="info-label">Estudiante:</div>
                <div class="info-value">${data.estudiante.nombre}</div>
            </div>
            <div class="info-row">
                <div class="info-label">Carrera:</div>
                <div class="info-value">${data.estudiante.carrera}</div>
            </div>
            <div class="info-row">
                <div class="info-label">Plan:</div>
                <div class="info-value">${data.estudiante.planEstudiante}</div>
            </div>`;
    }
    
    if (data.objeto) {
        content += data.objeto.ultimoEstado ? `
            <div class="info-row">
                <div class="info-label">Código Pertenencia:</div>
                <div class="info-value">${data.objeto.codigoPertenencia}</div>
            </div>
            <div class="info-row">
                <div class="info-label">Objeto:</div>
                <div class="info-value">${data.objeto.objeto}</div>
            </div>
            <div class="info-row">
                <div class="info-label">Última Fecha Actividad:</div>
                <div class="info-value">${data.objeto.fechaUltimaActividad}</div>
            </div>
            <div class="info-row">
                <div class="info-label">Último Estado:</div>
                <div class="info-value">${data.objeto.ultimoEstado}</div>
            </div>
            <div class="info-row">
                <div class="info-label">Imagen:</div>
                <div class="info-value">
                    <img src="${data.objeto.imgUri}" alt="${data.objeto.objeto}" class="objeto-img">
                </div>
            </div>` : `
            <div class="info-row">
                <div class="info-label">Nueva Pertenencia Registrada!!!</div>
                <div class="info-label">Objeto:</div>
                <div class="info-value">${data.objeto.objeto}</div>
            </div>
            <div class="info-row">
                <div class="info-label">Imagen:</div>
                <div class="info-value">
                    <img src="${data.objeto.imgUri}" alt="${data.objeto.objeto}" class="objeto-img">
                </div>
            </div>`;
    }
    
    registroInfo.innerHTML = content;
}

function mostrarIconoResultado(exito, mensaje) {
    if (!registroResult || !responseMessage || !successIcon || !errorIcon) {
        // Si no existen los elementos de resultado, usamos alert
        alert(mensaje);
        return;
    }
    
    registroResult.style.display = 'block';
    responseMessage.textContent = mensaje;
    successIcon.style.display = exito ? 'block' : 'none';
    errorIcon.style.display = exito ? 'none' : 'block';
}

// Funciones de API
async function fetchRegistrarIngresoPertenecia(formData) {
    const response = await fetch(API_URL + '/pertenencia/registrar-ingreso-pertenencia', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + getCookie('jwt')
        },
        body: formData
    });
    
    if (!response.ok) {
        throw await response.json();
    }
    
    return response.json();
}

async function fetchRegistrarPertenencia(formData) {
    const response = await fetch(API_URL + '/pertenencia/nueva-pertenencia', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + getCookie('jwt')
        },
        body: formData
    });
    
    if (!response.ok) {
        throw await response.json();
    }
    
    return response.json();
}

// Función auxiliar para convertir DataURI a File
function dataURItoFile(dataURI, filename) {
    const byteString = atob(dataURI.split(',')[1]);
    const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
    const ab = new ArrayBuffer(byteString.length);
    const ia = new Uint8Array(ab);
    
    for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    
    return new File([ab], filename, { type: mimeString });
}
function handleErrorResponse(error) {
    error.json().then(err => {
        mostrarIconoResultado(false, err.message || 'Error al Registrar Pertenencia');
    });
}

function abrirVentanaIdentificarObjeto() {
    let idEstudiante = data.estudiante.id;
    let url = 'identificar-objeto.html?idEstudiante=' + idEstudiante;
    window.open(url, '_blank');
}

