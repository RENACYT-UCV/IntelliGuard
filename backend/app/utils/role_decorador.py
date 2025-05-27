from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify
from ..models.usuario import BaseDatosUsuarios

from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_user_id = get_jwt_identity()
            base_datos_usuarios = BaseDatosUsuarios()
            user = base_datos_usuarios.consultar_usuario_por_id(current_user_id)
            
            if not user or user.rol != required_role:
                return jsonify({'error': 'No tienes permisos para realizar esta acción'}), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator