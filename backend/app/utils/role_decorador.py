from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify
from ..models.usuario import BaseDatosUsuarios

def role_required(required_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            
            # Si required_roles es una cadena, convertirla en lista
            roles_list = [required_roles] if isinstance(required_roles, str) else required_roles
            
            if claims.get('rol') not in roles_list:
                return jsonify({'error': 'No tienes permisos para realizar esta acción', 'status': 'error'}), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator