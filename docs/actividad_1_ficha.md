# Actividad 1: Identificación de clases, atributos y métodos

Convención: clases en `PascalCase`; atributos, métodos y propiedades en `snake_case`; atributos protegidos con prefijo `_` (PEP 8). Las «propiedades» son `@property`.

---

## RegistroAcademico (abstracta)

| Atributos (tipo) | Métodos y propiedades |
|---|---|
| `_nombre` (str) | `nombre` (propiedad get/set, valida no vacío y longitud máxima) |
| | `longitud_maxima_nombre` (propiedad **abstracta**, int) |
| | `resumen()` (método **abstracto**, str) |

**Justificación:** «Cursos, planes de estudio, escuelas y periodos son cosas muy distintas, pero todos tienen un nombre que debe validarse, aunque el tamaño máximo cambie en cada caso. Además, queremos que el sistema pueda recorrer una lista con todos ellos mezclados y pedirle a cada uno un resumen de sí mismo».

---

## Curso (hereda de RegistroAcademico)

| Atributos (tipo) | Métodos y propiedades |
|---|---|
| `_id` (int) | `id` (propiedad solo lectura) |
| `_codigo` (str) | `codigo` (get/set) |
| `_nombre` (str, heredado) | `creditos` (get/set: > 0, máx. 2 decimales) |
| `_creditos` (Decimal) | `horas_teoricas`, `horas_practicas`, `horas_seminario`, `horas_virtuales` (get/set: 0–255) |
| `_horas_teoricas` (int) | `horas_totales` (propiedad **calculada**) |
| `_horas_practicas` (int) | `longitud_maxima_nombre` → 200 |
| `_horas_seminario` (int) | `resumen()` |
| `_horas_virtuales` (int) | |

**Justificación:**
- «Cada curso tiene un identificador único que el sistema genera al registrarlo y que nadie puede cambiar después» → `id` sin setter.
- «un código, como IS-282, y un nombre que no puede quedar vacío ni pasar de 200 caracteres».
- «otorga una cantidad de créditos, que siempre es mayor que cero y puede tener hasta dos decimales» → `Decimal`.
- «horas teóricas, prácticas, de seminario y virtuales; ninguna de esas horas puede ser negativa ni pasar de 255».
- «Muchas veces nos piden las horas totales del curso, pero no queremos guardarlas» → `horas_totales` calculada.

---

## Seccion

| Atributos (tipo) | Métodos y propiedades |
|---|---|
| `_codigo` (str) | `codigo`, `codigo_curso`, `codigo_periodo` (get/set) |
| `_codigo_curso` (str) | `vacantes` (get/set: > 0 y ≥ matriculados) |
| `_codigo_periodo` (str) | `matriculados` (propiedad **solo lectura**) |
| `_vacantes` (int) | `vacantes_disponibles` (propiedad **calculada**) |
| `_matriculados` (int) | `matricular()`, `retirar()` |

**Justificación:**
- «Un curso del catálogo no tiene vacantes; las vacantes pertenecen a cada sección que abrimos en un periodo».
- «Una sección se identifica por su código, y sabemos a qué curso y a qué periodo corresponde por sus códigos».
- «Los matriculados nunca deben modificarse escribiendo un número directamente: solo aumentan cuando se matricula un estudiante y solo disminuyen cuando un estudiante se retira».
- «Si la sección está llena, la matrícula debe rechazarse».
- «Tampoco se puede reducir el número de vacantes por debajo de los que ya están matriculados».
- «Siempre queremos saber cuántas vacantes quedan disponibles».

---

## PlanEstudios (hereda de RegistroAcademico)

| Atributos (tipo) | Métodos y propiedades |
|---|---|
| `_nombre` (str, heredado) | `anio_aprobacion` (get/set) |
| `_anio_aprobacion` (int) | `creditos_obligatorios`, `creditos_electivos`, `creditos_extracurriculares` (get/set: ≥ 0) |
| `_creditos_obligatorios` (Decimal) | `creditos_totales` (propiedad **calculada**, sin setter) |
| `_creditos_electivos` (Decimal) | `vigente`, `es_nuevo` (get/set: guardan int, devuelven bool) |
| `_creditos_extracurriculares` (Decimal) | `longitud_maxima_nombre` → 36 |
| `_vigente` (int: 0/1) | `resumen()` |
| `_es_nuevo` (int: 0/1) | |

**Justificación:**
- «Cada escuela tiene planes de estudio, identificados por un nombre de hasta 36 caracteres y por el año en que se aprobaron».
- «Un plan exige una cantidad de créditos obligatorios, otra de créditos electivos y otra de créditos extracurriculares; ninguna puede ser negativa».
- «El total de créditos del plan es la suma de las tres, y nunca debe poder editarse por separado».
- «Queremos que el sistema conserve ese 0 o 1 internamente, pero que a quien lo consulte le responda simplemente verdadero o falso».

---

## EscuelaProfesional (hereda de RegistroAcademico)

| Atributos (tipo) | Métodos y propiedades |
|---|---|
| `_codigo` (str) | `codigo`, `informacion_general`, `perfil_egresado` (get/set) |
| `_nombre` (str, heredado) | `codigo_director`, `codigo_secretario_academico` (get/set) |
| `_informacion_general` (str) | `longitud_maxima_nombre` (el caso no da el número; se asume 100) |
| `_perfil_egresado` (str) | `resumen()` |
| `_codigo_director` (str) | |
| `_codigo_secretario_academico` (str) | |

**Justificación:**
- «Cada escuela profesional tiene un código, un nombre, una información general y un perfil del egresado».
- «Cada escuela tiene un director y un secretario académico; por ahora basta con guardar el código del docente que ocupa cada cargo».
- El caso exige validar el nombre de la escuela pero no indica su largo máximo; en el código se usa 100 caracteres.

---

## PeriodoAcademico (hereda de RegistroAcademico)

| Atributos (tipo) | Métodos y propiedades |
|---|---|
| `_nombre` (str, heredado) | `numero`, `anio` (get/set) |
| `_numero` (int) | `fecha_inicio`, `fecha_fin`, `fecha_inicio_matricula`, `fecha_fin_matricula` (solo lectura) |
| `_anio` (int) | `cambiar_fechas(inicio, fin)` |
| `_fecha_inicio` (date) | `cambiar_fechas_matricula(inicio, fin)` |
| `_fecha_fin` (date) | `es_verano` (get/set: guarda int, devuelve bool) |
| `_fecha_inicio_matricula` (date) | `nota_minima_aprobatoria` (get/set: 0–20) |
| `_fecha_fin_matricula` (date) | `estado` (get/set: acepta EstadoPeriodo o 1–4) |
| `_es_verano` (int: 0/1) | `longitud_maxima_nombre` → 45 |
| `_nota_minima_aprobatoria` (Decimal) | `resumen()` |
| `_estado` (EstadoPeriodo) | |

**Justificación:**
- «Cada periodo tiene un nombre de hasta 45 caracteres, un número y un año, por ejemplo el periodo 2026-II».
- «Tiene una fecha de inicio y una de fin, y además un intervalo de matrícula con su propia fecha de inicio y de fin».
- «En ningún caso la fecha de fin puede ser anterior a la de inicio; como las dos fechas de cada intervalo dependen una de la otra, deben poder cambiarse juntas».
- «El periodo indica también si es de verano, con el mismo 0 o 1 de los planes de estudio».
- «la nota mínima aprobatoria, que va de 0 a 20 y puede tener decimales».
- «cada periodo tiene un estado que hoy se guarda como un número».

---

## EstadoPeriodo (enumeración)

| Atributos (tipo) | Métodos y propiedades |
|---|---|
| `PLANIFICADO = 1` | — |
| `EN_CURSO = 2` | |
| `MATRICULA_CERRADA = 3` | |
| `FINALIZADO = 4` | |

**Justificación:** «1 es planificado, 2 en curso, 3 matrícula cerrada y 4 finalizado. Nadie recuerda qué significa cada número, y ya hemos visto periodos con estado 7».

---

## Persona (abstracta)

| Atributos (tipo) | Métodos y propiedades |
|---|---|
| `_dni` (str) | `dni`, `nombres`, `apellidos` (get/set) |
| `_nombres` (str) | `nombre_completo` (propiedad **calculada**) |
| `_apellidos` (str) | `rol` (propiedad **abstracta**) |
| | `__str__()` (muestra rol y nombre completo) |

**Justificación:**
- «De toda persona registramos su DNI, sus nombres y sus apellidos, y a menudo necesitamos su nombre completo».
- «Cuando el sistema muestra a una persona, debe indicar qué rol cumple en la universidad, y esa respuesta es distinta para un estudiante y para un docente».
- «Nunca registramos a alguien que sea solo persona, sin ser estudiante ni docente» → abstracta.

---

## Estudiante (hereda de Persona)

| Atributos (tipo) | Métodos y propiedades |
|---|---|
| `_codigo_estudiante` (str) | `codigo_estudiante`, `codigo_escuela` (get/set) |
| `_codigo_escuela` (str) | `rol` → «Estudiante» |

**Justificación:** «Del estudiante guardamos además su código de estudiante y el código de la escuela a la que pertenece».

---

## Docente (hereda de Persona)

| Atributos (tipo) | Métodos y propiedades |
|---|---|
| `_codigo_docente` (str) | `codigo_docente` (get/set) |
| | `rol` → «Docente» |

**Justificación:** «del docente, su código de docente».
