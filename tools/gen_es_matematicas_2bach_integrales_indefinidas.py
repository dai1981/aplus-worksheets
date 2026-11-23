# -*- coding: utf-8 -*-
"""
España Matemáticas II (2.º de Bachillerato): Integrales indefinidas (Sentido algebraico)
Primitivas inmediatas (potencias, exponenciales, 1/x, trigonométricas), linealidad, integrales casi inmediatas (regla de la cadena al revés), cambio de variable,
integración por partes, racionales sencillas, primitiva que pasa por un punto.
Errores: olvidar la constante C, ∫ xⁿ dx con n = −1, no compensar la derivada de dentro, ∫ f · g = ∫ f · ∫ g.
"""
import random
from fractions import Fraction as F
from es_bach import M, mix, sg, num, unit, L, E, poly, nf, fq, W, MINUS, sup, par

R = random.Random(52010)
I = "∫ "


def term(c, n):
    """c·xⁿ con c Fraction"""
    c = F(c)
    if c == 0:
        return ""
    xs = "x" if n == 1 else ("" if n == 0 else "x%s" % sup(n))
    if c.denominator > 1:
        return "%s%s%s" % (MINUS if c < 0 else "", fq(abs(c)), xs)
    if xs and abs(c) == 1:
        return (MINUS if c < 0 else "") + xs
    return sg(int(c)) + xs


def suma(ts):
    out = ""
    for t_ in ts:
        if not t_:
            continue
        if not out:
            out = t_
        elif t_.startswith(MINUS):
            out += " − " + t_[1:]
        else:
            out += " + " + t_
    return out or "0"


def s_inmediatas():
    t = R.choice(["poli", "poli", "pot", "raiz", "exp", "inv", "trig"])
    if t == "poli":
        cs = [(R.choice([1, 2, 3, 4, 6]) * R.choice([1, -1]), n) for n in (3, 2, 1, 0)][R.randint(0, 1):]
        cs = [(c, n) for c, n in cs if c]
        f = suma([term(c, n) for c, n in cs])
        Fp = suma([term(F(c, n + 1), n + 1) for c, n in cs])
        wrong1 = suma([term(c * n, n - 1) for c, n in cs if n])
        wrong2 = suma([term(c, n + 1) for c, n in cs])
        wrong3 = suma([term(F(c, n + 1), n + 1) for c, n in cs[:-1]] + [term(cs[-1][0], cs[-1][1])])
        return M("Calcula %s(%s) dx." % (I, f), Fp + " + C", W([wrong1 + " + C", wrong2 + " + C", Fp, wrong3 + " + C"]), "∫ xⁿ dx = xⁿ⁺¹/(n + 1) + C, término a término: <b>%s + C</b>." % Fp)
    if t == "pot":
        n = R.randint(2, 4)
        k = R.randint(1, 6)
        ok = "%s/x%s + C" % (sg(-F(k, n - 1)) if F(k, n - 1).denominator == 1 else MINUS + fq(F(k, n - 1)), sup(n - 1) if n > 2 else "")
        return M("Calcula %s%d/x%s dx." % (I, k, sup(n)), ok, W(["%s/x%s + C" % (sg(F(k, n + 1)) if F(k, n + 1).denominator == 1 else fq(F(k, n + 1)), sup(n + 1)), "%d ln x%s + C" % (k, sup(n)), "%s/x%s + C" % (sg(-k * n), sup(n + 1))]),
                 "%d/x%s = %dx<sup>−%d</sup> → %dx<sup>−%d</sup>/(−%d) = <b>%s</b>." % (k, sup(n), k, n, k, n - 1, n - 1, ok))
    if t == "raiz":
        k = R.choice([3, 6, 9, 1, 2])
        c = F(2 * k, 3)
        ok = "%sx√x + C" % (nf(c) if c != 1 else "")
        return M("Calcula %s%s√x dx." % (I, "" if k == 1 else k), ok, W(["%s/√x + C" % nf(F(k, 2)), "%sx√x + C" % nf(F(3 * k, 2)), "%s√x + C" % nf(F(k, 2)) if k > 1 else "√x/2 + C"]), "√x = x<sup>1/2</sup> → x<sup>3/2</sup>/(3/2) = (2/3)x√x: <b>%s</b>." % ok)
    if t == "exp":
        k = R.randint(2, 6)
        return M("Calcula %s%de<sup>x</sup> dx." % (I, k), "%de<sup>x</sup> + C" % k, ["%de<sup>x + 1</sup>/(x + 1) + C" % k, "%dxe<sup>x</sup> + C" % k, "e<sup>x</sup> + C"], "∫ eˣ dx = eˣ + C: <b>%de<sup>x</sup> + C</b>." % k)
    if t == "inv":
        k = R.randint(2, 9)
        return M("Calcula %s%d/x dx." % (I, k), "%d ln |x| + C" % k, ["%d/x² + C" % k, "%sx<sup>0</sup> + C" % k, "ln |%dx| + C" % k if False else "%dx ln x + C" % k], "∫ 1/x dx = ln |x| + C (la regla de las potencias no vale para n = −1): <b>%d ln |x| + C</b>." % k)
    k = R.randint(2, 6)
    q, a, w = R.choice([("%d cos x" % k, "%d sen x + C" % k, ["%s sen x + C" % sg(-k), "%d cos x + C" % k, "%d tg x + C" % k]), ("%d sen x" % k, "%s cos x + C" % sg(-k), ["%d cos x + C" % k, "%s sen x + C" % sg(-k), "%d sen x + C" % k]),
                         ("1/cos² x", "tg x + C", ["−1/sen x + C", "sen x / cos x²", "ln |cos x| + C"]), ("1/(1 + x²)", "arctg x + C", ["ln (1 + x²) + C", "1/(2x) + C", "x + x³/3 + C"])])
    return M("Calcula %s%s dx." % (I, q), a, w, "Integral inmediata: <b>%s</b>." % a)


def s_cadena():
    t = R.choice(["exp", "lin", "lnu", "potu", "sen", "x_exp"])
    a, b = R.randint(2, 6), R.randint(-5, 5)
    inner = E((a, "x"), (b, ""))
    if t == "exp":
        return M("Calcula %se<sup>%s</sup> dx." % (I, inner), "(1/%d)e<sup>%s</sup> + C" % (a, inner), ["%de<sup>%s</sup> + C" % (a, inner), "e<sup>%s</sup> + C" % inner, "e<sup>%s</sup>/(%s) + C" % (inner, inner)], "Falta la derivada de dentro (%d): se divide entre %d. <b>(1/%d)e<sup>%s</sup> + C</b>." % (a, a, a, inner))
    if t == "lin":
        n = R.randint(2, 5)
        ok = "(%s)%s/%d + C" % (inner, sup(n + 1), a * (n + 1))
        return M("Calcula %s(%s)%s dx." % (I, inner, sup(n)), ok, W(["(%s)%s/%d + C" % (inner, sup(n + 1), n + 1), "%d(%s)%s + C" % (n * a, inner, sup(n - 1) if n > 2 else ""), "(%s)%s/%d + C" % (inner, sup(n + 1), a)]), "u = %s, du = %d dx: u%s/(%d · %d) = <b>%s</b>." % (inner, a, sup(n + 1), n + 1, a, ok))
    if t == "lnu":
        ok = "(1/%d) ln |%s| + C" % (a, inner)
        return M("Calcula %s1/(%s) dx." % (I, inner), ok, ["ln |%s| + C" % inner, "%d ln |%s| + C" % (a, inner), "−1/(%s)² + C" % inner], "∫ u′/u = ln |u|; aquí u′ = %d, así que dividimos entre %d: <b>%s</b>." % (a, a, ok))
    if t == "potu":
        k = R.randint(1, 9)
        ok = "ln (x² + %d) + C" % k
        return M("Calcula %s2x/(x² + %d) dx." % (I, k), ok, ["2 ln (x² + %d) + C" % k, "x²/(x²/2 + %dx) + C" % k, "1/(x² + %d) + C" % k], "El numerador es la derivada del denominador: ∫ u′/u = <b>%s</b>." % ok)
    if t == "sen":
        k = R.choice(["sen", "cos"])
        ok = ("−(1/%d) cos (%s) + C" % (a, inner)) if k == "sen" else ("(1/%d) sen (%s) + C" % (a, inner))
        return M("Calcula %s%s (%s) dx." % (I, k, inner), ok, W(["−%d cos (%s) + C" % (a, inner) if k == "sen" else "%d sen (%s) + C" % (a, inner), "(1/%d) cos (%s) + C" % (a, inner) if k == "sen" else "−(1/%d) sen (%s) + C" % (a, inner), "cos (%s) + C" % inner if k == "sen" else "sen (%s) + C" % inner]), "Dividimos entre la derivada de dentro (%d): <b>%s</b>." % (a, ok))
    k = R.randint(1, 5)
    ok = "(1/2)e<sup>x²</sup> + C" if k == 1 else "(%s)e<sup>x²</sup> + C" % nf(F(k, 2))
    return M("Calcula %s%sx · e<sup>x²</sup> dx." % (I, "" if k == 1 else k), ok, ["%se<sup>x²</sup> + C" % ("" if k == 1 else k), "%dx² e<sup>x²</sup> + C" % k if k > 1 else "x² e<sup>x²</sup> + C", "e<sup>x³/3</sup> + C"], "u = x², du = 2x dx: <b>%s</b>." % ok)


def s_partes():
    t = R.choice(["xe", "xe", "xln", "xsen", "ln", "xcos", "xa", "xa", "xa", "kxln"])
    if t == "xa":
        a = R.choice([x for x in range(-5, 6) if x not in (0, 1)])
        xa_ = E((1, "x"), (a, ""))
        ok = "e<sup>x</sup>(%s) + C" % E((1, "x"), (a - 1, "")) if a != 1 else "x e<sup>x</sup> + C"
        return M("Calcula %s(%s) · e<sup>x</sup> dx (por partes)." % (I, xa_), ok, W(["e<sup>x</sup>(%s) + C" % E((1, "x"), (a + 1, "")), "(%s) · e<sup>x</sup> + C" % xa_, "e<sup>x</sup>(%s) + C" % E((1, "x"), (1 - a, "")) if 1 - a != a - 1 else "e<sup>x</sup> + C"]),
                 "u = %s, dv = eˣ dx: (%s)eˣ − ∫ eˣ dx = <b>%s</b>." % (xa_, xa_, ok))
    if t == "kxln":
        k = R.randint(2, 6)
        ok = "%s ln x − %s + C" % (term(F(k, 2), 2), term(F(k, 4), 2))
        return M("Calcula %s%dx · ln x dx (por partes)." % (I, k), ok, W(["%s ln x + C" % term(F(k, 2), 2), "%d ln x + %d + C" % (k, k), "%dx ln x − %dx + C" % (k, k)]), "u = ln x, dv = %dx dx: <b>%s</b>." % (k, ok))
    k = R.randint(1, 4)
    q, a, w = {"xe": ("x · e<sup>%sx</sup>" % ("" if k == 1 else k), "e<sup>%sx</sup>(x/%s − 1/%s) + C" % ("" if k == 1 else k, k, k * k) if k > 1 else "e<sup>x</sup>(x − 1) + C", ["x · e<sup>x</sup> + C" if k == 1 else "x · e<sup>%dx</sup>/%d + C" % (k, k), "e<sup>%sx</sup>(x + 1) + C" % ("" if k == 1 else k), "(x²/2)e<sup>%sx</sup> + C" % ("" if k == 1 else k)]),
               "xln": ("x · ln x", "(x²/2) ln x − x²/4 + C", ["(x²/2) ln x + C", "ln x + 1 + C", "x ln x − x + C"]), "ln": ("ln x", "x ln x − x + C", ["1/x + C", "x ln x + C", "(ln x)²/2 + C"]),
               "xsen": ("x · sen x", "−x cos x + sen x + C", ["x cos x + C", "−x cos x − sen x + C", "(x²/2) sen x + C"]), "xcos": ("x · cos x", "x sen x + cos x + C", ["x sen x − cos x + C", "−x sen x + C", "(x²/2) cos x + C"])}[t]
    return M("Calcula %s%s dx (por partes)." % (I, q), a, W(w), "∫ u dv = uv − ∫ v du, eligiendo u la parte que se simplifica al derivar: <b>%s</b>." % a)


def s_racionales():
    t = R.choice(["div", "simples", "simples"])
    if t == "div":
        a = R.randint(1, 5)
        b = R.randint(1, 6)
        # (x + a + b)/(x + a) = 1 + b/(x + a)
        ok = "x + %d ln |x + %d| + C" % (b, a)
        return M("Calcula %s(x + %d)/(x + %d) dx." % (I, a + b, a), ok, ["x + ln |x + %d| + C" % a, "%d ln |x + %d| + C" % (b, a), "ln |x + %d| + C" % (a + b)], "Dividimos: 1 + %d/(x + %d). <b>%s</b>." % (b, a, ok))
    r1, r2_ = sorted(R.sample(range(-5, 6), 2))
    A_, B_ = R.sample(range(1, 5), 2)
    # A/(x − r1) + B/(x − r2)
    num_ = E((A_ + B_, "x"), (-(A_ * r2_ + B_ * r1), ""))
    den = poly([1, -(r1 + r2_), r1 * r2_])
    xa = lambda r: "x" if r == 0 else ("x − %d" % r if r > 0 else "x + %d" % -r)
    ok = "%s ln |%s| + %s ln |%s| + C" % ("" if A_ == 1 else A_, xa(r1), "" if B_ == 1 else B_, xa(r2_))
    return M("Calcula %s(%s)/(%s) dx." % (I, num_, den), ok, W(["%s ln |%s| + %s ln |%s| + C" % ("" if B_ == 1 else B_, xa(r1), "" if A_ == 1 else A_, xa(r2_)), "ln |%s| + C" % den, "%s ln |%s| − %s ln |%s| + C" % ("" if A_ == 1 else A_, xa(r1), "" if B_ == 1 else B_, xa(r2_))]),
             "Descomponemos en fracciones simples: %d/(%s) + %d/(%s). <b>%s</b>." % (A_, xa(r1), B_, xa(r2_), ok))


def s_primitiva():
    t = R.choice(["punto", "punto", "teo"])
    if t == "punto":
        a, b = R.choice([1, 2, 3]), R.randint(-5, 5)
        x0 = R.randint(-2, 3)
        y0 = R.randint(-6, 6)
        # f = 2a x + b → F = a x² + b x + C ; F(x0) = y0
        C = y0 - a * x0 * x0 - b * x0
        f = E((2 * a, "x"), (b, ""))
        ok = "F(x) = %s" % poly([a, b, C])
        return M("Halla la primitiva de f(x) = %s que pasa por el punto (%s, %s)." % (f, sg(x0), sg(y0)), ok, W(["F(x) = %s" % poly([a, b, y0]), "F(x) = %s" % poly([2 * a, b, C]), "F(x) = %s" % poly([a, b, -C]) if C else "F(x) = %s" % poly([a, b, 1])]),
                 "F(x) = %s + C y F(%s) = %s → C = %s. <b>%s</b>." % (poly([a, b, 0]), sg(x0), sg(y0), sg(C), ok))
    q, a, w = R.choice([("Si F es una primitiva de f, ¿qué cumple?", "F′(x) = f(x)", ["f′(x) = F(x)", "F(x) = f(x) + 1", "F(x) · f(x) = 1"]), ("¿Cuántas primitivas tiene una función continua?", "infinitas (se diferencian en una constante)", ["una", "dos", "ninguna"]),
                        ("¿Es cierto que ∫ f · g dx = ∫ f dx · ∫ g dx?", "no, para productos se usa por partes o cambio de variable", ["sí, siempre", "solo si son polinomios", "sí, si f = g"]), ("¿Por qué se escribe + C?", "porque la derivada de una constante es 0", ["porque es obligatorio", "para indicar el área", "porque C = 1"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


seen = set()
sets = [("Integrales inmediatas", mix(R, seen, [(s_inmediatas, 20)])), ("Casi inmediatas y cambio de variable", mix(R, seen, [(s_cadena, 20)])), ("Integración por partes", mix(R, seen, [(s_partes, 12), (s_primitiva, 8)])),
        ("Integrales racionales", mix(R, seen, [(s_racionales, 12), (s_cadena, 8)])), ("Primitivas con condiciones", mix(R, seen, [(s_primitiva, 8), (s_inmediatas, 6), (s_partes, 6)]))]
think = ["Una <b>primitiva</b> de f es una función F con F′ = f. La integral indefinida es ∫ f(x) dx = F(x) + C.",
         "Inmediatas: ∫ xⁿ dx = xⁿ⁺¹/(n + 1) + C (n ≠ −1); ∫ 1/x dx = ln |x| + C; ∫ eˣ dx = eˣ + C; ∫ cos x dx = sen x + C; ∫ sen x dx = −cos x + C.",
         "<b>Casi inmediatas</b>: si aparece la derivada de lo de dentro, ∫ f(u) u′ dx = F(u) + C (se ajustan las constantes).",
         "<b>Por partes</b>: ∫ u dv = u · v − ∫ v du. <b>Racionales</b>: se descomponen en fracciones simples."]
ex = [("∫ x eˣ dx", ["u = x, dv = eˣ dx", "x eˣ − ∫ eˣ dx"], "eˣ(x − 1) + C"), ("∫ 2x/(x² + 1) dx", ["u′/u"], "ln (x² + 1) + C")]
mist = [["Olvidar + C", "Toda primitiva lleva su constante."], ["Usar xⁿ⁺¹/(n + 1) con n = −1", "∫ 1/x dx = ln |x| + C."], ["No compensar la derivada de dentro", "∫ e<sup>3x</sup> dx = (1/3)e<sup>3x</sup> + C."]]
body = L(think, ex, mist)
faq = [("¿Cómo sé qué método usar?", "Primero mira si es inmediata o si aparece la derivada de lo de dentro; si es un producto de tipos distintos (x · eˣ), por partes; si es un cociente de polinomios, fracciones simples."),
       ("¿Cómo compruebo una integral?", "Derivando el resultado: debe salir la función de partida.")]
unit(2, R, "integrales-indefinidas", "A", "Primitivas: integrales inmediatas, casi inmediatas, cambio de variable, integración por partes e integrales racionales sencillas",
     "Integrales indefinidas", "Integrales indefinidas", "Fichas de Matemáticas II (2.º de Bachillerato): integrales inmediatas, cambio de variable, integración por partes, racionales y primitivas con condiciones. 100 ejercicios.",
     "∫ f(x) dx = F(x) + C, con F′ = f", "Comprueba derivando el resultado.", body, faq, sets, 10)
