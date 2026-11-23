# -*- coding: utf-8 -*-
"""
España Matemáticas Aplicadas a las Ciencias Sociales I (1.º de Bachillerato): Derivadas (Sentido de la medida)
Tasa de variación media, derivada en un punto, reglas de derivación, regla de la cadena, recta tangente, crecimiento;
interpretación económica: coste e ingreso marginal, tasa de variación de ventas o población.
Reutiliza los generadores de Matemáticas I con otra semilla.
Errores: confundir la TVM con la derivada, dar C(x) en lugar de C′(x), olvidar la derivada interior.
"""
import random
from es_ccss import M, mix, num, unit, L, r2, W, eu, use_, sg, E, kurve, BLUE, RED

R = random.Random(53007)
s_tvm, s_reglas, s_prod, s_cadena, s_tangente = use_("gen_es_matematicas_1bach_derivadas", 53207, "s_tvm", "s_reglas", "s_prod", "s_cadena", "s_tangente")
s_monotonia, = use_("gen_es_matematicas_1bach_aplicaciones_derivadas", 53307, "s_monotonia"),


def C2(a, b, c):
    return E((a, "x²"), (b, "x"), (c, ""))


def s_marginal():
    t = R.choice(["coste", "coste", "ingreso", "tvm", "tvm", "interp", "signo"])
    if t == "coste":
        a, b, c = R.choice([0.01, 0.02, 0.05, 0.1]), R.randint(2, 20), R.randrange(200, 2001, 100)
        x = R.randrange(20, 201, 10)
        mg = 2 * a * x + b
        return M("El coste de producir x unidades es C(x) = %sx² + %dx + %s euros. Calcula el coste marginal para x = %d, C′(%d)." % (r2(a), b, num(c), x, x), eu(mg),
                 W([eu(a * x * x + b * x + c), eu(a * x + b), eu(2 * a + b), eu((a * x * x + b * x + c) / x)]),
                 "C′(x) = %sx + %d → C′(%d) = <b>%s</b>: producir una unidad más cuesta unos %s." % (r2(2 * a), b, x, eu(mg), eu(mg)))
    if t == "ingreso":
        p, q = R.randint(20, 90), R.choice([0.1, 0.2, 0.25, 0.5])
        x = R.randrange(10, int(p / (2 * q)), 5) if p / (2 * q) > 15 else None
        if x is None:
            return None
        mg = p - 2 * q * x
        return M("El ingreso por vender x unidades es I(x) = %dx − %sx² euros. ¿Cuál es el ingreso marginal para x = %d?" % (p, r2(q), x), eu(mg),
                 W([eu(p * x - q * x * x), eu(p - q * x), eu(p - 2 * q), eu(p)]),
                 "I′(x) = %d − %sx → I′(%d) = <b>%s</b>." % (p, "" if 2 * q == 1 else r2(2 * q), x, eu(mg)))
    if t == "tvm":
        a, b, c = R.choice([(-2, 40, 100), (-1, 20, 50), (3, 10, 200), (-3, 60, 150), (2, 5, 80), (-1, 30, 120)])
        t1, t2 = sorted(R.sample(range(0, 11), 2))
        f = lambda s: a * s * s + b * s + c
        v = (f(t2) - f(t1)) / (t2 - t1)
        quien = R.choice([("Las ventas de una tienda (en miles de euros)", "miles de euros por mes", "t en meses"), ("Los visitantes de una web (en miles)", "miles por semana", "t en semanas")])
        vs = sg(int(v)) if v == int(v) else r2(v)
        return M("%s son V(t) = %s, con %s. ¿Cuál es la tasa de variación media entre t = %d y t = %d?" % (quien[0], C2(a, b, c).replace("x", "t"), quien[2], t1, t2), "%s %s" % (vs, quien[1]),
                 W(["%s %s" % (sg(f(t2) - f(t1)), quien[1]), "%s %s" % (sg(2 * a * t2 + b), quien[1]), "%s %s" % (r2(-v) if v else "1", quien[1]), "%s %s" % (r2((f(t2) + f(t1)) / 2), quien[1])]),
                 "TVM = (V(%d) − V(%d))/(%d − %d) = (%s − %s)/%d = <b>%s</b>." % (t2, t1, t2, t1, sg(f(t2)), sg(f(t1)), t2 - t1, vs))
    if t == "interp":
        x, k = R.randrange(50, 501, 50), R.randint(2, 30)
        q, a, w = R.choice([("Si C′(%d) = %d, ¿qué significa?" % (x, k), "fabricar la unidad %d cuesta unos %d €" % (x + 1, k), ["fabricar %d unidades cuesta %d €" % (x, k), "el coste medio es %d €" % k, "el beneficio es %d €" % k]),
                            ("Si B′(%d) = −%d, ¿qué significa?" % (x, k), "al vender una unidad más, el beneficio baja unos %d €" % k, ["se pierden %d € en total" % k, "el beneficio es negativo", "al vender una unidad más, el beneficio sube unos %d €" % k]),
                            ("Si P′(t) &gt; 0 para todo t (población), ¿qué ocurre?", "la población crece siempre", ["la población decrece", "la población es constante", "la población es positiva"])])
        return M(q, a, w, "La derivada mide cuánto cambia la función por cada unidad más: <b>%s</b>." % a)
    a, b = R.randint(1, 5), R.randrange(20, 201, 10)
    x0 = b / (2 * a)
    if x0 != int(x0):
        return None
    x0 = int(x0)
    ok = "crece hasta x = %d y luego decrece" % x0
    return M("El beneficio de una empresa es B(x) = −%sx² + %dx (miles de euros). ¿Cómo se comporta según su derivada?" % ("" if a == 1 else a, b), ok,
             ["decrece hasta x = %d y luego crece" % x0, "crece siempre", "crece hasta x = %d y luego decrece" % b],
             "B′(x) = −%dx + %d es positiva si x &lt; %d y negativa si x &gt; %d: <b>%s</b>." % (2 * a, b, x0, x0, ok))


seen = set()
sets = [("Tasa de variación y derivada en un punto", mix(R, seen, [(s_tvm, 20)])), ("Reglas de derivación", mix(R, seen, [(s_reglas, 10), (s_prod, 10)])), ("Regla de la cadena", mix(R, seen, [(s_cadena, 20)])),
        ("Recta tangente y crecimiento", mix(R, seen, [(s_tangente, 12), (s_monotonia, 8)])), ("Derivadas en economía", mix(R, seen, [(s_marginal, 20)]))]
think = ["La <b>tasa de variación media</b> entre a y b es (f(b) − f(a))/(b − a): cuánto cambia f, por término medio, por cada unidad de x.",
         "La <b>derivada</b> f′(a) es la tasa de variación instantánea: la pendiente de la recta tangente en x = a.",
         "Reglas: (x<sup>n</sup>)′ = nx<sup>n−1</sup>; (f · g)′ = f′g + fg′; (f/g)′ = (f′g − fg′)/g²; cadena: (f(g(x)))′ = f′(g(x)) · g′(x).",
         "En economía, C′(x) es el <b>coste marginal</b>: lo que cuesta, aproximadamente, producir una unidad más. Si f′ &gt; 0, f crece; si f′ &lt; 0, decrece."]
ex = [("C(x) = 0,02x² + 5x + 800; coste marginal en x = 100", ["C′(x) = 0,04x + 5", "C′(100) = 4 + 5"], "9 € por unidad")]
mist = [["Confundir TVM con la derivada", "La TVM usa dos puntos; la derivada, uno."], ["Dar C(100) en lugar de C′(100)", "El coste marginal es la derivada."], ["Olvidar la derivada interior", "((3x + 1)⁴)′ = 4(3x + 1)³ · 3."]]
body = L(think, ex, mist, kurve([(lambda x: -0.5 * x * x + 6 * x, BLUE, "B(x)"), (lambda x: 18, RED, "")], (0, 12, 2), (0, 20, 4), W=330, H=240, label="beneficio: la tangente es horizontal en el máximo"))
faq = [("¿Qué es el coste marginal?", "La derivada del coste, C′(x). Indica cuánto aumenta aproximadamente el coste al producir una unidad más."),
       ("¿Qué diferencia hay entre la tasa de variación media y la derivada?", "La TVM mide el cambio medio en un intervalo; la derivada, el cambio instantáneo en un punto (la pendiente de la tangente).")]
unit(1, R, "derivadas", "M", "Derivadas: tasa de variación media, derivada en un punto, reglas de derivación, recta tangente, crecimiento e interpretación económica (coste e ingreso marginal)",
     "Derivadas", "Derivadas", "Fichas de Matemáticas Aplicadas a las Ciencias Sociales I: tasa de variación, reglas de derivación, recta tangente y coste marginal. 100 ejercicios con soluciones.",
     "C′(x): coste de una unidad más", "TVM: dos puntos; derivada: uno.", body, faq, sets, 7)
