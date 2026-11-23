# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: Ángulos (Sentido espacial)
Elementos de un ángulo (vértice y lados), el grado, ángulos recto, agudo, obtuso, llano y completo, medir con el transportador,
estimar, ángulos complementarios y suplementarios, sumar y restar ángulos, giros y ángulos en el reloj.
Errores: leer la escala equivocada del transportador (180° − x), pensar que el ángulo depende de lo largos que son los lados.
"""
import random
from es_common import mcq, mix, lesson, make_unit, relabel, fig, bank
import fr_common as _F
import gen_au_maths_y5_angles as AU

R = random.Random(44018)


def g(v):
    return "%d°" % v


def tipo(d):
    return "recto" if d == 90 else "agudo" if d < 90 else "obtuso" if d < 180 else "llano" if d == 180 else "completo" if d == 360 else "cóncavo"


def s1_tipo():
    if R.random() < 0.5:
        v = R.choice([20, 30, 40, 50, 60, 70, 90, 90, 110, 120, 130, 140, 150, 160, 180])
        rot = R.choice([0, 0, 15, 30, 40])
        pic = fig(relabel(AU.angle_fig(v, rot), "un ángulo"))
        t = tipo(v)
        return mcq(pic + "¿Qué tipo de ángulo es?", "ángulo " + t, ["ángulo " + x for x in ("agudo", "recto", "obtuso", "llano") if x != t],
                   "Agudo: menos de 90°; recto: 90°; obtuso: entre 90° y 180°; llano: 180°. Es un <b>ángulo %s</b>." % t)
    d = R.choice(list(range(10, 90, 5)) + list(range(95, 180, 5)) + [90, 180, 360])
    t = tipo(d)
    return mcq("Un ángulo mide %s. ¿Cómo se llama?" % g(d), "ángulo " + t, ["ángulo " + x for x in ("agudo", "recto", "obtuso", "llano", "completo") if x != t],
               "Agudo: menos de 90°; recto: 90°; obtuso: entre 90° y 180°; llano: 180°; completo: 360°. %s es un <b>ángulo %s</b>." % (g(d), t))


s1_conceptos = bank(R, [
    ("¿Cuántos grados mide un ángulo recto?", "90°", ["180°", "45°", "100°"]),
    ("¿Cuántos grados mide un ángulo llano?", "180°", ["90°", "360°", "100°"]),
    ("¿Cuántos grados mide un ángulo completo?", "360°", ["180°", "100°", "400°"]),
    ("¿Cuántos grados mide la mitad de un ángulo recto?", "45°", ["90°", "30°", "50°"]),
    ("¿Cuántos ángulos rectos forman un ángulo completo?", "4", ["2", "3", "360"]),
    ("¿Con qué instrumento se miden los ángulos?", "con el transportador", ["con el compás", "con la regla", "con la báscula"]),
    ("¿Cómo se llama el punto donde se juntan los dos lados de un ángulo?", "vértice", ["lado", "centro", "arista"]),
    ("Si alargas los lados de un ángulo de 40°, ¿cuánto mide el ángulo?", "40°", ["80°", "más de 40°", "menos de 40°"]),
    ("¿Cuántos ángulos rectos forman un ángulo llano?", "2", ["1", "3", "4"]),
    ("¿Qué ángulo forman las agujas de un reloj a las 3:00?", "un ángulo recto", ["un ángulo llano", "un ángulo agudo", "un ángulo obtuso"]),
    ("¿Qué ángulo forman las agujas de un reloj a las 6:00?", "un ángulo llano", ["un ángulo recto", "un ángulo agudo", "un ángulo completo"]),
], "conceptos")


def s2_transportador():
    v = R.choice(list(range(20, 165, 5)))
    if v == 90:
        return None
    if R.random() < 0.5:
        pic = AU.protractor_svg([0, v], "transportador")
        e = "Un lado está en el 0 de la derecha: leemos la escala <b>interior</b>, que empieza en 0 a la derecha. El otro lado pasa por el %d. El ángulo es %s: mide <b>%s</b>." % (v, tipo(v), g(v))
    else:
        pic = AU.protractor_svg([180, 180 - v], "transportador")
        e = "Un lado está en el 0 de la izquierda: leemos la escala <b>exterior</b>, que empieza en 0 a la izquierda. El otro lado pasa por el %d. El ángulo es %s: mide <b>%s</b>." % (v, tipo(v), g(v))
    pic = relabel(pic, "transportador midiendo un ángulo")
    return mcq(fig(pic) + "¿Cuánto mide el ángulo?", g(v), [g(180 - v), g(v + 10), g(v - 10), g(v + 5)], e + " (%s es lo que se lee en la otra escala.)" % g(180 - v))


def s2_estimar():
    v = R.choice([20, 30, 40, 45, 60, 70, 100, 120, 135, 150, 160])
    rot = R.choice([0, 0, 10, 20, 30])
    pic = fig(relabel(AU.angle_fig(v, rot), "un ángulo"))
    opts = [x for x in (20, 45, 70, 100, 135, 160, 30, 120, 60, 150) if abs(x - v) >= 25]
    R.shuffle(opts)
    return mcq(pic + "Estima: ¿qué medida se parece más a este ángulo?", g(v), [g(x) for x in opts],
               "Compara con el ángulo recto (90°): el ángulo es %s. La medida más cercana es <b>%s</b>." % (tipo(v), g(v)))


def s3_compl():
    k = R.choice(["compl", "supl", "compl", "supl", "suma", "resta"])
    if k == "compl":
        a = R.randint(5, 85)
        return mcq("Dos ángulos son <b>complementarios</b> si suman 90°. Un ángulo mide %s. ¿Cuánto mide su complementario?" % g(a), g(90 - a), [g(180 - a), g(a), g(100 - a)], "90° − %s = <b>%s</b>." % (g(a), g(90 - a)))
    if k == "supl":
        a = R.randint(10, 170)
        if a == 90:
            return None
        return mcq("Dos ángulos son <b>suplementarios</b> si suman 180°. Un ángulo mide %s. ¿Cuánto mide su suplementario?" % g(a), g(180 - a), [g(90 - a) if a < 90 else g(360 - a), g(a), g(200 - a)], "180° − %s = <b>%s</b>." % (g(a), g(180 - a)))
    a, b = R.randint(15, 80), R.randint(15, 80)
    if k == "suma":
        return mcq("Un ángulo de %s y otro de %s están juntos (tienen el mismo vértice y un lado común). ¿Cuánto mide el ángulo que forman?" % (g(a), g(b)), g(a + b),
                   [g(abs(a - b)) if a != b else g(a + b + 10), g(180 - a - b), g(a + b + 10)], "%s + %s = <b>%s</b>." % (g(a), g(b), g(a + b)))
    s = a + b + R.randint(20, 60)
    return mcq("Un ángulo de %s se divide en dos partes. Una parte mide %s. ¿Cuánto mide la otra?" % (g(s), g(a)), g(s - a), [g(s + a), g(180 - a), g(s - a + 10)], "%s − %s = <b>%s</b>." % (g(s), g(a), g(s - a)))


def s4_giros():
    k = R.choice(["giro", "giro2", "reloj", "reloj"])
    if k == "giro":
        f, v = R.choice([("un cuarto de vuelta", 90), ("media vuelta", 180), ("tres cuartos de vuelta", 270), ("una vuelta completa", 360)])
        return mcq("Un robot gira %s. ¿Cuántos grados gira?" % f, g(v), [g(x) for x in (90, 180, 270, 360, 45) if x != v], "Una vuelta completa son 360°: %s = <b>%s</b>." % (f, g(v)))
    if k == "giro2":
        a, b = R.choice([(90, 90), (90, 180), (45, 45), (180, 90), (90, 45), (45, 90), (180, 180)])
        return mcq("Una bailarina gira %s y después otros %s en el mismo sentido. ¿Cuántos grados ha girado en total?" % (g(a), g(b)), g(a + b),
                   [g(abs(a - b)) if a != b else g(a + b + 90), g(a + b + 45), g(a + b - 45)], "%s + %s = <b>%s</b>." % (g(a), g(b), g(a + b)))
    h = R.randint(1, 11)
    d = h * 30 if h <= 6 else 360 - h * 30
    return mcq("A las %d:00, ¿qué ángulo (el más pequeño) forman las agujas del reloj?" % h, g(d), [g(h * 5), g(d + 30), g(360 - d) if d != 180 else g(90), g(d - 30) if d > 30 else g(45)],
               "Entre dos números del reloj hay 360° : 12 = 30°. A las %d:00 las agujas están separadas %d números: %d × 30° = <b>%s</b>." % (h, d // 30, d // 30, g(d)))


def main():
    seen = set()
    sets = [
        ("Tipos de ángulos", mix(R, seen, [(s1_tipo, 12), (s1_conceptos, 8)])),
        ("Medir con el transportador", mix(R, seen, [(s2_transportador, 20)])),
        ("Estimar ángulos", mix(R, seen, [(s2_estimar, 10), (s1_tipo, 10)])),
        ("Complementarios, suplementarios, sumas y restas", mix(R, seen, [(s3_compl, 20)])),
        ("Giros y el reloj", mix(R, seen, [(s4_giros, 17), (s1_conceptos, 3)])),
    ]
    body = lesson(
        ["Un <b>ángulo</b> está formado por dos <b>lados</b> que salen de un mismo punto, el <b>vértice</b>. Los ángulos se miden en <b>grados</b> (°) con el <b>transportador</b>.",
         "Recto = 90°; llano = 180°; completo = 360°. Agudo: menos de 90°. Obtuso: entre 90° y 180°.",
         "Para medir, pon el centro del transportador en el vértice y el 0 sobre un lado. Lee la escala que empieza en 0 en ese lado.",
         "Complementarios: suman 90°. Suplementarios: suman 180°."],
        [("¿Cuánto mide el complementario de 35°?", ["90° − 35°"], "55°"),
         ("Un robot gira tres cuartos de vuelta", ["Una vuelta = 360°", "360° : 4 × 3"], "270°")],
        [["Leer la escala equivocada", "Un ángulo agudo no puede medir 130°: comprueba con el tipo de ángulo."],
         ["Pensar que lados más largos hacen un ángulo mayor", "El ángulo no cambia si alargas los lados."],
         ["Confundir complementario y suplementario", "Complementario → 90°; suplementario → 180°."]],
        fig(relabel(AU.angle_fig(60, 0), "un ángulo de 60 grados")))
    faq = [("¿Cómo se mide un ángulo con el transportador?", "Se coloca el centro del transportador en el vértice y la línea del 0 sobre uno de los lados. Se lee el número por el que pasa el otro lado en la escala que empieza en 0."),
           ("¿Qué son ángulos complementarios y suplementarios?", "Dos ángulos son complementarios si suman 90° y suplementarios si suman 180°.")]
    make_unit(R, "angulos", "E",
              "Ángulos: elementos, clasificación (recto, agudo, obtuso, llano y completo), medida en grados con el transportador, estimación; giros",
              "Ángulos: tipos y medida", "Ángulos",
              "Fichas de matemáticas de 4.º de Primaria: ángulos recto, agudo, obtuso, llano y completo, medir con el transportador, estimar, complementarios, suplementarios y giros. 100 ejercicios con soluciones.",
              "Recto 90°, llano 180°, completo 360°", "Agudo: menos de 90°. Obtuso: más de 90°.",
              body, faq, sets, 18)


if __name__ == "__main__":
    main()
