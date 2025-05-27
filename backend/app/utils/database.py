import sqlite3
from ..config import Config
import threading

class Database:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Database, cls).__new__(cls)
                    cls._instance.connection = None
        return cls._instance
    
    def get_connection(self):
        if self.connection is None:
            with self._lock:
                if self.connection is None:
                    self.connection = sqlite3.connect(Config.DATABASE_URL, check_same_thread=False)
        return self.connection 