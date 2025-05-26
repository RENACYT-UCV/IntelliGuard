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
    
        
    def consultar_pertenencia_estado_estudiante(idEstudiante,idEstado):
        base_datos_pertenencia = BaseDatosPertenencia("basededatos.db")
        pertenencias=base_datos_pertenencia.consultar_pertenencias_por_estado_estudiante(idEstado,idEstudiante)
        if pertenencias == []:
            return -1
        else:
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
                        'hora_entrada': p.fecha_ultima_actividad,
                        'id_estado': p.id_ultimo_estado,
                        'nombre_estado': p.estado_text,
                        'imagen_pertenencia': f'data:image/jpeg;base64,{imagen_base64}',
                        'id_estudiante': p.id_estudiante
                    }
                    registros_dic.append(pertenencia_dict)
        return registros_dic



    def registrar_salida_pertenencia(codPertenciasIdEstado):
        fecha_hora_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Reemplazar los dos puntos con guiones bajos
        try:
            base_datos_pertenencia = BaseDatosPertenencia("basededatos.db")
            for pertenencia in codPertenciasIdEstado:
                codPertenencia=pertenencia.get('codPertenecia')
                estado=pertenencia.get('estado')
                if not codPertenencia or estado is None:
                    continue
                if not base_datos_pertenencia.cambiar_estado_pertenencias(codPertenencia,estado,fecha_hora_actual):
                        return False
                base_datos_registrosPertenencia = BaseDatosRegistrosPertenencia("basededatos.db")
                base_datos_registrosPertenencia.actualizar_hora_estado_registro(codPertenencia,estado,fecha_hora_actual)
            return True
        except Exception as e:
            print(f"Error al registrar salida de perteencia {e}")
            return False

    
