from model.rol import Rol
from model.persona import Persona

class Usuario:
    def __init__(self, usuario: str, password_hash: str, rol: Rol, persona: Persona):
        self.__usuario = usuario
        self.__password_hash = password_hash
        self.__rol = rol
        self.__persona = persona

    @property
    def usuario(self) -> str:
        return self.__usuario

    @usuario.setter
    def usuario(self, valor: str) -> None:
        self.__usuario = valor

    @property
    def password_hash(self) -> str:
        return self.__password_hash

    @password_hash.setter
    def password_hash(self, valor: str) -> None:
        self.__password_hash = valor

    @property
    def rol(self) -> Rol:
        return self.__rol

    @rol.setter
    def rol(self, valor: Rol) -> None:
        self.__rol = valor

    @property
    def persona(self) -> Persona:
        return self.__persona

    @persona.setter
    def persona(self, valor: Persona) -> None:
        self.__persona = valor

    def autenticar(self, password_hash: str | None = None) -> bool:
        if password_hash is not None:
            return self.__password_hash == password_hash
        return True

    def puede(self, accion: str) -> bool:
        return self.__rol.tiene_permiso(accion) if self.__rol else False

    def __str__(self) -> str:
        rol_nom = self.__rol.nombre if self.__rol else "Sin rol"
        per_nom = self.__persona.nombre if self.__persona else "Sin persona"
        return f"Usuario(usuario='{self.__usuario}', rol='{rol_nom}', persona='{per_nom}')"

    def __repr__(self) -> str:
        return self.__str__()
