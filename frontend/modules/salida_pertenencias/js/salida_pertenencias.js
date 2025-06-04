import { API_CONFIG, fetchApi } from '../../../js/config.js';
import { checkAuth } from '../../../js/auth.js';

document.addEventListener('DOMContentLoaded', async () => {
    // Verificar autenticación
    await checkAuth();

    // Referencias a elementos del DOM
    const searchInput = document.getElementById('searchInput');
    const pertenenciasContainer = document.getElementById('pertenenciasContainer');
    const salidaForm = document.getElementById('salidaForm');

    let selectedPertenencia = null;

    // Función para buscar pertenencias
    async function searchPertenencias(query) {
        try {
            const response = await fetchApi(`${API_CONFIG.ENDPOINTS.BUSCAR_PERTENENCIAS}?query=${query}`, {
                method: 'GET'
            });

            renderPertenencias(response.pertenencias);
        } catch (error) {
            console.error('Error al buscar pertenencias:', error);
            showError('Error al buscar pertenencias');
        }
    }

    // Función para renderizar las pertenencias
    function renderPertenencias(pertenencias) {
        pertenenciasContainer.innerHTML = '';

        if (pertenencias.length === 0) {
            pertenenciasContainer.innerHTML = '<p class="no-results">No se encontraron pertenencias</p>';
            return;
        }

        pertenencias.forEach(pertenencia => {
            const card = document.createElement('div');
            card.className = 'pertenencia-card';
            card.innerHTML = `
                <img src="${pertenencia.imagen || '../../assets/default-item.png'}" alt="${pertenencia.nombre}" class="pertenencia-imagen">
                <div class="pertenencia-info">
                    <h3>${pertenencia.nombre}</h3>
                    <p><strong>Código:</strong> ${pertenencia.codigo}</p>
                    <p><strong>Estado:</strong> <span class="estado-${pertenencia.estado.toLowerCase()}">${pertenencia.estado}</span></p>
                    <p><strong>Propietario:</strong> ${pertenencia.propietario}</p>
                </div>
                <div class="pertenencia-actions">
                    <button class="btn-seleccionar" data-id="${pertenencia.id}">Seleccionar</button>
                </div>
            `;

            // Agregar event listener al botón de seleccionar
            const selectButton = card.querySelector('.btn-seleccionar');
            selectButton.addEventListener('click', () => {
                // Deseleccionar la pertenencia anterior si existe
                const prevSelected = document.querySelector('.pertenencia-card.selected');
                if (prevSelected) {
                    prevSelected.classList.remove('selected');
                }

                // Seleccionar la nueva pertenencia
                card.classList.add('selected');
                selectedPertenencia = pertenencia;

                // Mostrar el formulario de salida
                salidaForm.style.display = 'block';
                document.getElementById('pertenenciaId').value = pertenencia.id;
                document.getElementById('pertenenciaNombre').textContent = pertenencia.nombre;
                document.getElementById('pertenenciaCodigo').textContent = pertenencia.codigo;
            });

            pertenenciasContainer.appendChild(card);
        });
    }

    // Event listener para la búsqueda
    searchInput.addEventListener('input', debounce((e) => {
        const query = e.target.value.trim();
        if (query.length >= 2) {
            searchPertenencias(query);
        } else {
            pertenenciasContainer.innerHTML = '<p class="search-prompt">Ingrese al menos 2 caracteres para buscar</p>';
        }
    }, 300));

    // Event listener para el formulario de salida
    salidaForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!selectedPertenencia) {
            showError('Por favor, seleccione una pertenencia');
            return;
        }

        const formData = new FormData(e.target);
        const salidaData = {
            pertenencia_id: formData.get('pertenenciaId'),
            motivo: formData.get('motivo'),
            destino: formData.get('destino'),
            fecha_estimada_retorno: formData.get('fechaRetorno'),
            notas: formData.get('notas')
        };

        try {
            await fetchApi(API_CONFIG.ENDPOINTS.REGISTRAR_SALIDA, {
                method: 'POST',
                body: JSON.stringify(salidaData)
            });

            // Mostrar mensaje de éxito
            showSuccess('Salida registrada exitosamente');

            // Limpiar el formulario y la selección
            salidaForm.reset();
            salidaForm.style.display = 'none';
            selectedPertenencia = null;
            const selectedCard = document.querySelector('.pertenencia-card.selected');
            if (selectedCard) {
                selectedCard.classList.remove('selected');
            }

            // Limpiar la búsqueda
            searchInput.value = '';
            pertenenciasContainer.innerHTML = '<p class="search-prompt">Ingrese al menos 2 caracteres para buscar</p>';

        } catch (error) {
            console.error('Error al registrar salida:', error);
            showError('Error al registrar la salida');
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

    // Función helper para mostrar mensajes de éxito
    function showSuccess(message) {
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.textContent = message;
        document.body.appendChild(successDiv);
        setTimeout(() => successDiv.remove(), 3000);
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

    // Inicialización
    pertenenciasContainer.innerHTML = '<p class="search-prompt">Ingrese al menos 2 caracteres para buscar</p>';
}); 