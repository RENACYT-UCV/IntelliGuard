from typing import Dict, List, Optional, Tuple
from datetime import datetime
from ..models.pertenencia import Pertenencia, PertenenciaDetallada, PertenenciaModel
from ..models.estudiante import EstudianteModel

class PertenenciaService:
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
        descripcion: str = ""
    ) -> List[PertenenciaDetallada]:
        """
        Busca pertenencias con filtros.
        Retorna una lista de pertenencias con detalles del estudiante.
        """
        # Validar estado si se proporciona
        if estado and estado not in PertenenciaModel.ESTADOS_VALIDOS:
            return []

        return PertenenciaModel.buscar(
            datos_estudiante=datos_estudiante,
            estado=estado,
            descripcion=descripcion
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