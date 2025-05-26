import cv2
import os
import imutils
import time
import numpy as np
import tempfile
from ultralytics import YOLO

class DeteccionObjetos:
    def __init__(self):
        # Aquí podrías inicializar cualquier cosa necesaria para tu servicio
        pass

    def identificarObjeto(imagen):
        try:
            ruta_modelo = os.path.join('models', 'ModelObjetoFinal.pt') 
            modelo = YOLO(ruta_modelo) 
            resultados = modelo(imagen, imgsz=640, conf=0.80)
            if resultados is not None and len(resultados) > 0 and len(resultados[0].boxes) > 0:
                box = resultados[0].boxes[0]
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                imagen_recortada = imagen[y1:y2, x1:x2]
                etiqueta = resultados[0].names[int(box.cls)]
                return etiqueta, imagen_recortada
            else:
                print("No se encontraron objetos en la imagen.")
                return -1, None
        except Exception as error:
            print(f"Error en la detección de objetos: {str(error)}")
            return -1, None
        
        
    def entrenar_modelo_objeto(epochs=150, batch_size=16):
        try:    
            ruta_datos_train = 'path/to/train'
            ruta_datos_tval = 'path/to/val'
            ruta_modelo = 'models/ModeloObjetoFinal2.pt'
            modelo = YOLO('yolov8n.pt')
            datos = {
                'train': ruta_datos_train,
                'val': ruta_datos_tval
            }
            hyperparams = {
                'epochs': epochs,
                'batch_size': batch_size,
            }
            print("Comenzando el entrenamiento del modelo...")
            modelo.train(data=datos, **hyperparams)
            modelo.save(ruta_modelo)
            print(f"Modelo entrenado guardado en: {ruta_modelo}")
        except Exception as e:
            print(f"Error durante el entrenamiento del modelo YOLOv8: {str(e)}")


