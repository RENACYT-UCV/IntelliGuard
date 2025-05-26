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


class PertenenciasService:
    def __init__(self):
        pass

            
    def registrar_nueva_pertenencia(img_file,idEstudiante,idObjeto):
        fecha_hora_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        estadoPertenencia=1
        # Crear la carpeta si no existe
        uploads_path = os.path.join('uploads', 'pertenencia')
        if not os.path.exists(uploads_path):
            os.makedirs(uploads_path)
        img_name=f"{idEstudiante}_{fecha_hora_actual}.jpg"
        # Guardar la imagen de la pertenencia en la carpeta 'uploads/pertenencia'
        img_path = os.path.join(uploads_path, img_name)
        # Leer el contenido del FileStorage como bytes
        imagen_bytes = img_file.read()
        with open(img_path, 'wb') as img_file:
            img_file.write(imagen_bytes)
        base_datos_pertenencia = BaseDatosPertenencia("basededatos.db")
        base_datos_registrosPertenencia = BaseDatosRegistrosPertenencia("basededatos.db")
        print(idObjeto)
        codigoPertenencia = base_datos_pertenencia.registrar_pertenencia(idObjeto, img_name, idEstudiante, estadoPertenencia, fecha_hora_actual)
        
        print("codigoPerte:")
        print(codigoPertenencia)
        if codigoPertenencia == -1:
            return -1
        else:
            resultado = base_datos_registrosPertenencia.registrar_registro(idEstudiante,idObjeto,estadoPertenencia,codigoPertenencia,fecha_hora_actual,img_name)
            if resultado == -1:
                return -1
            else:
                return resultado

    def registrar_entrada_pertenencia(img_file,idEstudiante,idObjeto,codigoPertenencia):
        fecha_hora_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  
        estadoPertenencia=1
        # Crear la carpeta si no existe
        uploads_path = os.path.join('uploads', 'pertenencia')
        if not os.path.exists(uploads_path):
            os.makedirs(uploads_path)
        img_name=f"{idEstudiante}_{fecha_hora_actual}.jpg"
        # Guardar la imagen de la pertenencia en la carpeta 'uploads/pertenencia'
        img_path = os.path.join(uploads_path, img_name)
        # Leer el contenido del FileStorage como bytes
        imagen_bytes = img_file.read()
        with open(img_path, 'wb') as img_file:
            img_file.write(imagen_bytes)
        base_datos_pertenencia = BaseDatosPertenencia("basededatos.db")
        base_datos_registrosPertenencia = BaseDatosRegistrosPertenencia("basededatos.db")
        resultado = base_datos_registrosPertenencia.registrar_registro(idEstudiante,idObjeto,estadoPertenencia,codigoPertenencia,fecha_hora_actual,img_name)
        if resultado == -1:
            return -1
        else:
            resultado = base_datos_pertenencia.actualizar_pertenencia_por_actividad(codigoPertenencia,estadoPertenencia,fecha_hora_actual)
            if resultado == -1:
                return -1
            else:
                return 1



        

    
    
