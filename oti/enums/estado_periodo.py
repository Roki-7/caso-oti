"""Estado del periodo académico como enumeración.

Frase del caso: «cada periodo tiene un estado que hoy se guarda como un número:
1 es planificado, 2 en curso, 3 matrícula cerrada y 4 finalizado. Nadie recuerda
qué significa cada número, y ya hemos visto periodos con estado 7.»

Con un Enum solo existen los cuatro valores válidos: EstadoPeriodo(7) lanza
ValueError, y el código se lee con nombres (EstadoPeriodo.EN_CURSO) en vez de
números mágicos.
"""

from enum import Enum


class EstadoPeriodo(Enum):
    PLANIFICADO = 1
    EN_CURSO = 2
    MATRICULA_CERRADA = 3
    FINALIZADO = 4

    @property
    def descripcion(self) -> str:
        """Texto legible del estado, para mostrar al usuario."""
        return {
            1: "Planificado",
            2: "En curso",
            3: "Matrícula cerrada",
            4: "Finalizado",
        }[self.value]

    @classmethod
    def desde_numero(cls, numero: int) -> "EstadoPeriodo":
        """Convierte el número guardado en la base de datos al estado correspondiente."""
        if isinstance(numero, bool) or not isinstance(numero, int):
            raise TypeError(f"El estado debe ser un número entero, se recibió {numero!r}.")
        try:
            return cls(numero)
        except ValueError:
            permitidos = ", ".join(f"{e.value}={e.descripcion}" for e in cls)
            raise ValueError(
                f"Estado de periodo inválido: {numero}. Valores permitidos: {permitidos}."
            ) from None
