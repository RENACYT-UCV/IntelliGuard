from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
from ..database.db_manager import db

@dataclass
class Reporte:
    id: int
    id_pertenencia: int
    tipo: str
    fecha: datetime
    detalles: str
    estado: str

@dataclass
class ReporteDetallado:
    id: int
    id_pertenencia: int
    tipo: str
    fecha: datetime
    detalles: str
    estado: str
    descripcion_pertenencia: str
    codigo_estudiante: str
    nombre_estudiante: str
    carrera_estudiante: str
    plan_estudiante: str

class ReporteModel:
    TABLA = 'reportes'
    TIPOS_VALIDOS = ['entrada', 'salida', 'perdida', 'recuperacion']

    @staticmethod
    def validar_datos(id_pertenencia: int, tipo: str, detalles: str) -> List[str]:
        """Valida los datos de un reporte"""
        errores = []
        
        if not isinstance(id_pertenencia, int) or id_pertenencia <= 0:
            errores.append("El ID de la pertenencia es inválido")
            
        if not tipo or tipo not in ReporteModel.TIPOS_VALIDOS:
            errores.append(f"El tipo debe ser uno de: {', '.join(ReporteModel.TIPOS_VALIDOS)}")
            
        if not detalles or not isinstance(detalles, str) or len(detalles) < 5:
            errores.append("Los detalles deben tener al menos 5 caracteres")
            
        return errores

    @staticmethod
    def crear(id_pertenencia: int, tipo: str, detalles: str) -> Dict:
        """Crea un nuevo reporte"""
        # Validar datos
        errores = ReporteModel.validar_datos(id_pertenencia, tipo, detalles)
        if errores:
            return {'exito': False, 'errores': errores}

        try:
            # Obtener el estado actual de la pertenencia
            query_estado = """
                SELECT estado FROM pertenencias WHERE id = ?
            """
            resultado = db.fetch_one(query_estado, (id_pertenencia,))
            if not resultado:
                return {'exito': False, 'errores': ['La pertenencia no existe']}

            estado_actual = resultado[0]

            # Insertar reporte
            query = """
                INSERT INTO reportes (id_pertenencia, tipo, fecha, detalles, estado)
                VALUES (?, ?, CURRENT_TIMESTAMP, ?, ?)
            """
            cursor = db.execute_query(query, (id_pertenencia, tipo, detalles, estado_actual))
            db.commit()
            
            # Obtener el reporte creado
            reporte = ReporteModel.obtener_por_id(cursor.lastrowid)
            return {'exito': True, 'reporte': reporte}
        except Exception as e:
            db.rollback()
            return {'exito': False, 'errores': [str(e)]}

    @staticmethod
    def obtener_por_id(id: int) -> Optional[Reporte]:
        """Obtiene un reporte por su ID"""
        query = """
            SELECT id, id_pertenencia, tipo, fecha, detalles, estado
            FROM reportes 
            WHERE id = ?
        """
        resultado = db.fetch_one(query, (id,))
        if not resultado:
            return None
            
        return Reporte(
            id=resultado[0],
            id_pertenencia=resultado[1],
            tipo=resultado[2],
            fecha=datetime.strptime(resultado[3], "%Y-%m-%d %H:%M:%S"),
            detalles=resultado[4],
            estado=resultado[5]
        )

    @staticmethod
    def obtener_detallado_por_id(id: int) -> Optional[ReporteDetallado]:
        """Obtiene un reporte con detalles por su ID"""
        query = """
            SELECT 
                r.id, r.id_pertenencia, r.tipo, r.fecha, r.detalles, r.estado,
                p.descripcion, e.codigo, e.nombres, e.carrera, e.plan
            FROM reportes r
            JOIN pertenencias p ON r.id_pertenencia = p.id
            JOIN estudiantes e ON p.id_estudiante = e.id
            WHERE r.id = ?
        """
        resultado = db.fetch_one(query, (id,))
        if not resultado:
            return None
            
        return ReporteDetallado(
            id=resultado[0],
            id_pertenencia=resultado[1],
            tipo=resultado[2],
            fecha=datetime.strptime(resultado[3], "%Y-%m-%d %H:%M:%S"),
            detalles=resultado[4],
            estado=resultado[5],
            descripcion_pertenencia=resultado[6],
            codigo_estudiante=resultado[7],
            nombre_estudiante=resultado[8],
            carrera_estudiante=resultado[9],
            plan_estudiante=resultado[10]
        )

    @staticmethod
    def listar_por_pertenencia(id_pertenencia: int) -> List[Reporte]:
        """Lista todos los reportes de una pertenencia"""
        query = """
            SELECT id, id_pertenencia, tipo, fecha, detalles, estado
            FROM reportes
            WHERE id_pertenencia = ?
            ORDER BY fecha DESC
        """
        resultados = db.fetch_all(query, (id_pertenencia,))
        return [
            Reporte(
                id=r[0],
                id_pertenencia=r[1],
                tipo=r[2],
                fecha=datetime.strptime(r[3], "%Y-%m-%d %H:%M:%S"),
                detalles=r[4],
                estado=r[5]
            ) for r in resultados
        ]

    @staticmethod
    def buscar(
        datos_estudiante: str = "",
        tipo: str = "",
        fecha_inicio: str = "",
        fecha_fin: str = ""
    ) -> List[ReporteDetallado]:
        """Busca reportes con filtros"""
        query = """
            SELECT 
                r.id, r.id_pertenencia, r.tipo, r.fecha, r.detalles, r.estado,
                p.descripcion, e.codigo, e.nombres, e.carrera, e.plan
            FROM reportes r
            JOIN pertenencias p ON r.id_pertenencia = p.id
            JOIN estudiantes e ON p.id_estudiante = e.id
            WHERE 1=1
        """
        params = []
        
        if datos_estudiante:
            query += " AND (e.nombres LIKE ? OR e.codigo LIKE ?)"
            params.extend([f"%{datos_estudiante}%", f"%{datos_estudiante}%"])
            
        if tipo:
            query += " AND r.tipo = ?"
            params.append(tipo)
            
        if fecha_inicio:
            query += " AND r.fecha >= ?"
            params.append(fecha_inicio)
            
        if fecha_fin:
            query += " AND r.fecha <= ?"
            params.append(fecha_fin)
            
        query += " ORDER BY r.fecha DESC"
        
        resultados = db.fetch_all(query, tuple(params))
        return [
            ReporteDetallado(
                id=r[0],
                id_pertenencia=r[1],
                tipo=r[2],
                fecha=datetime.strptime(r[3], "%Y-%m-%d %H:%M:%S"),
                detalles=r[4],
                estado=r[5],
                descripcion_pertenencia=r[6],
                codigo_estudiante=r[7],
                nombre_estudiante=r[8],
                carrera_estudiante=r[9],
                plan_estudiante=r[10]
            ) for r in resultados
        ] 