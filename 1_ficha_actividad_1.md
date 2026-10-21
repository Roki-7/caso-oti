# Actividad 1: Identificación de clases, atributos y métodos

Convención: clases en `PascalCase`; atributos, métodos y propiedades en `snake_case`; atributos privados con doble guion bajo `__` (en Python esto activa el *name mangling*: el atributo queda oculto fuera de su clase). Las «propiedades» son `@property`.

---

## RegistroAcademico (abstracta)

| Atributos (tipo) | Métodos y propiedades |
|---|---|
| `__nombre` (str) | `nombre` (propiedad get/set, valida no vacío y longitud máxima) |
| | `longitud_maxima_nombre` (propiedad **abstracta**, int) |
| | `resumen()` (método **abstracto**, str) |

**Justificación:** «Cursos, planes de estudio, escuelas y periodos son cosas muy distintas, pero todos tienen un nombre que debe validarse, aunque el tamaño máximo cambie en cada caso. Además, queremos que el sistema pueda recorrer una lista con todos ellos mezclados y pedirle a cada uno un resumen de sí mismo».

---

## Curso (hereda de RegistroAcademico)

| Atributos (tipo) | Métodos y propiedades |
|---|---|
| `__id` (int) | `id` (propiedad solo lectura) |
| `__codigo` (str) | `codigo` (get/set) |
| *(`nombre`: propiedad heredada)* | `creditos` (get/set: > 0, máx. 2 decimales) |
| `__creditos` (Decimal) | `horas_teoricas`, `horas_practicas`, `horas_seminario`, `horas_virtuales` (get/set: 0–255) |
| `__horas_teoricas` (int) | `horas_totales` (propiedad **calculada**) |
| `__horas_practicas` (int) | `longitud_maxima_nombre` → 200 |
| `__horas_seminario` (int) | `resumen()` |
| `__horas_virtuales` (int) | |

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
| `__codigo` (str) | `codigo`, `codigo_curso`, `codigo_periodo` (get/set) |
| `__codigo_curso` (str) | `vacantes` (get/set: > 0 y ≥ matriculados) |
| `__codigo_periodo` (str) | `matriculados` (propiedad **solo lectura**) |
| `__vacantes` (int) | `vacantes_disponibles` (propiedad **calculada**) |
| `__matriculados` (int) | `matricular()`, `retirar()` |

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
| *(`nombre`: propiedad heredada)* | `anio_aprobacion`, `codigo_escuela` (get/set) |
| `__anio_aprobacion` (int) | `creditos_obligatorios`, `creditos_electivos`, `creditos_extracurriculares` (get/set: ≥ 0) |
| `__creditos_obligatorios` (Decimal) | `creditos_totales` (propiedad **calculada**, sin setter) |
| `__creditos_electivos` (Decimal) | `vigente`, `es_nuevo` (get/set: guardan int, devuelven bool) |
| `__creditos_extracurriculares` (Decimal) | `longitud_maxima_nombre` → 36 |
| `__vigente` (int: 0/1) | `resumen()` |
| `__es_nuevo` (int: 0/1) | |
| `__codigo_escuela` (str) | |

**Justificación:**
- «Cada escuela tiene planes de estudio» → el plan guarda `codigo_escuela` (solo el código, por la restricción del encargo).
- «Cada escuela tiene planes de estudio, identificados por un nombre de hasta 36 caracteres y por el año en que se aprobaron».
- «Un plan exige una cantidad de créditos obligatorios, otra de créditos electivos y otra de créditos extracurriculares; ninguna puede ser negativa».
- «El total de créditos del plan es la suma de las tres, y nunca debe poder editarse por separado».
- «Queremos que el sistema conserve ese 0 o 1 internamente, pero que a quien lo consulte le responda simplemente verdadero o falso».

---

## EscuelaProfesional (hereda de RegistroAcademico)

| Atributos (tipo) | Métodos y propiedades |
|---|---|
| `__codigo` (str) | `codigo`, `informacion_general`, `perfil_egresado` (get/set) |
| *(`nombre`: propiedad heredada)* | `codigo_director`, `codigo_secretario_academico` (get/set) |
| `__informacion_general` (str) | `longitud_maxima_nombre` (el caso no da el número; se asume 100) |
| `__perfil_egresado` (str) | `resumen()` |
| `__codigo_director` (str) | |
| `__codigo_secretario_academico` (str) | |

**Justificación:**
- «Cada escuela profesional tiene un código, un nombre, una información general y un perfil del egresado».
- «Cada escuela tiene un director y un secretario académico; por ahora basta con guardar el código del docente que ocupa cada cargo».
- El caso exige validar el nombre de la escuela pero no indica su largo máximo; en el código se usa 100 caracteres.

---

## PeriodoAcademico (hereda de RegistroAcademico)

| Atributos (tipo) | Métodos y propiedades |
|---|---|
| *(`nombre`: propiedad heredada)* | `numero`, `anio` (get/set) |
| `__numero` (int) | `fecha_inicio`, `fecha_fin`, `fecha_inicio_matricula`, `fecha_fin_matricula` (solo lectura) |
| `__anio` (int) | `cambiar_fechas(inicio, fin)` |
| `__fecha_inicio` (date) | `cambiar_fechas_matricula(inicio, fin)` |
| `__fecha_fin` (date) | `es_verano` (get/set: guarda int, devuelve bool) |
| `__fecha_inicio_matricula` (date) | `nota_minima_aprobatoria` (get/set: 0–20) |
| `__fecha_fin_matricula` (date) | `estado` (get/set: acepta EstadoPeriodo o 1–4) |
| `__es_verano` (int: 0/1) | `longitud_maxima_nombre` → 45 |
| `__nota_minima_aprobatoria` (Decimal) | `resumen()` |
| `__estado` (EstadoPeriodo) | |

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
| `__dni` (str) | `dni`, `nombres`, `apellidos` (get/set) |
| `__nombres` (str) | `nombre_completo` (propiedad **calculada**) |
| `__apellidos` (str) | `rol` (propiedad **abstracta**) |
| | `__str__()` (muestra rol y nombre completo) |

**Justificación:**
- «De toda persona registramos su DNI, sus nombres y sus apellidos, y a menudo necesitamos su nombre completo».
- «Cuando el sistema muestra a una persona, debe indicar qué rol cumple en la universidad, y esa respuesta es distinta para un estudiante y para un docente».
- «Nunca registramos a alguien que sea solo persona, sin ser estudiante ni docente» → abstracta.

---

## Estudiante (hereda de Persona)

| Atributos (tipo) | Métodos y propiedades |
|---|---|
| `__codigo_estudiante` (str) | `codigo_estudiante`, `codigo_escuela` (get/set) |
| `__codigo_escuela` (str) | `rol` → «Estudiante» |

**Justificación:** «Del estudiante guardamos además su código de estudiante y el código de la escuela a la que pertenece».

---

## Docente (hereda de Persona)

| Atributos (tipo) | Métodos y propiedades |
|---|---|
| `__codigo_docente` (str) | `codigo_docente` (get/set) |
| | `rol` → «Docente» |

**Justificación:** «del docente, su código de docente».
