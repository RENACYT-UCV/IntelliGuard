from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Usuario(Base):
    __tablename__ = 'usuarios'

    id_usuario = Column(Integer, primary_key=True)
    usuario = Column(String(50), unique=True, nullable=False)
    hash_contraseña = Column(String(255), nullable=False)
    id_rol = Column(Integer, ForeignKey('rol_usuario.id'), nullable=False)
    
    # Relación con el rol
    rol = relationship("RolUsuario", back_populates="usuarios")

    def __repr__(self):
        return f"<Usuario(id={self.id_usuario}, usuario={self.usuario}, rol={self.id_rol})>"

class RolUsuario(Base):
    __tablename__ = 'rol_usuario'

    id = Column(Integer, primary_key=True)
    rol = Column(String(50), unique=True, nullable=False)
    
    # Relación con usuarios
    usuarios = relationship("Usuario", back_populates="rol")

    def __repr__(self):
        return f"<RolUsuario(id={self.id}, rol={self.rol})>"

class BaseDatosUsuarios:
    def __init__(self, session):
        self.session = session

    def obtener_por_usuario(self, usuario: str):
        return self.session.query(Usuario).filter(Usuario.usuario == usuario).first()

    def obtener_por_id(self, id_usuario: int):
        return self.session.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

    def obtener_por_rol(self, usuario: str, id_rol: int):
        return self.session.query(Usuario).filter(
            Usuario.usuario == usuario,
            Usuario.id_rol == id_rol
        ).first()

    def listar_todos(self):
        return self.session.query(Usuario).all()

    def crear(self, usuario: str, hash_contraseña: str, id_rol: int):
        nuevo_usuario = Usuario(
            usuario=usuario,
            hash_contraseña=hash_contraseña,
            id_rol=id_rol
        )
        self.session.add(nuevo_usuario)
        self.session.commit()
        return nuevo_usuario.id_usuario

    def actualizar(self, id_usuario: int, usuario: str, hash_contraseña: str = None, id_rol: int = None):
        usuario_db = self.obtener_por_id(id_usuario)
        if not usuario_db:
            return False
        
        if usuario:
            usuario_db.usuario = usuario
        if hash_contraseña:
            usuario_db.hash_contraseña = hash_contraseña
        if id_rol:
            usuario_db.id_rol = id_rol
        
        self.session.commit()
        return True

    def eliminar(self, id_usuario: int):
        usuario = self.obtener_por_id(id_usuario)
        if usuario:
            self.session.delete(usuario)
            self.session.commit()
            return True
        return False

    def obtener_por_usuario_y_contraseña(self, usuario: str, hash_contraseña: str):
        return self.session.query(Usuario).filter(
            Usuario.usuario == usuario,
            Usuario.hash_contraseña == hash_contraseña
        ).first()

