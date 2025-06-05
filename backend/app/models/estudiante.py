from dataclasses import dataclass
from typing import Optional, List, Tuple
from ..database.db_manager import db

@dataclass
class Estudiante:
    id: int
    codigo: str
    nombres: str
    carrera: str
    plan: str

class EstudianteModel:
    TABLA = 'estudiantes'

    @staticmethod
    def validar_datos(codigo: str, nombres: str, carrera: str, plan: str) -> List[str]:
        """Valida los datos de un estudiante"""
        errores = []
        
        if not codigo or not isinstance(codigo, str) or len(codigo) < 3:
            errores.append("El código debe tener al menos 3 caracteres")
            
        if not nombres or not isinstance(nombres, str) or len(nombres) < 3:
            errores.append("El nombre debe tener al menos 3 caracteres")
            
        if not carrera or not isinstance(carrera, str):
            errores.append("La carrera es requerida")
            
        if not plan or not isinstance(plan, str):
            errores.append("El plan es requerido")
            
        return errores

    @staticmethod
    def crear(codigo: str, nombres: str, carrera: str, plan: str) -> Tuple[bool, List[str]]:
        """Crea un nuevo estudiante"""
        # Validar datos
        errores = EstudianteModel.validar_datos(codigo, nombres, carrera, plan)
        if errores:
            return False, errores

        try:
            # Verificar si ya existe
            if EstudianteModel.obtener_por_codigo(codigo):
                return False, ["El estudiante ya está registrado"]

            # Insertar nuevo estudiante
            query = """
                INSERT INTO estudiantes (codigo, nombres, carrera, plan)
                VALUES (?, ?, ?, ?)
            """
            db.execute_query(query, (codigo, nombres, carrera, plan))
            db.commit()
            return True, []
        except Exception as e:
            db.rollback()
            return False, [str(e)]

    @staticmethod
    def obtener_por_codigo(codigo: str) -> Optional[Estudiante]:
        """Obtiene un estudiante por su código"""
        query = """
            SELECT id, codigo, nombres, carrera, plan 
            FROM estudiantes 
            WHERE codigo = ?
        """
        resultado = db.fetch_one(query, (codigo,))
        return Estudiante(*resultado) if resultado else None

    @staticmethod
    def obtener_por_id(id: int) -> Optional[Estudiante]:
        """Obtiene un estudiante por su ID"""
        query = """
            SELECT id, codigo, nombres, carrera, plan 
            FROM estudiantes 
            WHERE id = ?
        """
        resultado = db.fetch_one(query, (id,))
        return Estudiante(*resultado) if resultado else None

    @staticmethod
    def listar_todos() -> List[Estudiante]:
        """Lista todos los estudiantes"""
        query = """
            SELECT id, codigo, nombres, carrera, plan 
            FROM estudiantes
        """
        resultados = db.fetch_all(query)
        return [Estudiante(*resultado) for resultado in resultados]

    @staticmethod
    def actualizar(id: int, codigo: str, nombres: str, carrera: str, plan: str) -> Tuple[bool, List[str]]:
        """Actualiza un estudiante existente"""
        # Validar datos
        errores = EstudianteModel.validar_datos(codigo, nombres, carrera, plan)
        if errores:
            return False, errores

        try:
            # Verificar si existe
            estudiante_actual = EstudianteModel.obtener_por_id(id)
            if not estudiante_actual:
                return False, ["El estudiante no existe"]

            # Verificar si el nuevo código ya existe (si se está cambiando)
            if codigo != estudiante_actual.codigo:
                estudiante_existente = EstudianteModel.obtener_por_codigo(codigo)
                if estudiante_existente:
                    return False, ["El código ya está registrado para otro estudiante"]

            # Actualizar estudiante
            query = """
                UPDATE estudiantes 
                SET codigo = ?, nombres = ?, carrera = ?, plan = ?
                WHERE id = ?
            """
            db.execute_query(query, (codigo, nombres, carrera, plan, id))
            db.commit()
            return True, []
        except Exception as e:
            db.rollback()
            return False, [str(e)]

    @staticmethod
    def eliminar(id: int) -> Tuple[bool, List[str]]:
        """Elimina un estudiante"""
        try:
            # Verificar si existe
            if not EstudianteModel.obtener_por_id(id):
                return False, ["El estudiante no existe"]

            # Eliminar estudiante
            query = "DELETE FROM estudiantes WHERE id = ?"
            db.execute_query(query, (id,))
            db.commit()
            return True, []
        except Exception as e:
            db.rollback()
            return False, [str(e)]

    @staticmethod
    def buscar_por_nombre(nombre: str) -> List[Estudiante]:
        """Busca estudiantes por nombre"""
        query = """
            SELECT id, codigo, nombres, carrera, plan 
            FROM estudiantes 
            WHERE nombres LIKE ?
        """
        resultados = db.fetch_all(query, (f"%{nombre}%",))
        return [Estudiante(*resultado) for resultado in resultados] 