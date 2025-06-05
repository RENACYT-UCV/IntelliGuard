import requests
import json

def test_admin_login():
    url = "http://localhost:5000/api/auth/login/administrador"
    headers = {'Content-Type': 'application/json'}
    data = {
        'usuario': 'admin',
        'contraseña': '123456'
    }
    
    response = requests.post(url, headers=headers, json=data)
    print("Admin Login Response:", response.status_code)
    print(json.dumps(response.json(), indent=2))

def test_personal_login():
    url = "http://localhost:5000/api/auth/login/personal"
    headers = {'Content-Type': 'application/json'}
    data = {
        'usuario': 'personal',
        'contraseña': '654321'
    }
    
    response = requests.post(url, headers=headers, json=data)
    print("\nPersonal Login Response:", response.status_code)
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    print("Probando login de administrador...")
    test_admin_login()
    
    print("\nProbando login de personal...")
    test_personal_login() 