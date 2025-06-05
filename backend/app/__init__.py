from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .config.config import config
from .database.db_init import init_db
from .utils.logger import logger

def create_app():
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración básica
    app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.JWT_ACCESS_TOKEN_EXPIRES
    app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
    
    # Configurar CORS
    CORS(app, resources={r"/*": {"origins": config.CORS_ORIGINS}})
    
    # Configurar JWT
    jwt = JWTManager(app)
    
    # Configurar rate limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=[config.RATELIMIT_DEFAULT],
        storage_uri=config.RATELIMIT_STORAGE_URL
    )
    
    # Registrar rutas
    from .routes.auth_routes import auth_bp
    from .routes.estudiante_routes import estudiante_bp
    from .routes.pertenencia_routes import pertenencia_bp
    from .routes.reporte_routes import reporte_bp
    from .routes.reconocimiento_routes import reconocimiento_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(estudiante_bp, url_prefix='/api/estudiantes')
    app.register_blueprint(pertenencia_bp, url_prefix='/api/pertenencias')
    app.register_blueprint(reporte_bp, url_prefix='/api/reportes')
    app.register_blueprint(reconocimiento_bp, url_prefix='/api/reconocimiento')
    
    # Inicializar la base de datos
    try:
        init_db()
        logger.info("Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
        raise
    
    @app.route('/')
    def index():
        return 'API de IntelliGuard funcionando'
    
    return app
