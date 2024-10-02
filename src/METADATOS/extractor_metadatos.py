import struct
import os


class ExtractorMetadatos:
    # Diccionario global que contiene los separadores de bloques
    SEPARADORES_BLOQUES = {
        "imagen": b"\x2C",
        "bloque_inicial": b"\x21",
        "fin": b"\x3B",
        "control_grafico": b"\xF9",
        "comentario": b"\xFE",
    }

    # extrae los valores de la cabecera respecto a la resolución + retorna el empaquetado
    # de la pantalla lógica
    def _obtener_metadatos_resolucion(
        self, logical_screen_descriptor: bytearray
    ) -> dict:
        ancho, alto, packed, fondo, proporcion_pixeles = struct.unpack(
            "<HHBBB", logical_screen_descriptor
        )
        return {
            "ancho": ancho,
            "alto": alto,
            "paleta_global": bool(packed & 0b10000000),
            "fondo": fondo,
            "proporcion_pixeles": proporcion_pixeles,
            "bits_color": ((packed & 0b01110000) >> 4) + 1,  # Bits 4-6: bits por pixel
            "packed": packed,
        }

    def leer_paleta_global(self, file, packed: bytearray) -> dict:
        tamanio_paleta = 3 * (2 ** ((packed & 0b00000111) + 1))  # Tamaño de la paleta
        paleta_global = file.read(tamanio_paleta)
        return list(
            struct.iter_unpack("BBB", paleta_global)
        )  # Lista de datos ordenados (R, G, B)

    def leer_bloque_imagen(self, file) -> dict:
        imagen_descriptor = file.read(9)
        x_offset, y_offset, ancho_img, alto_img, packed_img = struct.unpack(
            "<HHHHB", imagen_descriptor
        )
        imagen_data = {
            "tipo": "imagen",
            "x_offset": x_offset,
            "y_offset": y_offset,
            "ancho_img": ancho_img,
            "alto_img": alto_img,
            "entrelazado": bool(
                packed_img & 0b01000000
            ),  # Bit 6: Indica si está entrelazado
        }

        # Leer datos comprimidos (LZW)
        tamanio_codigo_inicial = struct.unpack("B", file.read(1))[0]
        imagen_data["tamanio_codigo_lzw"] = tamanio_codigo_inicial

        total_datos_comprimidos = 0  # Variable para contar el tamaño total
        while True:
            tamanio_sub_bloque = struct.unpack("B", file.read(1))[0]
            if tamanio_sub_bloque == 0:
                break
            file.read(tamanio_sub_bloque)  # Leer pero no almacenar los datos
            total_datos_comprimidos += (
                tamanio_sub_bloque  # Contar el tamaño de cada sub bloque
            )

        # Guardamos solo el tamaño total de los datos comprimidos
        imagen_data["tamanio_total_datos_comprimidos"] = total_datos_comprimidos
        return imagen_data

    def leer_control_grafico(self, file) -> dict:
        file.read(1)  # Tamaño de la extensión
        packed_fields = struct.unpack("B", file.read(1))[0]
        delay_time = struct.unpack("<H", file.read(2))[
            0
        ]  # Retraso en centésimas de segundo
        color_transparente = struct.unpack("B", file.read(1))[0]
        file.read(1)  # Terminador de extensión

        return {
            "tipo": "control_grafico",
            "transparente": bool(packed_fields & 0b00000001),
            "disposicion": (packed_fields & 0b00011100) >> 2,  # Disposición de marco
            "tiempo_retraso": delay_time,
            "color_transparente": color_transparente,
        }

    def leer_comentario(self, file) -> dict:
        comentarios = []
        while True:
            tamanio_sub_bloque = struct.unpack("B", file.read(1))[0]
            if tamanio_sub_bloque == 0:
                break  # Fin del bloque de comentario
            comentarios.append(file.read(tamanio_sub_bloque))

        return b"".join(comentarios).decode(
            "ascii", errors="ignore"
        )  # Unir y decodificar los comentarios

    def extraer_metadatos(self, gif_path, append_colors=False) -> dict:
        metadatos = {}

        # Obtener fechas de creación y modificación
        info_archivo = os.stat(gif_path)
        metadatos["fechas"] = {
            "fecha_creado": info_archivo.st_ctime,
            "fecha_modificado": info_archivo.st_mtime,
        }

        with open(gif_path, "rb") as file:
            # Cabecera (6 bytes)
            metadatos["header"] = file.read(6).decode("ascii")  # Ej: GIF89a

            # Descripción de pantalla lógica (7 bytes)
            logical_screen_descriptor = file.read(7)
            metadatos["pantalla"] = self._obtener_metadatos_resolucion(
                logical_screen_descriptor
            )
            packed = metadatos["pantalla"]["packed"]
            del metadatos["pantalla"]["packed"]

            # Paleta global
            if metadatos["pantalla"]["paleta_global"]:
                metadatos["paleta_global_colores"] = self.leer_paleta_global(
                    file, packed
                )
                metadatos["paleta_global_colores"] = {
                    "cantidad": len(metadatos["paleta_global_colores"]),
                    # borrar la paleta global.colores si no se requiere
                    "colores": (
                        None
                        if not append_colors
                        else metadatos["paleta_global_colores"]
                    ),
                }

            bloques = []
            cantidad_imagenes = 0
            cantidad_frames = 0
            cantidad_comentarios = 0

            while True:
                bloque_inicial = file.read(1)
                if (
                    bloque_inicial == self.SEPARADORES_BLOQUES["fin"]
                ):  # Fin del archivo GIF
                    metadatos["fin"] = "Archivo terminado"
                    break
                elif (
                    bloque_inicial == self.SEPARADORES_BLOQUES["imagen"]
                ):  # Bloque de imagen
                    cantidad_imagenes += 1
                    bloques.append(self.leer_bloque_imagen(file))
                elif (
                    bloque_inicial == self.SEPARADORES_BLOQUES["bloque_inicial"]
                ):  # Extensiones
                    extension_label = file.read(1)
                    if extension_label == self.SEPARADORES_BLOQUES["control_grafico"]:
                        cantidad_frames += 1
                        bloques.append(self.leer_control_grafico(file))
                    elif extension_label == self.SEPARADORES_BLOQUES["comentario"]:
                        cantidad_comentarios += 1
                        comentario = self.leer_comentario(file)
                        bloques.append({"tipo": "comentario", "contenido": comentario})

            metadatos["bloques"] = bloques
            metadatos["resumen"] = {
                "cantidad_imagenes": cantidad_imagenes,
                "cantidad_frames": cantidad_frames,
                "cantidad_comentarios": cantidad_comentarios,
            }
        return metadatos
