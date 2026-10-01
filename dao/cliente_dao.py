import sqlite3
from dao.dao import DAO
from model.cliente import Cliente
from model.persona import Persona

class ClienteDAO(DAO):
    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS persona (
                rut TEXT PRIMARY KEY,
                nombre TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cliente (
                rut TEXT PRIMARY KEY,
                tiene_deuda INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (rut) REFERENCES persona(rut)
            )
        """)
        self.conexion.commit()

    def insertar(self, cliente: Cliente) -> Cliente:
        if not cliente.persona or not cliente.persona.rut:
            raise ValueError("El cliente debe tener una persona con RUT válido.")
        # Insertar o actualizar persona
        self.cursor.execute("""
            INSERT INTO persona (rut, nombre) VALUES (?, ?)
            ON CONFLICT(rut) DO UPDATE SET nombre = excluded.nombre
        """, (cliente.persona.rut, cliente.persona.nombre))
        # Insertar cliente
        self.cursor.execute("""
            INSERT INTO cliente (rut, tiene_deuda) VALUES (?, ?)
        """, (cliente.persona.rut, 1 if cliente.tiene_deuda() else 0))
        self.conexion.commit()
        return cliente

    def buscar(self, rut: str) -> Cliente | None:
        self.cursor.execute("""
            SELECT p.rut, p.nombre, c.tiene_deuda
            FROM cliente c
            JOIN persona p ON c.rut = p.rut
            WHERE c.rut = ?
        """, (rut,))
        fila = self.cursor.fetchone()
        if fila is None:
            return None
        persona = Persona(fila[0], fila[1])
        return Cliente(persona, tiene_deuda=bool(fila[2]))

    def listar(self) -> list[Cliente]:
        self.cursor.execute("""
            SELECT p.rut, p.nombre, c.tiene_deuda
            FROM cliente c
            JOIN persona p ON c.rut = p.rut
            ORDER BY p.nombre
        """)
        clientes = []
        for fila in self.cursor.fetchall():
            persona = Persona(fila[0], fila[1])
            clientes.append(Cliente(persona, tiene_deuda=bool(fila[2])))
        return clientes

    def actualizar(self, cliente: Cliente) -> Cliente | None:
        if not cliente.persona or not cliente.persona.rut:
            raise ValueError("El cliente debe tener una persona con RUT válido.")
        self.cursor.execute("""
            UPDATE persona SET nombre = ? WHERE rut = ?
        """, (cliente.persona.nombre, cliente.persona.rut))
        self.cursor.execute("""
            UPDATE cliente SET tiene_deuda = ? WHERE rut = ?
        """, (1 if cliente.tiene_deuda() else 0, cliente.persona.rut))
        self.conexion.commit()
        if self.cursor.rowcount == 0:
            return None
        return self.buscar(cliente.persona.rut)

    def eliminar(self, rut: str) -> bool:
        try:
            self.cursor.execute("DELETE FROM cliente WHERE rut = ?", (rut,))
            self.cursor.execute("DELETE FROM persona WHERE rut = ?", (rut,))
            self.conexion.commit()
            return self.cursor.rowcount > 0
        except sqlite3.IntegrityError:
            self.conexion.rollback()
            return False
