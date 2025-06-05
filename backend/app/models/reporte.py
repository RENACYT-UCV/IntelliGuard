import sqlite3
from datetime import datetime

class ReportePertenencia:
    def __init__(self, id_registro, estado, hora_entrada, hora_salida, id_estudiante, nombres_estudiante, codigo_pertenencia, nombre_objeto):
        self.id_registro = id_registro
        self.estado = estado
        self.hora_entrada = hora_entrada
        self.hora_salida = hora_salida
        self.id_estudiante = id_estudiante
        self.nombres_estudiante = nombres_estudiante
        self.codigo_pertenencia = codigo_pertenencia
        self.nombre_objeto = nombre_objeto

class BaseDatosReportes:
    def __init__(self, nombre_archivo):
        self.conexion = sqlite3.connect(nombre_archivo)
        self.cursor = self.conexion.cursor()

    def consultar_registros_pertenencia_busqueda(self, datos_estudiante="", estado_pertenencia="", codigo_pertenencia=""):
        query = """
            SELECT r.idRegistro, ep.estado, r.horaEntrada, r.horaSalida, 
                   e.codigoEstudiante, e.Nombres, p.codigoPertenencia, o.Nombre
            FROM registros_pertenencia r
            JOIN pertenencias p ON r.idPertenencia = p.codigoPertenencia
            JOIN estado_pertenencias ep ON r.idEstado = ep.id
            JOIN estudiantes e ON p.idEstudiante = e.idEstudiante
            JOIN objetos o ON p.tipoObjeto = o.idObjeto
            WHERE 1=1
        """
        params = []
        
        if datos_estudiante:
            query += " AND (e.Nombres LIKE ? OR e.codigoEstudiante LIKE ?)"
            params.extend([f"%{datos_estudiante}%", f"%{datos_estudiante}%"])
        
        if estado_pertenencia:
            query += " AND ep.estado LIKE ?"
            params.append(f"%{estado_pertenencia}%")
        
        if codigo_pertenencia:
            query += " AND p.codigoPertenencia LIKE ?"
            params.append(f"%{codigo_pertenencia}%")

        self.cursor.execute(query, tuple(params))
        resultados = self.cursor.fetchall()
        registros = []

        for resultado in resultados:
            registro = ReportePertenencia(
                id_registro=resultado[0],
                estado=resultado[1],
                hora_entrada=resultado[2],
                hora_salida=resultado[3],
                id_estudiante=resultado[4],
                nombres_estudiante=resultado[5],
                codigo_pertenencia=resultado[6],
                nombre_objeto=resultado[7]
            )
            registros.append(registro)

        registros_ordenados = sorted(
            registros,
            key=lambda x: datetime.strptime(x.hora_entrada, "%Y-%m-%d_%H-%M-%S"),
            reverse=True
        )
        return registros_ordenados 