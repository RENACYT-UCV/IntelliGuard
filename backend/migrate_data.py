import sqlite3
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_data():
    try:
        # Conectar a ambas bases de datos
        source_conn = sqlite3.connect('basededatos.db')
        target_conn = sqlite3.connect('data/database.db')
        
        source_cur = source_conn.cursor()
        target_cur = target_conn.cursor()
        
        # Migrar estudiantes
        logger.info("Migrando datos de estudiantes...")
        students = source_cur.execute("SELECT * FROM estudiantes").fetchall()
        for student in students:
            # Verificar si el estudiante ya existe
            existing = target_cur.execute("SELECT id FROM estudiantes WHERE codigo = ?", (student[1],)).fetchone()
            if not existing:
                target_cur.execute(
                    "INSERT INTO estudiantes (codigo, nombres, carrera, plan) VALUES (?, ?, ?, ?)",
                    (student[1], student[2], student[3], student[4])
                )
                logger.info(f"Estudiante migrado: {student[2]}")
            else:
                logger.info(f"Estudiante ya existe: {student[2]}")
        
        # Confirmar cambios
        target_conn.commit()
        logger.info("Migración completada exitosamente")
        
        # Verificar los datos migrados
        count = target_cur.execute("SELECT COUNT(*) FROM estudiantes").fetchone()[0]
        logger.info(f"Total de estudiantes en la nueva base de datos: {count}")
        
    except Exception as e:
        logger.error(f"Error durante la migración: {e}")
        if 'target_conn' in locals():
            target_conn.rollback()
        raise
    finally:
        if 'source_conn' in locals():
            source_conn.close()
        if 'target_conn' in locals():
            target_conn.close()

if __name__ == '__main__':
    migrate_data() 