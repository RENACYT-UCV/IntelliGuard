import { API_CONFIG as GlobalConfig } from '../../../js/config.js';

export const API_CONFIG = {
    ...GlobalConfig,
    IA: {
        ...GlobalConfig.IA,
        ENTRENAR_MODELO: `${GlobalConfig.IA_URL}/entrenar-modelo`,
        REGISTRAR_ROSTRO: `${GlobalConfig.IA_URL}/registrar-rostro`,
        VERIFICAR_ROSTRO: `${GlobalConfig.IA_URL}/verificar-rostro`,
        COMPARAR_ROSTROS: `${GlobalConfig.IA_URL}/comparar-rostros`,
        OBTENER_SIMILITUD: `${GlobalConfig.IA_URL}/obtener-similitud`,
        ACTUALIZAR_MODELO: `${GlobalConfig.IA_URL}/actualizar-modelo`
    },
    ESTUDIANTE: {
        REGISTRAR: `${GlobalConfig.BASE_URL}/estudiante/registrar`,
        VERIFICAR: `${GlobalConfig.BASE_URL}/estudiante/verificar`,
        ACTUALIZAR: `${GlobalConfig.BASE_URL}/estudiante/actualizar`
    }
};






// ngrok http http://localhost:5000 --host-header="localhost:5000"