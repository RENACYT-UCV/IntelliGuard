import bcrypt
import logging
from .db_manager import db
from ..config.config import config

logger = logging.getLogger(__name__)

def init_database():
    """Inicializa la base de datos con las tablas y datos necesarios"""
    try:
        # Crear tablas
        _create_tables()
        
        # Insertar datos iniciales
        _insert_initial_data()
        
        logger.info("Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"Error inicializando la base de datos: {e}")
        raise

def _create_tables():
    """Crea todas las tablas necesarias"""
    queries = [
        # Tabla de roles
        """
        CREATE TABLE IF NOT EXISTS rol_usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rol TEXT NOT NULL UNIQUE
        )
        """,
        
        # Tabla de usuarios
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            hash_contraseña TEXT NOT NULL,
            id_rol INTEGER NOT NULL,
            FOREIGN KEY (id_rol) REFERENCES rol_usuario(id)
        )
        """,
        
        # Tabla de estudiantes
        """
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL UNIQUE,
            nombres TEXT NOT NULL,
            carrera TEXT NOT NULL,
            plan TEXT NOT NULL
        )
        """,
        
        # Tabla de pertenencias
        """
        CREATE TABLE IF NOT EXISTS pertenencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_estudiante INTEGER NOT NULL,
            descripcion TEXT NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            estado TEXT DEFAULT 'activo',
            FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id)
        )
        """,
        
        # Tabla de reportes
        """
        CREATE TABLE IF NOT EXISTS reportes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pertenencia INTEGER NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('entrada', 'salida', 'perdida', 'recuperacion')),
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            detalles TEXT NOT NULL,
            estado TEXT NOT NULL,
            FOREIGN KEY (id_pertenencia) REFERENCES pertenencias(id)
        )
        """
    ]
    
    for query in queries:
        db.execute_query(query)
    db.commit()

def _insert_initial_data():
    """Inserta los datos iniciales necesarios"""
    # Insertar roles si no existen
    roles = [
        (1, 'Personal'),
        (2, 'Administrador')
    ]
    
    for role_id, role_name in roles:
        db.execute_query(
            "INSERT OR IGNORE INTO rol_usuario (id, rol) VALUES (?, ?)",
            (role_id, role_name)
        )
    
    # Crear usuario administrador por defecto
    admin_user = "admin"
    admin_password = "admin123"
    hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
    
    db.execute_query(
        "INSERT OR IGNORE INTO usuarios (usuario, hash_contraseña, id_rol) VALUES (?, ?, ?)",
        (admin_user, hashed_password, 2)
    )
    
    db.commit()
    logger.info(f"Usuario administrador creado/actualizado: {admin_user}")

if __name__ == '__main__':
    # Configurar logging
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format=config.LOG_FORMAT
    )
    
    # Inicializar base de datos
    init_database() 