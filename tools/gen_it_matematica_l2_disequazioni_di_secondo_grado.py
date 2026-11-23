# -*- coding: utf-8 -*-
"""
Italia Matematica seconda liceo: Disequazioni di secondo grado (Aritmetica e algebra)
  python3 tools/gen_it_matematica_l2_disequazioni_di_secondo_grado.py
Segno del trinomio di secondo grado (parabola), disequazioni con Δ > 0, Δ = 0, Δ < 0, disequazioni fratte,
disequazioni di grado superiore scomposte (studio del segno), sistemi di disequazioni.
Errori: valori interni ed esterni invertiti, dimenticare di cambiare segno se a < 0, includere gli zeri del denominatore.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, P2, FR

R = random.Random(72207)
G = "seconda-liceo"
FL = {"&gt;": "&lt;", "&lt;": "&gt;", "≥": "≤", "≤": "≥"}


def est(p, q, strict):
    o1, o2 = ("&lt;", "&gt;") if strict else ("≤", "≥")
    return "x %s %s ∨ x %s %s" % (o1, fq(p), o2, fq(q))


def intn(p, q, strict):
    o = "&lt;" if strict else "≤"
    return "%s %s x %s %s" % (fq(p), o, o, fq(q))


def s1_due():
    p, q = sorted(R.sample(range(-7, 8), 2))
    a = R.choice([1, 1, 1, 2, -1])
    b, c = -a * (p + q), a * p * q
    op = R.choice(["&gt;", "&lt;", "≥", "≤"])
    strict = op in ("&gt;", "&lt;")
    pos = op in ("&gt;", "≥")
    if a < 0:
        pos = not pos
    ans = est(p, q, strict) if pos else intn(p, q, strict)
    alt = intn(p, q, strict) if pos else est(p, q, strict)
    w = [alt, est(p, q, not strict) if pos else intn(p, q, not strict), est(-q, -p, strict) if pos else intn(-q, -p, strict)]
    return M("Risolvi: %s %s 0" % (P2(a, b, c), op), ans, [x for x in w if x != ans],
             "Zeri: x = %s e x = %s. %sIl trinomio deve essere %s: succede per valori %s agli zeri, <b>%s</b>." % (fq(p), fq(q), "Con a &lt; 0 la parabola è rivolta verso il basso. " if a < 0 else "", {"&gt;": "positivo", "≥": "positivo o nullo", "&lt;": "negativo", "≤": "negativo o nullo"}[op], "esterni" if pos else "interni", ans))


def s2_zero():
    k = R.choice(["d0", "dneg"])
    if k == "d0":
        r = nz(R, -6, 6)
        a = 1
        b, c = -2 * r, r * r
        op = R.choice(["&gt;", "≥", "&lt;", "≤"])
        ans = {"&gt;": "x ≠ %s" % fq(r), "≥": "∀x ∈ ℝ", "&lt;": "nessuna soluzione", "≤": "x = %s" % fq(r)}[op]
        e = "%s = (%s)² è sempre ≥ 0 ed è 0 solo per x = %s: <b>%s</b>." % (P2(a, b, c), P2(0, 1, -r), fq(r), ans)
    else:
        a = R.choice([1, 1, 2, -1])
        b = R.randint(-4, 4)
        c = R.randint(1, 9) * (1 if a > 0 else -1)
        if b * b - 4 * a * c >= 0:
            return None
        op = R.choice(["&gt;", "&lt;", "≥", "≤"])
        ok = (op in ("&gt;", "≥")) == (a > 0)
        ans = "∀x ∈ ℝ" if ok else "nessuna soluzione"
        e = "Δ = %s &lt; 0: il trinomio ha sempre il segno di a (%s): <b>%s</b>." % (fq(b * b - 4 * a * c), "positivo" if a > 0 else "negativo", ans)
    opts = ["∀x ∈ ℝ", "nessuna soluzione", "x ≠ %s" % fq(-b / Fr(2 * a) if a else 0), "x = %s" % fq(-b / Fr(2 * a) if a else 0)]
    return M("Risolvi: %s %s 0" % (P2(a, b, c), op), ans, [o for o in opts if o != ans], e)


def s3_fratta():
    p, q = R.sample(range(-6, 7), 2)
    op = R.choice(["&gt;", "≥", "&lt;", "≤"])
    lo, hi = sorted([p, q])
    pos = op in ("&gt;", "≥")
    # (x − p)/(x − q): zero in p (incluso se ≥/≤), q escluso sempre
    if pos:
        o1 = "≤" if (op == "≥" and lo == p) else "&lt;"
        o2 = "≥" if (op == "≥" and hi == p) else "&gt;"
        ans = "x %s %s ∨ x %s %s" % (o1, fq(lo), o2, fq(hi))
    else:
        o1 = "≤" if (op == "≤" and lo == p) else "&lt;"
        o2 = "≤" if (op == "≤" and hi == p) else "&lt;"
        ans = "%s %s x %s %s" % (fq(lo), o1, o2, fq(hi))
    alt = "%s ≤ x ≤ %s" % (fq(lo), fq(hi)) if not pos else "x ≤ %s ∨ x ≥ %s" % (fq(lo), fq(hi))
    w = [alt, ("%s &lt; x &lt; %s" % (fq(lo), fq(hi))) if pos else ("x &lt; %s ∨ x &gt; %s" % (fq(lo), fq(hi))), "x %s %s" % (op, fq(p))]
    return M("Risolvi: %s %s 0" % (FR(P2(0, 1, -p), P2(0, 1, -q)), op), ans, [x for x in w if x != ans],
             "Studio il segno di numeratore e denominatore (C.E.: x ≠ %s, sempre escluso). La frazione è %s %s: <b>%s</b>." % (fq(q), "positiva" if pos else "negativa", "fuori dagli zeri" if pos else "tra gli zeri", ans))


def s4_terzo():
    a, b, c = sorted(R.sample(range(-5, 6), 3))
    op = R.choice(["&gt;", "&lt;"])
    if op == "&gt;":
        ans = "%s &lt; x &lt; %s ∨ x &gt; %s" % (fq(a), fq(b), fq(c))
        w = ["x &lt; %s ∨ %s &lt; x &lt; %s" % (fq(a), fq(b), fq(c)), "x &gt; %s" % fq(c), "%s &lt; x &lt; %s" % (fq(a), fq(c))]
    else:
        ans = "x &lt; %s ∨ %s &lt; x &lt; %s" % (fq(a), fq(b), fq(c))
        w = ["%s &lt; x &lt; %s ∨ x &gt; %s" % (fq(a), fq(b), fq(c)), "x &lt; %s" % fq(a), "%s &lt; x &lt; %s" % (fq(b), fq(c))]
    q = "%s %s 0" % ("".join("x" if r == 0 else "(%s)" % P2(0, 1, -r) for r in (a, b, c)), op)
    q = q.replace(")x(", ")·x·(") if False else q
    return M("Risolvi: %s" % q, ans, w, "Tre fattori: il segno è + a destra di %s e cambia a ogni zero (−, +, −, + da sinistra): <b>%s</b>." % (fq(c), ans))


def s5_sist():
    p, q = sorted(R.sample(range(-6, 7), 2))
    t = R.randint(-6, 6)
    k = R.choice(["int_gt", "est_lt"])
    if k == "int_gt":
        # p < x < q  e  x > t
        lo = max(p, t)
        if lo >= q:
            ans = "nessuna soluzione"
        else:
            ans = "%s &lt; x &lt; %s" % (fq(lo), fq(q))
        e1 = "%s &lt; 0" % P2(1, -(p + q), p * q)
        e2 = "x &gt; %s" % fq(t)
        w = ["%s &lt; x &lt; %s" % (fq(p), fq(q)), "x &gt; %s" % fq(t), "x &lt; %s ∨ x &gt; %s" % (fq(p), fq(q)), "nessuna soluzione", "%s &lt; x &lt; %s" % (fq(t), fq(q)) if t < q else "x &gt; %s" % fq(q)]
    else:
        # x < p ∨ x > q  e  x < t
        if t <= p:
            ans = "x &lt; %s" % fq(t)
        elif t <= q:
            ans = "x &lt; %s" % fq(p)
        else:
            ans = "x &lt; %s ∨ %s &lt; x &lt; %s" % (fq(p), fq(q), fq(t))
        e1 = "%s &gt; 0" % P2(1, -(p + q), p * q)
        e2 = "x &lt; %s" % fq(t)
        w = ["x &lt; %s ∨ x &gt; %s" % (fq(p), fq(q)), "x &lt; %s" % fq(t) if ans != "x &lt; %s" % fq(t) else "x &lt; %s" % fq(q), "%s &lt; x &lt; %s" % (fq(p), fq(q)), "nessuna soluzione"]
    return M("Risolvi il sistema: <span class='sys'>%s<br>%s</span>" % (e1, e2), ans, [x for x in w if x != ans],
             "Risolvo le due disequazioni e prendo l’intersezione delle soluzioni: <b>%s</b>." % ans)


def main():
    seen = set()
    sets = [
        ("Disequazioni con due zeri", mix(R, seen, [(s1_due, 20)])),
        ("Δ = 0 e Δ < 0", mix(R, seen, [(s2_zero, 14), (s1_due, 6)])),
        ("Disequazioni fratte", mix(R, seen, [(s3_fratta, 20)])),
        ("Grado superiore", mix(R, seen, [(s4_terzo, 12), (s3_fratta, 8)])),
        ("Sistemi di disequazioni", mix(R, seen, [(s5_sist, 16), (s2_zero, 4)])),
    ]
    body = L(["Il segno di ax² + bx + c si legge dalla <b>parabola</b>: se a &gt; 0 è rivolta verso l’alto. Con Δ &gt; 0 e zeri x<sub>1</sub> &lt; x<sub>2</sub>, il trinomio ha il segno di a per valori <b>esterni</b> e segno opposto per valori <b>interni</b>.",
              "Se Δ = 0 il trinomio ha sempre il segno di a, tranne nello zero doppio dove vale 0. Se Δ &lt; 0 ha sempre il segno di a.",
              "Nelle disequazioni <b>fratte</b> si studia il segno di numeratore e denominatore separatamente e si usa la regola dei segni. Gli zeri del denominatore sono sempre esclusi.",
              "Nei <b>sistemi</b> si risolve ogni disequazione e si prende l’intersezione."],
             [("x² − 5x + 6 &gt; 0", ["Zeri 2 e 3; a &gt; 0"], "x &lt; 2 ∨ x &gt; 3"),
              ("(x − 1)/(x + 2) ≤ 0", ["N ≥ 0 per x ≥ 1, D &gt; 0 per x &gt; −2"], "−2 &lt; x ≤ 1")],
             [["x² − 4 &gt; 0 → x &gt; ±2", "Le soluzioni sono esterne: x &lt; −2 ∨ x &gt; 2."],
              ["Non considerare a &lt; 0", "Con a negativo si scambiano interni ed esterni (o si moltiplica per −1 cambiando verso)."],
              ["Includere lo zero del denominatore", "Il denominatore non può essere 0: quel valore è sempre escluso."]],
             table(["", "a &gt; 0", "a &lt; 0"], [["Δ &gt; 0", "&gt; 0 esterni, &lt; 0 interni", "&lt; 0 esterni, &gt; 0 interni"], ["Δ = 0", "≥ 0 sempre (0 nello zero)", "≤ 0 sempre"], ["Δ &lt; 0", "&gt; 0 sempre", "&lt; 0 sempre"]]))
    faq = [("Perché si guarda la parabola?", "Perché y = ax² + bx + c è una parabola: dove sta sopra l’asse x il trinomio è positivo, dove sta sotto è negativo. Gli zeri sono i punti di intersezione con l’asse x."),
           ("In una disequazione fratta si può moltiplicare per il denominatore?", "No, perché non se ne conosce il segno: il verso potrebbe dover cambiare. Si studia invece il segno di numeratore e denominatore.")]
    unit(G, R, "disequazioni-di-secondo-grado", "A",
         "Disequazioni di secondo grado, fratte e di grado superiore; sistemi di disequazioni",
         "Disequazioni di secondo grado", "Disequazioni di secondo grado",
         "Schede di matematica per la seconda liceo sulle disequazioni di secondo grado: segno del trinomio, casi Δ > 0, Δ = 0, Δ < 0, disequazioni fratte, di grado superiore e sistemi. 100 esercizi con soluzioni.",
         "Concorde con a all’esterno, discorde all’interno.", "Con Δ < 0 il trinomio ha sempre il segno di a.",
         body, faq, sets, 7)


if __name__ == "__main__":
    main()
