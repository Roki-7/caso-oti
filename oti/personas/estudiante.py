"""Estudiante: es una Persona."""

from oti.base.validaciones import validar_cadena
from oti.personas.persona import Persona


class Estudiante(Persona):
    """«Del estudiante guardamos además su código de estudiante y el código de la
    escuela a la que pertenece»."""

    def __init__(
        self,
        dni: str,
        nombres: str,
        apellidos: str,
        codigo_estudiante: str,
        codigo_escuela: str,
    ):
        super().__init__(dni, nombres, apellidos)
        self.codigo_estudiante = codigo_estudiante
        self.codigo_escuela = codigo_escuela

    @property
    def rol(self) -> str:
        return "Estudiante"

    @property
    def codigo_estudiante(self) -> str:
        return self.__codigo_estudiante

    @codigo_estudiante.setter
    def codigo_estudiante(self, valor: str) -> None:
        self.__codigo_estudiante = validar_cadena(valor, "El código de estudiante")

    @property
    def codigo_escuela(self) -> str:
        return self.__codigo_escuela

    @codigo_escuela.setter
    def codigo_escuela(self, valor: str) -> None:
        self.__codigo_escuela = validar_cadena(valor, "El código de la escuela")
