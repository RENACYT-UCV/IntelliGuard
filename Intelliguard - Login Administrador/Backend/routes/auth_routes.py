from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.usuario import BaseDatosUsuarios
from flask_jwt_extended import jwt_required
import bcrypt

auth_bp = Blueprint('auth_bp', __name__)




@auth_bp.route('/login/administrador', methods=['POST'])
def loginAdministrador():
    data = request.get_json()
    usuario = data.get('usuario')
    contraseña = data.get('contraseña')
    base_datos_usuarios = BaseDatosUsuarios("basededatos.db")
    usuario_db = base_datos_usuarios.consultar_usuario_administrador(usuario)
    if usuario_db and bcrypt.checkpw(contraseña.encode('utf-8'), usuario_db.hash_contraseña):
        additional_claims = {"rol": usuario_db.rol}
        access_token = create_access_token(identity=usuario,additional_claims=additional_claims)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'mensaje': 'Credenciales incorrectas'}), 401



