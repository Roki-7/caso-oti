"""Genera diagrama_clases.drawio (UML editable en draw.io) solo con lo que dice el caso.

Notación:
    -  atributo privado            +  miembro público
    «property»  propiedad (@property)   {readOnly}  propiedad sin setter
    /nombre     atributo derivado (calculado, no se guarda)
    cursiva + {abstract}  miembro abstracto
"""
import xml.etree.ElementTree as ET
from pathlib import Path

ROW_H = 20
HEADER_H = 26
HEADER_H_STEREO = 40
SEP_H = 8
CHAR_W = 6.6
FONT = 11

# (texto, abstracto)
CLASES = {
    "RegistroAcademico": dict(stereo="abstract", attrs=[
        ("- _nombre: str", False),
        ("+ nombre: str «property»", False),
        ("+ longitud_maxima_nombre: int «property» {abstract}", True),
    ], methods=[
        ("+ resumen(): str {abstract}", True),
    ]),
    "Curso": dict(attrs=[
        ("- _id: int", False),
        ("- _codigo: str", False),
        ("- _creditos: Decimal", False),
        ("- _horas_teoricas: int", False),
        ("- _horas_practicas: int", False),
        ("- _horas_seminario: int", False),
        ("- _horas_virtuales: int", False),
        ("+ id: int «property» {readOnly}", False),
        ("+ codigo: str «property»", False),
        ("+ creditos: Decimal «property»", False),
        ("+ horas_teoricas: int «property»", False),
        ("+ horas_practicas: int «property»", False),
        ("+ horas_seminario: int «property»", False),
        ("+ horas_virtuales: int «property»", False),
        ("+ /horas_totales: int «property» {readOnly}", False),
        ("+ longitud_maxima_nombre: int «property»", False),
    ], methods=[
        ("+ resumen(): str", False),
    ]),
    "PeriodoAcademico": dict(attrs=[
        ("- _numero: int", False),
        ("- _anio: int", False),
        ("- _fecha_inicio: date", False),
        ("- _fecha_fin: date", False),
        ("- _fecha_inicio_matricula: date", False),
        ("- _fecha_fin_matricula: date", False),
        ("- _es_verano: int", False),
        ("- _nota_minima_aprobatoria: Decimal", False),
        ("- _estado: EstadoPeriodo", False),
        ("+ numero: int «property»", False),
        ("+ anio: int «property»", False),
        ("+ fecha_inicio: date «property» {readOnly}", False),
        ("+ fecha_fin: date «property» {readOnly}", False),
        ("+ fecha_inicio_matricula: date «property» {readOnly}", False),
        ("+ fecha_fin_matricula: date «property» {readOnly}", False),
        ("+ es_verano: bool «property»", False),
        ("+ nota_minima_aprobatoria: Decimal «property»", False),
        ("+ estado: EstadoPeriodo «property»", False),
        ("+ longitud_maxima_nombre: int «property»", False),
    ], methods=[
        ("+ cambiar_fechas(inicio: date, fin: date): None", False),
        ("+ cambiar_fechas_matricula(inicio: date, fin: date): None", False),
        ("+ resumen(): str", False),
    ]),
    "PlanEstudios": dict(attrs=[
        ("- _anio_aprobacion: int", False),
        ("- _creditos_obligatorios: Decimal", False),
        ("- _creditos_electivos: Decimal", False),
        ("- _creditos_extracurriculares: Decimal", False),
        ("- _vigente: int", False),
        ("- _es_nuevo: int", False),
        ("+ anio_aprobacion: int «property»", False),
        ("+ creditos_obligatorios: Decimal «property»", False),
        ("+ creditos_electivos: Decimal «property»", False),
        ("+ creditos_extracurriculares: Decimal «property»", False),
        ("+ /creditos_totales: Decimal «property» {readOnly}", False),
        ("+ vigente: bool «property»", False),
        ("+ es_nuevo: bool «property»", False),
        ("+ longitud_maxima_nombre: int «property»", False),
    ], methods=[
        ("+ resumen(): str", False),
    ]),
    "EscuelaProfesional": dict(attrs=[
        ("- _codigo: str", False),
        ("- _informacion_general: str", False),
        ("- _perfil_egresado: str", False),
        ("- _codigo_director: str", False),
        ("- _codigo_secretario_academico: str", False),
        ("+ codigo: str «property»", False),
        ("+ informacion_general: str «property»", False),
        ("+ perfil_egresado: str «property»", False),
        ("+ codigo_director: str «property»", False),
        ("+ codigo_secretario_academico: str «property»", False),
        ("+ longitud_maxima_nombre: int «property»", False),
    ], methods=[
        ("+ resumen(): str", False),
    ]),
    "Persona": dict(stereo="abstract", attrs=[
        ("- _dni: str", False),
        ("- _nombres: str", False),
        ("- _apellidos: str", False),
        ("+ dni: str «property»", False),
        ("+ nombres: str «property»", False),
        ("+ apellidos: str «property»", False),
        ("+ /nombre_completo: str «property» {readOnly}", False),
        ("+ rol: str «property» {abstract}", True),
    ], methods=[
        ("+ __str__(): str", False),
    ]),
    "Estudiante": dict(attrs=[
        ("- _codigo_estudiante: str", False),
        ("- _codigo_escuela: str", False),
        ("+ codigo_estudiante: str «property»", False),
        ("+ codigo_escuela: str «property»", False),
        ("+ rol: str «property»", False),
    ], methods=[]),
    "Docente": dict(attrs=[
        ("- _codigo_docente: str", False),
        ("+ codigo_docente: str «property»", False),
        ("+ rol: str «property»", False),
    ], methods=[]),
    "Seccion": dict(attrs=[
        ("- _codigo: str", False),
        ("- _codigo_curso: str", False),
        ("- _codigo_periodo: str", False),
        ("- _vacantes: int", False),
        ("- _matriculados: int", False),
        ("+ codigo: str «property»", False),
        ("+ codigo_curso: str «property»", False),
        ("+ codigo_periodo: str «property»", False),
        ("+ vacantes: int «property»", False),
        ("+ matriculados: int «property» {readOnly}", False),
        ("+ /vacantes_disponibles: int «property» {readOnly}", False),
    ], methods=[
        ("+ matricular(): None", False),
        ("+ retirar(): None", False),
    ]),
    "EstadoPeriodo": dict(stereo="enumeration", attrs=[
        ("PLANIFICADO = 1", False),
        ("EN_CURSO = 2", False),
        ("MATRICULA_CERRADA = 3", False),
        ("FINALIZADO = 4", False),
    ], methods=None),
}


def ancho(nombre):
    c = CLASES[nombre]
    textos = [t for t, _ in c["attrs"] + (c["methods"] or [])] + [nombre]
    return int(max(len(t) for t in textos) * CHAR_W + 24)


def alto(nombre):
    c = CLASES[nombre]
    cab = HEADER_H_STEREO if c.get("stereo") else HEADER_H
    filas = len(c["attrs"]) + len(c["methods"] or [])
    sep = SEP_H if c["methods"] is not None else 0
    return cab + ROW_H * filas + sep + 6


W = {n: ancho(n) for n in CLASES}
H = {n: alto(n) for n in CLASES}

# ---- Disposición -------------------------------------------------------------
GAP = 40
Y_TOP = 80
Y_MID = Y_TOP + max(H["RegistroAcademico"], H["Persona"]) + 90
fila = ["Curso", "PeriodoAcademico", "PlanEstudios", "EscuelaProfesional"]
POS = {}
x = 40
for n in fila:
    POS[n] = (x, Y_MID)
    x += W[n] + GAP
izq, der = POS["Curso"][0], POS["EscuelaProfesional"][0] + W["EscuelaProfesional"]
POS["RegistroAcademico"] = ((izq + der) / 2 - W["RegistroAcademico"] / 2, Y_TOP)

x_personas = x + 40
POS["Estudiante"] = (x_personas, Y_MID)
POS["Docente"] = (x_personas + W["Estudiante"] + GAP, Y_MID)
izq, der = POS["Estudiante"][0], POS["Docente"][0] + W["Docente"]
POS["Persona"] = ((izq + der) / 2 - W["Persona"] / 2, Y_TOP)

y_bajo = Y_MID + max(H[n] for n in fila) + 80
POS["EstadoPeriodo"] = (POS["PeriodoAcademico"][0] + 60, y_bajo)
POS["Seccion"] = (x_personas, Y_MID + max(H["Estudiante"], H["Docente"]) + 80)

# ---- XML ---------------------------------------------------------------------
mxfile = ET.Element("mxfile", host="app.diagrams.net", type="device")
diagram = ET.SubElement(mxfile, "diagram", id="caso-oti-uml", name="Diagrama de clases")
model = ET.SubElement(diagram, "mxGraphModel", dx="1600", dy="1000", grid="1", gridSize="10",
                      guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1",
                      pageScale="1", pageWidth="2600", pageHeight="1600", math="0", shadow="0")
root = ET.SubElement(model, "root")
ET.SubElement(root, "mxCell", id="0")
ET.SubElement(root, "mxCell", id="1", parent="0")
contador = [0]


def nuevo_id(prefijo):
    contador[0] += 1
    return f"{prefijo}-{contador[0]}"


def geom(cell, x, y, w, h):
    g = ET.SubElement(cell, "mxGeometry", x=str(int(x)), y=str(int(y)), width=str(int(w)),
                      height=str(int(h)))
    g.set("as", "geometry")


ESTILO_FILA = ("text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;"
               "spacingLeft=6;spacingRight=4;overflow=hidden;rotatable=0;"
               "points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;"
               f"fontSize={FONT};")
ESTILO_SEP = ("line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;"
              "spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=right;points=[];"
              "portConstraint=eastwest;strokeColor=inherit;")


def fila_texto(cid, texto, abstracto, y, w):
    estilo = ESTILO_FILA + ("fontStyle=2;" if abstracto else "fontStyle=0;")
    c = ET.SubElement(root, "mxCell", id=nuevo_id(cid), value=texto, style=estilo,
                      vertex="1", parent=cid)
    geom(c, 0, y, w, ROW_H)


for nombre, c in CLASES.items():
    x, y = POS[nombre]
    stereo = c.get("stereo")
    cab = HEADER_H_STEREO if stereo else HEADER_H
    if stereo == "abstract":
        valor, fs = f"«abstract»<br><b><i>{nombre}</i></b>", 0
    elif stereo:
        valor, fs = f"«{stereo}»<br><b>{nombre}</b>", 0
    else:
        valor, fs = nombre, 1
    estilo = (f"swimlane;fontStyle={fs};align=center;verticalAlign=top;childLayout=stackLayout;"
              f"horizontal=1;startSize={cab};horizontalStack=0;resizeParent=1;resizeParentMax=0;"
              "resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fontSize=12;"
              "fillColor=#ffffff;strokeColor=#000000;")
    cell = ET.SubElement(root, "mxCell", id=nombre, value=valor, style=estilo, vertex="1",
                         parent="1")
    geom(cell, x, y, W[nombre], H[nombre])
    yy = cab
    for texto, abstracto in c["attrs"]:
        fila_texto(nombre, texto, abstracto, yy, W[nombre])
        yy += ROW_H
    if c["methods"] is not None:
        sep = ET.SubElement(root, "mxCell", id=nuevo_id(nombre), value="", style=ESTILO_SEP,
                            vertex="1", parent=nombre)
        geom(sep, 0, yy, W[nombre], SEP_H)
        yy += SEP_H
        for texto, abstracto in c["methods"]:
            fila_texto(nombre, texto, abstracto, yy, W[nombre])
            yy += ROW_H


def arista(origen, destino, estilo, etiqueta=""):
    e = ET.SubElement(root, "mxCell", id=nuevo_id("rel"), value=etiqueta, style=estilo,
                      edge="1", parent="1", source=origen, target=destino)
    g = ET.SubElement(e, "mxGeometry", relative="1")
    g.set("as", "geometry")


# Herencia («es un»)
HERENCIA = ("endArrow=block;endSize=16;endFill=0;html=1;rounded=0;edgeStyle=orthogonalEdgeStyle;"
            "exitX=0.5;exitY=0;entryX=0.5;entryY=1;")
for hijo in fila:
    arista(hijo, "RegistroAcademico", HERENCIA)
for hijo in ["Estudiante", "Docente"]:
    arista(hijo, "Persona", HERENCIA)

# Asociación: el periodo usa el Enum para su estado (Actividad 3.3)
arista("PeriodoAcademico", "EstadoPeriodo",
       "endArrow=open;endSize=12;html=1;rounded=0;edgeStyle=orthogonalEdgeStyle;fontSize=10;"
       "labelBackgroundColor=#ffffff;exitX=0.3;exitY=1;entryX=0.5;entryY=0;", "estado")

# Título y leyenda
titulo = ET.SubElement(root, "mxCell", id="titulo", value="<b>Caso OTI - Diagrama de clases UML</b>",
                       style="text;html=1;align=left;verticalAlign=middle;fontSize=18;",
                       vertex="1", parent="1")
geom(titulo, 40, 20, 500, 34)

leyenda_txt = (
    "<b>Notación</b><br>"
    "<b>-</b> atributo privado &nbsp; <b>+</b> público<br>"
    "«property» propiedad (@property)<br>"
    "{readOnly} propiedad sin setter<br>"
    "<b>/</b>nombre atributo calculado (no se guarda)<br>"
    "<i>cursiva</i> {abstract} miembro abstracto<br>"
    "Triángulo hueco: herencia («es un»)"
)
leyenda = ET.SubElement(root, "mxCell", id="leyenda", value=leyenda_txt,
                        style="rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;"
                              "spacing=10;fillColor=#ffffff;strokeColor=#999999;fontSize=11;",
                        vertex="1", parent="1")
x_ley = POS["EstadoPeriodo"][0] + W["EstadoPeriodo"] + 60
geom(leyenda, x_ley, POS["EstadoPeriodo"][1], 290, 140)

ET.indent(mxfile, space="  ")
salida = Path(__file__).with_name("diagrama_clases.drawio")
ET.ElementTree(mxfile).write(salida, encoding="utf-8", xml_declaration=False)

# Comprobación de solapamientos
cajas = {n: (POS[n][0], POS[n][1], W[n], H[n]) for n in CLASES}
cajas["leyenda"] = (x_ley, POS["EstadoPeriodo"][1], 290, 140)
nombres = list(cajas)
for i, a in enumerate(nombres):
    for b in nombres[i + 1:]:
        ax, ay, aw, ah = cajas[a]
        bx, by, bw, bh = cajas[b]
        if ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah:
            print("SOLAPA:", a, b)
print("ok", salida)
