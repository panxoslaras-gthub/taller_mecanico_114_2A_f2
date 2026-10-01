import sqlite3
from dao.dao import DAO
from model.vehiculo import Vehiculo
from model.auto import Auto
from model.camion import Camion
from model.moto import Moto
from model.modelo import Modelo
from model.marca import Marca

class VehiculoDAO(DAO):
    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehiculo (
                patente TEXT PRIMARY KEY,
                anio INTEGER NOT NULL,
                en_taller INTEGER NOT NULL DEFAULT 0,
                modelo_id INTEGER NOT NULL,
                FOREIGN KEY (modelo_id) REFERENCES modelo(id)
            )
        """)
        self.conexion.commit()

    def _mapear_vehiculo(self, fila) -> Vehiculo:
        # fila: (patente, anio, en_taller, modelo_id, modelo_nom, marca_id, marca_nom, maletero, carga, es_moto)
        marca = Marca(fila[6]) if fila[6] else None
        if marca:
            marca.id = fila[5]
        modelo = Modelo(fila[4], marca, id=fila[3])
        en_taller = bool(fila[2])

        if fila[7] is not None:
            return Auto(fila[0], fila[1], modelo, capacidad_maletero=fila[7], en_taller=en_taller)
        elif fila[8] is not None:
            return Camion(fila[0], fila[1], modelo, capacidad_carga=fila[8], en_taller=en_taller)
        elif fila[9] is not None:
            return Moto(fila[0], fila[1], modelo, en_taller=en_taller)
        else:
            return Vehiculo(fila[0], fila[1], modelo, en_taller=en_taller)

    def insertar(self, vehiculo: Vehiculo) -> Vehiculo:
        if not vehiculo.modelo or vehiculo.modelo.id is None:
            raise ValueError("El vehículo debe tener un modelo con ID válido.")
        self.cursor.execute(
            "INSERT INTO vehiculo (patente, anio, en_taller, modelo_id) VALUES (?, ?, ?, ?)",
            (vehiculo.patente, vehiculo.anio, 1 if vehiculo.en_taller else 0, vehiculo.modelo.id)
        )
        self.conexion.commit()
        return vehiculo

    def buscar(self, patente: str) -> Vehiculo | None:
        self.cursor.execute("""
            SELECT v.patente, v.anio, v.en_taller, v.modelo_id,
                   m.nombre AS modelo_nom, ma.id AS marca_id, ma.nombre AS marca_nom,
                   a.capacidad_maletero, c.capacidad_carga, mo.patente AS es_moto
            FROM vehiculo v
            LEFT JOIN modelo m ON v.modelo_id = m.id
            LEFT JOIN marca ma ON m.marca_id = ma.id
            LEFT JOIN auto a ON v.patente = a.patente
            LEFT JOIN camion c ON v.patente = c.patente
            LEFT JOIN moto mo ON v.patente = mo.patente
            WHERE v.patente = ?
        """, (patente,))
        fila = self.cursor.fetchone()
        if fila is None:
            return None
        return self._mapear_vehiculo(fila)

    def listar(self) -> list[Vehiculo]:
        self.cursor.execute("""
            SELECT v.patente, v.anio, v.en_taller, v.modelo_id,
                   m.nombre AS modelo_nom, ma.id AS marca_id, ma.nombre AS marca_nom,
                   a.capacidad_maletero, c.capacidad_carga, mo.patente AS es_moto
            FROM vehiculo v
            LEFT JOIN modelo m ON v.modelo_id = m.id
            LEFT JOIN marca ma ON m.marca_id = ma.id
            LEFT JOIN auto a ON v.patente = a.patente
            LEFT JOIN camion c ON v.patente = c.patente
            LEFT JOIN moto mo ON v.patente = mo.patente
            ORDER BY v.patente
        """)
        return [self._mapear_vehiculo(fila) for fila in self.cursor.fetchall()]

    def listar_en_taller(self) -> list[Vehiculo]:
        self.cursor.execute("""
            SELECT v.patente, v.anio, v.en_taller, v.modelo_id,
                   m.nombre AS modelo_nom, ma.id AS marca_id, ma.nombre AS marca_nom,
                   a.capacidad_maletero, c.capacidad_carga, mo.patente AS es_moto
            FROM vehiculo v
            LEFT JOIN modelo m ON v.modelo_id = m.id
            LEFT JOIN marca ma ON m.marca_id = ma.id
            LEFT JOIN auto a ON v.patente = a.patente
            LEFT JOIN camion c ON v.patente = c.patente
            LEFT JOIN moto mo ON v.patente = mo.patente
            WHERE v.en_taller = 1
            ORDER BY v.patente
        """)
        return [self._mapear_vehiculo(fila) for fila in self.cursor.fetchall()]

    def actualizar(self, vehiculo: Vehiculo) -> Vehiculo | None:
        if not vehiculo.modelo or vehiculo.modelo.id is None:
            raise ValueError("El vehículo debe tener un modelo con ID válido.")
        self.cursor.execute("""
            UPDATE vehiculo
            SET anio = ?, en_taller = ?, modelo_id = ?
            WHERE patente = ?
        """, (vehiculo.anio, 1 if vehiculo.en_taller else 0, vehiculo.modelo.id, vehiculo.patente))
        self.conexion.commit()
        if self.cursor.rowcount == 0:
            return None
        return self.buscar(vehiculo.patente)

    def actualizar_estado(self, patente: str, en_taller: bool) -> bool:
        self.cursor.execute(
            "UPDATE vehiculo SET en_taller = ? WHERE patente = ?",
            (1 if en_taller else 0, patente)
        )
        self.conexion.commit()
        return self.cursor.rowcount > 0

    def eliminar(self, patente: str) -> bool:
        try:
            self.cursor.execute("DELETE FROM auto WHERE patente = ?", (patente,))
            self.cursor.execute("DELETE FROM camion WHERE patente = ?", (patente,))
            self.cursor.execute("DELETE FROM moto WHERE patente = ?", (patente,))
            self.cursor.execute("DELETE FROM vehiculo WHERE patente = ?", (patente,))
            self.conexion.commit()
            return self.cursor.rowcount > 0
        except sqlite3.IntegrityError:
            self.conexion.rollback()
            return False