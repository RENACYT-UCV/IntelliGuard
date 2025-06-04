import { API_CONFIG } from '../../../js/config.js';
import { getToken } from '../utils/sessionManager.js';

async function consultarPertenencias(event) {
    event.preventDefault();

    const formData = new FormData(document.getElementById('consultaForm'));
    const datosEstudiante = formData.get('datosEstudiante');
    const estadoRegistros = formData.get('estadoRegistros');
    const codigoPertenencia = formData.get('codigoPertenencia');

    try {
        const response = await fetch(API_CONFIG.PERTENENCIAS.CONSULTAR, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${getToken()}`
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error('Error al consultar pertenencias');
        }

        const data = await response.json();
        mostrarResultados(data.pertenencias);
    } catch (error) {
        console.error('Error:', error);
        mostrarError('Error al consultar las pertenencias');
    }
}

function mostrarResultados(pertenencias) {
    const resultadosDiv = document.getElementById('resultados');
    resultadosDiv.innerHTML = '';

    if (pertenencias.length === 0) {
        resultadosDiv.innerHTML = '<p>No se encontraron resultados</p>';
        return;
    }

    const tabla = document.createElement('table');
    tabla.className = 'tabla-resultados';

    // Crear encabezados
    const encabezados = ['Código', 'Estudiante', 'Descripción', 'Estado', 'Fecha', 'Acciones'];
    const thead = document.createElement('thead');
    const trHead = document.createElement('tr');
    encabezados.forEach(texto => {
        const th = document.createElement('th');
        th.textContent = texto;
        trHead.appendChild(th);
    });
    thead.appendChild(trHead);
    tabla.appendChild(thead);

    // Crear cuerpo de la tabla
    const tbody = document.createElement('tbody');
    pertenencias.forEach(pertenencia => {
        const tr = document.createElement('tr');

        // Añadir datos
        tr.innerHTML = `
            <td>${pertenencia.codigo}</td>
            <td>${pertenencia.estudiante}</td>
            <td>${pertenencia.descripcion}</td>
            <td>${pertenencia.estado}</td>
            <td>${new Date(pertenencia.fecha).toLocaleString()}</td>
            <td>
                <button onclick="generarReporte('${pertenencia.id}')" class="btn-reporte">
                    Generar Reporte
                </button>
            </td>
        `;

        tbody.appendChild(tr);
    });
    tabla.appendChild(tbody);

    resultadosDiv.appendChild(tabla);
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
        window.open(data.reporte_url, '_blank');
    } catch (error) {
        console.error('Error al generar reporte:', error);
        mostrarError('Error al generar el reporte');
    }
}

function mostrarError(mensaje) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = mensaje;
    errorDiv.style.display = 'block';
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 3000);
}

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('consultaForm').addEventListener('submit', consultarPertenencias);
});

// Exportar funciones para uso global
window.generarReporte = generarReporte; 