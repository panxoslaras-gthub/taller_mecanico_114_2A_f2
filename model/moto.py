from model.vehiculo import Vehiculo
from model.modelo import Modelo

class Moto(Vehiculo):
    def __init__(self, patente: str, anio: int, modelo: Modelo, en_taller: bool = False):
        super().__init__(patente, anio, modelo, en_taller=en_taller)

    def tarifa_hora(self) -> int:
        return 15000

    def __str__(self) -> str:
        estado = "En taller" if self.en_taller else "Fuera de taller"
        mod_nom = self.modelo.nombre if self.modelo else "Sin modelo"
        return f"Moto(patente='{self.patente}', anio={self.anio}, modelo='{mod_nom}', estado='{estado}')"

    def __repr__(self) -> str:
        return self.__str__()
