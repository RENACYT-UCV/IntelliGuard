from flask import Blueprint, jsonify, request, send_file
from ..services.pertenencia_service import PertenenciaService
from ..utils.role_decorador import role_required
from flask_jwt_extended import jwt_required
from datetime import datetime
import logging
import csv
import io
import pandas as pd
import os

logger = logging.getLogger(__name__)

pertenencia_bp = Blueprint('pertenencia', __name__, url_prefix='/api/pertenencia')
pertenencia_service = PertenenciaService()

@pertenencia_bp.route('/buscar', methods=['GET'])
@role_required(['admin', 'personal'])
def buscar_pertenencias():
    """Busca pertenencias por diferentes criterios"""
    try:
        datos_estudiante = request.args.get('datos_estudiante', '')
        estado = request.args.get('estado', '')
        codigo = request.args.get('codigo', '')
        
        pertenencias = PertenenciaService.buscar_pertenencias(
            datos_estudiante=datos_estudiante,
            estado=estado,
            codigo=codigo
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

@pertenencia_bp.route('/consulta-reporte', methods=['OPTIONS'])
def consulta_reporte_options():
    return '', 200

@pertenencia_bp.route('/consulta-reporte', methods=['GET', 'POST'])
@jwt_required()
@role_required(['admin', 'personal'])
def consulta_reporte():
    """Obtiene los datos para el reporte"""
    try:
        pertenencias = PertenenciaService.buscar_pertenencias()
        return jsonify({
            'pertenencias': pertenencias,
            'status': 'success'
        })
    except Exception as e:
        logger.error(f"Error consultando reporte: {str(e)}")
        return jsonify({
            'error': 'Error al consultar reporte',
            'status': 'error'
        }), 500

@pertenencia_bp.route('/descargar-excel', methods=['OPTIONS'])
def descargar_excel_options():
    return '', 200

@pertenencia_bp.route('/descargar-excel', methods=['GET'])
@jwt_required()
@role_required(['admin', 'personal'])
def descargar_excel():
    try:
        # Obtener datos de pertenencias
        pertenencias = pertenencia_service.get_all_pertenencias()
        
        # Crear DataFrame
        df = pd.DataFrame(pertenencias)
        df = df.rename(columns={
            'id': 'ID',
            'estudiante_id': 'ID Estudiante',
            'tipo': 'Tipo',
            'descripcion': 'Descripción',
            'fecha_registro': 'Fecha de Registro',
            'estado': 'Estado'
        })
        
        # Crear buffer en memoria para el archivo Excel
        output = io.BytesIO()
        
        # Escribir DataFrame a Excel
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Pertenencias', index=False)
            
            # Ajustar ancho de columnas
            worksheet = writer.sheets['Pertenencias']
            for i, col in enumerate(df.columns):
                column_len = max(df[col].astype(str).str.len().max(), len(col)) + 2
                worksheet.set_column(i, i, column_len)
        
        output.seek(0)
        
        # Generar nombre de archivo con fecha
        fecha_actual = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'reporte_pertenencias_{fecha_actual}.xlsx'
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        logger.error(f"Error generando reporte: {str(e)}")
        return jsonify({
            'error': 'Error al generar reporte',
            'status': 'error'
        }), 500