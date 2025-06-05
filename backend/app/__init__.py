from flask import Flask
from flask_cors import CORS
from .config.config import config
from .utils.db_init import init_db

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.JWT_ACCESS_TOKEN_EXPIRES
    
    # Configurar CORS
    CORS(app, resources={r"/*": {"origins": config.CORS_ORIGINS}})
    
    # Registrar rutas
    from .routes.auth_routes import auth_bp
    from .routes.estudiante_routes import estudiante_bp
    from .routes.pertenencias_route import pertenencias_bp
    from .routes.reportes_route import reportes_bp
    from .routes.reconocimiento_routes import reconocimiento_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(estudiante_bp)
    app.register_blueprint(pertenencias_bp)
    app.register_blueprint(reportes_bp)
    app.register_blueprint(reconocimiento_bp)
    
    # Inicializar la base de datos
    init_db()
    
    @app.route('/')
    def index():
        return 'API de IntelliGuard funcionando'
    
    return app
