const config = {
    // URL base de la API
    API_URL: 'http://127.0.0.1:5000',

    // Rutas de la API
    API_ROUTES: {
        // Autenticación
        LOGIN: '/auth/login',
        LOGOUT: '/auth/logout',
        REFRESH_TOKEN: '/auth/refresh',

        // Estudiantes
        ESTUDIANTES: '/estudiantes',
        ESTUDIANTE_DETALLE: (id) => `/estudiantes/${id}`,

        // Pertenencias
        PERTENENCIAS: '/pertenencias',
        PERTENENCIA_DETALLE: (id) => `/pertenencias/${id}`,
        REGISTRAR_ENTRADA: '/pertenencias/entrada',
        REGISTRAR_SALIDA: '/pertenencias/salida',

        // Reconocimiento
        RECONOCIMIENTO_FACIAL: '/reconocimiento/facial',
        DETECCION_OBJETOS: '/reconocimiento/objetos',

        // Reportes
        GENERAR_REPORTE: '/reportes/generar',
        CONSULTAR_REPORTE: '/reportes/consultar',
    },

    // Configuración de la cámara
    CAMERA: {
        WIDTH: 640,
        HEIGHT: 480,
        FACING_MODE: 'user',
    },

    // Configuración de la interfaz
    UI: {
        ITEMS_PER_PAGE: 10,
        DATE_FORMAT: 'DD/MM/YYYY HH:mm:ss',
        THEME: {
            PRIMARY_COLOR: '#1976d2',
            SECONDARY_COLOR: '#dc004e',
            SUCCESS_COLOR: '#4caf50',
            ERROR_COLOR: '#f44336',
        },
    },

    // Configuración de almacenamiento local
    STORAGE: {
        TOKEN_KEY: 'token',
        USER_KEY: 'user',
        PREFERENCES_KEY: 'preferences',
    },

    // Timeouts y reintentos
    TIMEOUTS: {
        API_REQUEST: 30000, // 30 segundos
        CAMERA_INIT: 5000,  // 5 segundos
        TOKEN_REFRESH: 300000, // 5 minutos
    },

    // Mensajes de error
    ERROR_MESSAGES: {
        NETWORK_ERROR: 'Error de conexión. Por favor, verifica tu conexión a internet.',
        AUTH_ERROR: 'Error de autenticación. Por favor, inicia sesión nuevamente.',
        CAMERA_ERROR: 'Error al acceder a la cámara. Por favor, verifica los permisos.',
        UNKNOWN_ERROR: 'Ha ocurrido un error inesperado. Por favor, intenta nuevamente.',
    },
};

export default config; 