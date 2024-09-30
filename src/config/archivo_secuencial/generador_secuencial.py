from .utils.secuencial_utils import append_bytes
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
