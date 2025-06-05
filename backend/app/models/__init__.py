# Este archivo puede estar vacío

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Crear la clase base para los modelos
Base = declarative_base()

# Crear una fábrica de sesiones
Session = sessionmaker()
