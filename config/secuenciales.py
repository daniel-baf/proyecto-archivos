"""
    DANIEL EDUARDO BAUTISTA FUENTES
    2121323

    CREACION, MANEJO Y OPERACIONES CON ARCHIVOS APILADOS

    ESTRUCTURA DEL ARCHIVO
    LEN FECHA 1byte EDAD 3bytes NIT LEN EMIAL LEN NOMBRE 
        ... REPITE ...
            LEN FECHA

"""

from os import path
from datetime import datetime


# BLOQUE SEPARA ELEMENTOS QUE TENGAN ALGO EN COMUN, SEGMENTO SEPARA ELEMENTOS QUE NO TIENEN NADA EN COMUN
SEPARADORES = {"SEGMENTO": "$".encode("UTF-8"), "BLOQUE": ">".encode("utf-8")}
FILE_NAME = "secuencial.bin"


# limpia la consola
def clear_screen():
    print("\033c", end="")


# enter para continuar
def esperar_enter(message=""):
    input(f"\n{message}\n\tPresione enter para continuar...")


# crea un archivo y escribe su texto
def escribir_bytes(nombre_archivo: str, bytes: bytearray, append=False):
    mode = "ab" if append else "wb"
    with open(nombre_archivo, mode) as file:
        file.write(bytes)


# configura el archivo para mostrar siempre al inicio del archivo la ultima fecha de modificacion
def configurar_archivo_secuencial(filename):
    try:
        # Obtener el timestamp como entero
        timestamp = int(datetime.now().timestamp())
        len_date = (
            timestamp.bit_length() + 7
        ) // 8  # Calcula los bytes necesarios para almacenar el entero
        timestamp_bytes = timestamp.to_bytes(len_date, byteorder="big")

        bytes_array = timestamp_bytes + SEPARADORES["SEGMENTO"]

        if not path.exists(filename):
            # Si el archivo no existe, lo crea con el contenido inicial
            escribir_bytes(filename, bytes_array)
        else:
            # Si el archivo existe, se modifica el primer byte y los siguientes bytes con los nuevos datos
            with open(filename, "r+b") as archivo:
                archivo.seek(0)  # Va al inicio del archivo
                archivo.write(bytes_array)  # Sobrescribe con los nuevos datos
    except Exception as e:
        esperar_enter("ERROR AL CONFIGURAR EL ARCHIVO")


# lee el archivo e imprime la información
def obtener_archivo(filename):
    try:
        data = {}
        with open(filename, "rb") as file:
            timestamp = recuperar_fecha_modificacion(file)
            data["timestamp"] = datetime.fromtimestamp(timestamp)
            while segment := manejar_segmento_archivo(file):
                print(
                    f"{'-'*40}\n\tNombre: {segment['nombre']}\n\tEdad: {segment['edad']}\n\tNIT: {segment['nit']}\n\tEmail: {segment['email']}"
                )
        esperar_enter()
    except Exception as e:
        esperar_enter("NO SE PUDO IMPRIMIR EL ARCHIVO " + str(e))


# recupera valores de un archivo hasta encontrar un separador de bloque || segmento
def buscar_hasta_separador(file, separador):
    try:
        bytes = bytearray()
        while True:
            byte = file.read(1)
            if byte == separador or byte == b"":
                break
            bytes += byte

        return bytes
    except Exception as e:
        esperar_enter(f"NO SE PUDO BUSCAR EL SEPARADOR {e}")
        return None


# lee hasta encontrar el separador de segmento y retorna la fecha de modificacion
def recuperar_fecha_modificacion(file):
    try:
        bytes = buscar_hasta_separador(file, SEPARADORES["SEGMENTO"])
        timestamp = int.from_bytes(bytes)  # fecha
        return timestamp
    except Exception as e:
        esperar_enter(f"NO SE PUDO RECUPERAR LA FECHA DE MODIFICACION")
        return 0


# funcion que retorna un JSON con los datos de un segmento de datos para el archivo apilado
def manejar_segmento_archivo(file):
    try:
        registro = {}
        # recuperar el nombre

        nombre = buscar_hasta_separador(file, SEPARADORES["BLOQUE"])
        if nombre == b"":
            return {}

        registro["nombre"] = nombre.decode("utf-8")  # nombre
        registro["edad"] = int.from_bytes(
            buscar_hasta_separador(file, SEPARADORES["BLOQUE"]), byteorder="big"
        )  # edad
        registro["nit"] = buscar_hasta_separador(file, SEPARADORES["BLOQUE"]).decode(
            "utf-8"
        )  # nit
        registro["email"] = buscar_hasta_separador(
            file, SEPARADORES["SEGMENTO"]
        ).decode(
            "utf-8"
        )  # email
        return registro
    except Exception as e:
        esperar_enter(f"SEGMENTO INVALIDO {e}")
        return {}


# recibe la informacion para guardar en el archivo
def leer_datos(filename):
    datos = {}
    try:
        nombre = input("Nombre: ")
        edad = int(input("Edad: "))
        nit = input("NIT: ")
        # trim del nit para longitud de 10
        nit = nit[:8].strip() if len(nit) > 8 else nit
        email = input("E mail: ")

        # convertir numeros a bytes
        nombre = nombre.encode("utf-8")
        email = email.encode("utf-8")
        nit = nit.encode("utf-8")
        edad = edad.to_bytes(1, byteorder="big")
        datos = {"nombre": nombre, "edad": edad, "nit": nit, "email": email}
    except Exception as e:
        esperar_enter(f"DATOS INVALIDOS {e}")
    finally:
        if datos == {}:
            return  # no hacer nada
        bytes = bytearray()
        for key, value in datos.items():
            bytes += value + SEPARADORES["BLOQUE"]
        # replace the last separator with a segment separator
        bytes = bytes[:-1] + SEPARADORES["SEGMENTO"]
        configurar_archivo_secuencial(filename)
        escribir_bytes(filename, bytes, True)


def print_menu():
    print(f"--- MENU ---\n\t1. Ingresar datos\n\t2. Mostrar datos\n\t0. Salir\n")
    return int(input("Opcion: "))


def main():
    configurar_archivo_secuencial(FILE_NAME)

    option = -1
    while option != 0:
        clear_screen()
        option = print_menu()
        if option == 0:
            exit()
        elif option == 1:
            leer_datos(FILE_NAME)
        elif option == 2:
            self.imprimir_archivo(FILE_NAME)
            pass


if __name__ == "__main__":
    main()
