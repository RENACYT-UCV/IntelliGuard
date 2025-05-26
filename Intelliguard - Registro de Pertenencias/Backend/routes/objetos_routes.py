from flask import Blueprint, jsonify,request
from flask_jwt_extended import jwt_required, get_jwt_identity
# from utils.role_decorador import role_required
import base64
from services.pertenencias_service import PertenenciasService
from services.objeto_service import ObjetoService
import cv2

objetos_bp = Blueprint('objetos', __name__)

@objetos_bp.route('/objeto/consultar-objeto-pertenencia', methods=['POST'])
# @jwt_required()
# @role_required('Personal')
def consultar_objeto_pertenencia():
    try:
        file = request.files['file']
        if not file:
            return jsonify({'error': 'El archivo es requerido'}), 400
        idEstudiante = request.form.get('idEstudiante')
        if not idEstudiante:
            return jsonify({'error': 'El código del estudiante es requerido'}), 400
        pertenencias, objeto, imagenRecortada = ObjetoService.identificar_objeto_pertenencia(file, idEstudiante)
        if pertenencias == "no object":
            return jsonify({'error': 'no_object'}), 404
        if imagenRecortada is not None:
            _, buffer = cv2.imencode('.jpg', imagenRecortada)
            imagen_recortada_base64 = base64.b64encode(buffer).decode('utf-8')
        else:
            return jsonify({'error': 'Error al procesar la imagen recortada'}), 500
        if pertenencias == "no pertenencia":
            return jsonify({
                'nombreObjeto': objeto.nombre,
                'idObjeto': objeto.id_objeto,
                'imagenRecortada': f'data:image/jpeg;base64,{imagen_recortada_base64}',
                'estado': "sin_registros"
            }), 200

        if objeto:
            return jsonify({
                'nombreObjeto': objeto.nombre,
                'idObjeto': objeto.id_objeto,
                'estado': "coincidencias",
                'imagenRecortada': f'data:image/jpeg;base64,{imagen_recortada_base64}',
                'pertenencias_coincidencia': pertenencias
            }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
