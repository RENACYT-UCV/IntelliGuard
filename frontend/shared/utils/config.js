const API_URL = 'http://localhost:5000';

// Configuración de la API
const API_CONFIG = {
    BASE_URL: API_URL,
    IA_URL: `${API_URL}/ia`,
    IA: {
        ENTRENAR_MODELO: `${API_URL}/ia/entrenar-modelo`,
        REGISTRAR_ROSTRO: `${API_URL}/ia/registrar-rostro`,
        VERIFICAR_ROSTRO: `${API_URL}/ia/verificar-rostro`,
        COMPARAR_ROSTROS: `${API_URL}/ia/comparar-rostros`,
        OBTENER_SIMILITUD: `${API_URL}/ia/obtener-similitud`,
        ACTUALIZAR_MODELO: `${API_URL}/ia/actualizar-modelo`
    },
    ESTUDIANTE: {
        REGISTRAR: `${API_URL}/estudiante/registrar`,
        VERIFICAR: `${API_URL}/estudiante/verificar`,
        ACTUALIZAR: `${API_URL}/estudiante/actualizar`,
        RECONOCIMIENTO_FACIAL: `${API_URL}/estudiante/reconocimiento-facial/video`
    },
    PERTENENCIA: {
        REGISTRAR: `${API_URL}/pertenencia/nueva-pertenencia`,
        REGISTRAR_INGRESO: `${API_URL}/pertenencia/registrar-ingreso-pertenencia`,
        VERIFICAR: `${API_URL}/pertenencia/verificar`
    },
    AUTH: {
        LOGIN: `${API_URL}/auth/login`,
        VERIFY: `${API_URL}/auth/verify`
    }
}; 