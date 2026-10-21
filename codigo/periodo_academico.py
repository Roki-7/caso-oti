"""Periodo académico (por ejemplo, 2026-II)."""

from datetime import date
from decimal import Decimal

from registro_academico import RegistroAcademico
from estado_periodo import EstadoPeriodo
from validaciones import validar_bandera, validar_decimal, validar_intervalo


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
        validar_intervalo(fecha_inicio, fecha_fin, "periodo")
        validar_intervalo(fecha_inicio_matricula, fecha_fin_matricula, "intervalo de matrícula")
        # Atributos privados (-)
        self.__numero = numero
        self.__anio = anio
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = fecha_fin
        self.__fecha_inicio_matricula = fecha_inicio_matricula
        self.__fecha_fin_matricula = fecha_fin_matricula
        self.__es_verano = validar_bandera(es_verano, "Es verano")
        self.__nota_minima_aprobatoria = validar_decimal(
            nota_minima_aprobatoria, "La nota mínima aprobatoria", minimo=0, maximo=20
        )
        self.estado = estado  # la propiedad valida que sea 1, 2, 3 o 4 y guarda self.__estado

    # ---- Implementación del contrato abstracto --------------------------------

    @property
    def longitud_maxima_nombre(self) -> int:
        return 45

    def resumen(self) -> str:
        verano = " (verano)" if self.es_verano else ""
        return (
            f"[Periodo académico] {self.nombre}{verano} | "
            f"{self.fecha_inicio} a {self.fecha_fin} | matrícula "
            f"{self.fecha_inicio_matricula} a {self.fecha_fin_matricula} | "
            f"nota mínima {self.nota_minima_aprobatoria} | estado {self.estado.name}"
        )

    # ---- Propiedades públicas (+): identificación ----------------------------

    @property
    def numero(self) -> int:
        return self.__numero

    @numero.setter
    def numero(self, valor: int) -> None:
        self.__numero = valor

    @property
    def anio(self) -> int:
        return self.__anio

    @anio.setter
    def anio(self, valor: int) -> None:
        self.__anio = valor

    # ---- Propiedades públicas (+): fechas de solo lectura, se cambian de a dos ----

    @property
    def fecha_inicio(self) -> date:
        return self.__fecha_inicio

    @property
    def fecha_fin(self) -> date:
        return self.__fecha_fin

    @property
    def fecha_inicio_matricula(self) -> date:
        return self.__fecha_inicio_matricula

    @property
    def fecha_fin_matricula(self) -> date:
        return self.__fecha_fin_matricula

    def cambiar_fechas(self, inicio: date, fin: date) -> None:
        """Cambia juntas las fechas del periodo, validando que fin >= inicio."""
        validar_intervalo(inicio, fin, "periodo")
        # Se asignan solo después de validar ambas: el objeto nunca queda a medias.
        self.__fecha_inicio = inicio
        self.__fecha_fin = fin

    def cambiar_fechas_matricula(self, inicio: date, fin: date) -> None:
        """Cambia juntas las fechas de matrícula, validando que fin >= inicio."""
        validar_intervalo(inicio, fin, "intervalo de matrícula")
        self.__fecha_inicio_matricula = inicio
        self.__fecha_fin_matricula = fin

    # ---- Propiedad pública (+): verano, 0/1 interno y bool externo -----------

    @property
    def es_verano(self) -> bool:
        return bool(self.__es_verano)

    @es_verano.setter
    def es_verano(self, valor: bool | int) -> None:
        self.__es_verano = validar_bandera(valor, "Es verano")

    # ---- Propiedad pública (+): nota mínima aprobatoria ----------------------

    @property
    def nota_minima_aprobatoria(self) -> Decimal:
        return self.__nota_minima_aprobatoria

    @nota_minima_aprobatoria.setter
    def nota_minima_aprobatoria(self, valor) -> None:
        self.__nota_minima_aprobatoria = validar_decimal(
            valor,
            "La nota mínima aprobatoria",
            minimo=0,
            maximo=20,
        )

    # ---- Propiedad pública (+): estado ---------------------------------------

    @property
    def estado(self) -> EstadoPeriodo:
        return self.__estado

    @estado.setter
    def estado(self, valor: EstadoPeriodo | int) -> None:
        # Acepta EstadoPeriodo o el número de la base de datos, solo si es 1, 2, 3 o 4.
        try:
            self.__estado = EstadoPeriodo(valor)
        except ValueError:
            raise ValueError(
                f"El estado: solo puede ser 1 (planificado), 2 (en curso), "
                f"3 (matrícula cerrada) o 4 (finalizado); se recibió {valor}."
            ) from None
