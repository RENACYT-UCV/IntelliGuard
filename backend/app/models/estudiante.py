import sqlite3
from ..utils.db import get_db_connection

class Estudiante:
    def __init__(self, codigo, nombres, carrera, plan):
        self.codigo = codigo
        self.nombres = nombres
        self.carrera = carrera
        self.plan = plan
        
    def validar(self):
        errores = []
        
        if not self.codigo or not isinstance(self.codigo, str) or len(self.codigo) < 3:
            errores.append("El código debe tener al menos 3 caracteres")
            
        if not self.nombres or not isinstance(self.nombres, str) or len(self.nombres) < 3:
            errores.append("El nombre debe tener al menos 3 caracteres")
            
        if not self.carrera or not isinstance(self.carrera, str):
            errores.append("La carrera es requerida")
            
        if not self.plan or not isinstance(self.plan, str):
            errores.append("El plan es requerido")
            
        return errores
    
    def guardar(self):
        errores = self.validar()
        if errores:
            return False, errores
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Verificar si ya existe
            cursor.execute('SELECT codigo FROM estudiantes WHERE codigo = ?', (self.codigo,))
            if cursor.fetchone():
                return False, ["El estudiante ya está registrado"]
                
            # Insertar nuevo estudiante
            cursor.execute('''
                INSERT INTO estudiantes (codigo, nombres, carrera, plan)
                VALUES (?, ?, ?, ?)
            ''', (self.codigo, self.nombres, self.carrera, self.plan))
            
            conn.commit()
            return True, []
            
        except Exception as e:
            return False, [str(e)]
        finally:
            conn.close()
    
    @staticmethod
    def obtener_por_codigo(codigo):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT codigo, nombres, carrera, plan 
                FROM estudiantes 
                WHERE codigo = ?
            ''', (codigo,))
            
            estudiante = cursor.fetchone()
            
            if estudiante:
                return Estudiante(
                    codigo=estudiante[0],
                    nombres=estudiante[1],
                    carrera=estudiante[2],
                    plan=estudiante[3]
                )
            return None
            
        finally:
            conn.close() 