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
