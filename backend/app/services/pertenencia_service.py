from typing import Dict, List, Optional, Tuple
from datetime import datetime
from ..models.pertenencia import Pertenencia, PertenenciaDetallada, PertenenciaModel
from ..models.estudiante import EstudianteModel
from ..database.db_manager import db
import logging

logger = logging.getLogger(__name__)

class PertenenciaService:
    def __init__(self):
        self.db = db

    @staticmethod
    def registrar_pertenencia(descripcion: str, id_estudiante: int) -> Dict:
        """
        Registra una nueva pertenencia para un estudiante.
        Retorna un diccionario con el resultado de la operación.
        """
        # Verificar que el estudiante existe
        estudiante = EstudianteModel.obtener_por_id(id_estudiante)
        if not estudiante:
            return {
                'exito': False,
                'errores': ['El estudiante no existe']
            }

        # Crear la pertenencia
        return PertenenciaModel.crear(descripcion, id_estudiante)

    @staticmethod
    def obtener_pertenencia(id: int, detallado: bool = False) -> Optional[Pertenencia | PertenenciaDetallada]:
        """
        Obtiene una pertenencia por su ID.
        Si detallado es True, incluye información del estudiante.
        """
        if detallado:
            return PertenenciaModel.obtener_detallado_por_id(id)
        return PertenenciaModel.obtener_por_id(id)

    @staticmethod
    def listar_pertenencias_estudiante(id_estudiante: int) -> List[Pertenencia]:
        """Lista todas las pertenencias de un estudiante"""
        return PertenenciaModel.listar_por_estudiante(id_estudiante)

    @staticmethod
    def buscar_pertenencias(
        datos_estudiante: str = "",
        estado: str = "",
        codigo: str = ""
    ) -> List[PertenenciaDetallada]:
        """
        Busca pertenencias con filtros.
        Retorna una lista de pertenencias con detalles del estudiante.
        """
        # Validar estado si se proporciona
        if estado and estado not in PertenenciaModel.ESTADOS_VALIDOS:
            return []

        # Si se proporciona un código, agregarlo a datos_estudiante
        datos_busqueda = datos_estudiante
        if codigo:
            datos_busqueda = codigo if not datos_estudiante else f"{datos_estudiante} {codigo}"

        return PertenenciaModel.buscar(
            datos_estudiante=datos_busqueda,
            estado=estado
        )

    @staticmethod
    def marcar_como_retirado(id: int) -> Dict:
        """Marca una pertenencia como retirada"""
        return PertenenciaModel.actualizar_estado(id, 'retirado')

    @staticmethod
    def marcar_como_perdido(id: int) -> Dict:
        """Marca una pertenencia como perdida"""
        return PertenenciaModel.actualizar_estado(id, 'perdido')

    @staticmethod
    def reactivar_pertenencia(id: int) -> Dict:
        """Reactiva una pertenencia (la marca como activa)"""
        return PertenenciaModel.actualizar_estado(id, 'activo')

    @staticmethod
    def obtener_estadisticas() -> Dict:
        """
        Obtiene estadísticas de las pertenencias.
        Retorna un diccionario con diferentes métricas.
        """
        try:
            query = """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN estado = 'activo' THEN 1 ELSE 0 END) as activas,
                    SUM(CASE WHEN estado = 'retirado' THEN 1 ELSE 0 END) as retiradas,
                    SUM(CASE WHEN estado = 'perdido' THEN 1 ELSE 0 END) as perdidas,
                    COUNT(DISTINCT id_estudiante) as total_estudiantes,
                    strftime('%Y-%m', fecha_registro) as mes
                FROM pertenencias
                GROUP BY strftime('%Y-%m', fecha_registro)
                ORDER BY mes DESC
                LIMIT 12
            """
            resultados = db.fetch_all(query)
            
            estadisticas = {
                'por_mes': [
                    {
                        'mes': r[5],
                        'total': r[0],
                        'activas': r[1],
                        'retiradas': r[2],
                        'perdidas': r[3],
                        'estudiantes_unicos': r[4]
                    } for r in resultados
                ]
            }
            
            # Agregar totales generales
            query_totales = """
                SELECT 
                    COUNT(*) as total,
                    COUNT(DISTINCT id_estudiante) as total_estudiantes,
                    SUM(CASE WHEN estado = 'activo' THEN 1 ELSE 0 END) as activas,
                    SUM(CASE WHEN estado = 'retirado' THEN 1 ELSE 0 END) as retiradas,
                    SUM(CASE WHEN estado = 'perdido' THEN 1 ELSE 0 END) as perdidas
                FROM pertenencias
            """
            totales = db.fetch_one(query_totales)
            
            estadisticas['totales'] = {
                'total': totales[0],
                'estudiantes_unicos': totales[1],
                'activas': totales[2],
                'retiradas': totales[3],
                'perdidas': totales[4]
            }
            
            return {'exito': True, 'estadisticas': estadisticas}
        except Exception as e:
            return {'exito': False, 'errores': [str(e)]}

    def get_all_pertenencias(self):
        """Obtiene todas las pertenencias con información del estudiante"""
        try:
            query = """
                SELECT 
                    p.id,
                    p.id_estudiante,
                    p.descripcion,
                    p.fecha_registro,
                    p.estado,
                    e.nombres as estudiante_nombre,
                    e.carrera as estudiante_carrera
                FROM pertenencias p
                LEFT JOIN estudiantes e ON p.id_estudiante = e.id
                ORDER BY p.fecha_registro DESC
            """
            pertenencias = self.db.fetch_all(query)
            return [dict(row) for row in pertenencias]
        except Exception as e:
            logger.error(f"Error al obtener pertenencias: {str(e)}")
            raise 