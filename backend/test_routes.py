import requests
import json

BASE_URL = 'http://localhost:5000'

def print_response(response):
    print(f"Status Code: {response.status_code}")
    print("Response:", json.dumps(response.json(), indent=2))
    print("-" * 50)

def test_routes():
    # 1. Intentar login como administrador
    print("\n1. Probando login administrador...")
    admin_login = requests.post(f"{BASE_URL}/login/administrador", json={
        "usuario": "admin",
        "contraseña": "123456"
    })
    print_response(admin_login)
    
    if admin_login.status_code == 200:
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
        print("\n4. Registrando nuevo usuario...")
        register = requests.post(f"{BASE_URL}/registro", 
            headers=headers,
            json={
                "usuario": "test_user",
                "contraseña": "test123",
                "idRol": 2  # Rol de personal
            }
        )
        print_response(register)
    
    # 5. Intentar login como personal
    print("\n5. Probando login personal...")
    personal_login = requests.post(f"{BASE_URL}/login/personal", json={
        "usuario": "test_user",
        "contraseña": "test123"
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

if __name__ == "__main__":
    try:
        test_routes()
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar al servidor. Asegúrate de que el servidor esté corriendo en http://localhost:5000") 