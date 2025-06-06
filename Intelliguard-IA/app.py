from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
from core.reconocimiento.facial import ReconocimientoFacial
from core.pertenencias.gestion import GestionPertenencias
from core.objetos.deteccion import DeteccionObjetos
import os
from datetime import datetime
from utils.config import ROOT_DIR, DATASET_FACIAL

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# Inicializar servicios
reconocedor = ReconocimientoFacial()
gestionador = GestionPertenencias()
detector = DeteccionObjetos()

@app.route('/ia/reconocimiento/capturar', methods=['POST'])
def capturar_rostro():
    try:
        data = request.json
        codigo_estudiante = data.get('codigo_estudiante')
        if not codigo_estudiante:
            return jsonify({'error': 'Código de estudiante requerido'}), 400
            
        reconocedor.capturar_rostro(codigo_estudiante)
        return jsonify({'mensaje': 'Rostro capturado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ia/reconocimiento/verificar', methods=['POST'])
def verificar_rostro():
    try:
        # Obtener imagen en base64
        data = request.json
        imagen_base64 = data.get('imagen')
        if not imagen_base64:
            return jsonify({'error': 'Imagen requerida'}), 400
        # Convertir base64 a imagen (ya viene puro, sin prefijo)
        imagen_bytes = base64.b64decode(imagen_base64)
        nparr = np.frombuffer(imagen_bytes, np.uint8)
        imagen = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # Realizar reconocimiento
        codigo, confianza = reconocedor.reconocimiento_facial(imagen)
        return jsonify({
            'codigo_estudiante': codigo,
            'confianza': confianza
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ia/pertenencias/registrar', methods=['POST'])
def registrar_pertenencia():
    try:
        data = request.json
        codigo_estudiante = data.get('codigo_estudiante')
        tipo_objeto = data.get('tipo_objeto')
        descripcion = data.get('descripcion')
        imagen_base64 = data.get('imagen')

        if not all([codigo_estudiante, tipo_objeto, imagen_base64]):
            return jsonify({'error': 'Faltan datos requeridos'}), 400

        # Convertir base64 a imagen
        imagen_bytes = base64.b64decode(imagen_base64.split(',')[1])
        nparr = np.frombuffer(imagen_bytes, np.uint8)
        imagen = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Guardar imagen
        ruta_imagen = detector.guardar_imagen(imagen, codigo_estudiante, tipo_objeto)
        if not ruta_imagen:
            return jsonify({'error': 'Error al guardar la imagen'}), 500

        # Registrar en la base de datos
        resultado = gestionador.registrar_pertenencia(
            codigo_estudiante=codigo_estudiante,
            tipo_objeto=tipo_objeto,
            descripcion=descripcion,
            ruta_imagen=ruta_imagen
        )
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ia/pertenencias/consultar', methods=['GET'])
def consultar_pertenencias():
    try:
        codigo_estudiante = request.args.get('codigo_estudiante')
        resultado = gestionador.consultar_pertenencias(codigo_estudiante)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ia/objetos/detectar', methods=['POST'])
def detectar_objetos():
    try:
        # Obtener imagen en base64
        data = request.json
        imagen_base64 = data.get('imagen')
        if not imagen_base64:
            return jsonify({'error': 'Imagen requerida'}), 400
            
        # Convertir base64 a imagen
        imagen_bytes = base64.b64decode(imagen_base64.split(',')[1])
        nparr = np.frombuffer(imagen_bytes, np.uint8)
        imagen = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Detectar objetos
        objetos = detector.detectar_objetos(imagen)
        return jsonify(objetos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ia/estudiantes/registrar', methods=['POST'])
def registrar_estudiante():
    try:
        data = request.json
        codigo_estudiante = data.get('codigo_estudiante')
        imagenes_base64 = data.get('imagenes', [])
        
        if not codigo_estudiante or not imagenes_base64:
            return jsonify({'error': 'Faltan datos requeridos'}), 400

        # Asegurar que el directorio DATASET_FACIAL existe
        os.makedirs(DATASET_FACIAL, exist_ok=True)

        # Guardar cada imagen
        rutas_imagenes = []
        for i, imagen_base64 in enumerate(imagenes_base64):
            # Convertir base64 a imagen
            imagen_bytes = base64.b64decode(imagen_base64)
            nparr = np.frombuffer(imagen_bytes, np.uint8)
            imagen = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Convertir a escala de grises para el reconocimiento facial
            gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
            
            # Detectar rostros
            rostros = reconocedor.detector.detectMultiScale(
                gris,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            if len(rostros) > 0:
                # Tomar el primer rostro detectado
                x, y, w, h = rostros[0]
                rostro = gris[y:y+h, x:x+w]
                
                # Guardar rostro en DATASET_FACIAL
                ruta_imagen = os.path.join(DATASET_FACIAL, f"{codigo_estudiante}_{i}.jpg")
                cv2.imwrite(ruta_imagen, rostro)
                rutas_imagenes.append(ruta_imagen)
            else:
                print(f"No se detectó rostro en la imagen {i}")

        if not rutas_imagenes:
            return jsonify({'error': 'No se detectaron rostros en ninguna imagen'}), 400

        # Entrenar el modelo con las nuevas imágenes
        reconocedor.entrenar_modelo()

        return jsonify({
            'mensaje': 'Estudiante registrado exitosamente',
            'rutas_imagenes': rutas_imagenes
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 