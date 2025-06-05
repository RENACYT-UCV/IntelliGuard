from app import create_app
from app.utils.logger import logger

app = create_app()

if __name__ == '__main__':
    try:
        logger.info("Iniciando servidor Flask...")
        app.run(host='127.0.0.1', port=5000, debug=True)
    except Exception as e:
        logger.error(f"Error al iniciar el servidor: {e}") 