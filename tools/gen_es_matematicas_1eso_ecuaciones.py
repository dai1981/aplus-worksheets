# -*- coding: utf-8 -*-
"""
España Matemáticas ESO: Ecuaciones (Sentido algebraico)
build(lv): lv = 1 → «ecuaciones-de-primer-grado»: comprobar, x + a = b, ax = b, incógnita en los dos miembros, paréntesis, problemas;
lv = 2 → «ecuaciones-de-primer-y-segundo-grado»: paréntesis, denominadores, 2.º grado incompletas y completas, problemas;
lv = 3 → «ecuaciones-de-segundo-grado»: incompletas, fórmula, discriminante, factorización y suma/producto, problemas.
Errores: pasar un término sin cambiarle el signo, dividir solo un término, olvidar la solución negativa de x² = 9, dividir entre x y perder x = 0.
"""
import math
import random
from fractions import Fraction as F
from es_eso import M, mix, E, P2, sg, fq, par, sol, unit, L, Kids, nz, num, fr

R = None
LV = 1
K = None


def lin(a, b):
    return E((a, "x"), (b, ""))


def s_comprobar():
    a, b = nz(R, -6, 6), nz(R, -12, 12)
    x = nz(R, -6, 6)
    c = a * x + b
    cand = [x, -x, x + 1, x - 1, c - b]
    cand = [v for i, v in enumerate(cand) if v not in cand[:i]]
    return M("¿Cuál es la solución de %s = %s: %s?" % (lin(a, b), sg(c), " o ".join(sg(v) for v in sorted(cand[:4]))), sg(x), [sg(v) for v in cand[:4] if v != x],
             "Sustituimos: %s · %s %s %d = %s. <b>x = %s</b>." % (sg(a), par(x), "+" if b > 0 else "−", abs(b), sg(c), sg(x)))


def s_basica():
    x = nz(R, -12, 15)
    t = R.choice(["+", "-", "ax", "x/a", "ax+b"])
    if t == "+":
        a = nz(R, -15, 15)
        return M("Resuelve: x %s %d = %s" % ("+" if a > 0 else "−", abs(a), sg(x + a)), "x = %s" % sg(x), ["x = %s" % sg(x + 2 * a), "x = %s" % sg(-x), "x = %s" % sg(x + 1)], "Pasamos %s al otro miembro cambiando el signo: <b>x = %s</b>." % (sg(a), sg(x)))
    if t == "-":
        a = R.randint(2, 15)
        return M("Resuelve: %d − x = %s" % (a, sg(a - x)), "x = %s" % sg(x), ["x = %s" % sg(-x), "x = %s" % sg(2 * a - x), "x = %s" % sg(x + 1)], "−x = %s, así que <b>x = %s</b>." % (sg(-x), sg(x)))
    if t == "ax":
        a = nz(R, -9, 9)
        if abs(a) == 1:
            return None
        return M("Resuelve: %sx = %s" % (sg(a), sg(a * x)), "x = %s" % sg(x), ["x = %s" % sg(a * x - a), "x = %s" % sg(-x), "x = %s" % sg(a * a * x)], "Dividimos entre %s: <b>x = %s</b>." % (sg(a), sg(x)))
    if t == "x/a":
        a = R.randint(2, 9)
        return M("Resuelve: x/%d = %s" % (a, sg(x)), "x = %s" % sg(a * x), ["x = %s" % fq(F(x, a)), "x = %s" % sg(x + a), "x = %s" % sg(-a * x)], "Multiplicamos por %d: <b>x = %s</b>." % (a, sg(a * x)))
    a, b = nz(R, -9, 9), nz(R, -15, 15)
    if abs(a) == 1:
        return None
    c = a * x + b
    return M("Resuelve: %s = %s" % (lin(a, b), sg(c)), "x = %s" % sg(x), ["x = %s" % fq(F(c + b, a)), "x = %s" % sg(c - b - a), "x = %s" % sg(-x)], "%sx = %s − %s = %s; x = <b>%s</b>." % (sg(a), sg(c), par(b), sg(c - b), sg(x)))


def s_dos_miembros():
    x = nz(R, -9, 9)
    a, c = nz(R, -9, 9), nz(R, -9, 9)
    if a == c:
        return None
    b = nz(R, -15, 15)
    e = a * x + b - c * x
    ok = "x = %s" % sg(x)
    wr = F(e - b, a + c) if a + c else None
    return M("Resuelve: %s = %s" % (lin(a, b), lin(c, e)), ok, ["x = %s" % fq(wr) if wr is not None and wr != x else "x = %s" % sg(x + 2), "x = %s" % sg(-x), "x = %s" % fq(F(e + b, a - c)) if F(e + b, a - c) != x else "x = %s" % sg(x - 1)],
             "Términos con x a un lado y números al otro: %sx = %s; <b>%s</b>." % (sg(a - c), sg(e - b), ok))


def s_parentesis():
    x = nz(R, -8, 8)
    k, a, b = nz(R, -5, 5), nz(R, -5, 5), nz(R, -9, 9)
    c = nz(R, -6, 6)
    if abs(k) == 1:
        return None
    lhs_val = k * (a * x + b)
    e = lhs_val - c * x
    if k * a == c:
        return None
    wrong = F(e - b, k * a - c) if k * a != c else None
    return M("Resuelve: %s(%s) = %s" % (sg(k), lin(a, b), lin(c, e)), "x = %s" % sg(x), ["x = %s" % fq(wrong) if wrong is not None and wrong != x else "x = %s" % sg(x + 1), "x = %s" % sg(-x), "x = %s" % sg(x + 2)],
             "Quitamos el paréntesis: %s = %s; resolvemos: <b>x = %s</b>." % (lin(k * a, k * b), lin(c, e), sg(x)))


def s_denominadores():
    x = nz(R, -10, 12)
    a, b = R.sample([2, 3, 4, 5, 6], 2)
    m = a * b // math.gcd(a, b)
    if (x % a) or (x % b):
        k = R.randint(1, 4)
        x = m * nz(R, -2, 2) if R.random() < 0.6 else x
        if x % a or x % b:
            return None
    c = x // a + x // b
    ok = "x = %s" % sg(x)
    return M("Resuelve: x/%d + x/%d = %s" % (a, b, sg(c)), ok, ["x = %s" % fq(F(c, 2)), "x = %s" % fq(F(c * (a + b), 1)) if c * (a + b) != x else "x = %s" % sg(x + m), "x = %s" % sg(-x)],
             "Multiplicamos todo por m.c.m.(%d, %d) = %d: %dx + %dx = %s; <b>%s</b>." % (a, b, m, m // a, m // b, sg(c * m), ok))


def s_den2():
    x = nz(R, -9, 9)
    a = R.choice([2, 3, 4, 5])
    b = nz(R, -5, 5)
    c = R.choice([2, 3, 4, 6])
    lhs = F(x + b, a)
    rhs_k = nz(R, -3, 3)
    if lhs.denominator != 1:
        return None
    e = lhs - F(x, c) if F(x, c).denominator == 1 else None
    if e is None:
        return None
    return M("Resuelve: (%s)/%d − x/%d = %s" % (lin(1, b), a, c, fq(e)), "x = %s" % sg(x), ["x = %s" % sg(-x), "x = %s" % sg(x + a), "x = %s" % fq(e * a - b) if e * a - b != x else "x = %s" % sg(x - 1)],
             "Multiplicamos por m.c.m.(%d, %d) y resolvemos: <b>x = %s</b>." % (a, c, sg(x)))


def s_incompleta():
    t = R.choice(["ax2=c", "ax2=c", "ax2+bx", "x2=neg"])
    if t == "ax2=c":
        r = R.randint(1, 12)
        a = R.choice([1, 1, 2, 3, 4, 5])
        c = a * r * r
        ok = sol([r, -r])
        return M("Resuelve: %s = %s" % (E((a, "x²")), num(c)), ok, ["x = %d" % r, sol([r * r, -r * r]) if a == 1 else sol([F(c, 2 * a), -F(c, 2 * a)]), sol([F(c, a), -F(c, a)]) if F(c, a) != r else sol([r + 1, -r - 1]), sol([r + 1, -r - 1]), "x = %d" % (-r)],
                 "x² = %s; x = ±√%s: <b>%s</b>." % (num(c // a), num(c // a), ok))
    if t == "ax2+bx":
        a = nz(R, -5, 5)
        r = nz(R, -9, 9)
        b = -a * r
        if abs(a) == 1 and R.random() < 0.3:
            pass
        ok = sol([0, r])
        return M("Resuelve: %s = 0" % E((a, "x²"), (b, "x")), ok, ["x = %s" % sg(r), sol([0, -r]), sol([r, -r]) if r else "x = 1"], "Sacamos factor común x: x(%s) = 0; <b>%s</b>." % (lin(a, b), ok))
    a = R.randint(1, 5)
    c = R.randint(1, 30)
    return M("Resuelve: %s + %d = 0" % (E((a, "x²")), c), "no tiene solución real", [sol([1, -1]) if c == a else "x = %s" % fq(F(-c, a)), "x = 0", "x = %s" % fq(F(c, a))],
             "x² = −%s, y ningún número al cuadrado es negativo: <b>no tiene solución real</b>." % fq(F(c, a)))


def s_completa():
    r1, r2 = nz(R, -9, 9), nz(R, -9, 9)
    a = R.choice([1, 1, 1, 2, -1, 3])
    b, c = -a * (r1 + r2), a * r1 * r2
    ok = sol([r1, r2])
    w = [sol([-r1, -r2]) if {-r1, -r2} != {r1, r2} else sol([r1, r2 + 1]), sol([r1, -r2]) if r2 and {r1, -r2} != {r1, r2} else sol([r1 + 1, r2]), "x = %s" % sg(r1)]
    return M("Resuelve: %s = 0" % P2(a, b, c), ok, w, "x = (−b ± √(b² − 4ac)) / 2a = (%s ± √%s) / %s: <b>%s</b>." % (sg(-b), num(b * b - 4 * a * c), sg(2 * a), ok))


def s_discr():
    a = R.choice([1, 1, 2, 3, -1])
    b = nz(R, -10, 10)
    c = R.randint(-12, 12)
    D = b * b - 4 * a * c
    n = 2 if D > 0 else 1 if D == 0 else 0
    ok = {2: "dos soluciones distintas", 1: "una solución doble", 0: "ninguna solución real"}[n]
    if R.random() < 0.35:
        r = nz(R, -6, 6)
        a, b, c = 1, -2 * r, r * r
        D, ok = 0, "una solución doble"
    return M("¿Cuántas soluciones tiene %s = 0?" % P2(a, b, c), ok, [x for x in ("dos soluciones distintas", "una solución doble", "ninguna solución real", "infinitas soluciones") if x != ok],
             "Δ = b² − 4ac = %s: %s. <b>%s</b>." % (sg(D), "positivo" if D > 0 else "cero" if D == 0 else "negativo", ok))


def s_factor():
    r1, r2 = nz(R, -9, 9), nz(R, -9, 9)
    t = R.choice(["fact", "sp", "build"])
    if t == "fact":
        ok = "(x %s %d)(x %s %d)" % ("−" if r1 > 0 else "+", abs(r1), "−" if r2 > 0 else "+", abs(r2))
        w = "(x %s %d)(x %s %d)" % ("+" if r1 > 0 else "−", abs(r1), "+" if r2 > 0 else "−", abs(r2))
        return M("Factoriza: %s" % P2(1, -(r1 + r2), r1 * r2), ok, [w, "x(x %s %d)" % ("−" if r1 + r2 > 0 else "+", abs(r1 + r2)) if r1 + r2 else "x² − %d" % (r1 * r1), "(x %s %d)²" % ("−" if r1 > 0 else "+", abs(r1)) if r1 != r2 else "(x − 1)(x + %d)" % abs(r1)],
                 "Las soluciones son %s y %s, así que x² + bx + c = (x − x₁)(x − x₂): <b>%s</b>." % (sg(r1), sg(r2), ok))
    if t == "sp":
        s, p = r1 + r2, r1 * r2
        return M("Las soluciones de %s = 0 suman S y multiplican P. ¿Cuánto valen S y P?" % P2(1, -s, p), "S = %s, P = %s" % (sg(s), sg(p)), ["S = %s, P = %s" % (sg(-s), sg(p)), "S = %s, P = %s" % (sg(p), sg(s)), "S = %s, P = %s" % (sg(-s), sg(-p))],
                 "En x² + bx + c = 0, S = −b y P = c: <b>S = %s, P = %s</b>." % (sg(s), sg(p)))
    ok = "%s = 0" % P2(1, -(r1 + r2), r1 * r2)
    return M("¿Qué ecuación tiene como soluciones %s y %s?" % (sg(r1), sg(r2)), ok, ["%s = 0" % P2(1, r1 + r2, r1 * r2), "%s = 0" % P2(1, -(r1 + r2), -r1 * r2), "%s = 0" % P2(1, r1 * r2, r1 + r2)],
             "x² − Sx + P = 0 con S = %s y P = %s: <b>%s</b>." % (sg(r1 + r2), sg(r1 * r2), ok))


def s_problema():
    p, q = K.two()
    t = R.choice(["edad", "consec", "triple", "dinero", "rect", "cuad", "numero2"] if LV >= 2 else ["edad", "consec", "triple", "dinero", "rect"])
    if t == "edad":
        x, a = R.randint(8, 16), R.randint(20, 35)
        k = R.randint(2, 4)
        n = (a + x * 0)
        if (a - k * x) % (k - 1):
            return None
        yrs = (a - k * x) // (k - 1)
        if yrs <= 0 or yrs > 20:
            return None
        return M("%s tiene %d años y su madre %d. ¿Dentro de cuántos años la edad de la madre será %s de la de %s?" % (p[0], x, a, {2: "el doble", 3: "el triple", 4: "el cuádruple"}[k], p[0]),
                 "%d años" % yrs, ["%d años" % (yrs + 1), "%d años" % (a - x), "%d años" % (a // k)], "%d + t = %d(%d + t); t = <b>%d años</b>." % (a, k, x, yrs))
    if t == "consec":
        x = R.randint(5, 60)
        n = R.choice([2, 3])
        s = n * x + (1 if n == 2 else 3)
        ok = ", ".join(str(x + i) for i in range(n))
        return M("La suma de %d números consecutivos es %d. ¿Qué números son?" % (n, s), ok, [", ".join(str(x + i + 1) for i in range(n)), ", ".join(str(x - 1 + i) for i in range(n)), ", ".join(str(x + 2 * i) for i in range(n))],
                 "%s = %d; <b>%s</b>." % (" + ".join(["x"] + ["(x + %d)" % i for i in range(1, n)]), s, ok))
    if t == "triple":
        x = R.randint(3, 20)
        a = R.randint(2, 15)
        return M("Si al triple de un número le restamos %d, obtenemos %d. ¿Qué número es?" % (a, 3 * x - a), str(x), [str(3 * x - a), str(x + 1), str((3 * x - a + a) // 3 + a)], "3x − %d = %d; 3x = %d; <b>x = %d</b>." % (a, 3 * x - a, 3 * x, x))
    if t == "dinero":
        x = R.randint(5, 40)
        k = R.randint(2, 4)
        tot = x + k * x
        return M("%s y %s tienen entre los dos %d €. %s tiene %s que %s. ¿Cuánto tiene %s?" % (p[0], q[0], tot, q[0], {2: "el doble", 3: "el triple", 4: "el cuádruple"}[k], p[0], p[0]), "%d €" % x,
                 ["%d €" % (k * x), "%d €" % (tot // 2) if tot % 2 == 0 and tot // 2 != x else "%d €" % (x + 1), "%d €" % (tot - k)], "x + %dx = %d; %dx = %d; <b>x = %d €</b>." % (k, tot, k + 1, tot, x))
    if t == "rect":
        w = R.randint(3, 20)
        a = R.randint(2, 10)
        per = 2 * w + 2 * (w + a)
        return M("El largo de un rectángulo mide %d cm más que el ancho y su perímetro es %d cm. ¿Cuánto mide el ancho?" % (a, per), "%d cm" % w, ["%d cm" % (w + a), "%d cm" % (per // 4), "%d cm" % (per // 2 - a)] if per % 4 else ["%d cm" % (w + a), "%d cm" % (per // 2 - a), "%d cm" % (w + 1)],
                 "2x + 2(x + %d) = %d; 4x = %d; <b>x = %d cm</b>." % (a, per, per - 2 * a, w))
    if t == "cuad":
        x = R.randint(3, 15)
        a = R.randint(1, 6)
        A = x * (x + a)
        return M("Un rectángulo tiene %d cm más de largo que de ancho y su área es %d cm². ¿Cuánto mide el ancho?" % (a, A), "%d cm" % x, ["%d cm" % (x + a), "%d cm" % (A // 2), "−%d cm" % (x + a)], "x(x + %d) = %d → x² + %dx − %d = 0; la solución positiva es <b>%d cm</b>." % (a, A, a, A, x))
    x = R.randint(3, 15)
    a = x * x + x
    return M("Un número positivo más su cuadrado da %d. ¿Qué número es?" % a, str(x), [str(x + 1), str(-x - 1), str(a // 2)], "x² + x − %d = 0; soluciones %d y −%d; positivo: <b>%d</b>." % (a, x, x + 1, x))


def build(lv):
    global R, LV, K
    LV = lv
    R = random.Random(47008 + (lv - 1) * 1000)
    K = Kids(R)
    seen = set()
    if lv == 1:
        sets = [("Comprobar soluciones", mix(R, seen, [(s_comprobar, 20)])), ("Ecuaciones sencillas", mix(R, seen, [(s_basica, 20)])), ("x en los dos miembros", mix(R, seen, [(s_dos_miembros, 20)])),
                ("Ecuaciones con paréntesis", mix(R, seen, [(s_parentesis, 20)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
        think = ["Una <b>ecuación</b> es una igualdad con una incógnita. Resolverla es encontrar el valor que la cumple.",
                 "Lo que suma en un miembro pasa restando al otro, y al revés. Lo que multiplica pasa dividiendo.",
                 "Pasos: quitar paréntesis, agrupar las x en un miembro y los números en el otro, y despejar."]
        ex = [("5x − 3 = 2x + 9", ["5x − 2x = 9 + 3", "3x = 12"], "x = 4"), ("2(x − 4) = x + 1", ["2x − 8 = x + 1", "x = 9"], "x = 9")]
        mist = [["Pasar un término sin cambiar su signo", "+3 pasa como −3."], ["Dividir solo una parte", "3x = 12 → x = 12 : 3."], ["Olvidar multiplicar todo el paréntesis", "2(x − 4) = 2x − 8."]]
        slug, title, short = "ecuaciones-de-primer-grado", "Ecuaciones de primer grado", "Ecuaciones"
        kb, ks = "Lo que suma pasa restando", "Lo que multiplica pasa dividiendo."
        meta = "Fichas de matemáticas de 1.º de ESO: comprobar soluciones, ecuaciones de primer grado sencillas, con paréntesis y problemas. 100 ejercicios con soluciones."
        std = "Ecuaciones lineales: resolución mediante transposición de términos; ecuaciones con paréntesis; planteamiento y resolución de problemas"
        sort = 8
    elif lv == 2:
        sets = [("Primer grado con paréntesis", mix(R, seen, [(s_parentesis, 10), (s_dos_miembros, 10)])), ("Primer grado con denominadores", mix(R, seen, [(s_denominadores, 12), (s_den2, 8)])),
                ("Segundo grado incompletas", mix(R, seen, [(s_incompleta, 20)])), ("Segundo grado completas", mix(R, seen, [(s_completa, 20)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
        think = ["Primer grado: quitar paréntesis, quitar denominadores multiplicando por el m.c.m., agrupar y despejar.",
                 "Segundo grado incompleta: si falta b, despeja x² (x = ±√…); si falta c, saca factor común x.",
                 "Segundo grado completa ax² + bx + c = 0: x = (−b ± √(b² − 4ac)) / 2a."]
        ex = [("x/2 + x/3 = 10", ["Por 6: 3x + 2x = 60", "5x = 60"], "x = 12"), ("x² − 5x + 6 = 0", ["x = (5 ± √(25 − 24)) / 2", "x = (5 ± 1) / 2"], "x₁ = 2, x₂ = 3")]
        mist = [["Olvidar la solución negativa", "x² = 9 → x = 3 y x = −3."], ["Dividir entre x", "En x² = 5x se pierde x = 0: saca factor común."], ["Equivocarse con el signo de −b", "Si b = −5, −b = 5."]]
        slug, title, short = "ecuaciones-de-primer-y-segundo-grado", "Ecuaciones de primer y segundo grado", "Ecuaciones"
        kb, ks = "x = (−b ± √(b² − 4ac)) / 2a", "Para ax² + bx + c = 0."
        meta = "Fichas de matemáticas de 2.º de ESO: ecuaciones de primer grado con paréntesis y denominadores, ecuaciones de segundo grado y problemas. 100 ejercicios con soluciones."
        std = "Ecuaciones de primer grado con paréntesis y denominadores; ecuaciones de segundo grado completas e incompletas; resolución de problemas"
        sort = 6
    else:
        sets = [("Incompletas", mix(R, seen, [(s_incompleta, 20)])), ("Fórmula general", mix(R, seen, [(s_completa, 20)])), ("Número de soluciones", mix(R, seen, [(s_discr, 20)])),
                ("Factorizar, suma y producto", mix(R, seen, [(s_factor, 20)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
        think = ["Una ecuación de segundo grado es ax² + bx + c = 0 con a ≠ 0. Se resuelve con x = (−b ± √Δ) / 2a, donde Δ = b² − 4ac.",
                 "El <b>discriminante</b> Δ dice cuántas soluciones hay: Δ &gt; 0, dos; Δ = 0, una doble; Δ &lt; 0, ninguna real.",
                 "Si las soluciones son x₁ y x₂: x² − Sx + P = 0, con S = x₁ + x₂ y P = x₁ · x₂. Y ax² + bx + c = a(x − x₁)(x − x₂)."]
        ex = [("2x² − 8 = 0", ["x² = 4"], "x₁ = −2, x₂ = 2"), ("x² + 2x − 15 = 0", ["Δ = 4 + 60 = 64", "x = (−2 ± 8) / 2"], "x₁ = −5, x₂ = 3")]
        mist = [["Olvidar la solución negativa", "x² = 16 → x = ±4."], ["Calcular mal Δ con b negativo", "(−6)² = 36, no −36."], ["Aceptar soluciones sin sentido en el problema", "Una longitud no puede ser negativa."]]
        slug, title, short = "ecuaciones-de-segundo-grado", "Ecuaciones de segundo grado", "Segundo grado"
        kb, ks = "Δ = b² − 4ac: cuántas soluciones", "Δ > 0 dos, Δ = 0 una, Δ < 0 ninguna."
        meta = "Fichas de matemáticas de 3.º de ESO: ecuaciones de segundo grado incompletas y completas, discriminante, factorización y problemas. 100 ejercicios con soluciones."
        std = "Ecuaciones de segundo grado: resolución algebraica, discriminante, relación entre coeficientes y soluciones; resolución de problemas"
        sort = 5
    body = L(think, ex, mist)
    faq = [("¿Cómo se comprueba la solución de una ecuación?", "Se sustituye el valor en la ecuación: si los dos miembros dan lo mismo, es solución."),
           ("¿Qué hago si en una ecuación hay denominadores?", "Multiplica los dos miembros por el m.c.m. de los denominadores para quitarlos.")]
    unit(lv, R, slug, "A", std, title, short, meta, kb, ks, body, faq, sets, sort)


if __name__ == "__main__":
    build(1)
