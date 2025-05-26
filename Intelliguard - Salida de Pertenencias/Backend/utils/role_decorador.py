from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify
from models.usuario import BaseDatosUsuarios

from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity

def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            claims = get_jwt()

            # Aquí consultas el rol desde la base de datos
            base_datos_usuarios = BaseDatosUsuarios("basededatos.db")
            usuario_db = base_datos_usuarios.consultar_usuario_por_usuario(current_user)

            if not usuario_db or usuario_db.rol not in roles:
                return jsonify({"msg": "No tienes permiso para acceder a esta ruta"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator