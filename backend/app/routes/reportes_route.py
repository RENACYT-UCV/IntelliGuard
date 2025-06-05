from flask import Blueprint, jsonify, request, send_file
from ..services.reportes_service import ReportesService
from datetime import datetime

reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/consultar-reporte', methods=['GET'])
def consultar_reporte():
    try:
        datos_estudiante = request.args.get('datos_estudiante', '')
        estado_registros = request.args.get('estado_registros', '')
        codigo_pertenencia = request.args.get('codigo_pertenencia', '')

        resultado = ReportesService.consultar_reporte_completo(
            datos_estudiante, estado_registros, codigo_pertenencia
        )

        if resultado == -1:
            return jsonify({'mensaje': 'No se encontraron registros'}), 404

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reportes_bp.route('/descargar-excel', methods=['GET'])
def descargar_excel():
    try:
        excel_buffer = ReportesService.generar_excel_reporte()
        
        if excel_buffer is None:
            return jsonify({'mensaje': 'Error al generar el archivo Excel'}), 500

        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"reporte_pertenencias_{fecha_actual}.xlsx"

        return send_file(
            excel_buffer,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=nombre_archivo
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500 