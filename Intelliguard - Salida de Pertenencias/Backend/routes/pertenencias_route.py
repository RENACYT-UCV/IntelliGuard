
from services.pertenencias_service import PertenenciasService
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, Blueprint, jsonify, request, send_from_directory
import os
from flask import current_app, send_from_directory
import base64
from utils.role_decorador import role_required
from openpyxl import Workbook
from io import BytesIO
from flask import send_file
import os
from flask import  send_from_directory,current_app
import base64
import numpy as np
from models.registros_pertencia import RegistrosPertenencia,BaseDatosRegistrosPertenencia

#from models.registros_pertencia import BaseDatosRegistrosPertenencia


pertenencias_bp = Blueprint('pertenencias', __name__)


    

@pertenencias_bp.route('/pertenencia/consultar-pertenencia-estado-estudiante', methods=['POST'])
# @jwt_required()
# @role_required('Personal')
def consulta_registro_estado_estudiante():
    idEstudiante = request.form.get('idEstudiante')
    idEstado = request.form.get('idEstado')
    if not idEstudiante:
        return jsonify({'error': 'El id del estudiante es requerido'}), 400
    print("consulta")
    try:
        pertenencias = PertenenciasService.consultar_pertenencia_estado_estudiante(idEstudiante,idEstado)
        if pertenencias == -1:
            return jsonify({'error': 'Error al registrar Pertenencia'}), 404
        else:
            return jsonify({'pertenencias':pertenencias}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@pertenencias_bp.route('/pertenencia/registrar-salida-pertenencia', methods=['POST'])
# @jwt_required()
# @role_required('Personal')
def salida_pertenecia():
    data = request.get_json()
    if not isinstance(data,dict):
        return jsonify({'error': 'Formato de datos incorrecto'}), 400
    
    codPertenciasIdEstado=data.get('codPertenciaIdEstado')
    if not codPertenciasIdEstado or not isinstance(codPertenciasIdEstado,list):
        return jsonify({'error': 'Formato de datos incorrecto'}), 400
    
    try:
        PertenenciasService.registrar_salida_pertenencia(codPertenciasIdEstado)
        return jsonify({'msg':'pertenencia registrada exitosamente'}), 200
    except Exception as e:
        print('Error al registrar pertencias')
        return jsonify({'error': str(e)}), 500

