from model.vehiculo import Vehiculo
from model.usuario import Usuario
from model.linea_detalle import LineaDetalle

class OrdenTrabajo:
    def __init__(self, numero: int | None, descripcion: str, vehiculo: Vehiculo, usuario: Usuario, horas: int = 0, cerrada: bool = False):
        self.__numero = numero
        self.__descripcion = descripcion
        self.__horas = horas
        self.__cerrada = cerrada
        self.__vehiculo = vehiculo
        self.__usuario = usuario
        self.__lineas_detalle: list[LineaDetalle] = []

    @property
    def numero(self) -> int | None:
        return self.__numero

    @numero.setter
    def numero(self, valor: int) -> None:
        self.__numero = valor

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        self.__descripcion = valor

    @property
    def horas(self) -> int:
        return self.__horas

    @property
    def cerrada(self) -> bool:
        return self.__cerrada

    @property
    def vehiculo(self) -> Vehiculo:
        return self.__vehiculo

    @vehiculo.setter
    def vehiculo(self, valor: Vehiculo) -> None:
        self.__vehiculo = valor

    @property
    def usuario(self) -> Usuario:
        return self.__usuario

    @usuario.setter
    def usuario(self, valor: Usuario) -> None:
        self.__usuario = valor

    @property
    def lineas_detalle(self) -> list[LineaDetalle]:
        return self.__lineas_detalle

    def agregar_horas(self, cantidad: int) -> None:
        if not self.__cerrada:
            self.__horas += cantidad

    def agregar_linea_detalle(self, linea: LineaDetalle) -> None:
        if not self.__cerrada:
            self.__lineas_detalle.append(linea)

    def cerrar(self) -> None:
        self.__cerrada = True

    def total(self) -> int:
        total_repuestos = sum(linea.subtotal() for linea in self.__lineas_detalle)
        tarifa = self.__vehiculo.tarifa_hora() if self.__vehiculo else 0
        total_horas = self.__horas * tarifa
        return total_repuestos + total_horas

    def __str__(self) -> str:
        estado = "Cerrada" if self.__cerrada else "Abierta"
        pat = self.__vehiculo.patente if self.__vehiculo else "S/P"
        user = self.__usuario.usuario if self.__usuario else "S/U"
        return f"OrdenTrabajo(num={self.__numero}, desc='{self.__descripcion}', vehiculo='{pat}', usuario='{user}', horas={self.__horas}, total={self.total()}, estado='{estado}')"

    def __repr__(self) -> str:
        return self.__str__()
