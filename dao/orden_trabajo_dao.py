import sqlite3
from dao.dao import DAO
from dao.vehiculo_dao import VehiculoDAO
from dao.usuario_dao import UsuarioDAO
from model.orden_trabajo import OrdenTrabajo
from model.linea_detalle import LineaDetalle
from model.repuesto import Repuesto

class OrdenTrabajoDAO(DAO):
    def __init__(self, conexion):
        super().__init__(conexion)
        self.vehiculo_dao = VehiculoDAO(conexion)
        self.usuario_dao = UsuarioDAO(conexion)

    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orden_trabajo (
                numero INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT NOT NULL,
                horas INTEGER NOT NULL DEFAULT 0,
                cerrada INTEGER NOT NULL DEFAULT 0,
                vehiculo_patente TEXT NOT NULL,
                usuario_username TEXT NOT NULL,
                FOREIGN KEY (vehiculo_patente) REFERENCES vehiculo(patente),
                FOREIGN KEY (usuario_username) REFERENCES usuario(usuario)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS linea_detalle (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                orden_numero INTEGER NOT NULL,
                repuesto_codigo TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario INTEGER NOT NULL,
                FOREIGN KEY (orden_numero) REFERENCES orden_trabajo(numero) ON DELETE CASCADE,
                FOREIGN KEY (repuesto_codigo) REFERENCES repuesto(codigo)
            )
        """)
        self.conexion.commit()

    def insertar(self, orden: OrdenTrabajo) -> OrdenTrabajo:
        if not orden.vehiculo or not orden.vehiculo.patente:
            raise ValueError("La orden debe tener un vehículo con patente válida.")
        if not orden.usuario or not orden.usuario.usuario:
            raise ValueError("La orden debe tener un usuario válido.")

        self.cursor.execute("""
            INSERT INTO orden_trabajo (descripcion, horas, cerrada, vehiculo_patente, usuario_username)
            VALUES (?, ?, ?, ?, ?)
        """, (
            orden.descripcion,
            orden.horas,
            1 if orden.cerrada else 0,
            orden.vehiculo.patente,
            orden.usuario.usuario
        ))
        orden.numero = self.cursor.lastrowid

        # Insertar líneas de detalle si trae
        for linea in orden.lineas_detalle:
            if not linea.repuesto or not linea.repuesto.codigo:
                raise ValueError("Cada línea de detalle debe contener un repuesto con código válido.")
            self.cursor.execute("""
                INSERT INTO linea_detalle (orden_numero, repuesto_codigo, cantidad, precio_unitario)
                VALUES (?, ?, ?, ?)
            """, (orden.numero, linea.repuesto.codigo, linea.cantidad, linea.precio_unitario))
            linea.id = self.cursor.lastrowid

        self.conexion.commit()
        return orden

    def buscar(self, numero: int) -> OrdenTrabajo | None:
        self.cursor.execute("""
            SELECT numero, descripcion, horas, cerrada, vehiculo_patente, usuario_username
            FROM orden_trabajo
            WHERE numero = ?
        """, (numero,))
        fila = self.cursor.fetchone()
        if fila is None:
            return None

        vehiculo = self.vehiculo_dao.buscar(fila[4])
        usuario = self.usuario_dao.buscar(fila[5])

        orden = OrdenTrabajo(
            numero=fila[0],
            descripcion=fila[1],
            vehiculo=vehiculo,
            usuario=usuario,
            horas=fila[2],
            cerrada=bool(fila[3])
        )

        # Cargar líneas de detalle
        self.cursor.execute("""
            SELECT ld.id, ld.cantidad, ld.precio_unitario,
                   r.codigo, r.nombre, r.stock, r.es_importado
            FROM linea_detalle ld
            JOIN repuesto r ON ld.repuesto_codigo = r.codigo
            WHERE ld.orden_numero = ?
            ORDER BY ld.id
        """, (numero,))
        for det in self.cursor.fetchall():
            repuesto = Repuesto(det[3], det[4], det[5], bool(det[6]))
            linea = LineaDetalle(det[1], det[2], repuesto, id=det[0])
            orden.lineas_detalle.append(linea)

        return orden

    def listar(self) -> list[OrdenTrabajo]:
        self.cursor.execute("SELECT numero FROM orden_trabajo ORDER BY numero DESC")
        numeros = [fila[0] for fila in self.cursor.fetchall()]
        return [self.buscar(num) for num in numeros if self.buscar(num) is not None]

    def agregar_linea(self, orden_numero: int, linea: LineaDetalle) -> LineaDetalle:
        orden = self.buscar(orden_numero)
        if not orden:
            raise ValueError(f"No existe orden con número {orden_numero}.")
        if orden.cerrada:
            raise ValueError("No se pueden agregar detalles a una orden cerrada.")
        if not linea.repuesto or not linea.repuesto.codigo:
            raise ValueError("La línea de detalle debe contener un repuesto con código válido.")

        self.cursor.execute("""
            INSERT INTO linea_detalle (orden_numero, repuesto_codigo, cantidad, precio_unitario)
            VALUES (?, ?, ?, ?)
        """, (orden_numero, linea.repuesto.codigo, linea.cantidad, linea.precio_unitario))
        linea.id = self.cursor.lastrowid
        self.conexion.commit()
        return linea

    def agregar_horas(self, orden_numero: int, cantidad: int) -> bool:
        self.cursor.execute("""
            UPDATE orden_trabajo
            SET horas = horas + ?
            WHERE numero = ? AND cerrada = 0
        """, (cantidad, orden_numero))
        self.conexion.commit()
        return self.cursor.rowcount > 0

    def cerrar_orden(self, orden_numero: int) -> bool:
        self.cursor.execute("""
            UPDATE orden_trabajo
            SET cerrada = 1
            WHERE numero = ?
        """, (orden_numero,))
        self.conexion.commit()
        return self.cursor.rowcount > 0

    def eliminar(self, numero: int) -> bool:
        try:
            self.cursor.execute("DELETE FROM linea_detalle WHERE orden_numero = ?", (numero,))
            self.cursor.execute("DELETE FROM orden_trabajo WHERE numero = ?", (numero,))
            self.conexion.commit()
            return self.cursor.rowcount > 0
        except sqlite3.IntegrityError:
            self.conexion.rollback()
            return False
