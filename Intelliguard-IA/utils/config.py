import os

# Rutas base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Rutas de modelos
MODELO_FACIAL = os.path.join(BASE_DIR, 'data', 'models', 'facial', 'modeloEstudiantes.xml')
MODELO_OBJETOS = os.path.join(BASE_DIR, 'data', 'models', 'objetos', 'ModelObjetoFinal.pt')

# Rutas de datos
DATASET_FACIAL = os.path.join(BASE_DIR, 'data', 'datasets', 'facial')
DATASET_OBJETOS = os.path.join(BASE_DIR, 'data', 'datasets', 'objetos')
PERTENENCIAS_DIR = os.path.join(BASE_DIR, 'data', 'pertenencias')

# Configuraciones de reconocimiento facial
CONFIANZA_MINIMA = 0.5
MAX_FOTOS = 10

# Configuraciones de detección de objetos
CONFIANZA_OBJETO = 0.5

# Configuraciones de base de datos
DB_PATH = os.path.join(BASE_DIR, 'data', 'pertenencias', 'basededatos.db')

# Asegurar que las carpetas existan
def crear_directorios():
    directorios = [
        os.path.dirname(MODELO_FACIAL),
        os.path.dirname(MODELO_OBJETOS),
        DATASET_FACIAL,
        DATASET_OBJETOS,
        PERTENENCIAS_DIR,
        os.path.dirname(DB_PATH)
    ]
    
    for directorio in directorios:
        if not os.path.exists(directorio):
            os.makedirs(directorio)
            print(f"Directorio creado: {directorio}")

# Crear directorios al importar el módulo
crear_directorios() 