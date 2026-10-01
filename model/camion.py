from model.vehiculo import Vehiculo
from model.modelo import Modelo

class Camion(Vehiculo):
    def __init__(self, patente: str, anio: int, modelo: Modelo, capacidad_carga: int, en_taller: bool = False):
        super().__init__(patente, anio, modelo, en_taller=en_taller)
        self.__capacidad_carga: int = capacidad_carga

    @property
    def capacidad_carga(self) -> int:
        return self.__capacidad_carga

    @capacidad_carga.setter
    def capacidad_carga(self, valor: int) -> None:
        self.__capacidad_carga = valor

    def tarifa_hora(self) -> int:
        return 40000

    def __str__(self) -> str:
        estado = "En taller" if self.en_taller else "Fuera de taller"
        mod_nom = self.modelo.nombre if self.modelo else "Sin modelo"
        return f"Camion(patente='{self.patente}', anio={self.anio}, modelo='{mod_nom}', carga={self.__capacidad_carga}kg, estado='{estado}')"

    def __repr__(self) -> str:
        return self.__str__()
