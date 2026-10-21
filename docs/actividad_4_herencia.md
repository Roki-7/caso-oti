# Actividad 4: Herencia

## 4.1 Jerarquías de herencia

```
RegistroAcademico «abstract»              Persona «abstract»
 ├── Curso                                  ├── Estudiante
 ├── PlanEstudios                           └── Docente
 ├── EscuelaProfesional
 └── PeriodoAcademico
```

| Relación | Frase «X es un Y» |
|---|---|
| `Curso(RegistroAcademico)` | Un curso **es un** registro académico con nombre validado y resumen propio |
| `PlanEstudios(RegistroAcademico)` | Un plan de estudios **es un** registro académico con nombre validado y resumen propio |
| `EscuelaProfesional(RegistroAcademico)` | Una escuela profesional **es un** registro académico con nombre validado y resumen propio |
| `PeriodoAcademico(RegistroAcademico)` | Un periodo académico **es un** registro académico con nombre validado y resumen propio |
| `Estudiante(Persona)` | Un estudiante **es una** persona |
| `Docente(Persona)` | Un docente **es una** persona |

### Relaciones que NO son herencia

| Relación | Por qué no es herencia |
|---|---|
| Seccion → Curso | Una sección **no es un** curso: **pertenece a** un curso. Además, el caso no le da nombre a la sección, solo código, por eso no hereda de `RegistroAcademico`. |
| Seccion → PeriodoAcademico | La sección **se abre en** un periodo. |
| EscuelaProfesional → Docente | La escuela **tiene un** director y un secretario. |
| PlanEstudios → EscuelaProfesional | «Cada escuela tiene planes de estudio»: el plan **pertenece a** una escuela. |
| Estudiante → EscuelaProfesional | El estudiante **pertenece a** una escuela. |

Todas son asociaciones. Por la restricción del encargo («por ahora se guarda solo el código como texto»), se modelan como atributos `str` (`codigo_curso`, `codigo_director`, etc.) y no como flechas en el diagrama. Reemplazarlos por objetos queda para un laboratorio posterior.

## 4.2 Qué hereda, qué agrega y qué redefine cada subclase

| Subclase | Hereda | Agrega | Redefine |
|---|---|---|---|
| `Curso` | `__nombre`, propiedad `nombre` con su validación | `id`, `codigo`, `creditos`, las 4 horas, `horas_totales` | `longitud_maxima_nombre` (200), `resumen()` |
| `PlanEstudios` | `__nombre`, propiedad `nombre` | `anio_aprobacion`, `codigo_escuela`, los 3 créditos, `creditos_totales`, `vigente`, `es_nuevo` | `longitud_maxima_nombre` (36), `resumen()` |
| `EscuelaProfesional` | `__nombre`, propiedad `nombre` | `codigo`, `informacion_general`, `perfil_egresado`, `codigo_director`, `codigo_secretario_academico` | `longitud_maxima_nombre` (valor asumido: 100), `resumen()` |
| `PeriodoAcademico` | `__nombre`, propiedad `nombre` | `numero`, `anio`, las 4 fechas, `cambiar_fechas()`, `cambiar_fechas_matricula()`, `es_verano`, `nota_minima_aprobatoria`, `estado` | `longitud_maxima_nombre` (45), `resumen()` |
| `Estudiante` | `dni`, `nombres`, `apellidos`, `nombre_completo`, `__str__()` | `codigo_estudiante`, `codigo_escuela` | `rol` («Estudiante») |
| `Docente` | `dni`, `nombres`, `apellidos`, `nombre_completo`, `__str__()` | `codigo_docente` | `rol` («Docente») |

Todas las subclases llaman a `super().__init__(...)` para que la clase base inicialice y valide los datos comunes.

## 4.3 Polimorfismo

Se recorre una lista mixta pidiendo a cada objeto su resumen, **sin `isinstance` ni `type()`**. Cada objeto responde con su propia versión de `resumen()` (`main.py`):

```python
registros = [curso, plan, escuela, periodo]
for registro in registros:
    print(registro.resumen())
```

Salida:

```
[Curso #1] IS-282 - Programación Orientada a Objetos | 4.5 créditos | 6 h totales (T:2 P:4 S:0 V:0)
[Plan de estudios] Plan de estudios 2018 (2018) - escuela IS | 220 créditos (Oblig:180 Elect:30 Extra:10) | vigente
[Escuela profesional] IS - Ingeniería de Sistemas | director: DOC-001 | secretario académico: DOC-002
[Periodo académico] 2026-II - Segundo semestre académico 2026 | 2026-08-17 a 2026-12-18 | matrícula 2026-08-03 a 2026-08-14 | nota mínima 10.5 | estado EN_CURSO
```

Lo mismo ocurre con las personas: `Persona.__str__()` usa `self.rol`, y cada subclase da una respuesta distinta («Cuando el sistema muestra a una persona, debe indicar qué rol cumple»).

```python
for persona in [estudiante, docente]:
    print(persona)
```

```
Estudiante: Ana Lucía Quispe Huamán (DNI 70123456)
Docente: Luis Alberto Pérez Rojas (DNI 40123456)
```

**¿Por qué funciona?** El bucle solo conoce el contrato de la clase base («todo registro sabe dar su resumen»). Si mañana se agrega un nuevo tipo de registro, basta con que herede de `RegistroAcademico` e implemente `resumen()`: el bucle no cambia.
