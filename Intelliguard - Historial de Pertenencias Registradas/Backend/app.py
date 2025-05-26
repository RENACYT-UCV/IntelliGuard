from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.pertenencias_route import pertenencias_bp


from models.pertenencia import BaseDatosPertenencia



app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'clave_12323'
jwt = JWTManager(app)

base_datos_pertenencia = BaseDatosPertenencia("basededatos.db")

@app.route('/')
def index():
    return 'Hola mundo'

app.register_blueprint(pertenencias_bp)


if __name__ == '__main__':
    app.run(debug=True)

