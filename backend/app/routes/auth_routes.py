from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from ..models.usuario import BaseDatosUsuarios
from ..utils.role_decorador import role_required
import bcrypt

auth_bp = Blueprint('auth', __name__)
base_datos_usuarios = BaseDatosUsuarios()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')
    contraseña = data.get('contraseña')
    
    user = base_datos_usuarios.consultar_usuario_por_usuario(usuario)
    
    if user and user.hash_contraseña == contraseña:  # En producción, usar hash seguro
        access_token = create_access_token(identity=user.id_usuario)
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id_usuario,
                'usuario': user.usuario,
                'rol': user.rol
            }
        }), 200
    
    return jsonify({'error': 'Credenciales inválidas'}), 401

@auth_bp.route('/login/personal', methods=['POST'])
def login_personal():
    try:
        data = request.get_json()
        usuario = data.get('usuario')
        contraseña = data.get('contraseña')
        
        if not usuario or not contraseña:
            return jsonify({
                'error': 'Usuario y contraseña son requeridos',
                'status': 'error'
            }), 400
        
        usuario_db = base_datos_usuarios.consultar_usuario_personal(usuario)
        if usuario_db and bcrypt.checkpw(contraseña.encode('utf-8'), usuario_db.hash_contraseña):
            additional_claims = {
                "rol": usuario_db.rol,
                "tipo": "personal"
            }
            access_token = create_access_token(identity=usuario, additional_claims=additional_claims)
            return jsonify({
                'access_token': access_token,
                'user': {
                    'id': usuario_db.id_usuario,
                    'usuario': usuario_db.usuario,
                    'rol': usuario_db.rol
                },
                'status': 'success'
            }), 200
        else:
            return jsonify({
                'error': 'Credenciales incorrectas',
                'status': 'error'
            }), 401
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@auth_bp.route('/login/administrador', methods=['POST'])
def login_administrador():
    try:
        data = request.get_json()
        usuario = data.get('usuario')
        contraseña = data.get('contraseña')
        
        if not usuario or not contraseña:
            return jsonify({
                'error': 'Usuario y contraseña son requeridos',
                'status': 'error'
            }), 400
        
        usuario_db = base_datos_usuarios.consultar_usuario_administrador(usuario)
        if usuario_db and bcrypt.checkpw(contraseña.encode('utf-8'), usuario_db.hash_contraseña):
            additional_claims = {
                "rol": usuario_db.rol,
                "tipo": "administrador"
            }
            access_token = create_access_token(identity=usuario, additional_claims=additional_claims)
            return jsonify({
                'access_token': access_token,
                'user': {
                    'id': usuario_db.id_usuario,
                    'usuario': usuario_db.usuario,
                    'rol': usuario_db.rol
                },
                'status': 'success'
            }), 200
        else:
            return jsonify({
                'error': 'Credenciales incorrectas',
                'status': 'error'
            }), 401
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@auth_bp.route('/registro', methods=['POST'])
@jwt_required()
@role_required('Administrador')
def registro():
    try:
        data = request.get_json()
        usuario = data.get('usuario')
        contraseña = data.get('contraseña')
        idRol = data.get('idRol')
        
        if not usuario or not contraseña or not idRol:
            return jsonify({
                'error': 'Usuario, contraseña y rol son requeridos',
                'status': 'error'
            }), 400
        
        if base_datos_usuarios.consultar_usuario_por_usuario(usuario):
            return jsonify({
                'error': 'El usuario ya existe',
                'status': 'error'
            }), 400
        
        hash_contraseña = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
        base_datos_usuarios.agregar_usuario(usuario, hash_contraseña, idRol)
        return jsonify({
            'mensaje': 'Usuario registrado exitosamente',
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@auth_bp.route('/usuarios', methods=['GET'])
@jwt_required()
@role_required('Administrador')
def listar_usuarios():
    try:
        usuarios = base_datos_usuarios.listar_usuarios()
        usuarios_json = []
        for usuario in usuarios:
            usuarios_json.append({
                'id': usuario.id_usuario,
                'usuario': usuario.usuario,
                'rol': usuario.rol
            })
        return jsonify({
            'usuarios': usuarios_json,
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@auth_bp.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
@jwt_required()
@role_required('Administrador')
def eliminar_usuario(id_usuario):
    try:
        # Verificar que no se pueda eliminar a sí mismo
        token_data = get_jwt()
        current_user = base_datos_usuarios.consultar_usuario_por_usuario(token_data['sub'])
        
        if current_user.id_usuario == id_usuario:
            return jsonify({
                'error': 'No puedes eliminar tu propio usuario',
                'status': 'error'
            }), 400
            
        base_datos_usuarios.eliminar_usuario(id_usuario)
        return jsonify({
            'mensaje': 'Usuario eliminado exitosamente',
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@auth_bp.route('/usuarios/<int:id_usuario>', methods=['PUT'])
@jwt_required()
@role_required('Administrador')
def editar_usuario(id_usuario):
    try:
        datos_usuario = request.json
        nuevo_usuario = datos_usuario.get('usuario')
        nueva_contraseña = datos_usuario.get('contraseña')
        nuevo_id_rol = datos_usuario.get('idRol')
        
        if not nuevo_usuario or not nuevo_id_rol:
            return jsonify({
                'error': 'Usuario y rol son requeridos',
                'status': 'error'
            }), 400
            
        # Si se proporciona una nueva contraseña, hashearla
        hash_contraseña = None
        if nueva_contraseña and nueva_contraseña.strip():
            hash_contraseña = bcrypt.hashpw(nueva_contraseña.encode('utf-8'), bcrypt.gensalt())
        
        base_datos_usuarios.editar_usuario(id_usuario, nuevo_usuario, hash_contraseña, nuevo_id_rol)
        return jsonify({
            'mensaje': 'Usuario editado exitosamente',
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

# Ruta para verificar el token y obtener información del usuario
@auth_bp.route('/verify-token', methods=['GET'])
@jwt_required()
def verify_token():
    try:
        token_data = get_jwt()
        current_user = base_datos_usuarios.consultar_usuario_por_usuario(token_data['sub'])
        
        return jsonify({
            'user': {
                'id': current_user.id_usuario,
                'usuario': current_user.usuario,
                'rol': current_user.rol
            },
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500
