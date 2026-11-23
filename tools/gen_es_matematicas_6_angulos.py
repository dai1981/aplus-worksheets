# -*- coding: utf-8 -*-
"""
España Matemáticas 6.º (y 5.º) de Primaria: Ángulos (Sentido espacial)
Medir y clasificar ángulos, ángulos complementarios y suplementarios, consecutivos, adyacentes y opuestos por el vértice,
la suma de los ángulos de un triángulo (180°) y de un cuadrilátero (360°); 6.º: grados, minutos y segundos (sistema sexagesimal).
Errores: confundir complementario (90°) y suplementario (180°), sumar los ángulos del triángulo a 360°, pasar 60′ como 100′.
"""
import random
from es_c3 import M, mix, lesson, make_unit, relabel, fig
import gen_au_maths_y5_angles as AU

R = None
LV = 6


def g(v):
    return "%d°" % v


def tipo(v):
    return "recto" if v == 90 else "agudo" if v < 90 else "obtuso" if v < 180 else "llano" if v == 180 else "cóncavo"


def s1_medir():
    v = R.choice(list(range(15, 170, 5)))
    if v == 90:
        return None
    if R.random() < 0.5:
        pic = relabel(AU.protractor_svg([0, v], "transportador"), "transportador midiendo un ángulo")
        return M(fig(pic) + "¿Cuánto mide el ángulo?", g(v), [g(180 - v), g(v + 10), g(v - 10)], "Un lado está en el 0 de la escala interior: el ángulo es %s y mide <b>%s</b>." % (tipo(v), g(v)))
    t = tipo(v)
    return M("Un ángulo mide %s. ¿Cómo es?" % g(v), "ángulo " + t, ["ángulo " + x for x in ("agudo", "recto", "obtuso", "llano") if x != t], "Agudo: menos de 90°; obtuso: entre 90° y 180°. Es <b>%s</b>." % t)


def s2_relaciones():
    k = R.choice(["compl", "supl", "compl", "supl", "opuestos", "adyacentes"])
    a = R.randint(10, 80)
    if k == "compl":
        return M("Dos ángulos son <b>complementarios</b> si suman 90°. ¿Cuál es el complementario de %s?" % g(a), g(90 - a), [g(180 - a), g(a), g(100 - a)], "90° − %s = <b>%s</b>." % (g(a), g(90 - a)))
    if k == "supl":
        a = R.randint(10, 170)
        if a == 90:
            return None
        return M("Dos ángulos son <b>suplementarios</b> si suman 180°. ¿Cuál es el suplementario de %s?" % g(a), g(180 - a), [g(90 - a) if a < 90 else g(360 - a), g(a), g(200 - a)], "180° − %s = <b>%s</b>." % (g(a), g(180 - a)))
    a = R.choice([35, 40, 50, 55, 60, 65, 70, 110, 120, 130])
    if k == "opuestos":
        return M("Dos rectas se cortan y forman un ángulo de %s. ¿Cuánto mide el ángulo opuesto por el vértice?" % g(a), g(a), [g(180 - a), g(90 - a) if a < 90 else g(360 - a), g(2 * a)], "Los ángulos opuestos por el vértice son iguales: <b>%s</b>." % g(a))
    return M("Dos rectas se cortan y forman un ángulo de %s. ¿Cuánto mide cada ángulo adyacente a él?" % g(a), g(180 - a), [g(a), g(90 - a) if a < 90 else g(a - 90), g(360 - a)], "Los ángulos adyacentes suman 180°: <b>%s</b>." % g(180 - a))


def s3_triangulo():
    k = R.choice(["tri", "tri", "rect", "iso", "cuad", "fig"])
    if k == "tri":
        a, b = R.randint(25, 100), R.randint(25, 70)
        c = 180 - a - b
        if c < 15:
            return None
        return M("Dos ángulos de un triángulo miden %s y %s. ¿Cuánto mide el tercero?" % (g(a), g(b)), g(c), [g(360 - a - b), g(a + b), g(c + 10), g(90 - a) if a < 90 and 90 - a != c else g(c - 10)], "180° − %s − %s = <b>%s</b>." % (g(a), g(b), g(c)))
    if k == "rect":
        a = R.randint(15, 75)
        return M("Un triángulo rectángulo tiene un ángulo de %s. ¿Cuánto mide el otro ángulo agudo?" % g(a), g(90 - a), [g(180 - a), g(a), g(270 - a)], "180° − 90° − %s = <b>%s</b>." % (g(a), g(90 - a)))
    if k == "iso":
        a = R.choice([30, 40, 50, 70, 80, 100, 120])
        return M("En un triángulo isósceles, el ángulo desigual mide %s. ¿Cuánto mide cada uno de los otros dos?" % g(a), g((180 - a) // 2), [g(180 - a), g(a), g((360 - a) // 2)], "(180° − %s) : 2 = <b>%s</b>." % (g(a), g((180 - a) // 2)))
    if k == "cuad":
        a, b, c = R.randint(60, 130), R.randint(60, 130), R.randint(50, 120)
        dd = 360 - a - b - c
        if not 40 <= dd <= 160:
            return None
        return M("Tres ángulos de un cuadrilátero miden %s, %s y %s. ¿Cuánto mide el cuarto?" % (g(a), g(b), g(c)), g(dd), [g(180 - a - b - c) if 180 - a - b - c > 0 else g(dd + 20), g(dd + 10), g(a + b + c)], "Los ángulos de un cuadrilátero suman 360°: <b>%s</b>." % g(dd))
    a, b = R.choice([(50, 60), (40, 75), (35, 65), (55, 70), (45, 80), (30, 100), (25, 110)])
    pts = AU.tri_pts(a, b, 170, 0)
    pic = fig(relabel(AU.shape_svg(pts, {0: g(a), 1: g(b), 2: "?"}, "triángulo"), "triángulo con dos ángulos marcados"))
    return M(pic + "¿Cuánto mide el ángulo marcado con «?»?", g(180 - a - b), [g(360 - a - b), g(a + b), g(180 - a - b + 10)], "180° − %s − %s = <b>%s</b>." % (g(a), g(b), g(180 - a - b)))


def sx(gr, mi, se=0):
    return "%d° %d′%s" % (gr, mi, " %d″" % se if se else "")


def s4_sexagesimal():
    k = R.choice(["min", "seg", "suma", "resta", "pasar"])
    if k == "min":
        a = R.randint(2, 9)
        return M("¿Cuántos minutos son %s?" % g(a), "%d′" % (a * 60), ["%d′" % (a * 100), "%d′" % (a * 10), "%d′" % (a * 360)], "1° = 60′: %d × 60 = <b>%d′</b>." % (a, a * 60))
    if k == "seg":
        a = R.randint(2, 9)
        return M("¿Cuántos segundos son %d′?" % a, "%d″" % (a * 60), ["%d″" % (a * 100), "%d″" % (a * 10), "%d″" % (a * 3600)], "1′ = 60″: <b>%d″</b>." % (a * 60))
    if k == "pasar":
        m = R.randint(61, 200)
        if m % 60 == 0:
            return None
        return M("Expresa %d′ en grados y minutos." % m, sx(m // 60, m % 60), [sx(m // 100, m % 100) if m >= 100 else sx(m // 60 + 1, m % 60), sx(m // 60, m % 60 + 10), sx(m // 10, m % 10)],
                 "%d′ = %d × 60′ + %d′ = <b>%s</b>." % (m, m // 60, m % 60, sx(m // 60, m % 60)))
    a, b, c, dd = R.randint(10, 80), R.randint(5, 59), R.randint(5, 60), R.randint(5, 59)
    if k == "suma":
        t = (a + c) * 60 + b + dd
        return M("Calcula: %s + %s" % (sx(a, b), sx(c, dd)), sx(t // 60, t % 60), [sx(a + c, b + dd) if b + dd >= 60 else sx(a + c + 1, (b + dd) % 60), sx(a + c, (b + dd) % 60) if b + dd >= 60 else sx(a + c, b + dd + 1), sx(t // 60 + 1, t % 60)],
                 "%s; como 60′ = 1°: <b>%s</b>." % (sx(a + c, b + dd), sx(t // 60, t % 60)) if b + dd >= 60 else "Sumamos grados y minutos: <b>%s</b>." % sx(t // 60, t % 60))
    t1, t2 = a * 60 + b, c * 60 + dd
    if t1 <= t2:
        t1, t2 = t2, t1
    r = t1 - t2
    if t1 % 60 >= t2 % 60:
        return None
    return M("Calcula: %s − %s" % (sx(t1 // 60, t1 % 60), sx(t2 // 60, t2 % 60)), sx(r // 60, r % 60), [sx(t1 // 60 - t2 // 60, abs(t1 % 60 - t2 % 60)), sx(r // 60 + 1, r % 60), sx(r // 60, (r % 60 + 40) % 60)],
             "Pasamos 1° a 60′: %s − %s = <b>%s</b>." % (sx(t1 // 60 - 1, t1 % 60 + 60), sx(t2 // 60, t2 % 60), sx(r // 60, r % 60)))


def s5_problema():
    k = R.choice(["reloj", "giro", "porcion", "rampa", "suma"])
    if k == "reloj":
        h = R.randint(1, 11)
        dd = h * 30 if h <= 6 else 360 - h * 30
        return M("¿Qué ángulo (el más pequeño) forman las agujas del reloj a las %d:00?" % h, g(dd), [g(h * 5), g(dd + 30), g(360 - dd) if dd != 180 else g(90)], "Cada hora son 30°: <b>%s</b>." % g(dd))
    if k == "giro":
        f, v = R.choice([("un cuarto de vuelta", 90), ("media vuelta", 180), ("tres cuartos de vuelta", 270), ("una vuelta y media", 540), ("un octavo de vuelta", 45)])
        return M("Una noria gira %s. ¿Cuántos grados ha girado?" % f, g(v), [g(x) for x in (90, 180, 270, 360, 45, 540) if x != v], "Una vuelta = 360°: <b>%s</b>." % g(v))
    if k == "porcion":
        n = R.choice([4, 5, 6, 8, 9, 10, 12])
        return M("Una pizza redonda se corta en %d porciones iguales desde el centro. ¿Qué ángulo tiene cada porción?" % n, g(360 // n), [g(180 // n) if 180 % n == 0 else g(360 // n + 5), g(360 - n), g(100 // n * 10 if n < 10 else 30 if n != 12 else 36)], "360° : %d = <b>%s</b>." % (n, g(360 // n)))
    if k == "rampa":
        a = R.randint(10, 40)
        return M("Una rampa forma un ángulo de %s con el suelo. ¿Qué ángulo forma con la pared, que es perpendicular al suelo?" % g(a), g(90 - a), [g(180 - a), g(a), g(90 + a)], "Los tres ángulos del triángulo suman 180°: 180° − 90° − %s = <b>%s</b>." % (g(a), g(90 - a)))
    a, b = R.randint(20, 70), R.randint(20, 70)
    return M("Un ángulo de %s y otro de %s son consecutivos (comparten vértice y un lado). ¿Cuánto mide el ángulo que forman juntos?" % (g(a), g(b)), g(a + b), [g(abs(a - b)) if a != b else g(a + b + 10), g(180 - a - b), g(a + b + 10)], "%s + %s = <b>%s</b>." % (g(a), g(b), g(a + b)))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(40015 + lv * 1000)
    seen = set()
    sets = [
        ("Medir y clasificar ángulos", mix(R, seen, [(s1_medir, 20)])),
        ("Complementarios, suplementarios y opuestos", mix(R, seen, [(s2_relaciones, 20)])),
        ("Ángulos de triángulos y cuadriláteros", mix(R, seen, [(s3_triangulo, 20)])),
        ("Grados, minutos y segundos" if lv == 6 else "Repaso", mix(R, seen, [(s4_sexagesimal, 20)] if lv == 6 else [(s1_medir, 6), (s2_relaciones, 7), (s3_triangulo, 7)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    think = ["Los ángulos se miden en <b>grados</b> con el transportador. Agudo: menos de 90°; recto: 90°; obtuso: entre 90° y 180°; llano: 180°.",
             "<b>Complementarios</b>: suman 90°. <b>Suplementarios</b>: suman 180°. Los ángulos <b>opuestos por el vértice</b> son iguales.",
             "Los ángulos de un <b>triángulo</b> suman 180° y los de un <b>cuadrilátero</b>, 360°."]
    if lv == 6:
        think.append("Sistema sexagesimal: 1° = 60′ (minutos) y 1′ = 60″ (segundos). Al sumar, cada 60′ forman 1°.")
    body = lesson(think,
                  [("Triángulo con ángulos de 48° y 75°", ["180° − 48° − 75°"], "57°"),
                   ("25° 40′ + 18° 35′" if lv == 6 else "Suplementario de 125°", ["43° 75′", "75′ = 1° 15′"] if lv == 6 else ["180° − 125°"], "44° 15′" if lv == 6 else "55°")],
                  [["Confundir complementario y suplementario", "Complementario → 90°; suplementario → 180°."],
                   ["Sumar los ángulos del triángulo a 360°", "Triángulo: 180°. Cuadrilátero: 360°."],
                   ["Pasar de minutos con 100" if lv == 6 else "Leer la escala equivocada", "60′ = 1°, no 100′." if lv == 6 else "Comprueba si el ángulo es agudo u obtuso."]])
    faq = [("¿Cuánto suman los ángulos de un triángulo?", "Siempre 180°. Por eso, si conoces dos ángulos, el tercero es 180° menos la suma de los otros dos."),
           ("¿Qué son ángulos complementarios y suplementarios?", "Complementarios: dos ángulos que suman 90°. Suplementarios: dos ángulos que suman 180°.")]
    make_unit(R, "angulos", "E",
              "Ángulos: medida con el transportador, clasificación, relaciones entre ángulos (complementarios, suplementarios, adyacentes y opuestos por el vértice), suma de los ángulos de triángulos y cuadriláteros" + ("; sistema sexagesimal" if lv == 6 else ""),
              "Ángulos: medida y relaciones", "Ángulos",
              "Fichas de matemáticas de %d.º de Primaria: medir y clasificar ángulos, complementarios y suplementarios, ángulos de triángulos y cuadriláteros%s y problemas. 100 ejercicios con soluciones." % (lv, ", grados y minutos" if lv == 6 else ""),
              "Triángulo: 180°. Cuadrilátero: 360°", "Complementarios: 90°. Suplementarios: 180°.",
              body, faq, sets, 15, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(6)
