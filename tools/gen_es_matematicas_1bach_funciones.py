# -*- coding: utf-8 -*-
"""
España Matemáticas I (1.º de Bachillerato): Funciones (Sentido algebraico)
Dominio (polinómicas, racionales, irracionales, logarítmicas), funciones elementales y sus gráficas, transformaciones (traslaciones y simetrías),
composición, función inversa, funciones definidas a trozos, simetrías.
Errores: (g ∘ f)(x) = g(f(x)), no f(g(x)); olvidar que en log el argumento debe ser positivo (no ≥ 0); f(x + 2) se traslada a la izquierda.
"""
import math
import random
from fractions import Fraction as F
from es_bach import M, mix, sg, num, unit, L, E, P2, nf, fq, kurve, BLUE, RED, W, MINUS

R = random.Random(51010)
INF, MINF = "+∞", MINUS + "∞"


def ivl(a, b, ca=False, cb=False):
    return "%s%s, %s%s" % ("[" if ca else "(", MINF if a is None else nf(a), INF if b is None else nf(b), "]" if cb else ")")


def xa(a):
    return "x" if a == 0 else ("x − %d" % a if a > 0 else "x + %d" % -a)


def s_dominio():
    t = R.choice(["rac", "rac2", "raiz", "raiz2", "log", "log2", "mix"])
    a = R.randint(-6, 6)
    b = R.choice([x for x in range(-6, 7) if x != a])
    if t == "rac":
        return M("¿Cuál es el dominio de f(x) = (x + 1)/(%s)?" % P2(1, -(a + b), a * b), "ℝ − {%s, %s}" % (sg(min(a, b)), sg(max(a, b))), W(["ℝ − {%s, %s}" % (sg(-max(a, b)), sg(-min(a, b))), "ℝ − {%s}" % sg(a * b) if a * b else "ℝ − {0}", "ℝ", "ℝ − {%s}" % sg(-1)]),
                 "Denominador = 0 → x = %s o x = %s: <b>ℝ − {%s, %s}</b>." % (sg(a), sg(b), sg(min(a, b)), sg(max(a, b))))
    if t == "rac2":
        k = R.randint(1, 9)
        return M("¿Cuál es el dominio de f(x) = 3/(x² + %d)?" % k, "ℝ", ["ℝ − {%s}" % sg(-k), "ℝ − {0}", "ℝ − {±%d}" % k], "x² + %d nunca es 0: <b>ℝ</b>." % k)
    if t == "raiz":
        return M("¿Cuál es el dominio de f(x) = √(%s)?" % xa(a), ivl(a, None, True), W([ivl(a, None), ivl(None, a, False, True), ivl(-a, None, True) if a else "ℝ"]), "%s ≥ 0 → <b>%s</b>." % (xa(a), ivl(a, None, True)))
    if t == "raiz2":
        r = R.randint(1, 6)
        ok = ivl(-r, r, True, True)
        return M("¿Cuál es el dominio de f(x) = √(%d − x²)?" % (r * r), ok, ["(%s, %s] ∪ [%s, %s)" % (MINF, sg(-r), sg(r), INF), ivl(-r, r), ivl(None, r * r, False, True)], "%d − x² ≥ 0 → −%d ≤ x ≤ %d: <b>%s</b>." % (r * r, r, r, ok))
    if t == "log":
        return M("¿Cuál es el dominio de f(x) = ln (%s)?" % xa(a), ivl(a, None), W([ivl(a, None, True), ivl(None, a), ivl(-a, None) if a else "ℝ", "ℝ"]), "El argumento del logaritmo debe ser positivo: %s &gt; 0 → <b>%s</b>." % (xa(a), ivl(a, None)))
    if t == "log2":
        r = R.randint(1, 5)
        ok = "(%s, %s) ∪ (%s, %s)" % (MINF, sg(-r), sg(r), INF)
        return M("¿Cuál es el dominio de f(x) = log (x² − %d)?" % (r * r), ok, [ivl(-r, r), "(%s, %s] ∪ [%s, %s)" % (MINF, sg(-r), sg(r), INF), ivl(r, None)], "x² − %d &gt; 0 → |x| &gt; %d: <b>%s</b>." % (r * r, r, ok))
    ok = ivl(a, b) if a < b else None
    if ok is None:
        return None
    return M("¿Cuál es el dominio de f(x) = √(%s) / (%s)?" % (xa(a), xa(b)) if False else "¿Cuál es el dominio de f(x) = ln (%s) + √(%s)?" % (xa(a), E((-1, "x"), (b, ""))), ivl(a, b, False, True), W([ivl(a, b, True, True), ivl(a, None), ivl(None, b, False, True), ivl(a, b)]),
             "%s &gt; 0 y %s ≥ 0 → %s &lt; x ≤ %s: <b>%s</b>." % (xa(a), E((-1, "x"), (b, "")), sg(a), sg(b), ivl(a, b, False, True)))


def s_composicion():
    a, b = R.randint(2, 5), R.randint(-5, 5)
    c = R.randint(-4, 4)
    f = "%s" % E((a, "x"), (b, ""))
    t = R.choice(["gof", "fog", "val", "val"])
    g_ = "x² %s" % (("+ %d" % c) if c > 0 else ("− %d" % -c) if c < 0 else "")
    g_ = g_.strip()
    gof = "(%s)² %s" % (f, (("+ %d" % c) if c > 0 else ("− %d" % -c) if c < 0 else "")) if True else ""
    gof = gof.strip()
    fog = "%d(%s) %s" % (a, g_, ("+ %d" % b) if b > 0 else ("− %d" % -b) if b < 0 else "")
    fog = E((a, "x²"), (a * c + b, ""))
    if t == "gof":
        return M("Si f(x) = %s y g(x) = %s, ¿cuál es (g ∘ f)(x)?" % (f, g_), gof, W([fog, "(%s)(%s)" % (f, g_), "%s %s" % (g_, ("+ " + f) if True else "")]), "(g ∘ f)(x) = g(f(x)): sustituimos x por %s en g. <b>%s</b>." % (f, gof))
    if t == "fog":
        return M("Si f(x) = %s y g(x) = %s, ¿cuál es (f ∘ g)(x)?" % (f, g_), fog, W([gof, E((a, "x²"), (b, "")), "(%s)(%s)" % (f, g_)]), "(f ∘ g)(x) = f(g(x)) = %d(%s) %s → <b>%s</b>." % (a, g_, ("+ %d" % b) if b > 0 else ("− %d" % -b) if b < 0 else "", fog))
    x0 = R.randint(-3, 3)
    fx = a * x0 + b
    gfx = fx * fx + c
    fgx = a * (x0 * x0 + c) + b
    k = R.choice(["gf", "fg"])
    v, o = (gfx, fgx) if k == "gf" else (fgx, gfx)
    return M("Si f(x) = %s y g(x) = %s, calcula (%s)(%s)." % (f, g_, "g ∘ f" if k == "gf" else "f ∘ g", sg(x0)), sg(v), W([sg(o) if o != v else sg(v + 1), sg(fx * (x0 * x0 + c)), sg(fx + x0 * x0 + c)]),
             "%s: <b>%s</b>." % ("f(%s) = %s y g(%s) = %s" % (sg(x0), sg(fx), sg(fx), sg(gfx)) if k == "gf" else "g(%s) = %s y f(%s) = %s" % (sg(x0), sg(x0 * x0 + c), sg(x0 * x0 + c), sg(fgx)), sg(v)))


def s_inversa():
    t = R.choice(["lin", "lin", "frac", "exp", "val"])
    a, b = R.randint(2, 6), R.randint(-8, 8)
    if t == "lin":
        ok = "f⁻¹(x) = (%s)/%d" % (E((1, "x"), (-b, "")), a) if b else "f⁻¹(x) = x/%d" % a
        return M("Halla la función inversa de f(x) = %s." % E((a, "x"), (b, "")), ok, W(["f⁻¹(x) = 1/(%s)" % E((a, "x"), (b, "")), "f⁻¹(x) = (%s)/%d" % (E((1, "x"), (b, "")), a) if b else "f⁻¹(x) = %dx" % a, "f⁻¹(x) = %s" % E((F(1, a), "x"), (-b, ""))]),
                 "y = %s → despejamos x y cambiamos los nombres: <b>%s</b>." % (E((a, "x"), (b, "")), ok))
    if t == "frac":
        ok = "f⁻¹(x) = %d/x %s %d" % (a, "+" if b >= 0 else "−", abs(b)) if b else "f⁻¹(x) = %d/x" % a
        return M("Halla la inversa de f(x) = %d/(%s)." % (a, xa(b)), ok, W(["f⁻¹(x) = (%s)/%d" % (xa(b), a), "f⁻¹(x) = %d/x %s %d" % (a, "−" if b >= 0 else "+", abs(b)) if b else "f⁻¹(x) = x/%d" % a, "f⁻¹(x) = %d/(x + %d)" % (a, a)]),
                 "y(x − %s) = %d → x = %d/y + %s → <b>%s</b>." % (sg(b), a, a, sg(b), ok))
    if t == "exp":
        k = R.choice(["e", "2", "10", "ln"])
        q, ok, w = {"e": ("e<sup>x</sup>", "ln x", ["1/e<sup>x</sup>", "log x", "e<sup>−x</sup>"]), "2": ("2<sup>x</sup>", "log<sub>2</sub> x", ["x/2", "√x", "x²"]),
                     "10": ("10<sup>x</sup>", "log x", ["ln x", "x/10", "1/10<sup>x</sup>"]), "ln": ("ln x", "e<sup>x</sup>", ["10<sup>x</sup>", "1/ln x", "x<sup>e</sup>"])}[k]
        return M("¿Cuál es la función inversa de f(x) = %s?" % q, "f⁻¹(x) = " + ok, ["f⁻¹(x) = " + x for x in w], "La exponencial y el logaritmo de la misma base son inversas: <b>%s</b>." % ok)
    x0 = R.randint(-4, 6)
    y0 = a * x0 + b
    return M("Si f(x) = %s, ¿cuánto vale f⁻¹(%s)?" % (E((a, "x"), (b, "")), sg(y0)), sg(x0), W([sg(a * y0 + b), nf(F(1, y0)) if y0 else "1", sg(x0 + 1), sg(y0)]), "f⁻¹(%s) es el x con f(x) = %s: %dx %s = %s → <b>x = %s</b>." % (sg(y0), sg(y0), a, ("+ %d" % b) if b >= 0 else ("− %d" % -b), sg(y0), sg(x0)))


BASE = [("x²", lambda x: x * x), ("√x", lambda x: math.sqrt(x) if x >= 0 else None), ("1/x", lambda x: 1 / x if abs(x) > 0.15 else None), ("|x|", abs), ("x³", lambda x: x ** 3)]


def s_transformacion():
    nm, f = R.choice(BASE)
    a, b = R.randint(-4, 4), R.randint(-3, 3)
    if a == 0 and b == 0:
        return None
    t = R.choice(["desc", "desc", "graf"])
    inner = nm.replace("x", "(%s)" % E((1, "x"), (-a, ""))) if a else nm
    expr = inner + ((" + %d" % b) if b > 0 else (" − %d" % -b) if b < 0 else "")
    def mov(a, b):
        p = []
        if a:
            p.append("%d unidad%s a la %s" % (abs(a), "es" if abs(a) > 1 else "", "derecha" if a > 0 else "izquierda"))
        if b:
            p.append("%d unidad%s hacia %s" % (abs(b), "es" if abs(b) > 1 else "", "arriba" if b > 0 else "abajo"))
        return " y ".join(p)
    ok = mov(a, b)
    if t == "desc":
        return M("¿Cómo se obtiene la gráfica de y = %s a partir de la de y = %s?" % (expr, nm), "se traslada " + ok, W(["se traslada " + mov(-a, b), "se traslada " + mov(a, -b), "se traslada " + mov(-a, -b), "se traslada " + mov(b, a) if a != b else "se refleja en el eje X"]),
                 "f(x − a) mueve a la derecha si a &gt; 0; sumar b mueve hacia arriba: <b>se traslada %s</b>." % ok)
    g = lambda x: (lambda v: None if v is None else v + b)(f(x - a))
    pic = kurve([(f, "#90a4ae", nm), (g, BLUE, "")], (-6, 6, 1), (-5, 5, 1), W=330, H=280, label="gráfica trasladada")
    opts = W([expr, (nm.replace("x", "(%s)" % E((1, "x"), (a, ""))) if a else nm) + ((" + %d" % b) if b > 0 else (" − %d" % -b) if b < 0 else ""), inner + ((" + %d" % -b) if -b > 0 else (" − %d" % b) if b > 0 else ""), (nm.replace("x", "(%s)" % E((1, "x"), (b, ""))) if b else nm) + ((" + %d" % a) if a > 0 else (" − %d" % -a) if a < 0 else "")])
    return M(pic + "La curva azul es la gris (y = %s) trasladada. ¿Cuál es su ecuación?" % nm, "y = " + expr, ["y = " + o for o in opts if o != expr], "Se ha movido %s: <b>y = %s</b>." % (ok, expr))


def s_trozos():
    t = R.choice(["val", "val", "cont", "sim"])
    a, b = R.randint(-3, 3), R.randint(1, 4)
    if t == "val":
        c = R.randint(-2, 3)
        f1 = E((b, "x"), (a, ""))
        f2 = "x² %s" % (("+ %d" % c) if c > 0 else ("− %d" % -c) if c < 0 else "")
        x0 = R.randint(-4, 4)
        v = b * x0 + a if x0 < 1 else x0 * x0 + c
        o = x0 * x0 + c if x0 < 1 else b * x0 + a
        return M("Si f(x) = %s si x &lt; 1 y f(x) = %s si x ≥ 1, ¿cuánto vale f(%s)?" % (f1, f2.strip(), sg(x0)), sg(v), W([sg(o) if o != v else sg(v + 1), sg(v + o), sg(-v) if v else "1"]), "%s %s 1, así que usamos %s: <b>%s</b>." % (sg(x0), "&lt;" if x0 < 1 else "≥", f1 if x0 < 1 else f2.strip(), sg(v)))
    if t == "cont":
        x0, c = R.randint(-2, 3), R.randint(-3, 3)
        k = x0 * x0 + c - b * x0
        f2 = "x² %s" % (("+ %d" % c) if c > 0 else ("− %d" % -c) if c < 0 else "")
        return M("¿Qué valor de k hace que f(x) = %dx + k si x &lt; %s y f(x) = %s si x ≥ %s no tenga saltos?" % (b, sg(x0), f2.strip(), sg(x0)), "k = %s" % sg(k), W(["k = %s" % sg(-k) if k else "k = 1", "k = %s" % sg(x0 * x0 + c), "k = %s" % sg(k + b)]),
                 "Los dos trozos deben valer lo mismo en x = %s: %s + k = %s → <b>k = %s</b>." % (sg(x0), sg(b * x0), sg(x0 * x0 + c), sg(k)))
    k = R.choice(["par", "impar", "ninguna"])
    f = {"par": R.choice(["x⁴ − 3x²", "cos x", "1/(x² + 1)", "|x| + 2", "e<sup>x²</sup>"]), "impar": R.choice(["x³ − x", "sen x", "1/x", "x/(x² + 1)", "x⁵"]), "ninguna": R.choice(["x² + x", "e<sup>x</sup>", "ln x", "x³ + 1", "(x − 1)²"])}[k]
    ok = {"par": "par (simétrica respecto al eje Y)", "impar": "impar (simétrica respecto al origen)", "ninguna": "ni par ni impar"}[k]
    return M("¿Qué simetría tiene f(x) = %s?" % f, ok, [o for o in ["par (simétrica respecto al eje Y)", "impar (simétrica respecto al origen)", "ni par ni impar", "simétrica respecto al eje X"] if o != ok], "Comparamos f(−x) con f(x) y con −f(x): <b>%s</b>." % ok)


def s_elementales():
    q, a, w = R.choice([("¿Qué función tiene como gráfica una parábola?", "f(x) = x² − 3x", ["f(x) = 2<sup>x</sup>", "f(x) = 1/x", "f(x) = √x"]),
                        ("¿Cuál es el recorrido de f(x) = e<sup>x</sup>?", "(0, +∞)", ["ℝ", "[0, +∞)", "(1, +∞)"]), ("¿Por qué punto pasan todas las funciones f(x) = a<sup>x</sup>?", "(0, 1)", ["(1, 0)", "(0, 0)", "(1, 1)"]),
                        ("¿Por qué punto pasan todas las funciones f(x) = log<sub>a</sub> x?", "(1, 0)", ["(0, 1)", "(0, 0)", "(a, 0)"]), ("¿Qué asíntota tiene f(x) = 1/(x − 2) + 3?", "x = 2 e y = 3", ["x = −2 e y = 3", "x = 3 e y = 2", "solo x = 2"]),
                        ("¿Cómo es f(x) = (1/2)<sup>x</sup>?", "decreciente", ["creciente", "constante", "periódica"]), ("¿Qué función es periódica?", "f(x) = sen x", ["f(x) = x²", "f(x) = e<sup>x</sup>", "f(x) = ln x"]),
                        ("¿Cuál es el vértice de f(x) = x² − 6x + 5?", "(3, −4)", ["(−3, 4)", "(3, 5)", "(6, 5)"]), ("¿Cuál es el dominio de f(x) = tg x?", "ℝ menos los múltiplos impares de π/2", ["ℝ", "[−1, 1]", "(0, +∞)"]),
                        ("¿Qué función crece más deprisa cuando x es muy grande?", "2<sup>x</sup>", ["x²", "x³", "100x"])])
    a, w = a.replace("−", MINUS), [x.replace("−", MINUS) for x in w]
    return M(q.replace("−", MINUS), a, w, "Respuesta: <b>%s</b>." % a)


seen = set()
sets = [("Dominio", mix(R, seen, [(s_dominio, 20)])), ("Funciones elementales y transformaciones", mix(R, seen, [(s_elementales, 8), (s_transformacion, 12)])), ("Composición de funciones", mix(R, seen, [(s_composicion, 20)])),
        ("Función inversa", mix(R, seen, [(s_inversa, 20)])), ("Funciones a trozos y simetrías", mix(R, seen, [(s_trozos, 20)]))]
think = ["El <b>dominio</b> son los x en los que se puede calcular f: denominador ≠ 0, radicando de índice par ≥ 0 y argumento del logaritmo &gt; 0.",
         "<b>Transformaciones</b>: f(x − a) traslada a la derecha (a &gt; 0); f(x) + b traslada hacia arriba; −f(x) refleja en el eje X.",
         "<b>Composición</b>: (g ∘ f)(x) = g(f(x)): primero f y después g.",
         "<b>Inversa</b>: se despeja x en y = f(x) y se cambian los nombres. Las gráficas de f y f⁻¹ son simétricas respecto a y = x."]
ex = [("Dominio de ln (x − 2)", ["x − 2 &gt; 0"], "(2, +∞)"), ("Inversa de f(x) = 3x − 6", ["y = 3x − 6 → x = (y + 6)/3"], "f⁻¹(x) = (x + 6)/3")]
mist = [["Confundir g ∘ f con f ∘ g", "g ∘ f: primero f."], ["Cerrar el intervalo en log", "El argumento debe ser &gt; 0."], ["f(x + 2) a la derecha", "Se mueve a la izquierda."]]
body = L(think, ex, mist, kurve([(lambda x: x * x, "#90a4ae", "y = x²"), (lambda x: (x - 2) ** 2 - 1, BLUE, "y = (x − 2)² − 1")], (-5, 5, 1), (-3, 6, 1), W=330, H=260, label="traslación de una parábola"))
faq = [("¿Todas las funciones tienen inversa?", "Solo las que son inyectivas (cada y viene de un único x). Por ejemplo, x² solo tiene inversa si nos quedamos con x ≥ 0."),
       ("¿Para qué sirve componer funciones?", "Para encadenar procesos: por ejemplo, el precio con IVA de un producto con descuento es una composición de dos funciones.")]
unit(1, R, "funciones", "A", "Funciones: dominio y recorrido, funciones elementales, transformaciones, composición, función inversa y funciones definidas a trozos",
     "Funciones", "Funciones", "Fichas de Matemáticas I (1.º de Bachillerato): dominio, funciones elementales, traslaciones, composición, función inversa, funciones a trozos y simetrías. 100 ejercicios.",
     "(g ∘ f)(x) = g(f(x))", "Primero se aplica f y después g.", body, faq, sets, 10)
