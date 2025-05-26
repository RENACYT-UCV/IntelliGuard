
from services.pertenencias_service import PertenenciasService
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, Blueprint, jsonify, request, send_from_directory
import os
from flask import current_app, send_from_directory
import base64
#from utils.role_decorador import role_required
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


@pertenencias_bp.route('/pertenencia/consulta-reporte', methods=['POST'])
# @jwt_required() #Se desactivada el jwt_required, debido a que se quito el login y por ello no se puede generar un token de sesion
# @role_required('Administrador') #Se desactivada el role_required, debido a que no existe un token de sesion y por ello no se puede validar el rol
def consulta_reporte():
    datosEstudiante = request.form.get('datosEstudiante')
    estadoRegistros = request.form.get('estadoRegistros')
    codigoPertenencia = request.form.get('codigoPertenencia')
    print("consulta")
    try:
        pertenencias = PertenenciasService.consultar_pertencias_estudiante_busqueda(datosEstudiante,estadoRegistros,codigoPertenencia)
        registros = PertenenciasService.consultar_registros_pertencia(datosEstudiante,estadoRegistros,codigoPertenencia)
        if pertenencias == -1 or registros == -1:
            return jsonify({'error': 'Error al consultar Datos de reporte'}), 404
        else:
            return jsonify({'pertenencias':pertenencias, 'registros':registros}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pertenencias_bp.route('/pertenencia/generar-excel', methods=['GET'])
def generar_excel():
    datosEstudiante = ""
    estadoPertenencia = ""
    codigoPertenencia = ""
    base_datos_registrosPertenencia = BaseDatosRegistrosPertenencia("basededatos.db")
    pertenencias = base_datos_registrosPertenencia.consultar_registros_pertencia_busqueda(datosEstudiante, estadoPertenencia, codigoPertenencia)
    
    # Crear un archivo Excel en memoria
    wb = Workbook()
    ws = wb.active
    ws.title = "Pertenencias"
    headers = ['ID Registro', 'Estado', 'Hora Entrada', 'Hora Salida', 'Cod Estudiante', 'Nombres Estudiante', 'Código Pertenencia', 'Nombre Objeto']
    ws.append(headers)
    
    if pertenencias and isinstance(pertenencias, list):
        for pertenencia in pertenencias:
            ws.append([
                pertenencia.id_registro,
                pertenencia.estado,
                pertenencia.hora_entrada,
                pertenencia.hora_salida,
                pertenencia.id_estudiante,
                pertenencia.nombres_estudiante,
                pertenencia.codigoPertenencia,
                pertenencia.nombre_objeto
            ])
    
    excel_buffer = BytesIO()
    wb.save(excel_buffer)
    excel_buffer.seek(0)
    return send_file(
        excel_buffer,
        as_attachment=True,
        download_name="Pertenencias.xlsx",
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    

