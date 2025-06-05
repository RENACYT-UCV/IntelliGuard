import os
import sys
from app.utils.logger import logger
from app.database.init_db import init_database
from app.utils.download_models import download_models
from app.config.config import config

def init_project():
    """Inicializa el proyecto creando directorios y descargando modelos"""
    try:
        # Crear directorios necesarios
        directories = [
            config.UPLOAD_FOLDER,
            config.MODELS_FOLDER,
            os.path.dirname(config.LOG_FILE),
            os.path.join(config.BASE_DIR, 'data', 'uploads'),
            os.path.join(config.BASE_DIR, 'data', 'models', 'facial'),
            os.path.join(config.BASE_DIR, 'data', 'models', 'objects'),
            os.path.dirname(config.DATABASE_PATH)  # Asegurar que el directorio de la base de datos existe
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Directorio creado: {directory}")
        
        # Inicializar base de datos
        logger.info("Inicializando base de datos...")
        init_database()
        logger.info("Base de datos inicializada correctamente")
        
        # Descargar modelos
        logger.info("Descargando modelos de IA...")
        if download_models():
            logger.info("Modelos descargados correctamente")
        else:
            logger.error("Error al descargar algunos modelos")
            return False
        
        logger.info("Inicialización del proyecto completada exitosamente")
        return True
        
    except Exception as e:
        logger.error(f"Error durante la inicialización del proyecto: {e}")
        return False

if __name__ == '__main__':
    if init_project():
        logger.info("Proyecto inicializado correctamente")
        sys.exit(0)
    else:
        logger.error("Error al inicializar el proyecto")
        sys.exit(1) 