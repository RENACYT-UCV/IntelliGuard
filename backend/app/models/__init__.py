# Este archivo puede estar vacío
# Todos los modelos usan el DatabaseManager directamente

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from ..config.config import config

# Crear el motor de la base de datos
engine = create_engine(config.DATABASE_URL)

# Crear la clase base para los modelos
Base = declarative_base()

# Crear una fábrica de sesiones thread-safe
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Función para obtener una sesión
def get_db_session():
    return Session()
