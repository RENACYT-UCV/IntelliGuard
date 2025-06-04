import { API_CONFIG, fetchApi } from '../../../js/config.js';
import { checkAuth } from '../../../js/auth.js';

document.addEventListener('DOMContentLoaded', async () => {
    // Verificar autenticación
    await checkAuth();

    // Referencias a elementos del DOM
    const searchInput = document.getElementById('searchInput');
    const filterSelect = document.getElementById('filterSelect');
    const viewToggleGrid = document.getElementById('viewToggleGrid');
    const viewToggleList = document.getElementById('viewToggleList');
    const pertenenciasContainer = document.getElementById('pertenenciasContainer');
    const exportButton = document.getElementById('exportButton');
    const paginationContainer = document.getElementById('pagination');

    let currentView = 'grid';
    let currentPage = 1;
    let itemsPerPage = 12;
    let totalItems = 0;
    let currentData = [];

    // Función para cargar las pertenencias
    async function loadPertenencias(page = 1, filter = '', search = '') {
        try {
            const response = await fetchApi(`${API_CONFIG.ENDPOINTS.CONSULTA_PERTENENCIAS}?page=${page}&filter=${filter}&search=${search}`, {
                method: 'GET'
            });

            currentData = response.pertenencias;
            totalItems = response.total;
            renderPertenencias(currentData);
            renderPagination();
        } catch (error) {
            console.error('Error al cargar pertenencias:', error);
            showError('Error al cargar las pertenencias');
        }
    }

    // Función para renderizar las pertenencias
    function renderPertenencias(pertenencias) {
        pertenenciasContainer.innerHTML = '';

        if (currentView === 'grid') {
            pertenenciasContainer.classList.add('grid-view');
            pertenenciasContainer.classList.remove('list-view');

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
                pertenenciasContainer.appendChild(card);
            });
        } else {
            pertenenciasContainer.classList.add('list-view');
            pertenenciasContainer.classList.remove('grid-view');

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
            pertenenciasContainer.appendChild(table);
        }

        // Agregar event listeners a los botones de detalles
        document.querySelectorAll('.btn-detalles').forEach(btn => {
            btn.addEventListener('click', () => mostrarDetalles(btn.dataset.id));
        });
    }

    // Función para mostrar detalles de una pertenencia
    async function mostrarDetalles(id) {
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
            showError('Error al cargar los detalles de la pertenencia');
        }
    }

    // Función para renderizar la paginación
    function renderPagination() {
        const totalPages = Math.ceil(totalItems / itemsPerPage);
        paginationContainer.innerHTML = '';

        if (totalPages <= 1) return;

        // Botón anterior
        const prevButton = document.createElement('button');
        prevButton.innerHTML = '&laquo;';
        prevButton.disabled = currentPage === 1;
        prevButton.addEventListener('click', () => {
            if (currentPage > 1) {
                currentPage--;
                loadPertenencias(currentPage, filterSelect.value, searchInput.value);
            }
        });
        paginationContainer.appendChild(prevButton);

        // Páginas
        for (let i = 1; i <= totalPages; i++) {
            const pageButton = document.createElement('button');
            pageButton.textContent = i;
            pageButton.classList.toggle('active', i === currentPage);
            pageButton.addEventListener('click', () => {
                currentPage = i;
                loadPertenencias(currentPage, filterSelect.value, searchInput.value);
            });
            paginationContainer.appendChild(pageButton);
        }

        // Botón siguiente
        const nextButton = document.createElement('button');
        nextButton.innerHTML = '&raquo;';
        nextButton.disabled = currentPage === totalPages;
        nextButton.addEventListener('click', () => {
            if (currentPage < totalPages) {
                currentPage++;
                loadPertenencias(currentPage, filterSelect.value, searchInput.value);
            }
        });
        paginationContainer.appendChild(nextButton);
    }

    // Event Listeners
    searchInput.addEventListener('input', debounce(() => {
        currentPage = 1;
        loadPertenencias(currentPage, filterSelect.value, searchInput.value);
    }, 300));

    filterSelect.addEventListener('change', () => {
        currentPage = 1;
        loadPertenencias(currentPage, filterSelect.value, searchInput.value);
    });

    viewToggleGrid.addEventListener('click', () => {
        currentView = 'grid';
        viewToggleGrid.classList.add('active');
        viewToggleList.classList.remove('active');
        renderPertenencias(currentData);
    });

    viewToggleList.addEventListener('click', () => {
        currentView = 'list';
        viewToggleList.classList.add('active');
        viewToggleGrid.classList.remove('active');
        renderPertenencias(currentData);
    });

    exportButton.addEventListener('click', async () => {
        try {
            const response = await fetchApi(API_CONFIG.ENDPOINTS.EXPORTAR_PERTENENCIAS, {
                method: 'POST',
                body: JSON.stringify({
                    filter: filterSelect.value,
                    search: searchInput.value
                })
            });

            // Crear y descargar el archivo
            const blob = new Blob([response.data], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `pertenencias_${new Date().toISOString().split('T')[0]}.csv`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            console.error('Error al exportar:', error);
            showError('Error al exportar las pertenencias');
        }
    });

    // Función helper para mostrar errores
    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        document.body.appendChild(errorDiv);
        setTimeout(() => errorDiv.remove(), 3000);
    }

    // Función helper para debounce
    function debounce(func, wait) {
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

    // Cargar pertenencias iniciales
    loadPertenencias();
}); 