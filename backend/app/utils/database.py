import sqlite3
from ..config import Config

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection = sqlite3.connect(Config.DATABASE_URL)
        return cls._instance
    
    def get_connection(self):
        return self.connection 