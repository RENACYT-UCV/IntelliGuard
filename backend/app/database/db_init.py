from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models import Base
from ..models.usuario import Usuario, RolUsuario
from ..config.config import config
import bcrypt
import logging

logger = logging.getLogger(__name__)

def crear_roles(session):
    """Crea los roles básicos si no existen"""
    roles = {
        1: "Administrador",
        2: "Personal",
        3: "Estudiante"
    }
    
    for id_rol, nombre_rol in roles.items():
        if not session.query(RolUsuario).filter_by(id=id_rol).first():
            rol = RolUsuario(id=id_rol, rol=nombre_rol)
            session.add(rol)
    
    session.commit()

def crear_usuario_admin(session):
    """Crea el usuario administrador si no existe"""
    if not session.query(Usuario).filter_by(usuario="admin").first():
        # Contraseña numérica por defecto: 123456
        password = "123456"
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        admin = Usuario(
            usuario="admin",
            hash_contraseña=hashed,
            id_rol=1  # Rol Administrador
        )
        session.add(admin)
        session.commit()
        logger.info("Usuario administrador creado con éxito")

def crear_usuario_personal(session):
    """Crea un usuario de personal si no existe"""
    if not session.query(Usuario).filter_by(usuario="personal").first():
        password = "654321"  # Contraseña numérica por defecto
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        personal = Usuario(
            usuario="personal",
            hash_contraseña=hashed,
            id_rol=2  # Rol Personal
        )
        session.add(personal)
        session.commit()
        logger.info("Usuario de personal creado con éxito")

def init_db(force=False):
    """Inicializa la base de datos y crea todas las tablas"""
    try:
        # Crear el engine de SQLAlchemy
        engine = create_engine(config.DATABASE_URL)
        
        if force:
            # Eliminar todas las tablas existentes
            Base.metadata.drop_all(engine)
            logger.info("Base de datos reinicializada")
        
        # Crear todas las tablas
        Base.metadata.create_all(engine)
        
        # Crear la sesión
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Crear roles y usuarios por defecto
        crear_roles(session)
        crear_usuario_admin(session)
        crear_usuario_personal(session)
        
        logger.info("Base de datos inicializada correctamente")
        return session
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
        raise 