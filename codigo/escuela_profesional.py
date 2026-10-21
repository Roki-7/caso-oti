"""Escuela profesional."""

from registro_academico import RegistroAcademico


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
        # Atributos privados (-)
        self.__codigo = codigo
        self.__informacion_general = informacion_general
        self.__perfil_egresado = perfil_egresado
        self.__codigo_director = codigo_director
        self.__codigo_secretario_academico = codigo_secretario_academico

    # ---- Implementación del contrato abstracto --------------------------------

    @property
    def longitud_maxima_nombre(self) -> int:
        return 100  # valor asumido: el caso no lo indica

    def resumen(self) -> str:
        return (
            f"[Escuela profesional] {self.codigo} - {self.nombre} | "
            f"director: {self.codigo_director} | "
            f"secretario académico: {self.codigo_secretario_academico}"
        )

    # ---- Propiedades públicas (+) --------------------------------------------

    @property
    def codigo(self) -> str:
        return self.__codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        self.__codigo = valor

    @property
    def informacion_general(self) -> str:
        return self.__informacion_general

    @informacion_general.setter
    def informacion_general(self, valor: str) -> None:
        self.__informacion_general = valor

    @property
    def perfil_egresado(self) -> str:
        return self.__perfil_egresado

    @perfil_egresado.setter
    def perfil_egresado(self, valor: str) -> None:
        self.__perfil_egresado = valor

    @property
    def codigo_director(self) -> str:
        return self.__codigo_director

    @codigo_director.setter
    def codigo_director(self, valor: str) -> None:
        self.__codigo_director = valor

    @property
    def codigo_secretario_academico(self) -> str:
        return self.__codigo_secretario_academico

    @codigo_secretario_academico.setter
    def codigo_secretario_academico(self, valor: str) -> None:
        self.__codigo_secretario_academico = valor
