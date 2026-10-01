from model.vehiculo import Vehiculo
from model.modelo import Modelo

class Auto(Vehiculo):
    def __init__(self, patente: str, anio: int, modelo: Modelo, capacidad_maletero: int, en_taller: bool = False):
        super().__init__(patente, anio, modelo, en_taller=en_taller)
        self.__capacidad_maletero: int = capacidad_maletero

    @property
    def capacidad_maletero(self) -> int:
        return self.__capacidad_maletero

    @capacidad_maletero.setter
    def capacidad_maletero(self, valor: int) -> None:
        self.__capacidad_maletero = valor

    def tarifa_hora(self) -> int:
        return 25000

    def __str__(self) -> str:
        estado = "En taller" if self.en_taller else "Fuera de taller"
        mod_nom = self.modelo.nombre if self.modelo else "Sin modelo"
        return f"Auto(patente='{self.patente}', anio={self.anio}, modelo='{mod_nom}', maletero={self.__capacidad_maletero}L, estado='{estado}')"

    def __repr__(self) -> str:
        return self.__str__()
