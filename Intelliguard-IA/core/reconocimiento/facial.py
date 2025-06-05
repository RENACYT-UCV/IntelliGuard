import cv2
import numpy as np
import os
from pathlib import Path
import sys

# Agregar el directorio raíz al path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

from utils.config import (
    MODELO_FACIAL,
    DATASET_FACIAL,
    CONFIANZA_MINIMA,
    MAX_FOTOS
)

class ReconocimientoFacial:
    def __init__(self):
        """Inicializa el reconocedor facial"""
        self.modelo = None
        self.detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.cargar_modelo()
        
    def cargar_modelo(self):
        """Carga el modelo de reconocimiento facial"""
        try:
            if os.path.exists(MODELO_FACIAL):
                self.modelo = cv2.face.LBPHFaceRecognizer_create()
                self.modelo.read(MODELO_FACIAL)
                print("Modelo facial cargado exitosamente")
            else:
                print("Modelo facial no encontrado. Se creará uno nuevo.")
                self.entrenar_modelo()
        except Exception as e:
            print(f"Error al cargar el modelo facial: {str(e)}")
            
    def reconocimiento_facial(self, imagen):
        """
        Realiza el reconocimiento facial en una imagen
        
        Args:
            imagen: Imagen en formato numpy array
            
        Returns:
            tuple: (codigo_estudiante, porcentaje_similitud) o (None, 0) si no se reconoce
        """
        try:
            # Convertir a escala de grises
            gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
            
            # Detectar rostros
            rostros = self.detector.detectMultiScale(
                gris,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            if len(rostros) == 0:
                return None, 0
                
            # Tomar el primer rostro detectado
            x, y, w, h = rostros[0]
            rostro = gris[y:y+h, x:x+w]
            
            # Realizar predicción
            codigo, confianza = self.modelo.predict(rostro)
            
            # Convertir confianza a porcentaje
            porcentaje = 100 - confianza
            
            if porcentaje >= CONFIANZA_MINIMA * 100:
                return codigo, porcentaje
            else:
                return None, 0
                
        except Exception as e:
            print(f"Error en reconocimiento facial: {str(e)}")
            return None, 0
            
    def capturar_rostro(self, codigo_estudiante, video_path=None):
        """
        Captura rostros desde un video o la cámara web
        
        Args:
            codigo_estudiante: Código del estudiante para nombrar las imágenes
            video_path: Ruta al archivo de video (opcional, si no se proporciona usa la cámara)
        """
        try:
            # Crear directorio si no existe
            os.makedirs(DATASET_FACIAL, exist_ok=True)
            
            # Iniciar captura de video
            if video_path:
                cap = cv2.VideoCapture(video_path)
            else:
                cap = cv2.VideoCapture(0)
                
            if not cap.isOpened():
                raise Exception("No se pudo abrir el video o la cámara")
                
            contador = 0
            frames_procesados = 0
            max_frames = 30  # Procesar un frame cada 30 frames para videos largos
            
            while contador < MAX_FOTOS:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                frames_procesados += 1
                if frames_procesados % max_frames != 0:
                    continue
                    
                # Convertir a escala de grises
                gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detectar rostros
                rostros = self.detector.detectMultiScale(
                    gris,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30)
                )
                
                # Guardar rostros detectados
                for (x, y, w, h) in rostros:
                    # Guardar rostro
                    rostro = gris[y:y+h, x:x+w]
                    ruta = os.path.join(DATASET_FACIAL, f"{codigo_estudiante}_{contador}.jpg")
                    cv2.imwrite(ruta, rostro)
                    contador += 1
                    if contador >= MAX_FOTOS:
                        break
                        
            cap.release()
            
            if contador == 0:
                raise Exception("No se detectaron rostros en el video")
                
            # Entrenar modelo con nuevas imágenes
            self.entrenar_modelo()
            
        except Exception as e:
            print(f"Error al capturar rostro: {str(e)}")
            raise e
            
    def entrenar_modelo(self):
        """Entrena el modelo con las imágenes disponibles"""
        try:
            # Obtener imágenes y etiquetas
            imagenes = []
            etiquetas = []
            
            for archivo in os.listdir(DATASET_FACIAL):
                if archivo.endswith('.jpg'):
                    # Extraer código de estudiante del nombre
                    codigo = int(archivo.split('_')[0])
                    
                    # Cargar imagen
                    ruta = os.path.join(DATASET_FACIAL, archivo)
                    imagen = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
                    
                    imagenes.append(imagen)
                    etiquetas.append(codigo)
                    
            if len(imagenes) > 0:
                # Crear y entrenar modelo
                self.modelo = cv2.face.LBPHFaceRecognizer_create()
                self.modelo.train(imagenes, np.array(etiquetas))
                
                # Guardar modelo
                os.makedirs(os.path.dirname(MODELO_FACIAL), exist_ok=True)
                self.modelo.save(MODELO_FACIAL)
                print("Modelo facial entrenado y guardado exitosamente")
            else:
                print("No hay imágenes para entrenar el modelo")
                
        except Exception as e:
            print(f"Error al entrenar modelo: {str(e)}") 