"""Personas del sistema: jerarquía Persona -> Estudiante / Docente."""

from oti.personas.docente import Docente
from oti.personas.estudiante import Estudiante
from oti.personas.persona import Persona

__all__ = ["Persona", "Estudiante", "Docente"]
