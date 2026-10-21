"""Genera docs/uml/diagrama_clases.drawio con notación UML editable en draw.io."""
import json
import xml.etree.ElementTree as ET

ROW_H = 20
HEADER_H = 26
HEADER_H_STEREO = 40
SEP_H = 8
CHAR_W = 6.6
FONT = 11

# Cada miembro: (texto, estilo) con estilo: "" normal, "a" abstracto (cursiva), "s" estático (subrayado)
CLASES = {
    "RegistroAcademico": dict(stereo="abstract", attrs=[
        ("- _nombre: str", ""),
        ("+ nombre: str «get/set»", ""),
    ], methods=[
        ("+ longitud_maxima_nombre(): int «get»", "a"),
        ("+ resumen(): str", "a"),
        ("+ __str__(): str", ""),
    ]),
    "Curso": dict(attrs=[
        ("+ LONGITUD_MAXIMA_NOMBRE: int = 200", "s"),
        ("+ HORAS_MAXIMAS: int = 255", "s"),
        ("- _ultimo_id: int", "s"),
        ("- _id: int", ""),
        ("- _codigo: str", ""),
        ("- _creditos: Decimal", ""),
        ("- _horas_teoricas: int", ""),
        ("- _horas_practicas: int", ""),
        ("- _horas_seminario: int", ""),
        ("- _horas_virtuales: int", ""),
        ("+ id: int «get»", ""),
        ("+ codigo: str «get/set»", ""),
        ("+ creditos: Decimal «get/set»", ""),
        ("+ horas_teoricas: int «get/set»", ""),
        ("+ horas_practicas: int «get/set»", ""),
        ("+ horas_seminario: int «get/set»", ""),
        ("+ horas_virtuales: int «get/set»", ""),
        ("+ horas_totales: int «get, calculado»", ""),
    ], methods=[
        ("+ longitud_maxima_nombre(): int «get»", ""),
        ("+ resumen(): str", ""),
        ("- _generar_id(): int", "s"),
    ]),
    "PeriodoAcademico": dict(attrs=[
        ("+ LONGITUD_MAXIMA_NOMBRE: int = 45", "s"),
        ("- _numero: int", ""),
        ("- _anio: int", ""),
        ("- _fecha_inicio: date", ""),
        ("- _fecha_fin: date", ""),
        ("- _fecha_inicio_matricula: date", ""),
        ("- _fecha_fin_matricula: date", ""),
        ("- _es_verano: int (0 o 1)", ""),
        ("- _nota_minima_aprobatoria: Decimal", ""),
        ("- _estado: EstadoPeriodo", ""),
        ("+ numero: int «get/set»", ""),
        ("+ anio: int «get/set»", ""),
        ("+ codigo: str «get, calculado»", ""),
        ("+ fecha_inicio: date «get»", ""),
        ("+ fecha_fin: date «get»", ""),
        ("+ fecha_inicio_matricula: date «get»", ""),
        ("+ fecha_fin_matricula: date «get»", ""),
        ("+ es_verano: bool «get/set»", ""),
        ("+ nota_minima_aprobatoria: Decimal «get/set»", ""),
        ("+ estado: EstadoPeriodo «get/set»", ""),
    ], methods=[
        ("+ cambiar_fechas(inicio: date, fin: date): None", ""),
        ("+ cambiar_fechas_matricula(inicio: date, fin: date): None", ""),
        ("+ longitud_maxima_nombre(): int «get»", ""),
        ("+ resumen(): str", ""),
    ]),
    "PlanEstudios": dict(attrs=[
        ("+ LONGITUD_MAXIMA_NOMBRE: int = 36", "s"),
        ("- _anio_aprobacion: int", ""),
        ("- _codigo_escuela: str", ""),
        ("- _creditos_obligatorios: Decimal", ""),
        ("- _creditos_electivos: Decimal", ""),
        ("- _creditos_extracurriculares: Decimal", ""),
        ("- _vigente: int (0 o 1)", ""),
        ("- _es_nuevo: int (0 o 1)", ""),
        ("+ anio_aprobacion: int «get/set»", ""),
        ("+ codigo_escuela: str «get/set»", ""),
        ("+ creditos_obligatorios: Decimal «get/set»", ""),
        ("+ creditos_electivos: Decimal «get/set»", ""),
        ("+ creditos_extracurriculares: Decimal «get/set»", ""),
        ("+ creditos_totales: Decimal «get, calculado»", ""),
        ("+ vigente: bool «get/set»", ""),
        ("+ es_nuevo: bool «get/set»", ""),
    ], methods=[
        ("+ longitud_maxima_nombre(): int «get»", ""),
        ("+ resumen(): str", ""),
    ]),
    "EscuelaProfesional": dict(attrs=[
        ("+ LONGITUD_MAXIMA_NOMBRE: int = 100", "s"),
        ("- _codigo: str", ""),
        ("- _informacion_general: str", ""),
        ("- _perfil_egresado: str", ""),
        ("- _codigo_director: str", ""),
        ("- _codigo_secretario_academico: str", ""),
        ("+ codigo: str «get/set»", ""),
        ("+ informacion_general: str «get/set»", ""),
        ("+ perfil_egresado: str «get/set»", ""),
        ("+ codigo_director: str «get/set»", ""),
        ("+ codigo_secretario_academico: str «get/set»", ""),
    ], methods=[
        ("+ longitud_maxima_nombre(): int «get»", ""),
        ("+ resumen(): str", ""),
    ]),
    "Persona": dict(stereo="abstract", attrs=[
        ("- _dni: str", ""),
        ("- _nombres: str", ""),
        ("- _apellidos: str", ""),
        ("+ dni: str «get/set»", ""),
        ("+ nombres: str «get/set»", ""),
        ("+ apellidos: str «get/set»", ""),
        ("+ nombre_completo: str «get, calculado»", ""),
    ], methods=[
        ("+ rol(): str «get»", "a"),
        ("+ __str__(): str", ""),
    ]),
    "Estudiante": dict(attrs=[
        ("- _codigo_estudiante: str", ""),
        ("- _codigo_escuela: str", ""),
        ("+ codigo_estudiante: str «get/set»", ""),
        ("+ codigo_escuela: str «get/set»", ""),
    ], methods=[
        ("+ rol(): str «get»", ""),
        ("+ __str__(): str", ""),
    ]),
    "Docente": dict(attrs=[
        ("- _codigo_docente: str", ""),
        ("+ codigo_docente: str «get/set»", ""),
    ], methods=[
        ("+ rol(): str «get»", ""),
        ("+ __str__(): str", ""),
    ]),
    "Seccion": dict(attrs=[
        ("- _codigo: str", ""),
        ("- _codigo_curso: str", ""),
        ("- _codigo_periodo: str", ""),
        ("- _vacantes: int", ""),
        ("- _matriculados: int", ""),
        ("+ codigo: str «get/set»", ""),
        ("+ codigo_curso: str «get/set»", ""),
        ("+ codigo_periodo: str «get/set»", ""),
        ("+ vacantes: int «get/set»", ""),
        ("+ matriculados: int «get»", ""),
        ("+ vacantes_disponibles: int «get, calculado»", ""),
        ("+ esta_llena: bool «get, calculado»", ""),
    ], methods=[
        ("+ matricular(): None", ""),
        ("+ retirar(): None", ""),
        ("+ __str__(): str", ""),
    ]),
    "EstadoPeriodo": dict(stereo="enumeration", attrs=[
        ("PLANIFICADO = 1", ""),
        ("EN_CURSO = 2", ""),
        ("MATRICULA_CERRADA = 3", ""),
        ("FINALIZADO = 4", ""),
    ], methods=[
        ("+ descripcion: str «get»", ""),
        ("+ desde_numero(numero: int): EstadoPeriodo", "s"),
    ]),
}

COLORES = {  # relleno de cabecera por grupo
    "abstract": ("#dae8fc", "#6c8ebf"),
    "registro": ("#d5e8d4", "#82b366"),
    "persona": ("#fff2cc", "#d6b656"),
    "otro": ("#f5f5f5", "#666666"),
    "enum": ("#e1d5e7", "#9673a6"),
}
GRUPO = {
    "RegistroAcademico": "abstract", "Persona": "abstract",
    "Curso": "registro", "PlanEstudios": "registro",
    "EscuelaProfesional": "registro", "PeriodoAcademico": "registro",
    "Estudiante": "persona", "Docente": "persona",
    "Seccion": "otro", "EstadoPeriodo": "enum",
}


def ancho(nombre):
    c = CLASES[nombre]
    textos = [t for t, _ in c["attrs"] + c["methods"]] + [nombre]
    return int(max(len(t) for t in textos) * CHAR_W + 24)


def alto(nombre):
    c = CLASES[nombre]
    cab = HEADER_H_STEREO if c.get("stereo") else HEADER_H
    return cab + ROW_H * (len(c["attrs"]) + len(c["methods"])) + SEP_H + 6


W = {n: ancho(n) for n in CLASES}
H = {n: alto(n) for n in CLASES}

# ---- Disposición -----------------------------------------------------------
GAP = 40
Y_TOP = 80
Y_MID = Y_TOP + max(H["RegistroAcademico"], H["Persona"]) + 90
fila = ["Curso", "PeriodoAcademico", "PlanEstudios", "EscuelaProfesional", "Estudiante", "Docente"]
POS = {}
x = 40
for n in fila:
    POS[n] = (x, Y_MID)
    x += W[n] + GAP
# Padres centrados sobre sus hijos
reg_hijos = ["Curso", "PeriodoAcademico", "PlanEstudios", "EscuelaProfesional"]
izq = POS["Curso"][0]
der = POS["EscuelaProfesional"][0] + W["EscuelaProfesional"]
POS["RegistroAcademico"] = ((izq + der) / 2 - W["RegistroAcademico"] / 2, Y_TOP)
izq = POS["Estudiante"][0]
der = POS["Docente"][0] + W["Docente"]
POS["Persona"] = ((izq + der) / 2 - W["Persona"] / 2, Y_TOP)
# Fila inferior
y_bajo_curso = Y_MID + H["Curso"] + 90
POS["Seccion"] = (POS["Curso"][0], y_bajo_curso)
POS["EstadoPeriodo"] = (POS["PeriodoAcademico"][0] + 140, Y_MID + H["PeriodoAcademico"] + 90)

# ---- XML ---------------------------------------------------------------------
mxfile = ET.Element("mxfile", host="app.diagrams.net", type="device")
diagram = ET.SubElement(mxfile, "diagram", id="caso-oti-uml", name="Diagrama de clases")
model = ET.SubElement(diagram, "mxGraphModel", dx="1600", dy="1000", grid="1", gridSize="10",
                      guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1",
                      pageScale="1", pageWidth="2400", pageHeight="1800", math="0", shadow="0")
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
    return g


ESTILO_FILA = ("text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;"
               "spacingLeft=6;spacingRight=4;overflow=hidden;rotatable=0;"
               "points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;"
               f"fontSize={FONT};fontFamily=Helvetica;")
ESTILO_SEP = ("line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;"
              "spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=right;points=[];"
              "portConstraint=eastwest;strokeColor=inherit;")
FONT_STYLE = {"": 0, "a": 2, "s": 4}

IDS = {}
for nombre, c in CLASES.items():
    x, y = POS[nombre]
    stereo = c.get("stereo")
    cab = HEADER_H_STEREO if stereo else HEADER_H
    relleno, borde = COLORES[GRUPO[nombre]]
    if stereo:
        nombre_html = f"<i>{nombre}</i>" if stereo == "abstract" else nombre
        valor = f"«{stereo}»<br><b>{nombre_html}</b>"
        font_style = 0
    else:
        valor = nombre
        font_style = 1
    cid = nombre
    IDS[nombre] = cid
    estilo = (f"swimlane;fontStyle={font_style};align=center;verticalAlign=top;childLayout=stackLayout;"
              f"horizontal=1;startSize={cab};horizontalStack=0;resizeParent=1;resizeParentMax=0;"
              f"resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;"
              f"fillColor={relleno};strokeColor={borde};swimlaneFillColor=#ffffff;fontSize=12;")
    cell = ET.SubElement(root, "mxCell", id=cid, value=valor, style=estilo, vertex="1", parent="1")
    geom(cell, x, y, W[nombre], H[nombre])
    yy = cab
    for texto, tipo in c["attrs"]:
        fila_cell = ET.SubElement(root, "mxCell", id=nuevo_id(cid), value=texto,
                                  style=ESTILO_FILA + f"fontStyle={FONT_STYLE[tipo]};",
                                  vertex="1", parent=cid)
        geom(fila_cell, 0, yy, W[nombre], ROW_H)
        yy += ROW_H
    sep = ET.SubElement(root, "mxCell", id=nuevo_id(cid), value="", style=ESTILO_SEP,
                        vertex="1", parent=cid)
    geom(sep, 0, yy, W[nombre], SEP_H)
    yy += SEP_H
    for texto, tipo in c["methods"]:
        fila_cell = ET.SubElement(root, "mxCell", id=nuevo_id(cid), value=texto,
                                  style=ESTILO_FILA + f"fontStyle={FONT_STYLE[tipo]};",
                                  vertex="1", parent=cid)
        geom(fila_cell, 0, yy, W[nombre], ROW_H)
        yy += ROW_H


def arista(origen, destino, estilo, etiqueta=""):
    e = ET.SubElement(root, "mxCell", id=nuevo_id("rel"), value=etiqueta, style=estilo,
                      edge="1", parent="1", source=IDS[origen], target=IDS[destino])
    g = ET.SubElement(e, "mxGeometry", relative="1")
    g.set("as", "geometry")


HERENCIA = ("endArrow=block;endSize=16;endFill=0;html=1;rounded=0;edgeStyle=orthogonalEdgeStyle;"
            "exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;")
for hijo in reg_hijos:
    arista(hijo, "RegistroAcademico", HERENCIA)
for hijo in ["Estudiante", "Docente"]:
    arista(hijo, "Persona", HERENCIA)

DEP = ("endArrow=open;endSize=12;dashed=1;html=1;rounded=0;edgeStyle=orthogonalEdgeStyle;"
       "fontSize=10;labelBackgroundColor=#ffffff;")
arista("Seccion", "Curso", DEP + "exitX=0.5;exitY=0;entryX=0.5;entryY=1;", "codigo_curso")
arista("Seccion", "PeriodoAcademico", DEP + "exitX=1;exitY=0.1;entryX=0.15;entryY=1;",
       "codigo_periodo")
arista("PlanEstudios", "EscuelaProfesional", DEP + "exitX=1;exitY=0.3;entryX=0;entryY=0.3;",
       "codigo_escuela")
arista("Estudiante", "EscuelaProfesional", DEP + "exitX=0;exitY=0.6;entryX=1;entryY=0.6;",
       "codigo_escuela")
arista("EscuelaProfesional", "Docente", DEP + "exitX=0.5;exitY=1;entryX=0.5;entryY=1;",
       "codigo_director /<br>codigo_secretario_academico")
arista("PeriodoAcademico", "EstadoPeriodo",
       "endArrow=open;endSize=12;html=1;rounded=0;fontSize=10;labelBackgroundColor=#ffffff;"
       "exitX=0.6;exitY=1;entryX=0.5;entryY=0;edgeStyle=orthogonalEdgeStyle;",
       "estado")

# Título y leyenda
titulo = ET.SubElement(root, "mxCell", id="titulo",
                       value="<b>Caso OTI - Diagrama de clases UML</b>",
                       style="text;html=1;align=left;verticalAlign=middle;fontSize=18;",
                       vertex="1", parent="1")
geom(titulo, 40, 20, 500, 34)

leyenda_txt = (
    "<b>Leyenda</b><br>"
    "<b>-</b> atributo privado (prefijo _ en Python)<br>"
    "<b>+</b> miembro público<br>"
    "«get» propiedad de solo lectura<br>"
    "«get/set» propiedad con setter que valida<br>"
    "«get, calculado» propiedad calculada (no se guarda)<br>"
    "<i>cursiva</i> método o propiedad abstracta<br>"
    "<u>subrayado</u> miembro de clase (estático)<br>"
    "Flecha con triángulo hueco: herencia («es un»)<br>"
    "Flecha punteada: referencia solo por código (texto)"
)
x_ley = POS["EstadoPeriodo"][0] + W["EstadoPeriodo"] + 80
y_ley = POS["EstadoPeriodo"][1]
leyenda = ET.SubElement(root, "mxCell", id="leyenda", value=leyenda_txt,
                        style="rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;"
                              "spacing=10;fillColor=#ffffff;strokeColor=#999999;fontSize=11;",
                        vertex="1", parent="1")
geom(leyenda, x_ley, y_ley, 320, 190)

ET.indent(mxfile, space="  ")
salida = __import__("pathlib").Path(__file__).with_name("diagrama_clases.drawio")
ET.ElementTree(mxfile).write(salida, encoding="utf-8", xml_declaration=False)

# Datos para la vista previa
cajas = {n: (POS[n][0], POS[n][1], W[n], H[n]) for n in CLASES}
cajas["Leyenda"] = (x_ley, y_ley, 320, 190)
pass
print("ok", salida)
