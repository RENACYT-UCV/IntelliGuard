import cv2
import numpy as np
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

def calcular_similitud(img1: np.ndarray, img2: np.ndarray) -> float:
    """
    Calcula la similitud entre dos imágenes usando SIFT y ratio de matches.
    
    Args:
        img1: Primera imagen en formato numpy array
        img2: Segunda imagen en formato numpy array
        
    Returns:
        float: Puntuación de similitud entre 0 y 1
    """
    try:
        # Convertir a escala de grises si es necesario
        if len(img1.shape) == 3:
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        if len(img2.shape) == 3:
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            
        # Inicializar SIFT
        sift = cv2.SIFT_create()
        
        # Encontrar keypoints y descriptores
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)
        
        # Si no hay suficientes keypoints, retornar 0
        if des1 is None or des2 is None or len(kp1) < 2 or len(kp2) < 2:
            return 0.0
        
        # Usar FLANN para matching
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        
        matches = flann.knnMatch(des1, des2, k=2)
        
        # Aplicar ratio test de Lowe
        good_matches = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good_matches.append(m)
        
        # Calcular puntuación de similitud
        similitud = len(good_matches) / max(len(kp1), len(kp2))
        return min(1.0, similitud)
        
    except Exception as e:
        logger.error(f"Error calculando similitud: {str(e)}")
        return 0.0

def ordenar_imagenes_por_similitud(
    imagen_referencia: np.ndarray,
    lista_imagenes: List[Tuple[str, np.ndarray]]
) -> List[Tuple[str, float]]:
    """
    Ordena una lista de imágenes por su similitud con una imagen de referencia.
    
    Args:
        imagen_referencia: Imagen de referencia en formato numpy array
        lista_imagenes: Lista de tuplas (id_imagen, imagen) donde imagen es un numpy array
        
    Returns:
        List[Tuple[str, float]]: Lista ordenada de tuplas (id_imagen, puntuación_similitud)
    """
    try:
        resultados = []
        for id_imagen, imagen in lista_imagenes:
            similitud = calcular_similitud(imagen_referencia, imagen)
            resultados.append((id_imagen, similitud))
        
        # Ordenar por similitud descendente
        return sorted(resultados, key=lambda x: x[1], reverse=True)
        
    except Exception as e:
        logger.error(f"Error ordenando imágenes por similitud: {str(e)}")
        return [(id_img, 0.0) for id_img, _ in lista_imagenes] 