import sqlite3
from dao.vehiculo_dao import VehiculoDAO
from model.moto import Moto
from model.modelo import Modelo
from model.marca import Marca

class MotoDAO(VehiculoDAO):
    def crear_tabla(self):
        super().crear_tabla()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS moto (
                patente TEXT PRIMARY KEY,
                FOREIGN KEY (patente) REFERENCES vehiculo(patente)
            )
        """)
        self.conexion.commit()

    def insertar(self, moto: Moto) -> Moto:
        super().insertar(moto)
        self.cursor.execute(
            "INSERT INTO moto (patente) VALUES (?)",
            (moto.patente,)
        )
        self.conexion.commit()
        return moto

    def buscar(self, patente: str) -> Moto | None:
        self.cursor.execute("""
            SELECT v.patente, v.anio, v.en_taller, v.modelo_id,
                   m.nombre AS modelo_nom, ma.id AS marca_id, ma.nombre AS marca_nom
            FROM vehiculo v
            JOIN moto mo ON v.patente = mo.patente
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
        return Moto(fila[0], fila[1], modelo, en_taller=bool(fila[2]))

    def listar(self) -> list[Moto]:
        self.cursor.execute("""
            SELECT v.patente, v.anio, v.en_taller, v.modelo_id,
                   m.nombre AS modelo_nom, ma.id AS marca_id, ma.nombre AS marca_nom
            FROM vehiculo v
            JOIN moto mo ON v.patente = mo.patente
            LEFT JOIN modelo m ON v.modelo_id = m.id
            LEFT JOIN marca ma ON m.marca_id = ma.id
            ORDER BY v.patente
        """)
        motos = []
        for fila in self.cursor.fetchall():
            marca = Marca(fila[6]) if fila[6] else None
            if marca:
                marca.id = fila[5]
            modelo = Modelo(fila[4], marca, id=fila[3])
            motos.append(Moto(fila[0], fila[1], modelo, en_taller=bool(fila[2])))
        return motos

    def actualizar(self, moto: Moto) -> Moto | None:
        super().actualizar(moto)
        return self.buscar(moto.patente)

    def eliminar(self, patente: str) -> bool:
        try:
            self.cursor.execute("DELETE FROM moto WHERE patente = ?", (patente,))
            self.cursor.execute("DELETE FROM vehiculo WHERE patente = ?", (patente,))
            self.conexion.commit()
            return self.cursor.rowcount > 0
        except sqlite3.IntegrityError:
            self.conexion.rollback()
            return False
