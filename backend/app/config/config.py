from datetime import timedelta
import os
from pathlib import Path
from dataclasses import dataclass
from typing import List

@dataclass
class Config:
    # Configuración de la base de datos
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATABASE_PATH = BASE_DIR / 'data' / 'database.db'
    DATABASE_URL = f'sqlite:///{DATABASE_PATH}'
    
    # Configuración de JWT
    JWT_SECRET_KEY = 'tu_clave_secreta_aqui'  # Cambiar en producción
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Configuración de CORS
    CORS_ORIGINS = [
        "http://localhost:5000",
        "http://127.0.0.1:5000",
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ]
    
    # Configuración de rutas
    UPLOAD_FOLDER = BASE_DIR / 'data' / 'uploads'
    MODELS_FOLDER = BASE_DIR / 'data' / 'models'
    
    # Asegurar que las carpetas existan
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    MODELS_FOLDER.mkdir(parents=True, exist_ok=True)
    
    # Configuración de IA
    FACE_RECOGNITION_MODEL = MODELS_FOLDER / 'facial' / 'face_recognition_model.pkl'
    OBJECT_DETECTION_MODEL = MODELS_FOLDER / 'objects' / 'yolov8n.pt'
    
    # Configuración de logging
    LOG_LEVEL = "INFO"
    LOG_FILE = BASE_DIR / 'logs' / 'app.log'
    
    # Configuración de seguridad
    BCRYPT_LOG_ROUNDS = 12
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit
    
    # Rate limiting
    RATELIMIT_DEFAULT = "100 per minute"
    RATELIMIT_STORAGE_URL = "memory://"

    # Configuración de la base de datos
    SQLITE_TIMEOUT: int = 30
    SQLITE_CHECK_SAME_THREAD: bool = False
    
    # Configuración de la aplicación
    DEBUG: bool = True
    TESTING: bool = False
    
    # Configuración de IA
    AI_DATA_DIR: str = os.path.join(BASE_DIR, 'data')
    AI_MODELS_DIR: str = os.path.join(AI_DATA_DIR, 'models')
    AI_DATASETS_DIR: str = os.path.join(AI_DATA_DIR, 'datasets')
    AI_IMAGES_DIR: str = os.path.join(AI_DATA_DIR, 'images')
    
    # Modelos de Detección de Objetos
    OBJECT_DETECTION_DIR: str = os.path.join(AI_MODELS_DIR, 'objetos')
    YOLO_MODEL_PATH: str = os.path.join(OBJECT_DETECTION_DIR, 'yolov4.weights')
    YOLO_CONFIG_PATH: str = os.path.join(OBJECT_DETECTION_DIR, 'yolov4.cfg')
    YOLO_CLASSES_PATH: str = os.path.join(OBJECT_DETECTION_DIR, 'coco.names')
    SIFT_MODEL_PATH: str = os.path.join(OBJECT_DETECTION_DIR, 'sift_model.yml')
    
    # Modelos de Reconocimiento Facial
    FACIAL_RECOGNITION_DIR: str = os.path.join(AI_MODELS_DIR, 'facial')
    FACE_DETECTION_MODEL: str = os.path.join(FACIAL_RECOGNITION_DIR, 'face_detection_model.dat')
    FACE_PREDICTOR_MODEL: str = os.path.join(FACIAL_RECOGNITION_DIR, 'shape_predictor_68_face_landmarks.dat')
    
    # Datasets
    FACES_DATASET: str = os.path.join(AI_DATASETS_DIR, 'faces')
    OBJECTS_DATASET: str = os.path.join(AI_DATASETS_DIR, 'objects')
    
    # Directorios de imágenes
    FACES_DIR: str = os.path.join(AI_IMAGES_DIR, 'faces')
    OBJECTS_DIR: str = os.path.join(AI_IMAGES_DIR, 'objects')
    BELONGINGS_DIR: str = os.path.join(AI_IMAGES_DIR, 'belongings')
    
    def __post_init__(self):
        # Crear directorios necesarios
        directories = [
            os.path.dirname(self.DATABASE_PATH),
            self.AI_MODELS_DIR,
            self.OBJECT_DETECTION_DIR,
            self.FACIAL_RECOGNITION_DIR,
            self.AI_DATASETS_DIR,
            self.FACES_DATASET,
            self.OBJECTS_DATASET,
            self.FACES_DIR,
            self.OBJECTS_DIR,
            self.BELONGINGS_DIR
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

# Instancia global de configuración
config = Config() 