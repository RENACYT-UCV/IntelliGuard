from ultralytics import YOLO
import cv2
import numpy as np
from typing import List, Dict, Optional
import logging
import os
from ...config.config import config

logger = logging.getLogger(__name__)

class DetectorObjetos:
    def __init__(self):
        self.model_path = config.OBJECT_DETECTION_MODEL
        self.model = YOLO(self.model_path)
        
    def detectar_objetos(self, imagen):
        """Detecta objetos en una imagen usando YOLOv8"""
        # Realizar la detección
        resultados = self.model(imagen)
        
        # Procesar resultados
        detecciones = []
        for resultado in resultados:
            boxes = resultado.boxes
            for box in boxes:
                # Obtener coordenadas y confianza
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confianza = float(box.conf[0].cpu().numpy())
                clase_id = int(box.cls[0].cpu().numpy())
                clase = resultado.names[clase_id]
                
                detecciones.append({
                    'clase': clase,
                    'confianza': confianza,
                    'bbox': [int(x1), int(y1), int(x2), int(y2)]
                })
        
        return detecciones
    
    def comparar_objetos(self, imagen1, imagen2):
        """Compara dos imágenes para determinar si contienen objetos similares"""
        # Detectar objetos en ambas imágenes
        detecciones1 = self.detectar_objetos(imagen1)
        detecciones2 = self.detectar_objetos(imagen2)
        
        # Contar objetos por clase en cada imagen
        objetos1 = {}
        objetos2 = {}
        
        for det in detecciones1:
            clase = det['clase']
            objetos1[clase] = objetos1.get(clase, 0) + 1
            
        for det in detecciones2:
            clase = det['clase']
            objetos2[clase] = objetos2.get(clase, 0) + 1
        
        # Calcular similitud
        similitud = 0
        total_objetos = 0
        
        for clase in set(objetos1.keys()) | set(objetos2.keys()):
            count1 = objetos1.get(clase, 0)
            count2 = objetos2.get(clase, 0)
            similitud += min(count1, count2)
            total_objetos += max(count1, count2)
        
        if total_objetos == 0:
            return 0
            
        return (similitud / total_objetos) * 100
    
    def guardar_detecciones(self, imagen, detecciones, output_path):
        """Guarda una imagen con las detecciones marcadas"""
        img_copy = imagen.copy()
        
        for det in detecciones:
            x1, y1, x2, y2 = det['bbox']
            clase = det['clase']
            confianza = det['confianza']
            
            # Dibujar bbox
            cv2.rectangle(img_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Agregar etiqueta
            label = f"{clase} {confianza:.2f}"
            cv2.putText(img_copy, label, (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        cv2.imwrite(output_path, img_copy)
        return True

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