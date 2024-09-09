"""
PROYECTO DE MANEJO E IMPLEMENTACIÓN DE ARCHIVOS, LECUTRA DE METADATOS EN UN ARCHIVO GIF
REALIZADO POR DANIEL B. & CHRIS VILLEGAS

ARCHIVO PRINCIPAL, DONDE SE EJECUTA EL PROGRAMA
"""

# importar el configurador
from config.configurador import Configurador

from pprint import pprint
import tkinter as tk
from tkinter import filedialog


class Main:
    def __init__(self):
        self.configurador = Configurador()

    # Método para seleccionar un archivo en caso no exista el archivo de configuración
    def seleccionar_path(self) -> str | None:
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana principal
        folder_path = filedialog.askdirectory(title="Selecciona una carpeta")
        if not folder_path:
            return None
        return folder_path

    # inicializa la app
    def start(self):
        existe_archivo = self.configurador.existe_archivo()
        json_gifs = None
        if not existe_archivo:
            path = self.seleccionar_path()
            if not path:
                return
            json_gifs = self.configurador.configurar(path)
        else:
            json_gifs = self.configurador.obtener_json()

        pprint(json_gifs)


if __name__ == "__main__":
    main = Main()
    main.start()
