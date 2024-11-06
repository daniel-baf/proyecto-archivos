def _leer_paleta_colores(self, metadata: dict, file: bytearray) -> None:
    """
    Extracts the global palette colors from the byte stream and adds them to the metadata dictionary.

    The function assumes that the global palette consists of a certain number of colors,
    and each color is represented by three bytes (RGB).
    """
    paleta_global = {}  # Diccionario para almacenar la paleta global
    paleta_bytes = extract_from_bytes(self.SEPARADORES["GRUPO"], file)
    try:
        cantidad = extract_from_bytes(self.SEPARADORES["CAMPO"], paleta_bytes)
        # almacenamos el valor
        paleta_global["cantidad"] = int.from_bytes(cantidad, byteorder="big")
        # index de tabla
        has_color_append = extract_from_bytes(
            self.SEPARADORES["CAMPO"], paleta_bytes
        )
        # vemos si hay varios colores
        # borramos el primer byte
        if bytes(has_color_append) == b"\x00":
            paleta_global["colores"] = None
            return

        # Hay listado de colores
        paleta_global["colores"] = []
        color_list = paleta_bytes
        for i in range(0, len(color_list), 4):
            r = color_list[i]
            g = color_list[i + 1]
            b = color_list[i + 2]
            paleta_global["colores"].append((r, g, b))
    except Exception as e:
        mostrar_error(f"Error al leer la paleta de colores: {e}")
    finally:
        metadata["paleta_global"] = paleta_global

def _leer_resumen(self, metadatos: dict, file: bytearray) -> None:
    """
    Extracts the summary information from the byte stream and adds it to the metadata dictionary.
    """
    resumen = {}
    try:
        resumen_bytes = extract_from_bytes(self.SEPARADORES["GRUPO"], file)
        tmp_bytes = extract_from_bytes(self.SEPARADORES["CAMPO"], resumen_bytes)
        resumen["cantidad_imagenes"] = int.from_bytes(tmp_bytes, byteorder="big")
        resumen["cantidad_frames"] = int.from_bytes(
            extract_from_bytes(self.SEPARADORES["CAMPO"], resumen_bytes),
            byteorder="big",
        )
        resumen["comentarios"] = int.from_bytes(
            extract_from_bytes(self.SEPARADORES["CAMPO"], resumen_bytes),
            byteorder="big",
        )
    except Exception as e:
        mostrar_error(f"Error al leer el resumen: {e}")
    metadatos["resumen"] = resumen

def _extract_type_of_block(self, tipo_bloque: str, valor: str) -> any:
    """
    Extracts the type of block from the byte array and returns it.
    """
    try:
        # Verificar el tipo de bloque
        if tipo_bloque == "bool":
            return bool(int(valor))
        elif tipo_bloque == "num":
            return int(valor)
        return valor
    except Exception as e:
        mostrar_error(f"No se ha podido extraer el tipo de bloque: {e}")
        return

def _leer_bloques(self, gif: dict, file: bytearray) -> None:
    """
    Extracts the blocks from the byte stream and adds them to the gif dictionary.
    """
    bloques = []  # Lista para almacenar bloques
    try:
        bloques_bytes = extract_from_bytes(self.SEPARADORES["GRUPO"], file)
        while bloque_subgrupo := extract_from_bytes(
                self.SEPARADORES["SUBGRUPO"], bloques_bytes
        ):
            bloque = {}
            # leer cada campo
            while campo := extract_from_bytes(
                    self.SEPARADORES["CAMPO"], bloque_subgrupo
            ):
                clave = extract_from_bytes(
                    self.SEPARADORES["DIVISOR"], campo
                ).decode("utf-8")
                tipo_bloque = extract_from_bytes(
                    self.SEPARADORES["DIVISOR"], campo
                ).decode("utf-8")
                valor = campo.decode("utf-8")
                bloque[clave] = self._extract_type_of_block(tipo_bloque, valor)
            bloques.append(bloque)
    except Exception as e:
        mostrar_error(f"No se ha podido leer los bloques: {e}")
    gif["bloques"] = bloques
#Configurador

""""
    -----------------------------------------
    ARCHIVO DE CONFIGURACIÓN DE LA APLICACIÓN
    -----------------------------------------
"""
# Librerías
import json
import os
#from .buscador_gifs import BuscadorGifs

"""from .archivo_secuencial.archivo_secuencial import (
    ControladorArchivoSecuencial,
)
"""
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
# Manejador de errores:
from pprint import pformat

from colorama import init, Fore, Style # type: ignore
# Inicializa colorama


init()


def mostrar_error(mensaje: str) -> None:
    """
    Muestra un mensaje de error.
    """
    # TODO mostrar en ventana con UI
    rojo = Fore.RED
    reset = Style.RESET_ALL
    mensaje_formateado = pformat(mensaje)
    print(f"{rojo}{mensaje_formateado}{reset}")


def mostrar_completado(mensaje: str) -> None:
    """
    Muestra un mensaje de completado.
    """
    # TODO mostrar en ventana con UI
    verde = Fore.GREEN
    reset = Style.RESET_ALL
    mensaje_formateado = pformat(mensaje)
    print(f"{verde}{mensaje_formateado}{reset}")

def mostrar_alerta(mensaje: str) -> None:
    """
    Muestra un mensaje de alerta.
    """
    # TODO mostrar en ventana con UI
    amarillo = Fore.YELLOW
    reset = Style.RESET_ALL
    mensaje_formateado = pformat(mensaje)
    print(f"{amarillo}{mensaje_formateado}{reset}")
#Buscador gifs

"""
ESTE ARCHIVO SE ENCARGA DE BUSCAR TODOS LOS ARCHIVOS
GIFs EN UNA CARPETA ESPECIFICA y retorna un listado de los archivos encontrados
"""
# Librerías
import os
from src.METADATOS.extractor_metadatos import ExtractorMetadatos


from src.utils.manejador_errores import mostrar_error
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
            mostrar_error(f"Error buscando archivos GIFs, se ha saltado este paso: {e}")
            return []

#Archivo secuencial
#from .extractor_secuencial import ExtractorSecuencial
#from .generador_secuencial import GeneradorArchivoSecuencial


class ControladorArchivoSecuencial:


    SEPARADORES = {
        "SEGMENTO": b"\x14",
        "GRUPO": b"\x15",
        "SUBGRUPO": b"\x16",
        "CAMPO": b"\x17",
        "DIVISOR": b"\x18",
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
#Extractor secuencial
from typing import BinaryIO
#from .utils.secuencial_utils import read_n_bytes, read_till_byte, extract_from_bytes


from src.utils.manejador_errores import mostrar_error, mostrar_alerta
class ExtractorSecuencial:

    def __init__(self, file_name: str, separadores: dict) -> None:
        self.file_name = file_name  # Nombre del archivo a leer
        self.data_dictionary = {
            "folder": "",
            "gifs": [],
        }  # Diccionario para almacenar datos extraídos
        self.SEPARADORES = separadores  # Separadores definidos para la lectura

    def _leer_generic(self, file: BinaryIO) -> None:
        """
        Extracts the generic data from the byte stream and adds it to the data dictionary.
        add folder
        It is used to extract the generic info of all the JSON file
        """
        try:
            generic_segment = read_till_byte(self.SEPARADORES["SEGMENTO"], file)
            folder = generic_segment.decode("utf-8")
            self.data_dictionary["folder"] = folder
        except Exception as e:
            mostrar_error(f"No se ha podido leer la carpeta: {e}")

    def _leer_generic_gif(self, gif: dict, file: bytearray) -> None:
        """
        Extracts the generic data from the byte stream and adds it to the gif dictionary., path and name
        """
        try:
            gif_path = extract_from_bytes(self.SEPARADORES["GRUPO"], file)
            gif_name = extract_from_bytes(self.SEPARADORES["GRUPO"], file)
            gif["path"] = gif_path.decode("utf-8")
            gif["nombre"] = gif_name.decode("utf-8")
        except Exception as e:
            mostrar_error(f"No se ha podido leer datos genéricos del gif: {e}")

    def _leer_fechas(self, gif: dict, file: bytearray) -> None:
        """
        Extracts the dates from the byte stream and adds them to the gif dictionary.
        """
        # Leer hasta el grupo de fechas
        date_bytes = extract_from_bytes(self.SEPARADORES["GRUPO"], file)

        # Diccionario para almacenar fechas
        fecha = {}
        try:
            # Extraer y convertir fecha_creado de bytes a cadena y luego a float
            created_bytes = extract_from_bytes(self.SEPARADORES["CAMPO"], date_bytes)
            fecha_creado_str = created_bytes.decode("utf-8")  # Decodificar a cadena
            fecha["fecha_creado"] = float(
                fecha_creado_str
            )  # Convertir la cadena a float

            # Extraer y convertir fecha_modificado de bytes a cadena y luego a float
            modified_bytes = extract_from_bytes(self.SEPARADORES["CAMPO"], date_bytes)
            fecha_modificado_str = modified_bytes.decode(
                "utf-8"
            )  # Decodificar a cadena
            fecha["fecha_modificado"] = float(
                fecha_modificado_str
            )  # Convertir la cadena a float

            # Agregar las fechas al diccionario gif
            gif["fechas"] = fecha

        except Exception as e:
            mostrar_error(f"Error al recuperar las fechas: {e}")

    def _leer_pantalla(self, metadata: dict, file: bytearray) -> None:
        try:
            pantalla = {}  # Diccionario para almacenar información de pantalla
            bytes_pantalla = extract_from_bytes(self.SEPARADORES["GRUPO"], file)
            # Leer propiedades de la pantalla
            ancho = int.from_bytes(
                extract_from_bytes(self.SEPARADORES["CAMPO"], bytes_pantalla),
                byteorder="big",
            )  # Leer ancho
            alto = int.from_bytes(
                extract_from_bytes(self.SEPARADORES["CAMPO"], bytes_pantalla),
                byteorder="big",
            )  # Leer alto
            paleta_global = (
                int.from_bytes(
                    extract_from_bytes(self.SEPARADORES["CAMPO"], bytes_pantalla),
                    byteorder="big",
                )
                == 1  # Verificar si la paleta global está presente
            )
            fondo = int.from_bytes(
                extract_from_bytes(self.SEPARADORES["CAMPO"], bytes_pantalla),
                byteorder="big",
            )  # Leer color de fondo
            proporcion_pixeles = int.from_bytes(
                extract_from_bytes(self.SEPARADORES["CAMPO"], bytes_pantalla),
                byteorder="big",
            )  # Leer proporción de píxeles
            bits_color = int.from_bytes(
                extract_from_bytes(self.SEPARADORES["CAMPO"], bytes_pantalla),
                byteorder="big",
            )  # Leer cantidad de bits de color

            # Crear diccionario de propiedades de la pantalla
            pantalla = {
                "ancho": ancho,
                "alto": alto,
                "paleta_global": paleta_global,
                "fondo": fondo,
                "proporcion_pixeles": proporcion_pixeles,
                "bits_color": bits_color,
            }

            metadata["pantalla"] = pantalla  # Agregar pantalla a los metadatos
        except Exception as e:
            mostrar_error(f"Error al leer la pantalla: {e}")

    def _leer_metadatos(self, bytes: bytearray, gif: dict) -> tuple:
        """
        Extrae los metadatos y los encapsula en un diccionario. Parte del diccionario del gif
        """
        try:
            metadatos = {}  # Diccionario para almacenar metadatos
            # get header
            metadatos["header"] = read_till_byte(
                self.SEPARADORES["GRUPO"], bytes
            ).decode(
                "utf-8"
            )  # Leer el encabezado
            # get pantalla
            self._leer_pantalla(bytes, metadatos)  # Leer información de la pantalla
            # get paleta colores
            self._leer_paleta_colores(bytes, metadatos)  # Leer paleta de colores

            while (len(bytes)) > 0:  # Mientras queden bytes por leer
                gif_group_byte = read_till_byte(
                    self.SEPARADORES["GRUPO"], bytes
                )  # Leer grupo de GIF

            gif["metadatos"] = metadatos  # Agregar metadatos al diccionario gif
        except Exception as e:
            mostrar_error(f"No se ha podido leer los metadatos: {e}")

    def leer(self) -> dict:
        with open(self.file_name, "rb") as file:  # Abrir el archivo en modo binario
            self._leer_generic(file)
            # Leer los GIFs, al final debemos eliminar el byte de SEGMENTO para cerrar el archivo
            self.data_dictionary["gifs"] = []  # Inicializar la lista de GIFs
            # Leer los GIFs
            while gif_bytes := read_till_byte(
                self.SEPARADORES["SEGMENTO"], file
            ):  # Mientras queden bytes de GIFs por leer
                gif = {}  # Diccionario para un GIF
                self._leer_generic_gif(gif, gif_bytes)  # Leer datos genéricos del GIF
                metadata = {}
                self._leer_fechas(metadata, gif_bytes)  # Leer fechas del GIF
                metadata["header"] = extract_from_bytes(
                    self.SEPARADORES["GRUPO"], gif_bytes
                ).decode("utf-8")
                self._leer_pantalla(
                    metadata, gif_bytes
                )  # Leer información de la pantalla
                self._leer_resumen(metadata, gif_bytes)  # Leer resumen del GIF
                self._leer_paleta_colores(metadata, gif_bytes)
                self._leer_bloques(gif, gif_bytes)  # Leer bloques del GIF
                gif["metadatos"] = metadata
                self.data_dictionary["gifs"].append(gif)  # Agregar el GIF a la lista
        return self.data_dictionary  # Retornar el diccionario de datos extraídos
#Generador secuencial:
#from .utils.secuencial_utils import append_bytes
from src.utils.manejador_errores import mostrar_error


class GeneradorArchivoSecuencial:
    def __init__(self, custom_dict, separadores: dict = []):
        self.data_dictionary = custom_dict
        self.SEPARADORES = separadores

    def _agregar_generic(self, file_name: str) -> None:
        """
        Agrega los datos genéricos al archivo como bytes.
        """
        try:
            bytes = bytearray()
            bytes += (
                self.data_dictionary["folder"].encode("utf-8")
                + self.SEPARADORES["SEGMENTO"]
            )
            append_bytes(bytes, file_name)
        except Exception as e:
            mostrar_error(f"Error recuperando datos de configuracion: {e}")

    def _agregar_gif_generic(self, file_name: str, gif: dict) -> None:
        """
        Agrega los datos de un gif al archivo como bytes. Agrega el path y el nombre del gif.
        """
        try:
            gif_generic_bytes = bytearray()
            gif_generic_bytes += gif["path"].encode("utf-8") + self.SEPARADORES["GRUPO"]
            gif_generic_bytes += (
                gif["nombre"].encode("utf-8") + self.SEPARADORES["GRUPO"]
            )
            append_bytes(gif_generic_bytes, file_name)
        except Exception as e:
            mostrar_error(f"Error recuperando los metadatos genéricos del gif: {e}")

    def _agregar_fechas(self, fechas: dict, file_name: str) -> None:
        """
        Agrega las fechas al archivo como texto codificado en bytes.
        Convierte los floats a cadena de texto antes de almacenarlos.
        """
        try:
            fechas_bytes = bytearray()
            for key, value in fechas.items():
                # Convertir el float a una representación de cadena
                if isinstance(value, float):
                    timestamp_str = f"{value:.15f}"  # Convertir float a cadena con 15 decimales de precisión
                else:
                    timestamp_str = str(
                        float(value)
                    )  # Convertir otros valores a float y luego a cadena
                # Convertir la cadena a bytes
                timestamp_bytes = timestamp_str.encode("utf-8")
                # Agregar los bytes al bytearray con el separador de campo
                fechas_bytes += timestamp_bytes + self.SEPARADORES["CAMPO"]
            # Finalizar con el separador de grupo
            fechas_bytes += self.SEPARADORES["GRUPO"]
            # Escribir los bytes en el archivo
            append_bytes(fechas_bytes, file_name)

        except Exception as e:
            mostrar_error(f"Error recuperando los metadatos de fechas: {e}")

    def _agregar_pantalla(self, pantalla: dict, file_name: str) -> None:
        """
        Agrega los metadatos de la pantalla al archivo como bytes.
        """
        try:
            screen_bytes = bytearray()
            # Convertir y agregar el ancho
            ancho = int(pantalla["ancho"])
            screen_bytes += (
                ancho.to_bytes(2, byteorder="big") + self.SEPARADORES["CAMPO"]
            )  # Suponiendo que el ancho usa 2 bytes
            # Convertir y agregar el alto
            alto = int(pantalla["alto"])
            screen_bytes += (
                alto.to_bytes(2, byteorder="big") + self.SEPARADORES["CAMPO"]
            )  # Suponiendo que el alto usa 2 bytes
            # Convertir y agregar el valor booleano de 'paleta_global'
            paleta_global = 1 if pantalla["paleta_global"] else 0
            screen_bytes += (
                paleta_global.to_bytes(1, byteorder="big") + self.SEPARADORES["CAMPO"]
            )  # Usando 1 byte para el booleano
            # Convertir y agregar el fondo
            fondo = int(pantalla["fondo"])
            screen_bytes += (
                fondo.to_bytes(1, byteorder="big") + self.SEPARADORES["CAMPO"]
            )  # Suponiendo que el fondo usa 1 byte
            # Convertir y agregar la proporción de píxeles
            proporcion_pixeles = int(pantalla["proporcion_pixeles"])
            screen_bytes += (
                proporcion_pixeles.to_bytes(1, byteorder="big")
                + self.SEPARADORES["CAMPO"]
            )  # Suponiendo que la proporción usa 1 byte
            # Convertir y agregar los bits de color
            bits_color = int(pantalla["bits_color"])
            screen_bytes += (
                bits_color.to_bytes(1, byteorder="big") + self.SEPARADORES["CAMPO"]
            )  # Suponiendo que los bits de color usan 1 byte
            # Finalizar con el separador de grupo
            screen_bytes += self.SEPARADORES["GRUPO"]
            append_bytes(screen_bytes, file_name)
        except Exception as e:
            mostrar_error(f"Error recuperando los metadatos de la pantalla: {e}")

    def _agregar_paleta_colores(
        self, paleta_global_colores: dict, file_name: str
    ) -> None:
        """
        Agrega los datos de la paleta global de colores al archivo como bytes.
        Maneja una cantidad de colores y una lista opcional de tuplas RGB.
        """
        try:
            # Convertir y agregar la cantidad de colores
            cantidad = int(paleta_global_colores["cantidad"])
            bytes_colores = bytearray()
            bytes_colores += cantidad.to_bytes(2, byteorder="big")
            bytes_colores += self.SEPARADORES["CAMPO"]

            # Manejar el caso en que 'colores' sea null o una lista
            colores = paleta_global_colores["colores"]

            byte_index_color = b"\x00" if colores is None else b"\x01"
            bytes_colores += byte_index_color
            bytes_colores += self.SEPARADORES["CAMPO"]
            append_bytes(bytes_colores, file_name)
            bytes_colores = bytearray()

            if colores is not None:
                # Si hay colores, iteramos sobre la lista de tuplas RGB
                for rgb_tuple in colores:
                    tmp_color_bytes = bytearray()
                    r, g, b = rgb_tuple
                    # Cada color (R, G, B) ocupa 1 byte, así que agregamos los 3 bytes para cada color
                    tmp_color_bytes.extend([r, g, b])
                    tmp_color_bytes.extend(self.SEPARADORES["CAMPO"])
                    append_bytes(tmp_color_bytes, file_name)

            # Finalizar con el separador de grupo
            bytes_colores.extend(self.SEPARADORES["GRUPO"])
            append_bytes(bytes_colores, file_name)
        except Exception as e:
            mostrar_error(
                f"Error recuperando los metadatos de la paleta de colores: {e}"
            )

    def _agregar_resumen(self, resumen: dict, file_name: str) -> None:
        """
        Agrega los datos del resumen al archivo como bytes.
        """
        try:
            # Convertir y agregar la cantidad de imágenes, frames y comentarios
            cantidad_imagenes = int(resumen["cantidad_imagenes"])
            cantidad_frames = int(resumen["cantidad_frames"])
            cantidad_comentarios = int(resumen["cantidad_comentarios"])
            summary_bytes = bytearray()
            summary_bytes += (
                cantidad_imagenes.to_bytes(1, byteorder="big")
                + self.SEPARADORES["CAMPO"]
                + cantidad_frames.to_bytes(1, byteorder="big")
                + self.SEPARADORES["CAMPO"]
                + cantidad_comentarios.to_bytes(1, byteorder="big")
                + self.SEPARADORES["CAMPO"]
                + self.SEPARADORES["GRUPO"]
            )
            # Finalizar con el separador de grupo
            append_bytes(summary_bytes, file_name)
        except Exception as e:
            mostrar_error(f"Error recuperando los metadatos del resumen: {e}")

    def _agregar_bloques(self, bloques: list, file_name: str) -> None:
        """
        Agrega toda la info encontrada de los sub bloques de metadatos al archivo como bytes.
        """
        try:
            bloques_bytes = bytearray()
            for bloque in bloques:
                for clave, valor in bloque.items():
                    clave_bytes = clave.encode("utf-8")
                    if isinstance(valor, bool):
                        tipo = "bool"
                        valor = b"1" if valor else b"0"
                    elif isinstance(valor, (int, float)):
                        tipo = "num"
                        valor = str(valor).encode("utf-8")
                    elif isinstance(valor, str):
                        tipo = "str"
                        valor = valor.encode("utf-8")
                    else:
                        continue  # Manejar otros tipos según sea necesario

                    # Agregar tipo y valor al bytearray
                    bloques_bytes += (
                        clave_bytes
                        + self.SEPARADORES["DIVISOR"]
                        + tipo.encode("utf-8")
                        + self.SEPARADORES["DIVISOR"]
                        + valor
                        + self.SEPARADORES["CAMPO"]
                    )

                bloques_bytes += self.SEPARADORES["SUBGRUPO"]
            bloques_bytes += self.SEPARADORES["GRUPO"]
            append_bytes(bloques_bytes, file_name)
        except Exception as e:
            mostrar_error(f"Error recuperando los metadatos de los bloques: {e}")

    def escribir(self, file_name: str = "config.bin") -> None:
        try:
            self._agregar_generic(file_name)
            # iteramos sobre el diccionario
            for element in self.data_dictionary["gifs"]:
                self._agregar_gif_generic(file_name, element)
                # guardamos las fechas
                metadatos = element["metadatos"]
                self._agregar_fechas(metadatos["fechas"], file_name)
                # guardamos el header
                bytes = bytearray()
                bytes += metadatos["header"].encode("utf-8") + self.SEPARADORES["GRUPO"]
                append_bytes(bytes, file_name)
                self._agregar_pantalla(metadatos["pantalla"], file_name)
                self._agregar_resumen(metadatos["resumen"], file_name)
                self._agregar_paleta_colores(
                    metadatos["paleta_global_colores"], file_name
                )
                self._agregar_bloques(metadatos["bloques"], file_name)
                append_bytes(
                    bytearray(self.SEPARADORES["SEGMENTO"]), file_name
                )  # fin de la lista de gifs
        except Exception as e:
            mostrar_error(f"Error inesperado: {e}")
#Utilis:
from typing import BinaryIO
from src.utils.manejador_errores import mostrar_error

import os


def read_n_bytes(steps: int, iterable_file: BinaryIO) -> bytearray:
    """
    Reads the specified number of bytes from the byte stream.

    :param steps: The number of bytes to read.
    :param byte_stream: The complete byte stream to read from.
    :return: A bytearray representing a segment of data.

    """
    current_segment = bytearray()
    for _ in range(steps):
        byte = iterable_file.read(1)
        if not byte:
            break
        current_segment.extend(byte)
    return current_segment


def read_till_byte(delimiter: bytes, iterable_file: BinaryIO) -> bytearray:
    """
    Reads the byte stream until the specified byte is encountered.

    :param delimiter: The byte to look for as a delimiter.
    :param byte_stream: The complete byte stream to read from.
    :return: A bytearray representing a segment of data.

    """
    current_segment = bytearray()  # To hold the current segment
    while True:  # Infinite loop
        byte = iterable_file.read(1)  # Read a byte
        if not byte or byte == delimiter:
            break
        current_segment.extend(byte)  # Append the byte to the current segment

    return current_segment  # Retornar el segmento leído


def extract_from_bytes(
    delimiter: bytes, bytes_array: bytearray, initial_position: int = 0
) -> bytearray:
    """
    Extracts the data from the byte stream until the specified delimiter is encountered.

    :param delimiter: The delimiter to look for in the byte stream.
    :param bytes_array: The byte stream to extract data from.
    :param initial_position: The starting position in the byte stream.
    :return: A bytearray containing the extracted data.
    """
    data_array = bytearray()  # To hold the extracted data
    try:
        position = initial_position
        while position < len(bytes_array):  # Iterate through the byte stream
            byte = bytes_array[position]
            if byte == delimiter[0]:  # Check if the byte is the delimiter
                break
            data_array.append(byte)  # Append the byte to the data array
            position += 1  # Move to the next byte
    except Exception as e:
        mostrar_error(f"Error al extraer datos del stream de bytes: {e}")
    finally:
        del bytes_array[: position + 1]
        return data_array


def append_bytes(bytes: bytearray, file_name: str) -> None:
    """
    Agrega los datos de un diccionario al archivo como bytes.
    """
    try:
        if not os.path.exists(file_name):
            with open(file_name, "wb") as file:
                pass
        with open(file_name, "ab") as file:
            file.write(bytes)
    except Exception as e:
        mostrar_error(f"No se han podido agregar los bytes al archivo: {e}")
"""
PROYECTO DE MANEJO E IMPLEMENTACIÓN DE ARCHIVOS, LECTURA DE METADATOS EN UN ARCHIVO GIF
REALIZADO POR DANIEL B. & CHRIS VILLEGAS

ARCHIVO PRINCIPAL, DONDE SE EJECUTA EL PROGRAMA
"""

# importar el configurador

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
        try:
            existe_archivo = self.configurador.existe_archivo()
            json_gifs = None
            path = "./"
            if not existe_archivo:
                path = self.seleccionar_path()
                if not path:
                    return
                json_gifs = self.configurador.configurar(path)
            else:
                json_gifs = self.configurador.obtener_config()
        except Exception as e:
            mostrar_error(f"Error inesperado: {e}")
            return

        mostrar_completado(json_gifs)


if __name__ == "__main__":
    main = Main()
    main.start()


