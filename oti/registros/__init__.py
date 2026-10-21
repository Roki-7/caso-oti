"""Registros académicos con nombre validado (subclases de RegistroAcademico)."""

from oti.registros.curso import Curso
from oti.registros.escuela_profesional import EscuelaProfesional
from oti.registros.periodo_academico import PeriodoAcademico
from oti.registros.plan_estudios import PlanEstudios

__all__ = ["Curso", "PlanEstudios", "EscuelaProfesional", "PeriodoAcademico"]
