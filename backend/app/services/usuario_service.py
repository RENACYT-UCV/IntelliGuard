import bcrypt
from typing import Optional, List
from ..models.usuario import Usuario, UsuarioModel

class UsuarioService:
    @staticmethod
    def autenticar(usuario: str, contraseña: str) -> Optional[Usuario]:
        """Autentica un usuario con su contraseña"""
        user = UsuarioModel.obtener_por_usuario(usuario)
        if not user:
            return None
        
        if bcrypt.checkpw(contraseña.encode('utf-8'), user.hash_contraseña):
            return user
        return None

    @staticmethod
    def crear_usuario(usuario: str, contraseña: str, id_rol: int) -> Optional[Usuario]:
        """Crea un nuevo usuario"""
        # Verificar si el usuario ya existe
        if UsuarioModel.obtener_por_usuario(usuario):
            return None
        
        # Hash de la contraseña
        hash_contraseña = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
        
        # Crear usuario
        id_usuario = UsuarioModel.crear(usuario, hash_contraseña, id_rol)
        return UsuarioModel.obtener_por_id(id_usuario)

    @staticmethod
    def actualizar_usuario(id_usuario: int, usuario: str, contraseña: Optional[str], id_rol: int) -> Optional[Usuario]:
        """Actualiza un usuario existente"""
        # Verificar si el usuario existe
        user_actual = UsuarioModel.obtener_por_id(id_usuario)
        if not user_actual:
            return None
        
        # Si se proporciona contraseña, hacer hash
        hash_contraseña = None
        if contraseña:
            hash_contraseña = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
        
        # Actualizar usuario
        if UsuarioModel.actualizar(id_usuario, usuario, hash_contraseña, id_rol):
            return UsuarioModel.obtener_por_id(id_usuario)
        return None

    @staticmethod
    def eliminar_usuario(id_usuario: int) -> bool:
        """Elimina un usuario"""
        return UsuarioModel.eliminar(id_usuario)

    @staticmethod
    def listar_usuarios() -> List[Usuario]:
        """Lista todos los usuarios"""
        return UsuarioModel.listar_todos()

    @staticmethod
    def obtener_usuario(id_usuario: int) -> Optional[Usuario]:
        """Obtiene un usuario por su ID"""
        return UsuarioModel.obtener_por_id(id_usuario)

    @staticmethod
    def obtener_usuario_por_nombre(usuario: str) -> Optional[Usuario]:
        """Obtiene un usuario por su nombre de usuario"""
        return UsuarioModel.obtener_por_usuario(usuario)

    @staticmethod
    def es_administrador(usuario: Usuario) -> bool:
        """Verifica si un usuario es administrador"""
        return usuario.id_rol == 2

    @staticmethod
    def es_personal(usuario: Usuario) -> bool:
        """Verifica si un usuario es personal"""
        return usuario.id_rol == 1 