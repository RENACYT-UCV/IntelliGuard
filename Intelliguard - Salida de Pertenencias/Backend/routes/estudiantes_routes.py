from flask import Blueprint, jsonify,request
from services.estudiantes_service import EstudiantesService
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from utils.role_decorador import role_required

estudiantes_bp = Blueprint('estudiantes', __name__)
estudiantes_service = EstudiantesService()



@estudiantes_bp.route('/estudiante/reconocimiento-facial', methods=['POST'])
# @jwt_required()
# @role_required('Personal')
def identificar_estudiante():
    file = request.files['file']
    resultado, porcentaje_similitud = estudiantes_service.identificar_estudiante(file)
    if resultado == -1:
        return jsonify({'error': 'Estudiante no reconocido'}), 404
    else:
        return jsonify({
            'idEstudiante': resultado.id_estudiante,
            'codigoEstudiante': resultado.codigo_estudiante,
            'Nombres':  resultado.nombres,
            'Carrera':  resultado.carrera,
            'PlanEstudiante':  resultado.planEstudiante,
            'Similitud': porcentaje_similitud
        }), 200

@estudiantes_bp.route('/estudiante/reconocimiento-facial/video', methods=['POST'])
# @jwt_required()
# @role_required('Personal')
def registrar_estudiante_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No se encontró ningún archivo en la solicitud'}), 400
    file = request.files['file']
    codigoEstudiante = request.form.get('codigoEstudiante')
    nombCompletos = request.form.get('NombreCompleto')
    carrera = request.form.get('carrera')
    planEstudiante = request.form.get('planEstudiante')
    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400
    estudiantes_service.registrar_estudiante(file,nombCompletos,codigoEstudiante,carrera,planEstudiante)
    return jsonify({'mensaje': 'Registro de estudiantes completado','Nombres':f'{nombCompletos}','CodEstudiante':f'{codigoEstudiante}'}), 200








