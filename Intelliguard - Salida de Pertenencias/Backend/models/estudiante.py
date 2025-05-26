import sqlite3

class Estudiante:
    def __init__(self, id_estudiante, nombres, codigo_estudiante,carrera,planEstudiante):
        self.id_estudiante = id_estudiante
        self.nombres = nombres
        self.codigo_estudiante = codigo_estudiante
        self.carrera = carrera
        self.planEstudiante = planEstudiante

class BaseDatosEstudiantes:
    def __init__(self, nombre_archivo):
        self.conexion = sqlite3.connect(nombre_archivo)
        self.cursor = self.conexion.cursor()
        self.crear_tabla_estudiantes()

    def crear_tabla_estudiantes(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS estudiantes (
                                idEstudiante INTEGER PRIMARY KEY AUTOINCREMENT,
                                Nombres TEXT,
                                codigoEstudiante TEXT,
                                Carrera TEXT,
                                planEstudiante TEXT)''')
        self.conexion.commit()

    def guardar_estudiante(self, estudiante):
        # Verificar si el estudiante ya está registrado
        if self.consultar_estudiante_por_codigo(estudiante.codigo_estudiante):
            print(f"El estudiante con código {estudiante.codigo_estudiante} ya está registrado.")
            return
        self.cursor.execute("INSERT INTO estudiantes (Nombres, codigoEstudiante,Carrera,planEstudiante) VALUES (?, ?,?,?)", (estudiante.nombres, estudiante.codigo_estudiante, estudiante.carrera, estudiante.planEstudiante))
        self.conexion.commit()

    def consultar_estudiante_por_codigo(self, codigo_estudiante):
        self.cursor.execute("SELECT * FROM estudiantes WHERE codigoEstudiante = ?", (codigo_estudiante,))
        resultado = self.cursor.fetchone()
        if resultado:
            return Estudiante(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4])
        else:
            return None
        
    def borrar_todos_los_estudiantes(self):
        self.cursor.execute("DELETE FROM estudiantes")
        self.conexion.commit()