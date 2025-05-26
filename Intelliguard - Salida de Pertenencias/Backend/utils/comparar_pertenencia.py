import cv2
import numpy as np
from flask import current_app
import os
from collections import defaultdict

def calcular_similitud(img1, img2):
    # Asegurarse de que las imágenes tengan el mismo tamaño
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    
    hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    hist1 = cv2.calcHist([hsv1], [0, 1], None, [180, 256], [0, 180, 0, 256])
    hist2 = cv2.calcHist([hsv2], [0, 1], None, [180, 256], [0, 180, 0, 256])
    cv2.normalize(hist1, hist1, 0, 1, cv2.NORM_MINMAX)
    cv2.normalize(hist2, hist2, 0, 1, cv2.NORM_MINMAX)
    similitud = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return similitud

def ordenar_imagenes_por_similitud(imagen_entrada, registros_pertenencia):
    resultados = defaultdict(lambda: {'similitudes': [], 'rutas': [], 'codigo': ''})
    
    UPLOAD_FOLDER = 'uploads/pertenencia'
    directory = os.path.join(current_app.root_path, UPLOAD_FOLDER)
    
    for registro in registros_pertenencia:
        ruta_completa = os.path.join(directory, registro.imagen_pertenencia)
        if os.path.exists(ruta_completa):
            imagen_objeto = cv2.imread(ruta_completa)
            if imagen_objeto is not None:
                similitud = calcular_similitud(imagen_entrada, imagen_objeto)
                resultados[registro.codigoPertenencia]['similitudes'].append(similitud)
                resultados[registro.codigoPertenencia]['rutas'].append(ruta_completa)
                resultados[registro.codigoPertenencia]['codigo'] = registro.codigoPertenencia
                print(f"Código: {registro.codigoPertenencia}, Ruta: {ruta_completa}, Similitud: {similitud}")
            else:
                print(f"No se pudo leer la imagen: {ruta_completa}")

    resultados_finales = []
    for codigo, datos in resultados.items():
        similitudes = np.array(datos['similitudes'])
        if len(similitudes) > 0:
            #valor_representativo = np.mean(similitudes)  # Promedio
            # valor_representativo = np.median(similitudes)  # Mediana
            valor_representativo = np.average(similitudes, weights=similitudes)  # Media ponderada
            # valor_representativo = np.sqrt(np.mean(similitudes**2))  # RMS
            # valor_representativo = np.percentile(similitudes, 75)  # Percentil 75

            resultados_finales.append({
                'codigo': codigo,
                'similitud': valor_representativo,
                'ruta': datos['rutas'][np.argmax(similitudes)]  # Ruta de la imagen con mayor similitud
            })

    resultados_finales.sort(key=lambda x: x['similitud'], reverse=True)

    
    return resultados_finales