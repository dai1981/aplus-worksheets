# -*- coding: utf-8 -*-
"""
España Matemáticas ESO: Polinomios (Sentido algebraico)
build(lv): lv = 2 → «polinomios-e-identidades-notables»: monomios, grado y valor numérico, sumar y multiplicar, identidades notables, sacar factor común;
lv = 3 → «polinomios-y-ruffini»: operaciones, división, regla de Ruffini, teorema del resto, factorizar;
lv = 4 → «polinomios-y-fracciones-algebraicas»: raíces y factorización, simplificar y operar fracciones algebraicas.
Errores: (a + b)² = a² + b², olvidar los huecos (coeficientes 0) en Ruffini, simplificar sumandos en una fracción algebraica.
"""
import random
from fractions import Fraction as F
from es_eso import M, mix, sg, fq, num, poly, E, unit, L, Kids, nz, sup, fr

R = None
LV = 2


def pm(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def pa(a, b):
    n = max(len(a), len(b))
    a = [0] * (n - len(a)) + a
    b = [0] * (n - len(b)) + b
    out = [x + y for x, y in zip(a, b)]
    while len(out) > 1 and out[0] == 0:
        out = out[1:]
    return out


def ev(p, x):
    v = 0
    for c in p:
        v = v * x + c
    return v


def rp(deg, lo=-6, hi=6):
    return [nz(R, -5, 5)] + [R.randint(lo, hi) for _ in range(deg)]


def lin(r):
    """(x − r) como texto"""
    return "(x %s %d)" % ("−" if r > 0 else "+", abs(r)) if r else "x"


def s_monomios():
    a, b = nz(R, -9, 9), nz(R, -9, 9)
    m, n = R.randint(1, 5), R.randint(1, 5)
    t = R.choice(["suma", "prod", "coc", "grado", "valor"])
    if t == "suma":
        return M("Calcula: %s %s %s" % (E((a, "x" + sup(m))), "+" if b > 0 else "−", E((abs(b), "x" + sup(m)))), E((a + b, "x" + sup(m))) if a + b else "0",
                 [E((a + b, "x" + sup(2 * m))) if a + b else "1", E((a * b, "x" + sup(m))), E((a - b, "x" + sup(m))) if a != b else "2x"], "Monomios semejantes: se suman los coeficientes: <b>%s</b>." % (E((a + b, "x" + sup(m))) if a + b else "0"))
    if t == "prod":
        return M("Calcula: (%s) · (%s)" % (E((a, "x" + sup(m))), E((b, "x" + sup(n)))), E((a * b, "x" + sup(m + n))), [E((a * b, "x" + sup(m * n))) if m * n != m + n else E((a * b, "x" + sup(m + n + 1))), E((a + b, "x" + sup(m + n))) if a + b else "0", E((a * b, "x"))],
                 "Coeficientes por coeficientes y se suman los exponentes: <b>%s</b>." % E((a * b, "x" + sup(m + n))))
    if t == "coc":
        if m <= n:
            m, n = n + 1, m
        return M("Calcula: (%s) : (%s)" % (E((a * b, "x" + sup(m))), E((b, "x" + sup(n)))), E((a, "x" + sup(m - n)) if m - n else (a, "")), [E((a, "x" + sup(m + n))), E((a * b * b, "x" + sup(m - n)) if m - n else (a * b * b, "")), E((-a, "x" + sup(m - n)) if m - n else (-a, ""))],
                 "Se dividen los coeficientes y se restan los exponentes: <b>%s</b>." % E((a, "x" + sup(m - n)) if m - n else (a, "")))
    p = rp(R.randint(2, 4))
    if t == "grado":
        return M("¿Cuál es el grado del polinomio %s?" % poly(p), str(len(p) - 1), [str(len(p)), str(p[0]) if p[0] not in (len(p) - 1, len(p)) else str(len(p) + 1), str(sum(1 for c in p if c))] if sum(1 for c in p if c) not in (len(p) - 1,) else [str(len(p)), str(len(p) + 1), str(len(p) - 2)],
                 "El grado es el mayor exponente: <b>%d</b>." % (len(p) - 1))
    x = nz(R, -3, 3)
    v = ev(p, x)
    return M("Calcula el valor numérico de P(x) = %s para x = %s." % (poly(p), sg(x)), sg(v), [sg(ev(p, -x)) if ev(p, -x) != v else sg(v + 1), sg(sum(p)) if sum(p) != v else sg(v - 2), sg(-v) if v else "1"], "P(%s) = <b>%s</b>." % (sg(x), sg(v)))


def s_operar():
    p, q = rp(2), rp(R.randint(1, 2))
    t = R.choice(["suma", "resta", "prod", "prod"])
    if t == "suma":
        r = pa(p, q)
        return M("Si P(x) = %s y Q(x) = %s, calcula P(x) + Q(x)." % (poly(p), poly(q)), poly(r), [poly(pa(p, [-c for c in q])), poly(pa(p, q[:-1] + [0])) if len(q) > 1 else poly(pa(p, [q[0] + 1])), poly(pm(p, q))], "Sumamos los términos del mismo grado: <b>%s</b>." % poly(r))
    if t == "resta":
        r = pa(p, [-c for c in q])
        w = pa(p, [-q[0]] + q[1:]) if len(q) > 1 else pa(p, [q[0]])
        return M("Si P(x) = %s y Q(x) = %s, calcula P(x) − Q(x)." % (poly(p), poly(q)), poly(r), [poly(w), poly(pa(p, q)), poly(pa([-c for c in p], q))], "Cambiamos el signo de todos los términos de Q y sumamos: <b>%s</b>." % poly(r))
    q = [nz(R, -4, 4), R.randint(-6, 6)]
    r = pm(p, q)
    w1 = pa(pm(p, [q[0], 0]), [q[1]])
    return M("Multiplica: (%s) · (%s)" % (poly(p), poly(q)), poly(r), [poly(w1), poly(pm(p, [q[0], -q[1]])), poly(pa(r, [1]))], "Cada término del primero por cada término del segundo, y reducimos: <b>%s</b>." % poly(r))


def s_identidades():
    a = R.randint(1, 5)
    b = R.randint(1, 9)
    v = R.choice(["x", "y", "a"])
    t = R.choice(["sq+", "sq-", "dif", "inv_sq", "inv_dif"])
    A = ("%d%s" % (a, v)) if a != 1 else v
    if t == "sq+":
        ok = E((a * a, v + "²"), (2 * a * b, v), (b * b, ""))
        return M("Desarrolla: (%s + %d)²" % (A, b), ok, [E((a * a, v + "²"), (b * b, "")), E((a * a, v + "²"), (a * b, v), (b * b, "")), E((a * a, v + "²"), (2 * a * b, v), (2 * b, ""))],
                 "(a + b)² = a² + 2ab + b²: <b>%s</b>." % ok)
    if t == "sq-":
        ok = E((a * a, v + "²"), (-2 * a * b, v), (b * b, ""))
        return M("Desarrolla: (%s − %d)²" % (A, b), ok, [E((a * a, v + "²"), (-b * b, "")), E((a * a, v + "²"), (-2 * a * b, v), (-b * b, "")), E((a * a, v + "²"), (2 * a * b, v), (b * b, ""))],
                 "(a − b)² = a² − 2ab + b²: <b>%s</b>." % ok)
    if t == "dif":
        ok = E((a * a, v + "²"), (-b * b, ""))
        return M("Desarrolla: (%s + %d)(%s − %d)" % (A, b, A, b), ok, [E((a * a, v + "²"), (b * b, "")), E((a * a, v + "²"), (-2 * a * b, v), (-b * b, "")), E((a * a, v + "²"), (-b, ""))],
                 "(a + b)(a − b) = a² − b²: <b>%s</b>." % ok)
    if t == "inv_sq":
        s = R.choice([1, -1])
        ok = "(%s %s %d)²" % (A, "+" if s > 0 else "−", b)
        return M("Escribe como cuadrado: %s" % E((a * a, v + "²"), (s * 2 * a * b, v), (b * b, "")), ok, ["(%s %s %d)²" % (A, "−" if s > 0 else "+", b), "(%s + %d)(%s − %d)" % (A, b, A, b), "(%s %s %d)²" % (A, "+" if s > 0 else "−", b * b)],
                 "Es un cuadrado perfecto: a = %s, b = %d: <b>%s</b>." % (A, b, ok))
    ok = "(%s + %d)(%s − %d)" % (A, b, A, b)
    return M("Factoriza: %s" % E((a * a, v + "²"), (-b * b, "")), ok, ["(%s − %d)²" % (A, b), "(%s + %d)²" % (A, b), "(%s − %d)(%s − %d)" % (A, b * b, A, 1) if b > 1 else "(%s − 1)²" % A],
             "Diferencia de cuadrados: a² − b² = (a + b)(a − b): <b>%s</b>." % ok)


def s_factor_comun():
    k = R.randint(2, 6)
    a, b = nz(R, -5, 5), nz(R, -7, 7)
    m = R.randint(1, 2)
    t = R.choice(["num", "x"])
    if t == "num":
        q = E((k * a, "x"), (k * b, ""))
        ok = "%d(%s)" % (k, E((a, "x"), (b, "")))
        return M("Saca factor común: %s" % q, ok, ["%d(%s)" % (k, E((a, "x"), (k * b, ""))), "%d(%s)" % (k * a, E((1, "x"), (b, ""))) if k * a > 0 else "x(%s)" % E((k * a, ""), (k * b, "")), "%dx(%s)" % (k, E((a, ""), (b, "")))],
                 "Dividimos cada término entre %d: <b>%s</b>." % (k, ok))
    q = E((k * a, "x" + sup(m + 1)), (k * b, "x" + sup(m)))
    ok = "%dx%s(%s)" % (k, sup(m), E((a, "x"), (b, "")))
    return M("Saca factor común: %s" % q, ok, ["%dx(%s)" % (k, E((a, "x" + sup(m)), (b, "x" + sup(m - 1) if m > 1 else ""))) if m > 1 else "x(%s)" % E((k * a, "x"), (k * b, "")), "%d(%s)" % (k, E((a, "x" + sup(m + 1)), (b, "x" + sup(m)))), "%dx%s(%s)" % (k, sup(m + 1), E((a, ""), (b, "")))],
             "El factor común es %dx%s: <b>%s</b>." % (k, sup(m), ok))


def s_division():
    q = rp(R.randint(1, 2))
    dv = [1, -nz(R, -5, 5)]
    r = R.randint(-9, 9)
    p = pa(pm(q, dv), [r])
    t = R.choice(["cociente", "resto", "resto_teo", "ruf"])
    a = -dv[1]
    if t == "cociente":
        return M("Divide %s entre %s. ¿Cuál es el cociente?" % (poly(p), poly(dv)), poly(q), [poly(pa(q, [1])), poly([-c for c in q]), poly(q + [0])], "Por Ruffini con %s: cociente <b>%s</b> y resto %s." % (sg(a), poly(q), sg(r)))
    if t in ("resto", "resto_teo"):
        return M("¿Cuál es el resto de dividir %s entre %s?" % (poly(p), poly(dv)), sg(r), [sg(ev(p, -a)) if ev(p, -a) != r else sg(r + 1), sg(r + a), sg(p[-1]) if p[-1] != r else sg(r - 1)],
                 "Teorema del resto: el resto es P(%s) = <b>%s</b>." % (sg(a), sg(r)))
    ok = "%s y resto %s" % (poly(q), sg(r))
    return M("Aplica la regla de Ruffini: (%s) : %s" % (poly(p), lin(a)), ok, ["%s y resto %s" % (poly(q), sg(-r) if r else "1"), "%s y resto %s" % (poly(pa(q, [1])), sg(r)), "%s y resto %s" % (poly([-c for c in q]), sg(r))],
             "Bajamos los coeficientes, multiplicamos por %s y sumamos: <b>%s</b>." % (sg(a), ok))


def s_raices():
    rs = R.sample([-4, -3, -2, -1, 1, 2, 3, 4, 5], R.choice([2, 3]))
    p = [1]
    for r in rs:
        p = pm(p, [1, -r])
    t = R.choice(["fact", "raices", "es_raiz", "k"])
    if t == "fact":
        ok = "".join(lin(r) for r in sorted(rs))
        w1 = "".join(lin(-r) for r in sorted(rs))
        w2 = "".join(lin(r) for r in sorted(rs)[:-1]) + lin(sorted(rs)[-1] + 1)
        return M("Factoriza: %s" % poly(p), ok, [w1, w2, "x" + "".join(lin(r) for r in sorted(rs)[1:])], "Las raíces son %s: <b>%s</b>." % (", ".join(sg(r) for r in sorted(rs)), ok))
    if t == "raices":
        ok = ", ".join(sg(r) for r in sorted(rs))
        return M("¿Cuáles son las raíces enteras de %s?" % poly(p), ok, [", ".join(sg(-r) for r in sorted(rs, reverse=True)), ", ".join(sg(r) for r in sorted(rs)[:-1]), ", ".join(sg(r) for r in sorted(rs[:-1] + [rs[-1] + 1]))],
                 "Probamos con los divisores del término independiente (%s): <b>%s</b>." % (sg(p[-1]), ok))
    if t == "es_raiz":
        c = R.choice([rs[0], -rs[0] if -rs[0] not in rs else rs[0] + 6])
        ok = "sí" if ev(p, c) == 0 else "no"
        return M("¿Es x = %s raíz de P(x) = %s?" % (sg(c), poly(p)), ok, ["no" if ok == "sí" else "sí", "solo si es positivo", "no se puede saber"], "P(%s) = %s: <b>%s</b>." % (sg(c), sg(ev(p, c)), ok))
    r = R.randint(-3, 3)
    base = rp(2)
    p2 = base[:-1] + [0]
    k = -ev(p2, r)
    return M("¿Qué valor de k hace que %s + k sea divisible por %s?" % (poly(p2), lin(r)), "k = %s" % sg(k), ["k = %s" % sg(-k) if k else "k = 1", "k = %s" % sg(k + r), "k = %s" % sg(r)],
             "Debe ser P(%s) = 0: %s + k = 0, <b>k = %s</b>." % (sg(r), sg(-k), sg(k)))


def s_fracciones():
    t = R.choice(["simp", "simp", "suma", "prod"])
    a, b = R.sample([-4, -3, -2, -1, 1, 2, 3, 4, 5], 2)
    if t == "simp":
        c = R.choice([x for x in (-5, -2, 1, 3, 6) if x not in (a, b)])
        num_ = pm([1, -a], [1, -b])
        den_ = pm([1, -a], [1, -c])
        ok = fr(poly([1, -b]), poly([1, -c]))
        return M("Simplifica: %s" % fr(poly(num_), poly(den_)), ok, [fr(poly([1, -a]), poly([1, -c])), fr(poly([1, -b]), poly([1, -a])), fr(poly(num_[1:]), poly(den_[1:])) if num_[1] and den_[1] else fr(str(-b), str(-c))],
                 "Factorizamos y tachamos el factor común %s: <b>%s</b>." % (lin(a), ok))
    if t == "suma":
        k1, k2 = nz(R, -5, 5), nz(R, -5, 5)
        numr = pa([k1, -k1 * b], [k2, -k2 * a])
        den = pm([1, -a], [1, -b])
        ok = fr(poly(numr), poly(den))
        return M("Calcula: %s + %s" % (fr(str(k1), poly([1, -a])), fr(str(k2), poly([1, -b]))), ok, [fr(str(k1 + k2), poly(pa([1, -a], [1, -b]))), fr(str(k1 + k2), poly(den)), fr(poly(pa([k1, -k1 * a], [k2, -k2 * b])), poly(den))],
                 "Común denominador %s%s: <b>%s</b>." % (lin(a), lin(b), ok))
    c = R.choice([x for x in (-5, -2, 1, 3, 6) if x not in (a, b)])
    ok = fr(poly([1, -b]), poly([1, -c]))
    return M("Calcula y simplifica: %s · %s" % (fr(poly([1, -a]), poly([1, -c])), fr(poly([1, -b]), poly([1, -a]))), ok, [fr(poly([1, -a]), poly([1, -c])), fr(poly([1, -b]), poly([1, -a])), fr("1", poly([1, -c]))],
             "Multiplicamos y tachamos %s: <b>%s</b>." % (lin(a), ok))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(48005 + (lv - 2) * 1000)
    seen = set()
    if lv == 2:
        sets = [("Monomios", mix(R, seen, [(s_monomios, 20)])), ("Sumar y restar polinomios", mix(R, seen, [(s_operar, 20)])), ("Multiplicar polinomios", mix(R, seen, [(s_operar, 20)])),
                ("Identidades notables", mix(R, seen, [(s_identidades, 20)])), ("Sacar factor común", mix(R, seen, [(s_factor_comun, 12), (s_identidades, 8)]))]
        think = ["Un <b>polinomio</b> es una suma de monomios. Su grado es el mayor exponente.",
                 "Para sumar, se juntan los términos del mismo grado. Para multiplicar, cada término por cada término.",
                 "<b>Identidades notables</b>: (a + b)² = a² + 2ab + b²; (a − b)² = a² − 2ab + b²; (a + b)(a − b) = a² − b²."]
        ex = [("(2x + 3)²", ["(2x)² + 2 · 2x · 3 + 3²"], "4x² + 12x + 9"), ("6x³ − 9x²", ["Factor común 3x²"], "3x²(2x − 3)")]
        slug, title, short, kb, ks, sort = "polinomios-e-identidades-notables", "Polinomios e identidades notables", "Polinomios", "(a + b)² = a² + 2ab + b²", "No es a² + b²: falta el doble producto.", 5
        meta = "Fichas de matemáticas de 2.º de ESO: monomios, polinomios, sumar y multiplicar, identidades notables y sacar factor común. 100 ejercicios con soluciones."
        std = "Expresiones algebraicas: monomios y polinomios; operaciones; identidades notables; extracción de factor común"
    elif lv == 3:
        sets = [("Operar con polinomios", mix(R, seen, [(s_operar, 20)])), ("Identidades notables", mix(R, seen, [(s_identidades, 20)])), ("División y regla de Ruffini", mix(R, seen, [(s_division, 20)])),
                ("Teorema del resto", mix(R, seen, [(s_division, 20)])), ("Factorizar polinomios", mix(R, seen, [(s_raices, 12), (s_factor_comun, 8)]))]
        think = ["Para dividir entre (x − a) se usa la <b>regla de Ruffini</b>: se bajan los coeficientes (con 0 en los huecos), se multiplica por a y se suma.",
                 "<b>Teorema del resto</b>: el resto de dividir P(x) entre (x − a) es P(a).",
                 "Si P(a) = 0, a es una <b>raíz</b> y (x − a) es un factor. Las raíces enteras son divisores del término independiente."]
        ex = [("(x³ − 2x + 5) : (x − 2)", ["Coeficientes 1, 0, −2, 5", "Ruffini con 2"], "x² + 2x + 2 y resto 9"), ("x² − x − 6", ["Raíces 3 y −2"], "(x − 3)(x + 2)")]
        slug, title, short, kb, ks, sort = "polinomios-y-ruffini", "Polinomios, Ruffini y teorema del resto", "Polinomios", "Resto de P(x) : (x − a) = P(a)", "Si P(a) = 0, (x − a) es factor.", 4
        meta = "Fichas de matemáticas de 3.º de ESO: operar con polinomios, identidades notables, regla de Ruffini, teorema del resto y factorizar. 100 ejercicios con soluciones."
        std = "Polinomios: operaciones, división, regla de Ruffini, teorema del resto; raíces y factorización"
    else:
        sets = [("Ruffini y teorema del resto", mix(R, seen, [(s_division, 20)])), ("Raíces y factorización", mix(R, seen, [(s_raices, 20)])), ("Identidades y factor común", mix(R, seen, [(s_identidades, 10), (s_factor_comun, 10)])),
                ("Simplificar fracciones algebraicas", mix(R, seen, [(s_fracciones, 20)])), ("Operar fracciones algebraicas", mix(R, seen, [(s_fracciones, 20)]))]
        think = ["Para factorizar: saca factor común, busca identidades notables y usa Ruffini con los divisores del término independiente.",
                 "Una <b>fracción algebraica</b> se simplifica factorizando numerador y denominador y tachando factores comunes (nunca sumandos).",
                 "Para sumar fracciones algebraicas, se busca un denominador común, como con los números."]
        ex = [("(x² − 4)/(x² + x − 2)", ["(x − 2)(x + 2) / ((x + 2)(x − 1))"], "(x − 2)/(x − 1)")]
        slug, title, short, kb, ks, sort = "polinomios-y-fracciones-algebraicas", "Polinomios y fracciones algebraicas", "Fracciones algebraicas", "Factoriza y tacha factores", "Nunca taches sumandos.", 3
        meta = "Fichas de matemáticas de 4.º de ESO: Ruffini, teorema del resto, raíces, factorizar polinomios, simplificar y operar fracciones algebraicas. 100 ejercicios con soluciones."
        std = "Polinomios: factorización y raíces; fracciones algebraicas: simplificación y operaciones"
    mist = [["Escribir (a + b)² = a² + b²", "Falta el doble producto 2ab."], ["Olvidar los huecos en Ruffini", "x³ − 2x + 5 tiene coeficientes 1, 0, −2, 5."], ["Tachar sumandos en una fracción", "Solo se tachan factores que multiplican."]]
    body = L(think, ex, mist)
    faq = [("¿Qué es la regla de Ruffini?", "Un método rápido para dividir un polinomio entre (x − a) usando solo los coeficientes."), ("¿Qué dice el teorema del resto?", "Que el resto de dividir P(x) entre (x − a) es igual a P(a).")]
    unit(lv, R, slug, "A", std, title, short, meta, kb, ks, body, faq, sets, sort)


if __name__ == "__main__":
    build(2)
