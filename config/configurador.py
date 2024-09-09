""""
    -----------------------------------------
    ARCHIVO DE CONFIGURACION DE LA APLICACION
    -----------------------------------------
"""

# Librerias
import json
import os
from config.buscador_gifs import BuscadorGifs


# Configuracion de la aplicacion
class Configurador:
    # Configuracion de la aplicacion
    CONFIG_PATH = "config/config.json"
    JSON_CONFIG = {"folder": "", "gifs": []}

    # Constructor
    def __init__(self):
        self.buscador_gifs = BuscadorGifs()

    # crea el archivo de configuracion
    def crear_archivo_configuracion(self, folder: str = ""):
        # Si el archivo existe, omitir
        if self.existe_archivo():
            return

        self.JSON_CONFIG["folder"] = folder
        json_copy = self.JSON_CONFIG.copy()
        json_copy["gifs"] = self.buscador_gifs.buscar_gifs(json_copy["folder"])
        with open(self.CONFIG_PATH, "w") as file:
            json.dump(json_copy, file, indent="\t")

    # Verifica si el archivo de configuracion existe y retorna el JSON
    def configurar(self, gifs_folder: str = "") -> dict | None:
        try:
            # Si el archivo existe, retorna el JSON
            self.crear_archivo_configuracion(gifs_folder)
            # Si el folder no esta vacio, se actualiza el folder
            return self.obtener_json()
        except Exception as e:
            print(f"Error: {e}")
            return None

    # Recupera el JSON del archivo de configuracion
    def obtener_json(self):
        with open(self.CONFIG_PATH, "r") as file:
            return json.load(file)

    # Verifica si el archivo de configuracion existe
    def existe_archivo(self):
        return os.path.exists(self.CONFIG_PATH)
