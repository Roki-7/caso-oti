"""Periodo académico (por ejemplo, 2026-II)."""

from datetime import date
from decimal import Decimal

from oti.base.registro_academico import RegistroAcademico
from oti.base.validaciones import (
    validar_bandera,
    validar_decimal,
    validar_entero,
    validar_fecha,
    validar_intervalo,
)
from oti.enums.estado_periodo import EstadoPeriodo

_ROMANOS = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}


class PeriodoAcademico(RegistroAcademico):
    """Periodo académico.

    Reglas del caso:
    - «un nombre de hasta 45 caracteres, un número y un año».
    - «En ningún caso la fecha de fin puede ser anterior a la de inicio; como las
      dos fechas de cada intervalo dependen una de la otra, deben poder cambiarse
      juntas» -> las fechas son de solo lectura y cambian con `cambiar_fechas()`
      y `cambiar_fechas_matricula()`, que reciben inicio y fin a la vez.
    - «si es de verano, con el mismo 0 o 1 de los planes» -> int interno, bool afuera.
    - «la nota mínima aprobatoria, que va de 0 a 20 y puede tener decimales».
    - estado: 1 planificado, 2 en curso, 3 matrícula cerrada, 4 finalizado -> Enum.
    """

    LONGITUD_MAXIMA_NOMBRE = 45
    NOTA_MINIMA = 0
    NOTA_MAXIMA = 20

    def __init__(
        self,
        nombre: str,
        numero: int,
        anio: int,
        fecha_inicio: date,
        fecha_fin: date,
        fecha_inicio_matricula: date,
        fecha_fin_matricula: date,
        nota_minima_aprobatoria,
        es_verano: bool | int = False,
        estado: EstadoPeriodo | int = EstadoPeriodo.PLANIFICADO,
    ):
        super().__init__(nombre)
        self.numero = numero
        self.anio = anio
        self.cambiar_fechas(fecha_inicio, fecha_fin)
        self.cambiar_fechas_matricula(fecha_inicio_matricula, fecha_fin_matricula)
        self.nota_minima_aprobatoria = nota_minima_aprobatoria
        self.es_verano = es_verano
        self.estado = estado

    # ---- Implementación del contrato abstracto --------------------------------

    @property
    def longitud_maxima_nombre(self) -> int:
        return self.LONGITUD_MAXIMA_NOMBRE

    def resumen(self) -> str:
        verano = " (verano)" if self.es_verano else ""
        return (
            f"[Periodo académico] {self.codigo}{verano} - {self.nombre} | "
            f"{self.fecha_inicio} a {self.fecha_fin} | matrícula "
            f"{self.fecha_inicio_matricula} a {self.fecha_fin_matricula} | "
            f"nota mínima {self.nota_minima_aprobatoria} | {self.estado.descripcion}"
        )

    # ---- Identificación -------------------------------------------------------

    @property
    def numero(self) -> int:
        return self._numero

    @numero.setter
    def numero(self, valor: int) -> None:
        self._numero = validar_entero(valor, "El número del periodo", minimo=0)

    @property
    def anio(self) -> int:
        return self._anio

    @anio.setter
    def anio(self, valor: int) -> None:
        self._anio = validar_entero(valor, "El año del periodo", minimo=1)

    @property
    def codigo(self) -> str:
        """Denominación calculada a partir del año y el número, p. ej. '2026-II'."""
        return f"{self.anio}-{_ROMANOS.get(self.numero, str(self.numero))}"

    # ---- Fechas: solo lectura, se cambian de a dos ----------------------------

    @property
    def fecha_inicio(self) -> date:
        return self._fecha_inicio

    @property
    def fecha_fin(self) -> date:
        return self._fecha_fin

    @property
    def fecha_inicio_matricula(self) -> date:
        return self._fecha_inicio_matricula

    @property
    def fecha_fin_matricula(self) -> date:
        return self._fecha_fin_matricula

    def cambiar_fechas(self, inicio: date, fin: date) -> None:
        """Cambia juntas las fechas del periodo, validando que fin >= inicio."""
        inicio = validar_fecha(inicio, "La fecha de inicio del periodo")
        fin = validar_fecha(fin, "La fecha de fin del periodo")
        validar_intervalo(inicio, fin, "periodo")
        # Se asignan solo después de validar ambas: el objeto nunca queda a medias.
        self._fecha_inicio = inicio
        self._fecha_fin = fin

    def cambiar_fechas_matricula(self, inicio: date, fin: date) -> None:
        """Cambia juntas las fechas de matrícula, validando que fin >= inicio."""
        inicio = validar_fecha(inicio, "La fecha de inicio de matrícula")
        fin = validar_fecha(fin, "La fecha de fin de matrícula")
        validar_intervalo(inicio, fin, "intervalo de matrícula")
        self._fecha_inicio_matricula = inicio
        self._fecha_fin_matricula = fin

    # ---- Verano: 0/1 interno, bool externo ------------------------------------

    @property
    def es_verano(self) -> bool:
        return bool(self._es_verano)

    @es_verano.setter
    def es_verano(self, valor: bool | int) -> None:
        self._es_verano = validar_bandera(valor, "Es verano")

    # ---- Nota mínima aprobatoria ----------------------------------------------

    @property
    def nota_minima_aprobatoria(self) -> Decimal:
        return self._nota_minima_aprobatoria

    @nota_minima_aprobatoria.setter
    def nota_minima_aprobatoria(self, valor) -> None:
        self._nota_minima_aprobatoria = validar_decimal(
            valor,
            "La nota mínima aprobatoria",
            minimo=self.NOTA_MINIMA,
            maximo=self.NOTA_MAXIMA,
        )

    # ---- Estado ---------------------------------------------------------------

    @property
    def estado(self) -> EstadoPeriodo:
        return self._estado

    @estado.setter
    def estado(self, valor: EstadoPeriodo | int) -> None:
        if isinstance(valor, EstadoPeriodo):
            self._estado = valor
        else:
            # Acepta el número de la base de datos, pero solo si es 1, 2, 3 o 4.
            self._estado = EstadoPeriodo.desde_numero(valor)
