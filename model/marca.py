class Marca:
    def __init__(self, nombre: str):
        self.__id=None
        self.__nombre = nombre

    @property
    def id(self)->int:
        return self.__id

    @id.setter
    def id(self, valor:int)->None:
        self.__id=valor
    
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = valor

    def __str__(self) -> str:
        return f"Marca(id={self.__id}, nombre='{self.__nombre}')"

    def __repr__(self) -> str:
        return self.__str__()
