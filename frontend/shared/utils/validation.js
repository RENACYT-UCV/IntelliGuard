export class ValidationManager {
    static validateUsername(username) {
        if (!username || typeof username !== 'string') {
            return 'El nombre de usuario es requerido';
        }
        if (username.length < 3) {
            return 'El nombre de usuario debe tener al menos 3 caracteres';
        }
        return null;
    }

    static validatePassword(password) {
        if (!password || typeof password !== 'string') {
            return 'La contraseña es requerida';
        }
        if (password.length < 6) {
            return 'La contraseña debe tener al menos 6 caracteres';
        }
        return null;
    }

    static validateRole(role) {
        if (!role) {
            return 'El rol es requerido';
        }
        if (!['1', '2'].includes(role)) {
            return 'El rol seleccionado no es válido';
        }
        return null;
    }

    static validateForm(data) {
        const errors = {};

        if (data.username !== undefined) {
            const usernameError = this.validateUsername(data.username);
            if (usernameError) errors.username = usernameError;
        }

        if (data.password !== undefined) {
            const passwordError = this.validatePassword(data.password);
            if (passwordError) errors.password = passwordError;
        }

        if (data.role !== undefined) {
            const roleError = this.validateRole(data.role);
            if (roleError) errors.role = roleError;
        }

        return Object.keys(errors).length > 0 ? errors : null;
    }

    static validateStudentId(studentId) {
        if (!studentId || typeof studentId !== 'string') {
            return 'El ID del estudiante es requerido';
        }
        if (!/^\d+$/.test(studentId)) {
            return 'El ID del estudiante debe contener solo números';
        }
        return null;
    }

    static validateDate(date) {
        if (!date) {
            return 'La fecha es requerida';
        }
        const dateObj = new Date(date);
        if (isNaN(dateObj.getTime())) {
            return 'La fecha no es válida';
        }
        return null;
    }

    static validateDescription(description) {
        if (!description || typeof description !== 'string') {
            return 'La descripción es requerida';
        }
        if (description.length < 10) {
            return 'La descripción debe tener al menos 10 caracteres';
        }
        return null;
    }
} 