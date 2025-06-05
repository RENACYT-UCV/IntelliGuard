from flask import Blueprint, jsonify, request
from ..services.pertenencia_service import PertenenciaService
from ..utils.role_decorador import role_required
import logging

logger = logging.getLogger(__name__)

pertenencia_bp = Blueprint('pertenencia', __name__, url_prefix='/api/pertenencia')

@pertenencia_bp.route('/buscar', methods=['POST'])
@role_required(['admin', 'personal'])
def buscar_pertenencias():
    """Busca pertenencias por diferentes criterios"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Se requieren criterios de búsqueda',
                'status': 'error'
            }), 400

        pertenencias = PertenenciaService.buscar_pertenencias(
            datos_estudiante=data.get('datos_estudiante', ''),
            estado=data.get('estado', ''),
            codigo=data.get('codigo', '')
        )
        
        return jsonify({
            'pertenencias': pertenencias,
            'status': 'success'
        })
    except Exception as e:
        logger.error(f"Error en búsqueda de pertenencias: {str(e)}")
        return jsonify({
            'error': 'Error al buscar pertenencias',
            'status': 'error'
        }), 500

@pertenencia_bp.route('/', methods=['POST'])
@role_required(['admin', 'personal'])
def registrar_pertenencia():
    """Registra una nueva pertenencia"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Se requieren datos de la pertenencia',
                'status': 'error'
            }), 400

        resultado = PertenenciaService.registrar_pertenencia(
            descripcion=data.get('descripcion'),
            id_estudiante=data.get('id_estudiante')
        )
        
        if not resultado.get('exito'):
            return jsonify(resultado), 400
            
        return jsonify(resultado), 201
    except Exception as e:
        logger.error(f"Error registrando pertenencia: {str(e)}")
        return jsonify({
            'error': 'Error al registrar pertenencia',
            'status': 'error'
        }), 500

@pertenencia_bp.route('/<int:id>', methods=['GET'])
@role_required(['admin', 'personal'])
def obtener_pertenencia(id):
    """Obtiene una pertenencia por su ID"""
    try:
        detallado = request.args.get('detallado', 'true').lower() == 'true'
        pertenencia = PertenenciaService.obtener_pertenencia(id, detallado=detallado)
        
        if not pertenencia:
            return jsonify({
                'error': 'Pertenencia no encontrada',
                'status': 'error'
            }), 404
            
        return jsonify({
            'pertenencia': pertenencia,
            'status': 'success'
        })
    except Exception as e:
        logger.error(f"Error obteniendo pertenencia {id}: {str(e)}")
        return jsonify({
            'error': 'Error al obtener pertenencia',
            'status': 'error'
        }), 500

@pertenencia_bp.route('/<int:id>/estado', methods=['PUT'])
@role_required(['admin', 'personal'])
def actualizar_estado(id):
    """Actualiza el estado de una pertenencia"""
    try:
        data = request.get_json()
        if not data or 'estado' not in data:
            return jsonify({
                'error': 'Se requiere el nuevo estado',
                'status': 'error'
            }), 400

        resultado = PertenenciaService.actualizar_estado(id, data['estado'])
        
        if not resultado.get('exito'):
            return jsonify(resultado), 400
            
        return jsonify(resultado)
    except Exception as e:
        logger.error(f"Error actualizando estado de pertenencia {id}: {str(e)}")
        return jsonify({
            'error': 'Error al actualizar estado',
            'status': 'error'
        }), 500

@pertenencia_bp.route('/estudiante/<int:id_estudiante>', methods=['GET'])
@role_required(['admin', 'personal'])
def listar_por_estudiante(id_estudiante):
    """Lista todas las pertenencias de un estudiante"""
    try:
        pertenencias = PertenenciaService.listar_por_estudiante(id_estudiante)
        return jsonify({
            'pertenencias': pertenencias,
            'status': 'success'
        })
    except Exception as e:
        logger.error(f"Error listando pertenencias del estudiante {id_estudiante}: {str(e)}")
        return jsonify({
            'error': 'Error al listar pertenencias',
            'status': 'error'
        }), 500 