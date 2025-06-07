function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
}

document.addEventListener('DOMContentLoaded', function() {
    const btnCargar = document.getElementById('btnCargarHistorial');
    const tablaBody = document.querySelector('#tablaHistorial tbody');

    btnCargar.onclick = function() {
        fetch(API_URL + '/ia/pertenencias/consultar', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + getCookie('jwt')
            }
        })
        .then(res => res.json())
        .then(data => {
            tablaBody.innerHTML = '';
            if (!Array.isArray(data) || data.length === 0) {
                tablaBody.innerHTML = '<tr><td colspan="5" class="text-center">No hay registros</td></tr>';
                return;
            }
            data.forEach(registro => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${registro.codigo_estudiante || ''}</td>
                    <td>${registro.tipo_objeto || ''}</td>
                    <td>${registro.fecha_entrada || ''}</td>
                    <td>${registro.fecha_salida || ''}</td>
                    <td>${registro.estado || ''}</td>
                `;
                tablaBody.appendChild(tr);
            });
        })
        .catch(err => {
            tablaBody.innerHTML = '<tr><td colspan="5" class="text-center">Error al cargar historial</td></tr>';
        });
    };

    document.getElementById('btnDescargarPDF').onclick = function() {
        fetch(API_URL + '/ia/pertenencias/reporte/pdf', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + getCookie('jwt')
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('No se pudo generar el PDF');
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'reporte_pertenencias.pdf';
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        })
        .catch(() => {
            alert('Error al descargar el PDF');
        });
    };
});

