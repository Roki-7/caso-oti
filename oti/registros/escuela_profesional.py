"""Escuela profesional."""

from oti.base.registro_academico import RegistroAcademico
from oti.base.validaciones import validar_cadena


class EscuelaProfesional(RegistroAcademico):
    """Escuela profesional.

    Reglas del caso:
    - «Cada escuela profesional tiene un código, un nombre, una información general
      y un perfil del egresado».
    - «tiene un director y un secretario académico; por ahora basta con guardar el
      código del docente que ocupa cada cargo» -> se guardan códigos (texto), no objetos.

    El caso exige validar el nombre de la escuela («todos tienen un nombre que debe
    validarse») pero no indica su tamaño máximo; se asume 100 caracteres.
    """

    LONGITUD_MAXIMA_NOMBRE = 100  # valor asumido: el caso no lo indica

    def __init__(
        self,
        codigo: str,
        nombre: str,
        informacion_general: str,
        perfil_egresado: str,
        codigo_director: str,
        codigo_secretario_academico: str,
    ):
        super().__init__(nombre)
        self.codigo = codigo
        self.informacion_general = informacion_general
        self.perfil_egresado = perfil_egresado
        self.codigo_director = codigo_director
        self.codigo_secretario_academico = codigo_secretario_academico

    # ---- Implementación del contrato abstracto --------------------------------

    @property
    def longitud_maxima_nombre(self) -> int:
        return self.LONGITUD_MAXIMA_NOMBRE

    def resumen(self) -> str:
        return (
            f"[Escuela profesional] {self.codigo} - {self.nombre} | "
            f"director: {self.codigo_director} | "
            f"secretario académico: {self.codigo_secretario_academico}"
        )

    # ---- Propiedades ----------------------------------------------------------

    @property
    def codigo(self) -> str:
        return self.__codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        self.__codigo = validar_cadena(valor, "El código de la escuela")

    @property
    def informacion_general(self) -> str:
        return self.__informacion_general

    @informacion_general.setter
    def informacion_general(self, valor: str) -> None:
        self.__informacion_general = validar_cadena(valor, "La información general")

    @property
    def perfil_egresado(self) -> str:
        return self.__perfil_egresado

    @perfil_egresado.setter
    def perfil_egresado(self, valor: str) -> None:
        self.__perfil_egresado = validar_cadena(valor, "El perfil del egresado")

    @property
    def codigo_director(self) -> str:
        return self.__codigo_director

    @codigo_director.setter
    def codigo_director(self, valor: str) -> None:
        self.__codigo_director = validar_cadena(valor, "El código del director")

    @property
    def codigo_secretario_academico(self) -> str:
        return self.__codigo_secretario_academico

    @codigo_secretario_academico.setter
    def codigo_secretario_academico(self, valor: str) -> None:
        self.__codigo_secretario_academico = validar_cadena(
            valor, "El código del secretario académico"
        )
