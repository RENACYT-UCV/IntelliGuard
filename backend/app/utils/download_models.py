import os
import requests
from tqdm import tqdm
from ..config.config import config
from ..utils.logger import logger

MODELS = {
    'face_detection': {
        'url': 'https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2',
        'path': config.FACE_PREDICTOR_MODEL
    },
    'yolov8': {
        'url': 'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt',
        'path': config.OBJECT_DETECTION_MODEL
    }
}

def download_file(url: str, destination: str):
    """Descarga un archivo mostrando una barra de progreso"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        
        with open(destination, 'wb') as file, tqdm(
            desc=os.path.basename(destination),
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for data in response.iter_content(block_size):
                size = file.write(data)
                pbar.update(size)
                
        return True
    except Exception as e:
        logger.error(f"Error al descargar {url}: {e}")
        return False

def download_models():
    """Descarga todos los modelos necesarios"""
    success = True
    for model_name, model_info in MODELS.items():
        if not os.path.exists(model_info['path']):
            logger.info(f"Descargando modelo {model_name}...")
            if not download_file(model_info['url'], model_info['path']):
                success = False
                logger.error(f"Error al descargar el modelo {model_name}")
        else:
            logger.info(f"El modelo {model_name} ya existe")
    
    return success

if __name__ == '__main__':
    if download_models():
        logger.info("Todos los modelos fueron descargados exitosamente")
    else:
        logger.error("Hubo errores al descargar algunos modelos") 