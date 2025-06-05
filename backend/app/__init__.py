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
    from .routes.pertenencias_route import pertenencias_bp
    from .routes.reconocimiento_routes import reconocimiento_bp
    from .routes.estudiante_routes import estudiante_bp
    from .routes.reportes_route import reportes_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(pertenencias_bp, url_prefix='/api/pertenencias')
    app.register_blueprint(reconocimiento_bp)
    app.register_blueprint(estudiante_bp)
    app.register_blueprint(reportes_bp, url_prefix='/api/reportes')
    
    @app.route('/')
    def index():
        return 'API de IntelliGuard funcionando'
    
    return app
