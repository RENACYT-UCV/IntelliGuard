from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.estudiantes_routes import estudiantes_bp


from models.estudiante import BaseDatosEstudiantes



app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'clave_12323'
jwt = JWTManager(app)


base_datos_estudiantes = BaseDatosEstudiantes("basededatos.db")


@app.route('/')
def index():
    return 'Hola mundo'


app.register_blueprint(estudiantes_bp)



if __name__ == '__main__':
    app.run(debug=True)

