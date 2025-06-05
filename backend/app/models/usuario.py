from dataclasses import dataclass
from typing import Optional
from ..database.db_manager import db

@dataclass
class Usuario:
    id_usuario: int
    usuario: str
    hash_contraseña: str
    id_rol: int
    rol: str

class UsuarioModel:
    TABLA_USUARIOS = 'usuarios'
    TABLA_ROLES = 'rol_usuario'

    @staticmethod
    def obtener_por_usuario(usuario: str) -> Optional[Usuario]:
        query = """
            SELECT u.id_usuario, u.usuario, u.hash_contraseña, u.id_rol, r.rol
            FROM usuarios u
            LEFT JOIN rol_usuario r ON u.id_rol = r.id
            WHERE u.usuario = ?
        """
        resultado = db.fetch_one(query, (usuario,))
        return Usuario(*resultado) if resultado else None

    @staticmethod
    def obtener_por_id(id_usuario: int) -> Optional[Usuario]:
        query = """
            SELECT u.id_usuario, u.usuario, u.hash_contraseña, u.id_rol, r.rol
            FROM usuarios u
            LEFT JOIN rol_usuario r ON u.id_rol = r.id
            WHERE u.id_usuario = ?
        """
        resultado = db.fetch_one(query, (id_usuario,))
        return Usuario(*resultado) if resultado else None

    @staticmethod
    def obtener_por_rol(usuario: str, id_rol: int) -> Optional[Usuario]:
        query = """
            SELECT u.id_usuario, u.usuario, u.hash_contraseña, u.id_rol, r.rol
            FROM usuarios u
            LEFT JOIN rol_usuario r ON u.id_rol = r.id
            WHERE u.usuario = ? AND u.id_rol = ?
        """
        resultado = db.fetch_one(query, (usuario, id_rol))
        return Usuario(*resultado) if resultado else None

    @staticmethod
    def listar_todos() -> list[Usuario]:
        query = """
            SELECT u.id_usuario, u.usuario, u.hash_contraseña, u.id_rol, r.rol
            FROM usuarios u
            LEFT JOIN rol_usuario r ON u.id_rol = r.id
        """
        resultados = db.fetch_all(query)
        return [Usuario(*resultado) for resultado in resultados]

    @staticmethod
    def crear(usuario: str, hash_contraseña: str, id_rol: int) -> int:
        query = """
            INSERT INTO usuarios (usuario, hash_contraseña, id_rol)
            VALUES (?, ?, ?)
        """
        cursor = db.execute_query(query, (usuario, hash_contraseña, id_rol))
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def actualizar(id_usuario: int, usuario: str, hash_contraseña: Optional[str], id_rol: int) -> bool:
        if hash_contraseña:
            query = """
                UPDATE usuarios 
                SET usuario = ?, hash_contraseña = ?, id_rol = ? 
                WHERE id_usuario = ?
            """
            params = (usuario, hash_contraseña, id_rol, id_usuario)
        else:
            query = """
                UPDATE usuarios 
                SET usuario = ?, id_rol = ? 
                WHERE id_usuario = ?
            """
            params = (usuario, id_rol, id_usuario)
        
        db.execute_query(query, params)
        db.commit()
        return True

    @staticmethod
    def eliminar(id_usuario: int) -> bool:
        query = "DELETE FROM usuarios WHERE id_usuario = ?"
        db.execute_query(query, (id_usuario,))
        db.commit()
        return True

    @staticmethod
    def obtener_por_usuario_y_contraseña(usuario: str, hash_contraseña: str) -> Optional[Usuario]:
        query = """
            SELECT u.id_usuario, u.usuario, u.hash_contraseña, u.id_rol, r.rol
            FROM usuarios u
            LEFT JOIN rol_usuario r ON u.id_rol = r.id
            WHERE u.usuario = ? AND u.hash_contraseña = ?
        """
        resultado = db.fetch_one(query, (usuario, hash_contraseña))
        return Usuario(*resultado) if resultado else None

