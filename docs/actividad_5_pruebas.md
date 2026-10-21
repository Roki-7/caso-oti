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

Resultado: **70/70 comprobaciones correctas**. La salida completa está en [`salida_programa_prueba.txt`](salida_programa_prueba.txt).

## Reglas probadas (todas tomadas del texto del caso)

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
| R27 | Persona | Rol distinto por subclase | «esa respuesta es distinta para un estudiante y para un docente» | «Estudiante» y «Docente» | Subclase sin `rol` | TypeError |
| R28 | RegistroAcademico | Clase abstracta con contrato | Actividad 3.1 y 3.2 | Curso implementa todo | `RegistroAcademico("X")` y subclase sin `resumen()` | TypeError |
| R29 | Todas | Polimorfismo sin `isinstance` | «pedirle a cada uno un resumen de sí mismo, sin tener que preguntar qué tipo de registro es» | Resumen de los 4 tipos | — | — |

## Puntos que el caso no define

Estos son los únicos valores que el código necesita y que el texto no indica:

| Punto | Qué se hizo |
|---|---|
| Tamaño máximo del nombre de la escuela | El caso exige validarlo pero no da el número; se asume 100 caracteres |
| Cómo se genera el id del curso | El caso solo dice que «el sistema genera» el id; se usa un contador interno (1, 2, 3…) |
| Fecha de fin igual a la de inicio | El caso solo prohíbe que sea **anterior**, así que el mismo día se acepta |
| Retirar de una sección sin matriculados | Se rechaza, porque los matriculados nunca pueden ser negativos |

Códigos, DNI, nombres, apellidos, años y número del periodo **no tienen reglas en el caso**: solo se verifica su tipo de dato (texto o entero).
