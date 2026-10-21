"""Clase abstracta común a Curso, PlanEstudios, EscuelaProfesional y PeriodoAcademico.

Frase del caso que la origina:
    «Cursos, planes de estudio, escuelas y periodos son cosas muy distintas, pero
    todos tienen un nombre que debe validarse, aunque el tamaño máximo cambie en
    cada caso. Además, queremos que el sistema pueda recorrer una lista con todos
    ellos mezclados y pedirle a cada uno un resumen de sí mismo...»
"""

from abc import ABC, abstractmethod

from validaciones import validar_texto


class RegistroAcademico(ABC):
    """Registro académico con nombre validado. No puede instanciarse."""

    def __init__(self, nombre: str):
        self.nombre = nombre  # pasa por el setter, que valida

    # ---- Contrato que toda subclase está obligada a cumplir -------------------

    @property
    @abstractmethod
    def longitud_maxima_nombre(self) -> int:
        """Cantidad máxima de caracteres que admite el nombre en esta subclase."""

    @abstractmethod
    def resumen(self) -> str:
        """Descripción breve del registro (base del polimorfismo)."""

    # ---- Comportamiento común heredado por todas las subclases ----------------

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        # La validación se escribe UNA vez aquí; solo el límite cambia por subclase.
        self.__nombre = validar_texto(valor, "El nombre", self.longitud_maxima_nombre)
