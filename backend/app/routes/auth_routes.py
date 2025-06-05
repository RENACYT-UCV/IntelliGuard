from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from ..models.usuario import BaseDatosUsuarios
from ..utils.role_decorador import role_required
from ..models import Session
import bcrypt
import re

auth_bp = Blueprint('auth', __name__)

def get_db():
    """Obtiene una nueva sesión de la base de datos"""
    session = Session()
    try:
        return session
    except:
        session.rollback()
        raise
    finally:
        session.close()

def validar_credenciales_numericas(usuario: str, contraseña: str) -> bool:
    """Valida que las credenciales sean solo números y tengan 6 dígitos"""
    patron = re.compile(r'^\d{6}$')
    return patron.match(usuario) is not None and patron.match(contraseña) is not None

def validar_contraseña_numerica(contraseña: str) -> bool:
    """Valida que la contraseña sea solo números y tenga 6 dígitos"""
    patron = re.compile(r'^\d{6}$')
    return patron.match(contraseña) is not None

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')
    contraseña = data.get('contraseña')
    
    db = get_db()
    base_datos_usuarios = BaseDatosUsuarios(db)
    
    user = base_datos_usuarios.obtener_por_usuario(usuario)
    
    if user and bcrypt.checkpw(contraseña.encode('utf-8'), user.hash_contraseña.encode('utf-8')):
        access_token = create_access_token(identity=user.id_usuario)
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id_usuario,
                'usuario': user.usuario,
                'rol': user.rol.rol if user.rol else None
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
            
        # Validar que la contraseña sea numérica y tenga 6 dígitos
        if not validar_contraseña_numerica(contraseña):
            return jsonify({
                'error': 'La contraseña debe ser un número de 6 dígitos',
                'status': 'error'
            }), 400
        
        db = get_db()
        base_datos_usuarios = BaseDatosUsuarios(db)
        usuario_db = base_datos_usuarios.obtener_por_usuario(usuario)
        
        if not usuario_db or usuario_db.id_rol != 2:  # Verificar que sea personal
            return jsonify({
                'error': 'Credenciales incorrectas',
                'status': 'error'
            }), 401
            
        if bcrypt.checkpw(contraseña.encode('utf-8'), usuario_db.hash_contraseña.encode('utf-8')):
            access_token = create_access_token(
                identity=usuario_db.usuario,
                additional_claims={
                    "rol": usuario_db.rol.rol,
                    "tipo": "personal"
                }
            )
            return jsonify({
                'access_token': access_token,
                'user': {
                    'id': usuario_db.id_usuario,
                    'usuario': usuario_db.usuario,
                    'rol': usuario_db.rol.rol
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
            
        # Validar que la contraseña sea numérica y tenga 6 dígitos
        if not validar_contraseña_numerica(contraseña):
            return jsonify({
                'error': 'La contraseña debe ser un número de 6 dígitos',
                'status': 'error'
            }), 400
        
        db = get_db()
        base_datos_usuarios = BaseDatosUsuarios(db)
        usuario_db = base_datos_usuarios.obtener_por_usuario(usuario)
        
        if not usuario_db or usuario_db.id_rol != 1:  # Verificar que sea administrador
            return jsonify({
                'error': 'Credenciales incorrectas',
                'status': 'error'
            }), 401
            
        if bcrypt.checkpw(contraseña.encode('utf-8'), usuario_db.hash_contraseña.encode('utf-8')):
            access_token = create_access_token(
                identity=usuario_db.usuario,
                additional_claims={
                    "rol": usuario_db.rol.rol,
                    "tipo": "administrador"
                }
            )
            return jsonify({
                'access_token': access_token,
                'user': {
                    'id': usuario_db.id_usuario,
                    'usuario': usuario_db.usuario,
                    'rol': usuario_db.rol.rol
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
        id_rol = data.get('idRol')
        
        if not usuario or not contraseña or not id_rol:
            return jsonify({
                'error': 'Usuario, contraseña y rol son requeridos',
                'status': 'error'
            }), 400
        
        db = get_db()
        base_datos_usuarios = BaseDatosUsuarios(db)
        
        if base_datos_usuarios.obtener_por_usuario(usuario):
            return jsonify({
                'error': 'El usuario ya existe',
                'status': 'error'
            }), 400
        
        hash_contraseña = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        base_datos_usuarios.crear(usuario, hash_contraseña, id_rol)
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
        db = get_db()
        base_datos_usuarios = BaseDatosUsuarios(db)
        usuarios = base_datos_usuarios.listar_todos()
        usuarios_json = []
        for usuario in usuarios:
            usuarios_json.append({
                'id': usuario.id_usuario,
                'usuario': usuario.usuario,
                'rol': usuario.rol.rol
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
        db = get_db()
        base_datos_usuarios = BaseDatosUsuarios(db)
        current_user = base_datos_usuarios.obtener_por_usuario(token_data['sub'])
        
        if current_user.id_usuario == id_usuario:
            return jsonify({
                'error': 'No puedes eliminar tu propio usuario',
                'status': 'error'
            }), 400
            
        base_datos_usuarios.eliminar(id_usuario)
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
            
        db = get_db()
        base_datos_usuarios = BaseDatosUsuarios(db)
        
        # Si se proporciona una nueva contraseña, hashearla
        hash_contraseña = None
        if nueva_contraseña and nueva_contraseña.strip():
            hash_contraseña = bcrypt.hashpw(nueva_contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        base_datos_usuarios.actualizar(id_usuario, nuevo_usuario, hash_contraseña, nuevo_id_rol)
        return jsonify({
            'mensaje': 'Usuario editado exitosamente',
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@auth_bp.route('/verify-token', methods=['GET'])
@jwt_required()
def verify_token():
    try:
        token_data = get_jwt()
        db = get_db()
        base_datos_usuarios = BaseDatosUsuarios(db)
        current_user = base_datos_usuarios.obtener_por_usuario(token_data['sub'])
        
        return jsonify({
            'user': {
                'id': current_user.id_usuario,
                'usuario': current_user.usuario,
                'rol': current_user.rol.rol
            },
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500
