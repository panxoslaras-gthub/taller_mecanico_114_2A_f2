import sqlite3
from typing import List, Optional
from dao.conexion import Conexion
from model.marca import Marca


class MarcaDAO:
    """
    Data Access Object (DAO) para la entidad Marca.
    Encapsula todas las operaciones de base de datos (CRUD) sobre la tabla 'marca'.
    """

    def __init__(self, conexion: Optional[Conexion] = None) -> None:
        self.conexion = conexion or Conexion()
        self.crear_tabla()

    def crear_tabla(self) -> None:
        """Crea la tabla 'marca' si no existe."""
        query = """
        CREATE TABLE IF NOT EXISTS marca (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL
        )
        """
        with self.conexion as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

    def insertar(self, marca: Marca) -> bool:
        """
        Inserta una nueva marca en la base de datos.
        Retorna True si la inserción fue exitosa, False si la marca ya existe o hubo error.
        """
        query = "INSERT INTO marca (nombre) VALUES (?)"
        try:
            with self.conexion as conn:
                cursor = conn.cursor()
                cursor.execute(query, (marca.nombre,))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
        except sqlite3.Error as e:
            print(f"Error al insertar marca: {e}")
            return False

    def obtener_por_nombre(self, nombre: str) -> Optional[Marca]:
        """
        Busca una marca por su nombre.
        Retorna la instancia de Marca si existe, o None si no se encuentra.
        """
        query = "SELECT nombre FROM marca WHERE LOWER(nombre) = LOWER(?)"
        with self.conexion as conn:
            cursor = conn.cursor()
            cursor.execute(query, (nombre,))
            fila = cursor.fetchone()
            if fila:
                return Marca(nombre=fila["nombre"])
            return None

    def obtener_por_id(self, id_marca: int) -> Optional[Marca]:
        """
        Busca una marca por su identificador numérico (ID).
        Retorna la instancia de Marca si existe, o None si no se encuentra.
        """
        query = "SELECT nombre FROM marca WHERE id = ?"
        with self.conexion as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id_marca,))
            fila = cursor.fetchone()
            if fila:
                return Marca(nombre=fila["nombre"])
            return None

    def listar_todas(self) -> List[Marca]:
        """
        Obtiene todas las marcas registradas en la base de datos ordenadas alfabéticamente.
        Retorna una lista de instancias de Marca.
        """
        query = "SELECT nombre FROM marca ORDER BY nombre ASC"
        marcas: List[Marca] = []
        with self.conexion as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            filas = cursor.fetchall()
            for fila in filas:
                marcas.append(Marca(nombre=fila["nombre"]))
        return marcas

    def actualizar(self, nombre_actual: str, nuevo_nombre: str) -> bool:
        """
        Actualiza el nombre de una marca existente.
        Retorna True si se modificó el registro, False en caso contrario.
        """
        query = "UPDATE marca SET nombre = ? WHERE LOWER(nombre) = LOWER(?)"
        try:
            with self.conexion as conn:
                cursor = conn.cursor()
                cursor.execute(query, (nuevo_nombre, nombre_actual))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False
        except sqlite3.Error as e:
            print(f"Error al actualizar marca: {e}")
            return False

    def eliminar(self, nombre: str) -> bool:
        """
        Elimina una marca de la base de datos por su nombre.
        Retorna True si se eliminó el registro, False en caso contrario.
        """
        query = "DELETE FROM marca WHERE LOWER(nombre) = LOWER(?)"
        with self.conexion as conn:
            cursor = conn.cursor()
            cursor.execute(query, (nombre,))
            conn.commit()
            return cursor.rowcount > 0
