import cv2
import numpy as np
import os
from pathlib import Path
import sys
from ultralytics import YOLO

# Agregar el directorio raíz al path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

from utils.config import (
    MODELO_OBJETOS,
    DATASET_OBJETOS,
    CONFIANZA_OBJETO
)

class DeteccionObjetos:
    def __init__(self):
        """Inicializa el detector de objetos"""
        self.modelo = None
        self.cargar_modelo()
        
    def cargar_modelo(self):
        """Carga el modelo YOLO"""
        try:
            if os.path.exists(MODELO_OBJETOS):
                self.modelo = YOLO(MODELO_OBJETOS)
                print("Modelo de objetos cargado exitosamente")
            else:
                print("Modelo de objetos no encontrado. Se creará uno nuevo.")
                self.entrenar_modelo()
        except Exception as e:
            print(f"Error al cargar el modelo de objetos: {str(e)}")
            
    def identificar_objeto(self, imagen):
        """
        Identifica objetos en una imagen
        
        Args:
            imagen: Imagen en formato numpy array
            
        Returns:
            tuple: (etiqueta_objeto, imagen_recortada) o (None, None) si no se detecta
        """
        try:
            if self.modelo is None:
                print("Error: El modelo de objetos no está cargado. No se puede realizar la detección.")
                return None, None
            # Realizar predicción
            resultados = self.modelo(imagen)
            
            if len(resultados) == 0:
                return None, None
                
            # Obtener el primer resultado
            resultado = resultados[0]
            
            # Verificar confianza
            if resultado.boxes.conf[0] < CONFIANZA_OBJETO:
                return None, None
                
            # Obtener etiqueta y coordenadas
            etiqueta = resultado.names[int(resultado.boxes.cls[0])]
            x1, y1, x2, y2 = map(int, resultado.boxes.xyxy[0])
            
            # Recortar objeto
            objeto = imagen[y1:y2, x1:x2]
            
            return etiqueta, objeto
            
        except Exception as e:
            print(f"Error en detección de objetos: {str(e)}")
            return None, None
            
    def entrenar_modelo(self):
        """Entrena el modelo YOLO con el dataset disponible"""
        try:
            # Verificar dataset
            if not os.path.exists(DATASET_OBJETOS):
                print("Dataset de objetos no encontrado")
                return
            # Permitir las clases globales necesarias para PyTorch 2.6+
            import torch
            from ultralytics.nn.tasks import DetectionModel
            from torch.nn.modules.container import Sequential
            from ultralytics.nn.modules import Conv
            torch.serialization.add_safe_globals([DetectionModel, Sequential, Conv])
            # Configurar entrenamiento
            self.modelo = YOLO('yolov8n.pt')  # Modelo base
            # Entrenar modelo
            self.modelo.train(
                data=os.path.join(DATASET_OBJETOS, 'dataset.yaml'),
                epochs=100,
                imgsz=640,
                batch=16,
                name='entrenamiento_objetos'
            )
            # Guardar modelo
            os.makedirs(os.path.dirname(MODELO_OBJETOS), exist_ok=True)
            self.modelo.save(MODELO_OBJETOS)
            print("Modelo de objetos entrenado y guardado exitosamente")
        except Exception as e:
            print(f"Error al entrenar modelo: {str(e)}")
            
    def procesar_imagen(self, ruta_imagen):
        """
        Procesa una imagen desde archivo
        
        Args:
            ruta_imagen: Ruta al archivo de imagen
            
        Returns:
            tuple: (etiqueta_objeto, imagen_recortada) o (None, None) si no se detecta
        """
        try:
            # Leer imagen
            imagen = cv2.imread(ruta_imagen)
            if imagen is None:
                print(f"No se pudo leer la imagen: {ruta_imagen}")
                return None, None
                
            return self.identificar_objeto(imagen)
            
        except Exception as e:
            print(f"Error al procesar imagen: {str(e)}")
            return None, None 