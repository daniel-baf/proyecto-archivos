from .extractor_secuencial import ExtractorSecuencial
from .generador_secuencial import GeneradorArchivoSecuencial


class ControladorArchivoSecuencial:

    SEPARADORES = {
        "SEGMENTO": b"\x02",
        "BLOQUE": b"\x03",
        "GRUPO": b"\x04",
        "SUBGRUPO": b"\x05",
        "CAMPO": b"\x06",
        "DIVISOR": b"\x07",
    }

    def __init__(self) -> None:
        pass

    def crear_archivo(self, nombre_archivo: str, diccionario_datos: dict) -> None:
        """
        Obtiene el diccionario de datos y crea un archivo secuencial
        """
        generador_secuencial = GeneradorArchivoSecuencial(
            diccionario_datos, self.SEPARADORES
        )
        generador_secuencial.escribir(nombre_archivo)

    def leer_archivo(self, nombre_archivo: str) -> dict:
        """
        Lee un archivo secuencial y retorna un diccionario con los datos
        """
        extractor_secuencial = ExtractorSecuencial(nombre_archivo, self.SEPARADORES)
        return extractor_secuencial.leer()
