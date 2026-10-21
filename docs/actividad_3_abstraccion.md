# Actividad 3: Abstracción

## 3.1 Lo que varias clases tienen en común

Según el pedido final de la jefatura, `Curso`, `PlanEstudios`, `EscuelaProfesional` y `PeriodoAcademico` son «cosas muy distintas», pero comparten dos cosas:

1. **Un nombre que debe validarse**, con un tamaño máximo distinto en cada clase.
2. **La capacidad de dar un resumen de sí mismos.**

Eso se define como la clase abstracta `RegistroAcademico` (`oti/base/registro_academico.py`), que hereda de `ABC`:

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
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = validar_texto(valor, "El nombre", self.longitud_maxima_nombre)
```

La validación del nombre se escribe **una sola vez** en la clase base. Cada subclase solo indica su límite. Si mañana cambia la regla (por ejemplo, prohibir caracteres especiales), se modifica en un solo lugar.

Intentar crearla directamente falla:

```
>>> RegistroAcademico("X")
TypeError: Can't instantiate abstract class RegistroAcademico without an
implementation for abstract methods 'longitud_maxima_nombre', 'resumen'
```

**Segunda abstracción:** `Persona` también es abstracta, porque el caso dice «Nunca registramos a alguien que sea solo persona, sin ser estudiante ni docente». Obliga a implementar la propiedad `rol`.

## 3.2 Métodos que la clase abstracta obliga a implementar

| Clase abstracta | Miembro abstracto | Por qué es abstracto |
|---|---|---|
| `RegistroAcademico` | `longitud_maxima_nombre` (propiedad) | El tamaño máximo «cambia en cada caso»: solo cada subclase lo conoce (200, 36, 100, 45) |
| `RegistroAcademico` | `resumen()` | Cada registro se describe distinto; es la base del polimorfismo |
| `Persona` | `rol` (propiedad) | «esa respuesta es distinta para un estudiante y para un docente» |

**Lo que NO es abstracto:** el setter de `nombre`, `nombre_completo` y `__str__` son iguales para todas las subclases, así que se implementan una vez en la clase base y se heredan.

Si una subclase olvida implementar un miembro abstracto, Python impide crearla:

```
>>> class RegistroSinResumen(RegistroAcademico):
...     longitud_maxima_nombre = property(lambda self: 50)
>>> RegistroSinResumen("X")
TypeError: Can't instantiate abstract class RegistroSinResumen without an
implementation for abstract method 'resumen'
```

## 3.3 Mejor representación del estado del periodo

**Problema:** el estado se guarda como un número suelto. «Nadie recuerda qué significa cada número, y ya hemos visto periodos con estado 7».

**Solución:** una enumeración (`oti/enums/estado_periodo.py`):

```python
class EstadoPeriodo(Enum):
    PLANIFICADO = 1
    EN_CURSO = 2
    MATRICULA_CERRADA = 3
    FINALIZADO = 4
```

Ventajas:

1. **Solo existen 4 valores.** `EstadoPeriodo(7)` lanza `ValueError`, así que un estado 7 no puede ni crearse.
2. **El código se lee con nombres**: `periodo.estado = EstadoPeriodo.EN_CURSO` en vez de `periodo.estado = 2`.
3. **Compatible con la base de datos**: `EstadoPeriodo.EN_CURSO.value` devuelve `2` para guardarlo, y `EstadoPeriodo.desde_numero(2)` lo reconstruye al leerlo.
4. **Texto legible**: la propiedad `descripcion` devuelve «En curso», «Matrícula cerrada», etc.

```
>>> periodo.estado = 7
ValueError: Estado de periodo inválido: 7. Valores permitidos: 1=Planificado,
2=En curso, 3=Matrícula cerrada, 4=Finalizado.
```
