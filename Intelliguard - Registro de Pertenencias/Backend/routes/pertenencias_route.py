
from services.pertenencias_service import PertenenciasService
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, Blueprint, jsonify, request, send_from_directory
import os
from flask import current_app, send_from_directory
import base64
# from utils.role_decorador import role_required
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


    

@pertenencias_bp.route('/pertenencia/nueva-pertenencia', methods=['POST'])
# @jwt_required()
# @role_required('Personal')
def nueva_pertenecia():
    file = request.files['file']
    if not file:
        return jsonify({'error': 'El archivo es requerido'}), 400
    idEstudiante = request.form.get('idEstudiante')
    idObjeto = request.form.get('idObjeto')
    if not idEstudiante:
        return jsonify({'error': 'El id del estudiante es requerido'}), 400
    
    try:
        pertenencias = PertenenciasService.registrar_nueva_pertenencia(file,idEstudiante,idObjeto)
        if pertenencias == -1:
            return jsonify({'error': 'Error al registrar Pertenencia'}), 404
        else:
            return jsonify({'msg':'pertenencia registrada exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@pertenencias_bp.route('/pertenencia/registrar-ingreso-pertenencia', methods=['POST'])
# @jwt_required()
# @role_required('Personal')
def ingreso_pertenecia():
    file = request.files['file']
    if not file:
        return jsonify({'error': 'El archivo es requerido'}), 400
    idEstudiante = request.form.get('idEstudiante')
    idObjeto = request.form.get('idObjeto')
    if not idEstudiante:
        return jsonify({'error': 'El id del estudiante es requerido'}), 400
    
    codigoPertenencia = request.form.get('codigoPertenencia')
    if not codigoPertenencia:
        return jsonify({'error': 'El codigoPertenencia es requerido'}), 400
    
    try:
        pertenencias = PertenenciasService.registrar_entrada_pertenencia(file,idEstudiante,idObjeto,codigoPertenencia)
        if pertenencias == -1:
            return jsonify({'error': 'Error al registrar ingreso Pertenencia'}), 404
        else:
            return jsonify({'msg':'ingreso de pertencia registrada exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
