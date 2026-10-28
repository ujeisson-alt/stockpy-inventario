# utils.py
# Funciones auxiliares y de validación de entrada de StockPy Solutions.
# Todas las lecturas repiten la pregunta hasta recibir un valor válido.


def leer_entero(mensaje: str, minimo: int = None, maximo: int = None,
                permitir_vacio: bool = False):
    """Solicita un entero al usuario, repitiendo si el valor es inválido.

    Si permitir_vacio es True y el usuario presiona Enter, retorna None
    (útil para "mantener el valor actual" al editar).
    """
    while True:
        texto = input(mensaje).strip()
        if permitir_vacio and texto == "":
            return None
        try:
            valor = int(texto)
        except ValueError:
            print("Por favor ingresa un número entero válido.")
            continue
        if minimo is not None and valor < minimo:
            print(f"El valor debe ser al menos {minimo}. Intenta de nuevo.")
            continue
        if maximo is not None and valor > maximo:
            print(f"El valor debe ser máximo {maximo}. Intenta de nuevo.")
            continue
        return valor


def leer_flotante(mensaje: str, minimo: float = 0.01, permitir_vacio: bool = False):
    """Solicita un número decimal al usuario (acepta coma o punto decimal)."""
    while True:
        texto = input(mensaje).strip().replace(",", ".")
        if permitir_vacio and texto == "":
            return None
        try:
            valor = float(texto)
        except ValueError:
            print("Por favor ingresa un número válido (ej: 29.99).")
            continue
        if valor < minimo:
            print(f"El valor debe ser al menos {minimo}. Intenta de nuevo.")
            continue
        return round(valor, 2)  # máximo 2 decimales


def leer_texto(mensaje: str, max_len: int = 100) -> str:
    """Solicita un texto no vacío al usuario."""
    while True:
        texto = input(mensaje).strip()
        if not texto:
            print("El campo no puede estar vacío. Intenta de nuevo.")
            continue
        if len(texto) > max_len:
            print(f"El texto no puede superar {max_len} caracteres.")
            continue
        return texto


def confirmar(mensaje: str) -> bool:
    """Pide confirmación al usuario (s/n)."""
    respuesta = input(f"{mensaje} (s/n): ").strip().lower()
    return respuesta in ("s", "si", "sí", "y", "yes")


def mostrar_separador(char: str = "-", largo: int = 72) -> None:
    """Imprime una línea separadora visual."""
    print(char * largo)
