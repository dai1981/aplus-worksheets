# -*- coding: utf-8 -*-
"""
Italia Matematica terza liceo: Equazioni e disequazioni con valore assoluto e irrazionali (Aritmetica e algebra)
  python3 tools/gen_it_matematica_l3_equazioni_e_disequazioni_con_valore_assoluto_e_irrazionali.py
|A(x)| = k, |A(x)| = |B(x)|, |A(x)| < k e > k, |A(x)| = B(x); equazioni irrazionali √A = B (condizioni e verifica),
√A = k, disequazioni irrazionali √A < k, √A > k, √A ≥ B nei casi semplici, biquadratiche e binomie.
Errori: |x − 3| < 5 → x < 8 soltanto, accettare soluzioni estranee nelle irrazionali, dimenticare A ≥ 0.
"""
import math
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, P2, sol

R = random.Random(72301)
G = "terza-liceo"


def lin(a, b):
    return P2(0, a, b)


def s1_abs_eq():
    a = R.choice([1, 1, 2, 3])
    b = R.randint(-8, 8)
    k = R.randint(1, 9)
    r1, r2 = Fr(k - b, a), Fr(-k - b, a)
    ans = sol([r1, r2])
    k2 = R.choice(["pos", "neg", "zero"]) if R.random() < 0.3 else "pos"
    if k2 == "neg":
        return M("Risolvi: |%s| = −%d" % (lin(a, b), k), "impossibile", [sol([r1, r2]), sol([r1]), sol([Fr(-b, a)])],
                 "Un valore assoluto non è mai negativo: <b>impossibile</b>.")
    if k2 == "zero":
        z = Fr(-b, a)
        return M("Risolvi: |%s| = 0" % lin(a, b), sol([z]), [sol([z, -z]) if z else "impossibile", "impossibile", "∀x ∈ ℝ"],
                 "|A| = 0 solo se A = 0: <b>%s</b>." % sol([z]))
    return M("Risolvi: |%s| = %d" % (lin(a, b), k), ans, [sol([r1]), sol([-r1, -r2]) if (-r1, -r2) != (r1, r2) else "impossibile", sol([Fr(k + b, a), Fr(-k + b, a)])],
             "|A| = %d ⟺ A = %d ∨ A = −%d: %s = ±%d → <b>%s</b>." % (k, k, k, lin(a, b), k, ans))


def s1_abs_dis():
    c = R.randint(-6, 6)
    k = R.randint(1, 8)
    op = R.choice(["&lt;", "≤", "&gt;", "≥"])
    lo, hi = c - k, c + k
    xs = "x − %d" % c if c > 0 else ("x + %d" % -c if c < 0 else "x")
    if op in ("&lt;", "≤"):
        ans = "%s %s x %s %s" % (fq(lo), op, op, fq(hi))
        w = ["x %s %s" % (op, fq(hi)), "x %s %s ∨ x %s %s" % (op, fq(lo), {"&lt;": "&gt;", "≤": "≥"}[op], fq(hi)), "%s %s x %s %s" % (fq(-k), op, op, fq(k)) if c else "%s %s x %s %s" % (fq(lo - 1), op, op, fq(hi + 1))]
        e = "|A| %s k ⟺ −k %s A %s k: %s %s %s %s %s → <b>%s</b>." % (op, op, op, fq(-k), op, xs, op, fq(k), ans)
    else:
        lop = {"&gt;": "&lt;", "≥": "≤"}[op]
        ans = "x %s %s ∨ x %s %s" % (lop, fq(lo), op, fq(hi))
        w = ["%s %s x %s %s" % (fq(lo), lop, lop, fq(hi)), "x %s %s" % (op, fq(hi)), "x %s %s ∨ x %s %s" % (lop, fq(-k), op, fq(k)) if c else "x %s %s" % (op, fq(lo))]
        e = "|A| %s k ⟺ A %s −k ∨ A %s k: <b>%s</b>." % (op, lop, op, ans)
    return M("Risolvi: |%s| %s %d" % (xs, op, k), ans, [x for x in w if x != ans], e)


def s2_abs_b():
    a, b = R.sample(range(-6, 7), 2)
    # |x − a| = |x − b| → x = (a + b)/2
    xa = "x − %d" % a if a > 0 else ("x + %d" % -a if a < 0 else "x")
    xb = "x − %d" % b if b > 0 else ("x + %d" % -b if b < 0 else "x")
    m = Fr(a + b, 2)
    return M("Risolvi: |%s| = |%s|" % (xa, xb), sol([m]), [sol([a, b]), sol([Fr(a - b, 2)]) if Fr(a - b, 2) != m else "impossibile", "impossibile" if m != 0 else sol([1]), sol([-m]) if m else sol([2])],
             "|A| = |B| ⟺ A = B ∨ A = −B. A = B è impossibile (%d ≠ %d); A = −B dà 2x = %s: <b>%s</b> (il punto medio tra %s e %s)." % (-a, -b, fq(a + b), sol([m]), fq(a), fq(b)))


def s3_irr():
    # √(x + a) = x + b, costruito da una soluzione accettabile r
    r = R.randint(-3, 8)
    b = R.randint(-4, 4)
    if r + b < 0:
        return None
    a = (r + b) ** 2 - r
    # x + a = (x + b)² → x² + (2b − 1)x + b² − a = 0
    B, C = 2 * b - 1, b * b - a
    D = B * B - 4 * C
    s_ = math.isqrt(D)
    if s_ * s_ != D:
        return None
    roots = sorted(set([Fr(-B + s_, 2), Fr(-B - s_, 2)]))
    good = [t for t in roots if t + b >= 0 and t + a >= 0]
    bad = [t for t in roots if t not in good]
    ans = sol(good) if good else "impossibile"
    rhs = lin(1, b) if b else "x"
    w = [sol(roots) if bad else sol([-t for t in good]), "impossibile" if good else sol(roots), sol([good[0] + 1]) if good else sol([1])]
    return M("Risolvi: √(%s) = %s" % (lin(1, a) if a else "x", rhs), ans, [x for x in w if x != ans],
             "Condizione: %s ≥ 0. Elevo al quadrato: %s = 0 → %s. %s" % (rhs, P2(1, B, C), sol(roots), ("Scarto %s (rende %s negativo). Soluzione: <b>%s</b>." % (sol(bad), rhs, ans)) if bad else "Sono accettabili: <b>%s</b>." % ans))


def s3_irr_k():
    a = R.choice([1, 2, 3])
    k = R.randint(1, 6)
    b = R.randint(-9, 9)
    x = Fr(k * k - b, a)
    neg = R.random() < 0.25
    if neg:
        return M("Risolvi: √(%s) = −%d" % (lin(a, b), k), "impossibile", [sol([x]), sol([Fr(-k * k - b, a)]), sol([Fr(k - b, a)])],
                 "Una radice quadrata non è mai negativa: <b>impossibile</b>.")
    return M("Risolvi: √(%s) = %d" % (lin(a, b), k), sol([x]), [sol([Fr(k - b, a)]), sol([Fr(-k * k - b, a)]), sol([x, -x]) if x else sol([1])],
             "Elevo al quadrato (il secondo membro è positivo): %s = %d → <b>%s</b>." % (lin(a, b), k * k, sol([x])))


def s4_irr_dis():
    a = R.randint(-6, 6)
    k = R.randint(1, 5)
    op = R.choice(["&lt;", "≤", "&gt;", "≥"])
    xs = "x − %d" % a if a > 0 else ("x + %d" % -a if a < 0 else "x")
    if op in ("&lt;", "≤"):
        ans = "%s ≤ x %s %s" % (fq(a), op, fq(a + k * k))
        w = ["x %s %s" % (op, fq(a + k * k)), "%s ≤ x %s %s" % (fq(a), op, fq(a + k)), "x ≥ %s" % fq(a)]
        e = "Condizione di esistenza x ≥ %s; elevo al quadrato: %s %s %d → x %s %s. Insieme: <b>%s</b>." % (fq(a), xs, op, k * k, op, fq(a + k * k), ans)
    else:
        ans = "x %s %s" % (op, fq(a + k * k))
        w = ["x %s %s" % (op, fq(a + k)), "%s ≤ x %s %s" % (fq(a), {"&gt;": "&lt;", "≥": "≤"}[op], fq(a + k * k)), "x ≥ %s" % fq(a)]
        e = "Elevo al quadrato (le soluzioni rispettano già x ≥ %s): %s %s %d → <b>%s</b>." % (fq(a), xs, op, k * k, ans)
    return M("Risolvi: √(%s) %s %d" % (xs, op, k), ans, [x for x in w if x != ans], e)


def s5_biq():
    p, q = R.sample([1, 4, 9, 16, 25], 2)
    k = R.choice(["4", "neg"])
    if k == "4":
        a, b = int(math.isqrt(p)), int(math.isqrt(q))
        ans = sol([a, -a, b, -b])
        return M("Risolvi l’equazione biquadratica: %s = 0" % P2(1, -(p + q), p * q).replace("x²", "x⁴", 1).replace(" x", " x²", 1).replace("x ", "x² ", 1) if False else "Risolvi l’equazione biquadratica: x⁴ %s %dx² %s %d = 0" % ("−" if p + q > 0 else "+", p + q, "+", p * q),
                 ans, [sol([a, b]), sol([p, q]), sol([p, -p, q, -q])],
                 "Pongo t = x²: t² − %dt + %d = 0 → t = %d ∨ t = %d → x² = %d ∨ x² = %d: <b>%s</b>." % (p + q, p * q, p, q, p, q, ans))
    a = int(math.isqrt(p))
    return M("Risolvi: x⁴ %s %dx² − %d = 0" % ("−" if p - q > 0 else "+", abs(p - q), p * q), sol([a, -a]),
             [sol([a, -a, int(math.isqrt(q)), -int(math.isqrt(q))]), sol([p, -q]), "impossibile"],
             "t = x²: t² %s %dt − %d = 0 → t = %d ∨ t = −%d. x² = −%d è impossibile, quindi x² = %d: <b>%s</b>." % ("−" if p - q > 0 else "+", abs(p - q), p * q, p, q, q, p, sol([a, -a])))


def s5_bin():
    n = R.choice([3, 3, 4, 5])
    if n == 4:
        b = R.randint(1, 4)
        return M("Risolvi: x⁴ = %d" % b ** 4, sol([b, -b]), [sol([b]), sol([b ** 2, -b ** 2]), "x = ±%d" % (b ** 4 // 4) if b > 1 else "impossibile"],
                 "Esponente pari: x = ±⁴√%d = <b>±%d</b>." % (b ** 4, b))
    b = R.randint(-4, 4)
    if b == 0:
        return None
    v = b ** n
    return M("Risolvi: x%s = %s" % ("³" if n == 3 else "⁵", fq(v)), sol([b]), [sol([b, -b]), sol([-b]), "impossibile"],
             "Esponente dispari: una sola soluzione reale, con lo stesso segno: <b>x = %s</b>." % fq(b))


def main():
    seen = set()
    sets = [
        ("Equazioni con il valore assoluto", mix(R, seen, [(s1_abs_eq, 14), (s2_abs_b, 6)])),
        ("Disequazioni con il valore assoluto", mix(R, seen, [(s1_abs_dis, 20)])),
        ("Equazioni irrazionali", mix(R, seen, [(s3_irr, 12), (s3_irr_k, 8)])),
        ("Disequazioni irrazionali", mix(R, seen, [(s4_irr_dis, 20)])),
        ("Equazioni biquadratiche e binomie", mix(R, seen, [(s5_biq, 10), (s5_bin, 10)])),
    ]
    body = L(["<b>Valore assoluto</b>: |A| = A se A ≥ 0, |A| = −A se A &lt; 0. Allora |A| = k (k &gt; 0) ⟺ A = ±k; |A| &lt; k ⟺ −k &lt; A &lt; k; |A| &gt; k ⟺ A &lt; −k ∨ A &gt; k.",
              "Un’equazione <b>irrazionale</b> √A = B si risolve elevando al quadrato con le condizioni A ≥ 0 e B ≥ 0, oppure controllando alla fine le soluzioni (alcune possono essere estranee).",
              "√A &lt; k (k &gt; 0) ⟺ 0 ≤ A &lt; k². √A &gt; k ⟺ A &gt; k².",
              "Le equazioni <b>biquadratiche</b> ax⁴ + bx² + c = 0 si risolvono ponendo t = x². Le <b>binomie</b> xⁿ = a hanno due soluzioni opposte se n è pari e a &gt; 0, una sola se n è dispari."],
             [("|2x − 1| &lt; 5", ["−5 &lt; 2x − 1 &lt; 5", "−4 &lt; 2x &lt; 6"], "−2 &lt; x &lt; 3"),
              ("√(x + 7) = x + 1", ["x + 1 ≥ 0", "x + 7 = x² + 2x + 1 → x² + x − 6 = 0 → x = 2 ∨ x = −3"], "x = 2 (−3 si scarta)")],
             [["|x − 3| &lt; 5 → x &lt; 8", "Il valore assoluto dà due condizioni: −2 &lt; x &lt; 8."],
              ["Non controllare le soluzioni", "Elevando al quadrato compaiono soluzioni estranee: verifica B ≥ 0."],
              ["√(x − 2) &lt; 3 → x &lt; 11", "Serve anche la condizione di esistenza: 2 ≤ x &lt; 11."]])
    faq = [("Perché elevando al quadrato compaiono soluzioni in più?", "Perché A = B e A = −B hanno lo stesso quadrato: l’equazione A² = B² contiene anche le soluzioni di A = −B, che non risolvono quella di partenza."),
           ("Che significato geometrico ha |x − a|?", "È la distanza tra x e a sulla retta. Così |x − 2| &lt; 3 vuol dire «x dista da 2 meno di 3», cioè −1 &lt; x &lt; 5.")]
    unit(G, R, "equazioni-e-disequazioni-con-valore-assoluto-e-irrazionali", "A",
         "Equazioni e disequazioni con valori assoluti e irrazionali; equazioni di grado superiore (biquadratiche, binomie)",
         "Equazioni e disequazioni con valore assoluto e irrazionali", "Valore assoluto e irrazionali",
         "Schede di matematica per la terza liceo su equazioni e disequazioni con valore assoluto e irrazionali: |A| = k, |A| < k, |A| > k, √A = B con verifica, √A < k, √A > k, equazioni biquadratiche e binomie. 100 esercizi con soluzioni.",
         "|A| < k ⟺ −k < A < k", "Nelle irrazionali: condizioni di esistenza e verifica delle soluzioni.",
         body, faq, sets, 1)


if __name__ == "__main__":
    main()
