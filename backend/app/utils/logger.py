import logging
from logging.handlers import RotatingFileHandler
from ..config.config import config
import os

def setup_logger():
    """Configura el logger del sistema"""
    # Crear el directorio de logs si no existe
    os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)
    
    # Configurar el logger
    logger = logging.getLogger('intelliguard')
    logger.setLevel(logging.getLevelName(config.LOG_LEVEL))
    
    # Configurar el formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Configurar el handler de archivo
    file_handler = RotatingFileHandler(
        config.LOG_FILE,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # Configurar el handler de consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Agregar los handlers al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Crear la instancia del logger
logger = setup_logger() 