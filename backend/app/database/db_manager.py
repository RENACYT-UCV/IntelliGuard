import sqlite3
from typing import List, Tuple, Optional, Any
from ..config.config import config
import logging
from flask import request, abort, g
import time
from functools import wraps
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class DatabaseManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._init_connection()
        return cls._instance
    
    def _init_connection(self):
        """Inicializa la conexión a la base de datos"""
        self.connection = sqlite3.connect(
            config.DATABASE_PATH,
            timeout=config.SQLITE_TIMEOUT,
            check_same_thread=config.SQLITE_CHECK_SAME_THREAD
        )
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        logger.info("Conexión a la base de datos establecida")

    def execute_query(self, query: str, params: Tuple = ()) -> sqlite3.Cursor:
        """Ejecuta una consulta SQL"""
        try:
            return self.cursor.execute(query, params)
        except sqlite3.Error as e:
            logger.error(f"Error ejecutando consulta: {str(e)}")
            self.connection.rollback()
            raise Exception(f"Error ejecutando consulta: {str(e)}")

    def fetch_one(self, query: str, params: Tuple = ()) -> Optional[sqlite3.Row]:
        """Ejecuta una consulta y retorna una fila"""
        try:
            return self.execute_query(query, params).fetchone()
        except sqlite3.Error as e:
            logger.error(f"Error obteniendo resultado: {str(e)}")
            raise Exception(f"Error obteniendo resultado: {str(e)}")

    def fetch_all(self, query: str, params: Tuple = ()) -> List[sqlite3.Row]:
        """Ejecuta una consulta y retorna todas las filas"""
        try:
            return self.execute_query(query, params).fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error obteniendo resultados: {str(e)}")
            raise Exception(f"Error obteniendo resultados: {str(e)}")

    def commit(self):
        """Confirma los cambios en la base de datos"""
        try:
            self.connection.commit()
        except sqlite3.Error as e:
            logger.error(f"Error confirmando cambios: {str(e)}")
            self.connection.rollback()
            raise Exception(f"Error confirmando cambios: {str(e)}")

    def rollback(self):
        """Revierte los cambios en la base de datos"""
        try:
            self.connection.rollback()
        except sqlite3.Error as e:
            logger.error(f"Error revirtiendo cambios: {str(e)}")
            raise Exception(f"Error revirtiendo cambios: {str(e)}")

    def close(self):
        """Cierra la conexión a la base de datos"""
        try:
            self.connection.close()
        except sqlite3.Error as e:
            logger.error(f"Error cerrando conexión: {str(e)}")
            raise Exception(f"Error cerrando conexión: {str(e)}")

    def execute_many(self, query, params_list):
        """Ejecuta una query múltiples veces con diferentes parámetros"""
        cursor = self.cursor
        try:
            cursor.executemany(query, params_list)
            return cursor
        except Exception as e:
            logger.error(f"Error ejecutando query multiple: {query} - Error: {e}")
            self.rollback()
            raise

# Instancia global del administrador de base de datos
db = DatabaseManager()

def rate_limit(max_requests: int, window: int):
    def decorator(f):
        requests = {}
        
        @wraps(f)
        def wrapped(*args, **kwargs):
            now = time.time()
            ip = request.remote_addr
            
            # Limpiar solicitudes antiguas
            requests[ip] = [req_time for req_time in requests.get(ip, [])
                          if now - req_time < window]
            
            # Verificar límite
            if len(requests.get(ip, [])) >= max_requests:
                abort(429, 'Demasiadas solicitudes')
                
            # Registrar solicitud
            requests.setdefault(ip, []).append(now)
            return f(*args, **kwargs)
            
        return wrapped
    return decorator 

class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url if request else "No URL"
        record.remote_addr = request.remote_addr if request else "No IP"
        record.method = request.method if request else "No method"
        record.user_id = g.get('user_id', 'No user')
        
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'url': record.url,
            'ip': record.remote_addr,
            'method': record.method,
            'user_id': record.user_id
        }
        
        return json.dumps(log_data) 