from model.persona import Persona

class Cliente:
    def __init__(self, persona: Persona, tiene_deuda: bool = False):
        self.__persona = persona
        self.__tiene_deuda = tiene_deuda

    @property
    def persona(self) -> Persona:
        return self.__persona

    @persona.setter
    def persona(self, valor: Persona) -> None:
        self.__persona = valor

    def tiene_deuda(self) -> bool:
        return self.__tiene_deuda

    def set_tiene_deuda(self, valor: bool) -> None:
        self.__tiene_deuda = bool(valor)

    def __str__(self) -> str:
        per_nom = self.__persona.nombre if self.__persona else "Sin persona"
        rut = self.__persona.rut if self.__persona else "S/RUT"
        return f"Cliente(rut='{rut}', nombre='{per_nom}', tiene_deuda={self.__tiene_deuda})"

    def __repr__(self) -> str:
        return self.__str__()
