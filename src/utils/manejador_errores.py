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
