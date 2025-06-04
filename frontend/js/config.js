const API_URL = 'http://localhost:5000';
const IA_URL = 'http://localhost:8000';
const REPORTES_URL = 'http://localhost:3000';

export const API_CONFIG = {
    BASE_URL: API_URL,
    IA_URL: IA_URL,
    REPORTES_URL: REPORTES_URL,
    AUTH: {
        LOGIN_ADMIN: `${API_URL}/login/administrador`,
        LOGIN_PERSONAL: `${API_URL}/login/personal`,
        REGISTRO: `${API_URL}/registro`,
        USUARIOS: `${API_URL}/usuarios`
    },
    PERTENENCIAS: {
        CONSULTAR: `${API_URL}/pertenencia/consultar-pertenencias-estudiante-busqueda`,
        REGISTRAR: `${API_URL}/pertenencia/registrar`,
        ACTUALIZAR: `${API_URL}/pertenencia/actualizar`,
        ELIMINAR: `${API_URL}/pertenencia/eliminar`
    },
    IA: {
        DETECTAR_ROSTRO: `${IA_URL}/detectar-rostro`,
        VERIFICAR_IDENTIDAD: `${IA_URL}/verificar-identidad`
    },
    REPORTES: {
        GENERAR_REPORTE: `${REPORTES_URL}/generar-reporte`,
        LISTAR_REPORTES: `${REPORTES_URL}/listar-reportes`
    }
};

// Función para construir URLs completas
function getApiUrl(endpoint) {
    return API_CONFIG.BASE_URL + endpoint;
}

// Función para manejar las peticiones al backend
async function fetchApi(endpoint, options = {}) {
    const token = localStorage.getItem('token');

    const defaultHeaders = {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
    };

    // Si hay FormData, no establecer Content-Type
    if (options.body instanceof FormData) {
        delete defaultHeaders['Content-Type'];
    }

    const config = {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers
        }
    };

    try {
        const response = await fetch(getApiUrl(endpoint), config);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Error en la petición');
        }

        return data;
    } catch (error) {
        console.error('Error en la petición:', error);
        throw error;
    }
}

// Función helper para formatear fechas
function formatDate(date) {
    return new Intl.DateTimeFormat('es-PE', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    }).format(date);
}

// Exportar las funciones y configuración
export { API_CONFIG, getApiUrl, fetchApi, formatDate }; 