import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "taller.db"

def crear_conexion():
    conexion = sqlite3.connect(DB_PATH)
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion



