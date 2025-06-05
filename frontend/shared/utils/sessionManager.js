// Constantes de sesión
const SESSION_KEYS = {
    TOKEN: 'token',
    ROLE: 'role',
    USER: 'username'
};

// Roles disponibles
export const ROLES = {
    ADMIN: 'admin',
    PERSONAL: 'personal'
};

// Rutas de la aplicación
const ROUTES = {
    LOGIN: '/index.html',
    MENU: '/frontend/modules/login_administrador/pages/menu.html'
};

// Clase para manejar la sesión
export class SessionManager {
    static setToken(token) {
        localStorage.setItem(SESSION_KEYS.TOKEN, token);
        const decodedToken = this.parseJwt(token);
        localStorage.setItem(SESSION_KEYS.USER, decodedToken.sub);
        localStorage.setItem(SESSION_KEYS.ROLE, decodedToken.rol.toLowerCase());
    }

    static getToken() {
        return localStorage.getItem(SESSION_KEYS.TOKEN);
    }

    static getRole() {
        return localStorage.getItem(SESSION_KEYS.ROLE);
    }

    static getUsername() {
        return localStorage.getItem(SESSION_KEYS.USER);
    }

    static isAuthenticated() {
        const token = this.getToken();
        if (!token) return false;

        try {
            const decodedToken = this.parseJwt(token);
            const currentTime = Date.now() / 1000;
            return decodedToken.exp > currentTime;
        } catch (e) {
            return false;
        }
    }

    static isAdmin() {
        return this.getRole() === ROLES.ADMIN;
    }

    static isPersonal() {
        return this.getRole() === ROLES.PERSONAL;
    }

    static clearSession() {
        localStorage.removeItem(SESSION_KEYS.TOKEN);
        localStorage.removeItem(SESSION_KEYS.ROLE);
        localStorage.removeItem(SESSION_KEYS.USER);
    }

    static parseJwt(token) {
        try {
            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const jsonPayload = decodeURIComponent(atob(base64).split('').map(c => {
                return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
            }).join(''));
            return JSON.parse(jsonPayload);
        } catch (e) {
            console.error('Error parsing JWT:', e);
            return null;
        }
    }

    static redirectToLogin() {
        window.location.href = ROUTES.LOGIN;
    }

    static redirectToMenu() {
        window.location.href = ROUTES.MENU;
    }

    static validateSession() {
        if (!this.isAuthenticated()) {
            this.clearSession();
            this.redirectToLogin();
            return false;
        }
        return true;
    }

    static validateAdminSession() {
        if (!this.validateSession() || !this.isAdmin()) {
            this.clearSession();
            this.redirectToLogin();
            return false;
        }
        return true;
    }

    static validatePersonalSession() {
        if (!this.validateSession() || !this.isPersonal()) {
            this.clearSession();
            this.redirectToLogin();
            return false;
        }
        return true;
    }

    static handleUnauthorized(response) {
        if (response.status === 403 || response.status === 401 || response.status === 422) {
            this.clearSession();
            this.redirectToLogin();
        }
    }
}

function validTokenSession() {
    var currentPage = window.location.pathname;
    if (currentPage !== '/index.html' && currentPage !== '/') {
        var jwtCookie = getCookie('jwt');
        var usernameCookie = getCookie('username');
        if (!jwtCookie || !usernameCookie) {
            logout();
        }
    }
}

function handleUnauthorized(response) {
    if (response.status === 403 || response.status === 401 || response.status === 422) {
        logout();
    }
}

function logout() {
    document.cookie = 'jwt=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 UTC; Secure; SameSite=Strict';
    document.cookie = 'username=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 UTC; Secure; SameSite=Strict';
    window.location.href = '/frontend/modules/login_administrador/pages/index.html';
}

function saveAuth(token, username) {
    document.cookie = `jwt=${token}; path=/; Secure; SameSite=Strict`;
    document.cookie = `username=${username}; path=/; Secure; SameSite=Strict`;
}

function getCookie(name) {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1, cookie.length);
        }
    }
    return null;
}

function menu() {
    window.location.href = '/frontend/modules/login_administrador/pages/menu.html';
} 