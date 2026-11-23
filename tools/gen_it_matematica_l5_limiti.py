# -*- coding: utf-8 -*-
"""
Italia Matematica quinta liceo: Limiti di funzioni (Relazioni e funzioni)
  python3 tools/gen_it_matematica_l5_limiti.py
Significato di limite (lettura dal grafico), limite destro e sinistro, limiti di funzioni continue (sostituzione),
limiti all’infinito di polinomi e funzioni elementari (eˣ, ln x, 1/x), algebra dei limiti con ∞ (forme determinate),
limiti infiniti per x → a (asintoti verticali), limiti delle successioni.
Errori: 1/0 = 0, ∞ − ∞ = 0, confondere 0⁺ e 0⁻, lim eˣ per x → −∞ = −∞.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, P2, FR, kurve, relabel, poly

R = random.Random(72503)
G = "quinta-liceo"
INF, PINF, MINF = "∞", "+∞", "−∞"
BLUE = "#1f6fd1"


def lim(x0, f):
    return "lim<sub>x→%s</sub> %s" % (x0, f)


def s1_sost():
    a, b, c = nz(R, -3, 3), R.randint(-5, 5), R.randint(-5, 5)
    x0 = R.randint(-3, 3)
    v = a * x0 * x0 + b * x0 + c
    return M("Calcola %s." % lim(fq(x0), "(%s)" % P2(a, b, c)), fq(v), [fq(x) for x in W(-v if v else 1, a * x0 * x0 - b * x0 + c, v + 1, a + b + c) if x != v],
             "Il polinomio è continuo: basta sostituire x = %s, <b>%s</b>." % (fq(x0), fq(v)))


ELEM = [(PINF, "e<sup>x</sup>", PINF), (MINF, "e<sup>x</sup>", "0"), ("0<sup>+</sup>", "ln x", MINF), (PINF, "ln x", PINF), (PINF, "1/x", "0"), ("0<sup>+</sup>", "1/x", PINF),
        ("0<sup>−</sup>", "1/x", MINF), (PINF, "e<sup>−x</sup>", "0"), (MINF, "e<sup>−x</sup>", PINF), (PINF, "√x", PINF), (MINF, "x³", MINF), (MINF, "x²", PINF),
        (PINF, "(1/2)<sup>x</sup>", "0"), (MINF, "2<sup>x</sup>", "0"), ("0<sup>+</sup>", "1/x²", PINF), ("0<sup>−</sup>", "1/x²", PINF), (PINF, "arctg x", "π/2")]


def s1_elem():
    x0, f, v = R.choice(ELEM)
    return M("Calcola %s." % lim(x0, f), v, [x for x in [PINF, MINF, "0", "1", "π/2"] if x != v][:3],
             "Dal grafico della funzione elementare %s: <b>%s</b>." % (f, v))


def s2_graf():
    a = R.randint(-2, 2)
    q = R.randint(-2, 2)
    side = R.choice(["+", "−"])
    k = R.choice([1, -1])
    f = lambda x, a=a, q=q, k=k: q + k / (x - a)
    fig = relabel(kurve([(f, BLUE, "")], (-5, 5, 1), (-6, 6, 1), W=300, H=280), "grafico della funzione")
    if R.random() < 0.5:
        v = (PINF if k > 0 else MINF) if side == "+" else (MINF if k > 0 else PINF)
        return M("%sDal grafico, quanto vale lim<sub>x→%s<sup>%s</sup></sub> f(x)?" % (fig, fq(a), side), v, [x for x in [PINF, MINF, fq(q), fq(a)] if x != v][:3],
                 "Avvicinandosi a x = %s da %s il grafico %s: <b>%s</b> (x = %s è asintoto verticale)." % (fq(a), "destra" if side == "+" else "sinistra", "sale senza limite" if v == PINF else "scende senza limite", v, fq(a)))
    return M("%sDal grafico, quanto vale lim<sub>x→+∞</sub> f(x)?" % fig, fq(q), [x for x in W(PINF, MINF, fq(a) if a != q else fq(q + 1), "0" if q else "1") if x != fq(q)],
             "Per x molto grande il grafico si avvicina alla retta y = %s: <b>%s</b> (asintoto orizzontale)." % (fq(q), fq(q)))


def s2_polyinf():
    n = R.randint(2, 5)
    cs = [nz(R, -5, 5)] + [R.randint(-9, 9) for _ in range(n)]
    x0 = R.choice([PINF, MINF])
    lead = cs[0]
    sign = 1 if lead > 0 else -1
    if x0 == MINF and n % 2 == 1:
        sign = -sign
    v = PINF if sign > 0 else MINF
    return M("Calcola %s." % lim(x0, "(%s)" % poly(cs)), v, [x for x in [PINF, MINF, "0", fq(lead)] if x != v][:3],
             "All’infinito conta il termine di grado massimo: %s → <b>%s</b>." % (poly([lead] + [0] * n), v))


def s3_razinf():
    n = R.randint(1, 3)
    m = R.choice([n - 1, n, n + 1]) if n > 1 else R.choice([n, n + 1])
    a, b = nz(R, -6, 6), nz(R, -6, 6)
    num = poly([a] + [R.randint(-5, 5) for _ in range(n)])
    den = poly([b] + [R.randint(-5, 5) for _ in range(m)])
    if n == m:
        v = fq(Fr(a, b))
        e = "Stesso grado: il limite è il rapporto dei coefficienti direttivi, %s/%s = <b>%s</b>." % (fq(a), fq(b), v)
    elif n < m:
        v = "0"
        e = "Il grado del numeratore è minore: <b>0</b>."
    else:
        v = PINF if a * b > 0 else MINF
        e = "Il grado del numeratore è maggiore: ±∞ con il segno del rapporto dei coefficienti direttivi (%s), <b>%s</b>." % (fq(Fr(a, b)), v)
    return M("Calcola %s." % lim(PINF, FR(num, den)), v, [x for x in W(PINF if v != PINF else MINF, "0" if v != "0" else fq(Fr(a, b)), fq(Fr(a, b)) if v != fq(Fr(a, b)) else "1", "1") if x != v][:3], e)


ALG = [("+∞ + 5", PINF), ("+∞ · (−3)", MINF), ("5 / (+∞)", "0"), ("(−∞) · (−∞)", PINF), ("+∞ + (+∞)", PINF), ("−∞ − 7", MINF), ("3 / 0<sup>+</sup>", PINF),
       ("−2 / 0<sup>+</sup>", MINF), ("4 / 0<sup>−</sup>", MINF), ("(+∞)<sup>2</sup>", PINF), ("0<sup>+</sup> · 7", "0"), ("+∞ − ∞", "forma indeterminata"),
       ("0 / 0", "forma indeterminata"), ("∞ / ∞", "forma indeterminata"), ("0 · ∞", "forma indeterminata"), ("1<sup>∞</sup>", "forma indeterminata")]


def s4_alg():
    f, v = R.choice(ALG)
    return M("Quanto vale (o che cos’è) %s?" % f, v, [x for x in [PINF, MINF, "0", "forma indeterminata"] if x != v][:3],
             "Regole dell’algebra dei limiti: %s → <b>%s</b>." % (f, v))


def s4_vert():
    a = nz(R, -5, 5)
    c = nz(R, -6, 6)
    side = R.choice(["+", "−"])
    sign = (1 if c > 0 else -1) * (1 if side == "+" else -1)
    v = PINF if sign > 0 else MINF
    f = FR(fq(c), P2(0, 1, -a))
    return M("Calcola lim<sub>x→%s<sup>%s</sup></sub> %s." % (fq(a), side, f), v, [x for x in [PINF, MINF, "0", fq(c)] if x != v][:3],
             "Per x → %s<sup>%s</sup> il denominatore tende a 0<sup>%s</sup> e il numeratore vale %s: <b>%s</b>." % (fq(a), side, side, fq(c), v))


def s5_succ():
    k = R.choice(["raz", "geo", "inv"])
    if k == "raz":
        a, b = nz(R, -6, 6), nz(R, 1, 6)
        c, dd = R.randint(-5, 5), R.randint(-5, 5)
        v = Fr(a, b)
        return M("Calcola il limite della successione a<sub>n</sub> = %s per n → +∞." % FR(P2(0, a, c).replace("x", "n"), P2(0, b, dd).replace("x", "n")), fq(v), [fq(x) for x in W(Fr(c, dd) if dd else Fr(c), Fr(b, a), 0, v + 1) if x != v] + [PINF],
                 "Stesso grado: rapporto dei coefficienti di n, <b>%s</b>." % fq(v))
    if k == "geo":
        q = R.choice([Fr(1, 2), Fr(2), Fr(3), Fr(-1, 3), Fr(2, 3), Fr(5, 4), Fr(1, 5)])
        v = "0" if abs(q) < 1 else PINF
        return M("Calcola lim<sub>n→+∞</sub> (%s)<sup>n</sup>." % fq(q), v, [x for x in ["0", PINF, "1", fq(q)] if x != v][:3],
                 "Una potenza qⁿ tende a 0 se |q| &lt; 1 e a +∞ se q &gt; 1: <b>%s</b>." % v)
    n = R.randint(2, 4)
    return M("Calcola lim<sub>n→+∞</sub> %s." % FR("1", "n<sup>%d</sup>" % n), "0", ["1", PINF, FR(1, n)],
             "Il denominatore cresce senza limite: <b>0</b>.")


def main():
    seen = set()
    sets = [
        ("Limiti delle funzioni elementari", mix(R, seen, [(s1_sost, 8), (s1_elem, 12)])),
        ("Leggere i limiti dal grafico", mix(R, seen, [(s2_graf, 20)])),
        ("Limiti all’infinito", mix(R, seen, [(s2_polyinf, 10), (s3_razinf, 10)])),
        ("Algebra dei limiti e limiti infiniti", mix(R, seen, [(s4_alg, 10), (s4_vert, 10)])),
        ("Limiti delle successioni", mix(R, seen, [(s5_succ, 12), (s3_razinf, 8)])),
    ]
    body = L(["lim<sub>x→x<sub>0</sub></sub> f(x) = ℓ vuol dire che f(x) si avvicina quanto si vuole a ℓ quando x si avvicina a x<sub>0</sub>. Si possono considerare il <b>limite destro</b> (x → x<sub>0</sub><sup>+</sup>) e il <b>sinistro</b> (x → x<sub>0</sub><sup>−</sup>).",
              "Se f è continua in x<sub>0</sub> (polinomi, eˣ, ln x … nel loro dominio) il limite si calcola <b>sostituendo</b>. Limiti fondamentali: eˣ → +∞ per x → +∞ ed eˣ → 0 per x → −∞; ln x → −∞ per x → 0⁺.",
              "All’infinito un polinomio si comporta come il termine di grado massimo; per un rapporto di polinomi si confrontano i gradi.",
              "Con ∞ valgono regole come +∞ + k = +∞, k/∞ = 0, k/0<sup>+</sup> = ±∞. Sono <b>forme indeterminate</b>: ∞ − ∞, 0 · ∞, 0/0, ∞/∞, 1<sup>∞</sup>."],
             [("lim<sub>x→+∞</sub> (3x² + 1)/(2x² − x)", ["Stesso grado"], "3/2"),
              ("lim<sub>x→2<sup>−</sup></sub> 1/(x − 2)", ["Denominatore → 0<sup>−</sup>"], "−∞")],
             [["1/0 = 0", "k/0<sup>±</sup> tende a ±∞, non a 0."],
              ["∞ − ∞ = 0", "È una forma indeterminata: va trasformata."],
              ["lim<sub>x→−∞</sub> eˣ = −∞", "eˣ è sempre positiva: tende a 0."]])
    faq = [("Che cos’è una forma indeterminata?", "Un’espressione come ∞ − ∞ o 0/0 il cui risultato dipende dalle funzioni coinvolte: per calcolare il limite bisogna trasformare l’espressione (raccogliere, scomporre, usare i limiti notevoli)."),
           ("Quando il limite destro e sinistro sono diversi?", "Per esempio per 1/x in 0: da destra +∞, da sinistra −∞. In quel caso il limite per x → 0 non esiste.")]
    unit(G, R, "limiti", "F",
         "Concetto di limite di una funzione e di una successione; calcolo dei limiti in casi semplici",
         "Limiti di funzioni", "Limiti",
         "Schede di matematica per la quinta liceo sui limiti: limiti delle funzioni elementari, lettura dal grafico, limite destro e sinistro, limiti all’infinito di polinomi e funzioni razionali, algebra dei limiti, limiti infiniti, successioni. 100 esercizi con soluzioni.",
         "All’infinito conta il grado massimo.", "Forme indeterminate: ∞ − ∞, 0 · ∞, 0/0, ∞/∞, 1^∞.",
         body, faq, sets, 3)


if __name__ == "__main__":
    main()
