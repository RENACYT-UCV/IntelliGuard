import cv2
import numpy as np
from typing import List, Dict, Optional, Tuple
import logging
from ...config.config import config

logger = logging.getLogger(__name__)

class ImageComparator:
    """Clase para comparación de imágenes usando SIFT"""
    
    def __init__(self):
        """Inicializa el comparador de imágenes"""
        self.sift = cv2.SIFT_create()
        self.matcher = cv2.BFMatcher()
        
    def extract_features(self, image: np.ndarray) -> Tuple[List, np.ndarray]:
        """
        Extrae características SIFT de una imagen.
        
        Args:
            image: Imagen en formato numpy array (BGR)
            
        Returns:
            Tuple[List, np.ndarray]: (keypoints, descriptores)
        """
        try:
            # Convertir a escala de grises
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detectar keypoints y computar descriptores
            keypoints, descriptors = self.sift.detectAndCompute(gray, None)
            
            return keypoints, descriptors
            
        except Exception as e:
            logger.error(f"Error extrayendo características: {str(e)}")
            return [], None
            
    def compare_images(
        self,
        image1: np.ndarray,
        image2: np.ndarray,
        ratio_thresh: float = 0.7,
        min_matches: int = 10
    ) -> Dict:
        """
        Compara dos imágenes usando SIFT.
        
        Args:
            image1: Primera imagen
            image2: Segunda imagen
            ratio_thresh: Umbral para filtrado de matches
            min_matches: Mínimo número de matches para considerar similitud
            
        Returns:
            Dict: Resultados de la comparación:
                {
                    'matches': int,
                    'similarity_score': float,
                    'is_similar': bool,
                    'homography': np.ndarray o None
                }
        """
        try:
            # Extraer características
            kp1, des1 = self.extract_features(image1)
            kp2, des2 = self.extract_features(image2)
            
            if des1 is None or des2 is None:
                return {
                    'matches': 0,
                    'similarity_score': 0.0,
                    'is_similar': False,
                    'homography': None
                }
                
            # Encontrar matches
            matches = self.matcher.knnMatch(des1, des2, k=2)
            
            # Aplicar ratio test
            good_matches = []
            for m, n in matches:
                if m.distance < ratio_thresh * n.distance:
                    good_matches.append(m)
                    
            num_matches = len(good_matches)
            
            # Calcular score de similitud
            similarity_score = num_matches / min(len(kp1), len(kp2))
            
            # Determinar si las imágenes son similares
            is_similar = num_matches >= min_matches
            
            # Calcular homografía si hay suficientes matches
            homography = None
            if is_similar and num_matches >= 4:
                src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                
                homography, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                
            return {
                'matches': num_matches,
                'similarity_score': similarity_score,
                'is_similar': is_similar,
                'homography': homography
            }
            
        except Exception as e:
            logger.error(f"Error comparando imágenes: {str(e)}")
            return {
                'matches': 0,
                'similarity_score': 0.0,
                'is_similar': False,
                'homography': None
            }
            
    def draw_matches(
        self,
        image1: np.ndarray,
        image2: np.ndarray,
        comparison_result: Dict
    ) -> np.ndarray:
        """
        Dibuja los matches entre dos imágenes.
        
        Args:
            image1: Primera imagen
            image2: Segunda imagen
            comparison_result: Resultado de la comparación
            
        Returns:
            np.ndarray: Imagen con los matches dibujados
        """
        try:
            if not comparison_result['is_similar']:
                # Concatenar imágenes horizontalmente
                height = max(image1.shape[0], image2.shape[0])
                width = image1.shape[1] + image2.shape[1]
                result = np.zeros((height, width, 3), dtype=np.uint8)
                result[:image1.shape[0], :image1.shape[1]] = image1
                result[:image2.shape[0], image1.shape[1]:] = image2
                
                # Dibujar mensaje
                cv2.putText(
                    result,
                    "No hay suficientes coincidencias",
                    (10, height - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )
                
                return result
                
            # Extraer características nuevamente
            kp1, des1 = self.extract_features(image1)
            kp2, des2 = self.extract_features(image2)
            
            # Encontrar matches
            matches = self.matcher.knnMatch(des1, des2, k=2)
            
            # Aplicar ratio test
            good_matches = []
            for m, n in matches:
                if m.distance < 0.7 * n.distance:
                    good_matches.append(m)
                    
            # Dibujar matches
            result = cv2.drawMatches(
                image1, kp1,
                image2, kp2,
                good_matches, None,
                flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
            )
            
            # Dibujar score
            cv2.putText(
                result,
                f"Score: {comparison_result['similarity_score']:.2f}",
                (10, result.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error dibujando matches: {str(e)}")
            # Devolver imágenes concatenadas sin matches
            height = max(image1.shape[0], image2.shape[0])
            width = image1.shape[1] + image2.shape[1]
            result = np.zeros((height, width, 3), dtype=np.uint8)
            result[:image1.shape[0], :image1.shape[1]] = image1
            result[:image2.shape[0], image1.shape[1]:] = image2
            return result 