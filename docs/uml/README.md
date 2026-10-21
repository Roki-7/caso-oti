# Diagrama de clases UML

![Diagrama de clases](diagrama_clases.png)

## Convenciones

| Símbolo | Significado |
|---|---|
| `-` | Atributo privado (en Python, prefijo `_`) |
| `+` | Miembro público |
| `«property»` | Propiedad (`@property`) |
| `{readOnly}` / `«readOnly»` | Propiedad sin setter |
| `/nombre` | Atributo derivado: se calcula, no se guarda |
| *cursiva* / `{abstract}` | Método o propiedad abstracta (`@abstractmethod`) |
| `«abstract»` | Clase abstracta: no se puede instanciar |
| flecha con triángulo | Herencia («es un») |

El archivo editable para draw.io es [`diagrama_clases.drawio`](diagrama_clases.drawio) (ábrelo en app.diagrams.net). Las referencias entre registros (sección → curso, escuela → director, etc.) son atributos `str` por la restricción del encargo, por eso no se dibujan como flechas.

## Código fuente del diagrama (GitHub lo dibuja automáticamente)

```mermaid
classDiagram
    direction TB

    class RegistroAcademico {
        <<abstract>>
        -_nombre : str
        +nombre : str «property»
        +longitud_maxima_nombre : int «property» «abstract»
        +resumen()* str
    }

    class Curso {
        -_id : int
        -_codigo : str
        -_creditos : Decimal
        -_horas_teoricas : int
        -_horas_practicas : int
        -_horas_seminario : int
        -_horas_virtuales : int
        +id : int «property» «readOnly»
        +codigo : str «property»
        +creditos : Decimal «property»
        +horas_teoricas : int «property»
        +horas_practicas : int «property»
        +horas_seminario : int «property»
        +horas_virtuales : int «property»
        +/horas_totales : int «property» «readOnly»
        +longitud_maxima_nombre : int «property»
        +resumen() str
    }

    class PeriodoAcademico {
        -_numero : int
        -_anio : int
        -_fecha_inicio : date
        -_fecha_fin : date
        -_fecha_inicio_matricula : date
        -_fecha_fin_matricula : date
        -_es_verano : int
        -_nota_minima_aprobatoria : Decimal
        -_estado : EstadoPeriodo
        +numero : int «property»
        +anio : int «property»
        +fecha_inicio : date «property» «readOnly»
        +fecha_fin : date «property» «readOnly»
        +fecha_inicio_matricula : date «property» «readOnly»
        +fecha_fin_matricula : date «property» «readOnly»
        +es_verano : bool «property»
        +nota_minima_aprobatoria : Decimal «property»
        +estado : EstadoPeriodo «property»
        +longitud_maxima_nombre : int «property»
        +cambiar_fechas(inicio: date, fin: date) None
        +cambiar_fechas_matricula(inicio: date, fin: date) None
        +resumen() str
    }

    class PlanEstudios {
        -_anio_aprobacion : int
        -_creditos_obligatorios : Decimal
        -_creditos_electivos : Decimal
        -_creditos_extracurriculares : Decimal
        -_vigente : int
        -_es_nuevo : int
        +anio_aprobacion : int «property»
        +creditos_obligatorios : Decimal «property»
        +creditos_electivos : Decimal «property»
        +creditos_extracurriculares : Decimal «property»
        +/creditos_totales : Decimal «property» «readOnly»
        +vigente : bool «property»
        +es_nuevo : bool «property»
        +longitud_maxima_nombre : int «property»
        +resumen() str
    }

    class EscuelaProfesional {
        -_codigo : str
        -_informacion_general : str
        -_perfil_egresado : str
        -_codigo_director : str
        -_codigo_secretario_academico : str
        +codigo : str «property»
        +informacion_general : str «property»
        +perfil_egresado : str «property»
        +codigo_director : str «property»
        +codigo_secretario_academico : str «property»
        +longitud_maxima_nombre : int «property»
        +resumen() str
    }

    class Persona {
        <<abstract>>
        -_dni : str
        -_nombres : str
        -_apellidos : str
        +dni : str «property»
        +nombres : str «property»
        +apellidos : str «property»
        +/nombre_completo : str «property» «readOnly»
        +rol : str «property» «abstract»
        +#95;#95;str#95;#95;() str
    }

    class Estudiante {
        -_codigo_estudiante : str
        -_codigo_escuela : str
        +codigo_estudiante : str «property»
        +codigo_escuela : str «property»
        +rol : str «property»
    }

    class Docente {
        -_codigo_docente : str
        +codigo_docente : str «property»
        +rol : str «property»
    }

    class Seccion {
        -_codigo : str
        -_codigo_curso : str
        -_codigo_periodo : str
        -_vacantes : int
        -_matriculados : int
        +codigo : str «property»
        +codigo_curso : str «property»
        +codigo_periodo : str «property»
        +vacantes : int «property»
        +matriculados : int «property» «readOnly»
        +/vacantes_disponibles : int «property» «readOnly»
        +matricular() None
        +retirar() None
    }

    class EstadoPeriodo {
        <<enumeration>>
        PLANIFICADO = 1
        EN_CURSO = 2
        MATRICULA_CERRADA = 3
        FINALIZADO = 4
    }

    RegistroAcademico <|-- Curso
    RegistroAcademico <|-- PeriodoAcademico
    RegistroAcademico <|-- PlanEstudios
    RegistroAcademico <|-- EscuelaProfesional
    Persona <|-- Estudiante
    Persona <|-- Docente
    PeriodoAcademico --> EstadoPeriodo : estado
```
