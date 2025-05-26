import cv2
import os
import imutils
import time
import numpy as np
import tempfile

class ReconocimientoFacial:
    def __init__(self):
        pass
    
    def reconocimiento_facial(imagen_archivo):
        modelo_reconocimiento = cv2.face.FisherFaceRecognizer_create()
        modelo_reconocimiento.read(os.path.join('models', 'modeloEstudiantes.xml'))
        imagen_temporal = np.frombuffer(imagen_archivo.read(), np.uint8)
        imagen = cv2.imdecode(imagen_temporal, cv2.IMREAD_COLOR)
        imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        clasificador_rostros = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        rostros_detectados = clasificador_rostros.detectMultiScale(imagen_gris, scaleFactor=1.3, minNeighbors=5)
        if len(rostros_detectados) == 0:
            return -1, 0 
        for (x, y, ancho, alto) in rostros_detectados:
            rostro_recortado = imagen_gris[y:y+alto, x:x+ancho]
            rostro_recortado = cv2.resize(rostro_recortado, (150, 150), interpolation=cv2.INTER_CUBIC)
            id_resultado, valor_similitud = modelo_reconocimiento.predict(rostro_recortado)
            if valor_similitud < 500:
                porcentaje_similitud = 100 - int(valor_similitud / 5)
                return id_resultado, porcentaje_similitud
            else:
                return -1, 0 
        return -1, 0 


    def capturar_rostro(self,video_path, estudiante_path, codigoEstudiante):
        try:
            if not os.path.exists(estudiante_path):
                os.makedirs(estudiante_path)

            cap = cv2.VideoCapture(video_path)

            duracion_maxima = 10
            frames_por_segundo = cap.get(cv2.CAP_PROP_FPS)
            total_frames_a_capturar = int(frames_por_segundo * duracion_maxima)

            frames_capturados = 0

            rostro_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            while True:
                ret, frame = cap.read()
                # if not ret or frames_capturados >= total_frames_a_capturar:
                #     break
                if not ret :
                    break

                frame = imutils.resize(frame, width=640)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                auxFrame = frame.copy()
                rostros = rostro_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in rostros:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    recorte_rostro = auxFrame[y:y+h, x:x+w]
                    recorte_rostro_gris = cv2.cvtColor(recorte_rostro, cv2.COLOR_BGR2GRAY)
                    recorte_rostro_gris = cv2.resize(recorte_rostro_gris, (150, 150), interpolation=cv2.INTER_CUBIC)
                    img_rostro = f'{codigoEstudiante}_{int(time.time())}.jpg'
                    cv2.imwrite(os.path.join(estudiante_path, img_rostro), recorte_rostro_gris)
                # frames_capturados += 1

            cap.release()
            cv2.destroyAllWindows()
            print("Proceso de registro completado.")
        except Exception as e:
            print(f"Error durante el proceso de registro: {str(e)}")
        


    def entrenar_modelo(self):
        try:
            ruta_imagenes = os.path.join('uploads', 'estudiante')
            ruta_modelo = os.path.join('models', 'modeloEstudiantes.xml')
            lista_personas = os.listdir(ruta_imagenes)
            print('Personas encontradas: ', lista_personas)
            etiquetas = []
            datos_rostros = []
            for nombre_directorio in lista_personas:
                ruta_persona = os.path.join(ruta_imagenes, nombre_directorio)
                print(f'Leyendo imágenes de: {nombre_directorio}')
                id_persona = int(nombre_directorio)
                for nombre_archivo in os.listdir(ruta_persona):
                    print(f'Procesando imagen: {nombre_archivo}')
                    ruta_imagen = os.path.join(ruta_persona, nombre_archivo)
                    imagen = cv2.imread(ruta_imagen, 0)
                    if imagen is not None:
                        etiquetas.append(id_persona)
                        datos_rostros.append(imagen)
                    else:
                        print(f'No se pudo leer la imagen: {ruta_imagen}')
            modelo_reconocimiento = cv2.face.FisherFaceRecognizer_create()
            print('Entrenando el modelo...')
            modelo_reconocimiento.train(datos_rostros, np.array(etiquetas))
            modelo_reconocimiento.write(ruta_modelo)
            print(f'Modelo guardado en: {ruta_modelo}')
        except Exception as e:
            print(f'Error durante el entrenamiento del modelo: {str(e)}')

    

        
