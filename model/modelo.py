from model.marca import Marca

class Modelo:
    def __init__(self, nombre: str, marca: Marca, id: int | None = None):
        self.__id = id
        self.__nombre = nombre
        self.__marca = marca

    @property
    def id(self) -> int | None:
        return self.__id

    @id.setter
    def id(self, valor: int) -> None:
        self.__id = valor

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = valor

    @property
    def marca(self) -> Marca:
        return self.__marca

    @marca.setter
    def marca(self, valor: Marca) -> None:
        self.__marca = valor

    def __str__(self) -> str:
        marca_nom = self.__marca.nombre if self.__marca else "Sin marca"
        return f"Modelo(id={self.__id}, nombre='{self.__nombre}', marca='{marca_nom}')"

    def __repr__(self) -> str:
        return self.__str__()
