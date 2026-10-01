from model.modelo import Modelo

class Vehiculo: # Define la clase Vehiculo
    def __init__(self, patente: str, anio: int, modelo: Modelo, en_taller: bool = False): # Constructor que recibe patente, año, modelo y estado opcional
        self.patente = patente # Asigna la patente mediante el setter para ejecutar la validación
        self.__anio: int = anio # Asigna el año recibido a un atributo privado
        self.__en_taller: bool = en_taller # Inicializa el estado en taller
        self.__modelo: Modelo = modelo

    @property
    def modelo(self) -> Modelo:
        return self.__modelo

    @modelo.setter
    def modelo(self, valor: Modelo) -> None:
        self.__modelo = valor

    @property
    def anio(self)-> int:
        return self.__anio

    @anio.setter
    def anio(self, valor: int) -> None:
        self.__anio = valor

    @property
    def en_taller(self)-> bool:
        return self.__en_taller

    @en_taller.setter
    def en_taller(self, valor: bool) -> None:
        self.__en_taller = bool(valor)

    @property
    def patente(self) -> str: # Getter que permite acceder a la patente como atributo (vehiculo.patente)
        return self.__patente # Retorna el valor del atributo privado __patente

    @patente.setter
    def patente(self, valor: str) -> None: # Setter que intercepta las asignaciones para validar la patente
        if len(valor) < 6 or " " in valor: # Valida que la patente tenga al menos 6 caracteres y sin espacios
            raise ValueError("La patente debe tener al menos 6 caracteres y no debe contener espacios.") # Lanza error si no es válida
        self.__patente: str = valor # Asigna el valor validado al atributo privado __patente

    def get_patente(self) -> str: # Método alternativo getter tradicional
        return self.patente # Retorna la patente a través de la propiedad

    def set_patente(self, valor: str) -> None: # Método alternativo setter tradicional
        self.patente = valor # Asigna a través del setter de la propiedad con validación

    def ingresar(self) -> str: # Método para registrar el ingreso del vehículo al taller
        if self.__en_taller: # Verifica si el vehículo ya está marcado como dentro del taller
            return "El vehículo ya se encuentra en el taller." # Devuelve mensaje si ya estaba ingresado
        self.__en_taller = True # Cambia el estado a True (ingresado)
        return "El vehículo ha ingresado al taller." # Devuelve mensaje de éxito

    def entregar(self) -> str: # Método para registrar la salida o entrega del vehículo
        if not self.__en_taller: # Verifica si el vehículo no está en el taller
            return "El vehículo no se encuentra en el taller." # Devuelve mensaje indicando que no se puede entregar
        self.__en_taller = False # Cambia el estado a False (fuera del taller)
        return "El vehículo ha sido entregado." # Devuelve mensaje de éxito

    def tarifa_hora(self) -> int: # Método que retorna el costo de la tarifa por hora
        return 5000 # Retorna un valor fijo de 5000

    def __str__(self) -> str:
        estado = "En taller" if self.__en_taller else "Fuera de taller"
        mod_nom = self.__modelo.nombre if self.__modelo else "Sin modelo"
        return f"Vehiculo(patente='{self.__patente}', anio={self.__anio}, modelo='{mod_nom}', estado='{estado}')"

    def __repr__(self) -> str:
        return self.__str__()
