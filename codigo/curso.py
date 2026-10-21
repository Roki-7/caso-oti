"""Curso del catálogo universitario."""

from decimal import Decimal
from itertools import count

from registro_academico import RegistroAcademico
from validaciones import validar_decimal, validar_entero

# Contador del módulo que genera los ids de los cursos: 1, 2, 3...
_ids = count(1)


class Curso(RegistroAcademico):
    """Curso del catálogo. Un curso NO tiene vacantes: las vacantes son de cada Seccion.

    Reglas del caso:
    - «un identificador único que el sistema genera al registrarlo y que nadie
      puede cambiar después» -> `id` sin setter, generado por un contador.
    - «un nombre que no puede quedar vacío ni pasar de 200 caracteres».
    - «créditos, que siempre es mayor que cero y puede tener hasta dos decimales».
    - horas «ninguna puede ser negativa ni pasar de 255».
    - «Muchas veces nos piden las horas totales del curso, pero no queremos
      guardarlas» -> `horas_totales` se calcula.
    """

    def __init__(
        self,
        codigo: str,
        nombre: str,
        creditos,
        horas_teoricas: int = 0,
        horas_practicas: int = 0,
        horas_seminario: int = 0,
        horas_virtuales: int = 0,
    ):
        super().__init__(nombre)
        # Atributos privados (-)
        self.__codigo = codigo
        self.__creditos = validar_decimal(
            creditos, "Los créditos del curso", minimo=0, minimo_inclusivo=False, max_decimales=2
        )
        self.__horas_teoricas = validar_entero(horas_teoricas, "Las horas teóricas", minimo=0, maximo=255)
        self.__horas_practicas = validar_entero(horas_practicas, "Las horas prácticas", minimo=0, maximo=255)
        self.__horas_seminario = validar_entero(horas_seminario, "Las horas de seminario", minimo=0, maximo=255)
        self.__horas_virtuales = validar_entero(horas_virtuales, "Las horas virtuales", minimo=0, maximo=255)
        # El id se genera al final: si alguna validación falla, no se consume un número.
        self.__id = next(_ids)

    # ---- Implementación del contrato abstracto --------------------------------

    @property
    def longitud_maxima_nombre(self) -> int:
        return 200

    def resumen(self) -> str:
        return (
            f"[Curso #{self.id}] {self.codigo} - {self.nombre} | "
            f"{self.creditos} créditos | {self.horas_totales} h totales "
            f"(T:{self.horas_teoricas} P:{self.horas_practicas} "
            f"S:{self.horas_seminario} V:{self.horas_virtuales})"
        )

    # ---- Propiedades públicas (+): identificador de solo lectura -------------

    @property
    def id(self) -> int:
        """Identificador único generado por el sistema. No tiene setter."""
        return self.__id

    # ---- Propiedades públicas (+): código y créditos -------------------------

    @property
    def codigo(self) -> str:
        return self.__codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        self.__codigo = valor

    @property
    def creditos(self) -> Decimal:
        return self.__creditos

    @creditos.setter
    def creditos(self, valor) -> None:
        self.__creditos = validar_decimal(
            valor,
            "Los créditos del curso",
            minimo=0,
            minimo_inclusivo=False,  # «siempre es mayor que cero»
            max_decimales=2,
        )

    # ---- Propiedades públicas (+): horas (0 a 255 cada una) ------------------

    @property
    def horas_teoricas(self) -> int:
        return self.__horas_teoricas

    @horas_teoricas.setter
    def horas_teoricas(self, valor: int) -> None:
        self.__horas_teoricas = validar_entero(valor, "Las horas teóricas", minimo=0, maximo=255)

    @property
    def horas_practicas(self) -> int:
        return self.__horas_practicas

    @horas_practicas.setter
    def horas_practicas(self, valor: int) -> None:
        self.__horas_practicas = validar_entero(valor, "Las horas prácticas", minimo=0, maximo=255)

    @property
    def horas_seminario(self) -> int:
        return self.__horas_seminario

    @horas_seminario.setter
    def horas_seminario(self, valor: int) -> None:
        self.__horas_seminario = validar_entero(valor, "Las horas de seminario", minimo=0, maximo=255)

    @property
    def horas_virtuales(self) -> int:
        return self.__horas_virtuales

    @horas_virtuales.setter
    def horas_virtuales(self, valor: int) -> None:
        self.__horas_virtuales = validar_entero(valor, "Las horas virtuales", minimo=0, maximo=255)

    # ---- Propiedad pública (+) calculada -------------------------------------

    @property
    def horas_totales(self) -> int:
        """Se calcula en cada consulta: nunca puede quedar desactualizado."""
        return (
            self.horas_teoricas
            + self.horas_practicas
            + self.horas_seminario
            + self.horas_virtuales
        )
