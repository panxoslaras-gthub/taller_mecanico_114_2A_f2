class Rol:
    def __init__(self, nombre: str, permisos: list, id: int | None = None):
        self.__id = id
        self.__nombre = nombre
        self.__permisos = list(permisos) if permisos else []

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
    def permisos(self) -> list:
        return self.__permisos

    @permisos.setter
    def permisos(self, valor: list) -> None:
        self.__permisos = list(valor)

    def tiene_permiso(self, accion: str) -> bool:
        return accion in self.__permisos

    def __str__(self) -> str:
        return f"Rol(id={self.__id}, nombre='{self.__nombre}', permisos={self.__permisos})"

    def __repr__(self) -> str:
        return self.__str__()
