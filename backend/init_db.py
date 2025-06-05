import bcrypt
from app.models.usuario import BaseDatosUsuarios
import sqlite3
import os

def init_db():
    print("Inicializando base de datos...")
    
    # Forzar la creación de un nuevo usuario administrador
    db = BaseDatosUsuarios()
    admin_user = "admin"
    admin_password = "123123"
    
    try:
        # Hash de la contraseña
        hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
        
        # Eliminar el usuario admin si existe
        cursor = db.conexion.cursor()
        cursor.execute("DELETE FROM usuarios WHERE usuario = ?", (admin_user,))
        
        # Agregar el nuevo usuario administrador (id_rol = 2 para Administrador)
        db.agregar_usuario(admin_user, hashed_password, 2)
        db.conexion.commit()
        
        print(f"Usuario administrador creado/actualizado exitosamente:")
        print(f"Usuario: {admin_user}")
        print(f"Contraseña: {admin_password}")
    except Exception as e:
        print(f"Error al crear usuario administrador: {str(e)}")
    
    print("Inicialización completada")

if __name__ == "__main__":
    init_db() 