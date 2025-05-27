from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .config import Config
from .utils.db_init import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    jwt = JWTManager(app)
    
    # Inicializar la base de datos
    init_db()
    
    # Registrar blueprints
    from .routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    
    @app.route('/')
    def index():
        return 'Hola mundo'
    
    return app
