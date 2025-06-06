// Configuración de URLs
const API_URL = 'http://localhost:3000/api';  // URL del backend principal
const IA_URL = 'http://localhost:5000';       // URL del servicio de IA

// Configuración de endpoints
const ENDPOINTS = {
    // Endpoints de autenticación
    LOGIN_ADMIN: '/login/administrador',
    LOGIN_PERSONAL: '/login/personal',
    
    // Endpoints de IA
    RECONOCIMIENTO_CAPTURAR: '/ia/reconocimiento/capturar',
    RECONOCIMIENTO_VERIFICAR: '/ia/reconocimiento/verificar',
    PERTENENCIAS_REGISTRAR: '/ia/pertenencias/registrar',
    PERTENENCIAS_CONSULTAR: '/ia/pertenencias/consultar',
    OBJETOS_DETECTAR: '/ia/objetos/detectar'
};

// Exportar configuración
window.API_URL = API_URL;
window.IA_URL = IA_URL;
window.ENDPOINTS = ENDPOINTS;

// ngrok http http://localhost:5000 --host-header="localhost:5000"