import { API_CONFIG, fetchApi } from '../utils/config.js';
import { getToken } from '../utils/sessionManager.js';
import { checkAuth } from '../utils/auth.js';

class ConsultaPertenencias {
    constructor() {
        this.currentView = 'grid';
        this.currentPage = 1;
        this.itemsPerPage = 12;
        this.totalItems = 0;
        this.currentData = [];

        // Elementos del DOM
        this.searchInput = document.getElementById('searchInput');
        this.filterSelect = document.getElementById('filterSelect');
        this.viewToggleGrid = document.getElementById('viewToggleGrid');
        this.viewToggleList = document.getElementById('viewToggleList');
        this.pertenenciasContainer = document.getElementById('pertenenciasContainer');
        this.exportButton = document.getElementById('exportButton');
        this.paginationContainer = document.getElementById('pagination');

        this.init();
    }

    async init() {
        await checkAuth();
        this.setupEventListeners();
        await this.loadPertenencias();
    }

    setupEventListeners() {
        // Formulario de consulta básica
        const consultaForm = document.getElementById('consultaForm');
        if (consultaForm) {
            consultaForm.addEventListener('submit', (e) => this.consultarPertenencias(e));
        }

        // Elementos de vista avanzada
        if (this.viewToggleGrid) {
            this.viewToggleGrid.addEventListener('click', () => this.cambiarVista('grid'));
            this.viewToggleList.addEventListener('click', () => this.cambiarVista('list'));
        }

        if (this.searchInput) {
            this.searchInput.addEventListener('input', this.debounce(() => {
                this.currentPage = 1;
                this.loadPertenencias(1, this.filterSelect.value, this.searchInput.value);
            }, 300));
        }

        if (this.filterSelect) {
            this.filterSelect.addEventListener('change', () => {
                this.currentPage = 1;
                this.loadPertenencias(1, this.filterSelect.value, this.searchInput.value);
            });
        }
    }

    async consultarPertenencias(event) {
        if (event) event.preventDefault();

        const formData = new FormData(document.getElementById('consultaForm'));

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
            this.mostrarResultadosBasicos(data.pertenencias);
        } catch (error) {
            console.error('Error:', error);
            this.mostrarError('Error al consultar las pertenencias');
        }
    }

    async loadPertenencias(page = 1, filter = '', search = '') {
        try {
            const response = await fetchApi(`${API_CONFIG.ENDPOINTS.CONSULTA_PERTENENCIAS}?page=${page}&filter=${filter}&search=${search}`, {
                method: 'GET'
            });

            this.currentData = response.pertenencias;
            this.totalItems = response.total;
            this.renderPertenencias(this.currentData);
            this.renderPagination();
        } catch (error) {
            console.error('Error al cargar pertenencias:', error);
            this.mostrarError('Error al cargar las pertenencias');
        }
    }

    mostrarResultadosBasicos(pertenencias) {
        const resultadosDiv = document.getElementById('resultados');
        if (!resultadosDiv) return;

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
            tr.innerHTML = `
                <td>${pertenencia.codigo}</td>
                <td>${pertenencia.estudiante}</td>
                <td>${pertenencia.descripcion}</td>
                <td>${pertenencia.estado}</td>
                <td>${new Date(pertenencia.fecha).toLocaleString()}</td>
                <td>
                    <button onclick="consultaPertenencias.generarReporte('${pertenencia.id}')" class="btn-reporte">
                        Generar Reporte
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
        tabla.appendChild(tbody);

        resultadosDiv.appendChild(tabla);
    }

    renderPertenencias(pertenencias) {
        if (!this.pertenenciasContainer) return;

        this.pertenenciasContainer.innerHTML = '';

        if (this.currentView === 'grid') {
            this.renderGridView(pertenencias);
        } else {
            this.renderListView(pertenencias);
        }

        // Agregar event listeners a los botones de detalles
        document.querySelectorAll('.btn-detalles').forEach(btn => {
            btn.addEventListener('click', () => this.mostrarDetalles(btn.dataset.id));
        });
    }

    renderGridView(pertenencias) {
        this.pertenenciasContainer.classList.add('grid-view');
        this.pertenenciasContainer.classList.remove('list-view');

        pertenencias.forEach(pertenencia => {
            const card = document.createElement('div');
            card.className = 'pertenencia-card';
            card.innerHTML = `
                <img src="${pertenencia.imagen || '../../assets/default-item.png'}" alt="${pertenencia.nombre}" class="pertenencia-imagen">
                <div class="pertenencia-info">
                    <h3>${pertenencia.nombre}</h3>
                    <p><strong>Código:</strong> ${pertenencia.codigo}</p>
                    <p><strong>Estado:</strong> <span class="estado-${pertenencia.estado.toLowerCase()}">${pertenencia.estado}</span></p>
                    <p><strong>Fecha:</strong> ${new Date(pertenencia.fecha_registro).toLocaleDateString()}</p>
                </div>
                <div class="pertenencia-actions">
                    <button class="btn-detalles" data-id="${pertenencia.id}">Ver Detalles</button>
                </div>
            `;
            this.pertenenciasContainer.appendChild(card);
        });
    }

    renderListView(pertenencias) {
        this.pertenenciasContainer.classList.add('list-view');
        this.pertenenciasContainer.classList.remove('grid-view');

        const table = document.createElement('table');
        table.className = 'pertenencias-table';
        table.innerHTML = `
            <thead>
                <tr>
                    <th>Código</th>
                    <th>Nombre</th>
                    <th>Estado</th>
                    <th>Fecha Registro</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                ${pertenencias.map(pertenencia => `
                    <tr>
                        <td>${pertenencia.codigo}</td>
                        <td>${pertenencia.nombre}</td>
                        <td><span class="estado-${pertenencia.estado.toLowerCase()}">${pertenencia.estado}</span></td>
                        <td>${new Date(pertenencia.fecha_registro).toLocaleDateString()}</td>
                        <td>
                            <button class="btn-detalles" data-id="${pertenencia.id}">Ver Detalles</button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        `;
        this.pertenenciasContainer.appendChild(table);
    }

    async mostrarDetalles(id) {
        try {
            const pertenencia = await fetchApi(`${API_CONFIG.ENDPOINTS.PERTENENCIA_DETALLES}/${id}`, {
                method: 'GET'
            });

            const modal = document.createElement('div');
            modal.className = 'modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <span class="close">&times;</span>
                    <h2>Detalles de la Pertenencia</h2>
                    <div class="detalles-grid">
                        <div class="detalle-imagen">
                            <img src="${pertenencia.imagen || '../../assets/default-item.png'}" alt="${pertenencia.nombre}">
                        </div>
                        <div class="detalle-info">
                            <p><strong>Nombre:</strong> ${pertenencia.nombre}</p>
                            <p><strong>Código:</strong> ${pertenencia.codigo}</p>
                            <p><strong>Estado:</strong> <span class="estado-${pertenencia.estado.toLowerCase()}">${pertenencia.estado}</span></p>
                            <p><strong>Fecha de Registro:</strong> ${new Date(pertenencia.fecha_registro).toLocaleDateString()}</p>
                            <p><strong>Descripción:</strong> ${pertenencia.descripcion}</p>
                            <p><strong>Propietario:</strong> ${pertenencia.propietario}</p>
                            <p><strong>Ubicación:</strong> ${pertenencia.ubicacion}</p>
                        </div>
                    </div>
                    <div class="historial-section">
                        <h3>Historial de Movimientos</h3>
                        <table class="historial-table">
                            <thead>
                                <tr>
                                    <th>Fecha</th>
                                    <th>Acción</th>
                                    <th>Usuario</th>
                                    <th>Notas</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${pertenencia.historial.map(h => `
                                    <tr>
                                        <td>${new Date(h.fecha).toLocaleString()}</td>
                                        <td>${h.accion}</td>
                                        <td>${h.usuario}</td>
                                        <td>${h.notas || '-'}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            `;

            document.body.appendChild(modal);

            modal.querySelector('.close').addEventListener('click', () => {
                modal.remove();
            });

            window.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.remove();
                }
            });
        } catch (error) {
            console.error('Error al cargar detalles:', error);
            this.mostrarError('Error al cargar los detalles de la pertenencia');
        }
    }

    async generarReporte(idRegistro) {
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
            this.mostrarError('Error al generar el reporte');
        }
    }

    renderPagination() {
        if (!this.paginationContainer) return;

        const totalPages = Math.ceil(this.totalItems / this.itemsPerPage);
        this.paginationContainer.innerHTML = '';

        if (totalPages <= 1) return;

        // Botón anterior
        const prevButton = document.createElement('button');
        prevButton.innerHTML = '&laquo;';
        prevButton.disabled = this.currentPage === 1;
        prevButton.addEventListener('click', () => {
            if (this.currentPage > 1) {
                this.currentPage--;
                this.loadPertenencias(this.currentPage, this.filterSelect.value, this.searchInput.value);
            }
        });
        this.paginationContainer.appendChild(prevButton);

        // Páginas
        for (let i = 1; i <= totalPages; i++) {
            const pageButton = document.createElement('button');
            pageButton.textContent = i;
            pageButton.classList.toggle('active', i === this.currentPage);
            pageButton.addEventListener('click', () => {
                this.currentPage = i;
                this.loadPertenencias(this.currentPage, this.filterSelect.value, this.searchInput.value);
            });
            this.paginationContainer.appendChild(pageButton);
        }

        // Botón siguiente
        const nextButton = document.createElement('button');
        nextButton.innerHTML = '&raquo;';
        nextButton.disabled = this.currentPage === totalPages;
        nextButton.addEventListener('click', () => {
            if (this.currentPage < totalPages) {
                this.currentPage++;
                this.loadPertenencias(this.currentPage, this.filterSelect.value, this.searchInput.value);
            }
        });
        this.paginationContainer.appendChild(nextButton);
    }

    mostrarError(mensaje) {
        const errorDiv = document.getElementById('error-message');
        if (!errorDiv) return;

        errorDiv.textContent = mensaje;
        errorDiv.style.display = 'block';
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 3000);
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    cambiarVista(vista) {
        this.currentView = vista;
        this.renderPertenencias(this.currentData);
    }
}

// Inicializar y exportar la instancia
const consultaPertenencias = new ConsultaPertenencias();
export default consultaPertenencias; 