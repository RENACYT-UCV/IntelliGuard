from functools import wraps
from typing import Union, List
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify, current_app
import logging

logger = logging.getLogger(__name__)

def role_required(required_roles: Union[str, List[str]]):
    """
    Decorador para proteger rutas basado en roles.
    
    Args:
        required_roles: Un rol o lista de roles requeridos para acceder a la ruta
        
    Returns:
        El decorador configurado
        
    Example:
        @role_required('admin')
        def admin_route():
            pass
            
        @role_required(['admin', 'personal'])
        def staff_route():
            pass
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                # Verificar JWT
                verify_jwt_in_request()
                claims = get_jwt()
                
                # Convertir required_roles a lista si es string
                roles_list = [required_roles] if isinstance(required_roles, str) else required_roles
                # Convertir a minúsculas para comparación
                roles_list = [r.lower() for r in roles_list]
                
                # Obtener el rol del usuario y convertir a minúsculas
                user_role = claims.get('rol', '').lower()
                
                # Verificar rol
                if user_role not in roles_list:
                    logger.warning(f"Intento de acceso no autorizado: Usuario con rol {claims.get('rol')} intentó acceder a ruta que requiere {roles_list}")
                    return jsonify({
                        'error': 'No tienes permisos para realizar esta acción',
                        'status': 'error'
                    }), 403
                
                return fn(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error en verificación de rol: {str(e)}")
                return jsonify({
                    'error': 'Error en la autenticación',
                    'status': 'error'
                }), 401
                
        return wrapper
    return decorator