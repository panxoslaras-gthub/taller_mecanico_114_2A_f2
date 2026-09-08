# Definición de la clase Vehiculo
class Vehiculo:
    def __init__(self, patente: str, anio: int, en_taller: bool = True):
        """
        Constructor de la clase Vehiculo.
        Inicializa los atributos de instancia al registrar un vehículo en el taller.
        """
        # Atributo de tipo texto (cadena de caracteres) para la patente
        self.patente = patente
        # Atributo de tipo número entero para el año del vehículo
        self.anio = anio
        # Atributo booleano protegido que indica si está en taller (por defecto True)
        self._en_taller = en_taller

    # Método para registrar el ingreso del vehículo al taller mecánico
    def ingresar(self) -> None:
        # Cambia el valor del atributo _en_taller a True indicando que está en taller
        self._en_taller = True

    # Método para registrar la entrega o salida del vehículo del taller
    def entregar(self) -> None:
        # Cambia el valor del atributo _en_taller a False indicando que ya no está en taller
        self._en_taller = False
