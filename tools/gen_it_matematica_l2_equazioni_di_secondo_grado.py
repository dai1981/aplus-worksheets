# -*- coding: utf-8 -*-
"""
Italia Matematica seconda liceo: Equazioni di secondo grado (Aritmetica e algebra)
  python3 tools/gen_it_matematica_l2_equazioni_di_secondo_grado.py
Equazioni pure, spurie e complete, formula risolutiva (anche ridotta), discriminante e numero di soluzioni, radici irrazionali,
somma e prodotto delle radici, equazione date le radici, scomposizione del trinomio, parametro per radici coincidenti, problemi.
Errori: x² = 9 → x = 3 soltanto, perdere x = 0 nelle spurie, −b con il segno sbagliato, Δ = b² + 4ac.
"""
import math
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, P2, sol, FR, simp_root

R = random.Random(72206)
G = "seconda-liceo"


def s1_pura():
    k = R.choice(["pos", "neg", "irr"])
    a = R.choice([1, 1, 2, 3, 4])
    if k == "pos":
        r = R.randint(1, 9)
        c = -a * r * r
        ans, w = sol([r, -r]), [sol([r]), sol([r * r, -r * r]), "impossibile"]
        e = "%s → x² = %d → <b>%s</b> (due soluzioni opposte)." % (P2(a, 0, c), r * r, ans)
    elif k == "neg":
        c = a * R.randint(1, 9)
        ans, w = "impossibile in ℝ", [sol([math.isqrt(c // a) or 1]), sol([c // a, -(c // a)]), "x = 0"]
        e = "x² = −%d: un quadrato non è mai negativo, quindi è <b>impossibile in ℝ</b>." % (c // a)
    else:
        n = R.choice([2, 3, 5, 6, 7, 8, 12, 18, 20])
        c = -a * n
        kk, m = simp_root(n)
        rr = ("" if kk == 1 else str(kk)) + "√" + str(m)
        ans, w = "x = ±%s" % rr, ["x = %s" % rr, "x = ±%d" % n, "x = ±%s" % ("√%d" % (2 * n))]
        e = "x² = %d → <b>x = ±%s</b>." % (n, rr)
    return M("Risolvi: %s = 0" % P2(a, 0, c), ans, w, e)


def s1_spuria():
    a = nz(R, -5, 5)
    r = Fr(nz(R, -9, 9), R.choice([1, 1, 1, 2, 3]))
    b = -a * r
    if b.denominator != 1:
        return None
    ans = sol([0, r])
    return M("Risolvi: %s = 0" % P2(a, b, 0), ans, [sol([r]), sol([0, -r]), sol([-r, r])],
             "Raccolgo x: x(%s) = 0 → x = 0 oppure x = %s: <b>%s</b>." % (P2(0, a, b), fq(r), ans))


def roots_eq():
    a = R.choice([1, 1, 1, 2, 3, -1])
    p, q = R.sample(range(-8, 9), 2)
    if R.random() < 0.3:
        p = Fr(nz(R, -5, 5), R.choice([2, 3]))
        if p.denominator != 1 and a % p.denominator != 0:
            a = p.denominator * R.choice([1, 1, -1])
    b, c = -a * (p + q), a * p * q
    return a, Fr(b), Fr(c), p, q


def s2_compl():
    a, b, c, p, q = roots_eq()
    if b.denominator != 1 or c.denominator != 1 or p == q or p == 0 or q == 0 or p == -q:
        return None
    ans = sol([p, q])
    w = [sol([-p, -q]), sol([p, -q]), sol([Fr(-b + 1, 2 * a), Fr(-b - 1, 2 * a)]) if False else sol([Fr(b, a) - p, q]) if Fr(b, a) - p != p else sol([p + 1, q])]
    D = b * b - 4 * a * c
    return M("Risolvi: %s = 0" % P2(a, b, c), ans, [x for x in w if x != ans],
             "Δ = b² − 4ac = %s, √Δ = %s; x = (−b ± √Δ)/(2a) = (%s ± %s)/%s: <b>%s</b>." % (fq(D), fq(Fr(math.isqrt(int(D)))), fq(-b), fq(Fr(math.isqrt(int(D)))), fq(2 * a), ans))


def s2_irr():
    a = 1
    b = R.choice([-6, -4, -2, 2, 4, 6, -8, 8])
    c = R.randint(-9, 9)
    dq = (b // 2) ** 2 - c
    if dq <= 0 or math.isqrt(dq) ** 2 == dq:
        return None
    k, m = simp_root(dq)
    rr = ("" if k == 1 else str(k)) + "√" + str(m)
    h = -b // 2
    ans = "x = %s ± %s" % (fq(h), rr) if h else "x = ±%s" % rr
    w = ["x = %s ± %s" % (fq(-h), rr), "x = %s ± √%d" % (fq(h), b * b - 4 * c), "x = %s ± %s" % (fq(h), ("" if 2 * k == 1 else str(2 * k)) + "√" + str(m))]
    return M("Risolvi: %s = 0" % P2(a, b, c), ans, w,
             "b è pari: formula ridotta, Δ/4 = (b/2)² − ac = %d; x = −b/2 ± √(Δ/4) = <b>%s</b>." % (dq, ans))


def s3_delta():
    a, b, c = nz(R, -4, 4), R.randint(-8, 8), R.randint(-8, 8)
    D = b * b - 4 * a * c
    ans = "due soluzioni reali distinte" if D > 0 else "due soluzioni coincidenti" if D == 0 else "nessuna soluzione reale"
    return M("Quante soluzioni reali ha l’equazione %s = 0?" % P2(a, b, c), ans, [o for o in ["due soluzioni reali distinte", "due soluzioni coincidenti", "nessuna soluzione reale", "infinite soluzioni"] if o != ans],
             "Δ = b² − 4ac = %s %s 0: <b>%s</b>." % (fq(D), "&gt;" if D > 0 else "=" if D == 0 else "&lt;", ans))


def s3_sp():
    a, b, c, p, q = roots_eq()
    if b.denominator != 1 or c.denominator != 1:
        return None
    k = R.choice(["s", "p"])
    if k == "s":
        v = -b / a
        return M("Senza risolvere, quanto vale la somma delle radici di %s = 0?" % P2(a, b, c), fq(v), [fq(x) for x in (b / a, c / a, -c / a) if x != v] + [fq(v + 1)],
                 "x<sub>1</sub> + x<sub>2</sub> = −b/a = <b>%s</b>." % fq(v))
    v = c / a
    return M("Senza risolvere, quanto vale il prodotto delle radici di %s = 0?" % P2(a, b, c), fq(v), [fq(x) for x in (-b / a, -c / a, b / a) if x != v] + [fq(v + 1)],
             "x<sub>1</sub> · x<sub>2</sub> = c/a = <b>%s</b>." % fq(v))


def s4_scrivi():
    p, q = R.sample(range(-7, 8), 2)
    s, pr = p + q, p * q
    ans = "%s = 0" % P2(1, -s, pr)
    return M("Scrivi un’equazione di secondo grado che ha per soluzioni %s e %s." % (fq(p), fq(q)), ans, ["%s = 0" % P2(1, s, pr), "%s = 0" % P2(1, -pr, s), "%s = 0" % P2(1, s, -pr), "%s = 0" % P2(1, -s, -pr), "%s = 0" % P2(1, -s - 1, pr)],
             "x² − sx + p = 0 con s = %s e p = %s: <b>%s</b>." % (fq(s), fq(pr), ans))


def s4_scomp():
    a = R.choice([2, 3, 4, 5, -2])
    p = Fr(nz(R, -4, 4), abs(a))
    q = Fr(nz(R, -5, 5))
    if p == q or p.denominator == 1:
        return None
    b, c = -a * (p + q), a * p * q
    if b.denominator != 1 or c.denominator != 1:
        return None
    f1 = "(%s)" % P2(0, abs(a) if a > 0 else -a, -p * abs(a))
    if a < 0:
        f1 = "(%s)" % P2(0, -a, p * a)
        ans = "−%s(%s)" % (f1, P2(0, 1, -q))
    else:
        ans = "%s(%s)" % (f1, P2(0, 1, -q))
    ans = ans.replace("(" + P2(0, 1, -q) + ")", "(%s)" % P2(0, 1, -q))
    w = ["%d(%s)(%s)" % (a, P2(0, 1, -p), P2(0, 1, -q)) if False else "(%s)(%s)" % (P2(0, 1, -p), P2(0, 1, -q)), "%s(%s)" % (f1, P2(0, 1, q)), "(%s)(%s)" % (P2(0, a, p * a), P2(0, 1, -q))]
    return M("Scomponi il trinomio %s." % P2(a, b, c), ans, [x for x in w if x != ans],
             "Le radici sono %s e %s; ax² + bx + c = a(x − x<sub>1</sub>)(x − x<sub>2</sub>) = <b>%s</b>." % (fq(p), fq(q), ans))


def s5_param():
    b = R.choice([2, 4, 6, 8, 10, -4, -6])
    k = Fr(b * b, 4)
    return M("Per quale valore di k l’equazione x² %s %dx + k = 0 ha due soluzioni coincidenti?" % ("+" if b > 0 else "−", abs(b)), "k = %s" % fq(k),
             ["k = %s" % fq(v) for v in W(b * b, Fr(b, 2), -k, k + 1, 2 * k)], "Radici coincidenti se Δ = 0: %d − 4k = 0 → <b>k = %s</b>." % (b * b, fq(k)))


def s5_probl():
    k = R.choice(["rett", "cons", "quad"])
    if k == "rett":
        x = R.randint(3, 12)
        dd = R.randint(1, 6)
        A = x * (x + dd)
        q = "Un rettangolo ha l’area di %d cm² e la base supera l’altezza di %d cm. Quanto misura l’altezza?" % (A, dd)
        return M(q, "%d cm" % x, ["%s cm" % v for v in W(x + dd, A // (x + dd + 1) if A % (x + dd + 1) == 0 else x - 1, math.isqrt(A), x + 1)],
                 "x(x + %d) = %d → %s = 0 → x = %d (la soluzione negativa si scarta): <b>%d cm</b>." % (dd, A, P2(1, dd, -A), x, x))
    if k == "cons":
        n = R.randint(3, 20)
        pr = n * (n + 1)
        q = "Il prodotto di due numeri naturali consecutivi è %d. Qual è il minore?" % pr
        return M(q, str(n), W(n + 1, n - 1, math.isqrt(pr) + 1 if math.isqrt(pr) + 1 != n + 1 else n + 2),
                 "x(x + 1) = %d → %s = 0 → <b>x = %d</b> (l’altra soluzione, −%d, non è naturale)." % (pr, P2(1, 1, -pr), n, n + 1))
    n = R.randint(2, 12)
    s = R.randint(2, 10)
    v = n * n + s * n
    q = "Il quadrato di un numero positivo, aumentato di %d volte il numero stesso, dà %d. Qual è il numero?" % (s, v)
    return M(q, str(n), W(n + 1, n + s, v // s if v // s != n else n + 2, n - 1, n + 2), "x² + %dx = %d → %s = 0 → <b>x = %d</b> (scarto la soluzione negativa)." % (s, v, P2(1, s, -v), n))


def main():
    seen = set()
    sets = [
        ("Equazioni pure e spurie", mix(R, seen, [(s1_pura, 10), (s1_spuria, 10)])),
        ("Formula risolutiva", mix(R, seen, [(s2_compl, 20)])),
        ("Discriminante e radici irrazionali", mix(R, seen, [(s3_delta, 10), (s2_irr, 10)])),
        ("Somma, prodotto e scomposizione", mix(R, seen, [(s3_sp, 8), (s4_scrivi, 6), (s4_scomp, 6)])),
        ("Parametri e problemi", mix(R, seen, [(s5_param, 6), (s5_probl, 14)])),
    ]
    body = L(["Forma normale: ax² + bx + c = 0 con a ≠ 0. <b>Pura</b> (b = 0): x² = −c/a. <b>Spuria</b> (c = 0): x(ax + b) = 0, quindi x = 0 e x = −b/a.",
              "<b>Formula risolutiva</b>: x = (−b ± √Δ)/(2a), con Δ = b² − 4ac. Se b è pari conviene la formula ridotta: x = (−b/2 ± √(Δ/4))/a.",
              "Δ &gt; 0: due soluzioni distinte; Δ = 0: due coincidenti; Δ &lt; 0: nessuna soluzione reale.",
              "Somma e prodotto delle radici: x<sub>1</sub> + x<sub>2</sub> = −b/a, x<sub>1</sub> · x<sub>2</sub> = c/a. Il trinomio si scompone: ax² + bx + c = a(x − x<sub>1</sub>)(x − x<sub>2</sub>)."],
             [("x² − 5x + 6 = 0", ["Δ = 25 − 24 = 1", "x = (5 ± 1)/2"], "x = 2 ∨ x = 3"),
              ("3x² − 12x = 0", ["3x(x − 4) = 0"], "x = 0 ∨ x = 4")],
             [["x² = 16 → x = 4", "Le soluzioni sono due: x = ±4."],
              ["Dividere per x nelle spurie", "Si perde x = 0: raccogli x e usa la legge di annullamento."],
              ["Δ = b² + 4ac", "Δ = b² − 4ac; attenzione ai segni di a e c."]])
    faq = [("Quando conviene la formula ridotta?", "Quando il coefficiente b è pari: si lavora con numeri più piccoli. x = (−b/2 ± √((b/2)² − ac))/a dà le stesse soluzioni della formula completa."),
           ("Che cosa vuol dire Δ &lt; 0?", "Che sotto la radice c’è un numero negativo: l’equazione non ha soluzioni reali e il trinomio ax² + bx + c non si scompone nei reali.")]
    unit(G, R, "equazioni-di-secondo-grado", "A",
         "Equazioni di secondo grado: formula risolutiva, discriminante, relazioni tra radici e coefficienti, scomposizione del trinomio, problemi",
         "Equazioni di secondo grado", "Equazioni di secondo grado",
         "Schede di matematica per la seconda liceo sulle equazioni di secondo grado: pure e spurie, formula risolutiva e ridotta, discriminante, somma e prodotto delle radici, scomposizione del trinomio, parametri, problemi. 100 esercizi con soluzioni.",
         "x = (−b ± √Δ)/(2a), Δ = b² − 4ac", "Δ > 0 due soluzioni, Δ = 0 coincidenti, Δ < 0 nessuna soluzione reale.",
         body, faq, sets, 6)


if __name__ == "__main__":
    main()
