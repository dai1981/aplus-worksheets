# -*- coding: utf-8 -*-
"""
España Matemáticas I (1.º de Bachillerato): Resolución de triángulos (Sentido espacial)
Teorema del seno, teorema del coseno, área con dos lados y el ángulo comprendido, resolver triángulos cualesquiera, problemas (distancias inaccesibles, navegación, topografía).
Errores: usar el teorema del seno con el lado y el ángulo que no se corresponden, olvidar el segundo triángulo (caso ambiguo), calculadora en radianes.
"""
import math
import random
from es_bach import M, mix, num, unit, L, r2, figure, W

R = random.Random(51006)


def tri_pic(a, b, C, lab):
    """triángulo con CA = b sobre el eje y CB = a con ángulo C"""
    Cx, Cy = 0, 0
    A = (b, 0)
    B = (a * math.cos(math.radians(C)), a * math.sin(math.radians(C)))
    s = 6 / max(a, b, 1)
    pts = {"C": (0, 0), "A": (A[0] * s, 0), "B": (B[0] * s, B[1] * s)}
    return figure(pts, [("A", "B"), ("B", "C"), ("C", "A")], sides=[("B", "C", lab[0]), ("C", "A", lab[1]), ("A", "B", lab[2])], label="triángulo ABC")


def ang(x):
    return "%s°" % r2(x, 1)


def s_seno():
    A, B = R.randint(25, 80), R.randint(25, 80)
    C = 180 - A - B
    if C < 20:
        return None
    a = R.randint(5, 30)
    k = a / math.sin(math.radians(A))
    b, c = k * math.sin(math.radians(B)), k * math.sin(math.radians(C))
    t = R.choice(["b", "c", "C"])
    if t == "C":
        return M("En un triángulo, A = %d° y B = %d°. ¿Cuánto mide C?" % (A, B), "%d°" % C, ["%d°" % (180 - A), "%d°" % (90 - A + B) if 90 - A + B != C else "%d°" % (C + 10), "%d°" % abs(A - B) if A != B else "%d°" % (C - 10)], "A + B + C = 180°: <b>%d°</b>." % C)
    v = b if t == "b" else c
    ang_ = B if t == "b" else C
    return M("En un triángulo, a = %d cm, A = %d° y %s = %d°. Calcula %s (redondea a las centésimas)." % (a, A, "B" if t == "b" else "C", ang_, t) + (" (B = %d°)" % B if t == "c" else ""),
             "%s cm" % r2(v), W(["%s cm" % r2(a * math.sin(math.radians(A)) / math.sin(math.radians(ang_))), "%s cm" % r2(a * ang_ / A), "%s cm" % r2(abs(a * math.cos(math.radians(ang_)) / math.cos(math.radians(A)))), "%s cm" % r2(a * math.sin(math.radians(ang_)))]),
             "Teorema del seno: %s / sen %d° = %d / sen %d° → %s ≈ <b>%s cm</b>." % (t, ang_, a, A, t, r2(v)))


def s_coseno():
    t = R.choice(["lado", "lado", "angulo", "angulo"])
    if t == "lado":
        a, b = R.randint(4, 20), R.randint(4, 20)
        C = R.choice([30, 40, 50, 60, 70, 80, 100, 110, 120, 135])
        c = math.sqrt(a * a + b * b - 2 * a * b * math.cos(math.radians(C)))
        pic = tri_pic(a, b, C, ("a = %d" % a, "b = %d" % b, "c = ?"))
        return M(pic + "En el triángulo, a = %d cm, b = %d cm y C = %d°. Calcula c (redondea a las centésimas)." % (a, b, C), "%s cm" % r2(c), W(["%s cm" % r2(math.sqrt(a * a + b * b)), "%s cm" % r2(math.sqrt(abs(a * a + b * b + 2 * a * b * math.cos(math.radians(C))))), "%s cm" % r2(a + b - C / 10)]),
                 "c² = a² + b² − 2ab cos C = %d + %d − %d cos %d° → c ≈ <b>%s cm</b>." % (a * a, b * b, 2 * a * b, C, r2(c)))
    while True:
        a, b, c = R.randint(3, 15), R.randint(3, 15), R.randint(3, 15)
        if a + b > c and a + c > b and b + c > a:
            break
    Cc = math.degrees(math.acos((a * a + b * b - c * c) / (2 * a * b)))
    Ar = math.degrees(math.acos((b * b + c * c - a * a) / (2 * b * c)))
    return M("Los lados de un triángulo miden a = %d, b = %d y c = %d. ¿Cuánto mide el ángulo C? (a las décimas de grado)" % (a, b, c), ang(Cc), W([ang(Ar), ang(180 - Cc), ang(math.degrees(math.acos(max(-1, min(1, (a * a + b * b + c * c) / (2 * a * b * 2)))))) if False else ang(Cc + 10), ang(Cc / 2)]),
             "cos C = (a² + b² − c²)/(2ab) = %d/%d → C ≈ <b>%s</b>." % (a * a + b * b - c * c, 2 * a * b, ang(Cc)))


def s_area():
    t = R.choice(["dos", "dos", "heron", "tipo"])
    if t == "dos":
        a, b = R.randint(3, 20), R.randint(3, 20)
        C = R.choice([30, 45, 60, 90, 120, 150, 40, 70, 110])
        S = a * b * math.sin(math.radians(C)) / 2
        return M("Calcula el área de un triángulo con lados de %d m y %d m que forman un ángulo de %d° (a las centésimas)." % (a, b, C), "%s m²" % r2(S), W(["%s m²" % r2(a * b / 2), "%s m²" % r2(a * b * math.sin(math.radians(C))), "%s m²" % r2(abs(a * b * math.cos(math.radians(C))) / 2) if C != 90 else "%s m²" % r2(a * b), "%s m²" % r2(a * b * math.sin(math.radians(C)) / 4), "%s m²" % r2((a + b) * math.sin(math.radians(C)))]),
                 "S = ½ · a · b · sen C = ½ · %d · %d · sen %d° ≈ <b>%s m²</b>." % (a, b, C, r2(S)))
    if t == "heron":
        a, b, c = R.choice([(13, 14, 15), (5, 5, 6), (7, 8, 9), (6, 8, 10), (9, 10, 17), (10, 13, 13), (5, 12, 13), (4, 13, 15)])
        p = (a + b + c) / 2
        S = math.sqrt(p * (p - a) * (p - b) * (p - c))
        return M("Calcula el área de un triángulo de lados %d, %d y %d con la fórmula de Herón." % (a, b, c), r2(S) if S != int(S) else num(int(S)), W([num(int(p)) if p == int(p) else r2(p), r2(a * b / 2), r2(S * 2), r2(S / 2), num(a + b + c)]),
                 "s = %s; S = √(s(s − a)(s − b)(s − c)) = <b>%s</b>." % (r2(p, 1) if p != int(p) else num(int(p)), r2(S) if S != int(S) else num(int(S))))
    q, a, w = R.choice([("Si en un triángulo a² &gt; b² + c², ¿cómo es el ángulo A?", "obtuso", ["agudo", "recto", "no se puede saber"]), ("Si a² = b² + c², el triángulo es…", "rectángulo en A", ["acutángulo", "obtusángulo", "equilátero"]),
                        ("El teorema del coseno con C = 90° se convierte en…", "el teorema de Pitágoras", ["el teorema del seno", "la fórmula de Herón", "el teorema de Tales"]),
                        ("¿Cuándo se usa el teorema del seno?", "cuando conocemos un lado y su ángulo opuesto", ["solo en triángulos rectángulos", "cuando conocemos los tres lados", "solo con ángulos de 30°, 45° y 60°"]),
                        ("¿Cuándo se usa el teorema del coseno?", "con dos lados y el ángulo que forman, o con los tres lados", ["solo con los tres ángulos", "solo en triángulos rectángulos", "cuando hay dos ángulos iguales"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s_ambiguo():
    t = R.choice(["n", "n", "q"])
    if t == "q":
        q, a, w = R.choice([("En el caso ambiguo (dos lados y el ángulo opuesto a uno de ellos), ¿cuántos triángulos puede haber?", "0, 1 o 2", ["siempre 1", "siempre 2", "infinitos"]),
                            ("Si sen B = 1,2 al aplicar el teorema del seno, ¿qué ocurre?", "no existe el triángulo", ["B = 90°", "hay dos triángulos", "B = 1,2°"])])
        return M(q, a, w, "Respuesta: <b>%s</b>." % a)
    A = R.choice([25, 30, 35, 40, 45])
    a = R.randint(5, 12)
    b = R.randint(a + 1, 2 * a)
    sB = b * math.sin(math.radians(A)) / a
    if sB >= 0.999:
        n = 0
    else:
        B1 = math.degrees(math.asin(sB))
        n = 2 if 180 - B1 + A < 180 else 1
    ok = {0: "ninguno", 1: "uno", 2: "dos"}[n]
    return M("¿Cuántos triángulos hay con a = %d, b = %d y A = %d°?" % (a, b, A), ok, [x for x in ["ninguno", "uno", "dos", "infinitos"] if x != ok],
             "sen B = %d · sen %d° / %d ≈ %s. %s" % (b, A, a, r2(sB, 3), "Mayor que 1: <b>ninguno</b>." if n == 0 else "B puede ser %s o %s: <b>dos</b>." % (ang(B1), ang(180 - B1)) if n == 2 else "<b>Uno</b>."))


def s_problema():
    t = R.choice(["rio", "barcos", "torre", "terreno", "faros"])
    if t == "rio":
        d_, A, B = R.randint(50, 200), R.randint(40, 75), R.randint(40, 75)
        C = 180 - A - B
        x = d_ * math.sin(math.radians(B)) / math.sin(math.radians(C))
        return M("Para medir la distancia de A a un árbol C al otro lado del río, se toma una base AB de %d m. Los ángulos en A y en B miden %d° y %d°. ¿Cuál es la distancia AC?" % (d_, A, B), "%s m" % r2(x), W(["%s m" % r2(d_ * math.sin(math.radians(A)) / math.sin(math.radians(C))), "%s m" % r2(d_ * math.tan(math.radians(A))), "%s m" % r2(d_ * math.sin(math.radians(B)))]),
                 "C = %d°; AC / sen %d° = %d / sen %d° → AC ≈ <b>%s m</b>." % (C, B, d_, C, r2(x)))
    if t == "barcos":
        v1, v2, g = R.randint(10, 30), R.randint(10, 30), R.choice([40, 60, 75, 90, 110, 120])
        h = R.randint(1, 3)
        a, b = v1 * h, v2 * h
        c = math.sqrt(a * a + b * b - 2 * a * b * math.cos(math.radians(g)))
        return M("Dos barcos salen del mismo puerto con rumbos que forman %d°, a %d y %d km/h. ¿Qué distancia los separa al cabo de %s?" % (g, v1, v2, "1 hora" if h == 1 else "%d horas" % h), "%s km" % r2(c), W(["%s km" % r2(math.sqrt(a * a + b * b)) if g != 90 else "%s km" % r2(math.sqrt(a * a + b * b + a * b)), "%s km" % r2(abs(a - b) + g / 10), "%s km" % r2(a + b), "%s km" % r2(math.sqrt(a * a + b * b + 2 * a * b * math.cos(math.radians(g))))]),
                 "Lados %d y %d km con %d°: c² = %d + %d − %d cos %d° → <b>%s km</b>." % (a, b, g, a * a, b * b, 2 * a * b, g, r2(c)))
    if t == "torre":
        d_, A, B = R.randint(20, 80), R.randint(20, 35), R.randint(40, 60)
        h = d_ * math.tan(math.radians(A)) * math.tan(math.radians(B)) / (math.tan(math.radians(B)) - math.tan(math.radians(A)))
        return M("Desde un punto se ve lo alto de una torre con un ángulo de %d°; acercándose %d m, con %d°. ¿Cuánto mide la torre?" % (A, d_, B), "%s m" % r2(h), W(["%s m" % r2(d_ * math.tan(math.radians(B))), "%s m" % r2(d_ * math.tan(math.radians(A))), "%s m" % r2(h * 1.5)]),
                 "Con el teorema del seno en el triángulo oblicuo (o con dos tangentes): h ≈ <b>%s m</b>." % r2(h))
    if t == "terreno":
        a, b, C = R.randint(20, 80), R.randint(20, 80), R.choice([50, 65, 80, 100, 115, 130])
        S = a * b * math.sin(math.radians(C)) / 2
        return M("Un terreno triangular tiene dos lados de %d m y %d m que forman %d°. ¿Cuál es su área?" % (a, b, C), "%s m²" % r2(S), W(["%s m²" % r2(a * b / 2), "%s m²" % r2(a * b * math.sin(math.radians(C))), "%s m²" % r2(a * b * abs(math.cos(math.radians(C))) / 2)]), "S = ½ · %d · %d · sen %d° ≈ <b>%s m²</b>." % (a, b, C, r2(S)))
    a, b, c = R.randint(5, 20), R.randint(5, 20), R.randint(5, 20)
    if not (a + b > c and a + c > b and b + c > a):
        return None
    C = math.degrees(math.acos((a * a + b * b - c * c) / (2 * a * b)))
    return M("Desde un barco se ven dos faros a %d km y %d km. Los faros están a %d km entre sí. ¿Qué ángulo forman las visuales desde el barco?" % (a, b, c), ang(C), W([ang(180 - C), ang(C / 2), ang(math.degrees(math.atan2(c, a)))]), "cos C = (%d + %d − %d)/(2 · %d · %d) → <b>%s</b>." % (a * a, b * b, c * c, a, b, ang(C)))


seen = set()
sets = [("Teorema del seno", mix(R, seen, [(s_seno, 20)])), ("Teorema del coseno", mix(R, seen, [(s_coseno, 20)])), ("Área de un triángulo", mix(R, seen, [(s_area, 20)])),
        ("Casos y número de soluciones", mix(R, seen, [(s_ambiguo, 10), (s_seno, 10)])), ("Problemas de distancias", mix(R, seen, [(s_problema, 20)]))]
think = ["<b>Teorema del seno</b>: a / sen A = b / sen B = c / sen C. Se usa cuando conocemos un lado y su ángulo opuesto.",
         "<b>Teorema del coseno</b>: c² = a² + b² − 2ab cos C. Se usa con dos lados y el ángulo que forman, o con los tres lados.",
         "<b>Área</b>: S = ½ · a · b · sen C (dos lados y el ángulo que forman).",
         "Con dos lados y el ángulo opuesto a uno (caso ambiguo) puede haber 0, 1 o 2 triángulos."]
ex = [("a = 7, b = 5, C = 60°", ["c² = 49 + 25 − 70 · 0,5 = 39"], "c ≈ 6,24"), ("a = 10, A = 40°, B = 70°", ["b = 10 · sen 70° / sen 40°"], "b ≈ 14,62")]
mist = [["Emparejar mal lados y ángulos", "El lado a está enfrente del ángulo A."], ["Olvidar el segundo triángulo", "sen B = 0,8 da B ≈ 53,1° o B ≈ 126,9°."], ["Calculadora en radianes", "Ponla en modo DEG."]]
body = L(think, ex, mist, tri_pic(7, 9, 55, ("a", "b", "c")))
faq = [("¿Qué diferencia hay con la trigonometría de 4.º de ESO?", "Ahora los triángulos no tienen que ser rectángulos: los teoremas del seno y del coseno sirven para cualquier triángulo."),
       ("¿Para qué se usa en la vida real?", "Para medir distancias que no se pueden recorrer: la anchura de un río, la distancia entre barcos o la altura de una montaña.")]
unit(1, R, "resolucion-de-triangulos", "E", "Resolución de triángulos cualesquiera: teoremas del seno y del coseno, área, problemas de medida",
     "Resolución de triángulos", "Resolución de triángulos", "Fichas de Matemáticas I (1.º de Bachillerato): teorema del seno, teorema del coseno, área, caso ambiguo y problemas de distancias. 100 ejercicios con soluciones.",
     "a / sen A = b / sen B = c / sen C", "c² = a² + b² − 2ab cos C", body, faq, sets, 6)
