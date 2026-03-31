import sqlite3
from datetime import datetime, timedelta
import os

DB_PATH = os.getenv("DB_PATH", "./data/logs.db")
DAYS_RETENTION = int(os.getenv("DAYS_RETENTION", 3))

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabela():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                level     TEXT NOT NULL,
                message   TEXT NOT NULL,
                service   TEXT NOT NULL
            )
        """)

def inserir_log(log: dict):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO logs (timestamp, level, message, service)
            VALUES (:timestamp, :level, :message, :service)
        """, log)

def buscar_logs(data: str = None, limit: int = 50, offset: int = 0):
    with get_connection() as conn:
        if data:
            rows = conn.execute("""
                SELECT * FROM logs
                WHERE DATE(timestamp) = ?
                ORDER BY timestamp ASC
            """, (data,)).fetchall()
        else:
            rows = conn.execute("""
                SELECT * FROM logs
                ORDER BY timestamp ASC
                LIMIT ? OFFSET ?
            """, (limit, offset)).fetchall()
    return [dict(row) for row in rows]

def buscar_logs_after_id(after_id: int):
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT * FROM logs
            WHERE id > ?
            ORDER BY timestamp ASC
        """, (after_id,)).fetchall()
    return [dict(row) for row in rows]

def limpar_logs_antigos():
    limite = (datetime.now() - timedelta(days=DAYS_RETENTION)).strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        conn.execute("DELETE FROM logs WHERE timestamp < ?", (limite,))