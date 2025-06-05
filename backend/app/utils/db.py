import sqlite3
import os

def get_db_connection():
    """
    Obtiene una conexión a la base de datos SQLite.
    La base de datos se crea si no existe.
    """
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'basededatos.db')
    
    # Crear la base de datos y la tabla si no existen
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Crear tabla de estudiantes si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estudiantes (
            codigo TEXT PRIMARY KEY,
            nombres TEXT NOT NULL,
            carrera TEXT NOT NULL,
            plan TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    return conn 