"""Curso del catálogo universitario."""

from decimal import Decimal

from oti.base.registro_academico import RegistroAcademico
from oti.base.validaciones import validar_cadena, validar_decimal, validar_entero


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

    LONGITUD_MAXIMA_NOMBRE = 200
    HORAS_MAXIMAS = 255  # máximo de un TINYINT UNSIGNED en la base de datos
    MAXIMO_DECIMALES_CREDITOS = 2

    _ultimo_id = 0  # contador compartido por todos los cursos (atributo de clase)

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
        self.codigo = codigo
        self.creditos = creditos
        self.horas_teoricas = horas_teoricas
        self.horas_practicas = horas_practicas
        self.horas_seminario = horas_seminario
        self.horas_virtuales = horas_virtuales
        # El id se genera al final: si alguna validación falla, no se consume un número.
        self._id = Curso._generar_id()

    @staticmethod
    def _generar_id() -> int:
        Curso._ultimo_id += 1
        return Curso._ultimo_id

    # ---- Implementación del contrato abstracto --------------------------------

    @property
    def longitud_maxima_nombre(self) -> int:
        return self.LONGITUD_MAXIMA_NOMBRE

    def resumen(self) -> str:
        return (
            f"[Curso #{self.id}] {self.codigo} - {self.nombre} | "
            f"{self.creditos} créditos | {self.horas_totales} h totales "
            f"(T:{self.horas_teoricas} P:{self.horas_practicas} "
            f"S:{self.horas_seminario} V:{self.horas_virtuales})"
        )

    # ---- Identificador: solo lectura ------------------------------------------

    @property
    def id(self) -> int:
        """Identificador único generado por el sistema. No tiene setter."""
        return self._id

    # ---- Código y créditos ----------------------------------------------------

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        self._codigo = validar_cadena(valor, "El código del curso")

    @property
    def creditos(self) -> Decimal:
        return self._creditos

    @creditos.setter
    def creditos(self, valor) -> None:
        self._creditos = validar_decimal(
            valor,
            "Los créditos del curso",
            minimo=0,
            minimo_inclusivo=False,  # «siempre es mayor que cero»
            max_decimales=self.MAXIMO_DECIMALES_CREDITOS,
        )

    # ---- Horas (0 a 255 cada una) ---------------------------------------------

    def _validar_horas(self, valor: int, campo: str) -> int:
        return validar_entero(valor, campo, minimo=0, maximo=self.HORAS_MAXIMAS)

    @property
    def horas_teoricas(self) -> int:
        return self._horas_teoricas

    @horas_teoricas.setter
    def horas_teoricas(self, valor: int) -> None:
        self._horas_teoricas = self._validar_horas(valor, "Las horas teóricas")

    @property
    def horas_practicas(self) -> int:
        return self._horas_practicas

    @horas_practicas.setter
    def horas_practicas(self, valor: int) -> None:
        self._horas_practicas = self._validar_horas(valor, "Las horas prácticas")

    @property
    def horas_seminario(self) -> int:
        return self._horas_seminario

    @horas_seminario.setter
    def horas_seminario(self, valor: int) -> None:
        self._horas_seminario = self._validar_horas(valor, "Las horas de seminario")

    @property
    def horas_virtuales(self) -> int:
        return self._horas_virtuales

    @horas_virtuales.setter
    def horas_virtuales(self, valor: int) -> None:
        self._horas_virtuales = self._validar_horas(valor, "Las horas virtuales")

    # ---- Dato calculado -------------------------------------------------------

    @property
    def horas_totales(self) -> int:
        """Se calcula en cada consulta: nunca puede quedar desactualizado."""
        return (
            self.horas_teoricas
            + self.horas_practicas
            + self.horas_seminario
            + self.horas_virtuales
        )
