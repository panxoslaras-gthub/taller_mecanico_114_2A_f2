class Repuesto:
    def __init__(self, codigo: str, nombre: str, stock: int, es_importado: bool):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__stock = stock
        self.__es_importado = es_importado

    @property
    def codigo(self) -> str:
        return self.__codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        self.__codigo = valor

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = valor

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, valor: int) -> None:
        self.__stock = valor

    @property
    def es_importado(self) -> bool:
        return self.__es_importado

    @es_importado.setter
    def es_importado(self, valor: bool) -> None:
        self.__es_importado = bool(valor)

    def hay_stock(self) -> bool:
        return self.__stock > 0

    def __str__(self) -> str:
        importado_str = "Importado" if self.__es_importado else "Nacional"
        return f"Repuesto(codigo='{self.__codigo}', nombre='{self.__nombre}', stock={self.__stock}, tipo='{importado_str}')"

    def __repr__(self) -> str:
        return self.__str__()
