import cv2
from utils.deteccion_objetos import DeteccionObjetos
from utils.comparar_pertenencia import ordenar_imagenes_por_similitud

from models.pertenencia import Pertenencia,BaseDatosPertenencia
from datetime import datetime
import os
from flask import  send_from_directory,current_app
import base64


class PertenenciasService:
    def __init__(self):
        pass


    def consultar_pertencias_estudiante_busqueda(datosEstudainte,estadoRegistros,codigoPertenencia):
        try:
            base_datos_pertenencia = BaseDatosPertenencia("basededatos.db")
            pertenencias=base_datos_pertenencia.consultar_pertencias_estudiante_busqueda(datosEstudainte,estadoRegistros,codigoPertenencia)
            registros_dic=[]
            for p in pertenencias:
                    UPLOAD_FOLDER = 'uploads/pertenencia'
                    imagen_path = os.path.join(current_app.root_path, UPLOAD_FOLDER, p.imagen_pertenencia)
                    with open(imagen_path, 'rb') as imagen_file:
                        imagen_base64 = base64.b64encode(imagen_file.read()).decode('utf-8')
                    pertenencia_dict = {
                        'codigo_pertenencia': p.codigo_pertenencia,
                        'tipo_objeto': p.tipo_objeto,
                        'nombre_objeto': p.objeto_text,
                        'hora_ultima_actividad': p.fecha_ultima_actividad,
                        'id_estado': p.id_ultimo_estado,
                        'nombre_estado': p.estado_text,
                        'imagen_pertenencia': f'data:image/jpeg;base64,{imagen_base64}',
                        'id_estudiante': p.id_estudiante,
                        'codigo_estudiante': p.codigo_estudiante,
                        'nombres_estudiante': p.nombres_estudiante,
                        'carrera_estudiante': p.carrera_estudiante,
                        'plan_estudiante': p.plan_estudiante
                    }
                    registros_dic.append(pertenencia_dict)
            return registros_dic
        except Exception as e:
            print(f"Error al registrar salida de perteencia {e}")
            return -1
