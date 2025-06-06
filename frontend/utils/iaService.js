// Servicio para manejar las llamadas a la IA
class IAService {
    // Reconocimiento Facial
    static async capturarRostro(codigoEstudiante) {
        try {
            const response = await fetch(`${IA_URL}/ia/reconocimiento/capturar`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ codigo_estudiante: codigoEstudiante })
            });

            if (!response.ok) {
                throw new Error('Error al capturar rostro');
            }

            return await response.json();
        } catch (error) {
            console.error('Error en IAService:', error);
            throw error;
        }
    }

    static async verificarRostro(imagenBase64) {
        try {
            const response = await fetch(`${IA_URL}/ia/reconocimiento/verificar`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ imagen: imagenBase64 })
            });

            if (!response.ok) {
                throw new Error('Error al verificar rostro');
            }

            return await response.json();
        } catch (error) {
            console.error('Error en IAService:', error);
            throw error;
        }
    }

    // Gestión de Pertenencias
    static async registrarPertenencia(codigoEstudiante, tipoObjeto, descripcion) {
        try {
            const response = await fetch(`${IA_URL}/ia/pertenencias/registrar`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({
                    codigo_estudiante: codigoEstudiante,
                    tipo_objeto: tipoObjeto,
                    descripcion: descripcion
                })
            });

            if (!response.ok) {
                throw new Error('Error al registrar pertenencia');
            }

            return await response.json();
        } catch (error) {
            console.error('Error en IAService:', error);
            throw error;
        }
    }

    static async consultarPertenencias(codigoEstudiante) {
        try {
            const response = await fetch(`${IA_URL}/ia/pertenencias/consultar?codigo_estudiante=${codigoEstudiante}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });

            if (!response.ok) {
                throw new Error('Error al consultar pertenencias');
            }

            return await response.json();
        } catch (error) {
            console.error('Error en IAService:', error);
            throw error;
        }
    }

    // Detección de Objetos
    static async detectarObjetos(imagenBase64) {
        try {
            const response = await fetch(`${IA_URL}/ia/objetos/detectar`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ imagen: imagenBase64 })
            });

            if (!response.ok) {
                throw new Error('Error al detectar objetos');
            }

            return await response.json();
        } catch (error) {
            console.error('Error en IAService:', error);
            throw error;
        }
    }
}

// Exportar el servicio
window.IAService = IAService; 