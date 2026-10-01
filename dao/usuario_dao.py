import sqlite3
import json
from dao.dao import DAO
from model.usuario import Usuario
from model.rol import Rol
from model.persona import Persona

class UsuarioDAO(DAO):
    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS rol (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                permisos TEXT NOT NULL DEFAULT '[]'
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS persona (
                rut TEXT PRIMARY KEY,
                nombre TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                usuario TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                rol_id INTEGER NOT NULL,
                persona_rut TEXT NOT NULL,
                FOREIGN KEY (rol_id) REFERENCES rol(id),
                FOREIGN KEY (persona_rut) REFERENCES persona(rut)
            )
        """)
        self.conexion.commit()

    def insertar_rol(self, rol: Rol) -> Rol:
        permisos_json = json.dumps(rol.permisos)
        self.cursor.execute(
            "INSERT INTO rol (nombre, permisos) VALUES (?, ?)",
            (rol.nombre, permisos_json)
        )
        rol.id = self.cursor.lastrowid
        self.conexion.commit()
        return rol

    def buscar_rol(self, id: int) -> Rol | None:
        self.cursor.execute("SELECT id, nombre, permisos FROM rol WHERE id = ?", (id,))
        fila = self.cursor.fetchone()
        if fila is None:
            return None
        permisos = json.loads(fila[2]) if fila[2] else []
        return Rol(fila[1], permisos, id=fila[0])

    def listar_roles(self) -> list[Rol]:
        self.cursor.execute("SELECT id, nombre, permisos FROM rol ORDER BY id")
        roles = []
        for fila in self.cursor.fetchall():
            permisos = json.loads(fila[2]) if fila[2] else []
            roles.append(Rol(fila[1], permisos, id=fila[0]))
        return roles

    def insertar(self, usuario: Usuario) -> Usuario:
        if not usuario.persona or not usuario.persona.rut:
            raise ValueError("El usuario debe estar asociado a una persona con RUT.")
        if not usuario.rol or usuario.rol.id is None:
            raise ValueError("El usuario debe tener un rol con ID válido.")

        # Asegurar persona en BD
        self.cursor.execute("""
            INSERT INTO persona (rut, nombre) VALUES (?, ?)
            ON CONFLICT(rut) DO UPDATE SET nombre = excluded.nombre
        """, (usuario.persona.rut, usuario.persona.nombre))

        self.cursor.execute("""
            INSERT INTO usuario (usuario, password_hash, rol_id, persona_rut)
            VALUES (?, ?, ?, ?)
        """, (usuario.usuario, usuario.password_hash, usuario.rol.id, usuario.persona.rut))
        self.conexion.commit()
        return usuario

    def buscar(self, username: str) -> Usuario | None:
        self.cursor.execute("""
            SELECT u.usuario, u.password_hash, u.rol_id, r.nombre AS rol_nom, r.permisos,
                   p.rut AS persona_rut, p.nombre AS persona_nom
            FROM usuario u
            JOIN rol r ON u.rol_id = r.id
            JOIN persona p ON u.persona_rut = p.rut
            WHERE u.usuario = ?
        """, (username,))
        fila = self.cursor.fetchone()
        if fila is None:
            return None
        permisos = json.loads(fila[4]) if fila[4] else []
        rol = Rol(fila[3], permisos, id=fila[2])
        persona = Persona(fila[5], fila[6])
        return Usuario(fila[0], fila[1], rol, persona)

    def listar(self) -> list[Usuario]:
        self.cursor.execute("""
            SELECT u.usuario, u.password_hash, u.rol_id, r.nombre AS rol_nom, r.permisos,
                   p.rut AS persona_rut, p.nombre AS persona_nom
            FROM usuario u
            JOIN rol r ON u.rol_id = r.id
            JOIN persona p ON u.persona_rut = p.rut
            ORDER BY u.usuario
        """)
        usuarios = []
        for fila in self.cursor.fetchall():
            permisos = json.loads(fila[4]) if fila[4] else []
            rol = Rol(fila[3], permisos, id=fila[2])
            persona = Persona(fila[5], fila[6])
            usuarios.append(Usuario(fila[0], fila[1], rol, persona))
        return usuarios

    def actualizar(self, usuario: Usuario) -> Usuario | None:
        if not usuario.rol or usuario.rol.id is None:
            raise ValueError("El usuario debe tener un rol con ID válido.")
        self.cursor.execute("""
            UPDATE usuario
            SET password_hash = ?, rol_id = ?
            WHERE usuario = ?
        """, (usuario.password_hash, usuario.rol.id, usuario.usuario))
        self.conexion.commit()
        if self.cursor.rowcount == 0:
            return None
        return self.buscar(usuario.usuario)

    def eliminar(self, username: str) -> bool:
        try:
            self.cursor.execute("DELETE FROM usuario WHERE usuario = ?", (username,))
            self.conexion.commit()
            return self.cursor.rowcount > 0
        except sqlite3.IntegrityError:
            self.conexion.rollback()
            return False
