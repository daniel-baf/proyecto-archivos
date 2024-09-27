class GeneradorArchivoSecuencial:
    def __init__(self, custom_dict, separadores: dict = []):
        self.data_dictionary = custom_dict
        self.SEPARADORES = separadores

    def _agregar_fechas(self, bytes: bytearray, fechas: dict) -> None:
        """
        Agrega las fechas al archivo, la fecha es un número del timestamp.
        Si 'value' es un float, lo multiplica por 1000 para conservar mili segundos.
        """
        for key, value in fechas.items():
            # Convertir el valor de float a int, manteniendo mili segundos si es necesario
            timestamp = int(value * 1000) if isinstance(value, float) else int(value)
            # Calcular la longitud en bytes
            len_date = (timestamp.bit_length() + 7) // 8
            # Convertir el timestamp a bytes
            timestamp_bytes = timestamp.to_bytes(len_date, byteorder="big")
            # Agregar al bytearray
            bytes += timestamp_bytes + self.SEPARADORES["CAMPO"]
        # Finalizar con el separador de grupo
        bytes += self.SEPARADORES["GRUPO"]

    def _agregar_pantalla(self, bytes: bytearray, pantalla: dict) -> None:
        """
        Agrega los metadatos de la pantalla al archivo como bytes.
        """
        # Convertir y agregar el ancho
        ancho = int(pantalla["ancho"])
        bytes += (
            ancho.to_bytes(2, byteorder="big") + self.SEPARADORES["CAMPO"]
        )  # Suponiendo que el ancho usa 2 bytes
        # Convertir y agregar el alto
        alto = int(pantalla["alto"])
        bytes += (
            alto.to_bytes(2, byteorder="big") + self.SEPARADORES["CAMPO"]
        )  # Suponiendo que el alto usa 2 bytes
        # Convertir y agregar el valor booleano de 'paleta_global'
        paleta_global = 1 if pantalla["paleta_global"] else 0
        bytes += (
            paleta_global.to_bytes(1, byteorder="big") + self.SEPARADORES["CAMPO"]
        )  # Usando 1 byte para el booleano
        # Convertir y agregar el fondo
        fondo = int(pantalla["fondo"])
        bytes += (
            fondo.to_bytes(1, byteorder="big") + self.SEPARADORES["CAMPO"]
        )  # Suponiendo que el fondo usa 1 byte
        # Convertir y agregar la proporción de píxeles
        proporcion_pixeles = int(pantalla["proporcion_pixeles"])
        bytes += (
            proporcion_pixeles.to_bytes(1, byteorder="big") + self.SEPARADORES["CAMPO"]
        )  # Suponiendo que la proporción usa 1 byte
        # Convertir y agregar los bits de color
        bits_color = int(pantalla["bits_color"])
        bytes += (
            bits_color.to_bytes(1, byteorder="big") + self.SEPARADORES["CAMPO"]
        )  # Suponiendo que los bits de color usan 1 byte
        # Finalizar con el separador de grupo
        bytes += self.SEPARADORES["GRUPO"]

    def _agregar_paleta_colores(
        self, bytes: bytearray, paleta_global_colores: dict
    ) -> None:
        """
        Agrega los datos de la paleta global de colores al archivo como bytes.
        Maneja una cantidad de colores y una lista opcional de tuplas RGB.
        """
        # Convertir y agregar la cantidad de colores
        cantidad = int(paleta_global_colores["cantidad"])
        bytes += (
            cantidad.to_bytes(2, byteorder="big") + self.SEPARADORES["CAMPO"]
        )  # Suponiendo que la cantidad usa 2 bytes

        # Manejar el caso en que 'colores' sea null o una lista
        colores = paleta_global_colores.get("colores")

        if colores is None:
            # Si es null, simplemente no agregamos nada más o podríamos agregar un marcador especial.
            bytes += b"\x00"  # Usamos un byte 0x00 como marcador de "sin colores"
        else:
            bytes += b"\x01"  # Usamos un byte 0x00 como marcador de "sin colores"
            # Si hay colores, iteramos sobre la lista de tuplas RGB
            for rgb_tuple in colores:
                r, g, b = rgb_tuple
                # Cada color (R, G, B) ocupa 1 byte, así que agregamos los 3 bytes para cada color
                bytes += r.to_bytes(1, byteorder="big")
                bytes += g.to_bytes(1, byteorder="big")
                bytes += b.to_bytes(1, byteorder="big")
            bytes += self.SEPARADORES["CAMPO"]

        # Finalizar con el separador de grupo
        bytes += self.SEPARADORES["GRUPO"]

    def _agregar_resumen(self, bytes: bytearray, resumen: dict) -> None:
        """
        Agrega los datos del resumen al archivo como bytes.
        """
        # Convertir y agregar la cantidad de imágenes, frames y comentarios
        cantidad_imagenes = int(resumen["cantidad_imagenes"])
        cantidad_frames = int(resumen["cantidad_frames"])
        cantidad_comentarios = int(resumen["cantidad_comentarios"])

        bytes += (
            cantidad_imagenes.to_bytes(2, byteorder="big") + self.SEPARADORES["CAMPO"]
        )
        bytes += (
            cantidad_frames.to_bytes(2, byteorder="big") + self.SEPARADORES["CAMPO"]
        )
        bytes += (
            cantidad_comentarios.to_bytes(2, byteorder="big")
            + self.SEPARADORES["CAMPO"]
        )

        # Finalizar con el separador de grupo
        bytes += self.SEPARADORES["GRUPO"]

    def _agregar_bloques(self, bytes: bytearray, bloques: list) -> None:
        for bloque in bloques:
            for clave, valor in bloque.items():
                clave_bytes = clave.encode("utf-8")
                if isinstance(valor, (int, float)):
                    tipo = "num"
                    valor_bytes = str(valor).encode("utf-8")
                elif isinstance(valor, bool):
                    tipo = "bool"
                    valor_bytes = b"1" if valor else b"0"
                elif isinstance(valor, str):
                    tipo = "str"
                    valor_bytes = valor.encode("utf-8")
                else:
                    continue  # Manejar otros tipos según sea necesario

                # Agregar tipo y valor al bytearray
                bytes += (
                    clave_bytes
                    + self.SEPARADORES["CAMPO"]
                    + f"{tipo}:{valor}".encode("utf-8")
                    + self.SEPARADORES["CAMPO"]
                )

        bytes += self.SEPARADORES["GRUPO"]

    def escribir(self, file_name: str = "config.bin") -> None:
        try:
            bytes = bytearray()
            bytes += (
                self.data_dictionary["folder"].encode("utf-8")
                + self.SEPARADORES["SEGMENTO"]
            )

            # iteramos sobre el diccionario
            for element in self.data_dictionary["gifs"]:
                # abrimos el archivo en modo escritura
                bytes += element["path"].encode("utf-8") + self.SEPARADORES["GRUPO"]
                bytes += element["nombre"].encode("utf-8") + self.SEPARADORES["GRUPO"]
                # guardamos las fechas
                metadatos = element["metadatos"]
                self._agregar_fechas(bytes, metadatos["fechas"])
                # guardamos el header
                bytes += metadatos["header"].encode("utf-8") + self.SEPARADORES["GRUPO"]
                # guardamos la pantalla
                self._agregar_pantalla(bytes, metadatos["pantalla"])
                # guardamos la paleta de colores
                self._agregar_paleta_colores(bytes, metadatos["paleta_global_colores"])
                # guardamos el resumen
                self._agregar_resumen(bytes, metadatos["resumen"])
                # guardamos los bloques
                self._agregar_bloques(bytes, metadatos["bloques"])
                bytes += self.SEPARADORES["BLOQUE"]  # fin de cada gif
            bytes += self.SEPARADORES["SEGMENTO"]  # fin de gifs

            with open(file_name, "wb") as file:
                file.write(bytes)
        except Exception as e:
            print(f"Error inesperado: {e}")
            return
