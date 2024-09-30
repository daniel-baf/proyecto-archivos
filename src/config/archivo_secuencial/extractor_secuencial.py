from typing import BinaryIO
from .utils.secuencial_utils import read_n_bytes, read_till_byte, extract_from_bytes
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

    def _leer_paleta_colores(self, metadata: dict, file: bytearray) -> None:
        """
        Extracts the global palette colors from the byte stream and adds them to the metadata dictionary.

        The function assumes that the global palette consists of a certain number of colors,
        and each color is represented by three bytes (RGB).
        """
        paleta_global = {}  # Diccionario para almacenar la paleta global
        try:
            cantidad = extract_from_bytes(self.SEPARADORES["CAMPO"], file)
            # almacenamos el valor
            paleta_global["cantidad"] = int.from_bytes(cantidad, byteorder="big")
            # vemos si hay varios colores
            # borramos el primer byte
            if bytes([file[0]]) == b"\x00":
                paleta_global["colores"] = None
                return

            # Hay listado de colores
            paleta_global["colores"] = []
            color_list = extract_from_bytes(self.SEPARADORES["GRUPO"], file)
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
            resumen["cantidad_imagenes"] = int.from_bytes(
                extract_from_bytes(self.SEPARADORES["CAMPO"], file), byteorder="big"
            )
            resumen["cantidad_frames"] = int.from_bytes(
                extract_from_bytes(self.SEPARADORES["CAMPO"], file), byteorder="big"
            )
            resumen["comentarios"] = int.from_bytes(
                extract_from_bytes(self.SEPARADORES["CAMPO"], file), byteorder="big"
            )
            # borramos un byte
            del file[0]
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
            while True:  # Mientras queden bytes de GIFs por leer
                gif_bytes = read_till_byte(self.SEPARADORES["SEGMENTO"], file)
                if len(gif_bytes) == 0:
                    break
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
                self._leer_paleta_colores(metadata, gif_bytes)
                self._leer_resumen(metadata, gif_bytes)  # Leer resumen del GIF
                self._leer_bloques(gif, gif_bytes)  # Leer bloques del GIF
                gif["metadatos"] = metadata
                self.data_dictionary["gifs"].append(gif)  # Agregar el GIF a la lista
            #     break

        return self.data_dictionary  # Retornar el diccionario de datos extraídos
