"""Sistema de la OTI: modelo de clases que protege la información académica.

Paquetes:
    base       -> clase abstracta RegistroAcademico y funciones de validación
    enums      -> EstadoPeriodo
    registros  -> Curso, PlanEstudios, EscuelaProfesional, PeriodoAcademico
    matricula  -> Seccion
    personas   -> Persona (abstracta), Estudiante, Docente
"""

from oti.base import RegistroAcademico
from oti.enums import EstadoPeriodo
from oti.matricula import Seccion
from oti.personas import Docente, Estudiante, Persona
from oti.registros import Curso, EscuelaProfesional, PeriodoAcademico, PlanEstudios

__all__ = [
    "RegistroAcademico",
    "EstadoPeriodo",
    "Curso",
    "PlanEstudios",
    "EscuelaProfesional",
    "PeriodoAcademico",
    "Seccion",
    "Persona",
    "Estudiante",
    "Docente",
]
