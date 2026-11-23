# -*- coding: utf-8 -*-
"""
Italia Matematica quinta liceo: Derivate (Relazioni e funzioni)
  python3 tools/gen_it_matematica_l5_derivate.py
Rapporto incrementale e definizione di derivata, derivate fondamentali, regole di derivazione (somma, prodotto,
quoziente), derivata della funzione composta, retta tangente, punti di non derivabilità, velocità come derivata.
Errori: D[xⁿ] = xⁿ⁻¹ senza n, (f·g)′ = f′·g′, dimenticare la derivata interna, segno sbagliato nel quoziente.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, W, fq, nz, FR, poly

R = random.Random(72506)
G = "quinta-liceo"


def dpoly(cs):
    n = len(cs) - 1
    return [c * (n - i) for i, c in enumerate(cs[:-1])]


def ev(cs, x):
    v = 0
    for c in cs:
        v = v * x + c
    return v


def s1_pot():
    n = R.randint(2, 5)
    cs = [nz(R, -6, 6)] + [R.choice([0, 0] + list(range(-7, 8))) for _ in range(n)]
    d = dpoly(cs)
    wrong1 = [c for c in cs[:-1]]                       # abbassa l’esponente senza moltiplicare
    wrong2 = d[:-1] + [d[-1] + cs[-1]] if cs[-1] else d[:-1] + [d[-1] + 1]  # tiene il termine noto
    wrong3 = [c * (n - i + 1) for i, c in enumerate(cs[:-1])]
    return M("Calcola la derivata di f(x) = %s." % poly(cs), "f′(x) = %s" % poly(d), ["f′(x) = %s" % poly(w) for w in W(wrong1, wrong2, wrong3, [-x for x in d]) if w != d][:3],
             "D[xⁿ] = n xⁿ⁻¹ e la derivata di una costante è 0: <b>f′(x) = %s</b>." % poly(d))


def s1_rad():
    T = [("√x", FR("1", "2√x"), [FR("1", "√x"), "2√x", FR("√x", "2")]),
         ("1/x", "−" + FR("1", "x²"), [FR("1", "x²"), "ln x", "−" + FR("1", "x")]),
         ("∛x", FR("1", "3∛(x²)"), [FR("1", "3∛x"), "3∛(x²)", FR("1", "∛(x²)")]),
         ("1/x²", "−" + FR("2", "x³"), [FR("2", "x³"), "−" + FR("1", "x³"), "−" + FR("2", "x")])]
    f, a, w = R.choice(T)
    return M("Calcola la derivata di f(x) = %s." % f, a, w, "Scrivo %s come potenza e uso D[x<sup>α</sup>] = α x<sup>α − 1</sup>: <b>%s</b>." % (f, a))


ELEM = [("sen x", "cos x", ["−cos x", "−sen x", "sen x"]), ("cos x", "−sen x", ["sen x", "cos x", "−cos x"]),
        ("e<sup>x</sup>", "e<sup>x</sup>", ["x e<sup>x − 1</sup>", "e<sup>x − 1</sup>", "1"]), ("ln x", FR("1", "x"), ["x", FR("1", "x²"), "e<sup>x</sup>"]),
        ("tg x", FR("1", "cos² x"), [FR("1", "sen² x"), "−" + FR("1", "cos² x"), "cotg x"]), ("2<sup>x</sup>", "2<sup>x</sup> ln 2", ["x · 2<sup>x − 1</sup>", "2<sup>x</sup>", FR("2<sup>x</sup>", "ln 2")]),
        ("arctg x", FR("1", "1 + x²"), [FR("1", "1 − x²"), "−" + FR("1", "1 + x²"), FR("x", "1 + x²")]), ("log<sub>2</sub> x", FR("1", "x ln 2"), [FR("1", "x"), FR("ln 2", "x"), FR("2", "x")])]


def cf(k, x):
    return x if k == 1 else ("−" + x if k == -1 else "%s %s%s" % (fq(k), "· " if x[0].isdigit() else "", x))


def s2_elem():
    f, a, w = R.choice(ELEM)
    k = R.choice([1, 1, 3, -2, 5, -4])
    if k == 1:
        return M("Calcola la derivata di f(x) = %s." % f, a, w, "È una derivata fondamentale: <b>%s</b>." % a)
    if "<span" in a:
        return None
    sg = lambda kk, x: cf(-kk, x[1:]) if x.startswith("−") else cf(kk, x)
    aa = sg(k, a)
    ww = [x for x in W(*([sg(k, x) for x in w] + [a])) if x != aa][:3]
    return M("Calcola la derivata di f(x) = %s." % cf(k, f), aa, ww, "La costante resta: D[k f] = k f′. <b>%s</b>." % aa)


def s2_prod():
    T = []
    a = nz(R, -4, 4)
    n = R.randint(2, 4)
    T.append(("x<sup>%d</sup> e<sup>x</sup>" % n if n > 1 else "x e<sup>x</sup>", "(x<sup>%d</sup> + %dx<sup>%d</sup>) e<sup>x</sup>" % (n, n, n - 1) if n > 2 else "(x² + 2x) e<sup>x</sup>",
              ["%dx<sup>%d</sup> e<sup>x</sup>" % (n, n - 1) if n > 2 else "2x e<sup>x</sup>", "x<sup>%d</sup> e<sup>x</sup>" % n if n > 2 else "x² e<sup>x</sup>", "(x<sup>%d</sup> − %dx<sup>%d</sup>) e<sup>x</sup>" % (n, n, n - 1) if n > 2 else "(x² − 2x) e<sup>x</sup>"],
              "Regola del prodotto: (fg)′ = f′g + fg′."))
    T.append(("x ln x", "ln x + 1", [FR("1", "x"), "ln x", "1 + " + FR("1", "x")], "(fg)′ = f′g + fg′ = 1 · ln x + x · 1/x."))
    T.append(("x sen x", "sen x + x cos x", ["cos x", "sen x − x cos x", "x cos x"], "(fg)′ = 1 · sen x + x cos x."))
    T.append(("x² cos x", "2x cos x − x² sen x", ["−2x sen x", "2x cos x + x² sen x", "2x sen x"], "(fg)′ = 2x cos x + x²(−sen x)."))
    T.append(("e<sup>x</sup> sen x", "e<sup>x</sup>(sen x + cos x)", ["e<sup>x</sup> cos x", "e<sup>x</sup>(sen x − cos x)", "e<sup>x</sup>(cos x − sen x)"], "(fg)′ = eˣ sen x + eˣ cos x."))
    T.append(("x² ln x", "2x ln x + x", ["2", "2x ln x", "2x + " + FR("1", "x")], "(fg)′ = 2x ln x + x² · 1/x."))
    b = R.randint(1, 5)
    T.append((FR("x", "x + %d" % b), FR(str(b), "(x + %d)²" % b), [FR("1", "x + %d" % b), FR("−%d" % b, "(x + %d)²" % b), FR("2x + %d" % b, "(x + %d)²" % b)],
              "Regola del quoziente: (f/g)′ = (f′g − fg′)/g² = (x + %d − x)/(x + %d)²." % (b, b)))
    T.append((FR("x + %d" % b, "x − %d" % b), FR("−%d" % (2 * b), "(x − %d)²" % b), [FR("%d" % (2 * b), "(x − %d)²" % b), "1", FR("−%d" % b, "(x − %d)²" % b)],
              "(f/g)′ = [(x − %d) − (x + %d)]/(x − %d)² = −%d/(x − %d)²." % (b, b, b, 2 * b, b)))
    T.append((FR("ln x", "x"), FR("1 − ln x", "x²"), [FR("ln x − 1", "x²"), FR("1", "x²"), FR("1 + ln x", "x²")], "(f/g)′ = (1/x · x − ln x · 1)/x² = (1 − ln x)/x²."))
    T.append((FR("e<sup>x</sup>", "x"), FR("e<sup>x</sup>(x − 1)", "x²"), [FR("e<sup>x</sup>(1 − x)", "x²"), "e<sup>x</sup>", FR("e<sup>x</sup>", "x²")], "(f/g)′ = (eˣ x − eˣ)/x²."))
    f, ans, w, e = R.choice(T)
    return M("Calcola la derivata di f(x) = %s." % f, ans, w, e + " <b>%s</b>." % ans)


def s3_comp():
    k = R.choice([2, 3, 4, 5, -2, -3])
    a, b = nz(R, -4, 5), R.randint(-6, 6)
    if a in (1, -1):
        a = 2
    lin = poly([a, b])
    kind = R.choice(["pow", "exp", "ln", "sen", "cos", "sqrt"])
    if kind == "pow":
        if b == 0:
            return None
        n = R.randint(2, 6)
        ans = "%d(%s)<sup>%d</sup>" % (n * a, lin, n - 1) if n > 2 else "%d(%s)" % (n * a, lin)
        ans = ans.replace("−", "−")
        w = ["%d(%s)<sup>%d</sup>" % (n, lin, n - 1) if n > 2 else "%d(%s)" % (n, lin), "%d(%s)<sup>%d</sup>" % (a, lin, n - 1) if n > 2 else "%d(%s)" % (a, lin),
             "%d(%s)<sup>%d</sup>" % (n * a, lin, n) ]
        f = "(%s)<sup>%d</sup>" % (lin, n)
        e = "Derivata della composta: %d(%s)<sup>%d</sup> · %s." % (n, lin, n - 1, fq(a))
        ans, w = ans.replace("-", "−"), [x.replace("-", "−") for x in w]
    elif kind == "exp":
        f = "e<sup>%s</sup>" % poly([k, 0])
        ans = "%s e<sup>%s</sup>" % (fq(k), poly([k, 0]))
        w = ["e<sup>%s</sup>" % poly([k, 0]), "%s e<sup>%s</sup>" % (fq(k), poly([k, -1])), "%s e<sup>x</sup>" % fq(k)]
        e = "D[e<sup>g(x)</sup>] = g′(x) e<sup>g(x)</sup> con g′ = %s." % fq(k)
    elif kind == "ln":
        f = "ln(%s)" % lin
        ans = FR(fq(a), lin)
        w = [FR("1", lin), FR(fq(a), "x"), fq(a) + " ln(%s)" % lin]
        e = "D[ln g(x)] = g′(x)/g(x) con g′ = %s." % fq(a)
    elif kind in ("sen", "cos") and k < 0:
        return None
    elif kind == "sen":
        f = "sen(%s)" % poly([k, 0])
        ans = "%s cos(%s)" % (fq(k), poly([k, 0]))
        w = ["cos(%s)" % poly([k, 0]), "%s cos(%s)" % (fq(-k), poly([k, 0])), "%s sen(%s)" % (fq(k), poly([k, 0]))]
        e = "D[sen g(x)] = g′(x) cos g(x) con g′ = %s." % fq(k)
    elif kind == "cos":
        f = "cos(%s)" % poly([k, 0])
        ans = "%s sen(%s)" % (fq(-k), poly([k, 0]))
        w = ["−sen(%s)" % poly([k, 0]), "%s sen(%s)" % (fq(k), poly([k, 0])), "%s cos(%s)" % (fq(-k), poly([k, 0]))]
        e = "D[cos g(x)] = −g′(x) sen g(x) con g′ = %s." % fq(k)
    else:
        if a < 0:
            return None
        f = "√(%s)" % lin
        ans = FR(fq(a), "2√(%s)" % lin)
        w = [FR("1", "2√(%s)" % lin), FR(fq(a), "√(%s)" % lin), "%s√(%s)" % (fq(a), lin)]
        e = "D[√g] = g′/(2√g) con g′ = %s." % fq(a)
    return M("Calcola la derivata di f(x) = %s." % f, ans, w, e + " <b>%s</b>." % ans)


def s4_val():
    n = R.randint(2, 3)
    cs = [nz(R, -3, 3)] + [R.randint(-5, 5) for _ in range(n)]
    x0 = R.randint(-2, 3)
    d = dpoly(cs)
    v = ev(d, x0)
    return M("f(x) = %s. Quanto vale f′(%s)?" % (poly(cs), fq(x0)), fq(v), [fq(x) for x in W(ev(cs, x0), ev(d, -x0), v + cs[-1] if cs[-1] else v + 2, v - 1) if x != v][:3],
             "f′(x) = %s, quindi f′(%s) = <b>%s</b>." % (poly(d), fq(x0), fq(v)))


def s4_tang():
    cs = [nz(R, -2, 3), R.randint(-5, 5), R.randint(-6, 6)]
    x0 = R.choice([-2, -1, 1, 2, 3])
    y0 = ev(cs, x0)
    m = ev(dpoly(cs), x0)
    q = y0 - m * x0
    yq = lambda mm, qq: "y = %s" % poly([mm, qq]) if mm else "y = %s" % fq(qq)
    ans = yq(m, q)
    return M("Scrivi la retta tangente al grafico di f(x) = %s nel punto di ascissa x = %s." % (poly(cs), fq(x0)), ans,
             [yq(*v) for v in W((m, y0), (y0, q), (m, y0 + m * x0), (-m, y0 + m * x0), (m + 1, q - x0), (cs[1], cs[2])) if v != (m, q)][:3],
             "f(%s) = %s e f′(%s) = %s; y − %s = %s(x − %s) dà <b>%s</b>." % (fq(x0), fq(y0), fq(x0), fq(m), "(%s)" % fq(y0) if y0 < 0 else fq(y0), fq(m) if m >= 0 else "(%s)" % fq(m), "(%s)" % fq(x0) if x0 < 0 else fq(x0), ans))


def s5_def():
    a = nz(R, -3, 3)
    b = R.randint(-5, 5)
    x0 = R.randint(-2, 3)
    T = R.choice(["ri", "lim"])
    h_ = R.choice([1, 2])
    if T == "ri":
        # rapporto incrementale di a x² + b x tra x0 e x0 + h
        f = lambda x: a * x * x + b * x
        r = Fr(f(x0 + h_) - f(x0), h_)
        return M("f(x) = %s. Calcola il rapporto incrementale di f tra x = %s e x = %s." % (poly([a, b, 0]), fq(x0), fq(x0 + h_)), fq(r),
                 [fq(x) for x in W(f(x0 + h_) - f(x0) if h_ == 2 else r + a, 2 * a * x0 + b, Fr(f(x0 + h_) + f(x0), h_), r + 1) if x != r][:3],
                 "[f(%s) − f(%s)]/%d = (%s − %s)/%d = <b>%s</b>." % (fq(x0 + h_), fq(x0), h_, fq(f(x0 + h_)), "(%s)" % fq(f(x0)) if f(x0) < 0 else fq(f(x0)), h_, fq(r)))
    v = 2 * a * x0 + b
    return M("f(x) = %s. Con la definizione, f′(%s) = lim<sub>h→0</sub> [f(%s + h) − f(%s)]/h. Quanto vale?" % (poly([a, b, 0]), fq(x0), fq(x0), fq(x0)), fq(v),
             [fq(x) for x in W(a * x0 * x0 + b * x0, 2 * a * x0, a * x0 + b, v + a, -v, v - a) if x != v][:3],
             "Il rapporto incrementale vale %s, che per h → 0 tende a <b>%s</b>." % (poly([a, v], "h"), fq(v)))


def s5_nd():
    T = [("f(x) = |x − {a}| in x = {a}", "punto angoloso", "Le derivate destra e sinistra valgono 1 e −1: sono finite ma diverse."),
         ("f(x) = ∛(x − {a}) in x = {a}", "flesso a tangente verticale", "La derivata 1/(3∛((x − {a})²)) tende a +∞ da entrambi i lati."),
         ("f(x) = √|x − {a}| in x = {a}", "cuspide", "Le derivate destra e sinistra tendono a +∞ e −∞."),
         ("f(x) = (x − {a})² in x = {a}", "la funzione è derivabile", "È un polinomio: f′({a}) = 0, tangente orizzontale."),
         ("f(x) = |x² − {a2}| in x = {r}", "punto angoloso", "Le derivate laterali valgono ±{d}: finite ma diverse.")]
    f, ans, e = R.choice(T)
    a = R.randint(1, 4)
    ff = f.format(a=a, a2=a * a, r=a)
    return M("Che tipo di punto è %s?" % ff, ans, [x for x in ["punto angoloso", "cuspide", "flesso a tangente verticale", "la funzione è derivabile"] if x != ans],
             e.format(a=a, d=2 * a) + " <b>%s</b>." % ans.capitalize())


def s5_vel():
    a, b, c = R.choice([1, 2, 3, 4, 5]), R.randint(1, 12), R.randint(0, 20)
    t0 = R.randint(1, 6)
    v = 2 * a * t0 + b
    ask = R.choice(["v", "acc"])
    s = poly([a, b, c], "t")
    if ask == "v":
        return M("Un corpo si muove secondo s(t) = %s (s in metri, t in secondi). Qual è la velocità all’istante t = %d s?" % (s, t0), "%d m/s" % v,
                 ["%d m/s" % x for x in W(a * t0 * t0 + b * t0 + c, a * t0 + b, v + c if c else v + 1, 2 * a + b, v + 2 * a) if x != v][:3],
                 "v(t) = s′(t) = %s, quindi v(%d) = <b>%d m/s</b>." % (poly([2 * a, b], "t"), t0, v))
    return M("Un corpo si muove secondo s(t) = %s (s in metri, t in secondi). Qual è l’accelerazione?" % s, "%d m/s²" % (2 * a),
             ["%d m/s²" % x for x in W(a, b, 2 * a + b, 0, 2 * a + 2 * b) if x != 2 * a][:3],
             "a(t) = s″(t): v(t) = %s e a(t) = <b>%d m/s²</b>." % (poly([2 * a, b], "t"), 2 * a))


def main():
    seen = set()
    sets = [
        ("Derivate delle potenze", mix(R, seen, [(s1_pot, 16), (s1_rad, 4)])),
        ("Derivate fondamentali, prodotto e quoziente", mix(R, seen, [(s2_elem, 8), (s2_prod, 12)])),
        ("Derivata della funzione composta", mix(R, seen, [(s3_comp, 20)])),
        ("Valore della derivata e retta tangente", mix(R, seen, [(s4_val, 8), (s4_tang, 12)])),
        ("Definizione, derivabilità e applicazioni", mix(R, seen, [(s5_def, 8), (s5_nd, 4), (s5_vel, 8)])),
    ]
    body = L(["La <b>derivata</b> f′(x<sub>0</sub>) è il limite del rapporto incrementale [f(x<sub>0</sub> + h) − f(x<sub>0</sub>)]/h per h → 0: è la pendenza della retta tangente al grafico.",
              "Derivate fondamentali: D[x<sup>n</sup>] = n x<sup>n − 1</sup>, D[eˣ] = eˣ, D[ln x] = 1/x, D[sen x] = cos x, D[cos x] = −sen x.",
              "Regole: (f + g)′ = f′ + g′; (fg)′ = f′g + fg′; (f/g)′ = (f′g − fg′)/g²; composta: [f(g(x))]′ = f′(g(x)) · g′(x).",
              "Retta tangente in x<sub>0</sub>: y − f(x<sub>0</sub>) = f′(x<sub>0</sub>)(x − x<sub>0</sub>). Se le derivate destra e sinistra sono diverse c’è un punto angoloso."],
             [("D[x³ − 4x² + 7]", ["3x² − 8x + 0"], "3x² − 8x"),
              ("D[e<sup>3x</sup>]", ["Derivata esterna e<sup>3x</sup>", "Derivata interna 3"], "3e<sup>3x</sup>")],
             [["D[x⁵] = x⁴", "Va moltiplicato per l’esponente: 5x⁴."],
              ["(fg)′ = f′g′", "La regola del prodotto è f′g + fg′."],
              ["D[sen 3x] = cos 3x", "Manca la derivata interna: 3 cos 3x."]])
    faq = [("Che cosa significa geometricamente la derivata?", "f′(x<sub>0</sub>) è il coefficiente angolare della retta tangente al grafico nel punto (x<sub>0</sub>; f(x<sub>0</sub>)). In fisica è la velocità istantanea se f è la posizione."),
           ("Una funzione continua è sempre derivabile?", "No: |x| è continua in 0 ma non derivabile (punto angoloso). Vale invece il contrario: una funzione derivabile è continua.")]
    unit(G, R, "derivate", "F",
         "Concetto di derivata, regole di derivazione, derivata della funzione composta e retta tangente",
         "Derivate", "Derivate",
         "Schede di matematica per la quinta liceo sulle derivate: derivate fondamentali, regole del prodotto e del quoziente, funzione composta, retta tangente, rapporto incrementale, punti di non derivabilità, velocità e accelerazione. 100 esercizi con soluzioni.",
         "f′(x₀) è la pendenza della retta tangente.", "Composta: f′(g(x)) · g′(x).",
         body, faq, sets, 6)


if __name__ == "__main__":
    main()
