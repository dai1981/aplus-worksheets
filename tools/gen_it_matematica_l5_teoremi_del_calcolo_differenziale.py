# -*- coding: utf-8 -*-
"""
Italia Matematica quinta liceo: Teoremi del calcolo differenziale (Relazioni e funzioni)
  python3 tools/gen_it_matematica_l5_teoremi_del_calcolo_differenziale.py
Teorema di Rolle, teorema di Lagrange (del valor medio) e punto c, conseguenze (funzione costante, crescente/decrescente
dal segno di f′), teorema di De l’Hôpital per le forme 0/0 e ∞/∞, ipotesi dei teoremi.
Errori: applicare Rolle senza f(a) = f(b), derivare il quoziente invece di numeratore e denominatore separati,
usare De l’Hôpital fuori dalle forme indeterminate.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, W, fq, nz, FR, poly

R = random.Random(72507)
G = "quinta-liceo"


def iv(a, b):
    return "[%s; %s]" % (fq(a), fq(b))


def s1_rolle():
    m = R.randint(-4, 4)
    h = R.randint(1, 4)
    a, b = m - h, m + h
    k = R.choice([1, 2, -1, 3])
    c0 = R.randint(-6, 6)
    cs = [k, -2 * k * m, c0]
    return M("f(x) = %s verifica il teorema di Rolle in %s. In quale punto c si ha f′(c) = 0?" % (poly(cs), iv(a, b)), "c = %s" % fq(m),
             ["c = %s" % fq(x) for x in W(-m, m + h, m - h, m + 1) if x != m][:3],
             "f(%s) = f(%s) = %s. f′(x) = %s si annulla in <b>c = %s</b>, che sta in (%s; %s)." % (fq(a), fq(b), fq(k * a * a - 2 * k * m * a + c0), poly([2 * k, -2 * k * m]), fq(m), fq(a), fq(b)))


def s1_rolle_k():
    a = R.randint(-3, 1)
    b = a + R.randint(2, 5)
    # f = x² + kx + 3 con f(a) = f(b): a² + ka = b² + kb  →  k = −(a + b)
    k = -(a + b)
    P = lambda x: "(%s)" % fq(x) if x < 0 else fq(x)
    return M("Per quale valore di k la funzione f(x) = x² + kx + 3 soddisfa le ipotesi del teorema di Rolle in %s?" % iv(a, b), "k = %s" % fq(k),
             ["k = %s" % fq(x) for x in W(a + b, k + 1, -(b - a), a * b) if x != k][:3],
             "Serve f(%s) = f(%s): %s = %s, da cui k = −(%s + %s) = <b>%s</b>." % (fq(a), fq(b), poly([a, a * a]).replace("x", "k"), poly([b, b * b]).replace("x", "k"), fq(a), P(b), fq(k)))

PAIRS_INV = [(1, 4), (1, 9), (2, 8), (4, 9), (1, 16), (3, 12), (2, 18), (4, 25)]
PAIRS_SQ = [(1, 9), (4, 16), (1, 25), (9, 25), (0, 4), (0, 16), (4, 36), (0, 36)]


def s2_lag():
    kind = R.choice(["q", "q", "inv", "sq", "cub"])
    if kind == "q":
        p, q = nz(R, -3, 3), R.randint(-6, 6)
        a = R.randint(-3, 2)
        b = a + R.choice([2, 4, 6])
        c = Fr(a + b, 2)
        f = poly([p, q, R.randint(-5, 5)])
        e = "Per una parabola (f(b) − f(a))/(b − a) = p(a + b) + q, e f′(c) = 2pc + q: c è il punto medio, <b>c = %s</b>." % fq(c)
        w = W(Fr(a, 1) + 1 if a + 1 != c else b - 1, Fr(b - a, 2), Fr(q, -2 * p), a + b, c + 1, b, c - 1, c + 2)
    elif kind == "inv":
        a, b = R.choice(PAIRS_INV)
        c = Fr(int((a * b) ** 0.5))
        f = "1/x"
        e = "(f(b) − f(a))/(b − a) = −1/(%d · %d); f′(c) = −1/c² dà c² = %d, <b>c = %s</b>." % (a, b, a * b, fq(c))
        w = W(Fr(a + b, 2), Fr(b - a, 2), Fr(a * b, 2), -c)
    elif kind == "sq":
        a, b = R.choice(PAIRS_SQ)
        ra, rb = int(a ** 0.5), int(b ** 0.5)
        c = Fr((ra + rb) ** 2, 4)
        f = "√x"
        e = "(√%d − √%d)/(%d − %d) = 1/%d; f′(c) = 1/(2√c) dà √c = %s, <b>c = %s</b>." % (b, a, b, a, ra + rb, fq(Fr(ra + rb, 2)), fq(c))
        w = W(Fr(a + b, 2), Fr(ra + rb, 2), Fr(b - a, 2), c + 1, Fr(b, 2) + 1, Fr(rb), c + 2, c * 3)
    else:
        k = R.choice([3, 6])
        a, b = 0, k
        # f = x³ su [0; 3]: (27)/3 = 9 = 3c² → c = √3 ; su [0; 6]: 216/6 = 36 = 3c² → c = 2√3
        f = "x³"
        ans = "c = √3" if k == 3 else "c = 2√3"
        return M("Trova il punto c del teorema di Lagrange per f(x) = x³ in %s." % iv(a, b), ans,
                 ["c = %s" % x for x in (["3", "3/2", "1"] if k == 3 else ["3", "√6", "2√6"])],
                 "(f(%d) − f(0))/%d = %d = 3c², quindi c² = %d e <b>%s</b> (c &gt; 0)." % (k, k, k * k, k * k // 3, ans))
    return M("Trova il punto c del teorema di Lagrange per f(x) = %s in %s." % (f, iv(a, b)), "c = %s" % fq(c),
             ["c = %s" % fq(x) for x in w if x != c][:3], e)


def s2_rapp():
    cs = [nz(R, -2, 2), R.randint(-4, 4), R.randint(-4, 4), R.randint(-5, 5)]
    a = R.randint(-2, 1)
    b = a + R.randint(1, 3)
    ev = lambda x: ((cs[0] * x + cs[1]) * x + cs[2]) * x + cs[3]
    r = Fr(ev(b) - ev(a), b - a)
    return M("Per il teorema di Lagrange esiste c in (%s; %s) con f′(c) uguale a quale valore, se f(x) = %s?" % (fq(a), fq(b), poly(cs)), fq(r),
             [fq(x) for x in W(ev(b) - ev(a), Fr(ev(b) + ev(a), b - a), r + 1, Fr(ev(b), b) if b else r - 1, -r, r - 2, r + 3) if x != r][:3],
             "f′(c) = (f(%s) − f(%s))/(%s − %s) = (%s − %s)/%d = <b>%s</b>." % (fq(b), fq(a), fq(b), "(%s)" % fq(a) if a < 0 else fq(a), fq(ev(b)), "(%s)" % fq(ev(a)) if ev(a) < 0 else fq(ev(a)), b - a, fq(r)))


def s3_hop():
    a, b = R.sample([1, 2, 3, 4, 5, 6, 7], 2)
    n = R.randint(2, 5)
    T = [("lim<sub>x→0</sub> %s" % FR("e<sup>%sx</sup> − 1" % (a if a > 1 else ""), "%sx" % (b if b > 1 else "")), Fr(a, b), "Forma 0/0: derivo sopra e sotto, %s e<sup>%sx</sup>/%s → %s/%s." % (a, a if a > 1 else "", b, a, b)),
         ("lim<sub>x→0</sub> %s" % FR("1 − cos %sx" % (a if a > 1 else ""), "x²"), Fr(a * a, 2), "Due volte De l’Hôpital: %s sen %sx/(2x) → %s/2." % (a, a if a > 1 else "", a * a)),
         ("lim<sub>x→%d</sub> %s" % (a, FR("x<sup>%d</sup> − %d" % (n, a ** n), "x − %d" % a)), Fr(n * a ** (n - 1)), "Forma 0/0: %dx<sup>%d</sup>/1 in x = %d." % (n, n - 1, a)),
         ("lim<sub>x→0</sub> %s" % FR("ln(1 + %sx)" % (a if a > 1 else ""), "%sx" % (b if b > 1 else "")), Fr(a, b), "Derivo: [%s/(1 + %sx)]/%s → %s/%s." % (a, a if a > 1 else "", b, a, b)),
         ("lim<sub>x→0</sub> %s" % FR("e<sup>x</sup> − 1 − x", "x²"), Fr(1, 2), "Due volte: (eˣ − 1)/(2x), poi eˣ/2 → 1/2."),
         ("lim<sub>x→0</sub> %s" % FR("x − sen x", "x³"), Fr(1, 6), "Tre volte: (1 − cos x)/(3x²) → sen x/(6x) → cos x/6 → 1/6."),
         ("lim<sub>x→0</sub> %s" % FR("tg %sx" % (a if a > 1 else ""), "%sx" % (b if b > 1 else "")), Fr(a, b), "Derivo: [%s/cos² %sx]/%s → %s/%s." % (a, a if a > 1 else "", b, a, b))]
    f, v, e = R.choice(T)
    return M("Calcola con il teorema di De l’Hôpital %s." % f, fq(v), [fq(x) for x in W(Fr(b, a), 1, 0, v * 2, v + 1, Fr(a)) if x != v][:3], e + " <b>%s</b>." % fq(v))


def s3_inf():
    n = R.randint(1, 4)
    def xp(c, e):
        return ("%s" % c if c != 1 else "") + ("x<sup>%d</sup>" % e if e > 1 else ("x" if e == 1 else ""))
    k = R.choice([1, 2, 3])
    T = [("lim<sub>x→+∞</sub> %s" % FR("x<sup>%d</sup>" % n if n > 1 else "x", "e<sup>x</sup>"), "0", "Derivo %d volte: il numeratore diventa una costante, il denominatore resta eˣ → +∞." % n),
         ("lim<sub>x→+∞</sub> %s" % FR("ln x", "x<sup>%d</sup>" % n if n > 1 else "x"), "0", "Derivo: (1/x)/(%s) = %s → 0." % (xp(n, n - 1) or "1", "1/(%s)" % xp(n, n) if n > 1 else "1/x")),
         ("lim<sub>x→+∞</sub> %s" % FR("e<sup>%sx</sup>" % (k if k > 1 else ""), "x<sup>%d</sup>" % n if n > 1 else "x"), "+∞", "Derivando più volte il denominatore diventa costante, il numeratore resta un esponenziale."),
         ("lim<sub>x→0<sup>+</sup></sub> x<sup>%d</sup> ln x" % n if n > 1 else "lim<sub>x→0<sup>+</sup></sub> x ln x", "0", "Forma 0 · ∞: scrivo ln x/(1/x<sup>%d</sup>) e derivo: −x<sup>%d</sup>/%d → 0." % (n, n, n)),
         ("lim<sub>x→+∞</sub> %s" % FR("x<sup>%d</sup>" % n if n > 1 else "x", "ln x"), "+∞", "Derivo: %s/(1/x) = %s → +∞." % (xp(n, n - 1) or "1", xp(n, n)))]
    f, v, e = R.choice(T)
    return M("Calcola %s." % f, v, [x for x in ["0", "+∞", "1", "−∞"] if x != v][:3], e + " <b>%s</b>." % v)


def s4_mono():
    r1 = R.randint(-4, 2)
    r2 = r1 + R.choice([2, 4, 6])
    k = R.choice([1, -1])
    # f′ = 3k(x − r1)(x − r2), f = k[x³ − 3/2 (r1 + r2) x² + 3 r1 r2 x]
    cs = [k, -Fr(3, 2) * (r1 + r2) * k, 3 * r1 * r2 * k, 0]
    f = poly(cs)
    dec = k > 0
    inside = "(%s; %s)" % (fq(r1), fq(r2))
    outside = "x &lt; %s ∨ x &gt; %s" % (fq(r1), fq(r2))
    ask = R.choice(["decrescente", "crescente"])
    ans = inside if (ask == "decrescente") == dec else outside
    w = [inside if ans == outside else outside, "(%s; %s)" % (fq(-r2), fq(-r1)) if (-r2, -r1) != (r1, r2) else "(0; %s)" % fq(r2), "x &gt; %s" % fq(r1)]
    fd = "%s(x %s)(x %s)" % ("3" if k > 0 else "−3", "− %s" % fq(r1) if r1 > 0 else ("+ %s" % fq(-r1) if r1 < 0 else ""), "− %s" % fq(r2) if r2 > 0 else ("+ %s" % fq(-r2) if r2 < 0 else ""))
    fd = fd.replace("(x )", "x")
    return M("f(x) = %s. In quale insieme f è %s?" % (f, ask), ans, w,
             "f′(x) = %s = %s: è %s tra le radici %s e %s e %s fuori. Quindi f è %s in <b>%s</b>." % (
                 poly([3 * k, cs[1] * 2, cs[2]]), fd, "negativa" if k > 0 else "positiva", fq(r1), fq(r2), "positiva" if k > 0 else "negativa", ask, ans))

IPO = [("f(x) = |x| in [−1; 1]", "Rolle", "no: f non è derivabile in x = 0"),
       ("f(x) = x² in [0; 2]", "Rolle", "no: f(0) ≠ f(2)"),
       ("f(x) = 1/x in [−1; 1]", "Lagrange", "no: f non è continua in x = 0"),
       ("f(x) = x² − 4x in [0; 4]", "Rolle", "sì, tutte le ipotesi sono verificate"),
       ("f(x) = √x in [0; 4]", "Lagrange", "sì, tutte le ipotesi sono verificate"),
       ("f(x) = sen x in [0; π]", "Rolle", "sì, tutte le ipotesi sono verificate"),
       ("f(x) = ∛x in [−1; 1]", "Lagrange", "no: f non è derivabile in x = 0"),
       ("f(x) = tg x in [0; π]", "Rolle", "no: f non è continua in x = π/2"),
       ("f(x) = eˣ in [0; 1]", "Rolle", "no: f(0) ≠ f(1)"),
       ("f(x) = ln x in [1; e]", "Lagrange", "sì, tutte le ipotesi sono verificate")]


def s5_ipo():
    f, t, a = R.choice(IPO)
    opts = ["sì, tutte le ipotesi sono verificate", "no: f non è derivabile in x = 0", "no: f non è continua in x = 0", "no: f(0) ≠ f(2)"]
    w = [o for o in opts if o != a]
    if a not in opts:
        w = w[:3]
    return M("Si può applicare il teorema di %s a %s?" % (t, f), a, w[:3],
             ("Rolle richiede f continua in [a; b], derivabile in (a; b) e f(a) = f(b)." if t == "Rolle" else "Lagrange richiede f continua in [a; b] e derivabile in (a; b).") + " Risposta: <b>%s</b>." % a)

CONC = [("Se f′(x) = 0 per ogni x di un intervallo, allora f…", "è costante nell’intervallo", ["è nulla", "ha un massimo", "è lineare non costante"], "È una conseguenza del teorema di Lagrange."),
        ("Se f′(x) &gt; 0 in un intervallo, allora f è…", "crescente nell’intervallo", ["positiva", "convessa", "decrescente nell’intervallo"], "Per Lagrange f(x<sub>2</sub>) − f(x<sub>1</sub>) = f′(c)(x<sub>2</sub> − x<sub>1</sub>) &gt; 0."),
        ("Due funzioni con la stessa derivata in un intervallo…", "differiscono per una costante", ["sono uguali", "hanno lo stesso grafico", "si intersecano sempre"], "La differenza ha derivata 0, quindi è costante."),
        ("De l’Hôpital si può usare per lim<sub>x→1</sub> (x² + 1)/(x + 1)?", "no, non è una forma indeterminata", ["sì, dà 1", "sì, dà 2", "no, la funzione non è derivabile"], "Sostituendo si ottiene 2/2 = 1: non è 0/0 né ∞/∞."),
        ("Nel teorema di De l’Hôpital si calcola il limite di…", "f′(x)/g′(x)", ["(f/g)′(x)", "f′(x) · g′(x)", "f(x)/g′(x)"], "Si derivano numeratore e denominatore separatamente."),
        ("Il teorema di Rolle garantisce che esista…", "almeno un punto in cui la tangente è orizzontale", ["un massimo assoluto", "esattamente un punto con f′ = 0", "uno zero di f"], "f′(c) = 0: tangente orizzontale in almeno un punto.")]


def s5_conc():
    q, a, w, e = R.choice(CONC)
    return M(q, a, w, e + " <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Teorema di Rolle", mix(R, seen, [(s1_rolle, 12), (s1_rolle_k, 8)])),
        ("Teorema di Lagrange", mix(R, seen, [(s2_lag, 12), (s2_rapp, 8)])),
        ("Teorema di De l’Hôpital", mix(R, seen, [(s3_hop, 14), (s3_inf, 6)])),
        ("Crescenza e decrescenza", mix(R, seen, [(s4_mono, 20)])),
        ("Ipotesi e conseguenze dei teoremi", mix(R, seen, [(s5_ipo, 8), (s5_conc, 6), (s3_inf, 6)])),
    ]
    body = L(["<b>Rolle</b>: se f è continua in [a; b], derivabile in (a; b) e f(a) = f(b), esiste c in (a; b) con f′(c) = 0.",
              "<b>Lagrange</b> (valor medio): se f è continua in [a; b] e derivabile in (a; b), esiste c con f′(c) = [f(b) − f(a)]/(b − a). Conseguenze: f′ = 0 ⇒ f costante; f′ &gt; 0 ⇒ f crescente; f′ &lt; 0 ⇒ f decrescente.",
              "<b>De l’Hôpital</b>: per le forme 0/0 o ∞/∞, lim f/g = lim f′/g′ se quest’ultimo esiste. Si derivano numeratore e denominatore separatamente; si può ripetere.",
              "Le forme 0 · ∞ e ∞ − ∞ si riportano prima a 0/0 o ∞/∞."],
             [("Lagrange per x² in [1; 5]", ["(25 − 1)/4 = 6 = 2c"], "c = 3"),
              ("lim<sub>x→0</sub> (e<sup>2x</sup> − 1)/x", ["0/0: derivo", "2e<sup>2x</sup>/1 → 2"], "2")],
             [["Applicare Rolle con f(a) ≠ f(b)", "Senza f(a) = f(b) vale solo Lagrange."],
              ["Derivare il quoziente f/g", "De l’Hôpital usa f′/g′, non (f/g)′."],
              ["Usare De l’Hôpital su un limite già determinato", "Prima verifica che sia 0/0 o ∞/∞."]])
    faq = [("Che significato geometrico ha il teorema di Lagrange?", "Esiste un punto in cui la retta tangente è parallela alla corda che congiunge (a; f(a)) e (b; f(b))."),
           ("Rolle è un caso particolare di Lagrange?", "Sì: se f(a) = f(b) la pendenza della corda è 0, quindi il punto c di Lagrange ha f′(c) = 0.")]
    unit(G, R, "teoremi-del-calcolo-differenziale", "F",
         "Teoremi di Rolle, di Lagrange e di De l’Hôpital e loro applicazioni",
         "Teoremi del calcolo differenziale", "Teoremi del calcolo differenziale",
         "Schede di matematica per la quinta liceo sui teoremi del calcolo differenziale: teorema di Rolle, teorema di Lagrange e punto c, crescenza e decrescenza dal segno della derivata, teorema di De l’Hôpital, verifica delle ipotesi. 100 esercizi con soluzioni.",
         "Lagrange: f′(c) = [f(b) − f(a)]/(b − a).", "De l’Hôpital: lim f/g = lim f′/g′ per 0/0 e ∞/∞.",
         body, faq, sets, 7)


if __name__ == "__main__":
    main()
