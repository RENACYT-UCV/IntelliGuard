from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..utils.role_decorador import role_required
from ..models.estudiante import Estudiante

estudiante_bp = Blueprint('estudiante', __name__)

@estudiante_bp.route('/estudiante/registrar', methods=['POST'])
@jwt_required()
@role_required(['Personal', 'Administrador'])
def registrar_estudiante():
    try:
        data = request.get_json()
        
        # Crear instancia de estudiante
        estudiante = Estudiante(
            codigo=data.get('codigo'),
            nombres=data.get('nombres'),
            carrera=data.get('carrera'),
            plan=data.get('plan')
        )
        
        # Validar y guardar
        exito, errores = estudiante.guardar()
        
        if exito:
            return jsonify({
                'mensaje': 'Estudiante registrado exitosamente',
                'status': 'success'
            }), 201
        else:
            return jsonify({
                'error': errores[0] if errores else 'Error al registrar estudiante',
                'errores': errores,
                'status': 'error'
            }), 422
            
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@estudiante_bp.route('/estudiante/<codigo>', methods=['GET'])
@jwt_required()
@role_required('Personal')
def obtener_estudiante(codigo):
    try:
        estudiante = Estudiante.obtener_por_codigo(codigo)
        
        if estudiante:
            return jsonify({
                'codigo': estudiante.codigo,
                'nombres': estudiante.nombres,
                'carrera': estudiante.carrera,
                'plan': estudiante.plan,
                'status': 'success'
            }), 200
        else:
            return jsonify({
                'error': 'Estudiante no encontrado',
                'status': 'error'
            }), 404
            
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500 