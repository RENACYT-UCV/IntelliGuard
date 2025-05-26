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
    
    def consultar_registros_pertenencia_por_codigo(self, codigo_pertenencia):
        try:
            query = """
                SELECT rp.*, ep.estado, o.Nombre AS nombreObjeto, e.Nombres AS nombreEstudiante
                FROM registros_pertenencia rp
                JOIN objetos o ON rp.idObjeto = o.idObjeto
                JOIN estudiantes e ON rp.idEstudiante = e.idEstudiante
                JOIN estado_pertenencias ep ON rp.idEstado = ep.id
                WHERE rp.codigoPertenencia = ?
            """
            self.cursor.execute(query, (codigo_pertenencia,))
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
            return pertenencias if pertenencias else None
        except sqlite3.Error as e:
            print(f"Error al consultar la pertenencia: {e}")
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
        
    def consultar_registros_por_estado_estudiante(self, id_estado, id_estudiante):
        try:
            query = """
                SELECT rp.*, ep.estado, o.Nombre AS nombreObjeto, e.Nombres AS nombreEstudiante
                FROM registros_pertenencia rp
                JOIN objetos o ON rp.idObjeto = o.idObjeto
                JOIN estudiantes e ON rp.idEstudiante = e.idEstudiante
                JOIN estado_pertenencias ep ON rp.idEstado = ep.id
                WHERE rp.idEstado = ? AND rp.idEstudiante = ?
            """
            self.cursor.execute(query, (id_estado, id_estudiante))
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
            return pertenencias if pertenencias else None
        except sqlite3.Error as e:
            print(f"Error al consultar la pertenencia: {e}")
            return -1
        
    def actualizar_hora_estado_registro(self, codPertenencia, idEstado, fecha_hora_actual):
        try:
            fecha_actual = fecha_hora_actual.split("_")[0]
            print(fecha_actual)
            self.cursor.execute('''UPDATE registros_pertenencia
                                SET idEstado = ?, Hora_Salida = ?
                                WHERE codigoPertenencia = ? AND substr(Hora_Entrada, 1, 10) = ? AND Hora_Salida IS NULL''',
                                (idEstado, fecha_hora_actual, codPertenencia, fecha_actual))
            if self.cursor.rowcount == 0:
                print(f"No se encontró ninguna registro_pertenencia con código {codPertenencia} para la fecha {fecha_actual}")
                return False
            self.conexion.commit()
            print(f"completado")
            return True
        except sqlite3.Error as e:
            print(f"Error al actualizar el estado de la pertenencia: {e}")
            self.conexion.rollback()
            return False

    def consultar_pertenencias_por_estudiante_y_tipo(self, id_estudiante, tipo_objeto):
        try:
            query = """
                SELECT rp.*, e.Nombres, e.codigoEstudiante
                FROM registros_pertenencia rp
                JOIN estudiantes e ON rp.idEstudiante = e.idEstudiante
                JOIN pertenencias p ON rp.codigoPertenencia = p.codigoPertenencia
                WHERE rp.idEstudiante = ? AND p.tipoObjeto = ?
            """
            self.cursor.execute(query, (id_estudiante, tipo_objeto))
            resultados = self.cursor.fetchall()
            if resultados:
                return resultados
            else:
                return -1
        except sqlite3.Error as e:
            print(f"Error al consultar las pertenencias: {e}")
            return -1

    def consultar_registros_pertencia_busqueda(self, datosEstudiante="", estadoRegistros="", codigoPertenencia=""):
        try:
            query = """
                SELECT rp.*, ep.estado, o.Nombre AS nombreObjeto, e.Nombres AS nombreEstudiante, e.codigoEstudiante AS codEstud
                FROM registros_pertenencia rp
                JOIN objetos o ON rp.idObjeto = o.idObjeto
                JOIN estudiantes e ON rp.idEstudiante = e.idEstudiante
                JOIN estado_pertenencias ep ON rp.idEstado = ep.id
                WHERE 1=1
            """
            params = []
            if datosEstudiante:
                query += " AND (e.Nombres LIKE ? OR e.codigoEstudiante LIKE ?)"
                params.extend([f"%{datosEstudiante}%", f"%{datosEstudiante}%"])
            if estadoRegistros:
                query += " AND ep.estado LIKE ?"
                params.append(f"%{estadoRegistros}%")
            if codigoPertenencia:
                query += " AND rp.codigoPertenencia LIKE ?"
                params.append(f"%{codigoPertenencia}%")
            self.cursor.execute(query, tuple(params))
            resultados = self.cursor.fetchall()
            pertenencias = []
            for resultado in resultados:
                pertenencia = RegistrosPertenencia(
                    id_registro=resultado[0],
                    id_estudiante=resultado[11],
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
            return pertenencias if pertenencias else None
        except sqlite3.Error as e:
            print(f"Error al consultar la pertenencia: {e}")
            return -1








































#     def guardar_pertenencia(self, id_estudiante, id_objeto, idEstado, fecha, imagen_pertenencia):
#         try:
#             self.cursor.execute('''INSERT INTO registros_pertenencia 
#                                    (idEstudiante, idObjeto, idEstado, Fecha, imagenPertenencia) 
#                                    VALUES (?, ?, ?, ?, ?)''',
#                                 (id_estudiante, id_objeto, idEstado, fecha, imagen_pertenencia))
#             self.conexion.commit()
#         except sqlite3.Error as e:
#             print(f"Error al guardar la pertenencia: {e}")
#             self.conexion.rollback()
#             return -1
#         return 1
    
#     def consultar_pertencia_por_idEstudiante_fecha(self, idEstudiante, idEstado, fecha_actual):
#         query = """
#         SELECT rp.*, ep.estado AS Estado, o.Nombre AS nombreObjeto, e.Nombres AS nombreEstudiante
#         FROM registros_pertenencia rp
#         JOIN objetos o ON rp.idObjeto = o.idObjeto
#         JOIN estudiantes e ON rp.idEstudiante = e.idEstudiante
#         JOIN estado_pertenencias ep ON rp.idEstado = ep.id
#         WHERE rp.idEstudiante = ? AND rp.idEstado = ?
#         """
#         self.cursor.execute(query, (idEstudiante, idEstado))
#         resultados = self.cursor.fetchall()
#         pertenencias = []

#         for resultado in resultados:
#             pertenencia = RegistrosPertenencia(
#                 id_pertenencia=resultado[0],
#                 id_estudiante=resultado[1],
#                 id_objeto=resultado[2],
#                 fecha=resultado[3],
#                 imagen_pertenencia=resultado[4],
#                 id_estado=resultado[5],
#                 estado=resultado[6],
#                 nombre_objeto=resultado[7],
#                 nombres_estudiante=resultado[8]
#             )
#             pertenencias.append(pertenencia)

#         return pertenencias
    
#     def consultar_pertenencias_por_busqueda(self, busqueda):
#         script_sql = """
#             SELECT rp.*, ep.estado AS Estado , o.Nombre AS nombreObjeto, e.Nombres AS nombreEstudiante
#             FROM registros_pertenencia rp
#             JOIN objetos o ON rp.idObjeto = o.idObjeto
#             JOIN estudiantes e ON rp.idEstudiante = e.idEstudiante
#             JOIN estado_pertenencias ep ON rp.idEstado = ep.id
#             WHERE e.Nombres LIKE ? OR e.codigoEstudiante LIKE ?;
#         """
#         self.cursor.execute(script_sql, (f"%{busqueda}%", f"%{busqueda}%"))
#         resultados = self.cursor.fetchall()
#         pertenencias = []
#         for resultado in resultados:
#             pertenencia = RegistrosPertenencia(
#                 id_pertenencia=resultado[0],
#                 id_estudiante=resultado[1],
#                 id_objeto=resultado[2],
#                 fecha=resultado[3],
#                 imagen_pertenencia=resultado[4],
#                 id_estado=resultado[5],
#                 estado=resultado[6],
#                 nombre_objeto=resultado[7],
#                 nombres_estudiante=resultado[8]
#             )
#             pertenencias.append(pertenencia)
#         return pertenencias
    
#     # Método en el modelo para cambiar el estado de pertenencias
#     def cambiar_estado_pertenencias(self, id_pertenencia, idEstado):
#         try:
#             # Actualizar el estado de la pertenencia en la base de datos
#             self.cursor.execute('''UPDATE registros_pertenencia 
#                                 SET idEstado = ? 
#                                 WHERE idPertenencia = ?''',
#                                 (idEstado, id_pertenencia))
#             self.conexion.commit()
#             return True
#         except sqlite3.Error as e:
#             print(f"Error al cambiar el estado de la pertenencia: {e}")
#             self.conexion.rollback()
#             return False
        
#     def borrar_todas_las_pertenencias(self):
#         self.cursor.execute("DELETE FROM registros_pertenencia")
#         self.conexion.commit()

#     def obtener_todas_pertenencias(self):
#             query = """
#                 SELECT rp.idPertenencia, e.codigoEstudiante, rp.idObjeto, ep.estado, rp.Fecha, o.Nombre AS nombreObjeto, 
#                 e.Nombres AS nombreEstudiante, rp.imagenPertenencia
#                 FROM registros_pertenencia rp
#                 JOIN objetos o ON rp.idObjeto = o.idObjeto
#                 JOIN estudiantes e ON rp.idEstudiante = e.idEstudiante
#                 JOIN estado_pertenencias ep ON rp.idEstado = ep.id
#             """
#             self.cursor.execute(query)
#             resultados = self.cursor.fetchall()
#             pertenencias = []
#             for resultado in resultados:
#                 pertenencia = RegistrosPertenencia(
#                     id_pertenencia=resultado[0],
#                     id_estudiante=resultado[1],
#                     id_objeto=resultado[2],
#                     id_estado=resultado[3],  
#                     estado=resultado[3],  
#                     fecha=resultado[4],  
#                     nombre_objeto=resultado[5],  
#                     nombres_estudiante=resultado[6], 
#                     imagen_pertenencia=resultado[7] 
#                 )
#                 pertenencias.append(pertenencia)
#             return pertenencias