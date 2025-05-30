from ..services.pertenencias_service import PertenenciasService
from flask import Blueprint, jsonify, request
import os
from flask import current_app
import base64

pertenencias_bp = Blueprint('pertenencias', __name__)

@pertenencias_bp.route('/pertenencia/consultar-pertenencias-estudiante-busqueda', methods=['POST'])
def consulta_pertenencias_estudiante_busqueda():
    datosEstudiante = request.form.get('datosEstudiante', "")
    estadoRegistros = request.form.get('estadoRegistros', "")
    codigoPertenencia = request.form.get('codigoPertenencia', "")
    print("consulta")
    try:
        pertenencias = PertenenciasService.consultar_pertenencias_estudiante_busqueda(datosEstudiante, estadoRegistros, codigoPertenencia)
        if pertenencias == -1:
            return jsonify({'error': 'Error al consultar Datos Pertenencia'}), 404
        else:
            return jsonify({'pertenencias': pertenencias}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 