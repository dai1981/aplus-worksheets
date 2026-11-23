# -*- coding: utf-8 -*-
"""
España Matemáticas I (1.º de Bachillerato): Números reales y logaritmos (Sentido numérico)
Intervalos y valor absoluto, radicales (simplificar, operar, racionalizar), logaritmos (definición, propiedades, cambio de base),
ecuaciones exponenciales y logarítmicas, problemas de crecimiento.
Errores: log(a + b) = log a + log b, aceptar soluciones que dan logaritmos de números negativos, racionalizar sin el conjugado.
"""
import math
import random
from fractions import Fraction as F
from es_bach import M, mix, fq, sg, d, num, unit, L, E, P2, sol, raiz, MINUS, r2, nf, use_, W

R = random.Random(51001)
S_IVL, S_UNION, S_ABS = use_("gen_es_matematicas_3eso_numeros_reales", 51101, "s_ivl", "s_union", "s_absoluto")
LOGS = {2: 0.301, 3: 0.477, 5: 0.699, 7: 0.845}


def s_radicales():
    t = R.choice(["simp", "simp", "suma", "prod", "rac", "conj"])
    if t == "simp":
        a, b = R.randint(2, 9), R.choice([2, 3, 5, 6, 7, 10, 11])
        n = a * a * b
        return M("Simplifica √%d." % n, "%d√%d" % (a, b), ["%d√%d" % (b, a) if a != b else "%d√%d" % (a + 1, b), "√%d" % (a * b), "%d√%d" % (a * a, b)], "%d = %d² · %d → √%d = <b>%d√%d</b>." % (n, a, b, n, a, b))
    if t == "suma":
        b = R.choice([2, 3, 5])
        a1, a2, a3 = R.sample(range(2, 7), 3)
        k1, k2 = R.randint(1, 4), R.randint(1, 4)
        tot = k1 * a1 + k2 * a2
        return M("Calcula %d√%d + %d√%d." % (k1, a1 * a1 * b, k2, a2 * a2 * b), raiz(tot * tot * b), ["%d√%d" % (k1 + k2, b * (a1 * a1 + a2 * a2)), "√%d" % (k1 * a1 * a1 * b + k2 * a2 * a2 * b), "%d√%d" % (k1 + k2, b)],
                 "%d√%d = %d√%d y %d√%d = %d√%d; suman <b>%s</b>." % (k1, a1 * a1 * b, k1 * a1, b, k2, a2 * a2 * b, k2 * a2, b, raiz(tot * tot * b)))
    if t == "prod":
        a, b = R.sample([2, 3, 5, 6, 8, 10, 12, 15, 18], 2)
        return M("Calcula √%d · √%d." % (a, b), raiz(a * b), ["√%d" % (a + b), raiz(a * b * 2) if raiz(a * b * 2) != raiz(a * b) else "%d" % (a * b), "%d" % (a * b)], "√%d · √%d = √%d = <b>%s</b>." % (a, b, a * b, raiz(a * b)))
    if t == "rac":
        a, b = R.randint(1, 12), R.choice([2, 3, 5, 6, 7])
        v = F(a, b)
        num_ = "%s√%d" % ("" if v.numerator == 1 else v.numerator, b)
        ok = num_ if v.denominator == 1 else "%s/%d" % (num_, v.denominator)
        return M("Racionaliza %d/√%d." % (a, b), ok, ["%d/%d" % (a, b), "%d√%d" % (a, b), "√%d/%d" % (a, b) if a != 1 else "√%d" % b], "Multiplicamos arriba y abajo por √%d: %d√%d/%d = <b>%s</b>." % (b, a, b, b, ok))
    n = R.choice([2, 3, 5, 6, 7])
    m = R.randint(1, 3)
    if n == m * m:
        return None
    den = n - m * m
    ok = "(√%d + %d)/%d" % (n, m, den) if den > 1 else "√%d + %d" % (n, m) if den == 1 else "−√%d − %d" % (n, m) if den == -1 else "−(√%d + %d)/%d" % (n, m, -den)
    return M("Racionaliza 1/(√%d − %d)." % (n, m), ok, ["(√%d − %d)/%d" % (n, m, abs(den)), "1/(√%d + %d)" % (n, m), "(√%d + %d)/%d" % (n, m, n + m * m), "(√%d + %d)/%d" % (n, m, abs(den))], "Multiplicamos por el conjugado √%d + %d: el denominador es %d − %d = %s. <b>%s</b>." % (n, m, n, m * m, sg(den), ok))


def s_log_def():
    t = R.choice(["ent", "neg", "frac", "ln", "inv"])
    b = R.choice([2, 3, 4, 5, 10])
    if t == "ent":
        k = R.randint(2, 5 if b < 5 else 3)
        return M("Calcula log<sub>%d</sub> %s." % (b, num(b ** k)), str(k), [str(b ** k // b), str(k + 1), str(b * k) if b * k != k else "1"], "%d<sup>%d</sup> = %s → <b>%d</b>." % (b, k, num(b ** k), k))
    if t == "neg":
        k = R.randint(1, 4 if b < 5 else 2)
        return M("Calcula log<sub>%d</sub> (1/%s)." % (b, num(b ** k)), sg(-k), [str(k), fq(F(1, k)) if k > 1 else "0", sg(-k - 1)], "1/%s = %d<sup>−%d</sup> → <b>%s</b>." % (num(b ** k), b, k, sg(-k)))
    if t == "frac":
        base, x, v = R.choice([(4, 2, F(1, 2)), (9, 3, F(1, 2)), (8, 2, F(1, 3)), (27, 3, F(1, 3)), (4, 8, F(3, 2)), (9, 27, F(3, 2)), (16, 8, F(3, 4)), (25, 125, F(3, 2)), (8, 4, F(2, 3)), (100, 10, F(1, 2))])
        return M("Calcula log<sub>%d</sub> %d." % (base, x), fq(v), [fq(1 / v), fq(F(x, base)), sg(x // 2) if x // 2 else "2"], "%d = %d<sup>%s</sup> → <b>%s</b>." % (x, base, fq(v), fq(v)))
    if t == "ln":
        k = R.randint(-3, 5)
        return M("Calcula ln e<sup>%d</sup>." % k if k != 1 else "Calcula ln e.", sg(k), [sg(k + 1), "e" if k != 1 else "0", sg(-k) if k else "1"], "ln e<sup>k</sup> = k: <b>%s</b>." % sg(k))
    k = R.randint(2, 4)
    return M("¿Qué número x cumple log<sub>%d</sub> x = %d?" % (b, k), num(b ** k), [num(b * k), num(k ** b) if k ** b != b ** k else num(b ** k + 1), num(b ** (k - 1))], "x = %d<sup>%d</sup> = <b>%s</b>." % (b, k, num(b ** k)))


def s_log_prop():
    t = R.choice(["calc", "calc", "calc", "base", "simp"])
    if t == "calc":
        e2, e3, e5 = R.randint(0, 3), R.randint(0, 2), R.choice([0, 0, 1, -1])
        if e2 == e3 == e5 == 0 or (e2 + e3 == 0):
            return None
        x = F(2) ** e2 * F(3) ** e3 * F(5) ** e5
        if x == 10 or x.denominator not in (1, 2, 4, 8, 5, 3) or x < 1:
            return None
        v = e2 * LOGS[2] + e3 * LOGS[3] + e5 * LOGS[5]
        xs = d(x) if x.denominator in (2, 4, 5, 8) else num(int(x)) if x.denominator == 1 else None
        if xs is None:
            return None
        fac = " · ".join(f for f in ["2" + ("<sup>%d</sup>" % e2 if e2 > 1 else "") if e2 else "", "3" + ("<sup>%d</sup>" % e3 if e3 > 1 else "") if e3 else "", ("5" if e5 > 0 else "") ] if f)
        if e5 < 0:
            fac = fac + " / 5"
        terms = []
        if e2:
            terms.append("%slog 2" % ("%d · " % e2 if e2 > 1 else ""))
        if e3:
            terms.append("%slog 3" % ("%d · " % e3 if e3 > 1 else ""))
        txt = " + ".join(terms)
        if e5:
            txt += " %s log 5" % ("+" if e5 > 0 else "−")
        return M("Sabiendo que log 2 ≈ 0,301 y log 3 ≈ 0,477, calcula log %s." % xs, r2(v, 3), [r2(LOGS[2] * LOGS[3] if e2 and e3 else v + 0.1, 3), r2(v * 2, 3), r2(abs(e2 * LOGS[2] - e3 * LOGS[3]) + 0.001 if e3 else v - 0.301, 3)],
                 "%s = %s → log %s = %s%s ≈ <b>%s</b>." % (xs, fac, xs, txt, " (log 5 = log 10 − log 2 ≈ 0,699)" if e5 else "", r2(v, 3)))
    if t == "base":
        b, x = R.choice([(2, 5), (2, 3), (3, 2), (2, 7), (3, 5), (5, 2), (3, 7), (5, 3), (7, 2)])
        v = math.log(x) / math.log(b)
        return M("Con la fórmula del cambio de base, calcula log<sub>%d</sub> %d (redondea a las milésimas)." % (b, x), r2(v, 3), [r2(math.log10(x) - math.log10(b), 3), r2(math.log(b) / math.log(x), 3), r2(x / b, 3)], "log<sub>%d</sub> %d = log %d / log %d ≈ <b>%s</b>." % (b, x, x, b, r2(v, 3)))
    a, b = R.sample([2, 3, 4, 5, 6, 8, 25, 20, 50], 2)
    k = R.choice(["suma", "resta"])
    if k == "suma":
        if a * b % 10 or a * b not in (10, 100, 1000):
            return None
        v = int(round(math.log10(a * b)))
        return M("Calcula log %d + log %d." % (a, b), str(v), ["log %d" % (a + b), str(v + 1), "%s" % r2(math.log10(a + b), 3)], "log %d + log %d = log %d = <b>%d</b>." % (a, b, a * b, v))
    if a % b or a // b not in (2, 4, 5, 10):
        return None
    return M("Expresa log %d − log %d como un único logaritmo." % (a, b), "log %d" % (a // b), ["log %d" % (a - b), "log %d" % (a * b), "log %d / log %d" % (a, b)], "La resta de logaritmos es el logaritmo del cociente: <b>log %d</b>." % (a // b))


def s_ecuaciones():
    t = R.choice(["exp1", "exp2", "exp3", "suma", "log1", "log2", "ln"])
    if t == "exp1":
        b = R.choice([2, 3, 5])
        k, n = R.randint(-3, 3), R.randint(2, 6 if b == 2 else 4)
        a = R.choice([1, 2])
        if (n - k) % a:
            return None
        x = F(n - k, a)
        lhs = ("%dx" % a if a > 1 else "x") + ((" + %d" % k) if k > 0 else (" − %d" % -k) if k < 0 else "")
        return M("Resuelve %d<sup>%s</sup> = %s." % (b, lhs, num(b ** n)), "x = %s" % nf(x), ["x = %s" % nf(F(n + k, a)), "x = %s" % nf(F(b ** n - k, a)), "x = %s" % nf(x + 1)], "%s = %d<sup>%d</sup> → %s = %d → <b>x = %s</b>." % (num(b ** n), b, n, lhs, n, nf(x)))
    if t == "exp2":
        b, p, q, x = R.choice([(4, 2, 2, F(3, 2)), (8, 2, 3, F(4, 3)), (9, 3, 2, F(3, 2)), (27, 3, 3, F(2, 3)), (4, 2, 2, F(5, 2)), (25, 5, 2, F(3, 2)), (8, 2, 3, F(5, 3))])
        rhs = p ** int(q * x)
        return M("Resuelve %d<sup>x</sup> = %d." % (b, rhs), "x = %s" % nf(x), ["x = %s" % nf(F(rhs, b)), "x = %s" % nf(1 / x), "x = %s" % nf(q * x)], "%d = %d<sup>%d</sup> y %d = %d<sup>%d</sup> → %dx = %d → <b>x = %s</b>." % (b, p, q, rhs, p, int(q * x), q, int(q * x), nf(x)))
    if t == "exp3":
        r1, r2_ = R.sample(range(0, 4), 2)
        b = R.choice([2, 3])
        u1, u2 = b ** r1, b ** r2_
        eq = "%d<sup>2x</sup> − %d · %d<sup>x</sup> + %d = 0" % (b, u1 + u2, b, u1 * u2)
        return M("Resuelve %s." % eq, sol([r1, r2_]), [sol([u1, u2]), "x = %d" % max(r1, r2_), sol([-r1, -r2_]) if r1 or r2_ else "x = 1"], "Cambio t = %d<sup>x</sup>: t² − %dt + %d = 0 → t = %d o t = %d → <b>%s</b>." % (b, u1 + u2, u1 * u2, u1, u2, sol([r1, r2_])))
    if t == "suma":
        b = R.choice([2, 3])
        x = R.randint(1, 4)
        tot = b ** x + b ** (x + 1)
        return M("Resuelve %d<sup>x</sup> + %d<sup>x + 1</sup> = %d." % (b, b, tot), "x = %d" % x, ["x = %d" % (x + 1), "x = %s" % nf(F(tot, 2 * b)), "x = %d" % (x - 1) if x > 1 else "x = 0"], "%d<sup>x</sup>(1 + %d) = %d → %d<sup>x</sup> = %d → <b>x = %d</b>." % (b, b, tot, b, b ** x, x))
    if t == "log1":
        b, k, a = R.choice([2, 3, 5]), R.randint(1, 4), R.randint(-5, 6)
        if b == 5 and k > 3:
            return None
        x = b ** k + a
        arg = E((1, "x"), (-a, ""))
        return M("Resuelve log<sub>%d</sub> (%s) = %d." % (b, arg, k), "x = %d" % x, ["x = %d" % (k + a), "x = %d" % (b * k + a), "x = %d" % (k ** b + a) if k ** b != b ** k else "x = %d" % (x + 1)], "%s = %d<sup>%d</sup> = %d → <b>x = %d</b>." % (arg, b, k, b ** k, x))
    if t == "log2":
        while True:
            x, k = R.randint(2, 10), R.randint(1, 6)
            p = x * (x - k)
            if p == 10 or p == 100:
                break
        lg = 1 if p == 10 else 2
        other = -(x - k) if False else k - x
        return M("Resuelve log x + log (x − %d) = %d." % (k, lg), "x = %d" % x, [sol([x, other]), "x = %d" % other, "x = %d" % (x + k)], "x(x − %d) = %d → x = %d o x = %s; la negativa no vale (no hay logaritmos de negativos). <b>x = %d</b>." % (k, p, x, sg(other), x))
    k = R.randint(2, 6)
    a = R.choice([1, 2, 3])
    v = math.exp(k) / a if R.random() < 0.0 else None
    return M("Resuelve ln (%dx) = %d." % (a, k) if a > 1 else "Resuelve ln x = %d." % k, "x = e<sup>%d</sup>%s" % (k, "/%d" % a if a > 1 else ""), ["x = %d/e" % k if a == 1 else "x = %de<sup>%d</sup>" % (a, k), "x = 10<sup>%d</sup>%s" % (k, "/%d" % a if a > 1 else ""), "x = %d" % (k * 10)], "%sx = e<sup>%d</sup> → <b>x = e<sup>%d</sup>%s</b>." % ("%d" % a if a > 1 else "", k, k, "/%d" % a if a > 1 else ""))


def s_problema():
    t = R.choice(["doble", "vida", "pobl", "capital", "doble", "vida", "pobl", "capital", "ph"])
    if t == "doble":
        r = R.choice([2, 3, 4, 5, 6, 8])
        tt = math.log(2) / math.log(1 + r / 100)
        n = math.ceil(tt)
        return M("Un capital se invierte al %d %% de interés compuesto anual. ¿Cuántos años completos tardará en duplicarse?" % r, "%d años" % n, ["%d años" % (100 // r), "%d años" % (n + 2), "%d años" % (n - 2)], "(1,%02d)<sup>t</sup> = 2 → t = log 2 / log 1,%02d ≈ %s → <b>%d años</b>." % (r, r, r2(tt, 1), n))
    if t == "vida":
        T, m0, m1 = R.choice([(5, 80, 10), (8, 200, 25), (10, 160, 20), (30, 64, 4), (12, 96, 12), (6, 120, 15)])
        k = round(math.log2(m0 / m1))
        return M("Una sustancia radiactiva tiene un periodo de semidesintegración de %d años. ¿Cuánto tarda en pasar de %d g a %d g?" % (T, m0, m1), "%d años" % (k * T), ["%d años" % (T * (m0 - m1) // m0 * 2 if False else (k + 1) * T), "%d años" % ((m0 // m1) * T), "%d años" % (k * T // 2)], "%d → %d son %d mitades: %d · %d = <b>%d años</b>." % (m0, m1, k, k, T, k * T))
    if t == "pobl":
        p0, r, n = R.choice([1000, 2000, 5000, 500]), R.choice([2, 3, 5]), R.randint(5, 15)
        v = p0 * (1 + r / 100) ** n
        return M("Una población de %s bacterias crece un %d %% cada hora. ¿Cuántas habrá dentro de %d horas? (redondea a las unidades)" % (num(p0), r, n), num(int(v + 0.5)), [num(int(p0 * (1 + r * n / 100) + 0.5)), num(int(p0 * (1 + r / 100) ** (n - 1) + 0.5)), num(int(v * (1 + r / 100) + 0.5))],
                 "P = %s · 1,%02d<sup>%d</sup> ≈ <b>%s</b>." % (num(p0), r, n, num(int(v + 0.5))))
    if t == "capital":
        c0, r, n = R.choice([1000, 2000, 5000, 3000]), R.choice([2, 3, 4]), R.randint(3, 10)
        v = c0 * (1 + r / 100) ** n
        return M("¿En qué se convierten %s € al %d %% de interés compuesto anual durante %d años? (redondea a los céntimos)" % (num(c0), r, n), "%s €" % r2(v), ["%s €" % r2(c0 * (1 + r * n / 100)), "%s €" % r2(c0 * (1 + r / 100) ** (n - 1)), "%s €" % r2(c0 * r / 100 * n)],
                 "C = %s · 1,%02d<sup>%d</sup> ≈ <b>%s €</b>." % (num(c0), r, n, r2(v)))
    k = R.randint(2, 6)
    return M("El pH se define como pH = −log [H<sup>+</sup>]. Si [H<sup>+</sup>] = 10<sup>−%d</sup> mol/L, ¿cuál es el pH?" % k, str(k), [sg(-k), str(10 - k) if 10 - k != k else "8", "%d" % (k * 10)], "pH = −log 10<sup>−%d</sup> = −(−%d) = <b>%d</b>." % (k, k, k))


seen = set()
sets = [("Intervalos y valor absoluto", mix(R, seen, [(S_IVL, 7), (S_UNION, 7), (S_ABS, 6)])), ("Radicales", mix(R, seen, [(s_radicales, 20)])),
        ("Logaritmos", mix(R, seen, [(s_log_def, 10), (s_log_prop, 10)])), ("Ecuaciones exponenciales y logarítmicas", mix(R, seen, [(s_ecuaciones, 20)])), ("Problemas de crecimiento", mix(R, seen, [(s_problema, 20)]))]
think = ["Los <b>números reales</b> se representan en la recta; un trozo de ella es un <b>intervalo</b>.",
         "<b>Racionalizar</b> es quitar las raíces del denominador: se multiplica por la raíz o por el <b>conjugado</b> (√a − b → √a + b).",
         "log<sub>b</sub> x = y significa b<sup>y</sup> = x. Propiedades: log (ab) = log a + log b; log (a/b) = log a − log b; log a<sup>n</sup> = n log a. Cambio de base: log<sub>b</sub> x = log x / log b.",
         "En las ecuaciones logarítmicas hay que <b>comprobar</b> que los logaritmos existen (argumento positivo)."]
ex = [("log x + log (x − 3) = 1", ["x(x − 3) = 10", "x = 5 o x = −2"], "x = 5"), ("4<sup>x</sup> = 8", ["2<sup>2x</sup> = 2<sup>3</sup>"], "x = 3/2")]
mist = [["log (a + b) = log a + log b", "Falso: es log (ab) = log a + log b."], ["Aceptar x = −2", "log (−2) no existe."], ["Racionalizar 1/(√5 − 1) con √5", "Hace falta el conjugado √5 + 1."]]
body = L(think, ex, mist)
faq = [("¿Qué diferencia hay entre log y ln?", "log es el logaritmo decimal (base 10) y ln el neperiano (base e ≈ 2,718)."),
       ("¿Para qué sirven los logaritmos?", "Para despejar exponentes: tiempos de duplicación, desintegración radiactiva, pH, terremotos o decibelios.")]
unit(1, R, "numeros-reales-y-logaritmos", "N", "Números reales: intervalos, valor absoluto, radicales y racionalización; logaritmos y sus propiedades; ecuaciones exponenciales y logarítmicas",
     "Números reales y logaritmos", "Reales y logaritmos", "Fichas de Matemáticas I (1.º de Bachillerato): intervalos, radicales, racionalización, logaritmos, ecuaciones exponenciales y logarítmicas. 100 ejercicios con soluciones.",
     "log (ab) = log a + log b", "Comprueba siempre las soluciones logarítmicas.", body, faq, sets, 1)
