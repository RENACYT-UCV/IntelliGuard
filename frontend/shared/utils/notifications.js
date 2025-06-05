export class NotificationManager {
    static TYPES = {
        SUCCESS: 'success',
        ERROR: 'danger',
        WARNING: 'warning',
        INFO: 'info'
    };

    static show(message, type = this.TYPES.INFO, duration = 3000) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Buscar el contenedor de mensajes o crear uno nuevo
        let messageContainer = document.getElementById('message-container');
        if (!messageContainer) {
            messageContainer = document.createElement('div');
            messageContainer.id = 'message-container';
            messageContainer.style.position = 'fixed';
            messageContainer.style.top = '20px';
            messageContainer.style.right = '20px';
            messageContainer.style.zIndex = '9999';
            document.body.appendChild(messageContainer);
        }

        messageContainer.appendChild(alertDiv);

        // Auto-cerrar después de la duración especificada
        setTimeout(() => {
            alertDiv.classList.remove('show');
            setTimeout(() => alertDiv.remove(), 150);
        }, duration);
    }

    static success(message, duration) {
        this.show(message, this.TYPES.SUCCESS, duration);
    }

    static error(message, duration) {
        this.show(message, this.TYPES.ERROR, duration);
    }

    static warning(message, duration) {
        this.show(message, this.TYPES.WARNING, duration);
    }

    static info(message, duration) {
        this.show(message, this.TYPES.INFO, duration);
    }

    // Método para mostrar errores de validación
    static showValidationErrors(errors) {
        if (typeof errors === 'string') {
            this.error(errors);
            return;
        }

        if (Array.isArray(errors)) {
            errors.forEach(error => this.error(error));
            return;
        }

        if (typeof errors === 'object') {
            Object.values(errors).forEach(error => this.error(error));
        }
    }
} 