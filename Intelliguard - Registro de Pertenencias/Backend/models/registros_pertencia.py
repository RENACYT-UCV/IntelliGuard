import sqlite3
from datetime import datetime

class RegistrosPertenencia:
    def __init__(self, id_registro, id_estudiante, id_objeto, id_estado, estado, hora_entrada, codigoPertenencia, hora_salida, imagen_pertenencia,nombre_objeto,nombres_estudiante):
        self.id_registro = id_registro
        self.id_estudiante = id_estudiante
        self.id_objeto = id_objeto
        self.id_estado = id_estado
        self.estado = estado
        self.hora_entrada = hora_entrada
        self.hora_salida = hora_salida
        self.imagen_pertenencia = imagen_pertenencia
        self.codigoPertenencia = codigoPertenencia
        self.nombre_objeto = nombre_objeto  # Nuevo atributo para almacenar el nombre del objeto
        self.nombres_estudiante = nombres_estudiante  # Nuevo atributo para almacenar el nombre del objeto

class BaseDatosRegistrosPertenencia:
    def __init__(self, nombre_archivo):
        self.conexion = sqlite3.connect(nombre_archivo)
        self.cursor = self.conexion.cursor()
        self.crear_tabla_registros_pertenencia()

    def crear_tabla_registros_pertenencia(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS registros_pertenencia (
            idPertenencia INTEGER PRIMARY KEY AUTOINCREMENT,
            idEstudiante INTEGER,
            idObjeto INTEGER,
            idEstado INTEGER,
            codigoPertenencia INTEGER,
            Hora_Entrada DATETIME,
            Hora_Salida DATETIME,
            imagenPertenencia TEXT,
            FOREIGN KEY (idEstudiante) REFERENCES estudiantes(idEstudiante),
            FOREIGN KEY (codigoPertenencia) REFERENCES pertenencias(codigoPertenencia),
            FOREIGN KEY (idObjeto) REFERENCES objetos(idObjeto),
            FOREIGN KEY (idEstado) REFERENCES estado_pertenencias(id)
        )''')
        self.conexion.commit()

    def registrar_registro(self, id_estudiante, id_objeto, id_estado, codigo_pertenencia, hora_entrada, imagen_pertenencia):
        try:
            self.cursor.execute('''INSERT INTO registros_pertenencia 
                                    (idEstudiante, idObjeto, idEstado, codigoPertenencia, Hora_Entrada, Hora_Salida, imagenPertenencia) 
                                    VALUES (?, ?, ?, ?, ?, NULL, ?)''',
                                (id_estudiante, id_objeto, id_estado, codigo_pertenencia, hora_entrada, imagen_pertenencia))
            self.conexion.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error al registrar la pertenencia: {e}")
            self.conexion.rollback()
            return -1
    

    
    def consultar_registros_pertenencia_por_similitud(self, id_estudiante, id_objeto):
        try:
            query = """
                SELECT rp.*, ep.estado, o.Nombre AS nombreObjeto, e.Nombres AS nombreEstudiante
                FROM registros_pertenencia rp
                JOIN objetos o ON rp.idObjeto = o.idObjeto
                JOIN estudiantes e ON rp.idEstudiante = e.idEstudiante
                JOIN estado_pertenencias ep ON rp.idEstado = ep.id
                WHERE rp.idEstudiante = ? AND rp.idObjeto = ?
            """
            self.cursor.execute(query, (id_estudiante,id_objeto))
            resultados = self.cursor.fetchall()
            pertenencias = []
            for resultado in resultados:
                pertenencia = RegistrosPertenencia(
                    id_registro=resultado[0],
                    id_estudiante=resultado[1],
                    id_objeto=resultado[2],
                    hora_entrada=resultado[3],
                    imagen_pertenencia=resultado[4],
                    id_estado=resultado[5],
                    codigoPertenencia=resultado[6],
                    hora_salida=resultado[7],
                    estado=resultado[8],
                    nombre_objeto=resultado[9],
                    nombres_estudiante=resultado[10]
                )
                pertenencias.append(pertenencia)
            return pertenencias if pertenencias else -1
        except sqlite3.Error as e:
            print(f"Error al consultar la pertenencia: {e}")
            return -1













