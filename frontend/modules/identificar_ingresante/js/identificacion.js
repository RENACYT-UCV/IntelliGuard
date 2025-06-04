import { API_CONFIG } from '../utils/config.js';
import { getToken } from '../utils/sessionManager.js';

let capturedImage = null;
let faceDetected = false;
let modeloEntrenado = false;
let mediaStream = null;
const MIN_FOTOS_ENTRENAMIENTO = 5;
const fotosEntrenamiento = [];
const UMBRAL_SIMILITUD = 0.85;

async function iniciarCamara() {
    try {
        if (mediaStream) {
            mediaStream.getTracks().forEach(track => track.stop());
        }

        const video = document.getElementById('camera');
        mediaStream = await navigator.mediaDevices.getUserMedia({
            video: {
                width: { ideal: 1280 },
                height: { ideal: 720 },
                facingMode: 'user',
                frameRate: { ideal: 30 }
            }
        });
        video.srcObject = mediaStream;

        // Manejar desconexión de cámara
        mediaStream.getVideoTracks()[0].onended = () => {
            mostrarError('La cámara se ha desconectado');
            reiniciarCamara();
        };

        await verificarModeloEntrenado();
    } catch (error) {
        console.error('Error al acceder a la cámara:', error);
        mostrarError('No se pudo acceder a la cámara. Verifique que esté conectada y que haya dado los permisos necesarios.');
    }
}

async function reiniciarCamara() {
    try {
        await iniciarCamara();
        mostrarExito('Cámara reiniciada exitosamente');
    } catch (error) {
        console.error('Error al reiniciar la cámara:', error);
        mostrarError('No se pudo reiniciar la cámara');
    }
}

async function verificarModeloEntrenado() {
    try {
        const response = await fetch(API_CONFIG.IA.VERIFICAR_ROSTRO, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${getToken()}`
            }
        });
        const data = await response.json();
        modeloEntrenado = data.modelo_entrenado;

        // Mostrar/ocultar elementos según el estado del modelo
        document.getElementById('entrenamientoSection').style.display =
            modeloEntrenado ? 'none' : 'block';
        document.getElementById('identificacionSection').style.display =
            modeloEntrenado ? 'block' : 'none';
    } catch (error) {
        console.error('Error al verificar modelo:', error);
        mostrarError('Error al verificar el estado del modelo');
    }
}

async function capturarFotoEntrenamiento() {
    const resultado = await capturarFoto();
    if (resultado && fotosEntrenamiento.length < MIN_FOTOS_ENTRENAMIENTO) {
        fotosEntrenamiento.push(capturedImage);
        actualizarProgresoEntrenamiento();

        if (fotosEntrenamiento.length === MIN_FOTOS_ENTRENAMIENTO) {
            await entrenarModelo();
        }
    }
}

async function capturarFoto() {
    const video = document.getElementById('camera');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');

    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    capturedImage = canvas.toDataURL('image/jpeg');

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

        mostrarExito('Rostro detectado correctamente');
        return true;
    } catch (error) {
        console.error('Error al detectar rostro:', error);
        mostrarError('Error al procesar la imagen');
        return false;
    }
}

async function entrenarModelo() {
    mostrarCargando('Entrenando modelo...');

    try {
        const formData = new FormData();
        fotosEntrenamiento.forEach((foto, index) => {
            formData.append(`foto_${index}`, foto);
        });

        const response = await fetch(API_CONFIG.IA.ENTRENAR_MODELO, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${getToken()}`
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error('Error al entrenar el modelo');
        }

        modeloEntrenado = true;
        mostrarExito('Modelo entrenado exitosamente');
        document.getElementById('entrenamientoSection').style.display = 'none';
        document.getElementById('identificacionSection').style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
        mostrarError('Error al entrenar el modelo');
    } finally {
        ocultarCargando();
    }
}

async function identificarIngresante() {
    if (!capturedImage || !faceDetected) {
        mostrarError('Debe capturar una foto primero');
        return;
    }

    if (!mediaStream?.active) {
        mostrarError('La cámara no está activa');
        await reiniciarCamara();
        return;
    }

    mostrarCargando('Identificando...');

    try {
        // Verificar identidad
        const verificacionResponse = await fetch(API_CONFIG.IA.VERIFICAR_IDENTIDAD, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getToken()}`
            },
            body: JSON.stringify({
                imagen: capturedImage,
                configuracion: {
                    umbral_similitud: UMBRAL_SIMILITUD,
                    modo_alta_precision: true
                }
            })
        });

        if (!verificacionResponse.ok) {
            throw new Error('Error en la verificación de identidad');
        }

        const verificacionData = await verificacionResponse.json();

        if (verificacionData.identidad_verificada) {
            // Obtener similitud y datos del estudiante
            const similitudResponse = await fetch(API_CONFIG.IA.OBTENER_SIMILITUD, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getToken()}`
                },
                body: JSON.stringify({ imagen: capturedImage })
            });

            if (!similitudResponse.ok) {
                throw new Error('Error al obtener similitud');
            }

            const similitudData = await similitudResponse.json();

            if (similitudData.similitud > UMBRAL_SIMILITUD) {
                mostrarResultadoIdentificacion(similitudData.estudiante);
                await registrarIngreso(similitudData.estudiante.id);

                // Actualizar modelo con la nueva imagen si la similitud es muy alta
                if (similitudData.similitud > 0.95) {
                    actualizarModeloConNuevaImagen(capturedImage, similitudData.estudiante.id);
                }
            } else {
                mostrarError(`No se pudo confirmar la identidad con suficiente certeza (${Math.round(similitudData.similitud * 100)}% de similitud)`);
            }
        } else {
            mostrarError('No se pudo verificar la identidad');
        }
    } catch (error) {
        console.error('Error:', error);
        mostrarError('Error en el proceso de identificación: ' + error.message);
    } finally {
        ocultarCargando();
    }
}

async function actualizarModeloConNuevaImagen(imagen, idEstudiante) {
    try {
        await fetch(API_CONFIG.IA.ACTUALIZAR_MODELO, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getToken()}`
            },
            body: JSON.stringify({
                imagen: imagen,
                id_estudiante: idEstudiante
            })
        });
    } catch (error) {
        console.error('Error al actualizar modelo:', error);
        // No mostramos error al usuario ya que esto es un proceso en segundo plano
    }
}

async function registrarIngreso(idEstudiante) {
    try {
        const response = await fetch(API_CONFIG.ESTUDIANTE.REGISTRAR, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getToken()}`
            },
            body: JSON.stringify({
                id_estudiante: idEstudiante,
                fecha_ingreso: new Date().toISOString()
            })
        });

        if (!response.ok) {
            throw new Error('Error al registrar el ingreso');
        }

        mostrarExito('Ingreso registrado exitosamente');
    } catch (error) {
        console.error('Error:', error);
        mostrarError('Error al registrar el ingreso');
    }
}

function actualizarProgresoEntrenamiento() {
    const progreso = document.getElementById('progresoEntrenamiento');
    const porcentaje = (fotosEntrenamiento.length / MIN_FOTOS_ENTRENAMIENTO) * 100;
    progreso.style.width = `${porcentaje}%`;
    progreso.textContent = `${fotosEntrenamiento.length}/${MIN_FOTOS_ENTRENAMIENTO} fotos`;
}

function mostrarResultadoIdentificacion(estudiante) {
    const resultadoDiv = document.getElementById('resultadoIdentificacion');
    resultadoDiv.innerHTML = `
        <h3>Estudiante Identificado</h3>
        <p><strong>Nombre:</strong> ${estudiante.nombre}</p>
        <p><strong>Código:</strong> ${estudiante.codigo}</p>
        <p><strong>Carrera:</strong> ${estudiante.carrera}</p>
    `;
    resultadoDiv.style.display = 'block';
}

function mostrarCargando(mensaje) {
    const loadingDiv = document.getElementById('loading');
    loadingDiv.textContent = mensaje;
    loadingDiv.style.display = 'block';
}

function ocultarCargando() {
    document.getElementById('loading').style.display = 'none';
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

// Función de limpieza
function limpiarRecursos() {
    if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());
        mediaStream = null;
    }
    capturedImage = null;
    faceDetected = false;
    fotosEntrenamiento.length = 0;
}

// Manejar cierre de página
window.addEventListener('beforeunload', limpiarRecursos);

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
    iniciarCamara();

    // Botones de entrenamiento
    document.getElementById('capturarEntrenamientoBtn').addEventListener('click', capturarFotoEntrenamiento);

    // Botones de identificación
    document.getElementById('capturarBtn').addEventListener('click', capturarFoto);
    document.getElementById('identificarBtn').addEventListener('click', identificarIngresante);

    // Botón de reinicio de cámara
    document.getElementById('reiniciarCamaraBtn')?.addEventListener('click', reiniciarCamara);
});

// Exportar funciones para uso global
window.capturarFotoEntrenamiento = capturarFotoEntrenamiento;
window.capturarFoto = capturarFoto;
window.identificarIngresante = identificarIngresante;
window.reiniciarCamara = reiniciarCamara; 