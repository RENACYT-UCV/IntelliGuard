import sqlite3
from ..config import Config

def init_db():
    conn = sqlite3.connect(Config.DATABASE_URL)
    cursor = conn.cursor()

    # Crear tabla de roles
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rol_usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rol TEXT NOT NULL
    )
    ''')

    # Insertar roles por defecto si no existen
    cursor.execute("SELECT COUNT(*) FROM rol_usuario")
    if cursor.fetchone()[0] == 0:
        roles = [
            (1, 'Personal'),
            (2, 'Administrador')
        ]
        cursor.executemany("INSERT INTO rol_usuario (id, rol) VALUES (?, ?)", roles)

    # Crear tabla de usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL UNIQUE,
        hash_contraseña TEXT NOT NULL,
        id_rol INTEGER NOT NULL,
        FOREIGN KEY (id_rol) REFERENCES rol_usuario(id)
    )
    ''')

    # Crear tabla de estudiantes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS estudiantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT NOT NULL UNIQUE,
        nombres TEXT NOT NULL,
        carrera TEXT NOT NULL,
        plan TEXT NOT NULL
    )
    ''')

    # Crear usuario administrador por defecto si no existe
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE id_rol = 2")
    if cursor.fetchone()[0] == 0:
        import bcrypt
        admin_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO usuarios (usuario, hash_contraseña, id_rol) VALUES (?, ?, ?)",
            ('admin', admin_password, 2)
        )

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de datos inicializada correctamente") 