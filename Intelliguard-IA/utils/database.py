import sqlite3
from .config import DB_PATH

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.conectar()
        self.crear_tablas()
        
    def conectar(self):
        """Establece conexión con la base de datos"""
        try:
            self.conn = sqlite3.connect(DB_PATH)
            self.cursor = self.conn.cursor()
            print("Conexión a base de datos establecida")
        except Exception as e:
            print(f"Error al conectar a la base de datos: {str(e)}")
            
    def crear_tablas(self):
        """Crea las tablas necesarias si no existen"""
        try:
            # Tabla de estudiantes
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS estudiantes (
                    codigo INTEGER PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de pertenencias
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS pertenencias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo_estudiante INTEGER,
                    tipo_objeto TEXT NOT NULL,
                    descripcion TEXT,
                    fecha_entrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_salida TIMESTAMP,
                    estado TEXT DEFAULT 'en_guardia',
                    FOREIGN KEY (codigo_estudiante) REFERENCES estudiantes(codigo)
                )
            ''')
            
            self.conn.commit()
            print("Tablas creadas exitosamente")
            
        except Exception as e:
            print(f"Error al crear tablas: {str(e)}")
            
    def cerrar(self):
        """Cierra la conexión a la base de datos"""
        if self.conn:
            self.conn.close()
            print("Conexión a base de datos cerrada")
            
    def ejecutar(self, query, params=None):
        """Ejecuta una consulta SQL"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            return self.cursor
        except Exception as e:
            print(f"Error al ejecutar consulta: {str(e)}")
            return None
            
    def obtener_uno(self, query, params=None):
        """Obtiene un solo resultado"""
        cursor = self.ejecutar(query, params)
        if cursor:
            return cursor.fetchone()
        return None
        
    def obtener_todos(self, query, params=None):
        """Obtiene todos los resultados"""
        cursor = self.ejecutar(query, params)
        if cursor:
            return cursor.fetchall()
        return [] 