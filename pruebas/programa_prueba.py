"""Actividad 5: programa de prueba.

Para cada regla del caso se muestra:
    1. un dato VÁLIDO que el sistema acepta, y
    2. un dato INVÁLIDO que el sistema rechaza, capturando el error con try/except.

Ejecución (desde la carpeta raíz del proyecto):
    python -m pruebas.programa_prueba
"""

import sys
from datetime import date
from pathlib import Path

# Permite ejecutar también con "python pruebas/programa_prueba.py".
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from oti import (  # noqa: E402
    Curso,
    Docente,
    EscuelaProfesional,
    EstadoPeriodo,
    Estudiante,
    PeriodoAcademico,
    Persona,
    PlanEstudios,
    RegistroAcademico,
    Seccion,
)

resultados = {"ok": 0, "fallo": 0}


# --------------------------------------------------------------------------- #
# Utilidades de la prueba
# --------------------------------------------------------------------------- #

def titulo(texto: str) -> None:
    print(f"\n{'=' * 78}\n{texto}\n{'=' * 78}")


def regla(codigo: str, descripcion: str) -> None:
    print(f"\n{codigo}. {descripcion}")


def aceptado(descripcion: str, accion) -> None:
    """Ejecuta un caso válido: debe funcionar sin lanzar error."""
    try:
        resultado = accion()
    except Exception as error:  # noqa: BLE001
        resultados["fallo"] += 1
        print(f"   [FALLO]     válido rechazado por error -> {descripcion}: {error}")
    else:
        resultados["ok"] += 1
        detalle = f" -> {resultado}" if resultado is not None else ""
        print(f"   [ACEPTADO]  {descripcion}{detalle}")


def rechazado(descripcion: str, accion, error_esperado=(ValueError, TypeError)) -> None:
    """Ejecuta un caso inválido: debe lanzar el error esperado."""
    try:
        accion()
    except error_esperado as error:
        resultados["ok"] += 1
        print(f"   [RECHAZADO] {descripcion}\n               {type(error).__name__}: {error}")
    else:
        resultados["fallo"] += 1
        print(f"   [FALLO]     inválido aceptado sin error -> {descripcion}")


# Datos de apoyo reutilizados por varias pruebas
def curso_valido(**cambios) -> Curso:
    datos = dict(codigo="IS-282", nombre="Programación Orientada a Objetos", creditos=4,
                 horas_teoricas=2, horas_practicas=4, horas_seminario=0, horas_virtuales=0)
    datos.update(cambios)
    return Curso(**datos)


def plan_valido(**cambios) -> PlanEstudios:
    datos = dict(nombre="Plan 2018", anio_aprobacion=2018, codigo_escuela="IS",
                 creditos_obligatorios=180, creditos_electivos=30,
                 creditos_extracurriculares=10, vigente=1, es_nuevo=0)
    datos.update(cambios)
    return PlanEstudios(**datos)


def escuela_valida(**cambios) -> EscuelaProfesional:
    datos = dict(codigo="IS", nombre="Ingeniería de Sistemas",
                 informacion_general="Escuela de la Facultad de Ingeniería.",
                 perfil_egresado="Profesional que diseña sistemas de información.",
                 codigo_director="DOC-001", codigo_secretario_academico="DOC-002")
    datos.update(cambios)
    return EscuelaProfesional(**datos)


def periodo_valido(**cambios) -> PeriodoAcademico:
    datos = dict(nombre="Segundo semestre académico 2026", numero=2, anio=2026,
                 fecha_inicio=date(2026, 8, 17), fecha_fin=date(2026, 12, 18),
                 fecha_inicio_matricula=date(2026, 8, 3),
                 fecha_fin_matricula=date(2026, 8, 14),
                 nota_minima_aprobatoria="10.5", es_verano=0,
                 estado=EstadoPeriodo.PLANIFICADO)
    datos.update(cambios)
    return PeriodoAcademico(**datos)


def asignar(objeto, atributo, valor):
    """Intenta asignar directamente un atributo (para probar los de solo lectura)."""
    setattr(objeto, atributo, valor)


# --------------------------------------------------------------------------- #
# CURSO
# --------------------------------------------------------------------------- #

def probar_curso() -> None:
    titulo("CURSO")

    regla("R01", "El id lo genera el sistema y nadie puede cambiarlo")
    c1, c2 = curso_valido(), curso_valido(codigo="IS-283")
    aceptado("dos cursos reciben ids distintos y automáticos",
             lambda: f"ids {c1.id} y {c2.id}")
    rechazado("curso.id = 99", lambda: asignar(c1, "id", 99), AttributeError)

    regla("R02", "El nombre no puede quedar vacío ni pasar de 200 caracteres")
    aceptado("nombre de 200 caracteres", lambda: len(curso_valido(nombre="A" * 200).nombre))
    rechazado("nombre vacío ('   ')", lambda: curso_valido(nombre="   "))
    rechazado("nombre de 201 caracteres", lambda: curso_valido(nombre="A" * 201))

    regla("R03", "Los créditos siempre son mayores que cero")
    aceptado("créditos = 0.5", lambda: curso_valido(creditos="0.5").creditos)
    rechazado("créditos = 0", lambda: curso_valido(creditos=0))
    rechazado("créditos = -3", lambda: curso_valido(creditos=-3))

    regla("R04", "Los créditos pueden tener hasta dos decimales")
    aceptado("créditos = 3.75", lambda: curso_valido(creditos="3.75").creditos)
    rechazado("créditos = 3.755", lambda: curso_valido(creditos="3.755"))

    regla("R05", "Ninguna hora puede ser negativa ni pasar de 255")
    aceptado("horas en los extremos 0 y 255",
             lambda: curso_valido(horas_teoricas=255, horas_virtuales=0).horas_teoricas)
    rechazado("horas prácticas = -1", lambda: curso_valido(horas_practicas=-1))
    rechazado("horas de seminario = 256", lambda: curso_valido(horas_seminario=256))
    c = curso_valido()
    rechazado("modificar horas virtuales a 300 en un curso existente",
              lambda: asignar(c, "horas_virtuales", 300))

    regla("R06", "Las horas totales se calculan, no se guardan")
    c = curso_valido()
    antes = c.horas_totales
    c.horas_teoricas = 3

    aceptado("al corregir una hora el total se actualiza solo",
             lambda: f"{antes} h -> {c.horas_totales} h")
    rechazado("curso.horas_totales = 50", lambda: asignar(c, "horas_totales", 50), AttributeError)


# --------------------------------------------------------------------------- #
# SECCIÓN
# --------------------------------------------------------------------------- #

def probar_seccion() -> None:
    titulo("SECCIÓN")

    regla("R07", "Las vacantes de una sección son mayores que cero")
    aceptado("sección con 2 vacantes",
             lambda: Seccion("IS282-A", "IS-282", "2026-II", 2).vacantes)
    rechazado("sección con 0 vacantes", lambda: Seccion("IS282-A", "IS-282", "2026-II", 0))

    regla("R08", "Los matriculados no se modifican escribiendo un número")
    s = Seccion("IS282-A", "IS-282", "2026-II", 2)
    s.matricular()
    aceptado("matricular() incrementa matriculados", lambda: s.matriculados)
    rechazado("seccion.matriculados = 40", lambda: asignar(s, "matriculados", 40),
              AttributeError)

    regla("R09", "Si la sección está llena, la matrícula se rechaza")
    s = Seccion("IS282-B", "IS-282", "2026-II", 2)
    s.matricular()
    aceptado("segunda matrícula en sección de 2 vacantes",
             lambda: (s.matricular(), f"{s.matriculados}/{s.vacantes}")[1])
    rechazado("tercera matrícula con la sección llena", s.matricular)

    regla("R10", "Los matriculados solo disminuyen cuando un estudiante se retira")
    s = Seccion("IS282-C", "IS-282", "2026-II", 3)
    s.matricular()
    aceptado("retirar() a un estudiante matriculado",
             lambda: (s.retirar(), f"quedan {s.matriculados}")[1])
    rechazado("retirar() de una sección sin matriculados", s.retirar)

    regla("R11", "No se pueden reducir las vacantes por debajo de los matriculados")
    s = Seccion("IS282-D", "IS-282", "2026-II", 5)
    for _ in range(3):
        s.matricular()
    aceptado("reducir de 5 a 3 vacantes con 3 matriculados",
             lambda: (asignar(s, "vacantes", 3), s.vacantes)[1])
    rechazado("reducir a 2 vacantes con 3 matriculados", lambda: asignar(s, "vacantes", 2))

    regla("R12", "Las vacantes disponibles se calculan")
    s = Seccion("IS282-E", "IS-282", "2026-II", 30)
    s.matricular()
    aceptado("30 vacantes y 1 matriculado", lambda: f"{s.vacantes_disponibles} disponibles")
    rechazado("seccion.vacantes_disponibles = 100",
              lambda: asignar(s, "vacantes_disponibles", 100), AttributeError)


# --------------------------------------------------------------------------- #
# PLAN DE ESTUDIOS
# --------------------------------------------------------------------------- #

def probar_plan() -> None:
    titulo("PLAN DE ESTUDIOS")

    regla("R13", "El nombre del plan tiene hasta 36 caracteres")
    aceptado("nombre de 36 caracteres", lambda: len(plan_valido(nombre="P" * 36).nombre))
    rechazado("nombre de 37 caracteres", lambda: plan_valido(nombre="P" * 37))

    regla("R14", "Ningún tipo de crédito del plan puede ser negativo")
    aceptado("créditos extracurriculares = 0",
             lambda: plan_valido(creditos_extracurriculares=0).creditos_extracurriculares)
    rechazado("créditos electivos = -5", lambda: plan_valido(creditos_electivos=-5))

    regla("R15", "El total es la suma de las tres partes y no se edita por separado")
    p = plan_valido()
    p.creditos_electivos = 40
    aceptado("total tras cambiar electivos de 30 a 40",
             lambda: f"{p.creditos_totales} = 180 + 40 + 10")
    rechazado("plan.creditos_totales = 999", lambda: asignar(p, "creditos_totales", 999),
              AttributeError)

    regla("R16", "Vigente / es nuevo: se guarda 0 o 1, se responde verdadero o falso")
    p = plan_valido(vigente=1, es_nuevo=False)
    aceptado("vigente=1 se guarda como int y se entrega como bool",
             lambda: f"interno {p._vigente!r} ({type(p._vigente).__name__}) -> "
                     f"externo {p.vigente!r} ({type(p.vigente).__name__})")
    rechazado("vigente = 2", lambda: plan_valido(vigente=2))


# --------------------------------------------------------------------------- #
# ESCUELA PROFESIONAL
# --------------------------------------------------------------------------- #

def probar_escuela() -> None:
    titulo("ESCUELA PROFESIONAL")

    regla("R17", "El nombre de la escuela se valida (máximo 100, decisión del equipo)")
    aceptado("nombre 'Ingeniería de Sistemas'", lambda: escuela_valida().nombre)
    rechazado("nombre de 101 caracteres", lambda: escuela_valida(nombre="E" * 101))

    regla("R18", "Director y secretario académico se guardan como código del docente")
    aceptado("códigos DOC-001 y DOC-002",
             lambda: (lambda e: f"{e.codigo_director}, {e.codigo_secretario_academico}")(
                 escuela_valida()))
    rechazado("código de director vacío", lambda: escuela_valida(codigo_director=""))


# --------------------------------------------------------------------------- #
# PERIODO ACADÉMICO
# --------------------------------------------------------------------------- #

def probar_periodo() -> None:
    titulo("PERIODO ACADÉMICO")

    regla("R19", "El nombre del periodo tiene hasta 45 caracteres")
    aceptado("nombre de 45 caracteres", lambda: len(periodo_valido(nombre="N" * 45).nombre))
    rechazado("nombre de 46 caracteres", lambda: periodo_valido(nombre="N" * 46))

    regla("R20", "La fecha de fin del periodo no puede ser anterior a la de inicio")
    aceptado("inicio y fin el mismo día (no es anterior)",
             lambda: periodo_valido(fecha_inicio=date(2026, 8, 17),
                                    fecha_fin=date(2026, 8, 17)).fecha_fin)
    rechazado("periodo que termina antes de empezar",
              lambda: periodo_valido(fecha_inicio=date(2026, 12, 18),
                                     fecha_fin=date(2026, 8, 17)))

    regla("R21", "La fecha de fin de matrícula no puede ser anterior a la de inicio")
    aceptado("matrícula del 3 al 14 de agosto",
             lambda: periodo_valido().fecha_fin_matricula)
    rechazado("matrícula del 14 al 3 de agosto",
              lambda: periodo_valido(fecha_inicio_matricula=date(2026, 8, 14),
                                     fecha_fin_matricula=date(2026, 8, 3)))

    regla("R22", "Las dos fechas de cada intervalo se cambian juntas")
    p = periodo_valido(fecha_inicio=date(2026, 3, 23), fecha_fin=date(2026, 7, 24))
    # Con setters separados este cambio fallaría: inicio 17/08 > fin 24/07 a mitad de camino.
    aceptado("mover el periodo de mar-jul a ago-dic con cambiar_fechas()",
             lambda: (p.cambiar_fechas(date(2026, 8, 17), date(2026, 12, 18)),
                      f"{p.fecha_inicio} a {p.fecha_fin}")[1])
    rechazado("periodo.fecha_inicio = ... (asignación individual)",
              lambda: asignar(p, "fecha_inicio", date(2026, 9, 1)), AttributeError)
    rechazado("cambiar_fechas() con fin anterior a inicio",
              lambda: p.cambiar_fechas(date(2026, 12, 18), date(2026, 8, 17)))
    aceptado("tras el rechazo el periodo conserva sus fechas",
             lambda: f"{p.fecha_inicio} a {p.fecha_fin}")

    regla("R23", "Es verano: se guarda 0 o 1, se responde verdadero o falso")
    p = periodo_valido(es_verano=True)
    aceptado("es_verano=True se guarda como 1 y se entrega como bool",
             lambda: f"interno {p._es_verano!r} -> externo {p.es_verano!r}")
    rechazado("es_verano = 'si'", lambda: periodo_valido(es_verano="si"))

    regla("R24", "La nota mínima aprobatoria va de 0 a 20 y puede tener decimales")
    aceptado("nota = 10.5", lambda: periodo_valido(nota_minima_aprobatoria=10.5)
             .nota_minima_aprobatoria)
    rechazado("nota = 20.5", lambda: periodo_valido(nota_minima_aprobatoria="20.5"))
    rechazado("nota = -1", lambda: periodo_valido(nota_minima_aprobatoria=-1))

    regla("R25", "El estado solo puede ser 1, 2, 3 o 4 (Enum EstadoPeriodo)")
    p = periodo_valido()
    aceptado("estado = 2 (número de la base de datos)",
             lambda: (asignar(p, "estado", 2), p.estado, p.estado.descripcion)[1:])
    aceptado("estado = EstadoPeriodo.FINALIZADO",
             lambda: (asignar(p, "estado", EstadoPeriodo.FINALIZADO), p.estado)[1])
    rechazado("estado = 7", lambda: asignar(p, "estado", 7))


# --------------------------------------------------------------------------- #
# PERSONAS
# --------------------------------------------------------------------------- #

def probar_personas() -> None:
    titulo("PERSONAS")

    regla("R26", "Nunca se registra a alguien que sea solo persona")
    aceptado("crear un Estudiante",
             lambda: type(Estudiante("70123456", "Ana", "Quispe Huamán", "2020100", "IS")).__name__)
    rechazado("Persona('70123456', 'Ana', 'Quispe')",
              lambda: Persona("70123456", "Ana", "Quispe"), TypeError)  # type: ignore[abstract]

    regla("R27", "El nombre completo se calcula a partir de nombres y apellidos")
    d = Docente("40123456", "Luis", "Pérez Rojas", "DOC-001")
    d.nombres = "Luis Alberto"
    aceptado("nombre completo tras corregir los nombres", lambda: d.nombre_completo)
    rechazado("docente.nombre_completo = 'X'", lambda: asignar(d, "nombre_completo", "X"),
              AttributeError)

    regla("R28", "El rol es distinto para un estudiante y para un docente")
    aceptado("rol del estudiante",
             lambda: Estudiante("70123456", "Ana", "Quispe", "2020100", "IS").rol)
    aceptado("rol del docente", lambda: Docente("40123456", "Luis", "Pérez", "DOC-001").rol)

    class PersonaSinRol(Persona):  # subclase que olvida definir rol
        pass

    rechazado("subclase de Persona que no define rol", lambda: PersonaSinRol("1", "A", "B"),
              TypeError)


# --------------------------------------------------------------------------- #
# ABSTRACCIÓN Y POLIMORFISMO
# --------------------------------------------------------------------------- #

def probar_abstraccion() -> None:
    titulo("ABSTRACCIÓN Y POLIMORFISMO")

    regla("R29", "RegistroAcademico es abstracto y obliga a implementar su contrato")
    aceptado("Curso implementa longitud_maxima_nombre y resumen()",
             lambda: curso_valido().longitud_maxima_nombre)
    rechazado("RegistroAcademico('X')", lambda: RegistroAcademico("X"), TypeError)

    class RegistroSinResumen(RegistroAcademico):  # define el límite, olvida resumen()
        @property
        def longitud_maxima_nombre(self) -> int:
            return 50

    rechazado("subclase que no implementa resumen()", lambda: RegistroSinResumen("X"),
              TypeError)

    regla("R30", "Recorrer una lista mixta pidiendo un resumen, sin isinstance")
    registros = [curso_valido(), plan_valido(), escuela_valida(), periodo_valido()]
    for registro in registros:
        aceptado(type(registro).__name__, registro.resumen)


# --------------------------------------------------------------------------- #

def main() -> int:
    print("PROGRAMA DE PRUEBA - CASO OTI")
    print("Cada regla muestra un dato válido aceptado y uno inválido rechazado.")

    probar_curso()
    probar_seccion()
    probar_plan()
    probar_escuela()
    probar_periodo()
    probar_personas()
    probar_abstraccion()

    total = resultados["ok"] + resultados["fallo"]
    titulo(f"RESULTADO: {resultados['ok']}/{total} comprobaciones correctas")
    return 0 if resultados["fallo"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
