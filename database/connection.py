from pathlib import Path
import sqlite3
import sys


def get_base_dir():
    """
    En desarrollo usa la carpeta raíz del proyecto.
    En ejecutable usa la carpeta donde está el .exe.
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent.parent


BASE_DIR = get_base_dir()
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "control_equipos.db"


def get_connection():
    DATA_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")

    return connection