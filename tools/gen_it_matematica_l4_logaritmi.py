# -*- coding: utf-8 -*-
"""
Italia Matematica quarta liceo: Logaritmi e funzione logaritmica (Relazioni e funzioni)
  python3 tools/gen_it_matematica_l4_logaritmi.py
Definizione di logaritmo, logaritmi decimali e naturali, proprietà (prodotto, quoziente, potenza), formula del cambiamento di base,
espressioni, funzione y = logₐ x (dominio, monotonia, punto (1; 0)), dominio di funzioni logaritmiche.
Errori: log(a + b) = log a + log b, log₂ 8 = 4, logaritmo di un numero negativo, log(x − 3) con dominio x > −3.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, d, nz, P2

R = random.Random(72402)
G = "quarta-liceo"


def lg(b, x):
    """log in base b di x (testo)"""
    if b == 10:
        return "log %s" % x
    if b == "e":
        return "ln %s" % x
    return "log<sub>%s</sub> %s" % (fq(b) if not isinstance(b, str) else b, x)


def arg(v):
    v = Fr(v)
    if v.denominator == 1:
        return d(v)
    try:
        return d(v) if b10(v) else fq(v)
    except ValueError:
        return fq(v)


def b10(v):
    t = v.denominator
    while t % 10 == 0:
        t //= 10
    return t == 1 and v.numerator == 1


def s1_def():
    b = R.choice([2, 3, 5, 10, 4, Fr(1, 2), 7])
    e = R.randint(-3, 5)
    if b == 10:
        e = R.randint(-4, 4)
    v = Fr(b) ** e
    if v.numerator > 100000 or e == 0:
        return None
    a = arg(v) if not (b == 10 and e < 0) else d(v)
    w = [Fr(-e), Fr(v, b) if (Fr(v, b)).denominator == 1 and Fr(v, b) < 50 else Fr(e + 1), Fr(e + 1) if e + 1 != -e else Fr(e - 1), Fr(1, e) if e not in (0,) and Fr(1, e) != e else Fr(e + 2)]
    return M("Calcola %s." % lg(b, a), fq(e), [fq(x) for x in W(*w) if x != e],
             "log<sub>a</sub> x = y significa a<sup>y</sup> = x: %s<sup>%s</sup> = %s, quindi <b>%s</b>." % (fq(b) if Fr(b).denominator == 1 else "(%s)" % fq(b), fq(e), a, fq(e)))


def s1_ln():
    k = R.choice(["ln", "exp", "zero", "base"])
    n = R.randint(2, 9)
    if k == "ln":
        return M("Calcola ln e<sup>%d</sup>." % n, str(n), ["e<sup>%d</sup>" % n, "1", str(n + 1)], "ln e<sup>%d</sup> = %d · ln e = <b>%d</b>." % (n, n, n))
    if k == "exp":
        return M("Calcola e<sup>ln %d</sup>." % n, str(n), ["ln %d" % n, "e", str(n * n)], "Esponenziale e logaritmo nella stessa base si annullano: <b>%d</b>." % n)
    if k == "zero":
        b = R.choice([2, 3, 5, 10, 7, "e"])
        return M("Quanto vale %s?" % lg(b, 1), "0", ["1", str(b) if b != "e" else "e", "non esiste"], "a<sup>0</sup> = 1 per ogni base: <b>0</b>.")
    b = R.choice([2, 3, 5, 7, 9])
    return M("Quanto vale %s?" % lg(b, b), "1", ["0", str(b), "%d" % (b * b)], "a<sup>1</sup> = a: <b>1</b>.")


def s2_prop():
    b = R.choice([2, 3, 5, 10, 6])
    k = R.choice(["somma", "diff", "pot"])
    if k == "somma":
        e = R.randint(2, 5)
        tot = b ** e
        x = R.choice([f for f in range(2, tot) if tot % f == 0 and f != b])
        y = tot // x
        q = "%s + %s" % (lg(b, x), lg(b, y))
        w = [Fr(x + y) if x + y < 30 else Fr(e + 1), Fr(e * e), Fr(e - 1)]
        e_ = "log<sub>a</sub> x + log<sub>a</sub> y = log<sub>a</sub>(xy) = %s = <b>%d</b>." % (lg(b, tot), e)
    elif k == "diff":
        e = R.randint(1, 4)
        y = R.randint(2, 9)
        x = y * b ** e
        q = "%s − %s" % (lg(b, x), lg(b, y))
        w = [Fr(e + 1), Fr(x - y) if x - y < 30 else Fr(e * 2), Fr(-e), Fr(e * 2), Fr(x, y) if x // y < 30 else None]
        e_ = "log<sub>a</sub> x − log<sub>a</sub> y = log<sub>a</sub>(x/y) = %s = <b>%d</b>." % (lg(b, b ** e), e)
    else:
        n = R.randint(2, 5)
        e = R.randint(2, 4)
        q = "%d · %s" % (n, lg(b, b ** e)) if R.random() < 0.5 else "%s" % lg(b, "%d<sup>%d</sup>" % (b ** e, n))
        w = [Fr(n + e), Fr(e), Fr(b ** e * n) if b ** e * n < 100 else Fr(n * e + 1)]
        e_ = "log<sub>a</sub> x<sup>n</sup> = n · log<sub>a</sub> x = %d · %d = <b>%d</b>." % (n, e, n * e)
        e = n * e
    return M("Calcola: %s" % q, str(e), [fq(x) for x in W(*w) if x != e], e_)


def s2_svil():
    k = R.choice(["a", "b"])
    a, b, c = R.sample(["x", "y", "z"], 3)
    n, m = R.randint(2, 4), R.randint(2, 3)
    if k == "a":
        q = "log (%s<sup>%d</sup>%s)" % (a, n, b)
        ans = "%d log %s + log %s" % (n, a, b)
        w = ["log %d%s + log %s" % (n, a, b), "%d log %s · log %s" % (n, a, b), "(log %s + log %s)<sup>%d</sup>" % (a, b, n)]
    else:
        q = "log (%s<sup>%d</sup> / %s<sup>%d</sup>)" % (a, n, b, m)
        ans = "%d log %s − %d log %s" % (n, a, m, b)
        w = ["%d log %s / %d log %s" % (n, a, m, b), "%d log %s + %d log %s" % (n, a, m, b), "log %s − log %s" % (a, b)]
    return M("Sviluppa con le proprietà dei logaritmi (x, y, z positivi): %s" % q, ans, w,
             "Prodotto → somma, quoziente → differenza, esponente → coefficiente: <b>%s</b>." % ans)


def s3_base():
    k = R.choice([(4, 8), (8, 4), (9, 27), (27, 9), (4, 32), (16, 8), (25, 125), (8, 16), (27, 3), (16, 2), (32, 4)])
    a, x = k
    import math
    p = 2 if a in (4, 8, 16, 32) else 3 if a in (9, 27) else 5
    ea = round(math.log(a, p))
    ex_ = round(math.log(x, p))
    v = Fr(ex_, ea)
    return M("Calcola %s con il cambiamento di base." % lg(a, x), fq(v), [fq(y) for y in W(Fr(ea, ex_), Fr(x, a), v + 1, Fr(ex_ - ea)) if y != v],
             "log<sub>%d</sub> %d = log<sub>%d</sub> %d / log<sub>%d</sub> %d = %d/%d = <b>%s</b>." % (a, x, p, x, p, a, ex_, ea, fq(v)))


def s4_dom():
    k = R.choice(["lin", "quad", "fraz", "neg"])
    a = R.randint(-6, 6)
    if k == "lin":
        f = "y = log (%s)" % P2(0, 1, -a)
        ans, w = "x &gt; %s" % fq(a), ["x &gt; %s" % fq(-a), "x ≥ %s" % fq(a), "ℝ"]
        e = "L’argomento deve essere positivo: %s &gt; 0 → <b>%s</b>." % (P2(0, 1, -a), ans)
    elif k == "neg":
        f = "y = ln (%s)" % P2(0, -1, a)
        ans, w = "x &lt; %s" % fq(a), W("x &gt; %s" % fq(a), "x &lt; %s" % fq(-a), "x ≤ %s" % fq(a), "x &gt; %s" % fq(-a), "ℝ")
        e = "%s &gt; 0 → <b>%s</b>." % (P2(0, -1, a), ans)
    elif k == "quad":
        c = R.randint(1, 6)
        f = "y = log<sub>2</sub> (%s)" % P2(1, 0, -c * c)
        ans, w = "x &lt; −%d ∨ x &gt; %d" % (c, c), W("x &gt; %d" % c, "−%d &lt; x &lt; %d" % (c, c), "x &gt; %d" % (c * c), "x ≠ %d" % c)
        e = "x² − %d &gt; 0: valori esterni, <b>%s</b>." % (c * c, ans)
    else:
        b = R.randint(-6, 6)
        if a == b:
            return None
        lo, hi = sorted([a, b])
        f = "y = log ((%s)/(%s))" % (P2(0, 1, -a), P2(0, 1, -b))
        ans, w = "x &lt; %s ∨ x &gt; %s" % (fq(lo), fq(hi)), ["%s &lt; x &lt; %s" % (fq(lo), fq(hi)), "x &gt; %s" % fq(hi), "x ≠ %s" % fq(b)]
        e = "Il quoziente deve essere positivo: valori esterni a %s e %s, <b>%s</b>." % (fq(lo), fq(hi), ans)
    return M("Qual è il dominio di %s?" % f, ans, w, e)


FL = [("y = log<sub>3</sub> x", "crescente"), ("y = log<sub>1/2</sub> x", "decrescente"), ("y = ln x", "crescente"), ("y = log<sub>0,2</sub> x", "decrescente"), ("y = log x", "crescente"), ("y = log<sub>2/3</sub> x", "decrescente")]


def s4_fun():
    f, m = R.choice(FL)
    k = R.choice(["m", "p", "seg"])
    if k == "m":
        return M("La funzione %s è…" % f, m, ["decrescente" if m == "crescente" else "crescente", "costante", "definita per ogni x reale"],
                 "y = log<sub>a</sub> x è crescente se a &gt; 1, decrescente se 0 &lt; a &lt; 1: <b>%s</b>." % m)
    if k == "p":
        return M("In quale punto il grafico di %s incontra l’asse x?" % f, "(1; 0)", ["(0; 1)", "(0; 0)", "non incontra l’asse x"],
                 "log<sub>a</sub> 1 = 0 per ogni base: <b>(1; 0)</b>. L’asse y (x = 0) è asintoto verticale.")
    ans = "0 &lt; x &lt; 1" if m == "crescente" else "x &gt; 1"
    return M("Per quali x la funzione %s è negativa?" % f, ans, ["x &gt; 1" if m == "crescente" else "0 &lt; x &lt; 1", "x &lt; 0", "x &lt; 1"],
             "Il grafico passa per (1; 0) ed è %s: è negativo per <b>%s</b>." % (m, ans))


def main():
    seen = set()
    sets = [
        ("Definizione di logaritmo", mix(R, seen, [(s1_def, 14), (s1_ln, 6)])),
        ("Proprietà dei logaritmi", mix(R, seen, [(s2_prop, 14), (s2_svil, 6)])),
        ("Cambiamento di base", mix(R, seen, [(s3_base, 11), (s1_def, 9)])),
        ("Dominio delle funzioni logaritmiche", mix(R, seen, [(s4_dom, 20)])),
        ("La funzione logaritmica", mix(R, seen, [(s4_fun, 12), (s2_prop, 8)])),
    ]
    body = L(["Il <b>logaritmo</b> in base a di x è l’esponente da dare ad a per ottenere x: log<sub>a</sub> x = y ⟺ a<sup>y</sup> = x (a &gt; 0, a ≠ 1, x &gt; 0). log x è in base 10, ln x in base e.",
              "Proprietà: log<sub>a</sub>(xy) = log<sub>a</sub> x + log<sub>a</sub> y; log<sub>a</sub>(x/y) = log<sub>a</sub> x − log<sub>a</sub> y; log<sub>a</sub> x<sup>n</sup> = n log<sub>a</sub> x.",
              "<b>Cambiamento di base</b>: log<sub>a</sub> x = log<sub>b</sub> x / log<sub>b</sub> a.",
              "La funzione y = log<sub>a</sub> x è l’inversa di y = a<sup>x</sup>: dominio x &gt; 0, passa per (1; 0), asintoto verticale x = 0; crescente se a &gt; 1, decrescente se 0 &lt; a &lt; 1."],
             [("log<sub>2</sub> 32", ["2<sup>5</sup> = 32"], "5"),
              ("log<sub>3</sub> 54 − log<sub>3</sub> 2", ["log<sub>3</sub>(54/2) = log<sub>3</sub> 27"], "3")],
             [["log(a + b) = log a + log b", "La proprietà vale per il prodotto: log(ab) = log a + log b."],
              ["log<sub>2</sub> 8 = 4", "2<sup>3</sup> = 8: il logaritmo è 3."],
              ["Dominio di log(x − 3): x &gt; −3", "L’argomento deve essere positivo: x − 3 &gt; 0, x &gt; 3."]])
    faq = [("Perché non esiste il logaritmo di un numero negativo?", "Perché a<sup>y</sup> con a &gt; 0 è sempre positivo: nessun esponente dà un numero negativo o zero."),
           ("Come si calcola log<sub>3</sub> 7 con la calcolatrice?", "Con il cambiamento di base: log<sub>3</sub> 7 = ln 7 / ln 3 ≈ 1,77.")]
    unit(G, R, "logaritmi", "F",
         "Logaritmi e loro proprietà; funzione logaritmica e suo grafico",
         "Logaritmi e funzione logaritmica", "Logaritmi",
         "Schede di matematica per la quarta liceo sui logaritmi: definizione, logaritmi decimali e naturali, proprietà, cambiamento di base, dominio e grafico della funzione logaritmica. 100 esercizi con soluzioni.",
         "logₐ x = y ⟺ aʸ = x", "log(xy) = log x + log y; log xⁿ = n log x; l’argomento deve essere positivo.",
         body, faq, sets, 2)


if __name__ == "__main__":
    main()
