from flask import Flask
from flask_cors import CORS
from core.api.reportes import reportes_bp

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# Registrar blueprints
app.register_blueprint(reportes_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 