from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..utils.role_decorador import role_required
import cv2
import numpy as np
import base64
import sys
from pathlib import Path
import os

# Agregar el directorio de IA al path
IA_DIR = Path(__file__).parent.parent.parent.parent / 'Intelliguard-IA'
sys.path.append(str(IA_DIR))

from core.reconocimiento.facial import ReconocimientoFacial

reconocimiento_bp = Blueprint('reconocimiento', __name__)
reconocedor = ReconocimientoFacial()

@reconocimiento_bp.route('/reconocimiento/capturar/<codigo_estudiante>', methods=['POST'])
@jwt_required()
@role_required(['Personal', 'Administrador'])
def capturar_rostro(codigo_estudiante):
    """
    Captura rostros desde la cámara web
    """
    try:
        # Obtener el video del request
        if 'video' not in request.files:
            return jsonify({
                'error': 'No se proporcionó video',
                'status': 'error'
            }), 400
            
        video_file = request.files['video']
        if not video_file:
            return jsonify({
                'error': 'Archivo de video vacío',
                'status': 'error'
            }), 400

        # Guardar el video temporalmente
        video_path = f'temp_{codigo_estudiante}.webm'
        video_file.save(video_path)
        
        try:
            # Procesar el video y capturar el rostro
            reconocedor.capturar_rostro(codigo_estudiante, video_path)
            
            return jsonify({
                'mensaje': 'Rostro capturado exitosamente',
                'status': 'success'
            }), 200
        finally:
            # Limpiar el archivo temporal
            if os.path.exists(video_path):
                os.remove(video_path)
                
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@reconocimiento_bp.route('/reconocimiento/identificar', methods=['POST'])
@jwt_required()
@role_required('Personal')
def identificar_rostro():
    """
    Identifica un rostro en una imagen
    """
    try:
        # Obtener imagen en base64 del request
        data = request.get_json()
        imagen_b64 = data.get('imagen')
        
        if not imagen_b64:
            return jsonify({
                'error': 'No se proporcionó imagen',
                'status': 'error'
            }), 400
            
        # Decodificar imagen
        imagen_bytes = base64.b64decode(imagen_b64.split(',')[1])
        imagen_np = np.frombuffer(imagen_bytes, dtype=np.uint8)
        imagen = cv2.imdecode(imagen_np, cv2.IMREAD_COLOR)
        
        # Realizar reconocimiento
        codigo, porcentaje = reconocedor.reconocimiento_facial(imagen)
        
        if codigo:
            return jsonify({
                'codigo_estudiante': str(codigo),
                'porcentaje': porcentaje,
                'status': 'success'
            }), 200
        else:
            return jsonify({
                'mensaje': 'No se reconoció ningún rostro',
                'status': 'error'
            }), 404
            
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@reconocimiento_bp.route('/reconocimiento/entrenar', methods=['POST'])
@jwt_required()
@role_required('Administrador')
def entrenar_modelo():
    """
    Entrena el modelo de reconocimiento facial
    """
    try:
        reconocedor.entrenar_modelo()
        return jsonify({
            'mensaje': 'Modelo entrenado exitosamente',
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500 