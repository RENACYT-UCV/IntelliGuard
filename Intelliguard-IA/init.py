from utils.config import crear_directorios
import cv2
import os

def init_facial():
    """Inicializa el sistema de reconocimiento facial"""
    # Crear directorios necesarios
    crear_directorios()
    
    # Verificar que OpenCV puede cargar el clasificador Haar Cascade
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    if not os.path.exists(cascade_path):
        raise Exception(f"No se encontró el clasificador Haar Cascade en {cascade_path}")
    
    detector = cv2.CascadeClassifier(cascade_path)
    if detector.empty():
        raise Exception("Error al cargar el clasificador Haar Cascade")
    
    print("Sistema de reconocimiento facial inicializado correctamente")

if __name__ == "__main__":
    init_facial() 