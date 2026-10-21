"""Funciones de validación reutilizables.

Todas las clases del sistema validan sus datos con estas funciones, de modo
que cada regla se escribe una sola vez y los mensajes de error son uniformes.
"""

from datetime import date, datetime
from decimal import Decimal, InvalidOperation


def validar_texto(valor, campo: str, longitud_maxima: int | None = None) -> str:
    """Valida un texto obligatorio (no vacío) con longitud máxima opcional."""
    if not isinstance(valor, str):
        raise TypeError(f"{campo}: debe ser texto (str), se recibió {type(valor).__name__}.")
    limpio = valor.strip()
    if not limpio:
        raise ValueError(f"{campo}: no puede quedar vacío.")
    if longitud_maxima is not None and len(limpio) > longitud_maxima:
        raise ValueError(
            f"{campo}: no puede pasar de {longitud_maxima} caracteres (tiene {len(limpio)})."
        )
    return limpio


def validar_cadena(valor, campo: str) -> str:
    """Valida solo que el dato sea texto (str). Se usa donde el caso no impone otra regla."""
    if not isinstance(valor, str):
        raise TypeError(f"{campo}: debe ser texto (str), se recibió {type(valor).__name__}.")
    return valor.strip()


def validar_entero(valor, campo: str, minimo: int | None = None, maximo: int | None = None) -> int:
    """Valida un número entero dentro de un rango cerrado [minimo, maximo]."""
    # bool es subclase de int en Python: True pasaría como 1, así que se rechaza.
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise TypeError(f"{campo}: debe ser un número entero, se recibió {valor!r}.")
    if minimo is not None and valor < minimo:
        raise ValueError(f"{campo}: no puede ser menor que {minimo} (se recibió {valor}).")
    if maximo is not None and valor > maximo:
        raise ValueError(f"{campo}: no puede ser mayor que {maximo} (se recibió {valor}).")
    return valor


def validar_decimal(
    valor,
    campo: str,
    minimo: Decimal | int | None = None,
    maximo: Decimal | int | None = None,
    minimo_inclusivo: bool = True,
    max_decimales: int | None = None,
) -> Decimal:
    """Valida un número con decimales y lo devuelve como Decimal.

    Se usa Decimal y no float porque 0.1 + 0.2 != 0.3 en float, y porque solo
    con Decimal se puede contar con exactitud cuántos decimales tiene un número.
    """
    if isinstance(valor, bool) or not isinstance(valor, (int, float, str, Decimal)):
        raise TypeError(f"{campo}: debe ser numérico, se recibió {valor!r}.")
    try:
        # str() evita arrastrar el error binario del float: Decimal(0.1) != Decimal("0.1")
        numero = Decimal(str(valor))
    except InvalidOperation:
        raise ValueError(f"{campo}: no es un número válido: {valor!r}.") from None
    if not numero.is_finite():
        raise ValueError(f"{campo}: debe ser un número finito, se recibió {valor!r}.")

    if minimo is not None:
        if minimo_inclusivo and numero < minimo:
            raise ValueError(f"{campo}: no puede ser menor que {minimo} (se recibió {valor}).")
        if not minimo_inclusivo and numero <= minimo:
            raise ValueError(f"{campo}: debe ser mayor que {minimo} (se recibió {valor}).")
    if maximo is not None and numero > maximo:
        raise ValueError(f"{campo}: no puede ser mayor que {maximo} (se recibió {valor}).")

    if max_decimales is not None:
        # normalize() quita ceros a la derecha: 3.50 -> 3.5, así "3.50" sí es válido.
        exponente = numero.normalize().as_tuple().exponent
        if exponente < -max_decimales:
            raise ValueError(
                f"{campo}: admite como máximo {max_decimales} decimales (se recibió {valor})."
            )
    return numero


def validar_bandera(valor, campo: str) -> int:
    """Convierte True/False o 0/1 al entero 0/1 que se guarda internamente."""
    if isinstance(valor, bool):
        return int(valor)
    if isinstance(valor, int) and valor in (0, 1):
        return valor
    raise ValueError(f"{campo}: solo admite 0/1 o True/False (se recibió {valor!r}).")


def validar_fecha(valor, campo: str) -> date:
    """Valida que el valor sea una fecha (datetime.date)."""
    if isinstance(valor, datetime):
        return valor.date()
    if not isinstance(valor, date):
        raise TypeError(f"{campo}: debe ser una fecha (datetime.date), se recibió {valor!r}.")
    return valor


def validar_intervalo(inicio: date, fin: date, nombre_intervalo: str) -> None:
    """Regla del caso: «En ningún caso la fecha de fin puede ser anterior a la de inicio»."""
    if fin < inicio:
        raise ValueError(
            f"La fecha de fin del {nombre_intervalo} ({fin}) no puede ser anterior "
            f"a la de inicio ({inicio})."
        )
