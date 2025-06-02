# Intelliguard-IA

Sistema unificado de reconocimiento facial, detección de objetos y gestión de pertenencias.

## Estructura del Proyecto

```
Intelliguard-IA/
├── core/                    # Módulos principales
│   ├── reconocimiento/      # Reconocimiento facial
│   ├── objetos/            # Detección de objetos
│   └── pertenencias/       # Gestión de pertenencias
├── data/                   # Datos y modelos
│   ├── models/            # Modelos entrenados
│   │   ├── facial/       # Modelos de reconocimiento facial
│   │   └── objetos/      # Modelos de detección de objetos
│   ├── datasets/         # Datasets para entrenamiento
│   │   ├── facial/      # Imágenes de rostros
│   │   └── objetos/     # Imágenes de objetos
│   └── pertenencias/    # Imágenes de pertenencias
├── utils/                # Utilidades
│   ├── config.py        # Configuración del sistema
│   └── database.py      # Gestión de base de datos
├── scripts/             # Scripts de utilidad
│   └── inicializar.py   # Inicialización del sistema
├── test_sistema.py      # Script de prueba
└── requirements.txt     # Dependencias
```

## Requisitos

- Python 3.10 o superior
- OpenCV
- NumPy
- Ultralytics (YOLO)
- imutils
- pathlib

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd Intelliguard-IA
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Inicializar el sistema:
```bash
python scripts/inicializar.py
```

## Uso

### Reconocimiento Facial

```python
from core.reconocimiento.facial import ReconocimientoFacial

# Inicializar reconocedor
reconocedor = ReconocimientoFacial()

# Capturar nuevo rostro
reconocedor.capturar_rostro("12345")  # Código del estudiante

# Reconocer rostro
codigo, porcentaje = reconocedor.reconocimiento_facial(imagen)
```

### Detección de Objetos

```python
from core.objetos.deteccion import DeteccionObjetos

# Inicializar detector
detector = DeteccionObjetos()

# Detectar objeto en imagen
etiqueta, objeto = detector.procesar_imagen("ruta/imagen.jpg")

# Entrenar modelo
detector.entrenar_modelo()
```

### Gestión de Pertenencias

```python
from core.pertenencias.gestion import GestionPertenencias

# Inicializar gestor
gestor = GestionPertenencias()

# Registrar entrada
gestor.registrar_entrada(
    codigo_estudiante="12345",
    tipo_objeto="mochila",
    descripcion="Mochila negra",
    imagen=imagen  # Opcional
)

# Registrar salida
gestor.registrar_salida(
    codigo_estudiante="12345",
    tipo_objeto="mochila"
)

# Consultar pertenencias
pertenencias = gestor.obtener_pertenencias(
    codigo_estudiante="12345",  # Opcional
    estado="ENTREGADO"         # Opcional
)
```

### Prueba del Sistema

Para probar todas las funcionalidades:

```bash
python test_sistema.py
```

## Notas Importantes

1. **Reconocimiento Facial**:
   - Se requieren al menos 10 fotos por estudiante
   - Las fotos deben ser claras y con buena iluminación
   - El modelo se entrena automáticamente al agregar nuevas fotos

2. **Detección de Objetos**:
   - Se requiere un dataset de entrenamiento en formato YOLO
   - El modelo base es YOLOv8n
   - Se puede entrenar con datos personalizados

3. **Gestión de Pertenencias**:
   - La base de datos se crea automáticamente
   - Se requieren imágenes claras de los objetos
   - Se mantiene un registro de entradas y salidas

## Solución de Problemas

1. **Error al cargar modelos**:
   - Verificar que los archivos existan en las rutas correctas
   - Ejecutar el script de inicialización

2. **Error en reconocimiento facial**:
   - Verificar la calidad de las imágenes
   - Ajustar el umbral de confianza en config.py

3. **Error en detección de objetos**:
   - Verificar el formato del dataset
   - Ajustar los parámetros de entrenamiento

4. **Error en base de datos**:
   - Verificar permisos de escritura
   - Ejecutar el script de inicialización

## Contribución

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request 
