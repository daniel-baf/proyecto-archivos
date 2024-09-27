from src.config.archivo_secuencial.generador_secuencial import (
    GeneradorArchivoSecuencial,
)
from src.config.archivo_secuencial.extractor_secuencial import (
    ExtractorSecuencial,
)


class ControladorArchivoSecuencial:

    SEPARADORES = {
        "SEGMENTO": "@".encode("UTF-8"),
        "BLOQUE": "^".encode("utf-8"),
        "GRUPO": "#".encode("utf-8"),
        "CAMPO": "$".encode("utf-8"),
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
