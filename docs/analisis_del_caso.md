# Análisis del caso OTI

Este documento recorre el texto del caso párrafo por párrafo y registra qué elemento del modelo sale de cada frase. Todo lo que está en el código y en el diagrama UML aparece en esta tabla. Si algo no está aquí, no forma parte del modelo.

## 1. El problema que se resuelve

El planteamiento menciona tres errores reales de la base de datos. Cada uno se resuelve con un concepto de POO:

| Error encontrado | Causa | Solución en el modelo |
|---|---|---|
| «secciones con más estudiantes matriculados que vacantes» | El número de matriculados se podía escribir directamente | `matriculados` sin setter; solo cambia con `matricular()` y `retirar()` (encapsulamiento) |
| «un periodo académico que terminaba antes de empezar» | Las fechas no se validaban | `cambiar_fechas()` valida `fin >= inicio` antes de guardar (encapsulamiento) |
| «planes de estudio cuyo total de créditos no coincidía con la suma de sus partes» | El total se guardaba aparte | `creditos_totales` se calcula y no se guarda (dato derivado) |

## 2. Trazabilidad: frase del caso → elemento del modelo

### Cursos

| Frase del caso | Elemento |
|---|---|
| «La universidad mantiene un catálogo de cursos» | Clase `Curso` (el catálogo es el conjunto de cursos, no una clase con datos propios) |
| «un identificador único que el sistema genera al registrarlo y que nadie puede cambiar después» | `__id: int` + propiedad `id` {readOnly} |
| «tiene un código, como IS-282» | `__codigo: str` + propiedad `codigo` |
| «un nombre que no puede quedar vacío ni pasar de 200 caracteres» | `nombre` heredado de `RegistroAcademico`; `longitud_maxima_nombre = 200` |
| «una cantidad de créditos, que siempre es mayor que cero y puede tener hasta dos decimales» | `__creditos: Decimal {> 0, máx. 2 decimales}` |
| «horas teóricas, prácticas, de seminario y virtuales; ninguna de esas horas puede ser negativa ni pasar de 255» | `__horas_teoricas`, `__horas_practicas`, `__horas_seminario`, `__horas_virtuales: int {0..255}` |
| «nos piden las horas totales del curso, pero no queremos guardarlas» | `/horas_totales` calculada {readOnly} |

### Secciones

| Frase del caso | Elemento |
|---|---|
| «Un curso del catálogo no tiene vacantes; las vacantes pertenecen a cada sección» | `vacantes` está en `Seccion`, **no** en `Curso` |
| «Una sección se identifica por su código» | `__codigo: str` |
| «sabemos a qué curso y a qué periodo corresponde por sus códigos» | `__codigo_curso: str`, `__codigo_periodo: str` |
| «un número de vacantes mayor que cero» | `__vacantes: int {> 0}` |
| «y un número de matriculados» | `__matriculados: int {≥ 0, ≤ vacantes}` |
| «nunca deben modificarse escribiendo un número directamente» | propiedad `matriculados` {readOnly} |
| «solo aumentan cuando se matricula un estudiante» | método `matricular()` |
| «solo disminuyen cuando un estudiante se retira» | método `retirar()` |
| «Si la sección está llena, la matrícula debe rechazarse» | `matricular()` lanza `ValueError` |
| «no se puede reducir el número de vacantes por debajo de los que ya están matriculados» | setter de `vacantes` {≥ matriculados} |
| «Siempre queremos saber cuántas vacantes quedan disponibles» | `/vacantes_disponibles` calculada |

### Planes de estudio

| Frase del caso | Elemento |
|---|---|
| «identificados por un nombre de hasta 36 caracteres» | `nombre` heredado; `longitud_maxima_nombre = 36` |
| «y por el año en que se aprobaron» | `__anio_aprobacion: int` |
| «Cada escuela tiene planes de estudio» | `__codigo_escuela: str` (solo el código, por la restricción del encargo) |
| «créditos obligatorios… electivos… extracurriculares; ninguna puede ser negativa» | tres atributos `Decimal {≥ 0}` |
| «El total de créditos del plan es la suma de las tres, y nunca debe poder editarse por separado» | `/creditos_totales` calculada {readOnly} |
| «para indicar si un plan está vigente o si es un plan nuevo, se guarda un 0 o un 1» | `__vigente: int {0 o 1}`, `__es_nuevo: int {0 o 1}` |
| «que a quien lo consulte le responda simplemente verdadero o falso» | propiedades `vigente: bool`, `es_nuevo: bool` |

### Escuelas profesionales

| Frase del caso | Elemento |
|---|---|
| «tiene un código, un nombre, una información general y un perfil del egresado» | `__codigo`, `nombre` (heredado), `__informacion_general`, `__perfil_egresado` |
| «un director y un secretario académico; por ahora basta con guardar el código del docente» | `__codigo_director: str`, `__codigo_secretario_academico: str` |

### Periodos académicos

| Frase del caso | Elemento |
|---|---|
| «un nombre de hasta 45 caracteres» | `nombre` heredado; `longitud_maxima_nombre = 45` |
| «un número y un año, por ejemplo el periodo 2026-II» | `__numero: int`, `__anio: int` |
| «una fecha de inicio y una de fin» | `__fecha_inicio`, `__fecha_fin: date` |
| «un intervalo de matrícula con su propia fecha de inicio y de fin» | `__fecha_inicio_matricula`, `__fecha_fin_matricula: date` |
| «En ningún caso la fecha de fin puede ser anterior a la de inicio» | restricción {≥ inicio} en ambos intervalos |
| «las dos fechas de cada intervalo… deben poder cambiarse juntas» | fechas {readOnly} + `cambiar_fechas()` y `cambiar_fechas_matricula()` |
| «si es de verano, con el mismo 0 o 1 de los planes» | `__es_verano: int {0 o 1}` + propiedad `es_verano: bool` |
| «la nota mínima aprobatoria, que va de 0 a 20 y puede tener decimales» | `__nota_minima_aprobatoria: Decimal {0..20}` |
| «1 es planificado, 2 en curso, 3 matrícula cerrada y 4 finalizado… ya hemos visto periodos con estado 7» | enumeración `EstadoPeriodo` + asociación `PeriodoAcademico → EstadoPeriodo` con rol `- __estado` y multiplicidad 1 |

### Personas

| Frase del caso | Elemento |
|---|---|
| «hay estudiantes y docentes» | Clases `Estudiante` y `Docente` |
| «De toda persona registramos su DNI, sus nombres y sus apellidos» | En `Persona`: `__dni`, `__nombres`, `__apellidos: str` |
| «a menudo necesitamos su nombre completo» | `/nombre_completo` calculada |
| «Del estudiante guardamos además su código de estudiante y el código de la escuela» | `__codigo_estudiante`, `__codigo_escuela: str` |
| «del docente, su código de docente» | `__codigo_docente: str` |
| «Cuando el sistema muestra a una persona, debe indicar qué rol cumple» | `__str__()` en `Persona` usa `rol` |
| «esa respuesta es distinta para un estudiante y para un docente» | `rol` abstracto, redefinido en cada subclase |
| «Nunca registramos a alguien que sea solo persona» | `Persona` es abstracta |

### Pedido final de la jefatura

| Frase del caso | Elemento |
|---|---|
| «Cursos, planes de estudio, escuelas y periodos… todos tienen un nombre que debe validarse» | Clase abstracta `RegistroAcademico` con `nombre` validado |
| «aunque el tamaño máximo cambie en cada caso» | propiedad abstracta `longitud_maxima_nombre` |
| «pedirle a cada uno un resumen de sí mismo» | método abstracto `resumen()` |
| «sin tener que preguntar qué tipo de registro es» | polimorfismo, sin `isinstance` |

### Restricción del encargo

| Frase del caso | Elemento |
|---|---|
| «Cuando un registro hace referencia a otro… por ahora se guarda solo el código como texto» | `codigo_curso`, `codigo_periodo`, `codigo_escuela`, `codigo_director` y `codigo_secretario_academico` son `str`; no hay asociaciones entre esas clases |

## 3. Sustantivos que NO son clases

| Sustantivo | Por qué no es una clase |
|---|---|
| OTI, jefatura, universidad | Son el contexto o los usuarios del sistema, no datos que se guarden |
| Base de datos | Es el almacenamiento, no una entidad del dominio |
| Catálogo de cursos | Es el conjunto de cursos; el caso no le da atributos propios |
| Matrícula | Es una acción sobre la sección (`matricular()`); el caso no pide guardar quién se matriculó |
| Cargo (director, secretario) | Solo se guarda el código del docente |

## 4. Interpretaciones del texto

| Punto | Interpretación | Frase que la respalda |
|---|---|---|
| «No vacío» se aplica a los nombres de las cuatro clases, no solo al curso | La validación del nombre es la misma para todas y solo cambia el tamaño máximo | «todos tienen un nombre que debe validarse, aunque el tamaño máximo cambie en cada caso» |
| El plan tiene dos indicadores 0/1, `vigente` y `es_nuevo` | «si un plan está vigente» y «si es un plan nuevo» son dos preguntas distintas | «para indicar si un plan está vigente o si es un plan nuevo, se guarda un 0 o un 1» |
| Los atributos son privados con `__` | El entregable pide «marcando atributos privados» y la convención de Python para lo privado es el doble guion bajo | «Convención obligatoria… según la convención de Python» |

## 5. Puntos que el caso no define

| Punto | Decisión mínima |
|---|---|
| Tamaño máximo del nombre de la escuela | El caso exige validarlo pero no da el número; se asume 100 (en el diagrama: `{= 100, asumido}`) |
| Mecanismo para generar el id del curso | Contador interno |
| Fin igual a inicio | Permitido: el caso solo prohíbe que sea anterior |
| Códigos, DNI, nombres, apellidos, años, número del periodo | Sin reglas en el caso: solo se verifica el tipo de dato |

## 6. Resumen del modelo

- **10 clases**: 2 abstractas (`RegistroAcademico`, `Persona`), 7 concretas y 1 enumeración (`EstadoPeriodo`).
- **2 jerarquías de herencia**: `RegistroAcademico` → `Curso`, `PlanEstudios`, `EscuelaProfesional`, `PeriodoAcademico`; y `Persona` → `Estudiante`, `Docente`.
- **1 asociación**: `PeriodoAcademico` → `EstadoPeriodo` (rol `__estado`, multiplicidad 1). Las demás referencias son códigos `str` por la restricción del encargo.
- **29 reglas** tomadas del texto, cada una probada con un caso válido y uno inválido.
