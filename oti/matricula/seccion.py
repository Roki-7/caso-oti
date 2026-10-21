"""Sección de un curso abierta en un periodo."""

from oti.base.validaciones import validar_entero, validar_texto


class Seccion:
    """Sección de un curso en un periodo.

    No hereda de RegistroAcademico: el caso no le asigna nombre, sino código.
    Una sección NO «es un» curso: pertenece a un curso (asociación por código).

    Reglas del caso:
    - «Un curso del catálogo no tiene vacantes; las vacantes pertenecen a cada sección».
    - «sabemos a qué curso y a qué periodo corresponde por sus códigos».
    - «un número de vacantes mayor que cero».
    - «Los matriculados nunca deben modificarse escribiendo un número directamente:
      solo aumentan cuando se matricula un estudiante y solo disminuyen cuando un
      estudiante se retira» -> `matriculados` sin setter; `matricular()` y `retirar()`.
    - «Si la sección está llena, la matrícula debe rechazarse».
    - «Tampoco se puede reducir el número de vacantes por debajo de los que ya están
      matriculados».
    - «Siempre queremos saber cuántas vacantes quedan disponibles» -> calculado.
    """

    def __init__(self, codigo: str, codigo_curso: str, codigo_periodo: str, vacantes: int):
        self.codigo = codigo
        self.codigo_curso = codigo_curso
        self.codigo_periodo = codigo_periodo
        self._matriculados = 0  # toda sección nueva empieza sin matriculados
        self.vacantes = vacantes

    # ---- Códigos --------------------------------------------------------------

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        self._codigo = validar_texto(valor, "El código de la sección")

    @property
    def codigo_curso(self) -> str:
        return self._codigo_curso

    @codigo_curso.setter
    def codigo_curso(self, valor: str) -> None:
        self._codigo_curso = validar_texto(valor, "El código del curso")

    @property
    def codigo_periodo(self) -> str:
        return self._codigo_periodo

    @codigo_periodo.setter
    def codigo_periodo(self, valor: str) -> None:
        self._codigo_periodo = validar_texto(valor, "El código del periodo")

    # ---- Vacantes y matriculados ----------------------------------------------

    @property
    def vacantes(self) -> int:
        return self._vacantes

    @vacantes.setter
    def vacantes(self, valor: int) -> None:
        valor = validar_entero(valor, "Las vacantes", minimo=1)
        if valor < self._matriculados:
            raise ValueError(
                f"No se puede reducir las vacantes a {valor}: ya hay "
                f"{self._matriculados} estudiantes matriculados."
            )
        self._vacantes = valor

    @property
    def matriculados(self) -> int:
        """Solo lectura. Cambia únicamente con matricular() y retirar()."""
        return self._matriculados

    @property
    def vacantes_disponibles(self) -> int:
        """Se calcula en cada consulta."""
        return self.vacantes - self.matriculados

    @property
    def esta_llena(self) -> bool:
        return self.vacantes_disponibles == 0

    def matricular(self) -> None:
        """Registra la matrícula de un estudiante. Rechaza si la sección está llena."""
        if self.esta_llena:
            raise ValueError(
                f"La sección {self.codigo} está llena ({self.vacantes} vacantes ocupadas)."
            )
        self._matriculados += 1

    def retirar(self) -> None:
        """Registra el retiro de un estudiante. Rechaza si no hay matriculados."""
        if self._matriculados == 0:
            raise ValueError(f"La sección {self.codigo} no tiene estudiantes para retirar.")
        self._matriculados -= 1

    def __str__(self) -> str:
        return (
            f"[Sección] {self.codigo} - curso {self.codigo_curso}, periodo "
            f"{self.codigo_periodo} | {self.matriculados}/{self.vacantes} matriculados, "
            f"{self.vacantes_disponibles} disponibles"
        )
