# -*- coding: utf-8 -*-
"""
Italia Matematica prima liceo: Scomposizione in fattori (Aritmetica e algebra)
  python3 tools/gen_it_matematica_l1_scomposizione_in_fattori.py
Raccoglimento totale e parziale, differenza di due quadrati, trinomio quadrato di un binomio, trinomio di secondo grado
(somma e prodotto), somma e differenza di cubi, scomposizioni in più passaggi.
Errori: raccogliere solo una parte, segni nel trinomio, a² + b² scomponibile, a³ − b³ = (a − b)(a² + 2ab + b²).
"""
import math
import random
from it_liceo import M, L, unit, mix, table, W, fq, nz, P, show

R = random.Random(72105)
G = "prima-liceo"


def lin(a, v, b):
    return show(P([(a, {v: 1}), (b, {})]))


def f(*ps):
    return "".join("(%s)" % p for p in ps)


def s1_racc():
    g = R.choice([2, 3, 4, 5, 6])
    e = R.randint(1, 3)
    v = R.choice(["x", "a"])
    a, b = nz(R, -7, 7), nz(R, -7, 7)
    k = R.randint(1, 2)
    if abs(a) == abs(b) or (a % 2 == 0 and b % 2 == 0) or (a % 3 == 0 and b % 3 == 0):
        return None
    p = P([(g * a, {v: e + k}), (g * b, {v: e})])
    inner = show(P([(a, {v: k}), (b, {})]))
    gm = show(P([(g, {v: e})]))
    ans = "%s(%s)" % (gm, inner)
    w = ["%s(%s)" % (show(P([(g, {v: e + k})])), show(P([(a, {}), (b, {v: -k})]))) if False else "%s(%s)" % (show(P([(g, {})])), show(P([(a, {v: e + k}), (b, {v: e})]))),
         "%s(%s)" % (gm, show(P([(a, {v: k}), (-b, {})]))), "%s(%s)" % (show(P([(g, {v: e - 1})])) if e > 1 else show(P([(1, {v: 1})])), show(P([(a, {v: k + 1}), (b, {v: 1})]))) if (e > 1 or g == 1) else "%s(%s)" % (show(P([(g * 2, {v: e})])), show(P([(a, {v: k}), (b, {})])))]
    return M("Scomponi con il raccoglimento totale: %s" % show(p), ans, w,
             "Raccolgo il MCD dei termini, %s: <b>%s</b>." % (gm, ans))


def s1_parz():
    a, b = nz(R, -6, 6), nz(R, -6, 6)
    v1, v2 = R.choice([("x", "y"), ("a", "b"), ("x", "a")])
    # (v1 + a)(v2 + b) = v1 v2 + b v1 + a v2 + ab
    p = P([(1, {v1: 1, v2: 1}), (b, {v1: 1}), (a, {v2: 1}), (a * b, {})])
    ans = f(lin(1, v1, a), lin(1, v2, b))
    w = [f(lin(1, v1, b), lin(1, v2, a)), f(lin(1, v1, -a), lin(1, v2, -b)), "%s(%s) %s %s" % (v1, lin(1, v2, b), "+" if a > 0 else "−", show(P([(abs(a), {v2: 1}), (abs(a) * b * (1 if a > 0 else 1), {})])))]
    return M("Scomponi con il raccoglimento parziale: %s" % show(p), ans, w,
             "Raccolgo %s nei primi due termini e %s negli altri due: %s(%s) %s %d(%s) = <b>%s</b>." % (v1, fq(a), v1, lin(1, v2, b), "+" if a > 0 else "−", abs(a), lin(1, v2, b), ans))


def s2_diff():
    a, b = R.randint(1, 7), R.randint(1, 9)
    if math.gcd(a, b) > 1:
        return None
    v = R.choice(["x", "a", "y"])
    e = R.choice([1, 1, 2])
    p = P([(a * a, {v: 2 * e}), (-b * b, {})])
    A = show(P([(a, {v: e})]))
    ans = f("%s + %d" % (A, b), "%s − %d" % (A, b))
    w = [f("%s − %d" % (A, b)) + "²", f("%s + %d" % (A, b)) + "²", f("%s + %d" % (A, b * b), "%s − %d" % (A, b * b)) if b > 1 else f("%s + %d" % (show(P([(a * a, {v: e})])), b), "%s − %d" % (show(P([(a * a, {v: e})])), b))]
    return M("Scomponi: %s" % show(p), ans, w, "Differenza di due quadrati: A² − B² = (A + B)(A − B) con A = %s e B = %d: <b>%s</b>." % (A, b, ans))


def s2_quad():
    a, b = R.randint(1, 5), R.randint(1, 7)
    if math.gcd(a, b) > 1:
        return None
    s = R.choice([1, -1])
    v = R.choice(["x", "a", "y"])
    p = P([(a * a, {v: 2}), (2 * s * a * b, {v: 1}), (b * b, {})])
    ans = "(%s)²" % lin(a, v, s * b)
    w = ["(%s)²" % lin(a, v, -s * b), f(lin(a, v, b), lin(a, v, -b)), "(%s)²" % lin(a * a, v, s * b) if a > 1 else "(%s)²" % lin(1, v, s * 2 * b)]
    return M("Scomponi: %s" % show(p), ans, w, "È il quadrato di un binomio: %s e %d sono quadrati e %s è il doppio prodotto: <b>%s</b>." % (show(P([(a * a, {v: 2})])), b * b, show(P([(2 * s * a * b, {v: 1})])), ans))


def s3_trin():
    a, b = nz(R, -9, 9), nz(R, -9, 9)
    if a + b == 0 or a == b:
        return None
    v = R.choice(["x", "a", "y"])
    p = P([(1, {v: 2}), (a + b, {v: 1}), (a * b, {})])
    ans = f(lin(1, v, a), lin(1, v, b))
    w = [f(lin(1, v, -a), lin(1, v, -b)), f(lin(1, v, a), lin(1, v, -b)), f(lin(1, v, -a), lin(1, v, b)), f(lin(1, v, a * b), lin(1, v, 1))]
    return M("Scomponi il trinomio: %s" % show(p), ans, [x for x in w if x != ans],
             "Cerco due numeri con somma %s e prodotto %s: sono %s e %s, quindi <b>%s</b>." % (fq(a + b), fq(a * b), fq(min(a, b)), fq(max(a, b)), ans))


def s3_cubi():
    a, b = R.randint(1, 3), R.randint(1, 5)
    s = R.choice([1, -1])
    v = R.choice(["x", "a", "y"])
    p = P([(a ** 3, {v: 3}), (s * b ** 3, {})])
    A = show(P([(a, {v: 1})]))
    ans = f(lin(a, v, s * b), show(P([(a * a, {v: 2}), (-s * a * b, {v: 1}), (b * b, {})])))
    w = [f(lin(a, v, s * b), show(P([(a * a, {v: 2}), (s * a * b, {v: 1}), (b * b, {})]))), f(lin(a, v, s * b), show(P([(a * a, {v: 2}), (-s * 2 * a * b, {v: 1}), (b * b, {})]))),
         "(%s)³" % lin(a, v, s * b), f(lin(a, v, -s * b), show(P([(a * a, {v: 2}), (s * a * b, {v: 1}), (b * b, {})])))]
    return M("Scomponi: %s" % show(p), ans, w,
             "%s di cubi: A³ %s B³ = (A %s B)(A² %s AB + B²) con A = %s, B = %d: <b>%s</b>." % ("Somma" if s > 0 else "Differenza", "+" if s > 0 else "−", "+" if s > 0 else "−", "−" if s > 0 else "+", A, b, ans))


def s4_multi():
    k = R.choice(["rd", "rq", "rt"])
    g = R.choice([2, 3, 5])
    v = R.choice(["x", "a"])
    if k == "rd":
        b = R.randint(1, 6)
        p = P([(g, {v: 3}), (-g * b * b, {v: 1})])
        gm = show(P([(g, {v: 1})]))
        ans = "%s(%s)(%s)" % (gm, lin(1, v, b), lin(1, v, -b))
        w = ["%s(%s)" % (gm, show(P([(1, {v: 2}), (-b * b, {})]))), "%s(%s)²" % (gm, lin(1, v, -b)), "%s(%s)(%s)" % (gm, lin(1, v, b * b), lin(1, v, -1))]
        e = "Raccolgo %s: %s(%s), poi differenza di quadrati: <b>%s</b>." % (gm, gm, show(P([(1, {v: 2}), (-b * b, {})])), ans)
    elif k == "rq":
        b = R.randint(1, 6)
        p = P([(g, {v: 2}), (2 * g * b, {v: 1}), (g * b * b, {})])
        ans = "%d(%s)²" % (g, lin(1, v, b))
        w = ["%d(%s)" % (g, show(P([(1, {v: 2}), (2 * b, {v: 1}), (b * b, {})]))), "(%s)²" % lin(g, v, b), "%d(%s)(%s)" % (g, lin(1, v, b), lin(1, v, -b))]
        e = "Raccolgo %d e riconosco il quadrato di un binomio: <b>%s</b>." % (g, ans)
    else:
        a, b = nz(R, -6, 6), nz(R, -6, 6)
        if a + b == 0 or a == b:
            return None
        p = P([(g, {v: 3}), (g * (a + b), {v: 2}), (g * a * b, {v: 1})])
        gm = show(P([(g, {v: 1})]))
        ans = "%s(%s)(%s)" % (gm, lin(1, v, a), lin(1, v, b))
        w = ["%s(%s)" % (gm, show(P([(1, {v: 2}), (a + b, {v: 1}), (a * b, {})]))), "%s(%s)(%s)" % (gm, lin(1, v, -a), lin(1, v, -b)), "%d(%s)(%s)" % (g, lin(1, v, a), lin(1, v, b))]
        e = "Raccolgo %s, poi scompongo il trinomio (somma %s, prodotto %s): <b>%s</b>." % (gm, fq(a + b), fq(a * b), ans)
    return M("Scomponi completamente: %s" % show(p), ans, w, e)


def s5_irr():
    a, b = R.randint(1, 5), R.randint(1, 7)
    if math.gcd(a, b) > 1:
        return None
    v = R.choice(["x", "a"])
    k = R.choice(["sq", "tr"])
    if k == "sq":
        p = P([(a * a, {v: 2}), (b * b, {})])
        w = [f(lin(a, v, b), lin(a, v, -b)), "(%s)²" % lin(a, v, b), f(lin(a, v, b), lin(a, v, b))]
        e = "Una <b>somma</b> di due quadrati non si scompone nei numeri reali: (A + B)(A − B) darebbe A² − B²."
    else:
        c = R.choice([2, 3, 5, 6, 7])
        p = P([(1, {v: 2}), (1, {v: 1}), (c, {})]) if R.random() < 0.5 else P([(1, {v: 2}), (2, {v: 1}), (c, {})])
        w = [f(lin(1, v, 1), lin(1, v, c)), f(lin(1, v, -1), lin(1, v, c)), "(%s)²" % lin(1, v, 1)]
        e = "Non esistono due interi con somma e prodotto richiesti (e il discriminante è negativo): il trinomio è <b>irriducibile</b>."
    return M("Come si scompone %s?" % show(p), "non si può scomporre (irriducibile)", w, e)


def main():
    seen = set()
    sets = [
        ("Raccoglimento totale e parziale", mix(R, seen, [(s1_racc, 12), (s1_parz, 8)])),
        ("Differenza di quadrati e quadrato di binomio", mix(R, seen, [(s2_diff, 10), (s2_quad, 10)])),
        ("Trinomio di secondo grado", mix(R, seen, [(s3_trin, 20)])),
        ("Cubi e polinomi irriducibili", mix(R, seen, [(s3_cubi, 12), (s5_irr, 8)])),
        ("Scomposizioni in più passaggi", mix(R, seen, [(s4_multi, 20)])),
    ]
    body = L(["Scomporre vuol dire scrivere un polinomio come <b>prodotto</b> di polinomi. Si prova sempre prima il <b>raccoglimento totale</b> (il MCD di tutti i termini).",
              "Poi si guarda il numero dei termini. Due termini: A² − B² = (A + B)(A − B), A³ ± B³ = (A ± B)(A² ∓ AB + B²). Tre termini: quadrato di un binomio o trinomio x² + sx + p = (x + a)(x + b) con a + b = s e a · b = p. Quattro termini: raccoglimento parziale.",
              "Si continua finché ogni fattore è <b>irriducibile</b>. A² + B² non si scompone."],
             [("Scomponi 2x³ − 18x.", ["Raccolgo 2x: 2x(x² − 9).", "x² − 9 = (x + 3)(x − 3)."], "2x(x + 3)(x − 3)"),
              ("Scomponi x² − x − 12.", ["Somma −1, prodotto −12: −4 e 3."], "(x − 4)(x + 3)")],
             [["Fermarsi a 2x(x² − 9)", "Controlla sempre se i fattori si scompongono ancora."],
              ["x² + 9 = (x + 3)(x − 3)", "(x + 3)(x − 3) = x² − 9: una somma di quadrati è irriducibile."],
              ["Sbagliare i segni nel trinomio", "Il prodotto negativo vuol dire due numeri di segno opposto."],
              ["a³ − b³ = (a − b)(a² + 2ab + b²)", "Nel secondo fattore c’è ab, non 2ab: (a − b)(a² + ab + b²)."]],
             table(["Termini", "Che cosa provare"], [["2", "differenza di quadrati, somma o differenza di cubi"], ["3", "quadrato di un binomio, trinomio somma e prodotto"], ["4", "raccoglimento parziale, cubo di un binomio"]]))
    faq = [("Da dove si comincia a scomporre?", "Sempre dal raccoglimento totale: se tutti i termini hanno un fattore comune lo si porta fuori. Poi si guarda il numero di termini e si cerca un prodotto notevole o il trinomio somma e prodotto."),
           ("Come si controlla una scomposizione?", "Si rimoltiplicano i fattori: si deve ritrovare il polinomio di partenza. Poi si verifica che nessun fattore sia ancora scomponibile.")]
    unit(G, R, "scomposizione-in-fattori", "A",
         "Scomposizione di un polinomio in fattori: raccoglimento, prodotti notevoli, trinomio di secondo grado",
         "Scomposizione in fattori", "Scomposizione in fattori",
         "Schede di matematica per la prima liceo sulla scomposizione in fattori: raccoglimento totale e parziale, differenza di quadrati, quadrato di un binomio, trinomio somma e prodotto, somma e differenza di cubi. 100 esercizi con soluzioni.",
         "A² − B² = (A + B)(A − B)", "Prima raccogli, poi guarda il numero dei termini; A² + B² è irriducibile.",
         body, faq, sets, 5)


if __name__ == "__main__":
    main()
