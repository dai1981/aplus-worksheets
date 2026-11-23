# -*- coding: utf-8 -*-
"""
España Matemáticas I (1.º de Bachillerato): Números complejos (Sentido numérico)
Forma binómica, opuesto y conjugado, operaciones, potencias de i, módulo y argumento, forma polar, producto y cociente en polar, ecuaciones de segundo grado con soluciones complejas.
Errores: i² = 1, olvidar multiplicar por el conjugado al dividir, argumento en el cuadrante equivocado.
"""
import math
import random
from fractions import Fraction as F
from es_bach import M, mix, sg, num, unit, L, P2, MINUS, nf, raiz, W

R = random.Random(51002)


def C(a, b):
    """a + bi"""
    a, b = F(a), F(b)
    if b == 0:
        return nf(a)
    bi = ("" if abs(b) == 1 else nf(abs(b))) + "i"
    if a == 0:
        return (MINUS if b < 0 else "") + bi
    return "%s %s %s" % (nf(a), "−" if b < 0 else "+", bi)


def pol(r, ang):
    return "%s<sub>%d°</sub>" % (r, ang)


def z():
    a, b = R.randint(-7, 7), R.randint(-7, 7)
    return (a, b) if b and a else None


def s_binomica():
    p = z()
    if not p:
        return None
    a, b = p
    t = R.choice(["re", "im", "conj", "op", "graf"])
    if t == "re":
        return M("¿Cuál es la parte real de z = %s?" % C(a, b), sg(a), [sg(b), C(0, b), sg(-a)], "z = a + bi: la parte real es a = <b>%s</b>." % sg(a))
    if t == "im":
        return M("¿Cuál es la parte imaginaria de z = %s?" % C(a, b), sg(b), [C(0, b), sg(a), sg(-b)], "La parte imaginaria es el número b (sin la i): <b>%s</b>." % sg(b))
    if t == "conj":
        return M("¿Cuál es el conjugado de z = %s?" % C(a, b), C(a, -b), [C(-a, b), C(-a, -b), C(b, a)], "El conjugado cambia el signo de la parte imaginaria: <b>%s</b>." % C(a, -b))
    if t == "op":
        return M("¿Cuál es el opuesto de z = %s?" % C(a, b), C(-a, -b), [C(a, -b), C(-a, b), C(b, a)], "El opuesto cambia el signo de las dos partes: <b>%s</b>." % C(-a, -b))
    q = (1 if a > 0 and b > 0 else 2 if a < 0 < b else 3 if a < 0 and b < 0 else 4)
    return M("¿En qué cuadrante se representa el afijo de z = %s?" % C(a, b), "en el %d.º" % q, ["en el %d.º" % k for k in range(1, 5) if k != q], "El afijo es el punto (%s, %s): <b>%d.º cuadrante</b>." % (sg(a), sg(b), q))


def s_operar():
    p, q = z(), z()
    if not p or not q:
        return None
    (a, b), (c, d_) = p, q
    t = R.choice(["suma", "resta", "prod", "prod", "div", "div"])
    if t == "suma":
        return M("Calcula (%s) + (%s)." % (C(a, b), C(c, d_)), C(a + c, b + d_), [C(a + c, b - d_), C(a * c, b * d_), C(a + d_, b + c)], "Sumamos partes reales y partes imaginarias: <b>%s</b>." % C(a + c, b + d_))
    if t == "resta":
        return M("Calcula (%s) − (%s)." % (C(a, b), C(c, d_)), C(a - c, b - d_), [C(a - c, b + d_), C(a + c, b + d_), C(c - a, d_ - b)], "Restamos parte a parte: <b>%s</b>." % C(a - c, b - d_))
    if t == "prod":
        re, im = a * c - b * d_, a * d_ + b * c
        return M("Calcula (%s) · (%s)." % (C(a, b), C(c, d_)), C(re, im), [C(a * c + b * d_, im), C(a * c, b * d_), C(re, a * d_ - b * c)], "(%s)(%s) = %s %s %si %s %si² y como i² = −1: <b>%s</b>." % (C(a, b), C(c, d_), sg(a * c), "+" if a * d_ + b * c >= 0 else "−", nf(abs(a * d_ + b * c)), "+" if b * d_ >= 0 else "−", nf(abs(b * d_)), C(re, im)))
    n2 = c * c + d_ * d_
    re, im = F(a * c + b * d_, n2), F(b * c - a * d_, n2)
    if re.denominator > 5 or im.denominator > 5:
        return None
    return M("Calcula (%s) / (%s)." % (C(a, b), C(c, d_)), C(re, im), [C(F(a, c), F(b, d_)), C(F(a * c - b * d_, n2), F(b * c + a * d_, n2)), C(-re, im) if re else C(re, -im)],
             "Multiplicamos arriba y abajo por el conjugado %s; abajo queda %d: <b>%s</b>." % (C(c, -d_), n2, C(re, im)))


def s_potencias():
    t = R.choice(["ipow", "ipow", "cuad", "inv"])
    if t == "ipow":
        n = R.randint(5, 150)
        v = ["1", "i", MINUS + "1", MINUS + "i"][n % 4]
        return M("Calcula i<sup>%d</sup>." % n, v, [x for x in ["1", "i", MINUS + "1", MINUS + "i"] if x != v], "%d : 4 da resto %d, así que i<sup>%d</sup> = i<sup>%d</sup> = <b>%s</b>." % (n, n % 4, n, n % 4, v))
    if t == "cuad":
        a, b = R.randint(1, 5), R.choice([1, 2, 3, -1, -2])
        return M("Calcula (%s)²." % C(a, b), C(a * a - b * b, 2 * a * b), [C(a * a + b * b, 2 * a * b), C(a * a, b * b), C(a * a - b * b, 0)], "(a + bi)² = a² − b² + 2abi: <b>%s</b>." % C(a * a - b * b, 2 * a * b))
    a, b = R.choice([(1, 1), (1, -1), (2, 1), (1, 2), (3, 4), (1, 3), (2, 2), (3, 1)])
    n2 = a * a + b * b
    return M("Calcula el inverso 1/(%s)." % C(a, b), C(F(a, n2), F(-b, n2)), [C(F(1, a), F(1, b)), C(F(a, n2), F(b, n2)), C(a, -b)], "1/z = z̄ / |z|² = (%s)/%d = <b>%s</b>." % (C(a, -b), n2, C(F(a, n2), F(-b, n2))))


ANG = {(1, 0): 0, (1, 1): 45, (0, 1): 90, (-1, 1): 135, (-1, 0): 180, (-1, -1): 225, (0, -1): 270, (1, -1): 315}


def s_polar():
    t = R.choice(["mod", "mod", "arg", "abin", "bina"])
    if t == "mod":
        a, b = R.choice([(3, 4), (6, 8), (5, 12), (1, 1), (1, 2), (2, 3), (8, 15), (1, 3), (2, 2), (4, 3)])
        a, b = a * R.choice([1, -1]), b * R.choice([1, -1])
        n = a * a + b * b
        return M("¿Cuál es el módulo de z = %s?" % C(a, b), raiz(n), [num(abs(a) + abs(b)), num(n), raiz(abs(a * a - b * b)) if a * a != b * b else "0"], "|z| = √(%s² + %s²) = √%d = <b>%s</b>." % ("(%s)" % sg(a) if a < 0 else sg(a), "(%s)" % sg(b) if b < 0 else sg(b), n, raiz(n)))
    if t == "arg":
        (u, v), ang = R.choice(list(ANG.items()))
        k = R.randint(1, 5)
        alt = sorted(set(ANG.values()) - {ang})
        R.shuffle(alt)
        return M("¿Cuál es el argumento de z = %s?" % C(k * u, k * v), "%d°" % ang, ["%d°" % x for x in alt[:3]], "Su afijo es (%s, %s): <b>%d°</b>." % (sg(k * u), sg(k * v), ang))
    if t == "abin":
        r = R.randint(2, 8)
        ang = R.choice([0, 90, 180, 270, 30, 60, 45, 150, 120])
        tab = {0: C(r, 0), 90: C(0, r), 180: C(-r, 0), 270: C(0, -r)}
        if ang in tab:
            ok = tab[ang]
            w = [tab[(ang + 90) % 360], tab[(ang + 180) % 360], tab[(ang + 270) % 360]]
        else:
            if r % 2:
                return None
            h = r // 2
            ok = {30: "%s√3 + %si" % (h if h > 1 else "", h if h > 1 else ""), 60: "%s + %s√3i" % (h, h if h > 1 else ""), 45: "%s√2 + %s√2i" % (h if h > 1 else "", h if h > 1 else ""),
                  150: "−%s√3 + %si" % (h if h > 1 else "", h if h > 1 else ""), 120: "−%s + %s√3i" % (h, h if h > 1 else "")}[ang]
            w = [ok.replace("+", "−", 1) if "+" in ok else ok + " ", ok.replace("√3", "", 1) if "√3" in ok else ok.replace("√2", "", 1), "%d + %di" % (r, r)]
        return M("Escribe en forma binómica z = %s." % pol(r, ang), ok, w, "z = %d(cos %d° + i sen %d°) = <b>%s</b>." % (r, ang, ang, ok))
    (u, v), ang = R.choice([((1, 1), 45), ((-1, 1), 135), ((-1, -1), 225), ((1, -1), 315), ((0, 1), 90), ((-1, 0), 180), ((0, -1), 270)])
    k = R.randint(1, 6)
    rr = raiz(2 * k * k) if u and v else str(k)
    return M("Escribe en forma polar z = %s." % C(k * u, k * v), pol(rr, ang), [pol(rr, (ang + 90) % 360), pol(rr, (360 - ang) % 360) if (360 - ang) % 360 != ang else pol(rr, (ang + 180) % 360), pol(str(2 * k) if u and v else raiz(2 * k * k), ang)],
             "Módulo %s y argumento %d°: <b>%s</b>." % (rr, ang, pol(rr, ang)))


def s_polar_ops():
    r1, r2_ = R.randint(2, 6), R.randint(2, 6)
    a1, a2 = R.choice([30, 45, 60, 90, 120, 150]), R.choice([30, 45, 60, 90, 120, 150, 200, 240])
    t = R.choice(["prod", "coc", "pot"])
    if t == "prod":
        return M("Calcula %s · %s." % (pol(r1, a1), pol(r2_, a2)), pol(r1 * r2_, (a1 + a2) % 360), [pol(r1 + r2_, (a1 + a2) % 360), pol(r1 * r2_, a1 * a2 % 360), pol(r1 * r2_, abs(a1 - a2))], "Se multiplican los módulos y se suman los argumentos: <b>%s</b>." % pol(r1 * r2_, (a1 + a2) % 360))
    if t == "coc":
        if (r1 * r2_) % r2_:
            return None
        m = r1 * r2_
        return M("Calcula %s : %s." % (pol(m, (a1 + a2) % 360), pol(r2_, a2)), pol(r1, a1), [pol(m - r2_, a1), pol(r1, (a1 + 2 * a2) % 360), pol(m * r2_, a1)], "Se dividen los módulos y se restan los argumentos: <b>%s</b>." % pol(r1, a1))
    n = R.randint(2, 5)
    r = R.randint(1, 3)
    a = R.choice([30, 45, 60, 90, 120])
    return M("Calcula (%s)<sup>%d</sup>." % (pol(r, a), n), pol(num(r ** n), a * n % 360), [pol(num(r * n), a * n % 360), pol(num(r ** n), a), pol(num(r ** n), (a + n) % 360)], "Fórmula de De Moivre: módulo %d<sup>%d</sup> y argumento %d · %d° = %d°: <b>%s</b>." % (r, n, n, a, a * n, pol(num(r ** n), a * n % 360)))


def s_ecuaciones():
    t = R.choice(["cuad", "cuad", "cuad", "sum", "raiz"])
    if t == "cuad":
        a, b = R.randint(-5, 5), R.randint(1, 6)
        f = P2(1, -2 * a, a * a + b * b)
        ok = "x = %s ± %si" % (sg(a), "" if b == 1 else b) if a else "x = ±%si" % ("" if b == 1 else b)
        return M("Resuelve %s = 0." % f, ok, [("x = %s ± %d" % (sg(a), b)) if a else "x = ±%d" % b, ("x = %s ± %si" % (sg(-a), "" if b == 1 else b)) if a else "x = ±%di" % (b * b), "no tiene solución"],
                 "Δ = %s &lt; 0 → √Δ = %di → <b>%s</b>." % (sg(4 * a * a - 4 * (a * a + b * b)), 2 * b, ok))
    if t == "sum":
        k = R.randint(2, 12)
        rt = raiz(k)
        return M("Resuelve x² + %d = 0." % k, "x = ±%si" % rt if not rt.isdigit() else "x = ±%si" % rt, ["x = ±%s" % rt, "x = %si" % rt, "no tiene solución"], "x² = −%d → x = ±√%d · i = <b>±%si</b>." % (k, k, rt))
    a, b = R.randint(-4, 4), R.randint(1, 5)
    if a == 0:
        return None
    return M("Si %s es una solución de una ecuación de segundo grado con coeficientes reales, ¿cuál es la otra?" % C(a, b), C(a, -b), [C(-a, b), C(-a, -b), C(b, a)], "Las soluciones complejas van en pareja con su conjugado: <b>%s</b>." % C(a, -b))


seen = set()
sets = [("Forma binómica", mix(R, seen, [(s_binomica, 20)])), ("Operaciones en forma binómica", mix(R, seen, [(s_operar, 20)])), ("Potencias de i e inverso", mix(R, seen, [(s_potencias, 20)])),
        ("Módulo, argumento y forma polar", mix(R, seen, [(s_polar, 12), (s_polar_ops, 8)])), ("Ecuaciones con soluciones complejas", mix(R, seen, [(s_ecuaciones, 12), (s_polar_ops, 8)]))]
think = ["La <b>unidad imaginaria</b> cumple i² = −1. Un número complejo en forma binómica es z = a + bi (a: parte real; b: parte imaginaria).",
         "Para <b>dividir</b> se multiplican numerador y denominador por el <b>conjugado</b> del denominador (a + bi → a − bi).",
         "Forma polar: z = r<sub>α</sub>, con módulo r = √(a² + b²) y argumento α (el ángulo del afijo). Al multiplicar, se multiplican los módulos y se suman los argumentos."]
ex = [("(2 + 3i)(1 − i)", ["2 − 2i + 3i − 3i²", "i² = −1"], "5 + i"), ("1 + i en forma polar", ["r = √2", "α = 45°"], "√2<sub>45°</sub>")]
mist = [["Usar i² = 1", "i² = −1: cambia el signo."], ["Dividir parte a parte", "Hay que multiplicar por el conjugado."], ["Argumento de −1 + i igual a −45°", "Mira el cuadrante: es 135°."]]
body = L(think, ex, mist)
faq = [("¿Para qué sirven los números complejos?", "Permiten resolver todas las ecuaciones polinómicas y se usan en electricidad (corriente alterna), señales y física."),
       ("¿Qué es la forma polar?", "Es escribir el número con su distancia al origen (módulo) y su ángulo (argumento); facilita multiplicar, dividir y elevar a potencias.")]
unit(1, R, "numeros-complejos", "N", "Números complejos: forma binómica y polar, representación, operaciones y aplicación a la resolución de ecuaciones",
     "Números complejos", "Números complejos", "Fichas de Matemáticas I (1.º de Bachillerato): forma binómica, conjugado, operaciones, potencias de i, módulo, argumento, forma polar y ecuaciones. 100 ejercicios con soluciones.",
     "i² = −1", "Para dividir, multiplica por el conjugado.", body, faq, sets, 2)
