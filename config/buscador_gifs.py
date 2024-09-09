"""
ESTE ARCHIVO SE ENCARGA DE BUSCAR TODOS LOS ARCHIVOS
GIFs EN UNA CARPETA ESPECIFICA y retorna un listado de los archivos encontrados
"""

# Librerias
import os


# Se encarga de buscar todos los archivos GIFs en un directorio
class BuscadorGifs:
    # Busca todos los archivos GIFs en un directorio de forma recursiva
    def _buscar_gifs(self, directorio: str, gifs: list) -> list:
        # Listar los elementos del directorio actual
        for elemento in os.listdir(directorio):
            ruta_completa = os.path.join(directorio, elemento)
            # Si es un archivo y termina en .gif, lo añadimos a la lista
            if os.path.isfile(ruta_completa) and ruta_completa.endswith(".gif"):
                # Convertir a ruta absoluta y añadir a la lista
                gifs.append(os.path.abspath(ruta_completa))
            # Si es un directorio, llamamos recursivamente a la función
            elif os.path.isdir(ruta_completa):
                self._buscar_gifs(ruta_completa, gifs)
        return gifs

    # Busca todos los archivos GIFs en un directorio de forma recursiva
    def buscar_gifs(self, root_folder: str):
        # Directorio de los archivos GIFs
        gifs = []
        return self._buscar_gifs(root_folder, gifs)
