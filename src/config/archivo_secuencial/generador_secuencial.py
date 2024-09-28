import os


class GeneradorArchivoSecuencial:
    def __init__(self, custom_dict, separadores: dict = []):
        self.data_dictionary = custom_dict
        self.SEPARADORES = separadores

    def _append_bytes(self, bytes: bytearray, file_name: str) -> None:
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
            print(f"No se han podido agregar los bytes al archivo: {e}")

    def _agregar_genericos(self, file_name: str) -> None:
        """
        Agrega los datos genéricos al archivo como bytes.
        """
        try:
            bytes = bytearray()
            bytes += (
                self.data_dictionary["folder"].encode("utf-8")
                + self.SEPARADORES["SEGMENTO"]
            )
            self._append_bytes(bytes, file_name)
        except Exception as e:
            print(f"Error recuperando datos de configuracion: {e}")

    def _agregar_gif_path(self, file_name: str, gif: dict) -> None:
        """
        Agrega los datos de un gif al archivo como bytes. Agrega el path y el nombre del gif.
        """
        try:
            gif_generic_bytes = bytearray()
            gif_generic_bytes += gif["path"].encode("utf-8") + self.SEPARADORES["GRUPO"]
            gif_generic_bytes += (
                gif["nombre"].encode("utf-8") + self.SEPARADORES["GRUPO"]
            )
            self._append_bytes(gif_generic_bytes, file_name)
        except Exception as e:
            print(f"Error recuperando los metadatos genéricos del gif: {e}")

    def _agregar_fechas(self, fechas: dict, file_name: str) -> None:
        try:
            """
            Agrega las fechas al archivo, la fecha es un número del timestamp.
            Si 'value' es un float, lo multiplica por 1000 para conservar mili segundos.
            """
            fechas_bytes = bytearray()
            for key, value in fechas.items():
                # Convertir el valor de float a int, manteniendo mili segundos si es necesario
                timestamp = (
                    int(value * 1000) if isinstance(value, float) else int(value)
                )
                # Calcular la longitud en bytes
                len_date = (timestamp.bit_length() + 7) // 8
                # Convertir el timestamp a bytes
                timestamp_bytes = timestamp.to_bytes(len_date, byteorder="big")
                # Agregar al bytearray
                fechas_bytes += timestamp_bytes + self.SEPARADORES["CAMPO"]
            # Finalizar con el separador de grupo
            fechas_bytes += self.SEPARADORES["GRUPO"]
            self._append_bytes(fechas_bytes, file_name)
        except Exception as e:
            print(f"Error recuperando los metadatos de fechas: {e}")

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
            self._append_bytes(screen_bytes, file_name)
        except Exception as e:
            print(f"Error recuperando los metadatos de la pantalla: {e}")

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
            bytes_colores += (
                cantidad.to_bytes(2, byteorder="big") + self.SEPARADORES["CAMPO"]
            )  # Suponiendo que la cantidad usa 2 bytes

            # Manejar el caso en que 'colores' sea null o una lista
            colores = paleta_global_colores["colores"]

            if colores is None:
                # Si es null, simplemente no agregamos nada más o podríamos agregar un marcador especial.
                bytes_colores += (
                    b"\x00"  # Usamos un byte 0x00 como marcador de "sin colores"
                )
            else:
                bytes_colores += (
                    b"\x01"  # Usamos un byte 0x00 como marcador de "sin colores"
                )
                # Si hay colores, iteramos sobre la lista de tuplas RGB
                for rgb_tuple in colores:
                    r, g, b = rgb_tuple
                    # Cada color (R, G, B) ocupa 1 byte, así que agregamos los 3 bytes para cada color
                    bytes_colores += r.to_bytes(1, byteorder="big")
                    bytes_colores += g.to_bytes(1, byteorder="big")
                    bytes_colores += b.to_bytes(1, byteorder="big")
                bytes_colores += self.SEPARADORES["CAMPO"]

            # Finalizar con el separador de grupo
            bytes_colores += self.SEPARADORES["GRUPO"]
            self._append_bytes(bytes_colores, file_name)
        except Exception as e:
            print(f"Error recuperando los metadatos de la paleta de colores: {e}")

    def _agregar_resumen(self, resumen: dict, file_name: str) -> None:
        """
        Agrega los datos del resumen al archivo como bytes.
        """
        # Convertir y agregar la cantidad de imágenes, frames y comentarios
        cantidad_imagenes = int(resumen["cantidad_imagenes"])
        cantidad_frames = int(resumen["cantidad_frames"])
        cantidad_comentarios = int(resumen["cantidad_comentarios"])
        summary_bytes = bytearray()
        summary_bytes += (
            cantidad_imagenes.to_bytes(2, byteorder="big") + self.SEPARADORES["CAMPO"]
        )
        summary_bytes += (
            cantidad_frames.to_bytes(2, byteorder="big") + self.SEPARADORES["CAMPO"]
        )
        summary_bytes += (
            cantidad_comentarios.to_bytes(2, byteorder="big")
            + self.SEPARADORES["CAMPO"]
        )

        # Finalizar con el separador de grupo
        summary_bytes += self.SEPARADORES["GRUPO"]
        self._append_bytes(summary_bytes, file_name)

    def _agregar_bloques(self, bloques: list, file_name: str) -> None:
        try:
            bloques_bytes = bytearray()
            for bloque in bloques:
                for clave, valor in bloque.items():
                    clave_bytes = clave.encode("utf-8")
                    if isinstance(valor, (int, float)):
                        tipo = "num"
                        valor = str(valor).encode("utf-8")
                    elif isinstance(valor, bool):
                        tipo = "bool"
                        valor = b"1" if valor else b"0"
                    elif isinstance(valor, str):
                        tipo = "str"
                        valor = valor.encode("utf-8")
                    else:
                        continue  # Manejar otros tipos según sea necesario

                    # Agregar tipo y valor al bytearray
                    bloques_bytes += (
                        clave_bytes
                        + self.SEPARADORES["CAMPO"]
                        + f"{tipo}:{valor}".encode("utf-8")
                        + self.SEPARADORES["CAMPO"]
                    )

            bloques_bytes += self.SEPARADORES["GRUPO"]
            self._append_bytes(bloques_bytes, file_name)
        except Exception as e:
            print(f"Error recuperando los metadatos de los bloques: {e}")

    def escribir(self, file_name: str = "config.bin") -> None:
        try:
            self._agregar_genericos(file_name)
            # iteramos sobre el diccionario
            for element in self.data_dictionary["gifs"]:
                self._agregar_gif_path(file_name, element)
                # guardamos las fechas
                metadatos = element["metadatos"]
                self._agregar_fechas(metadatos["fechas"], file_name)
            # guardamos el header
            bytes = bytearray()
            bytes += metadatos["header"].encode("utf-8") + self.SEPARADORES["GRUPO"]
            self._append_bytes(bytes, file_name)
            self._agregar_pantalla(metadatos["pantalla"], file_name)
            self._agregar_paleta_colores(metadatos["paleta_global_colores"], file_name)
            self._agregar_resumen(metadatos["resumen"], file_name)
            self._agregar_bloques(metadatos["bloques"], file_name)
            # bytes += self.SEPARADORES["BLOQUE"]  # fin de cada gif
            self._append_bytes(
                self.SEPARADORES["SEGMENTO"], file_name
            )  # fin de la lista de gifs
        except Exception as e:
            print(f"Error inesperado: {e}")
