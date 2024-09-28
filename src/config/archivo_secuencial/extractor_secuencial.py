class ExtractorSecuencial:
    def __init__(self, file_name: str, separadores: dict) -> None:
        self.file_name = file_name  # Nombre del archivo a leer
        self.data_dictionary = {
            "folder": "",
            "gifs": [],
        }  # Diccionario para almacenar datos extraídos
        self.SEPARADORES = separadores  # Separadores definidos para la lectura

    def _read_till_byte(self, delimiter: bytes, byte_stream: bytearray) -> bytearray:
        """
        Reads the byte stream until the specified byte is encountered.

        :param delimiter: The byte to look for as a delimiter.
        :param byte_stream: The complete byte stream to read from.
        :return: A bytearray representing a segment of data.
        """
        current_segment = bytearray()  # To hold the current segment
        index = 0  # Start from the beginning of the byte stream

        while index < len(byte_stream):  # Ensure we don't go out of bounds
            if (
                byte_stream[index : index + 1] == delimiter
            ):  # Check if the current byte matches the delimiter
                break  # Si se encuentra el delimitador, salir del bucle
            else:
                current_segment.append(byte_stream[index])  # Add to the current segment
            index += 1  # Move to the next byte

        # Update the byte_stream by slicing it to exclude the read segment and the delimiter
        byte_stream[:] = byte_stream[
            index + 1 :
        ]  # Actualizar el original byte_stream en su lugar

        return current_segment  # Retornar el segmento leído

    def _leer_fechas(self, bytes: bytearray, gif: dict) -> None:
        """
        Extracts the dates from the byte stream and adds them to the gif dictionary.
        """
        bytes_tmp = self._read_till_byte(
            self.SEPARADORES["GRUPO"], bytes
        )  # Leer hasta el grupo
        fecha = {}  # Diccionario para almacenar fechas
        # TODO save and recover float values
        fecha["fecha_creado"] = int.from_bytes(
            self._read_till_byte(self.SEPARADORES["CAMPO"], bytes_tmp), byteorder="big"
        )  # Leer fecha de creación
        fecha["fecha_modificado"] = int.from_bytes(
            self._read_till_byte(self.SEPARADORES["CAMPO"], bytes_tmp), byteorder="big"
        )  # Leer fecha de modificación
        gif["fechas"] = fecha  # Agregar fechas al diccionario gif

    def _leer_pantalla(self, bytes: bytearray, metadata: dict) -> None:
        pantalla = {}  # Diccionario para almacenar información de pantalla
        bytes_pantalla = self._read_till_byte(self.SEPARADORES["GRUPO"], bytes)

        # Leer propiedades de la pantalla
        ancho = int.from_bytes(
            self._read_till_byte(self.SEPARADORES["CAMPO"], bytes_pantalla),
            byteorder="big",
        )  # Leer ancho
        alto = int.from_bytes(
            self._read_till_byte(self.SEPARADORES["CAMPO"], bytes_pantalla),
            byteorder="big",
        )  # Leer alto
        paleta_global = (
            int.from_bytes(
                self._read_till_byte(self.SEPARADORES["CAMPO"], bytes_pantalla),
                byteorder="big",
            )
            == 1  # Verificar si la paleta global está presente
        )
        fondo = int.from_bytes(
            self._read_till_byte(self.SEPARADORES["CAMPO"], bytes_pantalla),
            byteorder="big",
        )  # Leer color de fondo
        proporcion_pixeles = int.from_bytes(
            self._read_till_byte(self.SEPARADORES["CAMPO"], bytes_pantalla),
            byteorder="big",
        )  # Leer proporción de píxeles
        bits_color = int.from_bytes(
            self._read_till_byte(self.SEPARADORES["CAMPO"], bytes_pantalla),
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

    def _leer_paleta_colores(self, bytes: bytearray, metadata: dict) -> None:
        """
        Extracts the global palette colors from the byte stream and adds them to the metadata dictionary.

        The function assumes that the global palette consists of a certain number of colors,
        and each color is represented by three bytes (RGB).
        """
        paleta_global = {}  # Diccionario para almacenar la paleta global
        # Número de colores en la paleta global, puedes cambiar este valor según tu necesidad
        cantidad = self._read_till_byte(self.SEPARADORES["CAMPO"], bytes)
        paleta_global["cantidad"] = int.from_bytes(
            cantidad, byteorder="big"
        )  # Por ejemplo, si hay 256 colores

        # Inicializa la lista para almacenar los colores
        colores = self._read_till_byte(self.SEPARADORES["CAMPO"], bytes)
        print(colores)

        # Check if the value is null and also if the first byte is equal to 0x01
        if (
            colores and colores[0] == 1
        ):  # Use `1` instead of `b"\x01"` for integer comparison
            paleta_global["colores"] = []
            # Read each color from the palette (RGB)
            color_bytes = self._read_till_byte(self.SEPARADORES["CAMPO"], bytes)

            # Read byte by byte and add color as [R, G, B]
            for index in range(0, len(color_bytes), 3):
                r = color_bytes[index]
                g = color_bytes[index + 1]
                b = color_bytes[index + 2]
                paleta_global["colores"].append((r, g, b))
        else:
            paleta_global["colores"] = None

        # Almacena la paleta global en el diccionario de metadatos
        metadata["paleta_global"] = paleta_global

    def _leer_metadatos(self, bytes: bytearray, gif: dict) -> tuple:
        metadatos = {}  # Diccionario para almacenar metadatos
        # get header
        metadatos["header"] = self._read_till_byte(
            self.SEPARADORES["GRUPO"], bytes
        ).decode(
            "utf-8"
        )  # Leer el encabezado
        # get pantalla
        self._leer_pantalla(bytes, metadatos)  # Leer información de la pantalla
        # get paleta colores
        self._leer_paleta_colores(bytes, metadatos)  # Leer paleta de colores

        while (len(bytes)) > 0:  # Mientras queden bytes por leer
            gif_group_byte = self._read_till_byte(
                self.SEPARADORES["GRUPO"], bytes
            )  # Leer grupo de GIF

        gif["metadatos"] = metadatos  # Agregar metadatos al diccionario gif

    def leer(self) -> dict:
        with open(self.file_name, "rb") as file:  # Abrir el archivo en modo binario
            bytes = bytearray(
                file.read()
            )  # Leer el contenido del archivo en un bytearray

        # Leer la carpeta
        self.data_dictionary["folder"] = self._read_till_byte(
            self.SEPARADORES["SEGMENTO"], bytes
        ).decode(
            "utf-8"
        )  # Leer el nombre de la carpeta

        gifs_bytes = self._read_till_byte(
            self.SEPARADORES["SEGMENTO"], bytes
        )  # Leer los bytes de los GIFs

        self.data_dictionary["gifs"] = []  # Inicializar la lista de GIFs

        # Leer los GIFs
        while len(gifs_bytes) > 0:  # Mientras queden bytes de GIFs por leer
            gif = {}  # Diccionario para un GIF
            gif_bytes = self._read_till_byte(
                self.SEPARADORES["BLOQUE"], gifs_bytes
            )  # Leer el bloque de GIF

            # leer nombre por bloque
            gif["path"] = self._read_till_byte(
                self.SEPARADORES["GRUPO"], gif_bytes
            ).decode(
                "utf-8"
            )  # Leer la ruta del GIF
            # get name
            gif["nombre"] = self._read_till_byte(
                self.SEPARADORES["GRUPO"], gif_bytes
            ).decode(
                "utf-8"
            )  # Leer el nombre del GIF
            # # get fecha
            # self._leer_fechas(gif_bytes, gif)  # Leer las fechas del GIF
            # # metadatos
            # self._leer_metadatos(gif_bytes, gif)  # Leer metadatos del GIF
            self.data_dictionary["gifs"].append(gif)  # Agregar el GIF a la lista

        return self.data_dictionary  # Retornar el diccionario de datos extraídos
