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
