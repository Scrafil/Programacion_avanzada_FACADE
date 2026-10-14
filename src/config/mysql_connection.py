import os

import mysql.connector

_config = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DB", "notas_db"),
}


def get_connection(include_db=True):
    cfg = dict(_config)
    if not include_db:
        cfg.pop("database", None)
    return mysql.connector.connect(**cfg)


def init_db():
    # 1. Crear DB si no existe (conexión sin database)
    conn = get_connection(include_db=False)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {_config['database']}")
    conn.commit()
    cur.close()
    conn.close()
    # 2. Crear tabla
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS notes(
        id INT AUTO_INCREMENT PRIMARY KEY,
        estudiante VARCHAR(100) NOT NULL,
        materia VARCHAR(100) NOT NULL,
        nota FLOAT NOT NULL,
        fecha DATE NOT NULL)"""
    )
    conn.commit()
    cur.close()
    conn.close()
