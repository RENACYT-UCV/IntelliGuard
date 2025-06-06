document.addEventListener('DOMContentLoaded', function() {
    //validTokenSession();
    const identificarObjetoBtn = document.getElementById('identificarObjetoBtn');
    const registroInfo = document.querySelector('.registro-info');
    const registroResult = document.querySelector('.registro-result');
    const responseMessage = registroResult.querySelector('.response-message');
    const successIcon = registroResult.querySelector('.success-icon');
    const errorIcon = registroResult.querySelector('.error-icon');
    let data = { estudiante: null, objeto: null };

    init();

    function init() {
        identificarObjetoBtn.addEventListener('click', abrirVentanaIdentificarObjeto);
        validarDatos();
        window.addEventListener('message', manejoDeVentanas);
    }
    function abrirVentanaIdentificarObjeto() {
        let idEstudiante = data.estudiante.id;
        let url = 'identificar-objeto.html?idEstudiante=' + idEstudiante;
        window.open(url, '_blank');
    }

function validarDatos() {
  // Intenta obtener los datos guardados en localStorage
  const data = JSON.parse(localStorage.getItem('data')) || {};

  // Si no hay estudiante ni objeto, redirige a la página de identificación
  if (!data.estudiante && !data.objeto) {
    window.open('identificar-estudiante.html', '_blank');
  }
}

    function manejoDeVentanas(event) {
        const { type, payload } = event.data;
        if (type === 'EstudianteData') {
            data.estudiante = payload;
            mostrarDatos(data);
            abrirVentanaIdentificarObjeto();
        } else if (type === 'ObjetoData') {
            data.objeto = payload;
            mostrarDatos(data);
            registrarPertenencia();
        }
    }

    function registrarPertenencia() {
        const file = dataURItoFile(data.objeto.imgUri, 'photo.jpg');
        const formData = new FormData();
        formData.append('file', file);
        formData.append('idEstudiante', data.estudiante.id);
        formData.append('idObjeto', data.objeto.idObjeto);
        console.log(data)
        if(data.objeto.tipoRegistro == "coincidencias"){
            console.log(data.objeto)
            formData.append('codigoPertenencia', data.objeto.codigoPertenencia);
            fetchRegistrarIngresoPertenecia(formData)
                .then(data => mostrarIconoResultado(true, data.message))
                .catch(error => handleErrorResponse(error));

        }else{
            fetchRegistrarPertenencia(formData)
                .then(data => mostrarIconoResultado(true, "Se registro la Entrada de pertenencia exitosamente"))
                .catch(error => handleErrorResponse(error));

        }
    }

    function fetchRegistrarIngresoPertenecia(formData) {
        return fetch(API_URL + '/pertenencia/registrar-ingreso-pertenencia', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + getCookie('jwt'),
            },
            body: formData
        })
        .then(handleResponse)
        .then(response => response.json());
    }

    function fetchRegistrarPertenencia(formData) {
        return fetch(API_URL + '/pertenencia/nueva-pertenencia', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + getCookie('jwt'),
            },
            body: formData
        })
        .then(handleResponse)
        .then(response => response.json());
    }

    function handleResponse(response) {
        //handleUnauthorized(response)
        if (!response.ok) {
            throw response;
        }
        return response;
    }

    function handleErrorResponse(error) {
        error.json().then(err => {
            mostrarIconoResultado(false, err.message || 'Error al Registrar Pertenencia');
        });
    }

    function mostrarIconoResultado(exito, mensaje) {
        registroResult.style.display = 'block';
        responseMessage.textContent = mensaje;
        successIcon.style.display = exito ? 'block' : 'none';
        errorIcon.style.display = exito ? 'none' : 'block';
    }

    function mostrarDatos(data) {
        let content = `<h2>Información del Registro</h2><br>`;
        if (data.estudiante) {
            content += `
                <div class="info-row"><div class="info-label">Código Estudiante: </div>
                    <div class="info-value">${data.estudiante.codigo}</div></div><div class="info-row">
                    <div class="info-label">Estudiante: </div>
                    <div class="info-value">${data.estudiante.nombre}</div></div><div class="info-row">
                    <div class="info-label">Carrera: </div>
                    <div class="info-value">${data.estudiante.carrera}</div></div><div class="info-row">
                    <div class="info-label">Plan: </div>
                    <div class="info-value">${data.estudiante.planEstudiante}</div></div>`;
        }
        if (data.objeto) {
            if(data.objeto.ultimoEstado){
                content += `
                    <div class="info-row">
                        <div class="info-label">Codigo Pertenencia</div>
                        <div class="info-value">${data.objeto.codigoPertenencia}</div></div><div class="info-row">
                        <div class="info-label">Objeto:</div>
                        <div class="info-value">${data.objeto.objeto}</div></div><div class="info-row">
                        <div class="info-label">Ultima Fecha Actividad:</div>
                        <div class="info-value">${data.objeto.fechaUltimaActividad}</div></div><div class="info-row">
                        <div class="info-label">Ultimo Estado:</div>
                        <div class="info-value">${data.objeto.ultimoEstado}</div></div><div class="info-row">
                        <div class="info-label">Imagen:</div>
                        <div class="info-value"><img src="${data.objeto.imgUri}" alt="${data.objeto.objeto}" class="objeto-img"></div>
                    </div>`;

            }else{
                content += `
                    <div class="info-row">
                        <div class="info-label">Nueva Pertenencia Registrada!!!</div><br>
                        <div class="info-label">Objeto:</div><br>
                        <div class="info-value">${data.objeto.objeto}</div></div><div class="info-row">
                        <div class="info-label">Imagen:</div>
                        <div class="info-value"><img src="${data.objeto.imgUri}" alt="${data.objeto.objeto}" class="objeto-img"></div>
                    </div>`;

            }

        }
        registroInfo.innerHTML = content;
    }

    // Elementos esenciales
    let stream = null;
    const video = document.getElementById('video');
    const captureBtn = document.getElementById('captureBtn');
    const preview = document.getElementById('preview');
    const form = document.getElementById('registroForm');
    const codigoInput = document.getElementById('codigoEstudiante');
    const tipoInput = document.getElementById('tipoObjeto');
    const descInput = document.getElementById('descripcion');
    let capturedImage = null;

    // Autollenar código de estudiante
    const user = JSON.parse(localStorage.getItem('user'));
    if (user && user.codigo) {
        codigoInput.value = user.codigo;
        codigoInput.readOnly = true;
    }

    // Iniciar cámara
    async function startCamera() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
        } catch (err) {
            alert('Error al acceder a la cámara: ' + err.message);
        }
    }
    startCamera();

    // Capturar imagen
    captureBtn.addEventListener('click', function() {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        capturedImage = canvas.toDataURL('image/jpeg').split(',')[1];
        preview.src = 'data:image/jpeg;base64,' + capturedImage;
        preview.style.display = 'block';
    });

    // Enviar formulario
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        if (!capturedImage) {
            alert('Primero capture una imagen del objeto.');
            return;
        }
        const codigoEstudiante = codigoInput.value;
        const tipoObjeto = tipoInput.value;
        const descripcion = descInput.value;
        try {
            const response = await fetch('http://localhost:5000/ia/pertenencias/registrar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    codigo_estudiante: codigoEstudiante,
                    tipo_objeto: tipoObjeto,
                    descripcion: descripcion,
                    imagen: capturedImage
                })
            });
            const data = await response.json();
            if (response.ok) {
                alert('Pertenencia registrada exitosamente');
                form.reset();
                preview.style.display = 'none';
                capturedImage = null;
            } else {
                alert('Error: ' + (data.error || 'No se pudo registrar la pertenencia.'));
            }
        } catch (err) {
            alert('Error al registrar pertenencia: ' + err.message);
        }
    });
});
