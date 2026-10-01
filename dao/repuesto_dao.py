import sqlite3
from dao.dao import DAO
from model.repuesto import Repuesto

class RepuestoDAO(DAO):
    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS repuesto (
                codigo TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0,
                es_importado INTEGER NOT NULL DEFAULT 0
            )
        """)
        self.conexion.commit()

    def insertar(self, repuesto: Repuesto) -> Repuesto:
        self.cursor.execute(
            "INSERT INTO repuesto (codigo, nombre, stock, es_importado) VALUES (?, ?, ?, ?)",
            (repuesto.codigo, repuesto.nombre, repuesto.stock, 1 if repuesto.es_importado else 0)
        )
        self.conexion.commit()
        return repuesto

    def buscar(self, codigo: str) -> Repuesto | None:
        self.cursor.execute(
            "SELECT codigo, nombre, stock, es_importado FROM repuesto WHERE codigo = ?",
            (codigo,)
        )
        fila = self.cursor.fetchone()
        if fila is None:
            return None
        return Repuesto(fila[0], fila[1], fila[2], bool(fila[3]))

    def listar(self) -> list[Repuesto]:
        self.cursor.execute("SELECT codigo, nombre, stock, es_importado FROM repuesto ORDER BY nombre")
        repuestos = []
        for fila in self.cursor.fetchall():
            repuestos.append(Repuesto(fila[0], fila[1], fila[2], bool(fila[3])))
        return repuestos

    def actualizar(self, repuesto: Repuesto) -> Repuesto | None:
        self.cursor.execute("""
            UPDATE repuesto
            SET nombre = ?, stock = ?, es_importado = ?
            WHERE codigo = ?
        """, (repuesto.nombre, repuesto.stock, 1 if repuesto.es_importado else 0, repuesto.codigo))
        self.conexion.commit()
        if self.cursor.rowcount == 0:
            return None
        return self.buscar(repuesto.codigo)

    def actualizar_stock(self, codigo: str, cantidad: int) -> bool:
        self.cursor.execute(
            "UPDATE repuesto SET stock = stock + ? WHERE codigo = ?",
            (cantidad, codigo)
        )
        self.conexion.commit()
        return self.cursor.rowcount > 0

    def eliminar(self, codigo: str) -> bool:
        try:
            self.cursor.execute("DELETE FROM repuesto WHERE codigo = ?", (codigo,))
            self.conexion.commit()
            return self.cursor.rowcount > 0
        except sqlite3.IntegrityError:
            self.conexion.rollback()
            return False
