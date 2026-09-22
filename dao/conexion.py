import sqlite3
from typing import Optional


class Conexion:
    """
    Clase para gestionar la conexión a la base de datos SQLite.
    Permite abrir, cerrar y utilizar la conexión mediante context manager.
    """

    def __init__(self, db_path: str = "taller.db") -> None:
        self.db_path = db_path
        self._conexion: Optional[sqlite3.Connection] = None

    def conectar(self) -> sqlite3.Connection:
        """Abre y retorna una conexión a la base de datos."""
        if self._conexion is None:
            self._conexion = sqlite3.connect(self.db_path)
            # Habilitar retorno de filas por nombre y claves foráneas
            self._conexion.row_factory = sqlite3.Row
        return self._conexion

    def desconectar(self) -> None:
        """Cierra la conexión actual si está abierta."""
        if self._conexion is not None:
            self._conexion.close()
            self._conexion = None

    def __enter__(self) -> sqlite3.Connection:
        """Soporte para uso con bloque 'with'."""
        return self.conectar()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Cierra la conexión automáticamente al salir del bloque 'with'."""
        self.desconectar()
