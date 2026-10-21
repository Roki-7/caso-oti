# Desarrollo de las actividades

La Actividad 1 (ficha) está en [1_ficha_actividad_1.md](1_ficha_actividad_1.md) y el diagrama UML en [2_diagrama_uml/](2_diagrama_uml/).

---

## Actividad 2: Encapsulamiento

Todos los datos se guardan en atributos **privados** con doble guion bajo (`__`), que es la convención de Python para lo privado: Python cambia internamente su nombre (*name mangling*), así que `curso.__creditos` no existe fuera de la clase. Se acceden solo mediante `@property`. Así cada asignación pasa por un setter que valida, y un dato inválido nunca llega a guardarse. Solo se validan las reglas que indica el caso; los datos sin regla (códigos, DNI, nombres, apellidos, años) se guardan tal como llegan.

### 2.1 Datos protegidos y su regla de validación

| Clase | Dato | Regla | Frase del caso |
|---|---|---|---|
| Todas las de `RegistroAcademico` | `nombre` | No vacío; máximo 200 (Curso), 36 (Plan), 45 (Periodo); Escuela: el caso no da el máximo (se usa 100) | «un nombre que debe validarse, aunque el tamaño máximo cambie» |
| Curso | `creditos` | Mayor que 0, hasta 2 decimales | «siempre es mayor que cero y puede tener hasta dos decimales» |
| Curso | `horas_teoricas`, `horas_practicas`, `horas_seminario`, `horas_virtuales` | Enteros de 0 a 255 | «ninguna de esas horas puede ser negativa ni pasar de 255» |
| Seccion | `vacantes` | Entero mayor que 0 y no menor que `matriculados` | «vacantes mayor que cero», «no se puede reducir el número de vacantes por debajo de los que ya están matriculados» |
| Seccion | `matriculados` | Entre 0 y vacantes; solo cambia de uno en uno | «Si la sección está llena, la matrícula debe rechazarse» |
| PlanEstudios | `creditos_obligatorios`, `creditos_electivos`, `creditos_extracurriculares` | Mayores o iguales a 0 | «ninguna puede ser negativa» |
| PlanEstudios | `vigente`, `es_nuevo` | Solo 0/1 o True/False | «se guarda un 0 o un 1» |
| PeriodoAcademico | fechas del periodo y de matrícula | `fin >= inicio` en cada intervalo | «En ningún caso la fecha de fin puede ser anterior a la de inicio» |
| PeriodoAcademico | `es_verano` | Solo 0/1 o True/False | «con el mismo 0 o 1 de los planes de estudio» |
| PeriodoAcademico | `nota_minima_aprobatoria` | De 0 a 20, con decimales | «va de 0 a 20 y puede tener decimales» |
| PeriodoAcademico | `estado` | Solo 1, 2, 3 o 4 | «ya hemos visto periodos con estado 7» |

Créditos y nota se guardan como `Decimal` y no como `float`, porque solo así se puede contar con exactitud cuántos decimales tiene un número.

### 2.2 Datos que no se guardan, sino que se calculan

| Clase | Dato calculado | Fórmula |
|---|---|---|
| Curso | `horas_totales` | teóricas + prácticas + seminario + virtuales |
| PlanEstudios | `creditos_totales` | obligatorios + electivos + extracurriculares |
| Seccion | `vacantes_disponibles` | vacantes − matriculados |
| Persona | `nombre_completo` | nombres + « » + apellidos |

**Problema que evita:** la **inconsistencia por redundancia** (anomalía de actualización). Si un dato derivado se guarda aparte, cada vez que alguien corrige una de sus partes debe acordarse de actualizar también el total. Basta un olvido para que el total quede mal, que es exactamente lo que encontró la OTI: «planes de estudio cuyo total de créditos no coincidía con la suma de sus partes» y «cada vez que alguien corrige una hora y olvida actualizar el total, el dato queda mal». Al calcularlo en cada consulta, el total siempre coincide con sus partes porque no existe una copia que pueda desactualizarse.

### 2.3 Datos que no se pueden modificar directamente

| Dato | ¿Cómo cambia? | Qué pasa si se intenta asignar |
|---|---|---|
| `Curso.id` | Nunca: lo genera el sistema al crear el curso | `AttributeError` (propiedad sin setter) |
| `Seccion.matriculados` | Solo con `matricular()` (+1) y `retirar()` (−1) | `AttributeError` |
| `PeriodoAcademico.fecha_inicio` / `fecha_fin` | Solo con `cambiar_fechas(inicio, fin)` | `AttributeError` |
| `PeriodoAcademico.fecha_inicio_matricula` / `fecha_fin_matricula` | Solo con `cambiar_fechas_matricula(inicio, fin)` | `AttributeError` |
| Todos los datos calculados de 2.2 | Cambian solos al modificar sus partes | `AttributeError` |

**¿Por qué las fechas se cambian juntas?** Si hubiera un setter para cada fecha, mover un periodo de marzo–julio a agosto–diciembre sería imposible: al cambiar primero el inicio a agosto, el objeto quedaría con «inicio agosto, fin julio» y la validación lo rechazaría. Con `cambiar_fechas()` ambas fechas se validan como pareja y se asignan solo si son correctas, así que el objeto nunca queda en un estado intermedio inválido.

### 2.4 Datos que se guardan con un tipo y se entregan con otro

| Dato | Se guarda como | Se entrega como |
|---|---|---|
| `PlanEstudios.vigente` | `int` (0 o 1) en `__vigente` | `bool` |
| `PlanEstudios.es_nuevo` | `int` (0 o 1) en `__es_nuevo` | `bool` |
| `PeriodoAcademico.es_verano` | `int` (0 o 1) en `__es_verano` | `bool` |
El setter acepta tanto `True/False` como `0/1` (lo que llega de la base de datos) y siempre guarda el entero. El getter convierte a `bool`. De este modo se respeta el formato de la base de datos y quien consulta recibe una respuesta clara: «verdadero o falso».

**Caso relacionado (`PeriodoAcademico.estado`):** el setter **recibe** el número `int` (1–4) que llega de la base de datos, pero lo **guarda y lo entrega** como `EstadoPeriodo` (Enum). Aquí la conversión ocurre al recibir el dato, no al entregarlo; se explica en la Actividad 3.3.

---

## Actividad 3: Abstracción

### 3.1 Lo que varias clases tienen en común

Según el pedido final de la jefatura, `Curso`, `PlanEstudios`, `EscuelaProfesional` y `PeriodoAcademico` son «cosas muy distintas», pero comparten dos cosas:

1. **Un nombre que debe validarse**, con un tamaño máximo distinto en cada clase.
2. **La capacidad de dar un resumen de sí mismos.**

Eso se define como la clase abstracta `RegistroAcademico` (`codigo/registro_academico.py`), que hereda de `ABC`:

```python
class RegistroAcademico(ABC):
    def __init__(self, nombre: str):
        self.nombre = nombre  # pasa por el setter, que valida

    @property
    @abstractmethod
    def longitud_maxima_nombre(self) -> int: ...

    @abstractmethod
    def resumen(self) -> str: ...

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = validar_texto(valor, "El nombre", self.longitud_maxima_nombre)
```

La validación del nombre se escribe una sola vez en la clase base; cada subclase solo indica su límite.

Intentar crearla directamente falla:

```
>>> RegistroAcademico("X")
TypeError: Can't instantiate abstract class RegistroAcademico without an
implementation for abstract methods 'longitud_maxima_nombre', 'resumen'
```

**Segunda abstracción:** `Persona` también es abstracta, porque el caso dice «Nunca registramos a alguien que sea solo persona, sin ser estudiante ni docente». Obliga a implementar la propiedad `rol`.

### 3.2 Métodos que la clase abstracta obliga a implementar

| Clase abstracta | Miembro abstracto | Por qué es abstracto |
|---|---|---|
| `RegistroAcademico` | `longitud_maxima_nombre` (propiedad) | El tamaño máximo «cambia en cada caso»: solo cada subclase lo conoce (curso 200, plan 36, periodo 45; para la escuela el caso no lo indica) |
| `RegistroAcademico` | `resumen()` | Cada registro se describe distinto; es la base del polimorfismo |
| `Persona` | `rol` (propiedad) | «esa respuesta es distinta para un estudiante y para un docente» |

### 3.3 Mejor representación del estado del periodo

**Problema:** el estado se guarda como un número suelto. «Nadie recuerda qué significa cada número, y ya hemos visto periodos con estado 7».

**Solución:** una enumeración (`codigo/estado_periodo.py`):

```python
class EstadoPeriodo(Enum):
    PLANIFICADO = 1
    EN_CURSO = 2
    MATRICULA_CERRADA = 3
    FINALIZADO = 4
```

Solo existen los 4 valores válidos, cada uno con un nombre legible. `EstadoPeriodo(7)` lanza `ValueError`, así que un estado 7 es rechazado:

```
>>> periodo.estado = 7
ValueError: El estado: solo puede ser 1 (planificado), 2 (en curso),
3 (matrícula cerrada) o 4 (finalizado); se recibió 7.
```

---

## Actividad 4: Herencia

### 4.1 Jerarquías de herencia

```
RegistroAcademico «abstract»              Persona «abstract»
 ├── Curso                                  ├── Estudiante
 ├── PlanEstudios                           └── Docente
 ├── EscuelaProfesional
 └── PeriodoAcademico
```

| Relación | Frase «X es un Y» |
|---|---|
| `Curso(RegistroAcademico)` | Un curso **es un** registro académico |
| `PlanEstudios(RegistroAcademico)` | Un plan de estudios **es un** registro académico |
| `EscuelaProfesional(RegistroAcademico)` | Una escuela profesional **es un** registro académico |
| `PeriodoAcademico(RegistroAcademico)` | Un periodo académico **es un** registro académico |
| `Estudiante(Persona)` | Un estudiante **es una** persona |
| `Docente(Persona)` | Un docente **es una** persona |

### 4.2 Qué hereda, qué agrega y qué redefine cada subclase

| Subclase | Hereda | Agrega | Redefine |
|---|---|---|---|
| `Curso` | propiedad `nombre` con su validación | `id`, `codigo`, `creditos`, las 4 horas, `horas_totales` | `longitud_maxima_nombre` (200), `resumen()` |
| `PlanEstudios` | propiedad `nombre` con su validación | `anio_aprobacion`, `codigo_escuela`, los 3 créditos, `creditos_totales`, `vigente`, `es_nuevo` | `longitud_maxima_nombre` (36), `resumen()` |
| `EscuelaProfesional` | propiedad `nombre` con su validación | `codigo`, `informacion_general`, `perfil_egresado`, `codigo_director`, `codigo_secretario_academico` | `longitud_maxima_nombre` (valor asumido: 100), `resumen()` |
| `PeriodoAcademico` | propiedad `nombre` con su validación | `numero`, `anio`, las 4 fechas, `cambiar_fechas()`, `cambiar_fechas_matricula()`, `es_verano`, `nota_minima_aprobatoria`, `estado` | `longitud_maxima_nombre` (45), `resumen()` |
| `Estudiante` | `dni`, `nombres`, `apellidos`, `nombre_completo`, `__str__()` | `codigo_estudiante`, `codigo_escuela` | `rol` («Estudiante») |
| `Docente` | `dni`, `nombres`, `apellidos`, `nombre_completo`, `__str__()` | `codigo_docente` | `rol` («Docente») |

Todas las subclases llaman a `super().__init__(...)` para que la clase base inicialice y valide los datos comunes.

### 4.3 Polimorfismo

Se recorre una lista mixta pidiendo a cada objeto su resumen, **sin `isinstance` ni `type()`**. Cada objeto responde con su propia versión de `resumen()` (regla R29 de `codigo/programa_prueba.py`):

```python
registros = [curso_valido(), plan_valido(), escuela_valida(), periodo_valido()]
for registro in registros:
    aceptado("resumen()", registro.resumen)
```

Salida:

```
[Curso #10] IS-282 - Programación Orientada a Objetos | 4 créditos | 6 h totales (T:2 P:4 S:0 V:0)
[Plan de estudios] Plan 2018 (2018) - escuela IS | 220 créditos (Oblig:180 Elect:30 Extra:10) | vigente
[Escuela profesional] IS - Ingeniería de Sistemas | director: DOC-001 | secretario académico: DOC-002
[Periodo académico] Segundo semestre académico 2026 | 2026-08-17 a 2026-12-18 | matrícula 2026-08-03 a 2026-08-14 | nota mínima 10.5 | estado PLANIFICADO
```

Lo mismo ocurre con las personas (regla R27): `Persona.__str__()` usa `self.rol`, y cada subclase da una respuesta distinta («Cuando el sistema muestra a una persona, debe indicar qué rol cumple»).

```python
for persona in personas:
    aceptado("str(persona)", lambda: str(persona))
```

```
Estudiante: Ana Lucía Quispe Huamán (DNI 70123456)
Docente: Luis Alberto Pérez Rojas (DNI 40123456)
```

---

## Actividad 5: Implementación y prueba

### Implementación

Todas las clases están en la carpeta `codigo/`, un archivo por clase:

| Archivo | Clase |
|---|---|
| `registro_academico.py` | `RegistroAcademico` (abstracta) |
| `curso.py`, `plan_estudios.py`, `escuela_profesional.py`, `periodo_academico.py` | Subclases de `RegistroAcademico` |
| `estado_periodo.py` | `EstadoPeriodo` (enumeración) |
| `seccion.py` | `Seccion` |
| `persona.py` | `Persona` (abstracta) |
| `estudiante.py`, `docente.py` | Subclases de `Persona` |
| `validaciones.py` | Funciones de validación usadas por las clases |

### Programa de prueba

Archivo: `codigo/programa_prueba.py`. Para cada regla muestra un dato **válido aceptado** y un dato **inválido rechazado**, capturando el error con `try/except`.

Ejecución:

```bash
python codigo/programa_prueba.py
```

Resultado: **72/72 comprobaciones correctas**. La salida completa está al final de esta actividad.

### Reglas probadas

| # | Clase | Regla | Frase del caso | Válido aceptado | Inválido rechazado | Error |
|---|---|---|---|---|---|---|
| R01 | Curso | El id lo genera el sistema y no se cambia | «el sistema genera al registrarlo y que nadie puede cambiar después» | Ids automáticos 1 y 2 | `curso.id = 99` | AttributeError |
| R02 | Curso | Nombre no vacío, máximo 200 | «no puede quedar vacío ni pasar de 200 caracteres» | 200 caracteres | `"   "` y 201 caracteres | ValueError |
| R03 | Curso | Créditos mayores que 0 | «siempre es mayor que cero» | 0.5 | 0 y −3 | ValueError |
| R04 | Curso | Créditos con hasta 2 decimales | «puede tener hasta dos decimales» | 3.75 | 3.755 | ValueError |
| R05 | Curso | Horas de 0 a 255 | «ninguna de esas horas puede ser negativa ni pasar de 255» | 0 y 255 | −1, 256 y 300 | ValueError |
| R06 | Curso | Horas totales calculadas | «no queremos guardarlas» | Total se actualiza al corregir una hora | `curso.horas_totales = 50` | AttributeError |
| R07 | Seccion | Vacantes mayores que 0 | «un número de vacantes mayor que cero» | 2 vacantes | 0 vacantes | ValueError |
| R08 | Seccion | Matriculados no se escriben | «nunca deben modificarse escribiendo un número directamente» | `matricular()` | `seccion.matriculados = 40` | AttributeError |
| R09 | Seccion | Sección llena rechaza matrícula | «Si la sección está llena, la matrícula debe rechazarse» | 2.ª matrícula de 2 | 3.ª matrícula | ValueError |
| R10 | Seccion | Matriculados solo bajan con retiro | «solo disminuyen cuando un estudiante se retira» | `retirar()` con 1 matriculado | `retirar()` con 0 | ValueError |
| R11 | Seccion | Vacantes no menores que matriculados | «no se puede reducir el número de vacantes por debajo de los que ya están matriculados» | Bajar de 5 a 3 con 3 matriculados | Bajar a 2 con 3 matriculados | ValueError |
| R12 | Seccion | Vacantes disponibles calculadas | «Siempre queremos saber cuántas vacantes quedan disponibles» | 30 − 1 = 29 | `vacantes_disponibles = 100` | AttributeError |
| R13 | PlanEstudios | Nombre máximo 36 | «un nombre de hasta 36 caracteres» | 36 caracteres | 37 caracteres | ValueError |
| R14 | PlanEstudios | Créditos no negativos | «ninguna puede ser negativa» | Extracurriculares = 0 | Electivos = −5 | ValueError |
| R15 | PlanEstudios | Total = suma, no editable | «es la suma de las tres, y nunca debe poder editarse por separado» | 180 + 40 + 10 = 230 | `creditos_totales = 999` | AttributeError |
| R16 | PlanEstudios | 0/1 interno, bool externo | «conserve ese 0 o 1 internamente… responda verdadero o falso» | `vigente=1` → `True` | `vigente=2` | ValueError |
| R17 | Escuela | El nombre se valida | «todos tienen un nombre que debe validarse» | «Ingeniería de Sistemas» | Nombre vacío | ValueError |
| R18 | Periodo | Nombre máximo 45 | «un nombre de hasta 45 caracteres» | 45 caracteres | 46 caracteres | ValueError |
| R19 | Periodo | Fin del periodo ≥ inicio | «En ningún caso la fecha de fin puede ser anterior a la de inicio» | Mismo día | Termina antes de empezar | ValueError |
| R20 | Periodo | Fin de matrícula ≥ inicio | (misma frase, intervalo de matrícula) | 3 al 14 de agosto | 14 al 3 de agosto | ValueError |
| R21 | Periodo | Fechas se cambian juntas | «deben poder cambiarse juntas» | Mover mar–jul a ago–dic | Asignar `fecha_inicio` sola; `cambiar_fechas` inválido | AttributeError / ValueError |
| R22 | Periodo | Verano: 0/1 interno, bool externo | «con el mismo 0 o 1 de los planes de estudio» | `True` → guarda 1 | `"si"` | ValueError |
| R23 | Periodo | Nota de 0 a 20 con decimales | «va de 0 a 20 y puede tener decimales» | 10.5 | 20.5 y −1 | ValueError |
| R24 | Periodo | Estado solo 1–4 | «1 es planificado, 2 en curso, 3 matrícula cerrada y 4 finalizado» | 2 y `EstadoPeriodo.FINALIZADO` | 7 | ValueError |
| R25 | Persona | No se registra «solo persona» | «Nunca registramos a alguien que sea solo persona» | `Estudiante(...)` | `Persona(...)` | TypeError |
| R26 | Persona | Nombre completo calculado | «a menudo necesitamos su nombre completo» | Se actualiza al corregir nombres | `nombre_completo = "X"` | AttributeError |
| R27 | Persona | Rol distinto por subclase | «esa respuesta es distinta para un estudiante y para un docente» | «Estudiante» y «Docente»; `str(persona)` muestra el rol | Subclase sin `rol` | TypeError |
| R28 | RegistroAcademico | Clase abstracta con contrato | Actividad 3.1 y 3.2 | Curso implementa todo | `RegistroAcademico("X")` y subclase sin `resumen()` | TypeError |
| R29 | Todas | Polimorfismo sin `isinstance` | «pedirle a cada uno un resumen de sí mismo, sin tener que preguntar qué tipo de registro es» | Resumen de los 4 tipos | — | — |

### Salida del programa de prueba

<details>
<summary>Ver la salida completa</summary>

```
PROGRAMA DE PRUEBA - CASO OTI
Cada regla muestra un dato válido aceptado y uno inválido rechazado.

==============================================================================
CURSO
==============================================================================

R01. El id lo genera el sistema y nadie puede cambiarlo
   [ACEPTADO]  dos cursos reciben ids distintos y automáticos -> ids 1 y 2
   [RECHAZADO] curso.id = 99
               AttributeError: property 'id' of 'Curso' object has no setter

R02. El nombre no puede quedar vacío ni pasar de 200 caracteres
   [ACEPTADO]  nombre de 200 caracteres -> 200
   [RECHAZADO] nombre vacío ('   ')
               ValueError: El nombre: no puede quedar vacío.
   [RECHAZADO] nombre de 201 caracteres
               ValueError: El nombre: no puede pasar de 200 caracteres (tiene 201).

R03. Los créditos siempre son mayores que cero
   [ACEPTADO]  créditos = 0.5 -> 0.5
   [RECHAZADO] créditos = 0
               ValueError: Los créditos del curso: debe ser mayor que 0 (se recibió 0).
   [RECHAZADO] créditos = -3
               ValueError: Los créditos del curso: debe ser mayor que 0 (se recibió -3).

R04. Los créditos pueden tener hasta dos decimales
   [ACEPTADO]  créditos = 3.75 -> 3.75
   [RECHAZADO] créditos = 3.755
               ValueError: Los créditos del curso: admite como máximo 2 decimales (se recibió 3.755).

R05. Ninguna hora puede ser negativa ni pasar de 255
   [ACEPTADO]  horas en los extremos 0 y 255 -> 255
   [RECHAZADO] horas prácticas = -1
               ValueError: Las horas prácticas: no puede ser menor que 0 (se recibió -1).
   [RECHAZADO] horas de seminario = 256
               ValueError: Las horas de seminario: no puede ser mayor que 255 (se recibió 256).
   [RECHAZADO] modificar horas virtuales a 300 en un curso existente
               ValueError: Las horas virtuales: no puede ser mayor que 255 (se recibió 300).

R06. Las horas totales se calculan, no se guardan
   [ACEPTADO]  al corregir una hora el total se actualiza solo -> 6 h -> 7 h
   [RECHAZADO] curso.horas_totales = 50
               AttributeError: property 'horas_totales' of 'Curso' object has no setter

==============================================================================
SECCIÓN
==============================================================================

R07. Las vacantes de una sección son mayores que cero
   [ACEPTADO]  sección con 2 vacantes -> 2
   [RECHAZADO] sección con 0 vacantes
               ValueError: Las vacantes: no puede ser menor que 1 (se recibió 0).

R08. Los matriculados no se modifican escribiendo un número
   [ACEPTADO]  matricular() incrementa matriculados -> 1
   [RECHAZADO] seccion.matriculados = 40
               AttributeError: property 'matriculados' of 'Seccion' object has no setter

R09. Si la sección está llena, la matrícula se rechaza
   [ACEPTADO]  segunda matrícula en sección de 2 vacantes -> 2/2
   [RECHAZADO] tercera matrícula con la sección llena
               ValueError: La sección IS282-B está llena (2 vacantes ocupadas).

R10. Los matriculados solo disminuyen cuando un estudiante se retira
   [ACEPTADO]  retirar() a un estudiante matriculado -> quedan 0
   [RECHAZADO] retirar() de una sección sin matriculados
               ValueError: La sección IS282-C no tiene estudiantes para retirar.

R11. No se pueden reducir las vacantes por debajo de los matriculados
   [ACEPTADO]  reducir de 5 a 3 vacantes con 3 matriculados -> 3
   [RECHAZADO] reducir a 2 vacantes con 3 matriculados
               ValueError: No se puede reducir las vacantes a 2: ya hay 3 estudiantes matriculados.

R12. Las vacantes disponibles se calculan
   [ACEPTADO]  30 vacantes y 1 matriculado -> 29 disponibles
   [RECHAZADO] seccion.vacantes_disponibles = 100
               AttributeError: property 'vacantes_disponibles' of 'Seccion' object has no setter

==============================================================================
PLAN DE ESTUDIOS
==============================================================================

R13. El nombre del plan tiene hasta 36 caracteres
   [ACEPTADO]  nombre de 36 caracteres -> 36
   [RECHAZADO] nombre de 37 caracteres
               ValueError: El nombre: no puede pasar de 36 caracteres (tiene 37).

R14. Ningún tipo de crédito del plan puede ser negativo
   [ACEPTADO]  créditos extracurriculares = 0 -> 0
   [RECHAZADO] créditos electivos = -5
               ValueError: Los créditos electivos: no puede ser menor que 0 (se recibió -5).

R15. El total es la suma de las tres partes y no se edita por separado
   [ACEPTADO]  total tras cambiar electivos de 30 a 40 -> 230 = 180 + 40 + 10
   [RECHAZADO] plan.creditos_totales = 999
               AttributeError: property 'creditos_totales' of 'PlanEstudios' object has no setter

R16. Vigente / es nuevo: se guarda 0 o 1, se responde verdadero o falso
   [ACEPTADO]  vigente=1 se guarda como int y se entrega como bool -> interno 1 (int) -> externo True (bool)
   [RECHAZADO] vigente = 2
               ValueError: Vigente: solo admite 0/1 o True/False (se recibió 2).

==============================================================================
ESCUELA PROFESIONAL
==============================================================================

R17. El nombre de la escuela también se valida
   [ACEPTADO]  nombre 'Ingeniería de Sistemas' -> Ingeniería de Sistemas
   [RECHAZADO] nombre vacío
               ValueError: El nombre: no puede quedar vacío.

==============================================================================
PERIODO ACADÉMICO
==============================================================================

R18. El nombre del periodo tiene hasta 45 caracteres
   [ACEPTADO]  nombre de 45 caracteres -> 45
   [RECHAZADO] nombre de 46 caracteres
               ValueError: El nombre: no puede pasar de 45 caracteres (tiene 46).

R19. La fecha de fin del periodo no puede ser anterior a la de inicio
   [ACEPTADO]  inicio y fin el mismo día (no es anterior) -> 2026-08-17
   [RECHAZADO] periodo que termina antes de empezar
               ValueError: La fecha de fin del periodo (2026-08-17) no puede ser anterior a la de inicio (2026-12-18).

R20. La fecha de fin de matrícula no puede ser anterior a la de inicio
   [ACEPTADO]  matrícula del 3 al 14 de agosto -> 2026-08-14
   [RECHAZADO] matrícula del 14 al 3 de agosto
               ValueError: La fecha de fin del intervalo de matrícula (2026-08-03) no puede ser anterior a la de inicio (2026-08-14).

R21. Las dos fechas de cada intervalo se cambian juntas
   [ACEPTADO]  mover el periodo de mar-jul a ago-dic con cambiar_fechas() -> 2026-08-17 a 2026-12-18
   [RECHAZADO] periodo.fecha_inicio = ... (asignación individual)
               AttributeError: property 'fecha_inicio' of 'PeriodoAcademico' object has no setter
   [RECHAZADO] cambiar_fechas() con fin anterior a inicio
               ValueError: La fecha de fin del periodo (2026-08-17) no puede ser anterior a la de inicio (2026-12-18).
   [ACEPTADO]  tras el rechazo el periodo conserva sus fechas -> 2026-08-17 a 2026-12-18

R22. Es verano: se guarda 0 o 1, se responde verdadero o falso
   [ACEPTADO]  es_verano=True se guarda como 1 y se entrega como bool -> interno 1 -> externo True
   [RECHAZADO] es_verano = 'si'
               ValueError: Es verano: solo admite 0/1 o True/False (se recibió 'si').

R23. La nota mínima aprobatoria va de 0 a 20 y puede tener decimales
   [ACEPTADO]  nota = 10.5 -> 10.5
   [RECHAZADO] nota = 20.5
               ValueError: La nota mínima aprobatoria: no puede ser mayor que 20 (se recibió 20.5).
   [RECHAZADO] nota = -1
               ValueError: La nota mínima aprobatoria: no puede ser menor que 0 (se recibió -1).

R24. El estado solo puede ser 1, 2, 3 o 4 (Enum EstadoPeriodo)
   [ACEPTADO]  estado = 2 (número de la base de datos) -> EstadoPeriodo.EN_CURSO
   [ACEPTADO]  estado = EstadoPeriodo.FINALIZADO -> EstadoPeriodo.FINALIZADO
   [RECHAZADO] estado = 7
               ValueError: El estado: solo puede ser 1 (planificado), 2 (en curso), 3 (matrícula cerrada) o 4 (finalizado); se recibió 7.

==============================================================================
PERSONAS
==============================================================================

R25. Nunca se registra a alguien que sea solo persona
   [ACEPTADO]  crear un Estudiante -> Estudiante
   [RECHAZADO] Persona('70123456', 'Ana', 'Quispe')
               TypeError: Can't instantiate abstract class Persona without an implementation for abstract method 'rol'

R26. El nombre completo se calcula a partir de nombres y apellidos
   [ACEPTADO]  nombre completo tras corregir los nombres -> Luis Alberto Pérez Rojas
   [RECHAZADO] docente.nombre_completo = 'X'
               AttributeError: property 'nombre_completo' of 'Docente' object has no setter

R27. El rol es distinto para un estudiante y para un docente
   [ACEPTADO]  rol del estudiante -> Estudiante
   [ACEPTADO]  rol del docente -> Docente
   [ACEPTADO]  str(persona) -> Estudiante: Ana Lucía Quispe Huamán (DNI 70123456)
   [ACEPTADO]  str(persona) -> Docente: Luis Alberto Pérez Rojas (DNI 40123456)
   [RECHAZADO] subclase de Persona que no define rol
               TypeError: Can't instantiate abstract class PersonaSinRol without an implementation for abstract method 'rol'

==============================================================================
ABSTRACCIÓN Y POLIMORFISMO
==============================================================================

R28. RegistroAcademico es abstracto y obliga a implementar su contrato
   [ACEPTADO]  Curso implementa longitud_maxima_nombre y resumen() -> 200
   [RECHAZADO] RegistroAcademico('X')
               TypeError: Can't instantiate abstract class RegistroAcademico without an implementation for abstract methods 'longitud_maxima_nombre', 'resumen'
   [RECHAZADO] subclase que no implementa resumen()
               TypeError: Can't instantiate abstract class RegistroSinResumen without an implementation for abstract method 'resumen'

R29. Recorrer una lista mixta pidiendo un resumen, sin isinstance
   [ACEPTADO]  resumen() -> [Curso #10] IS-282 - Programación Orientada a Objetos | 4 créditos | 6 h totales (T:2 P:4 S:0 V:0)
   [ACEPTADO]  resumen() -> [Plan de estudios] Plan 2018 (2018) - escuela IS | 220 créditos (Oblig:180 Elect:30 Extra:10) | vigente
   [ACEPTADO]  resumen() -> [Escuela profesional] IS - Ingeniería de Sistemas | director: DOC-001 | secretario académico: DOC-002
   [ACEPTADO]  resumen() -> [Periodo académico] Segundo semestre académico 2026 | 2026-08-17 a 2026-12-18 | matrícula 2026-08-03 a 2026-08-14 | nota mínima 10.5 | estado PLANIFICADO

==============================================================================
RESULTADO: 72/72 comprobaciones correctas
==============================================================================
```

</details>
