import bcrypt
from app.models.usuario import BaseDatosUsuarios

def init_db():
    print("Inicializando base de datos...")
    db = BaseDatosUsuarios()
    
    # Crear usuario administrador si no existe
    admin_user = "admin"
    admin_password = "123456"
    
    # Verificar si el usuario admin ya existe
    if not db.consultar_usuario_administrador(admin_user):
        # Hash de la contraseña
        hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
        
        # Agregar usuario administrador (id_rol = 2 para Administrador)
        db.agregar_usuario(admin_user, hashed_password, 2)
        print(f"Usuario administrador creado exitosamente:")
        print(f"Usuario: {admin_user}")
        print(f"Contraseña: {admin_password}")
    else:
        print("El usuario administrador ya existe")
    
    print("Inicialización completada")

if __name__ == "__main__":
    init_db() 