"""Plan de estudios de una escuela profesional."""

from decimal import Decimal

from registro_academico import RegistroAcademico
from validaciones import validar_bandera, validar_decimal


class PlanEstudios(RegistroAcademico):
    """Plan de estudios.

    Reglas del caso:
    - «Cada escuela tiene planes de estudio» -> el plan guarda el código de su escuela
      (restricción del encargo: las referencias se guardan solo como código de texto).
    - «identificados por un nombre de hasta 36 caracteres y por el año en que se aprobaron».
    - créditos obligatorios, electivos y extracurriculares: «ninguna puede ser negativa».
    - «El total de créditos del plan es la suma de las tres, y nunca debe poder
      editarse por separado» -> `creditos_totales` se calcula y no tiene setter.
    - «se guarda un 0 o un 1 ... que a quien lo consulte le responda simplemente
      verdadero o falso» -> `__vigente` y `__es_nuevo` son int; las propiedades devuelven bool.
    """

    def __init__(
        self,
        nombre: str,
        anio_aprobacion: int,
        codigo_escuela: str,
        creditos_obligatorios,
        creditos_electivos,
        creditos_extracurriculares,
        vigente: bool | int = True,
        es_nuevo: bool | int = False,
    ):
        super().__init__(nombre)
        # Atributos privados (-)
        self.__anio_aprobacion = anio_aprobacion
        self.__codigo_escuela = codigo_escuela
        self.__creditos_obligatorios = validar_decimal(creditos_obligatorios, "Los créditos obligatorios", minimo=0)
        self.__creditos_electivos = validar_decimal(creditos_electivos, "Los créditos electivos", minimo=0)
        self.__creditos_extracurriculares = validar_decimal(
            creditos_extracurriculares, "Los créditos extracurriculares", minimo=0
        )
        self.__vigente = validar_bandera(vigente, "Vigente")
        self.__es_nuevo = validar_bandera(es_nuevo, "Es nuevo")

    # ---- Implementación del contrato abstracto --------------------------------

    @property
    def longitud_maxima_nombre(self) -> int:
        return 36

    def resumen(self) -> str:
        estado = "vigente" if self.vigente else "no vigente"
        nuevo = ", nuevo" if self.es_nuevo else ""
        return (
            f"[Plan de estudios] {self.nombre} ({self.anio_aprobacion}) - escuela "
            f"{self.codigo_escuela} | "
            f"{self.creditos_totales} créditos "
            f"(Oblig:{self.creditos_obligatorios} Elect:{self.creditos_electivos} "
            f"Extra:{self.creditos_extracurriculares}) | {estado}{nuevo}"
        )

    # ---- Propiedades públicas (+): identificación ----------------------------

    @property
    def anio_aprobacion(self) -> int:
        return self.__anio_aprobacion

    @anio_aprobacion.setter
    def anio_aprobacion(self, valor: int) -> None:
        self.__anio_aprobacion = valor

    @property
    def codigo_escuela(self) -> str:
        return self.__codigo_escuela

    @codigo_escuela.setter
    def codigo_escuela(self, valor: str) -> None:
        self.__codigo_escuela = valor

    # ---- Propiedades públicas (+): créditos (ninguno negativo) ---------------

    @property
    def creditos_obligatorios(self) -> Decimal:
        return self.__creditos_obligatorios

    @creditos_obligatorios.setter
    def creditos_obligatorios(self, valor) -> None:
        self.__creditos_obligatorios = validar_decimal(valor, "Los créditos obligatorios", minimo=0)

    @property
    def creditos_electivos(self) -> Decimal:
        return self.__creditos_electivos

    @creditos_electivos.setter
    def creditos_electivos(self, valor) -> None:
        self.__creditos_electivos = validar_decimal(valor, "Los créditos electivos", minimo=0)

    @property
    def creditos_extracurriculares(self) -> Decimal:
        return self.__creditos_extracurriculares

    @creditos_extracurriculares.setter
    def creditos_extracurriculares(self, valor) -> None:
        self.__creditos_extracurriculares = validar_decimal(valor, "Los créditos extracurriculares", minimo=0)

    @property
    def creditos_totales(self) -> Decimal:
        """Suma de las tres partes. Sin setter: no puede editarse por separado."""
        return (
            self.creditos_obligatorios
            + self.creditos_electivos
            + self.creditos_extracurriculares
        )

    # ---- Propiedades públicas (+): se guardan como 0/1 y se entregan como bool ----

    @property
    def vigente(self) -> bool:
        return bool(self.__vigente)

    @vigente.setter
    def vigente(self, valor: bool | int) -> None:
        self.__vigente = validar_bandera(valor, "Vigente")

    @property
    def es_nuevo(self) -> bool:
        return bool(self.__es_nuevo)

    @es_nuevo.setter
    def es_nuevo(self, valor: bool | int) -> None:
        self.__es_nuevo = validar_bandera(valor, "Es nuevo")
