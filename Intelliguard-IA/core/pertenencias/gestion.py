import os
import sqlite3
from datetime import datetime
from pathlib import Path
import sys
import cv2

# Agregar el directorio raíz al path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

from utils.config import DB_PATH

class GestionPertenencias:
    def __init__(self):
        """Inicializa el gestor de pertenencias"""
        self.crear_tablas()
        
    def crear_tablas(self):
        """Crea las tablas necesarias si no existen"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Tabla de pertenencias
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pertenencias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo_estudiante TEXT NOT NULL,
                    tipo_objeto TEXT NOT NULL,
                    descripcion TEXT,
                    ruta_imagen TEXT NOT NULL,
                    fecha_entrada DATETIME DEFAULT CURRENT_TIMESTAMP,
                    fecha_salida DATETIME,
                    estado TEXT DEFAULT 'entrada'
                )
            ''')
            
            conn.commit()
            conn.close()
            print("Tablas creadas exitosamente")
        except Exception as e:
            print(f"Error al crear tablas: {str(e)}")
            
    def registrar_pertenencia(self, codigo_estudiante, tipo_objeto, descripcion, ruta_imagen):
        """
        Registra una nueva pertenencia
        
        Args:
            codigo_estudiante: Código del estudiante
            tipo_objeto: Tipo de objeto
            descripcion: Descripción adicional
            ruta_imagen: Ruta de la imagen guardada
            
        Returns:
            dict: Resultado de la operación
        """
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO pertenencias (codigo_estudiante, tipo_objeto, descripcion, ruta_imagen)
                VALUES (?, ?, ?, ?)
            ''', (codigo_estudiante, tipo_objeto, descripcion, ruta_imagen))
            
            conn.commit()
            conn.close()
            
            return {
                'mensaje': 'Pertenencia registrada exitosamente',
                'codigo_estudiante': codigo_estudiante,
                'tipo_objeto': tipo_objeto
            }
        except Exception as e:
            return {'error': str(e)}
            
    def registrar_salida(self, codigo_estudiante, tipo_objeto):
        """
        Registra la salida de una pertenencia
        
        Args:
            codigo_estudiante: Código del estudiante
            tipo_objeto: Tipo de objeto
            
        Returns:
            dict: Resultado de la operación
        """
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Verificar si existe una entrada sin salida
            cursor.execute('''
                SELECT id FROM pertenencias 
                WHERE codigo_estudiante = ? 
                AND tipo_objeto = ? 
                AND estado = 'entrada'
            ''', (codigo_estudiante, tipo_objeto))
            
            resultado = cursor.fetchone()
            if not resultado:
                return {'error': 'No se encontró una entrada registrada para este objeto'}
                
            # Registrar salida
            cursor.execute('''
                UPDATE pertenencias 
                SET fecha_salida = CURRENT_TIMESTAMP,
                    estado = 'salida'
                WHERE id = ?
            ''', (resultado[0],))
            
            conn.commit()
            conn.close()
            
            return {
                'mensaje': 'Salida registrada exitosamente',
                'codigo_estudiante': codigo_estudiante,
                'tipo_objeto': tipo_objeto
            }
        except Exception as e:
            return {'error': str(e)}
            
    def consultar_pertenencias(self, codigo_estudiante):
        """
        Consulta las pertenencias de un estudiante
        
        Args:
            codigo_estudiante: Código del estudiante
            
        Returns:
            list: Lista de pertenencias
        """
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT tipo_objeto, descripcion, fecha_entrada, fecha_salida, estado, ruta_imagen
                FROM pertenencias 
                WHERE codigo_estudiante = ?
                ORDER BY fecha_entrada DESC
            ''', (codigo_estudiante,))
            
            pertenencias = []
            for row in cursor.fetchall():
                pertenencias.append({
                    'tipo_objeto': row[0],
                    'descripcion': row[1],
                    'fecha_entrada': row[2],
                    'fecha_salida': row[3],
                    'estado': row[4],
                    'ruta_imagen': row[5]
                })
                
            conn.close()
            return pertenencias
        except Exception as e:
            return {'error': str(e)}
            
    def registrar_estudiante(self, codigo_estudiante):
        """
        Registra un estudiante en la base de datos si no existe
        
        Args:
            codigo_estudiante: Código del estudiante
            
        Returns:
            bool: True si el estudiante existe o se registró exitosamente
        """
        try:
            # Verificar si el estudiante ya existe
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM pertenencias 
                WHERE codigo_estudiante = ?
            ''', (codigo_estudiante,))
            
            estudiante = cursor.fetchone()
            conn.close()
            
            if estudiante:
                return True
                
            # Si no existe, registrarlo
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO pertenencias (codigo_estudiante, nombre, apellido)
                VALUES (?, ?, ?)
            ''', (codigo_estudiante, f"Estudiante {codigo_estudiante}", "No especificado"))
            
            conn.commit()
            conn.close()
            print(f"Estudiante {codigo_estudiante} registrado automáticamente")
            return True
            
        except Exception as e:
            print(f"Error al registrar estudiante: {str(e)}")
            return False
        
    def registrar_entrada(self, codigo_estudiante, tipo_objeto, descripcion, imagen=None):
        """
        Registra la entrada de una pertenencia
        
        Args:
            codigo_estudiante: Código del estudiante
            tipo_objeto: Tipo de objeto detectado
            descripcion: Descripción adicional del objeto
            imagen: Imagen del objeto (opcional)
            
        Returns:
            bool: True si se registró exitosamente
        """
        try:
            # Registrar estudiante si no existe
            if not self.registrar_estudiante(codigo_estudiante):
                return False
                
            # Guardar imagen si se proporciona
            ruta_imagen = None
            if imagen is not None:
                os.makedirs(PERTENENCIAS_DIR, exist_ok=True)
                nombre_archivo = f"{codigo_estudiante}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                ruta_imagen = os.path.join(PERTENENCIAS_DIR, nombre_archivo)
                cv2.imwrite(ruta_imagen, imagen)
                
            # Registrar en base de datos
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO pertenencias (codigo_estudiante, tipo_objeto, descripcion, ruta_imagen, estado)
                VALUES (?, ?, ?, ?, ?)
            ''', (codigo_estudiante, tipo_objeto, descripcion, ruta_imagen, 'ENTREGADO'))
            
            conn.commit()
            conn.close()
            
            print(f"Pertinencia registrada exitosamente para estudiante {codigo_estudiante}")
            return True
            
        except Exception as e:
            print(f"Error al registrar pertenencia: {str(e)}")
            return False
            
    def obtener_pertenencias(self, codigo_estudiante=None, estado=None):
        """
        Obtiene las pertenencias registradas
        
        Args:
            codigo_estudiante: Filtrar por estudiante (opcional)
            estado: Filtrar por estado (opcional)
            
        Returns:
            list: Lista de pertenencias (como diccionarios)
        """
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            query = "SELECT id, codigo_estudiante, tipo_objeto, descripcion, ruta_imagen, fecha_entrada, fecha_salida, estado FROM pertenencias"
            params = []
            if codigo_estudiante or estado:
                query += " WHERE"
                if codigo_estudiante:
                    query += " codigo_estudiante = ?"
                    params.append(codigo_estudiante)
                if estado:
                    if codigo_estudiante:
                        query += " AND"
                    query += " UPPER(estado) = ?"
                    params.append(estado.upper())
            query += " ORDER BY fecha_entrada DESC"
            
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            conn.close()
            # Devuelve una lista de diccionarios
            return [
                {
                    "id": row[0],
                    "codigo_estudiante": row[1],
                    "tipo_objeto": row[2],
                    "descripcion": row[3],
                    "ruta_imagen": row[4],
                    "fecha_entrada": row[5],
                    "fecha_salida": row[6],
                    "estado": row[7]
                }
                for row in rows
            ]
        except Exception as e:
            print(f"Error al obtener pertenencias: {str(e)}")
            return []
            
    def __del__(self):
        """Cierra la conexión a la base de datos"""
        pass 