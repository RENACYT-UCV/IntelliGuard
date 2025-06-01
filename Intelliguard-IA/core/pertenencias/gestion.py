import os
from datetime import datetime
from pathlib import Path
import sys

# Agregar el directorio raíz al path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

from utils.database import Database
from utils.config import PERTENENCIAS_DIR

class GestionPertenencias:
    def __init__(self):
        """Inicializa el gestor de pertenencias"""
        self.db = Database()
        
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
            # Verificar estudiante
            estudiante = self.db.obtener_uno(
                "SELECT * FROM estudiantes WHERE codigo = ?",
                (codigo_estudiante,)
            )
            
            if not estudiante:
                print(f"Estudiante {codigo_estudiante} no encontrado")
                return False
                
            # Guardar imagen si se proporciona
            ruta_imagen = None
            if imagen is not None:
                os.makedirs(PERTENENCIAS_DIR, exist_ok=True)
                nombre_archivo = f"{codigo_estudiante}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                ruta_imagen = os.path.join(PERTENENCIAS_DIR, nombre_archivo)
                cv2.imwrite(ruta_imagen, imagen)
                
            # Registrar en base de datos
            self.db.ejecutar(
                """
                INSERT INTO pertenencias (
                    codigo_estudiante,
                    tipo_objeto,
                    descripcion,
                    ruta_imagen,
                    fecha_entrada,
                    estado
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    codigo_estudiante,
                    tipo_objeto,
                    descripcion,
                    ruta_imagen,
                    datetime.now(),
                    'ENTREGADO'
                )
            )
            
            print(f"Pertinencia registrada exitosamente para estudiante {codigo_estudiante}")
            return True
            
        except Exception as e:
            print(f"Error al registrar pertenencia: {str(e)}")
            return False
            
    def registrar_salida(self, codigo_estudiante, tipo_objeto):
        """
        Registra la salida de una pertenencia
        
        Args:
            codigo_estudiante: Código del estudiante
            tipo_objeto: Tipo de objeto a retirar
            
        Returns:
            bool: True si se registró exitosamente
        """
        try:
            # Buscar pertenencia
            pertenencia = self.db.obtener_uno(
                """
                SELECT * FROM pertenencias 
                WHERE codigo_estudiante = ? 
                AND tipo_objeto = ? 
                AND estado = 'ENTREGADO'
                ORDER BY fecha_entrada DESC
                LIMIT 1
                """,
                (codigo_estudiante, tipo_objeto)
            )
            
            if not pertenencia:
                print(f"No se encontró pertenencia {tipo_objeto} para estudiante {codigo_estudiante}")
                return False
                
            # Actualizar estado
            self.db.ejecutar(
                """
                UPDATE pertenencias 
                SET estado = 'RETIRADO',
                    fecha_salida = ?
                WHERE id = ?
                """,
                (datetime.now(), pertenencia[0])
            )
            
            print(f"Pertinencia {tipo_objeto} retirada exitosamente por estudiante {codigo_estudiante}")
            return True
            
        except Exception as e:
            print(f"Error al registrar salida: {str(e)}")
            return False
            
    def obtener_pertenencias(self, codigo_estudiante=None, estado=None):
        """
        Obtiene las pertenencias registradas
        
        Args:
            codigo_estudiante: Filtrar por estudiante (opcional)
            estado: Filtrar por estado (opcional)
            
        Returns:
            list: Lista de pertenencias
        """
        try:
            query = "SELECT * FROM pertenencias"
            params = []
            
            if codigo_estudiante or estado:
                query += " WHERE"
                
                if codigo_estudiante:
                    query += " codigo_estudiante = ?"
                    params.append(codigo_estudiante)
                    
                if estado:
                    if codigo_estudiante:
                        query += " AND"
                    query += " estado = ?"
                    params.append(estado)
                    
            query += " ORDER BY fecha_entrada DESC"
            
            return self.db.obtener_todos(query, tuple(params))
            
        except Exception as e:
            print(f"Error al obtener pertenencias: {str(e)}")
            return []
            
    def __del__(self):
        """Cierra la conexión a la base de datos"""
        self.db.cerrar() 