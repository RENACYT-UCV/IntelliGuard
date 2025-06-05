import cv2
import numpy as np
from typing import List, Dict, Optional, Tuple
import face_recognition
import logging
import os
from ...config.config import config

logger = logging.getLogger(__name__)

class FaceRecognizer:
    """Clase para reconocimiento facial usando face_recognition"""
    
    def __init__(self):
        """Inicializa el reconocedor facial"""
        self.known_face_encodings = []
        self.known_face_ids = []
        self.model = "hog"  # o "cnn" si hay GPU
        
    def load_known_faces(self, faces_dir: str) -> bool:
        """
        Carga las caras conocidas desde un directorio.
        
        Args:
            faces_dir: Directorio con imágenes de caras conocidas
            
        Returns:
            bool: True si la carga fue exitosa
        """
        try:
            # Limpiar datos previos
            self.known_face_encodings = []
            self.known_face_ids = []
            
            # Verificar directorio
            if not os.path.exists(faces_dir):
                logger.error(f"Directorio {faces_dir} no encontrado")
                return False
                
            # Cargar imágenes
            for filename in os.listdir(faces_dir):
                if filename.endswith((".jpg", ".jpeg", ".png")):
                    try:
                        # Extraer ID del nombre del archivo
                        face_id = filename.split(".")[0]
                        
                        # Cargar y codificar imagen
                        image_path = os.path.join(faces_dir, filename)
                        face_image = face_recognition.load_image_file(image_path)
                        face_encoding = face_recognition.face_encodings(face_image)
                        
                        if face_encoding:
                            self.known_face_encodings.append(face_encoding[0])
                            self.known_face_ids.append(face_id)
                        else:
                            logger.warning(f"No se encontró cara en {filename}")
                            
                    except Exception as e:
                        logger.error(f"Error procesando {filename}: {str(e)}")
                        continue
                        
            logger.info(f"Cargadas {len(self.known_face_encodings)} caras conocidas")
            return True
            
        except Exception as e:
            logger.error(f"Error cargando caras conocidas: {str(e)}")
            return False
            
    def detect_faces(self, image: np.ndarray) -> List[Dict]:
        """
        Detecta caras en una imagen.
        
        Args:
            image: Imagen en formato numpy array (BGR)
            
        Returns:
            List[Dict]: Lista de caras detectadas con formato:
                {
                    'bbox': (top, right, bottom, left),
                    'encoding': np.array
                }
        """
        try:
            # Convertir BGR a RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Detectar caras
            face_locations = face_recognition.face_locations(rgb_image, model=self.model)
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
            
            # Preparar resultados
            faces = []
            for location, encoding in zip(face_locations, face_encodings):
                faces.append({
                    'bbox': location,  # (top, right, bottom, left)
                    'encoding': encoding
                })
                
            return faces
            
        except Exception as e:
            logger.error(f"Error detectando caras: {str(e)}")
            return []
            
    def identify_faces(self, faces: List[Dict], tolerance: float = 0.6) -> List[Dict]:
        """
        Identifica caras detectadas contra las caras conocidas.
        
        Args:
            faces: Lista de caras detectadas
            tolerance: Umbral de tolerancia para coincidencias
            
        Returns:
            List[Dict]: Lista de caras con identificación:
                {
                    'bbox': (top, right, bottom, left),
                    'id': str o None si no hay coincidencia,
                    'confidence': float
                }
        """
        try:
            results = []
            
            for face in faces:
                # Comparar con caras conocidas
                if self.known_face_encodings:
                    distances = face_recognition.face_distance(
                        self.known_face_encodings,
                        face['encoding']
                    )
                    
                    best_match_index = np.argmin(distances)
                    min_distance = distances[best_match_index]
                    
                    if min_distance <= tolerance:
                        results.append({
                            'bbox': face['bbox'],
                            'id': self.known_face_ids[best_match_index],
                            'confidence': 1 - min_distance
                        })
                    else:
                        results.append({
                            'bbox': face['bbox'],
                            'id': None,
                            'confidence': 0.0
                        })
                else:
                    results.append({
                        'bbox': face['bbox'],
                        'id': None,
                        'confidence': 0.0
                    })
                    
            return results
            
        except Exception as e:
            logger.error(f"Error identificando caras: {str(e)}")
            return []
            
    def draw_results(self, image: np.ndarray, results: List[Dict]) -> np.ndarray:
        """
        Dibuja los resultados de identificación en la imagen.
        
        Args:
            image: Imagen original
            results: Lista de resultados de identificación
            
        Returns:
            np.ndarray: Imagen con los resultados dibujados
        """
        try:
            image_copy = image.copy()
            
            for result in results:
                # Extraer coordenadas
                top, right, bottom, left = result['bbox']
                
                # Color según si fue identificado
                color = (0, 255, 0) if result['id'] else (0, 0, 255)
                
                # Dibujar bbox
                cv2.rectangle(
                    image_copy,
                    (left, top),
                    (right, bottom),
                    color,
                    2
                )
                
                # Dibujar etiqueta
                label = f"{result['id'] or 'Desconocido'} {result['confidence']:.2f}"
                cv2.putText(
                    image_copy,
                    label,
                    (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    2
                )
                
            return image_copy
            
        except Exception as e:
            logger.error(f"Error dibujando resultados: {str(e)}")
            return image 