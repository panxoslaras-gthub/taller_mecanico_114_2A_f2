import sqlite3
from dao.vehiculo_dao import VehiculoDAO
from model.camion import Camion
from model.modelo import Modelo
from model.marca import Marca

class CamionDAO(VehiculoDAO):
    def crear_tabla(self):
        super().crear_tabla()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS camion (
                patente TEXT PRIMARY KEY,
                capacidad_carga INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (patente) REFERENCES vehiculo(patente)
            )
        """)
        self.conexion.commit()

    def insertar(self, camion: Camion) -> Camion:
        super().insertar(camion)
        self.cursor.execute(
            "INSERT INTO camion (patente, capacidad_carga) VALUES (?, ?)",
            (camion.patente, camion.capacidad_carga)
        )
        self.conexion.commit()
        return camion

    def buscar(self, patente: str) -> Camion | None:
        self.cursor.execute("""
            SELECT v.patente, v.anio, v.en_taller, v.modelo_id,
                   m.nombre AS modelo_nom, ma.id AS marca_id, ma.nombre AS marca_nom,
                   c.capacidad_carga
            FROM vehiculo v
            JOIN camion c ON v.patente = c.patente
            LEFT JOIN modelo m ON v.modelo_id = m.id
            LEFT JOIN marca ma ON m.marca_id = ma.id
            WHERE v.patente = ?
        """, (patente,))
        fila = self.cursor.fetchone()
        if fila is None:
            return None
        marca = Marca(fila[6]) if fila[6] else None
        if marca:
            marca.id = fila[5]
        modelo = Modelo(fila[4], marca, id=fila[3])
        return Camion(fila[0], fila[1], modelo, capacidad_carga=fila[7], en_taller=bool(fila[2]))

    def listar(self) -> list[Camion]:
        self.cursor.execute("""
            SELECT v.patente, v.anio, v.en_taller, v.modelo_id,
                   m.nombre AS modelo_nom, ma.id AS marca_id, ma.nombre AS marca_nom,
                   c.capacidad_carga
            FROM vehiculo v
            JOIN camion c ON v.patente = c.patente
            LEFT JOIN modelo m ON v.modelo_id = m.id
            LEFT JOIN marca ma ON m.marca_id = ma.id
            ORDER BY v.patente
        """)
        camiones = []
        for fila in self.cursor.fetchall():
            marca = Marca(fila[6]) if fila[6] else None
            if marca:
                marca.id = fila[5]
            modelo = Modelo(fila[4], marca, id=fila[3])
            camiones.append(Camion(fila[0], fila[1], modelo, capacidad_carga=fila[7], en_taller=bool(fila[2])))
        return camiones

    def actualizar(self, camion: Camion) -> Camion | None:
        super().actualizar(camion)
        self.cursor.execute(
            "UPDATE camion SET capacidad_carga = ? WHERE patente = ?",
            (camion.capacidad_carga, camion.patente)
        )
        self.conexion.commit()
        return self.buscar(camion.patente)

    def eliminar(self, patente: str) -> bool:
        try:
            self.cursor.execute("DELETE FROM camion WHERE patente = ?", (patente,))
            self.cursor.execute("DELETE FROM vehiculo WHERE patente = ?", (patente,))
            self.conexion.commit()
            return self.cursor.rowcount > 0
        except sqlite3.IntegrityError:
            self.conexion.rollback()
            return False
