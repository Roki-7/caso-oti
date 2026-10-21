"""Demostración del sistema OTI (Actividad 4.3: polimorfismo).

Ejecución:
    python main.py
"""

from datetime import date

from oti import (
    Curso,
    Docente,
    EscuelaProfesional,
    EstadoPeriodo,
    Estudiante,
    PeriodoAcademico,
    PlanEstudios,
    Seccion,
)


def crear_registros() -> list:
    """Crea un registro de cada tipo y los devuelve mezclados en una sola lista."""
    escuela = EscuelaProfesional(
        codigo="IS",
        nombre="Ingeniería de Sistemas",
        informacion_general="Escuela de la Facultad de Ingeniería.",
        perfil_egresado="Profesional que analiza, diseña e implementa sistemas de información.",
        codigo_director="DOC-001",
        codigo_secretario_academico="DOC-002",
    )
    plan = PlanEstudios(
        nombre="Plan de estudios 2018",
        anio_aprobacion=2018,
        creditos_obligatorios=180,
        creditos_electivos=30,
        creditos_extracurriculares=10,
        vigente=1,   # así llega de la base de datos
        es_nuevo=0,
    )
    curso = Curso(
        codigo="IS-282",
        nombre="Programación Orientada a Objetos",
        creditos="4.5",
        horas_teoricas=2,
        horas_practicas=4,
    )
    periodo = PeriodoAcademico(
        nombre="Segundo semestre académico 2026",
        numero=2,
        anio=2026,
        fecha_inicio=date(2026, 8, 17),
        fecha_fin=date(2026, 12, 18),
        fecha_inicio_matricula=date(2026, 8, 3),
        fecha_fin_matricula=date(2026, 8, 14),
        nota_minima_aprobatoria="10.5",
        es_verano=0,
        estado=EstadoPeriodo.EN_CURSO,
    )
    return [curso, plan, escuela, periodo]


def main() -> None:
    print("=== Polimorfismo: lista mixta de registros académicos ===")
    # No se pregunta el tipo de cada registro (no hay isinstance ni type()):
    # cada objeto responde resumen() con su propia implementación.
    for registro in crear_registros():
        print(registro.resumen())

    print("\n=== Polimorfismo: lista mixta de personas ===")
    personas = [
        Estudiante("70123456", "Ana Lucía", "Quispe Huamán", "2020100", "IS"),
        Docente("40123456", "Luis Alberto", "Pérez Rojas", "DOC-001"),
    ]
    for persona in personas:
        print(persona)  # __str__ de Persona usa el rol que define cada subclase

    print("\n=== Sección: matrícula controlada ===")
    seccion = Seccion("IS282-A", "IS-282", "2026-II", vacantes=2)
    seccion.matricular()
    seccion.matricular()
    print(f"Sección {seccion.codigo}: {seccion.matriculados}/{seccion.vacantes} matriculados, {seccion.vacantes_disponibles} disponibles")
    try:
        seccion.matricular()
    except ValueError as error:
        print(f"Matrícula rechazada: {error}")


if __name__ == "__main__":
    main()
