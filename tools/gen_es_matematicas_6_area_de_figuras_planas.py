# -*- coding: utf-8 -*-
"""
España Matemáticas 6.º (y 5.º) de Primaria: Área de figuras planas (Sentido de la medida)
Área del cuadrado, rectángulo, romboide (base × altura), triángulo (base × altura : 2); 6.º: rombo (D × d : 2), trapecio,
polígono regular (perímetro × apotema : 2) y figuras compuestas. Perímetro y área.
Errores: olvidar dividir entre 2 en el triángulo, usar el lado inclinado como altura, confundir perímetro y área.
"""
import random
from es_c3 import M, mix, lesson, make_unit, num, d
from fractions import Fraction as F

R = None
LV = 6
INK, FILLC, RED = "#333", "#d6e2f6", "#c0392b"


def svg(w, h, body, label):
    return "<div class='fig'><svg viewBox='0 0 %d %d' width='%d' role='img' aria-label='%s'>%s</svg></div>" % (w, h, w, label, body)


def t(x, y, s, anchor="middle"):
    return "<text x='%d' y='%d' font-size='14' font-weight='700' fill='%s' text-anchor='%s'>%s</text>" % (x, y, RED, anchor, s)


def figura(kind, a, b, c=None):
    """dibujo con medidas: rect (a × b), tri (base a, altura b), para (base a, altura b), trap (B a, b, h c), rombo (D a, d b)"""
    if kind == "rect":
        return svg(300, 150, "<rect x='40' y='20' width='180' height='100' fill='%s' stroke='%s' stroke-width='2'/>" % (FILLC, INK) + t(130, 142, "%s cm" % a) + t(232, 75, "%s cm" % b, "start"), "rectángulo")
    if kind == "tri":
        return svg(260, 160, "<polygon points='30,120 230,120 90,20' fill='%s' stroke='%s' stroke-width='2'/>" % (FILLC, INK) +
                   "<line x1='90' y1='20' x2='90' y2='120' stroke='%s' stroke-dasharray='5 4'/><rect x='90' y='110' width='10' height='10' fill='none' stroke='%s'/>" % (INK, INK) + t(130, 144, "%s cm" % a) + t(96, 80, "%s cm" % b, "start"), "triángulo con base y altura")
    if kind == "para":
        return svg(280, 150, "<polygon points='30,120 210,120 250,20 70,20' fill='%s' stroke='%s' stroke-width='2'/>" % (FILLC, INK) +
                   "<line x1='70' y1='20' x2='70' y2='120' stroke='%s' stroke-dasharray='5 4'/>" % INK + t(120, 142, "%s cm" % a) + t(76, 80, "%s cm" % b, "start"), "romboide con base y altura")
    if kind == "trap":
        return svg(280, 160, "<polygon points='20,120 260,120 200,30 80,30' fill='%s' stroke='%s' stroke-width='2'/>" % (FILLC, INK) +
                   "<line x1='80' y1='30' x2='80' y2='120' stroke='%s' stroke-dasharray='5 4'/>" % INK + t(140, 144, "%s cm" % a) + t(140, 22, "%s cm" % b) + t(86, 85, "%s cm" % c, "start"), "trapecio con bases y altura")
    return svg(260, 190, "<polygon points='130,10 230,90 130,170 30,90' fill='%s' stroke='%s' stroke-width='2'/>" % (FILLC, INK) +
               "<line x1='130' y1='10' x2='130' y2='170' stroke='%s' stroke-dasharray='5 4'/><line x1='30' y1='90' x2='230' y2='90' stroke='%s' stroke-dasharray='5 4'/>" % (INK, INK) +
               t(136, 60, "%s cm" % a, "start") + t(190, 84, "%s cm" % b), "rombo con sus diagonales")


def s1_rect():
    k = R.choice(["rect", "cuad", "rect_fig"])
    a, b = R.randint(3, 25), R.randint(2, 15)
    if k == "cuad":
        return M("¿Cuál es el área de un cuadrado de %d cm de lado?" % a, "%s cm²" % num(a * a), ["%d cm²" % (4 * a) if 4 * a != a * a else "%d cm²" % (a * a + 1), "%d cm²" % (2 * a), "%s cm" % num(a * a)], "lado × lado = %d × %d = <b>%s cm²</b>." % (a, a, num(a * a)))
    if a == b:
        return None
    pic = figura("rect", a, b) if k == "rect_fig" else ""
    return M(pic + ("¿Cuál es el área del rectángulo?" if pic else "¿Cuál es el área de un rectángulo de %d cm por %d cm?" % (a, b)), "%s cm²" % num(a * b), ["%d cm²" % (2 * (a + b)), "%d cm²" % (a + b), "%s cm²" % num(a * b // 2) if a * b % 2 == 0 else "%s cm²" % num(a * b + 1), "%s cm" % num(a * b)],
             "base × altura = %d × %d = <b>%s cm²</b>." % (a, b, num(a * b)))


def s2_tri_para():
    k = R.choice(["tri", "tri", "para"])
    a, b = R.randint(3, 24), R.randint(2, 16)
    if k == "tri":
        A = F(a * b, 2)
        return M(figura("tri", a, b) + "¿Cuál es el área del triángulo?", "%s cm²" % d(A), ["%s cm²" % num(a * b), "%s cm²" % d(A / 2), "%s cm²" % num(a + b), "%s cm²" % d(A + 1)], "base × altura : 2 = %d × %d : 2 = <b>%s cm²</b>." % (a, b, d(A)))
    return M(figura("para", a, b) + "¿Cuál es el área del romboide?", "%s cm²" % num(a * b), ["%s cm²" % d(F(a * b, 2)), "%d cm²" % (2 * (a + b)), "%s cm²" % num(a * b + a), "%s cm²" % num(a + b)], "base × altura = %d × %d = <b>%s cm²</b>." % (a, b, num(a * b)))


def s3_otros():
    k = R.choice(["rombo", "trap", "reg", "trap"])
    if k == "rombo":
        D, dd = R.randint(4, 20), R.randint(2, 14)
        if D == dd:
            return None
        A = F(D * dd, 2)
        return M(figura("rombo", D, dd) + "¿Cuál es el área del rombo?", "%s cm²" % d(A), ["%s cm²" % num(D * dd), "%s cm²" % num(D + dd), "%s cm²" % d(A / 2)], "D × d : 2 = %d × %d : 2 = <b>%s cm²</b>." % (D, dd, d(A)))
    if k == "trap":
        B, b, h = R.randint(8, 20), R.randint(3, 7), R.randint(2, 12)
        A = F((B + b) * h, 2)
        return M(figura("trap", B, b, h) + "¿Cuál es el área del trapecio?", "%s cm²" % d(A), ["%s cm²" % num((B + b) * h), "%s cm²" % num(B * b * h), "%s cm²" % d(F(B * h, 2) + b), "%s cm²" % num(B * h)],
                 "(B + b) × h : 2 = (%d + %d) × %d : 2 = <b>%s cm²</b>." % (B, b, h, d(A)))
    n = R.choice([5, 6, 8])
    l = R.randint(4, 12)
    ap = R.randint(3, 10)
    A = F(n * l * ap, 2)
    nm = {5: "pentágono", 6: "hexágono", 8: "octógono"}[n]
    return M("Un %s regular tiene %d cm de lado y %d cm de apotema. ¿Cuál es su área?" % (nm, l, ap), "%s cm²" % d(A), ["%s cm²" % num(n * l * ap), "%s cm²" % num(n * l), "%s cm²" % d(F(l * ap, 2))],
             "perímetro × apotema : 2 = %d × %d : 2 = <b>%s cm²</b>." % (n * l, ap, d(A)))


def s4_compuesta():
    k = R.choice(["L", "casa", "marco"])
    if k == "L":
        a, b, c, e = R.randint(6, 12), R.randint(6, 12), R.randint(2, 4), R.randint(2, 4)
        A = a * c + (b - c) * e
        return M("Una figura en forma de L está formada por un rectángulo de %d cm × %d cm y otro de %d cm × %d cm (sin solaparse). ¿Cuál es su área?" % (a, c, b - c, e), "%d cm²" % A, ["%d cm²" % (a * b), "%d cm²" % (a * c), "%d cm²" % (A + c * e), "%d cm²" % (2 * (a + b))],
                 "%d × %d + %d × %d = <b>%d cm²</b>." % (a, c, b - c, e, A))
    if k == "casa":
        a, h1, h2 = R.choice([4, 6, 8, 10]), R.randint(3, 8), R.randint(2, 6)
        A = a * h1 + a * h2 // 2
        return M("El dibujo de una casa es un rectángulo de %d cm de base y %d cm de alto, con un tejado triangular de la misma base y %d cm de altura. ¿Cuál es el área total?" % (a, h1, h2), "%d cm²" % A,
                 ["%d cm²" % (a * h1 + a * h2), "%d cm²" % (a * (h1 + h2) // 2), "%d cm²" % (a * h1), "%d cm²" % (A + a)], "%d × %d + %d × %d : 2 = %d + %d = <b>%d cm²</b>." % (a, h1, a, h2, a * h1, a * h2 // 2, A))
    a, b, m = R.randint(8, 16), R.randint(6, 12), R.randint(1, 2)
    A = a * b - (a - 2 * m) * (b - 2 * m)
    return M("Un marco rectangular mide %d cm × %d cm por fuera y deja un hueco de %d cm × %d cm. ¿Cuál es el área del marco?" % (a, b, a - 2 * m, b - 2 * m), "%d cm²" % A, ["%d cm²" % (a * b), "%d cm²" % ((a - 2 * m) * (b - 2 * m)), "%d cm²" % (A + 4), "%d cm²" % (2 * (a + b))],
             "%d × %d − %d × %d = <b>%d cm²</b>." % (a, b, a - 2 * m, b - 2 * m, A))


def s5_problema():
    k = R.choice(["cesped", "baldosas", "vela", "pintar", "falta"])
    if k == "cesped":
        a, b, p = R.randint(5, 20), R.randint(4, 15), R.choice([3, 4, 5, 6])
        return M("Un jardín rectangular mide %d m por %d m. El césped cuesta %d € el m². ¿Cuánto cuesta cubrirlo?" % (a, b, p), "%s €" % num(a * b * p), ["%s €" % num(2 * (a + b) * p), "%s €" % num(a * b + p), "%s €" % num(a * b)], "%d × %d = %d m²; %d × %d = <b>%s €</b>." % (a, b, a * b, a * b, p, num(a * b * p)))
    if k == "vela":
        a, b = R.randint(2, 6), R.randint(3, 8)
        return M("La vela de un barco es un triángulo de %d m de base y %d m de altura. ¿Cuántos m² de tela tiene?" % (a, b), "%s m²" % d(F(a * b, 2)), ["%d m²" % (a * b), "%d m²" % (a + b), "%s m²" % d(F(a * b, 4))], "%d × %d : 2 = <b>%s m²</b>." % (a, b, d(F(a * b, 2))))
    if k == "pintar":
        a, h = R.randint(3, 8), R.randint(2, 3)
        v = R.choice([2, 3, 4])
        return M("Una pared mide %d m de ancho y %d m de alto y tiene una ventana de 1 m². ¿Cuántos m² hay que pintar?" % (a, h), "%d m²" % (a * h - 1), ["%d m²" % (a * h), "%d m²" % (2 * (a + h)), "%d m²" % (a * h + 1)], "%d × %d − 1 = <b>%d m²</b>." % (a, h, a * h - 1))
    if k == "falta":
        A, a = R.randint(3, 15), R.randint(2, 9)
        return M("Un rectángulo tiene %d cm² de área y %d cm de base. ¿Cuánto mide su altura?" % (A * a, a), "%d cm" % A, ["%d cm" % (A * a - a), "%d cm" % (A * a // 2), "%d cm" % (A + a)], "%d : %d = <b>%d cm</b>." % (A * a, a, A))
    a = R.randint(3, 8)
    return M("¿Cuántas baldosas de 1 dm² hacen falta para cubrir un cuadrado de %d dm de lado?" % a, str(a * a), [str(4 * a) if 4 * a != a * a else str(a * a + 1), str(2 * a), str(a * a * 10)], "%d × %d = <b>%d</b>." % (a, a, a * a))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(40017 + lv * 1000)
    seen = set()
    sets = [
        ("Cuadrado y rectángulo", mix(R, seen, [(s1_rect, 20)])),
        ("Triángulo y romboide", mix(R, seen, [(s2_tri_para, 20)])),
        ("Rombo, trapecio y polígonos regulares" if lv == 6 else "Repaso", mix(R, seen, [(s3_otros, 20)] if lv == 6 else [(s1_rect, 10), (s2_tri_para, 10)])),
        ("Figuras compuestas", mix(R, seen, [(s4_compuesta, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    think = ["El <b>área</b> es la medida de una superficie y se expresa en unidades cuadradas (cm², m²).",
             "Rectángulo y romboide: <b>base × altura</b>. Cuadrado: lado × lado. Triángulo: <b>base × altura : 2</b> (es la mitad de un romboide).",
             "La <b>altura</b> es perpendicular a la base; no es el lado inclinado."]
    if lv == 6:
        think.append("Rombo: D × d : 2. Trapecio: (B + b) × h : 2. Polígono regular: perímetro × apotema : 2.")
    body = lesson(think,
                  [("Triángulo de base 10 cm y altura 6 cm", ["10 × 6 = 60", "60 : 2"], "30 cm²"),
                   ("Trapecio: B = 12, b = 8, h = 5" if lv == 6 else "Romboide: base 9 cm, altura 4 cm", ["(12 + 8) × 5 = 100", "100 : 2"] if lv == 6 else ["9 × 4"], "50 cm²" if lv == 6 else "36 cm²")],
                  [["Olvidar dividir entre 2", "El triángulo es la mitad del romboide."],
                   ["Usar el lado inclinado como altura", "La altura forma un ángulo recto con la base."],
                   ["Confundir perímetro y área", "Perímetro en cm; área en cm²."]],
                  figura("tri", 10, 6))
    faq = [("¿Por qué el área del triángulo se divide entre 2?", "Porque dos triángulos iguales forman un romboide, cuya área es base × altura. Cada triángulo es la mitad."),
           ("¿Cómo se calcula el área de una figura compuesta?", "Se descompone en figuras conocidas (rectángulos, triángulos…), se calcula el área de cada una y se suman (o se restan los huecos).")]
    make_unit(R, "area-de-figuras-planas", "M",
              "Cálculo del área de figuras planas: cuadrado, rectángulo, romboide, triángulo" + (", rombo, trapecio y polígonos regulares" if lv == 6 else "") + "; figuras compuestas; resolución de problemas",
              "Área de figuras planas", "Área de figuras planas",
              "Fichas de matemáticas de %d.º de Primaria: área del cuadrado, el rectángulo, el romboide y el triángulo%s, figuras compuestas y problemas. 100 ejercicios con soluciones." % (lv, ", el rombo, el trapecio y polígonos regulares" if lv == 6 else ""),
              "Triángulo: base × altura : 2", "Rectángulo y romboide: base × altura.",
              body, faq, sets, 17, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(6)
