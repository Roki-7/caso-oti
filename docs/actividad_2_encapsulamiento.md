# Actividad 2: Encapsulamiento

Todos los datos se guardan en atributos **privados** con doble guion bajo (`__`), que es la convención de Python para lo privado: Python cambia internamente su nombre (*name mangling*), así que `curso.__creditos` no existe fuera de la clase. Se acceden solo mediante `@property`. Así cada asignación pasa por un setter que valida, y un dato inválido nunca llega a guardarse. Las validaciones comunes están en `oti/base/validaciones.py`. Solo se validan las reglas que dice el caso; los demás datos (códigos, DNI, nombres, apellidos, años) solo se verifican por tipo.

## 2.1 Datos protegidos y su regla de validación

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

**Decisión técnica:** créditos y nota se guardan como `Decimal` y no como `float`. En `float`, `0.1 + 0.2` da `0.30000000000000004`, y no se puede contar con exactitud cuántos decimales tiene un número, que es justamente lo que pide la regla de créditos.

## 2.2 Datos que no se guardan, sino que se calculan

| Clase | Dato calculado | Fórmula |
|---|---|---|
| Curso | `horas_totales` | teóricas + prácticas + seminario + virtuales |
| PlanEstudios | `creditos_totales` | obligatorios + electivos + extracurriculares |
| Seccion | `vacantes_disponibles` | vacantes − matriculados |
| Persona | `nombre_completo` | nombres + « » + apellidos |

**Problema que evita:** la **inconsistencia por redundancia** (anomalía de actualización). Si un dato derivado se guarda aparte, cada vez que alguien corrige una de sus partes debe acordarse de actualizar también el total. Basta un olvido para que el total quede mal, que es exactamente lo que encontró la OTI: «planes de estudio cuyo total de créditos no coincidía con la suma de sus partes» y «cada vez que alguien corrige una hora y olvida actualizar el total, el dato queda mal». Al calcularlo en cada consulta, el total siempre coincide con sus partes porque no existe una copia que pueda desactualizarse.

## 2.3 Datos que no se pueden modificar directamente

| Dato | ¿Cómo cambia? | Qué pasa si se intenta asignar |
|---|---|---|
| `Curso.id` | Nunca: lo genera el sistema al crear el curso | `AttributeError` (propiedad sin setter) |
| `Seccion.matriculados` | Solo con `matricular()` (+1) y `retirar()` (−1) | `AttributeError` |
| `PeriodoAcademico.fecha_inicio` / `fecha_fin` | Solo con `cambiar_fechas(inicio, fin)` | `AttributeError` |
| `PeriodoAcademico.fecha_inicio_matricula` / `fecha_fin_matricula` | Solo con `cambiar_fechas_matricula(inicio, fin)` | `AttributeError` |
| Todos los datos calculados de 2.2 | Cambian solos al modificar sus partes | `AttributeError` |

**¿Por qué las fechas se cambian juntas?** Si hubiera un setter para cada fecha, mover un periodo de marzo–julio a agosto–diciembre sería imposible: al cambiar primero el inicio a agosto, el objeto quedaría con «inicio agosto, fin julio» y la validación lo rechazaría. Con `cambiar_fechas()` ambas fechas se validan como pareja y se asignan solo si son correctas, así que el objeto nunca queda en un estado intermedio inválido.

## 2.4 Datos que se guardan con un tipo y se entregan con otro

| Dato | Se guarda como | Se entrega como |
|---|---|---|
| `PlanEstudios.vigente` | `int` (0 o 1) en `__vigente` | `bool` |
| `PlanEstudios.es_nuevo` | `int` (0 o 1) en `__es_nuevo` | `bool` |
| `PeriodoAcademico.es_verano` | `int` (0 o 1) en `__es_verano` | `bool` |
El setter acepta tanto `True/False` como `0/1` (lo que llega de la base de datos) y siempre guarda el entero. El getter convierte a `bool`. De este modo se respeta el formato de la base de datos y quien consulta recibe una respuesta clara: «verdadero o falso».

**Caso relacionado (`PeriodoAcademico.estado`):** el setter **recibe** el número `int` (1–4) que llega de la base de datos, pero lo **guarda y lo entrega** como `EstadoPeriodo` (Enum). Aquí la conversión ocurre al recibir el dato, no al entregarlo; se explica en la Actividad 3.3.
