import sqlite3
from dao.dao import DAO
from model.modelo import Modelo
from model.marca import Marca

class ModeloDAO(DAO):
    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS modelo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                marca_id INTEGER NOT NULL,
                FOREIGN KEY (marca_id) REFERENCES marca(id)
            )
        """)
        self.conexion.commit()

    def insertar(self, modelo: Modelo) -> Modelo:
        if not modelo.marca or modelo.marca.id is None:
            raise ValueError("El modelo debe estar asociado a una marca con ID válido.")
        self.cursor.execute(
            "INSERT INTO modelo (nombre, marca_id) VALUES (?, ?)",
            (modelo.nombre, modelo.marca.id)
        )
        modelo.id = self.cursor.lastrowid
        self.conexion.commit()
        return modelo

    def buscar(self, id: int) -> Modelo | None:
        self.cursor.execute("""
            SELECT m.id, m.nombre, m.marca_id, ma.nombre
            FROM modelo m
            LEFT JOIN marca ma ON m.marca_id = ma.id
            WHERE m.id = ?
        """, (id,))
        fila = self.cursor.fetchone()
        if fila is None:
            return None
        marca = Marca(fila[3])
        marca.id = fila[2]
        modelo = Modelo(fila[1], marca, id=fila[0])
        return modelo

    def listar(self) -> list[Modelo]:
        self.cursor.execute("""
            SELECT m.id, m.nombre, m.marca_id, ma.nombre
            FROM modelo m
            LEFT JOIN marca ma ON m.marca_id = ma.id
            ORDER BY m.id
        """)
        modelos = []
        for fila in self.cursor.fetchall():
            marca = Marca(fila[3]) if fila[3] else Marca("Desconocida")
            marca.id = fila[2]
            modelo = Modelo(fila[1], marca, id=fila[0])
            modelos.append(modelo)
        return modelos

    def listar_por_marca(self, marca_id: int) -> list[Modelo]:
        self.cursor.execute("""
            SELECT m.id, m.nombre, m.marca_id, ma.nombre
            FROM modelo m
            LEFT JOIN marca ma ON m.marca_id = ma.id
            WHERE m.marca_id = ?
            ORDER BY m.id
        """, (marca_id,))
        modelos = []
        for fila in self.cursor.fetchall():
            marca = Marca(fila[3]) if fila[3] else Marca("Desconocida")
            marca.id = fila[2]
            modelo = Modelo(fila[1], marca, id=fila[0])
            modelos.append(modelo)
        return modelos

    def actualizar(self, modelo: Modelo) -> Modelo | None:
        if not modelo.marca or modelo.marca.id is None:
            raise ValueError("El modelo debe estar asociado a una marca con ID válido.")
        self.cursor.execute(
            "UPDATE modelo SET nombre = ?, marca_id = ? WHERE id = ?",
            (modelo.nombre, modelo.marca.id, modelo.id)
        )
        self.conexion.commit()
        if self.cursor.rowcount == 0:
            return None
        return self.buscar(modelo.id)

    def eliminar(self, id: int) -> bool:
        try:
            self.cursor.execute("DELETE FROM modelo WHERE id = ?", (id,))
            self.conexion.commit()
            return self.cursor.rowcount > 0
        except sqlite3.IntegrityError:
            self.conexion.rollback()
            return False