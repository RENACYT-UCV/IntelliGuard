document.addEventListener('DOMContentLoaded', function() {
    const consultaInfo = document.querySelector('.consulta-info');
    const registroResult = document.querySelector('.registro-result');
    const registrarSalidaBtn = document.getElementById('registrarSalidaBtn');
    const resultDiv = document.getElementById('result');
    const containerResult = document.getElementById('container-result');
    const spinnerObjeto = document.querySelector('.spinner-box');
    let dataPertenencia = { estudiante: null, objetos: [] };
    const user = JSON.parse(localStorage.getItem('user'));
    const codigoEstudiante = user ? user.codigo : null;
    const container = document.getElementById('pertenencias-container');
    const codigoEstudianteDiv = document.getElementById('codigo-estudiante');

    init();

    function init() {
        //validTokenSession();
        if (!dataPertenencia.estudiante) {
            window.open('identificar-estudiante.html', '_blank');
        }
        registrarSalidaBtn.addEventListener('click', registrarSalida);
        window.addEventListener('message', handleMessage);

        if (!codigoEstudiante) {
            container.innerHTML = '<p>No se encontró el código del estudiante.</p>';
            registrarSalidaBtn.disabled = true;
            return;
        }

        if (codigoEstudianteDiv) {
            codigoEstudianteDiv.textContent = codigoEstudiante || 'No disponible';
        }

        // 1. Consultar pertenencias activas
        fetch(API_URL + '/ia/pertenencias/consultar?codigo_estudiante=' + codigoEstudiante, {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + getCookie('jwt')
            }
        })
        .then(res => res.json())
        .then(data => {
            dataPertenencia.objetos = (Array.isArray(data) ? data : []).filter(p =>
                p.estado && (p.estado.toUpperCase() === 'ENTREGADO' || p.estado.toLowerCase() === 'entrada')
            );
            if (dataPertenencia.objetos.length === 0) {
                container.innerHTML = '<p>No tienes pertenencias activas.</p>';
                registrarSalidaBtn.disabled = true;
                return;
            }
            container.innerHTML = dataPertenencia.objetos.map((p, i) => `
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="pertenencia" id="pertenencia${i}" value="${p.id}">
                    <label class="form-check-label" for="pertenencia${i}">
                        ${p.tipo_objeto} - ${p.descripcion} (${p.fecha_entrada})
                    </label>
                </div>
            `).join('');
            registrarSalidaBtn.disabled = false;
        });
    }

    function handleMessage(event) {
        if (event.data.type === 'EstudianteData') {
            dataPertenencia.estudiante = event.data.payload;
            consultarPertenencias(dataPertenencia);
        }
    }

    function consultarPertenencias(dataPertenencia) {
        mostrarSpinner(true);
        console.log(dataPertenencia);

        fetchConsultarRegistros()
            .then(data => {
                containerResult.style.display = 'block';
                mostrarInfoEstudiante(dataPertenencia);
                actualizarVistaPertenencias(data);
                inicializarCheckboxes();
            })
            .catch(error => {
                mostrarInfoEstudiante(dataPertenencia);
                mostrarIconoResultado(false, error.message);
            });
    }

    function fetchConsultarRegistros() {
        const formData = new FormData();
        formData.append('idEstudiante', dataPertenencia.estudiante.id);
        formData.append('idEstado', '1');
        return fetch(API_URL + '/pertenencia/consultar-pertenencia-estado-estudiante', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + getCookie('jwt'),
            },
            body: formData
        })
        .then(handleResponse)
        .then(response => response.json());
    }

    function registrarSalida() {
        containerResult.style.display = 'none';
        const seleccionada = document.querySelector('input[name="pertenencia"]:checked');
        if (!seleccionada) {
            alert('Selecciona una pertenencia para registrar la salida.');
            return;
        }
        const idSeleccionada = seleccionada.value;
        const pertenencia = dataPertenencia.objetos.find(p => p.id == idSeleccionada);

        fetch(API_URL + '/ia/pertenencias/registrar-salida', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + getCookie('jwt')
            },
            body: JSON.stringify({
                codigo_estudiante: codigoEstudiante,
                tipo_objeto: pertenencia.tipo_objeto
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.mensaje) {
                alert('Salida registrada exitosamente');
                window.location.reload();
            } else {
                alert(data.error || 'Error al registrar salida');
            }
        });
    }

    function handleResponse(response) {
        mostrarSpinner(false);
        // handleUnauthorized(response);
        if (response.status === 404) {
            return response.json().then(data => {
                mostrarIconoResultado(false, 'No hay pertenencias registradas del estudiante');
                throw new Error('No hay pertenencias registradas del estudiante');
            });
        }
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response;
    }

    function actualizarVistaPertenencias(data) {
        const pertenenciasContainer = document.getElementById('pertenencias-container');
        pertenenciasContainer.innerHTML = '';
        console.log(data.pertenencias);
        dataPertenencia.objetos = data.pertenencias; // Asegúrate de actualizar correctamente el dataPertenencia.objetos
        console.log(dataPertenencia.objetos);
        data.pertenencias.forEach(pertenencia => {
            const fechaHora = convertirFecha(pertenencia.hora_entrada);
            const fechaTexto = fechaHora.toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
            const horaTexto = fechaHora.toLocaleTimeString('es-ES', { hour: 'numeric', minute: 'numeric', second: 'numeric' });
        
            const pertenenciaDiv = document.createElement('div');
            pertenenciaDiv.classList.add('pertenencia');
            pertenenciaDiv.innerHTML = `
                <div class="checkbox-container">
                    <input type="checkbox" class="select-pertenencia" checked>
                    <img src="${pertenencia.imagen_pertenencia}" alt="Imagen de la Pertenencia" class="pertenencia-img" style="width: 200px;">
                </div>
                <div class="pertenencia-info">
                    <h4>C. Pertenencia : ${pertenencia.codigo_pertenencia}</h4>
                    <h4>Objeto: ${pertenencia.nombre_objeto}</h4>
                    <p>Fecha: ${fechaTexto}</p>
                    <p>Hora: ${horaTexto}</p>
                    <h4>Estado Actual: ${pertenencia.nombre_estado}</h4>
                </div>
            `;
            pertenenciasContainer.appendChild(pertenenciaDiv);
        });
    }

    function mostrarInfoEstudiante(data) {
        dataPertenencia.objetos = data.pertenencias;
        consultaInfo.innerHTML = `
            <div class="info-row">
                <div class="info-label">Código Estudiante: </div>
                <div class="info-value">${data.estudiante.codigo}</div>
            </div>
            <div class="info-row">
                <div class="info-label">Estudiante: </div>
                <div class="info-value">${data.estudiante.nombre}</div>
            </div>
            <div class="info-row">
                <div class="info-label">Carrera: </div>
                <div class="info-value">${data.estudiante.carrera}</div>
            </div>
            <div class="info-row">
                <div class="info-label">Plan: </div>
                <div class="info-value">${data.estudiante.planEstudiante}</div>
            </div>
            <hr>
            <div class="checkbox-title">
                <div class="checkbox-title">** Las Pertenencias que no tengan un Check serán marcadas como Extraviadas **</div>
            </div>
            <div class="info-checkbox">
                <input type="checkbox" id="select-all" class="check-label" checked> Todas Las Pertenencias
            </div>
        `;
        document.getElementById('select-all').addEventListener('change', toggleSelectAll);
    }

    function inicializarCheckboxes() {
        const checkboxes = document.querySelectorAll('.select-pertenencia');
        checkboxes.forEach(checkbox => {
            checkbox.checked = true;
            checkbox.addEventListener('change', function() {
                if (!this.checked) {
                    document.getElementById('select-all').checked = false;
                }
            });
        });
    }

    function toggleSelectAll(event) {
        const isChecked = event.target.checked;
        const checkboxes = document.querySelectorAll('.select-pertenencia');
        checkboxes.forEach(checkbox => {
            checkbox.checked = isChecked;
        });
    }

    function crearPertenenciaDiv(pertenencia) {
    
        const fechaHora = convertirFecha(pertenencia.hora_entrada);
        const fechaTexto = fechaHora.toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
        const horaTexto = fechaHora.toLocaleTimeString('es-ES', { hour: 'numeric', minute: 'numeric', second: 'numeric' });
    
        const pertenenciaDiv = document.createElement('div');
        pertenenciaDiv.classList.add('pertenencia');
        pertenenciaDiv.innerHTML = `
            <div class="checkbox-container">
                <input type="checkbox" class="select-pertenencia" checked>
                <img src="${pertenencia.imagen_pertenencia}" alt="Imagen de la Pertenencia" class="pertenencia-img">
            </div>
            <div class="pertenencia-info">
                <h4>C. Pertenencia : ${pertenencia.codigo_pertenencia}</h4>
                <h4>Objeto: ${pertenencia.nombre_objeto}</h4>
                <p>Fecha: ${fechaTexto}</p>
                <p>Hora: ${horaTexto}</p>
                <h4>Estado Actual: ${pertenencia.nombre_estado}</h4>
            </div>
        `;
    
        return pertenenciaDiv;
    }

    function mostrarIconoResultado(exito, mensaje) {
        registroResult.style.display = 'block';
        const responseMessage = registroResult.querySelector('.response-message');

        responseMessage.textContent = mensaje;


    }

    function mostrarSpinner(mostrar) {
        spinnerObjeto.style.display = mostrar ? 'flex' : 'none';
    }
});


