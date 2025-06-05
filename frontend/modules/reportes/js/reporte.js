import config from '../../../shared/config/config.js';
import { SessionManager } from '../../../shared/utils/sessionManager.js';

document.addEventListener('DOMContentLoaded', async () => {
    // Configuración común para las gráficas
    const chartConfig = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    padding: 20,
                    font: {
                        size: 12,
                        family: "'Segoe UI', sans-serif"
                    }
                }
            },
            title: {
                display: false
            }
        }
    };

    // Colores para las gráficas
    const colors = {
        blue: '#1a73e8',
        green: '#34a853',
        yellow: '#fbbc04',
        red: '#ea4335',
        purple: '#673ab7',
        teal: '#009688'
    };

    // Configurar gráfica de tipos de objetos
    const objectTypeChart = new Chart(
        document.getElementById('objectTypeChart').getContext('2d'),
        {
            type: 'bar',
            data: {
                labels: [],
                datasets: [{
                    data: [],
                    backgroundColor: Object.values(colors),
                    borderColor: 'white',
                    borderWidth: 2
                }]
            },
            options: {
                ...chartConfig,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        }
    );

    // Configurar gráfica de estado de pertenencias
    const statusPieChart = new Chart(
        document.getElementById('statusPieChart').getContext('2d'),
        {
            type: 'doughnut',
            data: {
                labels: ['Ingresada', 'Salida', 'Extraviada'],
                datasets: [{
                    data: [0, 0, 0],
                    backgroundColor: [colors.blue, colors.green, colors.yellow],
                    borderColor: 'white',
                    borderWidth: 2
                }]
            },
            options: {
                ...chartConfig,
                cutout: '60%'
            }
        }
    );

    async function fetchData(method = 'GET', filters = {}) {
        const token = localStorage.getItem('token');
        let url = `${config.API_URL}/api/pertenencia/consulta-reporte`;

        if (method === 'GET') {
            const params = new URLSearchParams(filters);
            url += `?${params.toString()}`;
        }

        const response = await fetch(url, {
            method: method,
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
                'X-User-Role': 'personal'
            },
            body: method === 'POST' ? JSON.stringify(filters) : undefined
        });

        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = '../../login_personal/pages/index.html';
                return;
            }
            throw new Error('Error al obtener los datos');
        }

        return await response.json();
    }

    // Función para actualizar los datos
    async function updateCharts() {
        try {
            const data = await fetchData();

            if (data.status === 'success' && data.pertenencias) {
                // Procesar datos para la gráfica de tipos
                const typeCount = {};
                data.pertenencias.forEach(item => {
                    const type = item.tipo || 'Sin clasificar';
                    typeCount[type] = (typeCount[type] || 0) + 1;
                });

                objectTypeChart.data.labels = Object.keys(typeCount);
                objectTypeChart.data.datasets[0].data = Object.values(typeCount);
                objectTypeChart.update();

                // Procesar datos para la gráfica de estado
                const statusCount = {
                    'Ingresada': 0,
                    'Salida': 0,
                    'Extraviada': 0
                };

                data.pertenencias.forEach(item => {
                    if (statusCount.hasOwnProperty(item.estado)) {
                        statusCount[item.estado]++;
                    }
                });

                statusPieChart.data.datasets[0].data = [
                    statusCount['Ingresada'],
                    statusCount['Salida'],
                    statusCount['Extraviada']
                ];
                statusPieChart.update();

                // Actualizar tabla de resumen
                updateSummaryTable(data.pertenencias);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    // Función para actualizar la tabla de resumen
    function updateSummaryTable(pertenencias) {
        const tbody = document.querySelector('tbody');
        tbody.innerHTML = '';

        // Agrupar por fecha
        const groupedByDate = {};
        pertenencias.forEach(item => {
            const date = new Date(item.fecha_registro).toLocaleDateString();
            if (!groupedByDate[date]) {
                groupedByDate[date] = {
                    ingresados: 0,
                    salidos: 0,
                    extraviados: 0
                };
            }

            switch (item.estado) {
                case 'Ingresada':
                    groupedByDate[date].ingresados++;
                    break;
                case 'Salida':
                    groupedByDate[date].salidos++;
                    break;
                case 'Extraviada':
                    groupedByDate[date].extraviados++;
                    break;
            }
        });

        // Ordenar fechas de más reciente a más antigua
        const sortedDates = Object.keys(groupedByDate).sort((a, b) =>
            new Date(b) - new Date(a)
        );

        // Crear filas de la tabla
        sortedDates.forEach(date => {
            const row = document.createElement('tr');
            const data = groupedByDate[date];
            const total = data.ingresados + data.salidos + data.extraviados;

            row.innerHTML = `
                <td>${date}</td>
                <td>${data.ingresados}</td>
                <td>${data.salidos}</td>
                <td>${data.extraviados}</td>
                <td>${total}</td>
            `;
            tbody.appendChild(row);
        });
    }

    // Actualizar datos inicialmente
    updateCharts();

    // Actualizar cada 5 minutos
    setInterval(updateCharts, 300000);

    // Configurar botones de descarga
    document.getElementById('downloadPagePdf').addEventListener('click', async () => {
        const element = document.getElementById('main');
        const opt = {
            margin: 1,
            filename: 'reporte.pdf',
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { scale: 2 },
            jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
        };

        try {
            await html2pdf().set(opt).from(element).save();
        } catch (error) {
            console.error('Error al generar PDF:', error);
            alert('Error al generar el PDF. Por favor, intente nuevamente.');
        }
    });

    window.fetchExcelFile = async function () {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`${config.API_URL}/api/pertenencia/descargar-excel`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'X-User-Role': 'personal'
                }
            });

            if (!response.ok) {
                if (response.status === 401) {
                    window.location.href = '../../login_personal/pages/index.html';
                    return;
                }
                throw new Error('Error al descargar el archivo Excel');
            }

            // Obtener el nombre del archivo del header Content-Disposition si existe
            const contentDisposition = response.headers.get('Content-Disposition');
            let filename = 'reporte.csv';
            if (contentDisposition) {
                const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
                if (filenameMatch && filenameMatch[1]) {
                    filename = filenameMatch[1].replace(/['"]/g, '');
                }
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();

            // Limpiar
            setTimeout(() => {
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            }, 100);
        } catch (error) {
            console.error('Error:', error);
            alert('Error al descargar el archivo. Por favor, intente nuevamente.');
        }
    };

    // Función para regresar a la página anterior
    window.goBack = function () {
        window.history.back();
    };

    // Función para cerrar sesión
    window.logout = function () {
        localStorage.removeItem('token');
        window.location.href = '../../login_personal/pages/index.html';
    };
});

