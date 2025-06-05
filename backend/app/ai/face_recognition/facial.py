import cv2
import face_recognition
import numpy as np
import os
from pathlib import Path
from ...config.config import config

class ReconocimientoFacial:
    def __init__(self):
        self.faces_dir = config.FACES_DIR
        self.model_dir = config.FACIAL_RECOGNITION_DIR
        self.face_encodings = {}
        self.load_faces()
        
    def load_faces(self):
        """Carga los rostros conocidos desde el directorio de rostros"""
        if not os.path.exists(self.faces_dir):
            os.makedirs(self.faces_dir)
            return
            
        for filename in os.listdir(self.faces_dir):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                codigo = filename.split('_')[0]
                image_path = os.path.join(self.faces_dir, filename)
                image = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(image)
                
                if face_encodings:
                    self.face_encodings[codigo] = face_encodings[0]
    
    def capturar_rostro(self, codigo_estudiante: str, video_path: str):
        """Captura rostros desde un video"""
        cap = cv2.VideoCapture(video_path)
        faces_captured = 0
        
        while cap.isOpened() and faces_captured < 5:  # Capturar 5 imágenes
            ret, frame = cap.read()
            if not ret:
                break
                
            # Detectar rostros
            face_locations = face_recognition.face_locations(frame)
            if face_locations:
                # Guardar la imagen con el rostro
                filename = f"{codigo_estudiante}_{faces_captured}.jpg"
                filepath = os.path.join(self.faces_dir, filename)
                cv2.imwrite(filepath, frame)
                faces_captured += 1
                
        cap.release()
        
        if faces_captured > 0:
            self.load_faces()  # Recargar los rostros
            return True
        return False
    
    def reconocimiento_facial(self, imagen):
        """Reconoce un rostro en una imagen"""
        # Detectar rostros en la imagen
        face_locations = face_recognition.face_locations(imagen)
        if not face_locations:
            return None, 0
            
        # Obtener encodings del rostro detectado
        face_encodings = face_recognition.face_encodings(imagen, face_locations)
        if not face_encodings:
            return None, 0
            
        # Comparar con rostros conocidos
        best_match = None
        best_distance = float('inf')
        
        for codigo, known_encoding in self.face_encodings.items():
            distance = face_recognition.face_distance([known_encoding], face_encodings[0])[0]
            if distance < best_distance:
                best_distance = distance
                best_match = codigo
                
        if best_match and best_distance < 0.6:  # Umbral de similitud
            confidence = (1 - best_distance) * 100
            return best_match, confidence
            
        return None, 0
    
    def entrenar_modelo(self):
        """Entrena el modelo con los rostros capturados"""
        # En este caso, no necesitamos entrenar ya que face_recognition
        # usa un modelo pre-entrenado. Solo recargamos los rostros.
        self.load_faces()
        return True 