# Este archivo puede estar vacío 

from .auth_routes import auth_bp
from .estudiante_routes import estudiante_bp
from .pertenencia_routes import pertenencia_bp
from .reconocimiento_routes import reconocimiento_bp

__all__ = [
    'auth_bp',
    'estudiante_bp',
    'pertenencia_bp',
    'reconocimiento_bp'
] 