# -*- coding: utf-8 -*-
"""
Italia Matematica quinta liceo: Massimi, minimi e flessi (Relazioni e funzioni)
  python3 tools/gen_it_matematica_l5_massimi_minimi_e_flessi.py
Punti stazionari, massimi e minimi relativi con lo studio del segno di f′, valore massimo e minimo, concavità e punti
di flesso con f″, massimo e minimo assoluti in un intervallo chiuso, problemi di ottimizzazione.
Errori: scambiare massimo e minimo, dimenticare gli estremi dell’intervallo, flesso dove f′ = 0 invece di f″ = 0.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, W, fq, nz, poly

R = random.Random(72508)
G = "quinta-liceo"


def cubic():
    """f = k[x³ − 3/2 (r1 + r2) x² + 3 r1 r2 x] + d con f′ = 3k(x − r1)(x − r2)"""
    r1 = R.randint(-4, 2)
    r2 = r1 + R.choice([2, 4, 6])
    k = R.choice([1, -1])
    d = R.randint(-5, 5)
    cs = [k, -Fr(3, 2) * (r1 + r2) * k, 3 * r1 * r2 * k, d]
    if cs[1].denominator != 1:
        return None
    cs = [int(c) for c in cs]
    return r1, r2, k, cs


def ev(cs, x):
    v = 0
    for c in cs:
        v = v * x + c
    return v


def pt(x, y):
    return "(%s; %s)" % (fq(x), fq(y))


def s1_staz():
    c = cubic()
    if not c:
        return None
    r1, r2, k, cs = c
    ask = R.choice(["massimo", "minimo"])
    xmax, xmin = (r1, r2) if k > 0 else (r2, r1)
    ans = xmax if ask == "massimo" else xmin
    oth = xmin if ask == "massimo" else xmax
    return M("f(x) = %s. In quale ascissa f ha un %s relativo?" % (poly(cs), ask), "x = %s" % fq(ans),
             ["x = %s" % fq(v) for v in W(oth, -ans, -oth, Fr(r1 + r2, 2), ans + 1, oth + 2) if v != ans][:3],
             "f′(x) = %s si annulla in %s e %s. f′ è %s prima di %s, %s tra le radici, %s dopo: il %s è in <b>x = %s</b>." % (
                 poly([3 * k, 2 * cs[1], cs[2]]), fq(r1), fq(r2), "positiva" if k > 0 else "negativa", fq(r1), "negativa" if k > 0 else "positiva", "positiva" if k > 0 else "negativa", ask, fq(ans)))


def s1_quad():
    a = nz(R, -3, 3)
    v = R.randint(-4, 4)
    b, c = -2 * a * v, R.randint(-6, 6)
    cs = [a, b, c]
    y = ev(cs, v)
    t = "massimo" if a < 0 else "minimo"
    return M("f(x) = %s. Qual è il punto di %s?" % (poly(cs), t), pt(v, y), [pt(*p) for p in W((-v, y), (v, c), (y, v), (v, -y), (v, y + a), (v + 1, y)) if p != (v, y)][:3],
             "f′(x) = %s = 0 per x = %s; f″ = %s %s 0, quindi è un %s: f(%s) = %s, <b>%s</b>." % (poly([2 * a, b]), fq(v), fq(2 * a), "&lt;" if a < 0 else "&gt;", t, fq(v), fq(y), pt(v, y)))


def s2_val():
    c = cubic()
    if not c:
        return None
    r1, r2, k, cs = c
    ask = R.choice(["massimo", "minimo"])
    xmax, xmin = (r1, r2) if k > 0 else (r2, r1)
    xa = xmax if ask == "massimo" else xmin
    v = ev(cs, xa)
    vo = ev(cs, xmin if ask == "massimo" else xmax)
    return M("f(x) = %s. Quanto vale il %s relativo di f?" % (poly(cs), ask), fq(v), [fq(x) for x in W(vo, xa, -v, v + cs[-1] if cs[-1] else v + 1, ev(cs, -xa)) if x != v][:3],
             "I punti stazionari sono x = %s e x = %s; il %s relativo è in x = %s e vale f(%s) = <b>%s</b>." % (fq(r1), fq(r2), ask, fq(xa), fq(xa), fq(v)))


def s3_fl():
    a = R.choice([1, -1, 2, -2, 1])
    xf = R.randint(-3, 3)
    b = -3 * a * xf
    c, d = R.randint(-9, 9), R.randint(-5, 5)
    cs = [a, b, c, d]
    yf = ev(cs, xf)
    ask = R.choice(["x", "p", "conc"])
    if ask == "x":
        return M("f(x) = %s. In quale ascissa f ha un punto di flesso?" % poly(cs), "x = %s" % fq(xf),
                 ["x = %s" % fq(v) for v in W(-xf, xf + 1, Fr(-b, a), Fr(c, 3 * a) if c else xf - 1) if v != xf][:3],
                 "f″(x) = %s si annulla e cambia segno in <b>x = %s</b>." % (poly([6 * a, 2 * b]), fq(xf)))
    if ask == "p":
        return M("f(x) = %s. Qual è il punto di flesso?" % poly(cs), pt(xf, yf), [pt(*p) for p in W((xf, d), (-xf, yf), (yf, xf), (xf, -yf), (xf, yf + 1)) if p != (xf, yf)][:3],
                 "f″(x) = %s = 0 per x = %s e f(%s) = %s: <b>%s</b>." % (poly([6 * a, 2 * b]), fq(xf), fq(xf), fq(yf), pt(xf, yf)))
    up = a > 0
    return M("f(x) = %s. Dove il grafico di f volge la concavità verso l’alto?" % poly(cs), "x &gt; %s" % fq(xf) if up else "x &lt; %s" % fq(xf),
             ["x &lt; %s" % fq(xf) if up else "x &gt; %s" % fq(xf), "x &gt; %s" % fq(-xf) if xf else "x &gt; 1", "in tutto ℝ"],
             "f″(x) = %s è positiva per <b>%s</b>." % (poly([6 * a, 2 * b]), "x &gt; %s" % fq(xf) if up else "x &lt; %s" % fq(xf)))


def s3_tipo():
    T = [("f′(x<sub>0</sub>) = 0 e f″(x<sub>0</sub>) &gt; 0", "minimo relativo"), ("f′(x<sub>0</sub>) = 0 e f″(x<sub>0</sub>) &lt; 0", "massimo relativo"),
         ("f″(x<sub>0</sub>) = 0 e f″ cambia segno in x<sub>0</sub>", "punto di flesso"), ("f′(x<sub>0</sub>) = 0, f″(x<sub>0</sub>) = 0 e f″ cambia segno", "flesso a tangente orizzontale"),
         ("f′ passa da positiva a negativa in x<sub>0</sub>", "massimo relativo"), ("f′ passa da negativa a positiva in x<sub>0</sub>", "minimo relativo")]
    q, a = R.choice(T)
    opts = ["minimo relativo", "massimo relativo", "punto di flesso", "flesso a tangente orizzontale"]
    return M("Se %s, in x<sub>0</sub> c’è un…" % q, a, [o for o in opts if o != a],
             "f′ dà la crescenza (massimi e minimi), f″ la concavità (flessi): <b>%s</b>." % a)


def s4_ass():
    a = nz(R, -2, 2)
    v = R.randint(-2, 3)
    cs = [a, -2 * a * v, R.randint(-5, 5)]
    lo = v - R.randint(1, 3)
    hi = v + R.randint(1, 4)
    if R.random() < 0.3:  # vertice fuori dall’intervallo
        lo, hi = v + 1, v + R.randint(3, 5)
    vals = {x: ev(cs, x) for x in (lo, hi)}
    if lo < v < hi:
        vals[v] = ev(cs, v)
    ask = R.choice(["massimo", "minimo"])
    best = max(vals.values()) if ask == "massimo" else min(vals.values())
    other = min(vals.values()) if ask == "massimo" else max(vals.values())
    return M("f(x) = %s. Qual è il %s assoluto di f nell’intervallo [%s; %s]?" % (poly(cs), ask, fq(lo), fq(hi)), fq(best),
             [fq(x) for x in W(other, ev(cs, v) if not lo < v < hi else ev(cs, lo) + ev(cs, hi), -best, best + 1, ev(cs, (lo + hi) // 2)) if x != best][:3],
             "Confronto f nei punti stazionari interni e negli estremi: %s. Il %s è <b>%s</b>." % ("; ".join("f(%s) = %s" % (fq(x), fq(y)) for x, y in sorted(vals.items())), ask, fq(best)))


def s5_opt():
    k = R.choice(["rett", "fiume", "num", "quad", "scatola", "somma2"])
    if k == "rett":
        p = R.choice([20, 24, 32, 36, 40, 48, 60, 80])
        s = p // 4
        return M("Tra i rettangoli di perimetro %d cm, quale ha area massima?" % p, "il quadrato di lato %d cm" % s,
                 ["il rettangolo %d cm × %d cm" % (s + 2, s - 2), "il quadrato di lato %d cm" % (p // 2), "il rettangolo %d cm × %d cm" % (p // 2 - 1, 1)],
                 "Con lati x e %d − x l’area è A(x) = x(%d − x); A′ = %d − 2x = 0 per x = %d: <b>il quadrato di lato %d cm</b>." % (p // 2, p // 2, p // 2, s, s))
    if k == "fiume":
        l_ = R.choice([40, 60, 80, 100, 120, 200])
        x = l_ // 4
        return M("Con %d m di rete si recinta un terreno rettangolare lungo un fiume (il lato sul fiume non si recinta). Qual è l’area massima?" % l_, "%d m²" % (l_ * l_ // 8),
                 ["%d m²" % v for v in W(l_ * l_ // 16, l_ * l_ // 4, (l_ // 3) * (l_ // 3), (l_ // 3) * (l_ - 2 * (l_ // 3))) if v != l_ * l_ // 8][:3],
                 "Con x i lati perpendicolari al fiume, A(x) = x(%d − 2x); A′ = %d − 4x = 0 per x = %d, area %d · %d = <b>%d m²</b>." % (l_, l_, x, x, l_ - 2 * x, l_ * l_ // 8))
    if k == "num":
        s = R.choice([10, 12, 16, 20, 24, 30, 40, 50])
        return M("Due numeri positivi hanno somma %d. Qual è il prodotto massimo?" % s, str(s * s // 4),
                 [str(v) for v in W((s // 2 - 1) * (s // 2 + 1), s * s // 2, s * 2) if v != s * s // 4][:3],
                 "P(x) = x(%d − x), P′ = %d − 2x = 0 per x = %d: prodotto <b>%d</b>." % (s, s, s // 2, s * s // 4))
    if k == "somma2":
        s = R.choice([8, 10, 12, 14, 16, 20])
        return M("Due numeri hanno somma %d. Qual è il valore minimo della somma dei loro quadrati?" % s, str(s * s // 2),
                 [str(v) for v in W(s * s // 4, s * s, (s // 2 + 1) ** 2 + (s // 2 - 1) ** 2) if v != s * s // 2][:3],
                 "S(x) = x² + (%d − x)², S′ = 4x − %d = 0 per x = %d: S = <b>%d</b>." % (s, 2 * s, s // 2, s * s // 2))
    if k == "quad":
        p = R.choice([1, 2, 3, 4, 5])
        # distanza minima di (0; p) dalla parabola y = x²? semplice: punto della retta y = x più vicino a (2p; 0)
        a = 2 * p
        return M("Qual è il punto della retta y = x più vicino al punto (%d; 0)?" % a, "(%d; %d)" % (p, p),
                 ["(%d; %d)" % v for v in [(a, a), (0, 0), (p + 1, p + 1)]],
                 "d²(x) = (x − %d)² + x², derivata 4x − %d = 0 per x = %d: <b>(%d; %d)</b>." % (a, 2 * a, p, p, p))
    l_ = R.choice([12, 18, 24, 30, 36])
    x = l_ // 6
    v = x * (l_ - 2 * x) ** 2
    return M("Da un quadrato di cartone di lato %d cm si tagliano agli angoli quadratini di lato x e si piega una scatola senza coperchio. Per quale x il volume è massimo?" % l_, "x = %d cm" % x,
             ["x = %d cm" % w for w in W(l_ // 4, l_ // 3, l_ // 2, x + 1) if w != x][:3],
             "V(x) = x(%d − 2x)²; V′(x) = (%d − 2x)(%d − 6x) = 0 per x = %d (l’altra radice dà volume 0): <b>x = %d cm</b>, V = %d cm³." % (l_, l_, l_, x, x, v))


def main():
    seen = set()
    sets = [
        ("Punti stazionari", mix(R, seen, [(s1_quad, 8), (s1_staz, 12)])),
        ("Valori massimi e minimi", mix(R, seen, [(s2_val, 14), (s1_staz, 6)])),
        ("Concavità e flessi", mix(R, seen, [(s3_fl, 16), (s3_tipo, 4)])),
        ("Massimo e minimo assoluti", mix(R, seen, [(s4_ass, 20)])),
        ("Problemi di ottimizzazione", mix(R, seen, [(s5_opt, 20)])),
    ]
    body = L(["I <b>punti stazionari</b> sono quelli in cui f′(x) = 0. Se f′ passa da positiva a negativa c’è un <b>massimo relativo</b>, da negativa a positiva un <b>minimo relativo</b>.",
              "Con la derivata seconda: f′(x<sub>0</sub>) = 0 e f″(x<sub>0</sub>) &lt; 0 ⇒ massimo; f″(x<sub>0</sub>) &gt; 0 ⇒ minimo.",
              "f″ &gt; 0: concavità verso l’alto; f″ &lt; 0: verso il basso. Un <b>flesso</b> è un punto in cui la concavità cambia (f″ si annulla e cambia segno).",
              "In un intervallo chiuso [a; b] il massimo e il minimo assoluti si cercano tra i punti stazionari interni <b>e gli estremi</b> a e b. Nei problemi di ottimizzazione si scrive la grandezza come funzione di una variabile e se ne cerca il massimo o il minimo."],
             [("f(x) = x³ − 3x", ["f′ = 3x² − 3 = 0 per x = ±1", "f″(−1) = −6 &lt; 0, f″(1) = 6 &gt; 0"], "massimo in x = −1, minimo in x = 1"),
              ("Flesso di x³ − 6x²", ["f″ = 6x − 12 = 0"], "x = 2")],
             [["Scambiare massimo e minimo", "Guarda il segno di f′ prima e dopo il punto."],
              ["Cercare il flesso con f′ = 0", "Il flesso si cerca con f″ = 0."],
              ["Dimenticare gli estremi dell’intervallo", "Il massimo assoluto può essere in a o in b."]])
    faq = [("Un punto stazionario è sempre un massimo o un minimo?", "No: per f(x) = x³ in x = 0 si ha f′ = 0 ma la funzione cresce sempre; è un flesso a tangente orizzontale."),
           ("Come si imposta un problema di ottimizzazione?", "Scegli la variabile, scrivi la grandezza da rendere massima o minima in funzione di essa, indica il dominio, deriva e studia il segno di f′.")]
    unit(G, R, "massimi-minimi-e-flessi", "F",
         "Ricerca di massimi, minimi e flessi; problemi di ottimizzazione",
         "Massimi, minimi e flessi", "Massimi, minimi e flessi",
         "Schede di matematica per la quinta liceo su massimi, minimi e flessi: punti stazionari, massimi e minimi relativi, concavità e punti di flesso, massimo e minimo assoluti in un intervallo, problemi di ottimizzazione. 100 esercizi con soluzioni.",
         "Massimo: f′ passa da + a −.", "Flesso: f″ si annulla e cambia segno.",
         body, faq, sets, 8)


if __name__ == "__main__":
    main()
