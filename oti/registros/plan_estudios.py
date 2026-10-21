"""Plan de estudios de una escuela profesional."""

from decimal import Decimal

from oti.base.registro_academico import RegistroAcademico
from oti.base.validaciones import (
    validar_bandera,
    validar_decimal,
    validar_entero,
    validar_texto,
)


class PlanEstudios(RegistroAcademico):
    """Plan de estudios.

    Reglas del caso:
    - «identificados por un nombre de hasta 36 caracteres y por el año en que se aprobaron».
    - créditos obligatorios, electivos y extracurriculares: «ninguna puede ser negativa».
    - «El total de créditos del plan es la suma de las tres, y nunca debe poder
      editarse por separado» -> `creditos_totales` se calcula y no tiene setter.
    - «se guarda un 0 o un 1 ... que a quien lo consulte le responda simplemente
      verdadero o falso» -> `_vigente` y `_es_nuevo` son int; las propiedades devuelven bool.
    - Restricción del encargo: la escuela se referencia solo por su código (texto).
    """

    LONGITUD_MAXIMA_NOMBRE = 36

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
        self.anio_aprobacion = anio_aprobacion
        self.codigo_escuela = codigo_escuela
        self.creditos_obligatorios = creditos_obligatorios
        self.creditos_electivos = creditos_electivos
        self.creditos_extracurriculares = creditos_extracurriculares
        self.vigente = vigente
        self.es_nuevo = es_nuevo

    # ---- Implementación del contrato abstracto --------------------------------

    @property
    def longitud_maxima_nombre(self) -> int:
        return self.LONGITUD_MAXIMA_NOMBRE

    def resumen(self) -> str:
        estado = "vigente" if self.vigente else "no vigente"
        nuevo = ", nuevo" if self.es_nuevo else ""
        return (
            f"[Plan de estudios] {self.nombre} ({self.anio_aprobacion}) - escuela "
            f"{self.codigo_escuela} | {self.creditos_totales} créditos "
            f"(Oblig:{self.creditos_obligatorios} Elect:{self.creditos_electivos} "
            f"Extra:{self.creditos_extracurriculares}) | {estado}{nuevo}"
        )

    # ---- Identificación -------------------------------------------------------

    @property
    def anio_aprobacion(self) -> int:
        return self._anio_aprobacion

    @anio_aprobacion.setter
    def anio_aprobacion(self, valor: int) -> None:
        self._anio_aprobacion = validar_entero(valor, "El año de aprobación", minimo=1)

    @property
    def codigo_escuela(self) -> str:
        return self._codigo_escuela

    @codigo_escuela.setter
    def codigo_escuela(self, valor: str) -> None:
        self._codigo_escuela = validar_texto(valor, "El código de la escuela")

    # ---- Créditos (ninguno negativo) ------------------------------------------

    @staticmethod
    def _validar_creditos(valor, campo: str) -> Decimal:
        return validar_decimal(valor, campo, minimo=0)

    @property
    def creditos_obligatorios(self) -> Decimal:
        return self._creditos_obligatorios

    @creditos_obligatorios.setter
    def creditos_obligatorios(self, valor) -> None:
        self._creditos_obligatorios = self._validar_creditos(valor, "Los créditos obligatorios")

    @property
    def creditos_electivos(self) -> Decimal:
        return self._creditos_electivos

    @creditos_electivos.setter
    def creditos_electivos(self, valor) -> None:
        self._creditos_electivos = self._validar_creditos(valor, "Los créditos electivos")

    @property
    def creditos_extracurriculares(self) -> Decimal:
        return self._creditos_extracurriculares

    @creditos_extracurriculares.setter
    def creditos_extracurriculares(self, valor) -> None:
        self._creditos_extracurriculares = self._validar_creditos(
            valor, "Los créditos extracurriculares"
        )

    @property
    def creditos_totales(self) -> Decimal:
        """Suma de las tres partes. Sin setter: no puede editarse por separado."""
        return (
            self.creditos_obligatorios
            + self.creditos_electivos
            + self.creditos_extracurriculares
        )

    # ---- Banderas: se guardan como 0/1 y se entregan como bool ----------------

    @property
    def vigente(self) -> bool:
        return bool(self._vigente)

    @vigente.setter
    def vigente(self, valor: bool | int) -> None:
        self._vigente = validar_bandera(valor, "Vigente")

    @property
    def es_nuevo(self) -> bool:
        return bool(self._es_nuevo)

    @es_nuevo.setter
    def es_nuevo(self, valor: bool | int) -> None:
        self._es_nuevo = validar_bandera(valor, "Es nuevo")
