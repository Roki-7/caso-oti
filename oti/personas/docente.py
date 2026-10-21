"""Docente: es una Persona."""

from oti.base.validaciones import validar_cadena
from oti.personas.persona import Persona


class Docente(Persona):
    """«del docente, su código de docente»."""

    def __init__(self, dni: str, nombres: str, apellidos: str, codigo_docente: str):
        super().__init__(dni, nombres, apellidos)
        self.codigo_docente = codigo_docente

    @property
    def rol(self) -> str:
        return "Docente"

    @property
    def codigo_docente(self) -> str:
        return self._codigo_docente

    @codigo_docente.setter
    def codigo_docente(self, valor: str) -> None:
        self._codigo_docente = validar_cadena(valor, "El código de docente")
