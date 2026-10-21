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
| «un identificador único que el sistema genera al registrarlo y que nadie puede cambiar después» | `_id: int` + propiedad `id` {readOnly} |
| «tiene un código, como IS-282» | `_codigo: str` + propiedad `codigo` |
| «un nombre que no puede quedar vacío ni pasar de 200 caracteres» | `nombre` heredado de `RegistroAcademico`; `longitud_maxima_nombre = 200` |
| «una cantidad de créditos, que siempre es mayor que cero y puede tener hasta dos decimales» | `_creditos: Decimal {> 0, máx. 2 decimales}` |
| «horas teóricas, prácticas, de seminario y virtuales; ninguna de esas horas puede ser negativa ni pasar de 255» | `_horas_teoricas`, `_horas_practicas`, `_horas_seminario`, `_horas_virtuales: int {0..255}` |
| «nos piden las horas totales del curso, pero no queremos guardarlas» | `/horas_totales` calculada {readOnly} |

### Secciones

| Frase del caso | Elemento |
|---|---|
| «Un curso del catálogo no tiene vacantes; las vacantes pertenecen a cada sección» | `vacantes` está en `Seccion`, **no** en `Curso` |
| «Una sección se identifica por su código» | `_codigo: str` |
| «sabemos a qué curso y a qué periodo corresponde por sus códigos» | `_codigo_curso: str`, `_codigo_periodo: str` |
| «un número de vacantes mayor que cero» | `_vacantes: int {> 0}` |
| «y un número de matriculados» | `_matriculados: int` |
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
| «y por el año en que se aprobaron» | `_anio_aprobacion: int` |
| «créditos obligatorios… electivos… extracurriculares; ninguna puede ser negativa» | tres atributos `Decimal {≥ 0}` |
| «El total de créditos del plan es la suma de las tres, y nunca debe poder editarse por separado» | `/creditos_totales` calculada {readOnly} |
| «para indicar si un plan está vigente o si es un plan nuevo, se guarda un 0 o un 1» | `_vigente: int {0 o 1}`, `_es_nuevo: int {0 o 1}` |
| «que a quien lo consulte le responda simplemente verdadero o falso» | propiedades `vigente: bool`, `es_nuevo: bool` |

### Escuelas profesionales

| Frase del caso | Elemento |
|---|---|
| «tiene un código, un nombre, una información general y un perfil del egresado» | `_codigo`, `nombre` (heredado), `_informacion_general`, `_perfil_egresado` |
| «un director y un secretario académico; por ahora basta con guardar el código del docente» | `_codigo_director: str`, `_codigo_secretario_academico: str` |

### Periodos académicos

| Frase del caso | Elemento |
|---|---|
| «un nombre de hasta 45 caracteres» | `nombre` heredado; `longitud_maxima_nombre = 45` |
| «un número y un año, por ejemplo el periodo 2026-II» | `_numero: int`, `_anio: int` |
| «una fecha de inicio y una de fin» | `_fecha_inicio`, `_fecha_fin: date` |
| «un intervalo de matrícula con su propia fecha de inicio y de fin» | `_fecha_inicio_matricula`, `_fecha_fin_matricula: date` |
| «En ningún caso la fecha de fin puede ser anterior a la de inicio» | restricción {≥ inicio} en ambos intervalos |
| «las dos fechas de cada intervalo… deben poder cambiarse juntas» | fechas {readOnly} + `cambiar_fechas()` y `cambiar_fechas_matricula()` |
| «si es de verano, con el mismo 0 o 1 de los planes» | `_es_verano: int {0 o 1}` + propiedad `es_verano: bool` |
| «la nota mínima aprobatoria, que va de 0 a 20 y puede tener decimales» | `_nota_minima_aprobatoria: Decimal {0..20}` |
| «1 es planificado, 2 en curso, 3 matrícula cerrada y 4 finalizado… ya hemos visto periodos con estado 7» | enumeración `EstadoPeriodo` + `_estado: EstadoPeriodo` |

### Personas

| Frase del caso | Elemento |
|---|---|
| «hay estudiantes y docentes» | Clases `Estudiante` y `Docente` |
| «De toda persona registramos su DNI, sus nombres y sus apellidos» | En `Persona`: `_dni`, `_nombres`, `_apellidos: str` |
| «a menudo necesitamos su nombre completo» | `/nombre_completo` calculada |
| «Del estudiante guardamos además su código de estudiante y el código de la escuela» | `_codigo_estudiante`, `_codigo_escuela: str` |
| «del docente, su código de docente» | `_codigo_docente: str` |
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

## 4. Puntos que el caso no define

| Punto | Decisión mínima |
|---|---|
| Tamaño máximo del nombre de la escuela | El caso exige validarlo pero no da el número; se asume 100 |
| Mecanismo para generar el id del curso | Contador interno |
| Fin igual a inicio | Permitido: el caso solo prohíbe que sea anterior |
| Códigos, DNI, nombres, apellidos, años, número del periodo | Sin reglas en el caso: solo se verifica el tipo de dato |

## 5. Resumen del modelo

- **10 clases**: 2 abstractas (`RegistroAcademico`, `Persona`), 7 concretas y 1 enumeración (`EstadoPeriodo`).
- **2 jerarquías de herencia**: `RegistroAcademico` → `Curso`, `PlanEstudios`, `EscuelaProfesional`, `PeriodoAcademico`; y `Persona` → `Estudiante`, `Docente`.
- **1 asociación**: `PeriodoAcademico` → `EstadoPeriodo`.
- **29 reglas** tomadas del texto, cada una probada con un caso válido y uno inválido.
