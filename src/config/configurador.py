""""
    -----------------------------------------
    ARCHIVO DE CONFIGURACIÓN DE LA APLICACIÓN
    -----------------------------------------
"""

# Librerías
import json
import os
from .buscador_gifs import BuscadorGifs
from .archivo_secuencial.archivo_secuencial import (
    ControladorArchivoSecuencial,
)


# Configuración de la aplicación
class Configurador:
    # Configuración de la aplicación
    CONFIG_PATH = "config.bin"
    DATA_CONFIG = {"folder": "", "gifs": []}

    # Constructor
    def __init__(self):
        self.buscador_gifs = BuscadorGifs()
        self.archivo_secuencial = ControladorArchivoSecuencial()

    # crea el archivo de Configuración
    def crear_archivo_configuracion(self, folder: str = ""):
        try:
            self.DATA_CONFIG["folder"] = folder
            json_copy = self.DATA_CONFIG.copy()
            json_copy["gifs"] = self.buscador_gifs.buscar_gifs(json_copy["folder"])
            # llamamos al servicio de secuenciales
            self.archivo_secuencial.crear_archivo(self.CONFIG_PATH, json_copy)
            self.DATA_CONFIG = json_copy
        except Exception as e:
            print(f"No se pudo crear el archivo de configuración: {e}")
            exit()

    # Verifica si el archivo de configuración existe y retorna el JSON
    def configurar(self, gifs_folder: str = "") -> dict | None:
        try:
            # Si el archivo existe, retorna el JSON
            self.crear_archivo_configuracion(gifs_folder)
            # Si el folder no esta vació, se actualiza el folder
            return self.obtener_config()
        except Exception as e:
            print(f"No se pudo configurar el archivo: {e}")
            exit()

    # Recupera el JSON del archivo de configuracion
    def obtener_config(self):
        try:
            return self.archivo_secuencial.leer_archivo(self.CONFIG_PATH)
        except Exception as e:
            print(f"No se ha podido leer el archivo de configuración: {e}")
            return {}

    # Verifica si el archivo de configuración existe
    def existe_archivo(self):
        return os.path.exists(self.CONFIG_PATH)
