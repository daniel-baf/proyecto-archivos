"""
ESTE ARCHIVO SE ENCARGA DE BUSCAR TODOS LOS ARCHIVOS
GIFs EN UNA CARPETA ESPECIFICA y retorna un listado de los archivos encontrados
"""

# Librerías
import os
from src.METADATOS.extractor_metadatos import ExtractorMetadatos


# Se encarga de buscar todos los archivos GIFs en un directorio
class BuscadorGifs:
    # Busca todos los archivos GIFs en un directorio de forma recursiva
    def _buscar_gifs(self, directorio: str, gifs: list) -> list:
        extractorMetadatos = ExtractorMetadatos()
        # Listar los elementos del directorio actual
        for elemento in os.listdir(directorio):
            ruta_completa = os.path.join(directorio, elemento)
            # Si es un archivo y termina en .gif, lo añadimos a la lista
            if os.path.isfile(ruta_completa) and ruta_completa.endswith(".gif"):
                # Convertir a ruta absoluta y añadir a la lista
                path = os.path.abspath(ruta_completa)
                gifs.append(
                    {
                        "path": path,
                        "nombre": elemento,
                        "metadatos": extractorMetadatos.extraer_metadatos(path),
                    }
                )
            # Si es un directorio, llamamos recursivamente a la función
            elif os.path.isdir(ruta_completa):
                self._buscar_gifs(ruta_completa, gifs)
        return gifs

    # Busca todos los archivos GIFs en un directorio de forma recursiva
    def buscar_gifs(self, root_folder: str):
        try:
            gifs = []
            # Directorio de los archivos GIFs
            return self._buscar_gifs(root_folder, gifs)
        except Exception as e:
            print(f"Error buscando archivos GIFs, se ha saltado este paso: {e}")
            return []
