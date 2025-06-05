const API_URL = 'http://localhost:5000';

export const API_CONFIG = {
    BASE_URL: API_URL,
    ENDPOINTS: {
        // Auth endpoints
        AUTH: {
            LOGIN_ADMIN: '/api/auth/admin/login',
            LOGIN_PERSONAL: '/api/auth/personal/login',
            LOGIN_ESTUDIANTE: '/api/auth/estudiante/login',
            REGISTRO: '/api/auth/registro',
            USUARIOS: '/api/auth/usuarios'
        },

        // Pertenencias endpoints
        PERTENENCIAS: {
            CONSULTAR: '/api/pertenencias/consultar-pertenencias-estudiante-busqueda',
            REGISTRAR: '/api/pertenencias/nueva-pertenencia',
            REGISTRAR_INGRESO: '/api/pertenencias/registrar-ingreso-pertenencia',
            REGISTRAR_SALIDA: '/api/pertenencias/registrar-salida-pertenencia',
            ACTUALIZAR: '/api/pertenencias/actualizar',
            ELIMINAR: '/api/pertenencias/eliminar',
            HISTORIAL: '/api/pertenencias/historial'
        },

        // IA endpoints
        IA: {
            DETECTAR_ROSTRO: '/api/reconocimiento/detectar-rostro',
            VERIFICAR_IDENTIDAD: '/api/reconocimiento/verificar-identidad',
            DETECTAR_OBJETO: '/api/reconocimiento/detectar-objeto'
        },

        // Reportes endpoints
        REPORTES: {
            CONSULTAR: '/api/reportes/consultar-reporte',
            DESCARGAR: '/api/reportes/descargar-excel'
        }
    }
};

// Función para manejar las peticiones al backend
async function fetchApi(endpoint, options = {}) {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');

    const defaultHeaders = {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...(role && { 'X-User-Role': role })
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
        const response = await fetch(API_URL + endpoint, config);
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
export { API_CONFIG, fetchApi, formatDate }; 