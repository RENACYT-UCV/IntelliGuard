from flask import Blueprint, jsonify, request, send_file
from ..services.reporte_service import ReporteService
from ..utils.role_decorador import role_required
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

reporte_bp = Blueprint('reporte', __name__, url_prefix='/api/reporte')

@reporte_bp.route('/', methods=['POST'])
@role_required(['admin', 'personal'])
def registrar_reporte():
    """Registra un nuevo reporte"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Se requieren datos del reporte',
                'status': 'error'
            }), 400

        resultado = ReporteService.registrar_reporte(
            id_pertenencia=data.get('id_pertenencia'),
            tipo=data.get('tipo'),
            detalles=data.get('detalles')
        )
        
        if not resultado.get('exito'):
            return jsonify(resultado), 400
            
        return jsonify(resultado), 201
    except Exception as e:
        logger.error(f"Error registrando reporte: {str(e)}")
        return jsonify({
            'error': 'Error al registrar reporte',
            'status': 'error'
        }), 500

@reporte_bp.route('/<int:id>', methods=['GET'])
@role_required(['admin', 'personal'])
def obtener_reporte(id):
    """Obtiene un reporte por su ID"""
    try:
        detallado = request.args.get('detallado', 'true').lower() == 'true'
        reporte = ReporteService.obtener_reporte(id, detallado=detallado)
        
        if not reporte:
            return jsonify({
                'error': 'Reporte no encontrado',
                'status': 'error'
            }), 404
            
        return jsonify({
            'reporte': reporte,
            'status': 'success'
        })
    except Exception as e:
        logger.error(f"Error obteniendo reporte {id}: {str(e)}")
        return jsonify({
            'error': 'Error al obtener reporte',
            'status': 'error'
        }), 500

@reporte_bp.route('/pertenencia/<int:id_pertenencia>', methods=['GET'])
@role_required(['admin', 'personal'])
def listar_reportes_pertenencia(id_pertenencia):
    """Lista todos los reportes de una pertenencia"""
    try:
        reportes = ReporteService.listar_reportes_pertenencia(id_pertenencia)
        return jsonify({
            'reportes': reportes,
            'status': 'success'
        })
    except Exception as e:
        logger.error(f"Error listando reportes de pertenencia {id_pertenencia}: {str(e)}")
        return jsonify({
            'error': 'Error al listar reportes',
            'status': 'error'
        }), 500

@reporte_bp.route('/buscar', methods=['GET'])
@role_required(['admin', 'personal'])
def buscar_reportes():
    """Busca reportes por diferentes criterios"""
    try:
        datos_estudiante = request.args.get('datos_estudiante', '')
        tipo = request.args.get('tipo', '')
        fecha_inicio = request.args.get('fecha_inicio', '')
        fecha_fin = request.args.get('fecha_fin', '')
        
        reportes = ReporteService.buscar_reportes(
            datos_estudiante=datos_estudiante,
            tipo=tipo,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        
        return jsonify({
            'reportes': reportes,
            'status': 'success'
        })
    except Exception as e:
        logger.error(f"Error en búsqueda de reportes: {str(e)}")
        return jsonify({
            'error': 'Error al buscar reportes',
            'status': 'error'
        }), 500

@reporte_bp.route('/estadisticas', methods=['GET'])
@role_required(['admin'])
def obtener_estadisticas():
    """Obtiene estadísticas de reportes por período"""
    try:
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        
        if not fecha_inicio or not fecha_fin:
            return jsonify({
                'error': 'Se requieren fecha_inicio y fecha_fin',
                'status': 'error'
            }), 400
        
        resultado = ReporteService.obtener_estadisticas_por_periodo(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        
        if not resultado.get('exito'):
            return jsonify(resultado), 400
            
        return jsonify(resultado)
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {str(e)}")
        return jsonify({
            'error': 'Error al obtener estadísticas',
            'status': 'error'
        }), 500

@reporte_bp.route('/excel', methods=['GET'])
@role_required(['admin', 'personal'])
def descargar_excel():
    """Genera y descarga un reporte en Excel"""
    try:
        excel_buffer = ReporteService.generar_excel_reporte()
        
        if excel_buffer is None:
            return jsonify({
                'error': 'Error al generar el archivo Excel',
                'status': 'error'
            }), 500

        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"reporte_pertenencias_{fecha_actual}.xlsx"

        return send_file(
            excel_buffer,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=nombre_archivo
        )
    except Exception as e:
        logger.error(f"Error generando Excel: {str(e)}")
        return jsonify({
            'error': 'Error al generar Excel',
            'status': 'error'
        }), 500 