from typing import Dict, List, Optional
from datetime import datetime
from ..models.reporte import Reporte, ReporteDetallado, ReporteModel
from ..models.pertenencia import PertenenciaModel
import pandas as pd
import io
import csv

class ReporteService:
    @staticmethod
    def registrar_reporte(id_pertenencia: int, tipo: str, detalles: str) -> Dict:
        """
        Registra un nuevo reporte para una pertenencia.
        Retorna un diccionario con el resultado de la operación.
        """
        # Verificar que la pertenencia existe
        pertenencia = PertenenciaModel.obtener_por_id(id_pertenencia)
        if not pertenencia:
            return {
                'exito': False,
                'errores': ['La pertenencia no existe']
            }

        # Validar el tipo de reporte según el estado actual de la pertenencia
        if tipo == 'entrada' and pertenencia.estado != 'activo':
            return {
                'exito': False,
                'errores': ['Solo se pueden registrar entradas para pertenencias activas']
            }
        elif tipo == 'salida' and pertenencia.estado != 'activo':
            return {
                'exito': False,
                'errores': ['Solo se pueden registrar salidas para pertenencias activas']
            }
        elif tipo == 'perdida' and pertenencia.estado != 'activo':
            return {
                'exito': False,
                'errores': ['Solo se pueden registrar pérdidas para pertenencias activas']
            }
        elif tipo == 'recuperacion' and pertenencia.estado != 'perdido':
            return {
                'exito': False,
                'errores': ['Solo se pueden registrar recuperaciones para pertenencias perdidas']
            }

        # Crear el reporte
        resultado = ReporteModel.crear(id_pertenencia, tipo, detalles)
        
        # Si el reporte se creó exitosamente, actualizar el estado de la pertenencia
        if resultado['exito']:
            if tipo == 'perdida':
                PertenenciaModel.actualizar_estado(id_pertenencia, 'perdido')
            elif tipo == 'recuperacion':
                PertenenciaModel.actualizar_estado(id_pertenencia, 'activo')

        return resultado

    @staticmethod
    def obtener_reporte(id: int, detallado: bool = False) -> Optional[Reporte | ReporteDetallado]:
        """
        Obtiene un reporte por su ID.
        Si detallado es True, incluye información de la pertenencia y el estudiante.
        """
        if detallado:
            return ReporteModel.obtener_detallado_por_id(id)
        return ReporteModel.obtener_por_id(id)

    @staticmethod
    def listar_reportes_pertenencia(id_pertenencia: int) -> List[Reporte]:
        """Lista todos los reportes de una pertenencia"""
        return ReporteModel.listar_por_pertenencia(id_pertenencia)

    @staticmethod
    def buscar_reportes(
        datos_estudiante: str = "",
        tipo: str = "",
        fecha_inicio: str = "",
        fecha_fin: str = ""
    ) -> List[ReporteDetallado]:
        """
        Busca reportes con filtros.
        Retorna una lista de reportes con detalles de la pertenencia y el estudiante.
        """
        # Validar tipo si se proporciona
        if tipo and tipo not in ReporteModel.TIPOS_VALIDOS:
            return []

        # Validar fechas si se proporcionan
        try:
            if fecha_inicio:
                datetime.strptime(fecha_inicio, "%Y-%m-%d")
            if fecha_fin:
                datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            return []

        return ReporteModel.buscar(
            datos_estudiante=datos_estudiante,
            tipo=tipo,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )

    @staticmethod
    def obtener_estadisticas_por_periodo(
        fecha_inicio: str,
        fecha_fin: str
    ) -> Dict:
        """
        Obtiene estadísticas de reportes para un período específico.
        """
        try:
            query = """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN tipo = 'entrada' THEN 1 ELSE 0 END) as entradas,
                    SUM(CASE WHEN tipo = 'salida' THEN 1 ELSE 0 END) as salidas,
                    SUM(CASE WHEN tipo = 'perdida' THEN 1 ELSE 0 END) as perdidas,
                    SUM(CASE WHEN tipo = 'recuperacion' THEN 1 ELSE 0 END) as recuperaciones,
                    COUNT(DISTINCT id_pertenencia) as pertenencias_afectadas
                FROM reportes
                WHERE fecha BETWEEN ? AND ?
            """
            resultado = db.fetch_one(query, (fecha_inicio, fecha_fin))
            
            if not resultado:
                return {
                    'exito': False,
                    'errores': ['No se encontraron datos para el período especificado']
                }
            
            return {
                'exito': True,
                'estadisticas': {
                    'total_reportes': resultado[0],
                    'entradas': resultado[1],
                    'salidas': resultado[2],
                    'perdidas': resultado[3],
                    'recuperaciones': resultado[4],
                    'pertenencias_afectadas': resultado[5],
                    'periodo': {
                        'inicio': fecha_inicio,
                        'fin': fecha_fin
                    }
                }
            }
        except Exception as e:
            return {'exito': False, 'errores': [str(e)]} 

    @staticmethod
    def generar_excel_reporte() -> Optional[io.BytesIO]:
        """Genera un reporte CSV simple con los datos de los reportes"""
        try:
            # Obtener reportes
            reportes = ReporteModel.buscar()
            
            if not reportes:
                return None
                
            # Crear buffer para el CSV
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Escribir encabezados
            writer.writerow(['Fecha', 'Tipo', 'Detalles', 'Pertenencia', 'Estado', 'Estudiante'])
            
            # Escribir datos
            for reporte in reportes:
                writer.writerow([
                    reporte.fecha.strftime('%Y-%m-%d %H:%M:%S'),
                    reporte.tipo,
                    reporte.detalles,
                    reporte.pertenencia.descripcion if reporte.pertenencia else '',
                    reporte.pertenencia.estado if reporte.pertenencia else '',
                    reporte.pertenencia.estudiante.nombres if reporte.pertenencia and reporte.pertenencia.estudiante else ''
                ])
            
            # Convertir a bytes
            return io.BytesIO(output.getvalue().encode('utf-8'))
        except Exception as e:
            print(f"Error generando reporte: {str(e)}")
            return None