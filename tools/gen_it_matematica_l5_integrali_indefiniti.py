# -*- coding: utf-8 -*-
"""
Italia Matematica quinta liceo: Integrali indefiniti (Relazioni e funzioni)
  python3 tools/gen_it_matematica_l5_integrali_indefiniti.py
Primitive e integrale indefinito, integrali immediati (potenze, esponenziali, funzioni goniometriche),
integrali del tipo f′/f e f′ · g(f) (sostituzione), integrazione per parti, funzioni razionali con denominatore
di secondo grado, primitiva che passa per un punto.
Errori: ∫xⁿ dx = xⁿ⁺¹ senza dividere, dimenticare + c, ∫1/x dx = ln x senza valore assoluto, segno di ∫sen x.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, W, fq, nz, FR, poly

R = random.Random(72510)
G = "quinta-liceo"
C = " + c"


def I(f):
    return "∫ %s dx" % f


def mono(c, n, v="x"):
    """c xⁿ con c razionale → testo"""
    if c == 0:
        return ""
    xs = v if n == 1 else ("%s<sup>%d</sup>" % (v, n) if n not in (2, 3) else v + ("²" if n == 2 else "³"))
    if n == 0:
        return fq(c)
    if c == 1:
        return xs
    if c == -1:
        return "−" + xs
    if c.denominator != 1 if isinstance(c, Fr) else False:
        sgn = "−" if c < 0 else ""
        return sgn + FR(str(abs(c.numerator)), str(c.denominator)) + " " + xs
    return "%s%s" % (fq(c), xs)


def psum(ts):
    out = ""
    for t in ts:
        if not t:
            continue
        if not out:
            out = t
        elif t.startswith("−"):
            out += " − " + t[1:]
        else:
            out += " + " + t
    return out or "0"


def s1_pot():
    n = R.randint(1, 4)
    m = R.randint(0, n - 1)
    a, b = nz(R, -6, 6), nz(R, -6, 6)
    k = R.randint(-5, 5) if m else 0
    f = psum([mono(Fr(a), n), mono(Fr(b), m), mono(Fr(k), 0) if k else ""])
    F = psum([mono(Fr(a, n + 1), n + 1), mono(Fr(b, m + 1), m + 1), mono(Fr(k), 1) if k else ""])
    w1 = psum([mono(Fr(a), n + 1), mono(Fr(b), m + 1), mono(Fr(k), 1) if k else ""])
    w2 = psum([mono(Fr(a * n), n - 1) if n > 1 else fq(a), mono(Fr(b * m), m - 1) if m > 1 else (fq(b * m) if m == 1 else "")])
    w3 = psum([mono(Fr(a, n), n + 1), mono(Fr(b, m) if m else Fr(b), m + 1), mono(Fr(k), 1) if k else ""])
    w4 = psum([mono(Fr(a, n + 1), n + 1), mono(Fr(b), m), mono(Fr(k), 0) if k else ""])
    w5 = psum([mono(Fr(-a, n + 1), n + 1), mono(Fr(b, m + 1), m + 1), mono(Fr(k), 1) if k else ""])
    return M("Calcola %s." % I(f if " " not in f else "(%s)" % f), F + C, [x + C for x in W(w1, w2, w3, w4, w5) if x != F][:3],
             "∫xⁿ dx = xⁿ⁺¹/(n + 1) + c, termine per termine: <b>%s + c</b>." % F)


IMM = [("cos x", "sen x", ["−sen x", "cos x", "−cos x"]), ("sen x", "−cos x", ["cos x", "sen x", "−sen x"]),
       ("e<sup>x</sup>", "e<sup>x</sup>", [FR("e<sup>x + 1</sup>", "x + 1"), "x e<sup>x</sup>", "e<sup>x − 1</sup>"]),
       (FR("1", "x"), "ln |x|", ["−" + FR("1", "x²"), "ln x²", FR("1", "x²")]),
       (FR("1", "cos² x"), "tg x", ["cotg x", FR("1", "cos x"), "−tg x"]),
       (FR("1", "1 + x²"), "arctg x", ["ln(1 + x²)", "arcsen x", FR("x", "1 + x²")]),
       (FR("1", "√(1 − x²)"), "arcsen x", ["arctg x", "√(1 − x²)", "arccos x"]),
       ("2<sup>x</sup>", FR("2<sup>x</sup>", "ln 2"), ["2<sup>x</sup> ln 2", FR("2<sup>x + 1</sup>", "x + 1"), "2<sup>x</sup>"]),
       ("√x", FR("2", "3") + " x√x", [FR("1", "2√x"), FR("3", "2") + " x√x", "x√x"]),
       (FR("1", "x²"), "−" + FR("1", "x"), [FR("1", "x"), "ln x²", "−" + FR("1", "x³")])]


def s2_imm():
    f, F, w = R.choice(IMM)
    return M("Calcola %s." % I(f), F + C, [x + C for x in w], "È un integrale immediato: <b>%s + c</b>." % F)


def s2_lin():
    k = R.choice([2, 3, 4, 5, -2, -3])
    kind = R.choice(["e", "cos", "sen", "inv"])
    kx = mono(Fr(k), 1)
    if kind == "e":
        f, F = "e<sup>%s</sup>" % kx, "%s e<sup>%s</sup>" % (coef(Fr(1, k)), kx)
        w = ["%s e<sup>%s</sup>" % (fq(k), kx), "e<sup>%s</sup>" % kx, "%s e<sup>%s</sup>" % (coef(Fr(1, k + 1)), poly([k, 1]))]
        e = "∫e<sup>kx</sup> dx = e<sup>kx</sup>/k + c con k = %s." % fq(k)
    elif kind == "cos":
        if k < 0:
            return None
        f, F = "cos(%s)" % kx, "%s sen(%s)" % (coef(Fr(1, k)), kx)
        w = ["%s sen(%s)" % (fq(k), kx), "sen(%s)" % kx, "−%s sen(%s)" % (coef(Fr(1, k)), kx)]
        e = "∫cos kx dx = (1/k) sen kx + c con k = %s." % fq(k)
    elif kind == "sen":
        if k < 0:
            return None
        f, F = "sen(%s)" % kx, "−%s cos(%s)" % (coef(Fr(1, k)), kx)
        w = ["%s cos(%s)" % (coef(Fr(1, k)), kx), "−%s cos(%s)" % (fq(k), kx), "−cos(%s)" % kx]
        e = "∫sen kx dx = −(1/k) cos kx + c con k = %s." % fq(k)
    else:
        b = nz(R, -6, 6)
        lin = poly([k, b])
        f, F = FR("1", lin), "%s ln |%s|" % (coef(Fr(1, k)), lin)
        w = ["ln |%s|" % lin, "%s ln |%s|" % (fq(k), lin), "−%s" % FR(fq(k), "(%s)²" % lin)]
        e = "∫1/(ax + b) dx = (1/a) ln |ax + b| + c con a = %s." % fq(k)
    return M("Calcola %s." % I(f), F + C, [x + C for x in w], e + " <b>%s + c</b>." % F)


def coef(c):
    """1/3 → '⅓' come frazione HTML, −1/2 → '−½'"""
    if c == 1:
        return ""
    if c == -1:
        return "−"
    s = "−" if c < 0 else ""
    c = abs(c)
    return s + (FR(str(c.numerator), str(c.denominator)) if c.denominator != 1 else str(c.numerator))


def s3_sost():
    kind = R.choice(["ln", "ln", "exp2", "pow", "sencos", "lnx"])
    a, b = R.randint(1, 5), R.randint(1, 9)
    if kind == "ln":
        g = poly([1, 0, b]) if R.random() < 0.5 else poly([1, a, b])
        gp = "2x" if "x²" in g and g.count("x") == 1 else poly([2, a])
        f = FR(gp, g)
        F = "ln(%s)" % g if g.count("x") == 1 else "ln |%s|" % g
        w = [FR("1", g), "ln |%s|" % gp, "%s ln |%s|" % (gp, g)]
        e = "Il numeratore è la derivata del denominatore: ∫f′/f dx = ln |f| + c."
    elif kind == "exp2":
        f = "2x e<sup>x²</sup>" if a % 2 else "x e<sup>x²</sup>"
        F = "e<sup>x²</sup>" if a % 2 else coef(Fr(1, 2)) + " e<sup>x²</sup>"
        w = ["x² e<sup>x²</sup>", "2 e<sup>x²</sup>", "e<sup>x³</sup>"] if a % 2 else ["2 e<sup>x²</sup>", "e<sup>x²</sup>", "x² e<sup>x²</sup>"]
        e = "Con t = x², dt = 2x dx: ∫e<sup>t</sup> dt%s." % ("" if a % 2 else " · ½")
    elif kind == "pow":
        n = R.randint(2, 5)
        f = "2x(x² + %d)<sup>%d</sup>" % (b, n)
        F = "%s(x² + %d)<sup>%d</sup>" % (coef(Fr(1, n + 1)), b, n + 1)
        w = ["(x² + %d)<sup>%d</sup>" % (b, n + 1), "%s(x² + %d)<sup>%d</sup>" % (coef(Fr(1, n)), b, n + 1), "x²(x² + %d)<sup>%d</sup>" % (b, n + 1)]
        e = "Con t = x² + %d, dt = 2x dx: ∫t<sup>%d</sup> dt = t<sup>%d</sup>/%d." % (b, n, n + 1, n + 1)
    elif kind == "sencos":
        n = R.randint(2, 5)
        f = "sen<sup>%d</sup> x cos x" % n
        F = "%s sen<sup>%d</sup> x" % (coef(Fr(1, n + 1)), n + 1)
        w = ["sen<sup>%d</sup> x" % (n + 1), "%s cos<sup>%d</sup> x" % (coef(Fr(1, n + 1)), n + 1), "−%s sen<sup>%d</sup> x" % (coef(Fr(1, n + 1)), n + 1)]
        e = "Con t = sen x, dt = cos x dx: ∫t<sup>%d</sup> dt." % n
    else:
        n = R.randint(1, 4)
        f = FR("ln<sup>%d</sup> x" % n if n > 1 else "ln x", "x")
        F = "%s ln<sup>%d</sup> x" % (coef(Fr(1, n + 1)), n + 1)
        w = ["ln<sup>%d</sup> x" % (n + 1), FR("1", "x²"), "%s ln<sup>%d</sup> x" % (coef(Fr(1, n)), n + 1) if n > 1 else "x ln x"]
        e = "Con t = ln x, dt = dx/x: ∫t<sup>%d</sup> dt = t<sup>%d</sup>/%d." % (n, n + 1, n + 1)
    return M("Calcola %s." % I(f), F + C, [x + C for x in w], e + " <b>%s + c</b>." % F)


def s4_parti():
    k = R.choice([1, 2, 3, -1])
    T = [("x e<sup>x</sup>", "(x − 1) e<sup>x</sup>", ["x e<sup>x</sup>", "(x + 1) e<sup>x</sup>", FR("x²", "2") + " e<sup>x</sup>"], "f = x, g′ = eˣ: x eˣ − ∫eˣ dx."),
         ("x cos x", "x sen x + cos x", ["x sen x − cos x", "−x sen x + cos x", FR("x²", "2") + " sen x"], "f = x, g′ = cos x: x sen x − ∫sen x dx."),
         ("x sen x", "−x cos x + sen x", ["x cos x + sen x", "−x cos x − sen x", FR("x²", "2") + " cos x"], "f = x, g′ = sen x: −x cos x + ∫cos x dx."),
         ("ln x", "x ln x − x", ["x ln x", FR("1", "x"), "x ln x + x"], "f = ln x, g′ = 1: x ln x − ∫x · (1/x) dx."),
         ("x ln x", FR("x²", "2") + " ln x − " + FR("x²", "4"), [FR("x²", "2") + " ln x", FR("x²", "2") + " ln x + " + FR("x²", "4"), "x ln x − x"], "f = ln x, g′ = x: (x²/2) ln x − ∫(x/2) dx."),
         ("x e<sup>−x</sup>", "−(x + 1) e<sup>−x</sup>", ["(x − 1) e<sup>−x</sup>", "−x e<sup>−x</sup>", "(x + 1) e<sup>−x</sup>"], "f = x, g′ = e<sup>−x</sup>: −x e<sup>−x</sup> + ∫e<sup>−x</sup> dx."),
         ("x² e<sup>x</sup>", "(x² − 2x + 2) e<sup>x</sup>", ["(x² + 2x + 2) e<sup>x</sup>", "(x² − 2x) e<sup>x</sup>", FR("x³", "3") + " e<sup>x</sup>"], "Due volte per parti: x² eˣ − 2∫x eˣ dx."),
         ("e<sup>x</sup> sen x", FR("e<sup>x</sup>(sen x − cos x)", "2"), [FR("e<sup>x</sup>(sen x + cos x)", "2"), "e<sup>x</sup> cos x", "e<sup>x</sup>(sen x − cos x)"], "Due volte per parti si ritrova l’integrale iniziale: 2I = eˣ(sen x − cos x)."),
         ("arctg x", "x arctg x − " + FR("1", "2") + " ln(1 + x²)", ["x arctg x", FR("1", "1 + x²"), "x arctg x + " + FR("1", "2") + " ln(1 + x²)"], "f = arctg x, g′ = 1: x arctg x − ∫x/(1 + x²) dx.")]
    f, F, w, e = R.choice(T)
    return M("Calcola per parti %s." % I(f), F + C, [x + C for x in w], "∫f g′ dx = f g − ∫f′ g dx. " + e + " <b>%s + c</b>." % F)


def s5_cond():
    a, b = nz(R, -3, 3), R.randint(-5, 5)
    x0 = R.randint(-2, 2)
    y0 = R.randint(-6, 6)
    # F(x) = a x² + b x + c con F(x0) = y0  (integrale di 2a x + b)
    c = y0 - a * x0 * x0 - b * x0
    F = lambda cc: poly([a, b, cc])
    return M("Trova la primitiva di f(x) = %s che passa per il punto (%s; %s)." % (poly([2 * a, b]), fq(x0), fq(y0)), "F(x) = %s" % F(c),
             ["F(x) = %s" % F(v) for v in W(y0, -c, c + 1, y0 + a * x0 * x0 + b * x0, c - 2, c + 3) if v != c][:3],
             "Le primitive sono %s; impongo F(%s) = %s: c = <b>%s</b>, quindi F(x) = %s." % (poly([a, b, 0]) + " + c", fq(x0), fq(y0), fq(c), F(c)))


def s5_raz():
    a, b = R.sample([-4, -3, -2, -1, 1, 2, 3, 4], 2)
    a, b = max(a, b), min(a, b)
    xm = lambda r: "x − %d" % r if r > 0 else "x + %d" % -r
    d = a - b
    f = FR("1", "(%s)(%s)" % (xm(a), xm(b)))
    lg = lambda c, t: ("%s ln |%s|" % (coef(c), t)).strip()
    F = lg(Fr(1, d), FR(xm(a), xm(b)))
    w = [lg(Fr(1, d), FR(xm(b), xm(a))), "ln |(%s)(%s)|" % (xm(a), xm(b)), lg(Fr(d) if d > 1 else Fr(2), FR(xm(a), xm(b)))]
    return M("Calcola %s." % I(f), F + C, [x + C for x in w],
             "Scompongo: 1/[(%s)(%s)] = A/(%s) + B/(%s) con A = 1/%d, B = −1/%d; integrando: <b>%s + c</b>." % (xm(a), xm(b), xm(a), xm(b), d, d, F))


def main():
    seen = set()
    sets = [
        ("Integrali di potenze e polinomi", mix(R, seen, [(s1_pot, 20)])),
        ("Integrali immediati", mix(R, seen, [(s2_imm, 10), (s2_lin, 10)])),
        ("Integrazione per sostituzione", mix(R, seen, [(s3_sost, 20)])),
        ("Integrazione per parti", mix(R, seen, [(s4_parti, 9), (s2_lin, 6), (s3_sost, 5)])),
        ("Primitive con condizione e funzioni razionali", mix(R, seen, [(s5_cond, 12), (s5_raz, 8)])),
    ]
    body = L(["F è una <b>primitiva</b> di f se F′(x) = f(x). L’<b>integrale indefinito</b> ∫f(x) dx è l’insieme di tutte le primitive: F(x) + c.",
              "Integrali immediati: ∫xⁿ dx = xⁿ⁺¹/(n + 1) + c (n ≠ −1), ∫1/x dx = ln |x| + c, ∫eˣ dx = eˣ + c, ∫cos x dx = sen x + c, ∫sen x dx = −cos x + c.",
              "<b>Sostituzione</b>: se nell’integrale compaiono g(x) e la sua derivata, pongo t = g(x). In particolare ∫f′/f dx = ln |f| + c.",
              "<b>Per parti</b>: ∫f g′ dx = f g − ∫f′ g dx. Si sceglie come f la funzione che si semplifica derivando (x, ln x, arctg x)."],
             [("∫(6x² − 4x) dx", ["6 · x³/3 − 4 · x²/2"], "2x³ − 2x² + c"),
              ("∫x eˣ dx", ["f = x, g′ = eˣ", "x eˣ − ∫eˣ dx"], "(x − 1) eˣ + c")],
             [["∫x³ dx = x⁴ + c", "Si divide per il nuovo esponente: x⁴/4 + c."],
              ["∫sen x dx = cos x + c", "La derivata di −cos x è sen x: il risultato è −cos x + c."],
              ["Dimenticare + c", "Le primitive sono infinite e differiscono per una costante."]])
    faq = [("Perché si scrive + c?", "Perché due primitive della stessa funzione differiscono per una costante: la derivata di una costante è 0."),
           ("Come scelgo il metodo?", "Prima prova gli integrali immediati; se compare una funzione insieme alla sua derivata usa la sostituzione; con prodotti come x eˣ, x sen x o ln x usa l’integrazione per parti.")]
    unit(G, R, "integrali-indefiniti", "F",
         "Concetto di primitiva e di integrale indefinito; integrali immediati, per sostituzione e per parti",
         "Integrali indefiniti", "Integrali indefiniti",
         "Schede di matematica per la quinta liceo sugli integrali indefiniti: primitive, integrali immediati di potenze, esponenziali e funzioni goniometriche, integrazione per sostituzione e per parti, funzioni razionali, primitiva per un punto. 100 esercizi con soluzioni.",
         "∫xⁿ dx = xⁿ⁺¹/(n + 1) + c", "Per parti: ∫f g′ dx = f g − ∫f′ g dx.",
         body, faq, sets, 10)


if __name__ == "__main__":
    main()
