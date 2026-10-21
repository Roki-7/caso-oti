# Actividad 5: Implementación y prueba

## Implementación

Todas las clases están en el paquete `oti/`, organizadas por carpetas:

| Carpeta | Contenido |
|---|---|
| `oti/base/` | `RegistroAcademico` (abstracta) y `validaciones.py` (funciones de validación reutilizables) |
| `oti/enums/` | `EstadoPeriodo` |
| `oti/registros/` | `Curso`, `PlanEstudios`, `EscuelaProfesional`, `PeriodoAcademico` |
| `oti/matricula/` | `Seccion` |
| `oti/personas/` | `Persona` (abstracta), `Estudiante`, `Docente` |

## Programa de prueba

Archivo: `pruebas/programa_prueba.py`. Para cada regla muestra un dato **válido aceptado** y un dato **inválido rechazado**, capturando el error con `try/except`:

```python
def rechazado(descripcion, accion, error_esperado=(ValueError, TypeError)):
    try:
        accion()
    except error_esperado as error:
        print(f"   [RECHAZADO] {descripcion}\n               {type(error).__name__}: {error}")
    else:
        print(f"   [FALLO]     inválido aceptado sin error -> {descripcion}")
```

Ejecución:

```bash
python -m pruebas.programa_prueba
```

Resultado: **72/72 comprobaciones correctas**. La salida completa está en [`salida_programa_prueba.txt`](salida_programa_prueba.txt).

## Reglas probadas

| # | Clase | Regla | Válido aceptado | Inválido rechazado | Error |
|---|---|---|---|---|---|
| R01 | Curso | El id lo genera el sistema y no se cambia | Ids automáticos 1 y 2 | `curso.id = 99` | AttributeError |
| R02 | Curso | Nombre no vacío, máximo 200 | 200 caracteres | `"   "` y 201 caracteres | ValueError |
| R03 | Curso | Créditos mayores que 0 | 0.5 | 0 y −3 | ValueError |
| R04 | Curso | Créditos con hasta 2 decimales | 3.75 | 3.755 | ValueError |
| R05 | Curso | Horas de 0 a 255 | 0 y 255 | −1, 256 y 300 | ValueError |
| R06 | Curso | Horas totales calculadas | Total se actualiza al corregir una hora | `curso.horas_totales = 50` | AttributeError |
| R07 | Seccion | Vacantes mayores que 0 | 2 vacantes | 0 vacantes | ValueError |
| R08 | Seccion | Matriculados no se escriben | `matricular()` | `seccion.matriculados = 40` | AttributeError |
| R09 | Seccion | Sección llena rechaza matrícula | 2.ª matrícula de 2 | 3.ª matrícula | ValueError |
| R10 | Seccion | Matriculados solo bajan con retiro | `retirar()` con 1 matriculado | `retirar()` con 0 | ValueError |
| R11 | Seccion | Vacantes no menores que matriculados | Bajar de 5 a 3 con 3 matriculados | Bajar a 2 con 3 matriculados | ValueError |
| R12 | Seccion | Vacantes disponibles calculadas | 30 − 1 = 29 | `vacantes_disponibles = 100` | AttributeError |
| R13 | PlanEstudios | Nombre máximo 36 | 36 caracteres | 37 caracteres | ValueError |
| R14 | PlanEstudios | Créditos no negativos | Extracurriculares = 0 | Electivos = −5 | ValueError |
| R15 | PlanEstudios | Total = suma, no editable | 180 + 40 + 10 = 230 | `creditos_totales = 999` | AttributeError |
| R16 | PlanEstudios | 0/1 interno, bool externo | `vigente=1` → `True` | `vigente=2` | ValueError |
| R17 | Escuela | Nombre máximo 100 | «Ingeniería de Sistemas» | 101 caracteres | ValueError |
| R18 | Escuela | Director y secretario como código | DOC-001, DOC-002 | Código vacío | ValueError |
| R19 | Periodo | Nombre máximo 45 | 45 caracteres | 46 caracteres | ValueError |
| R20 | Periodo | Fin del periodo ≥ inicio | Mismo día | Termina antes de empezar | ValueError |
| R21 | Periodo | Fin de matrícula ≥ inicio | 3 al 14 de agosto | 14 al 3 de agosto | ValueError |
| R22 | Periodo | Fechas se cambian juntas | Mover mar–jul a ago–dic | Asignar `fecha_inicio` sola; `cambiar_fechas` inválido | AttributeError / ValueError |
| R23 | Periodo | Verano: 0/1 interno, bool externo | `True` → guarda 1 | `"si"` | ValueError |
| R24 | Periodo | Nota de 0 a 20 con decimales | 10.5 | 20.5 y −1 | ValueError |
| R25 | Periodo | Estado solo 1–4 | 2 y `EstadoPeriodo.FINALIZADO` | 7 | ValueError |
| R26 | Persona | No se registra «solo persona» | `Estudiante(...)` | `Persona(...)` | TypeError |
| R27 | Persona | Nombre completo calculado | Se actualiza al corregir nombres | `nombre_completo = "X"` | AttributeError |
| R28 | Persona | Rol distinto por subclase | «Estudiante» y «Docente» | Subclase sin `rol` | TypeError |
| R29 | RegistroAcademico | Clase abstracta con contrato | Curso implementa todo | `RegistroAcademico("X")` y subclase sin `resumen()` | TypeError |
| R30 | Todas | Polimorfismo sin `isinstance` | Resumen de los 4 tipos | — | — |

## Decisiones del equipo (no indicadas en el caso)

| Decisión | Motivo |
|---|---|
| Nombre de la escuela: máximo 100 caracteres | El caso pide validar el nombre de todas, pero no da el límite de la escuela |
| Id del curso con un contador interno | El caso solo dice que «el sistema genera» el id; un contador da ids legibles (1, 2, 3…) |
| `Decimal` para créditos y nota | Exactitud y conteo confiable de decimales |
| Fecha de fin igual a la de inicio es válida | El caso solo prohíbe que sea **anterior** |
| No se exige que la matrícula esté dentro del periodo | El caso no lo pide; se propone como mejora futura |
| No se valida el formato del DNI ni del código del curso | El caso no lo pide; solo se exige texto no vacío |
| Una sección nueva empieza con 0 matriculados | Los matriculados solo cambian con `matricular()` y `retirar()` |
