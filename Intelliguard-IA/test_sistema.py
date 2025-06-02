import os
import cv2
from pathlib import Path
import sys

# Agregar el directorio raíz al path
ROOT_DIR = Path(__file__).parent
sys.path.append(str(ROOT_DIR))

from core.reconocimiento.facial import ReconocimientoFacial
from core.objetos.deteccion import DeteccionObjetos
from core.pertenencias.gestion import GestionPertenencias

def test_reconocimiento_facial():
    """Prueba el módulo de reconocimiento facial"""
    print("\n=== Prueba de Reconocimiento Facial ===")
    
    # Inicializar reconocedor
    reconocedor = ReconocimientoFacial()
    
    # Menú de opciones
    while True:
        print("\n1. Capturar nuevo rostro")
        print("2. Reconocer rostro")
        print("3. Volver")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            codigo = input("Ingrese código de estudiante: ")
            reconocedor.capturar_rostro(codigo)
            
        elif opcion == "2":
            print("\nIniciando reconocimiento facial con cámara web...")
            print("Presione 'q' para salir")
            
            # Iniciar cámara web
            cap = cv2.VideoCapture(0)
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error al acceder a la cámara web")
                    break
                
                # Realizar reconocimiento facial
                codigo, porcentaje = reconocedor.reconocimiento_facial(frame)
                
                # Mostrar resultados en tiempo real
                if codigo:
                    cv2.putText(frame, f"Estudiante: {codigo}", (10, 30),
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, f"Similitud: {porcentaje:.2f}%", (10, 70),
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, "No reconocido", (10, 30),
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                # Mostrar frame
                cv2.imshow('Reconocimiento Facial', frame)
                
                # Salir con 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            # Liberar recursos
            cap.release()
            cv2.destroyAllWindows()
                
        elif opcion == "3":
            break
            
        else:
            print("\nOpción inválida")

def test_deteccion_objetos():
    """Prueba el módulo de detección de objetos"""
    print("\n=== Prueba de Detección de Objetos ===")
    
    # Inicializar detector
    detector = DeteccionObjetos()
    
    # Menú de opciones
    while True:
        print("\n1. Detectar objeto en imagen")
        print("2. Entrenar modelo")
        print("3. Volver")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            ruta = input("Ingrese ruta de la imagen: ")
            if os.path.exists(ruta):
                etiqueta, objeto = detector.procesar_imagen(ruta)
                
                if etiqueta:
                    print(f"\nObjeto detectado:")
                    print(f"Tipo: {etiqueta}")
                    
                    # Guardar imagen recortada
                    if objeto is not None:
                        ruta_guardar = os.path.join(
                            os.path.dirname(ruta),
                            f"objeto_{etiqueta}.jpg"
                        )
                        cv2.imwrite(ruta_guardar, objeto)
                        print(f"Imagen guardada en: {ruta_guardar}")
                else:
                    print("\nNo se detectó ningún objeto")
            else:
                print("\nLa imagen no existe")
                
        elif opcion == "2":
            detector.entrenar_modelo()
            
        elif opcion == "3":
            break
            
        else:
            print("\nOpción inválida")

def test_gestion_pertenencias():
    """Prueba el módulo de gestión de pertenencias"""
    print("\n=== Prueba de Gestión de Pertenencias ===")
    
    # Inicializar gestor
    gestor = GestionPertenencias()
    
    # Menú de opciones
    while True:
        print("\n1. Registrar entrada")
        print("2. Registrar salida")
        print("3. Consultar pertenencias")
        print("4. Volver")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            codigo = input("Código de estudiante: ")
            tipo = input("Tipo de objeto: ")
            descripcion = input("Descripción: ")
            
            # Capturar imagen
            ruta = input("Ruta de imagen (opcional): ")
            imagen = None
            if ruta and os.path.exists(ruta):
                imagen = cv2.imread(ruta)
                
            if gestor.registrar_entrada(codigo, tipo, descripcion, imagen):
                print("\nEntrada registrada exitosamente")
            else:
                print("\nError al registrar entrada")
                
        elif opcion == "2":
            codigo = input("Código de estudiante: ")
            tipo = input("Tipo de objeto: ")
            
            if gestor.registrar_salida(codigo, tipo):
                print("\nSalida registrada exitosamente")
            else:
                print("\nError al registrar salida")
                
        elif opcion == "3":
            codigo = input("Código de estudiante (opcional): ")
            estado = input("Estado (ENTREGADO/RETIRADO, opcional): ")
            
            pertenencias = gestor.obtener_pertenencias(
                codigo if codigo else None,
                estado if estado else None
            )
            
            if pertenencias:
                print("\nPertenencias encontradas:")
                for p in pertenencias:
                    print(f"\nID: {p[0]}")
                    print(f"Estudiante: {p[1]}")
                    print(f"Tipo: {p[2]}")
                    print(f"Descripción: {p[3]}")
                    print(f"Estado: {p[6]}")
                    print(f"Fecha entrada: {p[4]}")
                    if p[5]:  # Fecha salida
                        print(f"Fecha salida: {p[5]}")
            else:
                print("\nNo se encontraron pertenencias")
                
        elif opcion == "4":
            break
            
        else:
            print("\nOpción inválida")

def main():
    """Función principal"""
    while True:
        print("\n=== Sistema Intelliguard-IA ===")
        print("\n1. Reconocimiento Facial")
        print("2. Detección de Objetos")
        print("3. Gestión de Pertenencias")
        print("4. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            test_reconocimiento_facial()
        elif opcion == "2":
            test_deteccion_objetos()
        elif opcion == "3":
            test_gestion_pertenencias()
        elif opcion == "4":
            print("\n¡Hasta pronto!")
            break
        else:
            print("\nOpción inválida")

if __name__ == "__main__":
    main() 