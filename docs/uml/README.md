# Diagrama de clases UML

![Diagrama de clases](diagrama_clases.png)

## Convenciones

| Símbolo | Significado |
|---|---|
| `-` | Atributo privado (en Python, prefijo `_`) |
| `+` | Miembro público |
| `«get»` | Propiedad de solo lectura (`@property` sin setter) |
| `«get/set»` | Propiedad con setter que valida |
| `«get, calculado»` | Propiedad calculada: no se guarda |
| *cursiva* | Método o propiedad abstracta (`@abstractmethod`) |
| subrayado | Miembro de clase (estático) |
| `«abstract»` | Clase abstracta: no se puede instanciar |
| flecha con triángulo | Herencia («es un») |
| flecha punteada | Referencia solo por código (texto), según la restricción del encargo |

## Código fuente del diagrama (GitHub lo dibuja automáticamente)

```mermaid
classDiagram
    direction TB

    class RegistroAcademico {
        <<abstract>>
        -_nombre : str
        +nombre : str «get/set»
        +longitud_maxima_nombre()* int «get»
        +resumen()* str
        +#95;#95;str#95;#95;() str
    }

    class Curso {
        +LONGITUD_MAXIMA_NOMBRE : int = 200$
        +HORAS_MAXIMAS : int = 255$
        -_ultimo_id : int$
        -_id : int
        -_codigo : str
        -_creditos : Decimal
        -_horas_teoricas : int
        -_horas_practicas : int
        -_horas_seminario : int
        -_horas_virtuales : int
        +id : int «get»
        +codigo : str «get/set»
        +creditos : Decimal «get/set»
        +horas_teoricas : int «get/set»
        +horas_practicas : int «get/set»
        +horas_seminario : int «get/set»
        +horas_virtuales : int «get/set»
        +horas_totales : int «get, calculado»
        +longitud_maxima_nombre() int «get»
        +resumen() str
    }

    class PlanEstudios {
        +LONGITUD_MAXIMA_NOMBRE : int = 36$
        -_anio_aprobacion : int
        -_codigo_escuela : str
        -_creditos_obligatorios : Decimal
        -_creditos_electivos : Decimal
        -_creditos_extracurriculares : Decimal
        -_vigente : int 0 o 1
        -_es_nuevo : int 0 o 1
        +anio_aprobacion : int «get/set»
        +codigo_escuela : str «get/set»
        +creditos_obligatorios : Decimal «get/set»
        +creditos_electivos : Decimal «get/set»
        +creditos_extracurriculares : Decimal «get/set»
        +creditos_totales : Decimal «get, calculado»
        +vigente : bool «get/set»
        +es_nuevo : bool «get/set»
        +longitud_maxima_nombre() int «get»
        +resumen() str
    }

    class EscuelaProfesional {
        +LONGITUD_MAXIMA_NOMBRE : int = 100$
        -_codigo : str
        -_informacion_general : str
        -_perfil_egresado : str
        -_codigo_director : str
        -_codigo_secretario_academico : str
        +codigo : str «get/set»
        +informacion_general : str «get/set»
        +perfil_egresado : str «get/set»
        +codigo_director : str «get/set»
        +codigo_secretario_academico : str «get/set»
        +longitud_maxima_nombre() int «get»
        +resumen() str
    }

    class PeriodoAcademico {
        +LONGITUD_MAXIMA_NOMBRE : int = 45$
        -_numero : int
        -_anio : int
        -_fecha_inicio : date
        -_fecha_fin : date
        -_fecha_inicio_matricula : date
        -_fecha_fin_matricula : date
        -_es_verano : int 0 o 1
        -_nota_minima_aprobatoria : Decimal
        -_estado : EstadoPeriodo
        +numero : int «get/set»
        +anio : int «get/set»
        +codigo : str «get, calculado»
        +fecha_inicio : date «get»
        +fecha_fin : date «get»
        +fecha_inicio_matricula : date «get»
        +fecha_fin_matricula : date «get»
        +es_verano : bool «get/set»
        +nota_minima_aprobatoria : Decimal «get/set»
        +estado : EstadoPeriodo «get/set»
        +cambiar_fechas(inicio, fin) None
        +cambiar_fechas_matricula(inicio, fin) None
        +longitud_maxima_nombre() int «get»
        +resumen() str
    }

    class EstadoPeriodo {
        <<enumeration>>
        PLANIFICADO = 1
        EN_CURSO = 2
        MATRICULA_CERRADA = 3
        FINALIZADO = 4
        +descripcion : str «get»
        +desde_numero(numero)$ EstadoPeriodo
    }

    class Seccion {
        -_codigo : str
        -_codigo_curso : str
        -_codigo_periodo : str
        -_vacantes : int
        -_matriculados : int
        +codigo : str «get/set»
        +codigo_curso : str «get/set»
        +codigo_periodo : str «get/set»
        +vacantes : int «get/set»
        +matriculados : int «get»
        +vacantes_disponibles : int «get, calculado»
        +esta_llena : bool «get, calculado»
        +matricular() None
        +retirar() None
        +#95;#95;str#95;#95;() str
    }

    class Persona {
        <<abstract>>
        -_dni : str
        -_nombres : str
        -_apellidos : str
        +dni : str «get/set»
        +nombres : str «get/set»
        +apellidos : str «get/set»
        +nombre_completo : str «get, calculado»
        +rol()* str «get»
        +#95;#95;str#95;#95;() str
    }

    class Estudiante {
        -_codigo_estudiante : str
        -_codigo_escuela : str
        +codigo_estudiante : str «get/set»
        +codigo_escuela : str «get/set»
        +rol() str «get»
        +#95;#95;str#95;#95;() str
    }

    class Docente {
        -_codigo_docente : str
        +codigo_docente : str «get/set»
        +rol() str «get»
        +#95;#95;str#95;#95;() str
    }

    RegistroAcademico <|-- Curso
    RegistroAcademico <|-- PlanEstudios
    RegistroAcademico <|-- EscuelaProfesional
    RegistroAcademico <|-- PeriodoAcademico
    Persona <|-- Estudiante
    Persona <|-- Docente

    PeriodoAcademico --> EstadoPeriodo : estado
    Seccion ..> Curso : codigo_curso
    Seccion ..> PeriodoAcademico : codigo_periodo
    PlanEstudios ..> EscuelaProfesional : codigo_escuela
    Estudiante ..> EscuelaProfesional : codigo_escuela
    EscuelaProfesional ..> Docente : codigo_director / codigo_secretario_academico
```
