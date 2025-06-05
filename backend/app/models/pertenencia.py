from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict
from ..database.db_manager import db

@dataclass
class Pertenencia:
    id: int
    descripcion: str
    fecha_registro: datetime
    estado: str
    id_estudiante: int

@dataclass
class PertenenciaDetallada:
    id: int
    descripcion: str
    fecha_registro: datetime
    estado: str
    id_estudiante: int
    codigo_estudiante: str
    nombre_estudiante: str
    carrera_estudiante: str
    plan_estudiante: str

class PertenenciaModel:
    TABLA = 'pertenencias'
    ESTADOS_VALIDOS = ['activo', 'retirado', 'perdido']

    @staticmethod
    def validar_datos(descripcion: str, id_estudiante: int, estado: str = 'activo') -> List[str]:
        """Valida los datos de una pertenencia"""
        errores = []
        
        if not descripcion or not isinstance(descripcion, str) or len(descripcion) < 3:
            errores.append("La descripción debe tener al menos 3 caracteres")
            
        if not isinstance(id_estudiante, int) or id_estudiante <= 0:
            errores.append("El ID del estudiante es inválido")
            
        if estado not in PertenenciaModel.ESTADOS_VALIDOS:
            errores.append(f"El estado debe ser uno de: {', '.join(PertenenciaModel.ESTADOS_VALIDOS)}")
            
        return errores

    @staticmethod
    def crear(descripcion: str, id_estudiante: int, estado: str = 'activo') -> Dict:
        """Crea una nueva pertenencia"""
        # Validar datos
        errores = PertenenciaModel.validar_datos(descripcion, id_estudiante, estado)
        if errores:
            return {'exito': False, 'errores': errores}

        try:
            # Insertar pertenencia
            query = """
                INSERT INTO pertenencias (descripcion, id_estudiante, estado, fecha_registro)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """
            cursor = db.execute_query(query, (descripcion, id_estudiante, estado))
            db.commit()
            
            # Obtener la pertenencia creada
            pertenencia = PertenenciaModel.obtener_por_id(cursor.lastrowid)
            return {'exito': True, 'pertenencia': pertenencia}
        except Exception as e:
            db.rollback()
            return {'exito': False, 'errores': [str(e)]}

    @staticmethod
    def obtener_por_id(id: int) -> Optional[Pertenencia]:
        """Obtiene una pertenencia por su ID"""
        query = """
            SELECT id, descripcion, fecha_registro, estado, id_estudiante
            FROM pertenencias 
            WHERE id = ?
        """
        resultado = db.fetch_one(query, (id,))
        if not resultado:
            return None
            
        return Pertenencia(
            id=resultado[0],
            descripcion=resultado[1],
            fecha_registro=datetime.strptime(resultado[2], "%Y-%m-%d %H:%M:%S"),
            estado=resultado[3],
            id_estudiante=resultado[4]
        )

    @staticmethod
    def obtener_detallado_por_id(id: int) -> Optional[PertenenciaDetallada]:
        """Obtiene una pertenencia con detalles del estudiante por su ID"""
        query = """
            SELECT 
                p.id, p.descripcion, p.fecha_registro, p.estado, p.id_estudiante,
                e.codigo, e.nombres, e.carrera, e.plan
            FROM pertenencias p
            JOIN estudiantes e ON p.id_estudiante = e.id
            WHERE p.id = ?
        """
        resultado = db.fetch_one(query, (id,))
        if not resultado:
            return None
            
        return PertenenciaDetallada(
            id=resultado[0],
            descripcion=resultado[1],
            fecha_registro=datetime.strptime(resultado[2], "%Y-%m-%d %H:%M:%S"),
            estado=resultado[3],
            id_estudiante=resultado[4],
            codigo_estudiante=resultado[5],
            nombre_estudiante=resultado[6],
            carrera_estudiante=resultado[7],
            plan_estudiante=resultado[8]
        )

    @staticmethod
    def listar_por_estudiante(id_estudiante: int) -> List[Pertenencia]:
        """Lista todas las pertenencias de un estudiante"""
        query = """
            SELECT id, descripcion, fecha_registro, estado, id_estudiante
            FROM pertenencias
            WHERE id_estudiante = ?
            ORDER BY fecha_registro DESC
        """
        resultados = db.fetch_all(query, (id_estudiante,))
        return [
            Pertenencia(
                id=r[0],
                descripcion=r[1],
                fecha_registro=datetime.strptime(r[2], "%Y-%m-%d %H:%M:%S"),
                estado=r[3],
                id_estudiante=r[4]
            ) for r in resultados
        ]

    @staticmethod
    def buscar(
        datos_estudiante: str = "",
        estado: str = "",
        descripcion: str = ""
    ) -> List[PertenenciaDetallada]:
        """Busca pertenencias con filtros"""
        query = """
            SELECT 
                p.id, p.descripcion, p.fecha_registro, p.estado, p.id_estudiante,
                e.codigo, e.nombres, e.carrera, e.plan
            FROM pertenencias p
            JOIN estudiantes e ON p.id_estudiante = e.id
            WHERE 1=1
        """
        params = []
        
        if datos_estudiante:
            query += " AND (e.nombres LIKE ? OR e.codigo LIKE ?)"
            params.extend([f"%{datos_estudiante}%", f"%{datos_estudiante}%"])
            
        if estado:
            query += " AND p.estado = ?"
            params.append(estado)
            
        if descripcion:
            query += " AND p.descripcion LIKE ?"
            params.append(f"%{descripcion}%")
            
        query += " ORDER BY p.fecha_registro DESC"
        
        resultados = db.fetch_all(query, tuple(params))
        return [
            PertenenciaDetallada(
                id=r[0],
                descripcion=r[1],
                fecha_registro=datetime.strptime(r[2], "%Y-%m-%d %H:%M:%S"),
                estado=r[3],
                id_estudiante=r[4],
                codigo_estudiante=r[5],
                nombre_estudiante=r[6],
                carrera_estudiante=r[7],
                plan_estudiante=r[8]
            ) for r in resultados
        ]

    @staticmethod
    def actualizar_estado(id: int, nuevo_estado: str) -> Dict:
        """Actualiza el estado de una pertenencia"""
        if nuevo_estado not in PertenenciaModel.ESTADOS_VALIDOS:
            return {
                'exito': False,
                'errores': [f"Estado inválido. Debe ser uno de: {', '.join(PertenenciaModel.ESTADOS_VALIDOS)}"]
            }

        try:
            query = """
                UPDATE pertenencias
                SET estado = ?
                WHERE id = ?
            """
            db.execute_query(query, (nuevo_estado, id))
            db.commit()
            
            pertenencia = PertenenciaModel.obtener_por_id(id)
            return {'exito': True, 'pertenencia': pertenencia}
        except Exception as e:
            db.rollback()
            return {'exito': False, 'errores': [str(e)]} 