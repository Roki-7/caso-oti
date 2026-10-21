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
