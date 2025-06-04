const API_URL = 'http://localhost:5000';

export const API_CONFIG = {
    BASE_URL: API_URL,
    AUTH: {
        LOGIN_ADMIN: `${API_URL}/login/administrador`,
    }
};

// ngrok http http://localhost:5000 --host-header="localhost:5000"