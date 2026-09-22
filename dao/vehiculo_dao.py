import sqlite3
from typing import List, Optional
from dao.conexion import Conexion
from model.vehiculo import Vehiculo


class VehiculoDAO:
    """
    Data Access Object (DAO) para la entidad Vehiculo.
    Encapsula todas las operaciones de base de datos (CRUD) sobre la tabla 'vehiculo'.
    """

    def __init__(self, conexion: Optional[Conexion] = None) -> None:
        self.conexion = conexion or Conexion()
        self.crear_tabla()

    def crear_tabla(self) -> None:
        """Crea la tabla 'vehiculo' si no existe."""
        query = """
        CREATE TABLE IF NOT EXISTS vehiculo (
            patente TEXT PRIMARY KEY,
            anio INTEGER,
            en_taller INTEGER
        )
        """
        with self.conexion as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

    def insertar(self, vehiculo: Vehiculo) -> bool:
        """
        Inserta un nuevo vehículo en la base de datos.
        Retorna True si la inserción fue exitosa, False si la patente ya existe o hubo error.
        """
        query = """
        INSERT INTO vehiculo (patente, anio, en_taller)
        VALUES (?, ?, ?)
        """
        try:
            with self.conexion as conn:
                cursor = conn.cursor()
                cursor.execute(query, (
                    vehiculo.patente,
                    vehiculo.anio,
                    1 if vehiculo.en_taller else 0
                ))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
        except sqlite3.Error as e:
            print(f"Error al insertar vehículo: {e}")
            return False

    def obtener_por_patente(self, patente: str) -> Optional[Vehiculo]:
        """
        Busca un vehículo por su patente.
        Retorna la instancia de Vehiculo si existe, o None si no se encuentra.
        """
        query = "SELECT patente, anio, en_taller FROM vehiculo WHERE patente = ?"
        with self.conexion as conn:
            cursor = conn.cursor()
            cursor.execute(query, (patente,))
            fila = cursor.fetchone()
            if fila:
                vehiculo = Vehiculo(patente=fila["patente"], anio=fila["anio"])
                if fila["en_taller"]:
                    vehiculo.ingresar()
                return vehiculo
            return None

    def listar_todos(self) -> List[Vehiculo]:
        """
        Obtiene todos los vehículos registrados en la base de datos.
        Retorna una lista de instancias de Vehiculo.
        """
        query = "SELECT patente, anio, en_taller FROM vehiculo ORDER BY patente ASC"
        vehiculos: List[Vehiculo] = []
        with self.conexion as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            filas = cursor.fetchall()
            for fila in filas:
                vehiculo = Vehiculo(patente=fila["patente"], anio=fila["anio"])
                if fila["en_taller"]:
                    vehiculo.ingresar()
                vehiculos.append(vehiculo)
        return vehiculos

    def actualizar_estado(self, patente: str, en_taller: bool) -> bool:
        """
        Actualiza el estado 'en_taller' de un vehículo según su patente.
        Retorna True si se modificó algún registro, False en caso contrario.
        """
        query = "UPDATE vehiculo SET en_taller = ? WHERE patente = ?"
        with self.conexion as conn:
            cursor = conn.cursor()
            cursor.execute(query, (1 if en_taller else 0, patente))
            conn.commit()
            return cursor.rowcount > 0

    def eliminar(self, patente: str) -> bool:
        """
        Elimina un vehículo de la base de datos por su patente.
        Retorna True si se eliminó el registro, False en caso contrario.
        """
        query = "DELETE FROM vehiculo WHERE patente = ?"
        with self.conexion as conn:
            cursor = conn.cursor()
            cursor.execute(query, (patente,))
            conn.commit()
            return cursor.rowcount > 0
