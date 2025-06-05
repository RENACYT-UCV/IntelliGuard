import cv2
import numpy as np
from typing import List, Dict, Optional
import logging
import os
from ...config.config import config

logger = logging.getLogger(__name__)

class ObjectDetector:
    """Clase para detección de objetos usando YOLO"""
    
    def __init__(self):
        """Inicializa el detector de objetos"""
        self.net = None
        self.classes = []
        self.output_layers = []
        self.initialized = False
        
    def initialize(self) -> bool:
        """
        Inicializa el modelo YOLO.
        Returns:
            bool: True si la inicialización fue exitosa
        """
        try:
            # Cargar configuración y pesos
            weights_path = os.path.join(config.BASE_DIR, 'data', 'models', 'yolov4.weights')
            config_path = os.path.join(config.BASE_DIR, 'data', 'models', 'yolov4.cfg')
            classes_path = os.path.join(config.BASE_DIR, 'data', 'models', 'coco.names')
            
            # Verificar archivos
            if not all(os.path.exists(p) for p in [weights_path, config_path, classes_path]):
                logger.error("Archivos de modelo no encontrados")
                return False
            
            # Cargar modelo
            self.net = cv2.dnn.readNet(weights_path, config_path)
            
            # Configurar backend
            if cv2.cuda.getCudaEnabledDeviceCount() > 0:
                self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
                self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
            else:
                logger.warning("CUDA no disponible, usando CPU")
                
            # Cargar clases
            with open(classes_path, 'r') as f:
                self.classes = [line.strip() for line in f.readlines()]
                
            # Obtener capas de salida
            layer_names = self.net.getLayerNames()
            self.output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
            
            self.initialized = True
            logger.info("Detector de objetos inicializado correctamente")
            return True
            
        except Exception as e:
            logger.error(f"Error inicializando detector: {str(e)}")
            return False
            
    def detect(self, image: np.ndarray, conf_threshold: float = 0.5) -> List[Dict]:
        """
        Detecta objetos en una imagen.
        
        Args:
            image: Imagen en formato numpy array (BGR)
            conf_threshold: Umbral de confianza para detecciones
            
        Returns:
            List[Dict]: Lista de objetos detectados con formato:
                {
                    'class': str,
                    'confidence': float,
                    'bbox': (x, y, w, h)
                }
        """
        if not self.initialized:
            if not self.initialize():
                return []
                
        try:
            # Preprocesar imagen
            height, width = image.shape[:2]
            blob = cv2.dnn.blobFromImage(
                image, 
                1/255.0,  # escala
                (416, 416),  # tamaño
                swapRB=True,  # BGR a RGB
                crop=False
            )
            
            # Detección
            self.net.setInput(blob)
            outputs = self.net.forward(self.output_layers)
            
            # Procesar resultados
            boxes = []
            confidences = []
            class_ids = []
            
            for output in outputs:
                for detection in output:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    
                    if confidence > conf_threshold:
                        # Convertir coordenadas
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        x = int(center_x - w/2)
                        y = int(center_y - h/2)
                        
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
            
            # Aplicar NMS
            indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, 0.4)
            
            # Preparar resultados
            detections = []
            for i in indices:
                i = i[0] if isinstance(i, np.ndarray) else i
                box = boxes[i]
                detections.append({
                    'class': self.classes[class_ids[i]],
                    'confidence': confidences[i],
                    'bbox': tuple(box)
                })
                
            return detections
            
        except Exception as e:
            logger.error(f"Error en detección: {str(e)}")
            return []
            
    def draw_detections(self, image: np.ndarray, detections: List[Dict]) -> np.ndarray:
        """
        Dibuja las detecciones en la imagen.
        
        Args:
            image: Imagen original
            detections: Lista de detecciones
            
        Returns:
            np.ndarray: Imagen con las detecciones dibujadas
        """
        try:
            image_copy = image.copy()
            
            for det in detections:
                # Extraer información
                x, y, w, h = det['bbox']
                label = f"{det['class']} {det['confidence']:.2f}"
                
                # Dibujar bbox
                cv2.rectangle(
                    image_copy,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )
                
                # Dibujar etiqueta
                cv2.putText(
                    image_copy,
                    label,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )
                
            return image_copy
            
        except Exception as e:
            logger.error(f"Error dibujando detecciones: {str(e)}")
            return image 