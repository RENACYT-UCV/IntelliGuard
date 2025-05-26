import cv2
from utils.deteccion_objetos import DeteccionObjetos
from utils.comparar_pertenencia import ordenar_imagenes_por_similitud
from models.objeto import Objeto,BaseDatosObjetos
from models.registros_pertencia import RegistrosPertenencia,BaseDatosRegistrosPertenencia
from models.pertenencia import Pertenencia,BaseDatosPertenencia
from datetime import datetime
import os
from flask import  send_from_directory,current_app
import base64


class ObjetoService:
    def __init__(self):
        # Aquí podrías inicializar cualquier cosa necesaria para tu servicio
        pass

    def identificar_objeto_pertenencia(img_file,idEstudiante):
        imagen = cv2.imread(img_file)
        posicion, imagenRecortada=DeteccionObjetos.identificarObjeto(imagen)
        if posicion == -1:
            return "no object", None, None
        else:
            base_datos_objetos = BaseDatosObjetos("basededatos.db")
            base_datos_pertenencia = BaseDatosPertenencia("basededatos.db")
            base_datos_registrosPertenencia = BaseDatosRegistrosPertenencia("basededatos.db")
            objeto = base_datos_objetos.consultar_objeto_por_id(posicion)
            registrosPertenecia=base_datos_registrosPertenencia.consultar_registros_pertenencia_por_similitud(idEstudiante,objeto.id_objeto)
            if registrosPertenecia == -1:
                return "no pertenencia", objeto, imagenRecortada
            else:
                resultados_finales = ordenar_imagenes_por_similitud(imagenRecortada, registrosPertenecia)
                pertenencias = base_datos_pertenencia.consultar_pertenencias_codigos(resultados_finales)
                pertenencias_dict = []
                for p in pertenencias:
                    UPLOAD_FOLDER = 'uploads/pertenencia'
                    imagen_path = os.path.join(current_app.root_path, UPLOAD_FOLDER, p.imagen_pertenencia)
                    with open(imagen_path, 'rb') as imagen_file:
                        imagen_base64 = base64.b64encode(imagen_file.read()).decode('utf-8')
                    pertenencia_dict = {
                        'codigo_pertenencia': p.codigo_pertenencia,
                        'tipo_objeto': p.tipo_objeto,
                        'imagen_pertenencia': f'data:image/jpeg;base64,{imagen_base64}',
                        'id_estudiante': p.id_estudiante,
                        'id_ultimo_estado': p.id_ultimo_estado,
                        'fecha_ultima_actividad': p.fecha_ultima_actividad,
                        'ultimo_estado': p.estado_text
                    }
                    pertenencias_dict.append(pertenencia_dict)
                return pertenencias_dict, objeto, imagenRecortada
