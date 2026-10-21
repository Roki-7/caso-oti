"""Funciones de validación que usan las clases para aplicar las reglas del caso."""

from decimal import Decimal


def validar_texto(valor: str, campo: str, longitud_maxima: int) -> str:
    """El texto no puede quedar vacío ni pasar de la longitud máxima."""
    limpio = valor.strip()
    if not limpio:
        raise ValueError(f"{campo}: no puede quedar vacío.")
    if len(limpio) > longitud_maxima:
        raise ValueError(
            f"{campo}: no puede pasar de {longitud_maxima} caracteres (tiene {len(limpio)})."
        )
    return limpio


def validar_entero(valor: int, campo: str, minimo: int, maximo: int | None = None) -> int:
    """El entero debe estar dentro del rango [minimo, maximo]."""
    if valor < minimo:
        raise ValueError(f"{campo}: no puede ser menor que {minimo} (se recibió {valor}).")
    if maximo is not None and valor > maximo:
        raise ValueError(f"{campo}: no puede ser mayor que {maximo} (se recibió {valor}).")
    return valor


def validar_decimal(
    valor,
    campo: str,
    minimo: int,
    maximo: int | None = None,
    minimo_inclusivo: bool = True,
    max_decimales: int | None = None,
) -> Decimal:
    """Valida un número con decimales y lo devuelve como Decimal.

    Se usa Decimal y no float porque solo con Decimal se puede contar con
    exactitud cuántos decimales tiene un número.
    """
    numero = Decimal(str(valor))
    if minimo_inclusivo and numero < minimo:
        raise ValueError(f"{campo}: no puede ser menor que {minimo} (se recibió {valor}).")
    if not minimo_inclusivo and numero <= minimo:
        raise ValueError(f"{campo}: debe ser mayor que {minimo} (se recibió {valor}).")
    if maximo is not None and numero > maximo:
        raise ValueError(f"{campo}: no puede ser mayor que {maximo} (se recibió {valor}).")
    if max_decimales is not None and numero.normalize().as_tuple().exponent < -max_decimales:
        raise ValueError(
            f"{campo}: admite como máximo {max_decimales} decimales (se recibió {valor})."
        )
    return numero


def validar_bandera(valor, campo: str) -> int:
    """Convierte True/False o 0/1 al entero 0/1 que se guarda internamente."""
    if valor not in (0, 1):
        raise ValueError(f"{campo}: solo admite 0/1 o True/False (se recibió {valor!r}).")
    return int(valor)


def validar_intervalo(inicio, fin, nombre_intervalo: str) -> None:
    """La fecha de fin no puede ser anterior a la de inicio."""
    if fin < inicio:
        raise ValueError(
            f"La fecha de fin del {nombre_intervalo} ({fin}) no puede ser anterior "
            f"a la de inicio ({inicio})."
        )
