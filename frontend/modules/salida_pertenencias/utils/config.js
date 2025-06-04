import { API_CONFIG as GlobalConfig } from '../../../js/config.js';

export const API_CONFIG = {
    ...GlobalConfig,
    SALIDA: {
        REGISTRAR: `${GlobalConfig.BASE_URL}/pertenencia/registrar-salida`,
        VERIFICAR: `${GlobalConfig.BASE_URL}/pertenencia/verificar-salida`,
        ACTUALIZAR_ESTADO: `${GlobalConfig.BASE_URL}/pertenencia/actualizar-estado`
    }
};

const API_URL = 'http://localhost:5000';






// ngrok http http://localhost:5000 --host-header="localhost:5000"