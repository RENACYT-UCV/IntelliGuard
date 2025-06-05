import requests
import json

BASE_URL = 'http://localhost:5000'

def print_response(response):
    print(f"Status Code: {response.status_code}")
    print("Response:", json.dumps(response.json(), indent=2))
    print("-" * 50)

def test_routes():
    # Datos de prueba
    admin_credentials = {
        "usuario": "admin",
        "contraseña": "123456"  # Esta es la contraseña en texto plano que configuramos en init_db.py
    }
    
    # 1. Intentar login como administrador
    print("\n1. Probando login administrador...")
    print(f"Intentando login con usuario: {admin_credentials['usuario']}")
    admin_login = requests.post(f"{BASE_URL}/login/administrador", json=admin_credentials)
    print_response(admin_login)
    
    if admin_login.status_code == 200:
        print("¡Login de administrador exitoso!")
        admin_token = admin_login.json()['access_token']
        headers = {'Authorization': f'Bearer {admin_token}'}
        
        # 2. Verificar token de administrador
        print("\n2. Verificando token de administrador...")
        verify = requests.get(f"{BASE_URL}/verify-token", headers=headers)
        print_response(verify)
        
        # 3. Listar usuarios
        print("\n3. Listando usuarios...")
        users = requests.get(f"{BASE_URL}/usuarios", headers=headers)
        print_response(users)
        
        # 4. Intentar registrar nuevo usuario
        new_user = {
            "usuario": "test_user",
            "contraseña": "test123",
            "idRol": 1  # Rol de personal
        }
        print("\n4. Registrando nuevo usuario...")
        register = requests.post(f"{BASE_URL}/registro", headers=headers, json=new_user)
        print_response(register)
        
        # 5. Intentar login como personal
        print("\n5. Probando login personal...")
        personal_login = requests.post(f"{BASE_URL}/login/personal", json={
            "usuario": new_user["usuario"],
            "contraseña": new_user["contraseña"]
        })
        print_response(personal_login)
        
        if personal_login.status_code == 200:
            personal_token = personal_login.json()['access_token']
            headers = {'Authorization': f'Bearer {personal_token}'}
            
            # 6. Verificar token de personal
            print("\n6. Verificando token de personal...")
            verify = requests.get(f"{BASE_URL}/verify-token", headers=headers)
            print_response(verify)
            
            # 7. Intentar acceder a ruta protegida de admin (debería fallar)
            print("\n7. Intentando acceder a ruta protegida (debería fallar)...")
            users = requests.get(f"{BASE_URL}/usuarios", headers=headers)
            print_response(users)
    else:
        print("Error: No se pudo iniciar sesión como administrador")

if __name__ == "__main__":
    try:
        test_routes()
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar al servidor. Asegúrate de que el servidor esté corriendo en http://localhost:5000")
    except Exception as e:
        print(f"Error inesperado: {str(e)}") 