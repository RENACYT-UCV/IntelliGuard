
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


#from models.registros_pertencia import BaseDatosRegistrosPertenencia


pertenencias_bp = Blueprint('pertenencias', __name__)


@pertenencias_bp.route('/pertenencia/consultar-pertenencias-estudiante-busqueda', methods=['POST'])
# @jwt_required() #Se desactivada el jwt_required, debido a que se quito el login y por ello no se puede generar un token de sesion
# @role_required('Personal') #Se desactivada el role_required, debido a que no existe un token de sesion y por ello no se puede validar el rol
def consulta_pertenencias_estudiante_busqueda():
    datosEstudiante = request.form.get('datosEstudiante', "")
    estadoRegistros = request.form.get('estadoRegistros', "")
    codigoPertenencia = request.form.get('codigoPertenencia', "")
    print("consulta")
    try:
        pertenencias = PertenenciasService.consultar_pertencias_estudiante_busqueda(datosEstudiante,estadoRegistros,codigoPertenencia)
        if pertenencias == -1:
            return jsonify({'error': 'Error al consultar Datos Pertenencia'}), 404
        else:
            return jsonify({'pertenencias':pertenencias}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

