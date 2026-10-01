from model.repuesto import Repuesto

class LineaDetalle:
    def __init__(self, cantidad: int, precio_unitario: int, repuesto: Repuesto, id: int | None = None):
        self.__id = id
        self.__cantidad = cantidad
        self.__precio_unitario = precio_unitario
        self.__repuesto = repuesto

    @property
    def id(self) -> int | None:
        return self.__id

    @id.setter
    def id(self, valor: int) -> None:
        self.__id = valor

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        self.__cantidad = valor

    @property
    def precio_unitario(self) -> int:
        return self.__precio_unitario

    @precio_unitario.setter
    def precio_unitario(self, valor: int) -> None:
        self.__precio_unitario = valor

    @property
    def repuesto(self) -> Repuesto:
        return self.__repuesto

    @repuesto.setter
    def repuesto(self, valor: Repuesto) -> None:
        self.__repuesto = valor

    def subtotal(self) -> int:
        return self.__cantidad * self.__precio_unitario

    def __str__(self) -> str:
        rep_nom = self.__repuesto.nombre if self.__repuesto else "Sin repuesto"
        return f"LineaDetalle(id={self.__id}, repuesto='{rep_nom}', cant={self.__cantidad}, precio={self.__precio_unitario}, subtotal={self.subtotal()})"

    def __repr__(self) -> str:
        return self.__str__()
