# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de ESO: Ecuaciones y sistemas (Sentido algebraico)
Ecuaciones bicuadradas, racionales (con x en el denominador), irracionales (con radicales, comprobando soluciones), exponenciales sencillas,
sistemas no lineales y problemas.
Errores: olvidar las soluciones negativas en las bicuadradas (x = ±√t), no comprobar en las irracionales, aceptar una solución que anula un denominador.
"""
import random
from fractions import Fraction as F
from es_eso import M, mix, sg, fq, num, unit, L, E, P2, sol, MINUS, sup

R = random.Random(50004)


def xa(a):
    return "x" if a == 0 else ("x + %d" % a if a > 0 else "x − %d" % -a)


def pares(ps):
    ps = sorted(set(ps))
    return " y ".join("(%s, %s)" % (sg(x), sg(y)) for x, y in ps)


def s_bicuadrada():
    t = R.choice(["cuatro", "cuatro", "dos", "ninguna", "cero"])
    if t == "cuatro":
        a, b = sorted(R.sample(range(1, 7), 2))
        B, C = -(a * a + b * b), a * a * b * b
        eq = "x⁴ %s x² + %s = 0" % (MINUS, num(-B)) if True else ""
        eq = "x⁴ − %dx² + %s = 0" % (-B, num(C))
        ok = sol([-a, a, -b, b])
        return M("Resuelve %s." % eq, ok, [sol([a, b]), sol([a * a, b * b]), sol([-a * a, a * a, -b * b, b * b])], "t = x²: t² − %dt + %s = 0 → t = %d o t = %d → x = ±%d, x = ±%d. <b>%s</b>." % (-B, num(C), a * a, b * b, a, b, ok))
    if t == "dos":
        a, b = R.sample(range(1, 7), 2)
        B, C = b * b - a * a, -a * a * b * b
        eq = "x⁴ %s %s = 0" % (("+ %dx²" % B) if B > 0 else ("− %dx²" % -B) if B < 0 else "", "− %s" % num(-C))
        eq = eq.replace("  ", " ")
        ok = sol([-a, a])
        return M("Resuelve %s." % eq, ok, [sol([-a, a, -b, b]), sol([a * a]), sol([-b, b]) if a != b else sol([a * a, -a * a])], "t = x²: t = %d o t = %s (no vale, x² no puede ser negativo) → <b>%s</b>." % (a * a, sg(-b * b), ok))
    if t == "ninguna":
        a, b = sorted(R.sample(range(1, 6), 2))
        eq = "x⁴ + %dx² + %s = 0" % (a * a + b * b, num(a * a * b * b))
        return M("¿Cuántas soluciones reales tiene %s?" % eq, "ninguna", ["4", "2", "1"], "t = %s o t = %s: x² no puede ser negativo. <b>Ninguna</b>." % (sg(-a * a), sg(-b * b)))
    a = R.randint(2, 7)
    eq = "x⁴ − %dx² = 0" % (a * a)
    ok = sol([-a, 0, a])
    return M("Resuelve %s." % eq, ok, [sol([-a, a]), sol([0, a]), sol([0, a * a])], "x²(x² − %d) = 0 → x = 0 o x = ±%d. <b>%s</b>." % (a * a, a, ok))


def s_racional():
    t = R.choice(["suma", "suma", "prop", "anula"])
    if t == "suma":
        r1, r2 = R.sample([v for v in range(-6, 8) if v], 2)
        s, p = r1 + r2, r1 * r2
        if s == 0:
            return None
        eq = "x + %s/x = %s" % (("%d" % p) if p > 0 else "(%s)" % sg(p), sg(s))
        eq = "x %s %d/x = %s" % ("+" if p > 0 else "−", abs(p), sg(s))
        ok = sol([r1, r2])
        return M("Resuelve %s." % eq, ok, [sol([-r1, -r2]), sol([s]), sol([r1, p]) if p != r2 else sol([r1 + 1, r2])], "Multiplicamos por x: %s = 0 → <b>%s</b>." % (P2(1, -s, p), ok))
    if t == "prop":
        a, b = R.randint(1, 6), R.randint(1, 6)
        p, q = R.randint(-6, 6), R.randint(-6, 6)
        if a == b or p == q:
            return None
        x = F(a * q - b * p, a - b)
        if x.denominator > 1 or x in (p, q):
            return None
        eq = "%d / (%s) = %d / (%s)" % (a, xa(-p), b, xa(-q))
        return M("Resuelve %s." % eq, "x = %s" % sg(int(x)), ["x = %s" % sg(int(-x)) if x else "x = 1", "x = %s" % sg(p + q), "x = %s" % fq(F(a * p - b * q, a - b)) if F(a * p - b * q, a - b) != x else "x = %s" % sg(p), "x = %s" % sg(q), "x = %s" % sg(int(x) + 1)],
                 "En cruz: %d(%s) = %d(%s) → <b>x = %s</b>." % (a, xa(-q), b, xa(-p), sg(int(x))))
    a = R.randint(1, 7)
    c = R.randint(1, 5)
    eq = "x / (x − %d) = %d / (x − %d) + %d" % (a, a, a, c) if c == 1 else None
    eq = "(x + %d) / (x − %d) = %d / (x − %d)" % (c, a, a + c, a)
    return M("Resuelve %s." % eq, "no tiene solución", ["x = %d" % a, "x = %d" % (a + c), "x = %s" % sg(-c)], "x + %d = %d → x = %d, que anula el denominador: <b>no tiene solución</b>." % (c, a + c, a))


def s_irracional():
    t = R.choice(["simple", "simple", "dos", "una"])
    if t == "simple":
        a, r = R.randint(-9, 9), R.randint(2, 9)
        eq = "√(%s) = %d" % (xa(a), r)
        x = r * r - a
        return M("Resuelve %s." % eq, "x = %s" % sg(x), ["x = %s" % sg(r - a), "x = %s" % sg(r * r + a) if a else "x = %d" % (2 * r), "x = %s" % sg(r * r)] if a else ["x = %d" % r, "x = %d" % (2 * r), "x = %d" % (r * r + 1)],
                 "Elevamos al cuadrado: %s = %d → <b>x = %s</b>." % (xa(a), r * r, sg(x)))
    b = R.randint(0, 5)
    r = R.randint(b + 1, b + 7)
    a = (r - b) ** 2 - r
    r2 = 2 * b + 1 - r
    good2 = r2 - b >= 0 and r2 + a >= 0
    if (t == "dos") != good2 or r2 == r:
        return None
    eq = "√(%s) = %s" % (xa(a), xa(-b))
    ok = sol([r, r2]) if good2 else "x = %s" % sg(r)
    w = ["x = %s" % sg(r2), sol([r, r2]) if not good2 else "x = %s" % sg(r), sol([-r, -r2]) if -r != r2 else "x = %s" % sg(-r), "x = %s" % sg(r + 1)]
    return M("Resuelve %s." % eq, ok, w, "Al cuadrado: %s = %s → %s = 0 → x = %s o x = %s. Comprobando, %s. <b>%s</b>." % (xa(a), "(%s)²" % xa(-b) if b else "x²", P2(1, -(2 * b + 1), b * b - a), sg(r), sg(r2), "valen las dos" if good2 else "x = %s no vale" % sg(r2), ok))


def s_exponencial():
    b = R.choice([2, 3, 5])
    t = R.choice(["directa", "suma", "cuad", "fraccion"])
    if t == "directa":
        n = R.randint(2, 6 if b == 2 else 4)
        return M("Resuelve %d<sup>x</sup> = %s." % (b, num(b ** n)), "x = %d" % n, ["x = %d" % (b ** n // b), "x = %d" % (n + 1), "x = %d" % (b ** n // n) if b ** n % n == 0 and b ** n // n != n else "x = %d" % (n - 1)], "%s = %d<sup>%d</sup> → <b>x = %d</b>." % (num(b ** n), b, n, n))
    if t == "suma":
        k, n = R.randint(-4, 4), R.randint(1, 5 if b == 2 else 3)
        if k == 0:
            return None
        return M("Resuelve %d<sup>%s</sup> = %s." % (b, xa(k), num(b ** n)), "x = %s" % sg(n - k), ["x = %s" % sg(n + k), "x = %s" % sg(n), "x = %s" % sg(b ** n - k)], "%s = %d<sup>%d</sup> → %s = %d → <b>x = %s</b>." % (num(b ** n), b, n, xa(k), n, sg(n - k)))
    if t == "cuad":
        r = R.randint(1, 3)
        return M("Resuelve %d<sup>x² − %d</sup> = 1." % (b, r * r), sol([-r, r]), ["x = %d" % r, "x = %d" % (r * r), "no tiene solución"], "1 = %d⁰ → x² − %d = 0 → <b>%s</b>." % (b, r * r, sol([-r, r])))
    n = R.randint(1, 4 if b == 2 else 3)
    return M("Resuelve %d<sup>x</sup> = 1/%s." % (b, num(b ** n)), "x = %s" % sg(-n), ["x = %d" % n, "x = %s" % fq(F(1, n)), "no tiene solución"], "1/%s = %d<sup>−%d</sup> → <b>x = %s</b>." % (num(b ** n), b, n, sg(-n)))


def s_sistema():
    t = R.choice(["sp", "sp", "cuad", "dif", "rect"])
    if t in ("sp", "rect"):
        x, y = R.sample(range(1, 13), 2)
        s, p = x + y, x * y
        if t == "rect":
            return M("Un rectángulo tiene %d cm de perímetro y %d cm² de área. ¿Cuánto miden sus lados?" % (2 * s, p), "%d cm y %d cm" % (min(x, y), max(x, y)), ["%d cm y %d cm" % (min(x, y) + 1, max(x, y) - 1) if min(x, y) + 1 != max(x, y) else "%d cm y %d cm" % (min(x, y) - 1, max(x, y) + 1), "%d cm y %d cm" % (1, p), "%d cm y %d cm" % (s, 2 * s)],
                     "x + y = %d, x · y = %d → t² − %dt + %d = 0 → <b>%d cm y %d cm</b>." % (s, p, s, p, min(x, y), max(x, y)))
        ok = pares([(x, y), (y, x)])
        return M("Resuelve el sistema: <span class='sys'>x + y = %d<br>x · y = %d</span>" % (s, p), ok, [pares([(x, y)]), pares([(-x, -y), (-y, -x)]), pares([(x + 1, y - 1), (y - 1, x + 1)]) if x + 1 != y else pares([(x - 1, y + 1), (y + 1, x - 1)])],
                 "y = %d − x → x(%d − x) = %d → x² − %dx + %d = 0 → x = %d o x = %d. <b>%s</b>." % (s, s, p, s, p, x, y, ok))
    if t == "cuad":
        x, y = R.sample(range(1, 9), 2)
        k = x - y
        c = x * x + y * y
        # x − y = k; x² + y² = c
        y2 = -x
        x2 = -y
        ok = pares([(x, y), (x2, y2)]) if (x, y) != (x2, y2) else pares([(x, y)])
        return M("Resuelve el sistema: <span class='sys'>x² + y² = %d<br>x − y = %s</span>" % (c, sg(k)), ok, [pares([(x, y)]), pares([(y, x), (-x, -y)]), pares([(-x, y), (x, -y)])],
                 "x = y %s → sustituimos y resolvemos la ecuación de segundo grado. <b>%s</b>." % (("+ %d" % k) if k > 0 else ("− %d" % -k) if k else "", ok))
    x, y = R.randint(1, 9), R.randint(1, 9)
    a = x * x - y
    # y = x² − a ; y = mx + n through (x,y) and another point
    m = R.choice([1, 2, 3, -1, -2])
    n = y - m * x
    # x² − a = m x + n → x² − m x − (a + n) = 0, roots x and m − x
    x2 = m - x
    y2 = m * x2 + n
    ok = pares([(x, y), (x2, y2)]) if x2 != x else pares([(x, y)])
    return M("Resuelve el sistema: <span class='sys'>y = %s<br>y = %s</span>" % (P2(1, 0, -a), E((m, "x"), (n, ""))), ok, [pares([(x, y)]), pares([(x2, y2)]) if x2 != x else pares([(-x, y)]), pares([(-x, -y), (-x2, -y2)])],
             "Igualamos: %s = %s → x = %s o x = %s. <b>%s</b>." % (P2(1, 0, -a), E((m, "x"), (n, "")), sg(x), sg(x2), ok))


def s_problema():
    t = R.choice(["edad", "num", "cuadrado", "grifos", "compra"])
    if t == "num":
        a = R.randint(2, 12)
        return M("La suma de un número positivo y su inverso es %s. ¿Cuál es el número? (también vale su inverso)" % fq(F(a * a + 1, a)), "%d o 1/%d" % (a, a), ["%d" % (a * a + 1), "%d o %d" % (a, a + 1), "1/%d" % (a * a)], "x + 1/x = %s → %dx² − %dx + %d = 0 → <b>x = %d o x = 1/%d</b>." % (fq(F(a * a + 1, a)), a, a * a + 1, a, a, a))
    if t == "cuadrado":
        n = R.randint(3, 15)
        return M("Si al cuadrado de un número positivo le restamos %d veces el número, obtenemos %d. ¿Cuál es el número?" % (n - 1, n), "%d" % n, ["%d" % (n - 1), "%d" % (n + 1), "%d" % (n * n)], "x² − %dx − %d = 0 → x = %d o x = −1 (no vale). <b>%d</b>." % (n - 1, n, n, n))
    if t == "edad":
        h, k = R.randint(4, 15), R.randint(20, 35)
        p = h + k
        prod = h * p
        return M("Un padre tiene %d años más que su hijo y el producto de sus edades es %d. ¿Cuántos años tiene el hijo?" % (k, prod), "%d" % h, ["%d" % p, "%d" % (h + 1), "%d" % (prod // k) if prod % k == 0 and prod // k != h else "%d" % (h - 1)], "x(x + %d) = %d → x² + %dx − %d = 0 → <b>x = %d</b>." % (k, prod, k, prod, h))
    if t == "grifos":
        a, b = R.choice([(3, 6), (4, 12), (6, 12), (2, 6), (10, 15), (12, 24), (6, 3)])
        tt = F(a * b, a + b)
        if tt.denominator > 1:
            return None
        return M("Un grifo llena un depósito en %d horas y otro en %d horas. ¿Cuánto tardan los dos juntos?" % (a, b), "%d h" % tt, ["%d h" % ((a + b) // 2) if (a + b) % 2 == 0 else "%d h" % (a + b), "%d h" % (a + b), "%d h" % abs(a - b) if abs(a - b) != tt else "%d h" % (tt + 1), "%d h" % (a * b)],
                 "1/%d + 1/%d = 1/t → t = <b>%d h</b>." % (a, b, tt))
    n = R.randint(4, 10)
    pu = R.choice([2, 3, 4, 5, 6])
    total = n * pu
    m = n + 2
    # total / n − total / (n + 2) = d → pu − total/(n+2)
    p2 = F(total, m)
    if p2.denominator > 1:
        return None
    dd = pu - p2
    return M("Con %d € se compran unos cuadernos. Si cada uno costase %s € menos, se podrían comprar 2 más. ¿Cuántos cuadernos se compran?" % (total, fq(dd)), "%d" % n, ["%d" % m, "%d" % (n - 2), "%d" % pu], "%d/x − %d/(x + 2) = %s → <b>x = %d</b>." % (total, total, fq(dd), n))


seen = set()
sets = [("Ecuaciones bicuadradas", mix(R, seen, [(s_bicuadrada, 20)])), ("Ecuaciones racionales", mix(R, seen, [(s_racional, 20)])), ("Ecuaciones irracionales y exponenciales", mix(R, seen, [(s_irracional, 12), (s_exponencial, 8)])),
        ("Sistemas no lineales", mix(R, seen, [(s_sistema, 20)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
think = ["<b>Bicuadrada</b> (ax⁴ + bx² + c = 0): cambio t = x², resolvemos la de segundo grado y luego x = ±√t (solo si t ≥ 0).",
         "<b>Racional</b>: multiplicamos por el denominador común y comprobamos que ninguna solución lo anula.",
         "<b>Irracional</b>: aislamos la raíz, elevamos al cuadrado y <b>comprobamos</b> cada solución en la ecuación original.",
         "<b>Exponencial</b>: escribimos los dos lados como potencias de la misma base e igualamos exponentes.",
         "<b>Sistemas no lineales</b>: despejamos una incógnita en la ecuación más sencilla y sustituimos."]
ex = [("x⁴ − 13x² + 36 = 0", ["t² − 13t + 36 = 0", "t = 4, t = 9"], "x = ±2, x = ±3"), ("√(x + 1) = x − 5", ["x + 1 = x² − 10x + 25", "x = 8 o x = 3; x = 3 no vale"], "x = 8")]
mist = [["Olvidar las soluciones negativas", "x² = 9 → x = ±3."], ["No comprobar en las irracionales", "Al elevar al cuadrado pueden aparecer soluciones falsas."], ["Aceptar un valor que anula el denominador", "Esa x no está en el dominio."]]
body = L(think, ex, mist)
faq = [("¿Por qué hay que comprobar las soluciones de una ecuación irracional?", "Porque al elevar al cuadrado se pueden añadir soluciones que no cumplen la ecuación original (la raíz es siempre positiva)."),
       ("¿Cuántas soluciones puede tener una bicuadrada?", "Cuatro, tres, dos, una o ninguna, según los valores de t = x² que salgan.")]
unit(4, R, "ecuaciones-y-sistemas", "A", "Ecuaciones bicuadradas, racionales, irracionales y exponenciales sencillas; sistemas de ecuaciones no lineales; resolución de problemas",
     "Ecuaciones y sistemas", "Ecuaciones y sistemas", "Fichas de matemáticas de 4.º de ESO: ecuaciones bicuadradas, racionales, irracionales y exponenciales, sistemas no lineales y problemas. 100 ejercicios con soluciones.",
     "Irracionales: comprueba siempre", "Bicuadradas: t = x² y después x = ±√t.", body, faq, sets, 4)
