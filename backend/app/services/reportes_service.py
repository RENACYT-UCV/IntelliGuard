from ..models.reporte import BaseDatosReportes
from ..models.pertenencia import BaseDatosPertenencia
from openpyxl import Workbook
from io import BytesIO

class ReportesService:
    @staticmethod
    def consultar_reporte_completo(datos_estudiante="", estado_registros="", codigo_pertenencia=""):
        try:
            # Consultar pertenencias
            db_pertenencias = BaseDatosPertenencia("basededatos.db")
            pertenencias = db_pertenencias.consultar_pertenencias_estudiante_busqueda(
                datos_estudiante, estado_registros, codigo_pertenencia
            )

            # Consultar registros
            db_reportes = BaseDatosReportes("basededatos.db")
            registros = db_reportes.consultar_registros_pertenencia_busqueda(
                datos_estudiante, estado_registros, codigo_pertenencia
            )

            if not pertenencias or not registros:
                return -1

            return {
                'pertenencias': [vars(p) for p in pertenencias],
                'registros': [vars(r) for r in registros]
            }
        except Exception as e:
            print(f"Error en consultar_reporte_completo: {str(e)}")
            return -1

    @staticmethod
    def generar_excel_reporte():
        try:
            db_reportes = BaseDatosReportes("basededatos.db")
            registros = db_reportes.consultar_registros_pertenencia_busqueda()

            # Crear un archivo Excel en memoria
            wb = Workbook()
            ws = wb.active
            ws.title = "Pertenencias"

            # Definir encabezados
            headers = [
                'ID Registro',
                'Estado',
                'Hora Entrada',
                'Hora Salida',
                'Cod Estudiante',
                'Nombres Estudiante',
                'Código Pertenencia',
                'Nombre Objeto'
            ]
            ws.append(headers)

            # Agregar datos
            if registros and isinstance(registros, list):
                for registro in registros:
                    ws.append([
                        registro.id_registro,
                        registro.estado,
                        registro.hora_entrada,
                        registro.hora_salida,
                        registro.id_estudiante,
                        registro.nombres_estudiante,
                        registro.codigo_pertenencia,
                        registro.nombre_objeto
                    ])

            # Guardar en buffer
            excel_buffer = BytesIO()
            wb.save(excel_buffer)
            excel_buffer.seek(0)

            return excel_buffer
        except Exception as e:
            print(f"Error en generar_excel_reporte: {str(e)}")
            return None 