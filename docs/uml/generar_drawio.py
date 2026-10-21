"""Genera diagrama_clases.drawio (UML a colores, editable en draw.io) y diagrama_clases.mmd.

Todo el contenido sale del texto del caso. Cada clase tiene tres compartimentos:
    1. atributos privados (con las restricciones del caso entre llaves)
    2. propiedades (@property), con fondo tenue
    3. métodos

Notación:
    -  privado    +  público    «property»  propiedad    {readOnly}  sin setter
    /nombre  atributo derivado (calculado)    {…}  restricción indicada en el caso
    texto rojo en cursiva  miembro abstracto
"""
import xml.etree.ElementTree as ET
from pathlib import Path

ROW_H = 20
HEADER_H = 28
HEADER_H_STEREO = 42
SEP_H = 8
CHAR_W = 6.5
FONT = 11
ROJO = "#B85450"

# Paleta por grupo: (cabecera, borde, fondo tenue de propiedades)
PALETA = {
    "abstracta": ("#DAE8FC", "#6C8EBF", "#F3F7FD"),
    "registro": ("#D5E8D4", "#82B366", "#F2F8F1"),
    "persona": ("#FFE6CC", "#D79B00", "#FFF7EE"),
    "independiente": ("#F8CECC", "#B85450", "#FDF3F3"),
    "enumeracion": ("#E1D5E7", "#9673A6", "#F7F2F9"),
}

# Miembro: (texto, abstracto)
A = True
CLASES = {
    "RegistroAcademico": dict(grupo="abstracta", estereotipo="abstract",
        privados=[("- __nombre: str {no vacío, máx. longitud_maxima_nombre}", 0)],
        propiedades=[("+ nombre: str «property»", 0),
                     ("+ longitud_maxima_nombre: int «property» {abstract}", A)],
        metodos=[("+ resumen(): str {abstract}", A)]),

    "Curso": dict(grupo="registro",
        privados=[("- __id: int", 0),
                  ("- __codigo: str", 0),
                  ("- __creditos: Decimal {> 0, máx. 2 decimales}", 0),
                  ("- __horas_teoricas: int {0..255}", 0),
                  ("- __horas_practicas: int {0..255}", 0),
                  ("- __horas_seminario: int {0..255}", 0),
                  ("- __horas_virtuales: int {0..255}", 0)],
        propiedades=[("+ id: int «property» {readOnly}", 0),
                     ("+ codigo: str «property»", 0),
                     ("+ creditos: Decimal «property»", 0),
                     ("+ horas_teoricas: int «property»", 0),
                     ("+ horas_practicas: int «property»", 0),
                     ("+ horas_seminario: int «property»", 0),
                     ("+ horas_virtuales: int «property»", 0),
                     ("+ /horas_totales: int «property» {readOnly}", 0),
                     ("+ longitud_maxima_nombre: int «property» {= 200}", 0)],
        metodos=[("+ resumen(): str", 0)]),

    "PeriodoAcademico": dict(grupo="registro",
        privados=[("- __numero: int", 0),
                  ("- __anio: int", 0),
                  ("- __fecha_inicio: date", 0),
                  ("- __fecha_fin: date {≥ fecha_inicio}", 0),
                  ("- __fecha_inicio_matricula: date", 0),
                  ("- __fecha_fin_matricula: date {≥ fecha_inicio_matricula}", 0),
                  ("- __es_verano: int {0 o 1}", 0),
                  ("- __nota_minima_aprobatoria: Decimal {0..20}", 0)],
        propiedades=[("+ numero: int «property»", 0),
                     ("+ anio: int «property»", 0),
                     ("+ fecha_inicio: date «property» {readOnly}", 0),
                     ("+ fecha_fin: date «property» {readOnly}", 0),
                     ("+ fecha_inicio_matricula: date «property» {readOnly}", 0),
                     ("+ fecha_fin_matricula: date «property» {readOnly}", 0),
                     ("+ es_verano: bool «property»", 0),
                     ("+ nota_minima_aprobatoria: Decimal «property»", 0),
                     ("+ estado: EstadoPeriodo «property»", 0),
                     ("+ longitud_maxima_nombre: int «property» {= 45}", 0)],
        metodos=[("+ cambiar_fechas(inicio: date, fin: date): None", 0),
                 ("+ cambiar_fechas_matricula(inicio: date, fin: date): None", 0),
                 ("+ resumen(): str", 0)]),

    "PlanEstudios": dict(grupo="registro",
        privados=[("- __anio_aprobacion: int", 0),
                  ("- __codigo_escuela: str", 0),
                  ("- __creditos_obligatorios: Decimal {≥ 0}", 0),
                  ("- __creditos_electivos: Decimal {≥ 0}", 0),
                  ("- __creditos_extracurriculares: Decimal {≥ 0}", 0),
                  ("- __vigente: int {0 o 1}", 0),
                  ("- __es_nuevo: int {0 o 1}", 0)],
        propiedades=[("+ anio_aprobacion: int «property»", 0),
                     ("+ codigo_escuela: str «property»", 0),
                     ("+ creditos_obligatorios: Decimal «property»", 0),
                     ("+ creditos_electivos: Decimal «property»", 0),
                     ("+ creditos_extracurriculares: Decimal «property»", 0),
                     ("+ /creditos_totales: Decimal «property» {readOnly}", 0),
                     ("+ vigente: bool «property»", 0),
                     ("+ es_nuevo: bool «property»", 0),
                     ("+ longitud_maxima_nombre: int «property» {= 36}", 0)],
        metodos=[("+ resumen(): str", 0)]),

    "EscuelaProfesional": dict(grupo="registro",
        privados=[("- __codigo: str", 0),
                  ("- __informacion_general: str", 0),
                  ("- __perfil_egresado: str", 0),
                  ("- __codigo_director: str", 0),
                  ("- __codigo_secretario_academico: str", 0)],
        propiedades=[("+ codigo: str «property»", 0),
                     ("+ informacion_general: str «property»", 0),
                     ("+ perfil_egresado: str «property»", 0),
                     ("+ codigo_director: str «property»", 0),
                     ("+ codigo_secretario_academico: str «property»", 0),
                     ("+ longitud_maxima_nombre: int «property» {= 100, asumido}", 0)],
        metodos=[("+ resumen(): str", 0)]),

    "Persona": dict(grupo="abstracta", estereotipo="abstract",
        privados=[("- __dni: str", 0),
                  ("- __nombres: str", 0),
                  ("- __apellidos: str", 0)],
        propiedades=[("+ dni: str «property»", 0),
                     ("+ nombres: str «property»", 0),
                     ("+ apellidos: str «property»", 0),
                     ("+ /nombre_completo: str «property» {readOnly}", 0),
                     ("+ rol: str «property» {abstract}", A)],
        metodos=[("+ __str__(): str", 0)]),

    "Estudiante": dict(grupo="persona",
        privados=[("- __codigo_estudiante: str", 0),
                  ("- __codigo_escuela: str", 0)],
        propiedades=[("+ codigo_estudiante: str «property»", 0),
                     ("+ codigo_escuela: str «property»", 0),
                     ("+ rol: str «property» {= \"Estudiante\"}", 0)],
        metodos=[]),

    "Docente": dict(grupo="persona",
        privados=[("- __codigo_docente: str", 0)],
        propiedades=[("+ codigo_docente: str «property»", 0),
                     ("+ rol: str «property» {= \"Docente\"}", 0)],
        metodos=[]),

    "Seccion": dict(grupo="independiente",
        privados=[("- __codigo: str", 0),
                  ("- __codigo_curso: str", 0),
                  ("- __codigo_periodo: str", 0),
                  ("- __vacantes: int {> 0, ≥ matriculados}", 0),
                  ("- __matriculados: int {≥ 0, ≤ vacantes}", 0)],
        propiedades=[("+ codigo: str «property»", 0),
                     ("+ codigo_curso: str «property»", 0),
                     ("+ codigo_periodo: str «property»", 0),
                     ("+ vacantes: int «property»", 0),
                     ("+ matriculados: int «property» {readOnly}", 0),
                     ("+ /vacantes_disponibles: int «property» {readOnly}", 0)],
        metodos=[("+ matricular(): None", 0),
                 ("+ retirar(): None", 0)]),

    "EstadoPeriodo": dict(grupo="enumeracion", estereotipo="enumeration",
        privados=[("PLANIFICADO = 1", 0),
                  ("EN_CURSO = 2", 0),
                  ("MATRICULA_CERRADA = 3", 0),
                  ("FINALIZADO = 4", 0)],
        propiedades=None, metodos=None),
}


def compartimentos(c):
    return [x for x in (c["privados"], c["propiedades"], c["metodos"]) if x]


def ancho(nombre):
    c = CLASES[nombre]
    textos = [t for comp in compartimentos(c) for t, _ in comp] + [nombre + "    "]
    return int(max(len(t) for t in textos) * CHAR_W + 26)


def alto(nombre):
    c = CLASES[nombre]
    comps = compartimentos(c)
    cab = HEADER_H_STEREO if c.get("estereotipo") else HEADER_H
    return cab + sum(len(x) for x in comps) * ROW_H + (len(comps) - 1) * SEP_H + 6


W = {n: ancho(n) for n in CLASES}
H = {n: alto(n) for n in CLASES}

# ---- Disposición -------------------------------------------------------------
GAP = 40
Y_TOP = 90
Y_MID = Y_TOP + max(H["RegistroAcademico"], H["Persona"]) + 90
FILA_REG = ["Curso", "PeriodoAcademico", "PlanEstudios", "EscuelaProfesional"]
POS = {}
x = 40
for n in FILA_REG:
    POS[n] = (x, Y_MID)
    x += W[n] + GAP
izq, der = POS["Curso"][0], POS["EscuelaProfesional"][0] + W["EscuelaProfesional"]
POS["RegistroAcademico"] = ((izq + der) / 2 - W["RegistroAcademico"] / 2, Y_TOP)

X_PER = x + 60
POS["Estudiante"] = (X_PER, Y_MID)
POS["Docente"] = (X_PER + W["Estudiante"] + GAP, Y_MID)
izq, der = POS["Estudiante"][0], POS["Docente"][0] + W["Docente"]
POS["Persona"] = ((izq + der) / 2 - W["Persona"] / 2, Y_TOP)

Y_SEC = Y_MID + max(H["Estudiante"], H["Docente"]) + 70
POS["Seccion"] = (X_PER, Y_SEC)
Y_BAJO = Y_MID + max(H[n] for n in FILA_REG) + 70
POS["EstadoPeriodo"] = (POS["PeriodoAcademico"][0] + 60, Y_BAJO)

# ---- XML ---------------------------------------------------------------------
mxfile = ET.Element("mxfile", host="app.diagrams.net", type="device")
diagram = ET.SubElement(mxfile, "diagram", id="caso-oti-uml", name="Diagrama de clases")
model = ET.SubElement(diagram, "mxGraphModel", dx="1600", dy="1000", grid="1", gridSize="10",
                      guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1",
                      pageScale="1", pageWidth="2800", pageHeight="1700", math="0", shadow="0",
                      background="#FFFFFF")
root = ET.SubElement(model, "root")
ET.SubElement(root, "mxCell", id="0")
ET.SubElement(root, "mxCell", id="1", parent="0")
_contador = [0]


def nuevo_id(prefijo):
    _contador[0] += 1
    return f"{prefijo}-{_contador[0]}"


def geom(cell, x, y, w, h):
    g = ET.SubElement(cell, "mxGeometry", x=str(int(x)), y=str(int(y)), width=str(int(w)),
                      height=str(int(h)))
    g.set("as", "geometry")


def celda(valor, estilo, x, y, w, h, padre="1", cid=None):
    c = ET.SubElement(root, "mxCell", id=cid or nuevo_id("c"), value=valor, style=estilo,
                      vertex="1", parent=padre)
    geom(c, x, y, w, h)
    return c


def estilo_fila(abstracto, fondo):
    base = ("text;strokeColor=none;align=left;verticalAlign=middle;spacingLeft=6;"
            "spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];"
            f"portConstraint=eastwest;whiteSpace=wrap;html=1;fontSize={FONT};")
    base += f"fillColor={fondo};" if fondo else "fillColor=none;"
    base += f"fontStyle=2;fontColor={ROJO};" if abstracto else "fontStyle=0;fontColor=#1A1A1A;"
    return base


def estilo_separador(borde):
    return ("line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;"
            "spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=right;points=[];"
            f"portConstraint=eastwest;strokeColor={borde};")


for nombre, c in CLASES.items():
    cabecera, borde, tenue = PALETA[c["grupo"]]
    est = c.get("estereotipo")
    cab = HEADER_H_STEREO if est else HEADER_H
    if est == "abstract":
        valor, fs = f"«abstract»<br><b><i>{nombre}</i></b>", 0
    elif est:
        valor, fs = f"«{est}»<br><b>{nombre}</b>", 0
    else:
        valor, fs = f"<b>{nombre}</b>", 0
    estilo = (f"swimlane;fontStyle={fs};align=center;verticalAlign=top;childLayout=stackLayout;"
              f"horizontal=1;startSize={cab};horizontalStack=0;resizeParent=1;resizeParentMax=0;"
              "resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fontSize=13;"
              f"fillColor={cabecera};strokeColor={borde};strokeWidth=1.5;swimlaneFillColor=#FFFFFF;"
              "rounded=1;arcSize=4;shadow=1;")
    celda(valor, estilo, *POS[nombre], W[nombre], H[nombre], cid=nombre)
    yy = cab
    comps = [("privados", c["privados"]), ("propiedades", c["propiedades"]),
             ("metodos", c["metodos"])]
    comps = [(k, v) for k, v in comps if v]
    for i, (tipo, filas) in enumerate(comps):
        if i > 0:
            celda("", estilo_separador(borde), 0, yy, W[nombre], SEP_H, padre=nombre)
            yy += SEP_H
        fondo = tenue if tipo == "propiedades" else None
        for texto, abstracto in filas:
            celda(texto, estilo_fila(abstracto, fondo), 0, yy, W[nombre], ROW_H, padre=nombre)
            yy += ROW_H


def arista(origen, destino, estilo, etiqueta=""):
    e = ET.SubElement(root, "mxCell", id=nuevo_id("rel"), value=etiqueta, style=estilo,
                      edge="1", parent="1", source=origen, target=destino)
    g = ET.SubElement(e, "mxGeometry", relative="1")
    g.set("as", "geometry")


def herencia(color):
    return ("endArrow=block;endSize=16;endFill=0;html=1;rounded=0;edgeStyle=orthogonalEdgeStyle;"
            f"strokeColor={color};strokeWidth=1.5;exitX=0.5;exitY=0;entryX=0.5;entryY=1;")


for hijo in FILA_REG:
    arista(hijo, "RegistroAcademico", herencia(PALETA["registro"][1]))
for hijo in ["Estudiante", "Docente"]:
    arista(hijo, "Persona", herencia(PALETA["persona"][1]))
arista("PeriodoAcademico", "EstadoPeriodo",
       "endArrow=open;endSize=12;html=1;rounded=0;edgeStyle=orthogonalEdgeStyle;fontSize=11;"
       f"strokeColor={PALETA['enumeracion'][1]};strokeWidth=1.5;fontColor={PALETA['enumeracion'][1]};"
       "labelBackgroundColor=#FFFFFF;exitX=0.3;exitY=1;entryX=0.5;entryY=0;", "- __estado&nbsp;&nbsp;1")

# ---- Título ------------------------------------------------------------------
ANCHO_TOTAL = POS["Docente"][0] + W["Docente"]
celda("<b>Caso OTI</b> · Diagrama de clases UML",
      "text;html=1;align=center;verticalAlign=middle;fontSize=20;fontColor=#1A1A1A;"
      "fillColor=#FFE6CC;strokeColor=#33CC33;strokeWidth=2;",
      ANCHO_TOTAL / 2 + 40, 20, 340, 40)  # posición que se le dio en draw.io

# ---- Leyenda -----------------------------------------------------------------
x_ley = POS["EstadoPeriodo"][0] + W["EstadoPeriodo"] + 460
y_ley = Y_BAJO
ANCHO_LEY = 260
filas_color = [
    ("abstracta", "Clase abstracta (no se instancia)"),
    ("registro", "Subclase de RegistroAcademico"),
    ("persona", "Subclase de Persona"),
    ("independiente", "Clase sin herencia"),
    ("enumeracion", "Enumeración"),
]
alto_ley = 34 + len(filas_color) * 24 + 26
celda("<b>Leyenda</b>", "rounded=1;arcSize=3;whiteSpace=wrap;html=1;align=left;verticalAlign=top;"
      "spacingLeft=10;spacingTop=4;fillColor=#FFFFFF;strokeColor=#999999;fontSize=12;",
      x_ley, y_ley, ANCHO_LEY, alto_ley)
yy = y_ley + 32
for grupo, texto in filas_color:
    cabecera, borde, _ = PALETA[grupo]
    celda("", f"rounded=1;arcSize=10;fillColor={cabecera};strokeColor={borde};strokeWidth=1.5;",
          x_ley + 12, yy + 3, 26, 16)
    celda(texto, "text;html=1;align=left;verticalAlign=middle;fontSize=11;",
          x_ley + 46, yy, ANCHO_LEY - 56, 22)
    yy += 24

ET.indent(mxfile, space="  ")
aqui = Path(__file__).parent
ET.ElementTree(mxfile).write(aqui / "diagrama_clases.drawio", encoding="utf-8",
                             xml_declaration=False)

# ---- Comprobación de solapamientos -------------------------------------------
cajas = {n: (POS[n][0], POS[n][1], W[n], H[n]) for n in CLASES}
cajas["leyenda"] = (x_ley, y_ley, ANCHO_LEY, alto_ley)
nombres = list(cajas)
for i, a in enumerate(nombres):
    for b in nombres[i + 1:]:
        ax, ay, aw, ah = cajas[a]
        bx, by, bw, bh = cajas[b]
        if ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah:
            print("SOLAPA:", a, b)

# ---- Versión Mermaid (la muestra GitHub) --------------------------------------
L = ["classDiagram", "    direction TB", ""]
for nombre, c in CLASES.items():
    L.append(f"    class {nombre} {{")
    if c.get("estereotipo"):
        L.append(f"        <<{c['estereotipo']}>>")
    for comp in (c["privados"], c["propiedades"] or []):
        for t, abstracto in comp:
            t = t.replace("- ", "-", 1).replace("+ ", "+", 1)
            t = t.replace("__", "#95;#95;")
            t = t.replace("{", "[").replace("}", "]").replace(": ", " : ", 1)
            L.append(f"        {t}")
    for t, abstracto in (c["metodos"] or []):
        t = t.replace("+ ", "+", 1).replace(" {abstract}", "").replace("__str__", "#95;#95;str#95;#95;")
        cuerpo, tipo = t.rsplit("): ", 1)
        L.append(f"        {cuerpo})" + ("*" if abstracto else "") + f" {tipo}")
    L += ["    }", ""]
for h in FILA_REG:
    L.append(f"    RegistroAcademico <|-- {h}")
L += ["    Persona <|-- Estudiante", "    Persona <|-- Docente",
      "    PeriodoAcademico --> \"1\" EstadoPeriodo : -#95;#95;estado", ""]
for nombre, c in CLASES.items():
    cabecera, borde, _ = PALETA[c["grupo"]]
    L.append(f"    style {nombre} fill:{cabecera},stroke:{borde},stroke-width:2px")
(aqui / "diagrama_clases.mmd").write_text("\n".join(L) + "\n")
print("ok")
