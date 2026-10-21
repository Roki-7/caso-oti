"""Persona: clase abstracta base de Estudiante y Docente."""

from abc import ABC, abstractmethod



class Persona(ABC):
    """Persona registrada en el sistema. No puede instanciarse.

    Reglas del caso:
    - «De toda persona registramos su DNI, sus nombres y sus apellidos, y a menudo
      necesitamos su nombre completo» -> `nombre_completo` se calcula.
    - «Cuando el sistema muestra a una persona, debe indicar qué rol cumple en la
      universidad, y esa respuesta es distinta para un estudiante y para un docente»
      -> `rol` es abstracto; cada subclase lo redefine.
    - «Nunca registramos a alguien que sea solo persona, sin ser estudiante ni
      docente» -> Persona es abstracta.
    """

    def __init__(self, dni: str, nombres: str, apellidos: str):
        # Atributos privados (-)
        self.__dni = dni
        self.__nombres = nombres
        self.__apellidos = apellidos

    @property
    @abstractmethod
    def rol(self) -> str:
        """Rol que la persona cumple en la universidad."""

    # ---- Propiedades públicas (+) --------------------------------------------

    @property
    def dni(self) -> str:
        return self.__dni

    @dni.setter
    def dni(self, valor: str) -> None:
        self.__dni = valor

    @property
    def nombres(self) -> str:
        return self.__nombres

    @nombres.setter
    def nombres(self, valor: str) -> None:
        self.__nombres = valor

    @property
    def apellidos(self) -> str:
        return self.__apellidos

    @apellidos.setter
    def apellidos(self, valor: str) -> None:
        self.__apellidos = valor

    @property
    def nombre_completo(self) -> str:
        """Se calcula: si cambian los nombres o apellidos, se actualiza solo."""
        return f"{self.nombres} {self.apellidos}"

    def __str__(self) -> str:
        # Método plantilla: usa self.rol, que cada subclase define a su manera.
        return f"{self.rol}: {self.nombre_completo} (DNI {self.dni})"
