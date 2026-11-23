# -*- coding: utf-8 -*-
"""
España Matemáticas 3.º de Primaria: Rectas y ángulos (Sentido espacial)
Recta, semirrecta y segmento; rectas paralelas, secantes y perpendiculares; ángulo recto, agudo, obtuso y llano; giros.
Ángulos: reutiliza los generadores de 4.º (mismo ciclo), sin el transportador.
Errores: llamar perpendiculares a todas las secantes, pensar que dos rectas que no se cortan en el dibujo son paralelas.
"""
import math
import random
from es_common import mcq, fig
from es_low import unit, src

R = random.Random(33016)
SEED = 33916
BLUE, RED = "#1565c0", "#c62828"


def arrow(x, y, ang, col):
    a1, a2 = ang + 2.7, ang - 2.7
    return "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (x, y, x + 16 * math.cos(a1), y + 16 * math.sin(a1), x + 16 * math.cos(a2), y + 16 * math.sin(a2), col)


def linea(kind, ang, label):
    """recta (dos flechas), semirrecta (punto y flecha), segmento (dos puntos)"""
    cx, cy, L = 150, 60, 110
    dx, dy = L * math.cos(ang), L * math.sin(ang)
    x1, y1, x2, y2 = cx - dx, cy - dy, cx + dx, cy + dy
    s = "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (x1, y1, x2, y2, BLUE)
    if kind == "recta":
        s += arrow(x1, y1, ang + math.pi, BLUE) + arrow(x2, y2, ang, BLUE)
    elif kind == "semirrecta":
        s += "<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (x1, y1, BLUE) + arrow(x2, y2, ang, BLUE)
    else:
        s += "<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/><circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (x1, y1, BLUE, x2, y2, BLUE)
    return fig("<svg viewBox='0 0 300 120' width='300' height='120' role='img' aria-label='%s'>%s</svg>" % (label, s))


def dos_rectas(kind, ang):
    s = ""
    cx, cy, L = 150, 80, 120
    if kind == "paralelas":
        off = R.choice([30, 40, 50])
        nx, ny = -math.sin(ang), math.cos(ang)
        segs = [(cx + nx * off / 2, cy + ny * off / 2, ang, BLUE), (cx - nx * off / 2, cy - ny * off / 2, ang, RED)]
    else:
        b = ang + (math.pi / 2 if kind == "perpendiculares" else R.choice([0.5, 0.7, 2.3, 2.6]))
        segs = [(cx, cy, ang, BLUE), (cx + R.randint(-30, 30), cy, b, RED) if kind == "secantes" else (cx, cy, b, RED)]
    for x, y, a, col in segs:
        dx, dy = L * math.cos(a), L * math.sin(a)
        if abs(dy) > 70:
            k = 70 / abs(dy)
            dx, dy = dx * k, dy * k
        s += "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (x - dx, y - dy, x + dx, y + dy, col)
    if kind == "perpendiculares":
        a = ang
        p = [(cx + 12 * math.cos(a), cy + 12 * math.sin(a)), (cx + 12 * math.cos(a) + 12 * math.cos(a + math.pi / 2), cy + 12 * math.sin(a) + 12 * math.sin(a + math.pi / 2)),
             (cx + 12 * math.cos(a + math.pi / 2), cy + 12 * math.sin(a + math.pi / 2))]
        s += "<polyline points='%s' fill='none' stroke='#333' stroke-width='1.5'/>" % " ".join("%.1f,%.1f" % q for q in p)
    return fig("<svg viewBox='0 0 300 160' width='300' height='160' role='img' aria-label='dos rectas'>%s</svg>" % s)


def s_lineas():
    k = R.choice(["recta", "semirrecta", "segmento"])
    ang = math.radians(R.choice([0, 10, -15, 25, -30, 160, 200, 35]))
    if R.random() < 0.7:
        return mcq(linea(k, ang, "una línea") + "¿Qué es esta línea?", "una %s" % k if k != "segmento" else "un segmento", [x for x in ("una recta", "una semirrecta", "un segmento", "una curva") if x != ("una %s" % k if k != "segmento" else "un segmento")],
                   "Recta: no tiene principio ni fin. Semirrecta: tiene principio pero no fin. Segmento: tiene principio y fin. Es <b>%s</b>." % ("una %s" % k if k != "segmento" else "un segmento"))
    q, a, w = R.choice([("¿Qué línea tiene principio y fin y se puede medir?", "el segmento", ["la recta", "la semirrecta", "ninguna"]),
                        ("¿Qué línea tiene principio pero no tiene fin?", "la semirrecta", ["la recta", "el segmento", "la curva"]),
                        ("¿Qué línea no tiene ni principio ni fin?", "la recta", ["la semirrecta", "el segmento", "el punto"]),
                        ("Un punto divide una recta en…", "dos semirrectas", ["dos segmentos", "dos rectas", "tres semirrectas"]),
                        ("¿Cuántas rectas pasan por dos puntos?", "una", ["dos", "ninguna", "muchas"]),
                        ("¿Cuántas rectas pasan por un punto?", "muchas", ["una", "dos", "ninguna"])])
    return mcq(q, a, w, "Respuesta: <b>%s</b>." % a)


def s_posicion():
    k = R.choice(["paralelas", "perpendiculares", "secantes"])
    ang = math.radians(R.choice([0, 15, -20, 30, 45, -40, 60]))
    ok = {"paralelas": "paralelas", "perpendiculares": "perpendiculares", "secantes": "secantes, no perpendiculares"}[k]
    return mcq(dos_rectas(k, ang) + "¿Cómo son estas dos rectas?", ok, [x for x in ("paralelas", "perpendiculares", "secantes, no perpendiculares", "iguales") if x != ok],
               "Paralelas: nunca se cortan. Secantes: se cortan. Perpendiculares: se cortan formando cuatro ángulos rectos. Son <b>%s</b>." % ok)


def s_mundo():
    q, a, w = R.choice([("Los raíles de una vía de tren son…", "paralelos", ["perpendiculares", "secantes", "curvos"]),
                        ("Los dos bordes de una hoja que forman una esquina son…", "perpendiculares", ["paralelos", "iguales", "curvos"]),
                        ("Las líneas de los cuadernos de rayas son…", "paralelas", ["perpendiculares", "secantes", "semirrectas"]),
                        ("Las calles que se cruzan formando una cruz son…", "perpendiculares", ["paralelas", "iguales", "curvas"]),
                        ("Los lados opuestos de una puerta son…", "paralelos", ["perpendiculares", "secantes", "curvos"]),
                        ("Las dos agujas del reloj a las 9:00 son…", "perpendiculares", ["paralelas", "una recta", "iguales"]),
                        ("Dos rectas que se cortan se llaman…", "secantes", ["paralelas", "segmentos", "semirrectas"]),
                        ("Dos rectas paralelas, ¿se cortan alguna vez?", "no, nunca", ["sí, en un punto", "sí, en dos puntos", "solo si son largas"]),
                        ("¿Cuántos ángulos rectos forman dos rectas perpendiculares?", "4", ["1", "2", "0"]),
                        ("¿Qué tipo de ángulo tiene la esquina de un libro?", "recto", ["agudo", "obtuso", "llano"])])
    return mcq(q, a, w, "Respuesta: <b>%s</b>." % a)


tipo, conc, est, giros = src("angulos", SEED, "s1_tipo", "s1_conceptos", "s2_estimar", "s4_giros", sin=("transportador", "complementario", "suplementario"))

unit(3, "rectas-y-angulos", 16, "E", "Rectas, semirrectas y segmentos; posiciones relativas de rectas (paralelas, secantes y perpendiculares); ángulos recto, agudo y obtuso; giros",
     "Rectas y ángulos", "Rectas y ángulos",
     "Fichas de matemáticas de 3.º de Primaria: recta, semirrecta y segmento, rectas paralelas, secantes y perpendiculares, tipos de ángulos y giros. 100 ejercicios con soluciones.",
     "Perpendiculares: 4 ángulos rectos", "Paralelas: nunca se cortan.",
     ["Una <b>recta</b> no tiene principio ni fin; una <b>semirrecta</b> tiene principio; un <b>segmento</b> tiene principio y fin.",
      "Dos rectas <b>paralelas</b> nunca se cortan. Las <b>secantes</b> se cortan. Si al cortarse forman ángulos rectos, son <b>perpendiculares</b>.",
      "Un ángulo <b>recto</b> mide 90° (como la esquina de un folio). <b>Agudo</b>: menos. <b>Obtuso</b>: más."],
     [("La esquina de una mesa", ["Es como la esquina de un folio"], "ángulo recto"), ("Una aguja del reloj da media vuelta", ["Media vuelta = 2 ángulos rectos"], "180°")],
     [["Llamar perpendiculares a todas las secantes", "Solo si forman ángulos rectos."], ["Pensar que el ángulo depende de lo largos que son los lados", "Mide la abertura, no los lados."], ["Confundir semirrecta y segmento", "El segmento tiene dos extremos."]],
     [("¿Qué diferencia hay entre recta y segmento?", "La recta no tiene principio ni fin; el segmento tiene principio y fin, y por eso se puede medir."),
      ("¿Qué son rectas perpendiculares?", "Son dos rectas que se cortan formando cuatro ángulos rectos.")],
     [("Recta, semirrecta y segmento", [(s_lineas, 20)]), ("Paralelas, secantes y perpendiculares", [(s_posicion, 14), (s_mundo, 6)]), ("Tipos de ángulos", [(tipo, 14), (conc, 6)]),
      ("Estimar ángulos", [(est, 14), (tipo, 6)]), ("Giros", [(giros, 14), (s_mundo, 4), (conc, 2)])], 33016, dos_rectas("perpendiculares", 0.3))
