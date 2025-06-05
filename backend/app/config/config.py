import os
from dataclasses import dataclass
from typing import List

@dataclass
class Config:
    # Configuración de la base de datos
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATABASE_PATH: str = os.path.join(BASE_DIR, 'data', 'database.db')
    DATABASE_URL: str = f'sqlite:///{DATABASE_PATH}'
    SQLITE_TIMEOUT: int = 30
    SQLITE_CHECK_SAME_THREAD: bool = False

    # Configuración de seguridad
    JWT_SECRET_KEY: str = "clave_12323"  # TODO: Mover a variable de entorno
    JWT_ACCESS_TOKEN_EXPIRES: int = 3600  # 1 hora
    
    # Configuración de CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    # Configuración de la aplicación
    DEBUG: bool = True
    TESTING: bool = False
    
    # Configuración de logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    def __post_init__(self):
        # Asegurar que el directorio data existe
        os.makedirs(os.path.dirname(self.DATABASE_PATH), exist_ok=True)

# Instancia global de configuración
config = Config() 