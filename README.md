# Caso OTI

Trabajo del curso de **Programación Orientada a Objetos** (2026-II).

La OTI de la universidad usa una base de datos que guarda la información, pero no la cuida. Se encontraron secciones con más matriculados que vacantes, periodos que terminaban antes de empezar y planes de estudio cuyo total de créditos no coincidía con la suma de sus partes. Este proyecto diseña e implementa en Python un sistema de clases que **impide** esos errores, aplicando encapsulamiento, abstracción, herencia y polimorfismo.

## Entregables

| N.º | Entregable | Archivo |
|:---:|---|---|
| 1 | Ficha de la Actividad 1 | [1_ficha_actividad_1.md](1_ficha_actividad_1.md) |
| 3 | Desarrollo de las actividades 2 a 5 | [3_desarrollo_actividades.md](3_desarrollo_actividades.md) |
| — | Código en Python y programa de prueba | [codigo/](codigo/) |

## Clases del sistema

| Clase | Descripción |
|---|---|
| `RegistroAcademico` | Clase abstracta: valida el nombre y exige un `resumen()` |
| `Curso`, `PlanEstudios`, `EscuelaProfesional`, `PeriodoAcademico` | Heredan de `RegistroAcademico` |
| `EstadoPeriodo` | Enumeración del estado del periodo (1 a 4) |
| `Seccion` | Controla vacantes y matriculados |
| `Persona` | Clase abstracta: exige un `rol` |
| `Estudiante`, `Docente` | Heredan de `Persona` |

## Ejecución

Requiere Python 3.10 o superior. Desde la carpeta raíz:

```bash
python codigo/programa_prueba.py
```

Para cada regla del caso, el programa muestra un dato válido aceptado y uno inválido rechazado:

```
R09. Si la sección está llena, la matrícula se rechaza
   [ACEPTADO]  segunda matrícula en sección de 2 vacantes -> 2/2
   [RECHAZADO] tercera matrícula con la sección llena
               ValueError: La sección IS282-B está llena (2 vacantes ocupadas).
...
RESULTADO: 72/72 comprobaciones correctas
```
