# -*- coding: utf-8 -*-
"""
España Matemáticas 2.º de ESO: Teorema de Pitágoras (Sentido espacial)
Hipotenusa y catetos, reconocer triángulos rectángulos, aplicaciones en figuras planas y en el espacio, problemas.
Errores: sumar los lados sin elevar al cuadrado, restar en lugar de sumar al calcular la hipotenusa, aplicar el teorema a triángulos que no son rectángulos.
"""
import math
import random
from fractions import Fraction as F
from es_eso import M, mix, d, num, raiz, unit, L, Kids, figure

R = random.Random(48009)
K = Kids(R)
TRIP = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41), (6, 8, 10), (9, 12, 15), (12, 16, 20), (15, 20, 25), (10, 24, 26), (12, 35, 37)]


def L_(v):
    """longitud: entera o redondeada a décimas"""
    if abs(v - round(v)) < 1e-9:
        return num(int(round(v)))
    return d(F(int(math.floor(v * 10 + 0.5)), 10))


def tri(a, b, c, ask):
    pts = {"A": (0, 0), "B": (b, 0), "C": (0, a)}
    lab = {"a": "%s cm" % a if ask != "a" else "?", "b": "%s cm" % b if ask != "b" else "?", "c": "%s cm" % c if ask != "c" else "?"}
    return figure(pts, [("A", "B"), ("B", "C"), ("C", "A")], sides=[("A", "C", lab["a"]), ("A", "B", lab["b"]), ("B", "C", lab["c"])], right=[("A", "B", "C")], label="triángulo rectángulo")


def s_hip():
    a, b, c = R.choice(TRIP)
    k = R.choice([1, 1, 2]) if c < 30 else 1
    a, b, c = a * k, b * k, c * k
    if R.random() < 0.5:
        a, b = b, a
    if R.random() < 0.6:
        return M(tri(a, b, c, "c") + "Calcula la hipotenusa.", "%s cm" % num(c), ["%s cm" % num(a + b), "%s cm" % L_(math.sqrt(abs(b * b - a * a))) if a != b else "%s cm" % num(c + 1), "%s cm" % num(c * c)],
                 "c² = %d² + %d² = %s; c = <b>%s cm</b>." % (a, b, num(c * c), num(c)))
    x, y = R.randint(2, 12), R.randint(2, 12)
    h = math.sqrt(x * x + y * y)
    if abs(h - round(h)) < 1e-9:
        return None
    return M("Los catetos de un triángulo rectángulo miden %d cm y %d cm. ¿Cuánto mide la hipotenusa (redondea a las décimas)?" % (x, y), "%s cm" % L_(h), ["%d cm" % (x + y), "%s cm" % L_(math.sqrt(abs(x * x - y * y))) if x != y else "%d cm" % (x + 1), "%s cm" % L_(h + 1)],
             "c = √(%d + %d) = √%d ≈ <b>%s cm</b>." % (x * x, y * y, x * x + y * y, L_(h)))


def s_cateto():
    a, b, c = R.choice(TRIP)
    if R.random() < 0.5:
        a, b = b, a
    if R.random() < 0.6:
        return M(tri(a, b, c, "b") + "Calcula el cateto que falta.", "%s cm" % num(b), ["%s cm" % L_(math.sqrt(a * a + c * c)), "%s cm" % num(c - a), "%s cm" % num(b + 1)],
                 "b² = c² − a² = %s − %s = %s; b = <b>%s cm</b>." % (num(c * c), num(a * a), num(b * b), num(b)))
    c2 = R.randint(8, 20)
    a2 = R.randint(2, c2 - 1)
    v = math.sqrt(c2 * c2 - a2 * a2)
    if abs(v - round(v)) < 1e-9:
        return None
    return M("La hipotenusa de un triángulo rectángulo mide %d cm y un cateto %d cm. ¿Cuánto mide el otro cateto (a las décimas)?" % (c2, a2), "%s cm" % L_(v), ["%s cm" % L_(math.sqrt(c2 * c2 + a2 * a2)), "%d cm" % (c2 - a2), "%s cm" % L_(v + 1)],
             "b = √(%d − %d) = √%d ≈ <b>%s cm</b>." % (c2 * c2, a2 * a2, c2 * c2 - a2 * a2, L_(v)))


def s_rect():
    if R.random() < 0.5:
        a, b, c = R.choice(TRIP)
        ok = "sí"
    else:
        a, b = R.randint(3, 15), R.randint(3, 15)
        c = int(math.sqrt(a * a + b * b)) + R.choice([1, 2])
        ok = "no"
        if a * a + b * b == c * c:
            return None
    s = sorted([a, b, c])
    tipo = "rectángulo" if s[0] ** 2 + s[1] ** 2 == s[2] ** 2 else "acutángulo" if s[0] ** 2 + s[1] ** 2 > s[2] ** 2 else "obtusángulo"
    if R.random() < 0.5:
        return M("¿Es rectángulo un triángulo de lados %d cm, %d cm y %d cm?" % tuple(s), ok, ["no" if ok == "sí" else "sí", "solo si es isósceles", "no se puede saber"],
                 "%d² + %d² = %d y %d² = %d: <b>%s</b>." % (s[0], s[1], s[0] ** 2 + s[1] ** 2, s[2], s[2] ** 2, "sí, son iguales" if ok == "sí" else "no, son distintos"))
    return M("Un triángulo tiene lados %d cm, %d cm y %d cm. ¿Cómo es según sus ángulos?" % tuple(s), tipo, [x for x in ("rectángulo", "acutángulo", "obtusángulo", "equilátero") if x != tipo],
             "Comparamos %d con %d² = %d: <b>%s</b>." % (s[0] ** 2 + s[1] ** 2, s[2], s[2] ** 2, tipo))


def s_figuras():
    t = R.choice(["diag_rect", "diag_cuad", "iso", "equi", "rombo", "ortoedro"])
    if t == "diag_rect":
        a, b, c = R.choice(TRIP)
        return M("¿Cuánto mide la diagonal de un rectángulo de %d cm × %d cm?" % (a, b), "%s cm" % num(c), ["%s cm" % num(a + b), "%s cm" % num(2 * (a + b)), "%s cm" % num(c + 2)], "d = √(%d² + %d²) = <b>%s cm</b>." % (a, b, num(c)))
    if t == "diag_cuad":
        l = R.randint(2, 15)
        return M("¿Cuánto mide la diagonal de un cuadrado de %d cm de lado? (exacto)" % l, "%s cm" % raiz(2 * l * l), ["%d cm" % (2 * l), "%s cm" % raiz(l * l), "%s cm" % raiz(2 * l)], "d = √(%d² + %d²) = √%d = <b>%s cm</b>." % (l, l, 2 * l * l, raiz(2 * l * l)))
    if t == "iso":
        a, b, c = R.choice(TRIP)
        return M("Un triángulo isósceles tiene los lados iguales de %d cm y la base de %d cm. ¿Cuánto mide su altura?" % (c, 2 * a), "%s cm" % num(b), ["%s cm" % L_(math.sqrt(c * c - 4 * a * a)) if c > 2 * a else "%s cm" % num(c - a), "%s cm" % num(c), "%s cm" % num(b + 1)],
                 "La altura divide la base en dos mitades de %d cm: h = √(%d² − %d²) = <b>%s cm</b>." % (a, c, a, num(b)))
    if t == "equi":
        l = R.choice([2, 4, 6, 8, 10, 12])
        return M("¿Cuánto mide la altura de un triángulo equilátero de %d cm de lado? (exacto)" % l, "%s cm" % raiz(3 * (l // 2) ** 2), ["%s cm" % raiz(5 * (l // 2) ** 2), "%d cm" % l, "%s cm" % raiz(3 * l * l)],
                 "h = √(%d² − %d²) = √%d = <b>%s cm</b>." % (l, l // 2, 3 * (l // 2) ** 2, raiz(3 * (l // 2) ** 2)))
    if t == "rombo":
        a, b, c = R.choice(TRIP)
        return M("Las diagonales de un rombo miden %d cm y %d cm. ¿Cuánto mide su lado?" % (2 * a, 2 * b), "%s cm" % num(c), ["%s cm" % num(2 * c), "%s cm" % num(a + b), "%s cm" % L_(math.sqrt(4 * a * a + 4 * b * b))], "Las semidiagonales son %d y %d: l = √(%d² + %d²) = <b>%d cm</b>." % (a, b, a, b, c))
    x, y, z = R.choice([(3, 4, 12), (2, 3, 6), (1, 4, 8), (2, 6, 9), (6, 6, 7), (2, 10, 11), (4, 4, 7), (1, 2, 2)])
    D = math.sqrt(x * x + y * y + z * z)
    return M("¿Cuánto mide la diagonal de un ortoedro de %d cm × %d cm × %d cm?" % (x, y, z), "%s cm" % L_(D), ["%s cm" % L_(math.sqrt(x * x + y * y)), "%d cm" % (x + y + z), "%s cm" % L_(D + 1)], "D = √(%d² + %d² + %d²) = <b>%s cm</b>." % (x, y, z, L_(D)))


def s_problema():
    t = R.choice(["escalera", "tv", "cometa", "rampa", "parque", "mastil"])
    a, b, c = R.choice(TRIP[:8])
    if t == "escalera":
        return M("Una escalera de %d m se apoya en una pared y su pie está a %d m de la pared. ¿A qué altura llega?" % (c, a), "%d m" % b, ["%d m" % (c - a), "%s m" % L_(math.sqrt(c * c + a * a)), "%d m" % (b + 1)], "h = √(%d² − %d²) = <b>%d m</b>." % (c, a, b))
    if t == "tv":
        w, h = R.choice([(32, 18), (48, 27), (64, 36), (80, 45)])
        dg = math.sqrt(w * w + h * h)
        return M("Una pantalla mide %d pulgadas de ancho y %d de alto. ¿Cuántas pulgadas mide su diagonal (a las unidades)?" % (w, h), "%d pulgadas" % round(dg), ["%d pulgadas" % (w + h), "%d pulgadas" % w, "%d pulgadas" % (round(dg) + 5)], "d = √(%d² + %d²) ≈ <b>%d pulgadas</b>." % (w, h, round(dg)))
    if t == "cometa":
        return M("Una cometa está atada con un hilo tenso de %d m. Su sombra en el suelo está a %d m de quien la sujeta. ¿A qué altura vuela (desde la mano)?" % (c, a), "%d m" % b, ["%d m" % (c - a), "%s m" % L_(math.sqrt(c * c + a * a)), "%d m" % c], "h = √(%d² − %d²) = <b>%d m</b>." % (c, a, b))
    if t == "rampa":
        return M("Una rampa sube %d m de altura en %d m de distancia horizontal. ¿Cuánto mide la rampa?" % (a, b), "%d m" % c, ["%d m" % (a + b), "%d m" % (b - a) if b > a else "%d m" % (a - b), "%d m" % (c + 1)], "√(%d² + %d²) = <b>%d m</b>." % (a, b, c))
    if t == "parque":
        return M("Un parque rectangular mide %d m × %d m. ¿Cuántos metros te ahorras si lo cruzas por la diagonal en lugar de por los bordes?" % (a * 10, b * 10), "%d m" % ((a + b - c) * 10), ["%d m" % (c * 10), "%d m" % ((a + b) * 10), "%d m" % ((a + b - c) * 10 + 10)],
                 "Bordes %d m, diagonal %d m: ahorro <b>%d m</b>." % ((a + b) * 10, c * 10, (a + b - c) * 10))
    return M("Un mástil de %d m se sujeta con un cable desde la punta hasta un punto del suelo a %d m de la base. ¿Cuánto mide el cable?" % (b, a), "%d m" % c, ["%d m" % (a + b), "%d m" % (b - a) if b > a else "%d m" % (c - 2), "%d m" % (c + 2)], "√(%d² + %d²) = <b>%d m</b>." % (b, a, c))


seen = set()
sets = [("Calcular la hipotenusa", mix(R, seen, [(s_hip, 20)])), ("Calcular un cateto", mix(R, seen, [(s_cateto, 20)])), ("¿Es rectángulo?", mix(R, seen, [(s_rect, 20)])),
        ("Pitágoras en figuras", mix(R, seen, [(s_figuras, 20)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
body = L(["En un triángulo rectángulo, la <b>hipotenusa</b> es el lado opuesto al ángulo recto y los otros dos son los <b>catetos</b>.",
          "<b>Teorema de Pitágoras</b>: c² = a² + b². Para un cateto: b² = c² − a².",
          "Si en un triángulo se cumple c² = a² + b², es rectángulo; si c² &lt; a² + b², acutángulo; si c² &gt; a² + b², obtusángulo."],
         [("Catetos 6 cm y 8 cm", ["c² = 36 + 64 = 100"], "c = 10 cm"), ("Hipotenusa 13 m y un cateto 5 m", ["b² = 169 − 25 = 144"], "b = 12 m")],
         [["Sumar los lados sin elevar al cuadrado", "6 + 8 no es la hipotenusa: √(36 + 64) = 10."], ["Sumar al calcular un cateto", "Para un cateto se resta: c² − a²."], ["Aplicarlo a cualquier triángulo", "Solo vale si hay un ángulo recto."]],
         tri(6, 8, 10, "c"))
faq = [("¿Para qué sirve el teorema de Pitágoras?", "Para calcular un lado de un triángulo rectángulo conociendo los otros dos, y para saber si un triángulo es rectángulo."),
       ("¿Qué es una terna pitagórica?", "Tres números enteros que cumplen a² + b² = c², como 3, 4 y 5.")]
unit(2, R, "teorema-de-pitagoras", "E", "Teorema de Pitágoras: justificación geométrica y aplicaciones en figuras planas y en el espacio; resolución de problemas",
     "Teorema de Pitágoras", "Teorema de Pitágoras",
     "Fichas de matemáticas de 2.º de ESO: hipotenusa, catetos, triángulos rectángulos, Pitágoras en figuras planas y en el espacio y problemas. 100 ejercicios con soluciones.",
     "c² = a² + b²", "c es la hipotenusa, el lado mayor.", body, faq, sets, 9)
