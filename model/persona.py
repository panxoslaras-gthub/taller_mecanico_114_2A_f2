class Persona:
    def __init__(self, rut: str, nombre: str):
        self.__rut = rut
        self.__nombre = nombre

    @property
    def rut(self) -> str:
        return self.__rut

    @rut.setter
    def rut(self, valor: str) -> None:
        self.__rut = valor

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = valor

    def __str__(self) -> str:
        return f"Persona(rut='{self.__rut}', nombre='{self.__nombre}')"

    def __repr__(self) -> str:
        return self.__str__()
