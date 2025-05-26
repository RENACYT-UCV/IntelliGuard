import sqlite3
from datetime import datetime
class Pertenencia:
    def __init__(self, codigo_pertenencia, tipo_objeto, imagen_pertenencia, id_estudiante,id_ultimo_estado,fecha_ultima_actividad,estado_text,objeto_text):
        self.codigo_pertenencia = codigo_pertenencia
        self.tipo_objeto = tipo_objeto
        self.imagen_pertenencia = imagen_pertenencia
        self.id_estudiante = id_estudiante
        self.id_ultimo_estado = id_ultimo_estado
        self.fecha_ultima_actividad = fecha_ultima_actividad
        self.estado_text = estado_text
        self.objeto_text=objeto_text

class PertenenciaEstudiante:
    def __init__(self, codigo_pertenencia, tipo_objeto, imagen_pertenencia, id_estudiante,id_ultimo_estado,fecha_ultima_actividad,estado_text,objeto_text,codigo_estudiante,nombres_estudiante,carrera_estudiante,plan_estudiante):
        self.codigo_pertenencia = codigo_pertenencia
        self.tipo_objeto = tipo_objeto
        self.imagen_pertenencia = imagen_pertenencia
        self.id_estudiante = id_estudiante
        self.id_ultimo_estado = id_ultimo_estado
        self.fecha_ultima_actividad = fecha_ultima_actividad
        self.estado_text = estado_text
        self.objeto_text=objeto_text
        self.codigo_estudiante=codigo_estudiante
        self.nombres_estudiante=nombres_estudiante
        self.carrera_estudiante=carrera_estudiante
        self.plan_estudiante=plan_estudiante


class BaseDatosPertenencia:
    def __init__(self, nombre_archivo):
        self.conexion = sqlite3.connect(nombre_archivo)
        self.cursor = self.conexion.cursor()
        self.crear_tabla_pertenencias()

    def crear_tabla_pertenencias(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS pertenencias (
                                codigoPertenencia INTEGER PRIMARY KEY AUTOINCREMENT,
                                tipoObjeto INTEGER,
                                imagenPertenencia TEXT,
                                idEstudiante INTEGER,
                                idUltimoEstado INTEGER,
                                FechaUltimaActividad INTEGER,
                                FOREIGN KEY (idUltimoEstado) REFERENCES estado_pertenencias(id),
                                FOREIGN KEY (idEstudiante) REFERENCES estudiantes(idEstudiante))''')
        self.conexion.commit()

        



    

    #queda
    def consultar_pertencias_estudiante_busqueda(self, datosEstudiante="", estadoPertenencia="", codigoPertenencia=""):
        query = """
            SELECT p.codigoPertenencia, p.tipoObjeto, p.imagenPertenencia, p.idEstudiante, p.idUltimoEstado,
                    p.FechaUltimaActividad, ep.estado, o.Nombre, e.codigoEstudiante, e.Nombres, e.Carrera, e.planEstudiante
            FROM pertenencias p
            JOIN estado_pertenencias ep ON p.idUltimoEstado = ep.id
            JOIN objetos o ON p.tipoObjeto = o.idObjeto
            JOIN estudiantes e ON p.idEstudiante = e.idEstudiante
            WHERE 1=1
        """
        params = []
        if datosEstudiante:
            query += " AND (e.Nombres LIKE ? OR e.codigoEstudiante LIKE ?)"
            params.extend([f"%{datosEstudiante}%", f"%{datosEstudiante}%"])
        if estadoPertenencia:
            query += " AND ep.estado LIKE ?"
            params.append(f"%{estadoPertenencia}%")
        if codigoPertenencia:
            query += " AND p.codigoPertenencia LIKE ?"
            params.append(f"%{codigoPertenencia}%")
        self.cursor.execute(query, tuple(params))
        resultados = self.cursor.fetchall()
        pertenencias = []
        for resultado in resultados:
            pertenenciaEstudiante = PertenenciaEstudiante(
                codigo_pertenencia=resultado[0],
                tipo_objeto=resultado[1],
                imagen_pertenencia=resultado[2],
                id_estudiante=resultado[3],
                id_ultimo_estado=resultado[4],
                fecha_ultima_actividad=resultado[5],
                estado_text=resultado[6],
                objeto_text=resultado[7],
                codigo_estudiante=resultado[8],
                nombres_estudiante=resultado[9],
                carrera_estudiante=resultado[10],
                plan_estudiante=resultado[11]
            )
            pertenencias.append(pertenenciaEstudiante)
        pertenencias_ordenadas = sorted(pertenencias, 
                                        key=lambda x: datetime.strptime(x.fecha_ultima_actividad, "%Y-%m-%d_%H-%M-%S"),reverse=True)
        return pertenencias_ordenadas

    

