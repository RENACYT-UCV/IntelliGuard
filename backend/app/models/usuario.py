from ..utils.database import Database

class Usuario:
    def __init__(self, id_usuario, usuario, hash_contraseña, id_rol, rol):
        self.id_usuario = id_usuario
        self.usuario = usuario
        self.hash_contraseña = hash_contraseña
        self.id_rol = id_rol
        self.rol = rol

class BaseDatosUsuarios:
    def __init__(self):
        self.db = Database()
        self.conexion = self.db.get_connection()
        self.crear_tabla_roles()
        self.crear_tabla_usuarios()

    def crear_tabla_roles(self):
        cursor = self.conexion.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS rol_usuario (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            rol TEXT NOT NULL
                        )''')
        # Insertar roles básicos si no existen
        cursor.execute("INSERT OR IGNORE INTO rol_usuario (id, rol) VALUES (1, 'Personal')")
        cursor.execute("INSERT OR IGNORE INTO rol_usuario (id, rol) VALUES (2, 'Administrador')")
        self.conexion.commit()

    def crear_tabla_usuarios(self):
        cursor = self.conexion.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                                usuario TEXT NOT NULL,
                                hash_contraseña TEXT NOT NULL,
                                id_rol INTEGER NOT NULL,
                                FOREIGN KEY (id_rol) REFERENCES rol_usuario(id)
                            )''')
        self.conexion.commit()

    def agregar_usuario(self, usuario, contraseña, idRol):
        cursor = self.conexion.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, hash_contraseña, id_rol) VALUES (?, ?, ?)", 
                          (usuario, contraseña, idRol))
        self.conexion.commit()

    def consultar_usuario_por_usuario(self, usuario):
        cursor = self.conexion.cursor()
        cursor.execute("""
            SELECT u.id_usuario, u.usuario, u.hash_contraseña, u.id_rol, r.rol
            FROM usuarios u
            LEFT JOIN rol_usuario r ON u.id_rol = r.id
            WHERE u.usuario = ?
        """, (usuario,))
        resultado = cursor.fetchone()
        if resultado:
            id_usuario, usuario, hash_contraseña, id_rol, rol = resultado
            return Usuario(id_usuario, usuario, hash_contraseña, id_rol, rol)
        else:
            return None

    def consultar_usuario_personal(self, usuario):
        cursor = self.conexion.cursor()
        rol_id = 1  # ID del rol de personal
        cursor.execute("""
            SELECT u.id_usuario, u.usuario, u.hash_contraseña, u.id_rol, r.rol
            FROM usuarios u
            LEFT JOIN rol_usuario r ON u.id_rol = r.id
            WHERE u.usuario = ? AND u.id_rol = ?
        """, (usuario, rol_id))
        resultado = cursor.fetchone()
        if resultado:
            id_usuario, usuario, hash_contraseña, id_rol, rol = resultado
            return Usuario(id_usuario, usuario, hash_contraseña, id_rol, rol)
        else:
            return None

    def consultar_usuario_administrador(self, usuario):
        cursor = self.conexion.cursor()
        rol_id = 2  # ID del rol de administrador
        cursor.execute("""
            SELECT u.id_usuario, u.usuario, u.hash_contraseña, u.id_rol, r.rol
            FROM usuarios u
            LEFT JOIN rol_usuario r ON u.id_rol = r.id
            WHERE u.usuario = ? AND u.id_rol = ?
        """, (usuario, rol_id))
        resultado = cursor.fetchone()
        if resultado:
            id_usuario, usuario, hash_contraseña, id_rol, rol = resultado
            return Usuario(id_usuario, usuario, hash_contraseña, id_rol, rol)
        else:
            return None

    def consultar_usuario_por_id(self, id_usuario):
        cursor = self.conexion.cursor()
        cursor.execute("""
            SELECT u.id_usuario, u.usuario, u.hash_contraseña, u.id_rol, r.rol
            FROM usuarios u
            LEFT JOIN rol_usuario r ON u.id_rol = r.id
            WHERE u.id_usuario = ?
        """, (id_usuario,))
        resultado = cursor.fetchone()
        if resultado:
            id_usuario, usuario, hash_contraseña, id_rol, rol = resultado
            return Usuario(id_usuario, usuario, hash_contraseña, id_rol, rol)
        else:
            return None

    def listar_usuarios(self):
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                SELECT u.id_usuario, u.usuario, u.hash_contraseña, u.id_rol, r.rol
                FROM usuarios u
                LEFT JOIN rol_usuario r ON u.id_rol = r.id
            """)
            resultados = cursor.fetchall()
            usuarios = []
            for resultado in resultados:
                id_usuario, usuario, hash_contraseña, id_rol, rol = resultado
                usuarios.append(Usuario(id_usuario, usuario, hash_contraseña, id_rol, rol))
            return usuarios
        except Exception as e:
            print(f"Error al listar usuarios: {e}")
            return []
    
    def editar_usuario(self, id_usuario, nuevo_usuario, nueva_contraseña, nuevo_id_rol):
        cursor = self.conexion.cursor()
        if nueva_contraseña:  # Si la nueva contraseña no está vacía
            cursor.execute("""
                UPDATE usuarios 
                SET usuario = ?, hash_contraseña = ?, id_rol = ? 
                WHERE id_usuario = ?
            """, (nuevo_usuario, nueva_contraseña, nuevo_id_rol, id_usuario))
        else:
            cursor.execute("""
                UPDATE usuarios 
                SET usuario = ?, id_rol = ? 
                WHERE id_usuario = ?
            """, (nuevo_usuario, nuevo_id_rol, id_usuario))
            
        self.conexion.commit()

    def eliminar_usuario(self, id_usuario):
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = ?", (id_usuario,))
        self.conexion.commit()

