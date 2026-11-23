# -*- coding: utf-8 -*-
"""
Italia Matematica prima liceo: Equazioni lineari (Aritmetica e algebra)
  python3 tools/gen_it_matematica_l1_equazioni_lineari.py
Equazioni numeriche intere, con le frazioni e con i prodotti notevoli, determinate, impossibili e indeterminate,
legge di annullamento del prodotto (equazioni di grado superiore scomponibili), problemi risolti con le equazioni.
Errori: trasportare senza cambiare segno, sviluppare (x + 2)² senza doppio prodotto, dividere per x perdendo x = 0.
Il primo insieme riusa le funzioni del generatore della terza media (con un nuovo seme).
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, P, show, mul, add, sol, ex, Kids
import gen_it_matematica_m3_equazioni_di_primo_grado as m3e

R = random.Random(72107)
m3e.R = R
G = "prima-liceo"


def lin(a, b, v="x"):
    return show(P([(a, {v: 1}), (b, {})]))


def s1_notev():
    a, b = nz(R, -6, 6), nz(R, -6, 6)
    if a == b or a == -b:
        return None
    # (x + a)² − (x + b)² = c  → 2(a − b)x + a² − b² = c
    x = nz(R, -8, 8)
    c = 2 * (a - b) * x + a * a - b * b
    q = "(%s)² − (%s)² = %s" % (lin(1, a), lin(1, b), fq(c))
    wrong_c = c - (a * a - b * b)
    w = [Fr(c, 2 * (a - b)), Fr(c - a * a + b * b, a - b), Fr(c + a * a - b * b, 2 * (a - b)), -x]
    return M("Risolvi: %s" % q, ex(x), [ex(v) for v in w if v != x],
             "Sviluppo: %s − (%s) = %s → %s = %s → <b>x = %s</b>." % (show(P([(1, {"x": 2}), (2 * a, {"x": 1}), (a * a, {})])), show(P([(1, {"x": 2}), (2 * b, {"x": 1}), (b * b, {})])), fq(c), show(P([(2 * (a - b), {"x": 1})])), fq(c - a * a + b * b), fq(x)))


def s1_prod():
    a, b = nz(R, -5, 5), R.randint(-9, 9)
    c, dd = nz(R, -5, 5), R.randint(-9, 9)
    # (x + a)(x + b) = (x + c)(x + dd) + k → (a + b − c − dd)x = k + c·dd − a·b
    co = a + b - c - dd
    if co == 0:
        return None
    x = nz(R, -6, 6)
    k = co * x + a * b - c * dd
    q = "(%s)(%s) = (%s)(%s) %s %d" % (lin(1, a), lin(1, b), lin(1, c), lin(1, dd), "+" if k >= 0 else "−", abs(k))
    w = [Fr(k + c * dd + a * b, co), Fr(k, co), -x, Fr(k - c * dd + a * b, co) if Fr(k - c * dd + a * b, co) != x else x + 1]
    return M("Risolvi: %s" % q, ex(x), [ex(v) for v in w if v != x],
             "Sviluppo i prodotti: x² si elimina e resta %s = %s, quindi <b>x = %s</b>." % (show(P([(co, {"x": 1})])), fq(k + c * dd - a * b), fq(x)))


def s2_fraz():
    d1, d2, d3 = R.choice([(2, 3, 6), (3, 4, 12), (2, 5, 10), (4, 6, 12), (3, 6, 2), (2, 4, 4), (5, 3, 15)])
    x = R.randint(-6, 9)
    a, b = nz(R, -4, 4), R.randint(-5, 5)
    # (x + a)/d1 − (x + b)/d2 = rhs
    rhs = Fr(x + a, d1) - Fr(x + b, d2)
    coef = Fr(1, d1) - Fr(1, d2)
    if coef == 0 or rhs.denominator not in (1, 2, 3, 4, 5, 6, 10, 12, 15):
        return None
    m = d1 * d2 // __import__("math").gcd(d1, d2)
    q = "<span class='fr'><span class='fn'>%s</span><span class='fd'>%d</span></span> − <span class='fr'><span class='fn'>%s</span><span class='fd'>%d</span></span> = %s" % (lin(1, a), d1, lin(1, b), d2, fq(rhs))
    wrong = (rhs * m - m // d1 * a + b) / (m // d1 - m // d2) if m // d1 != m // d2 else None
    w = [wrong, (rhs - Fr(a, d1) + Fr(b, d2)) / (Fr(1, d1) + Fr(1, d2)), -x, x + 1]
    return M("Risolvi: %s" % q, ex(x), [ex(v) for v in w if v is not None and v != x],
             "Moltiplico tutto per il m.c.m. %d: %d(%s) − %d(%s) = %s. Attenzione al segno − davanti alla seconda frazione: <b>x = %s</b>." % (m, m // d1, lin(1, a), m // d2, lin(1, b), fq(rhs * m), fq(x)))


def s3_annul():
    k = R.choice(["2f", "racc", "diff", "3f"])
    if k == "2f":
        a, b = nz(R, -6, 6), nz(R, -6, 6)
        c = R.choice([1, 1, 2, 3])
        rs = [Fr(-a), Fr(-b, c)]
        q = "(%s)(%s) = 0" % (lin(1, a), lin(c, b))
        w = [sol([a, Fr(b, c)]), sol([-a]), sol([-a, -b]), sol([-a, Fr(b, c)]), sol([a, Fr(-b, c)])]
    elif k == "racc":
        a = nz(R, -9, 9)
        c = R.choice([1, 2, 3])
        rs = [Fr(0), Fr(a, c)]
        q = "%s = 0" % show(P([(c, {"x": 2}), (-a, {"x": 1})]))
        w = [sol([Fr(a, c)]), sol([0, Fr(-a, c)]), sol([a]) if c > 1 else sol([0, -a]), sol([Fr(-a, c)]), "impossibile"]
    elif k == "diff":
        a = R.randint(1, 9)
        rs = [Fr(-a), Fr(a)]
        q = "%s = 0" % show(P([(1, {"x": 2}), (-a * a, {})]))
        w = [sol([a]), sol([a * a, -a * a]), "impossibile", sol([0, a])]
    else:
        a, b = R.sample([-4, -3, -2, -1, 1, 2, 3, 4], 2)
        rs = [Fr(0), Fr(a), Fr(b)]
        q = "%s = 0" % show(mul(mul(P([(1, {"x": 1})]), P([(1, {"x": 1}), (-a, {})])), P([(1, {"x": 1}), (-b, {})])))
        w = [sol([a, b]), sol([0, -a, -b]), sol([-a, -b])]
    ans = sol(rs)
    return M("Risolvi con la legge di annullamento del prodotto: %s" % q, ans, [x for x in w if x != ans],
             "Scompongo (se serve) e pongo ogni fattore uguale a 0: <b>%s</b>." % ans)


def s4_probl():
    k = R.choice(["cons", "eta", "rett", "soldi", "triplo"])
    if k == "cons":
        n = R.randint(3, 40)
        cnt = R.choice([2, 3])
        s = sum(n + i for i in range(cnt))
        q = "La somma di %s numeri naturali consecutivi è %d. Qual è il più piccolo?" % ("due" if cnt == 2 else "tre", s)
        e = "x + (x + 1)%s = %d → %dx + %d = %d → <b>x = %d</b>." % (" + (x + 2)" if cnt == 3 else "", s, cnt, cnt * (cnt - 1) // 2, s, n)
        a, w = n, [n + 1, s // cnt, n - 1, n + cnt, s // cnt + 1]
    elif k == "eta":
        f = R.randint(6, 14)
        diff = R.randint(24, 34)
        p = f + diff
        t = R.randint(2, 8)
        # tra t anni il padre avrà ... volte? usa: oggi padre ha diff anni più del figlio; la somma delle età è S
        S = f + p
        q = "Un padre ha %d anni più del figlio e la somma delle loro età è %d. Quanti anni ha il figlio?" % (diff, S)
        e = "x + (x + %d) = %d → 2x = %d → <b>x = %d</b>." % (diff, S, S - diff, f)
        a, w = f, [S // 2, (S + diff) // 2, S - diff]
    elif k == "rett":
        b = R.randint(3, 15)
        dd = R.randint(2, 8)
        h = b + dd
        per = 2 * (b + h)
        q = "In un rettangolo l’altezza supera la base di %d cm e il perimetro è %d cm. Quanto misura la base?" % (dd, per)
        e = "2[x + (x + %d)] = %d → 4x + %d = %d → <b>x = %d cm</b>." % (dd, per, 2 * dd, per, b)
        a, w = "%d cm" % b, ["%d cm" % h, "%d cm" % (per // 4), "%d cm" % ((per - dd) // 2)]
    elif k == "soldi":
        x = R.randint(10, 60)
        m = R.choice([2, 3, 4])
        tot = x + m * x
        n1, n2 = R.sample(["Giulia", "Marco", "Sofia", "Luca", "Chiara", "Pietro"], 2)
        q = "%s e %s hanno insieme %d €. %s ha il %s di %s. Quanto ha %s?" % (n1, n2, tot, n2, {2: "doppio", 3: "triplo", 4: "quadruplo"}[m], n1, n1)
        e = "x + %dx = %d → %dx = %d → <b>x = %d €</b>." % (m, tot, m + 1, tot, x)
        a, w = "%d €" % x, ["%d €" % (m * x), "%d €" % (tot // m), "%d €" % (tot // 2), "%d €" % (tot - x - 1 if False else x + m)]
    else:
        x = R.randint(3, 20)
        m = R.choice([2, 3, 4, 5])
        dd = R.randint(1, 12)
        rhs = m * x - dd
        q = "Il %s di un numero, diminuito di %d, è uguale al numero aumentato di %d. Qual è il numero?" % ({2: "doppio", 3: "triplo", 4: "quadruplo", 5: "quintuplo"}[m], dd, rhs - x)
        if rhs - x <= 0:
            return None
        e = "%dx − %d = x + %d → %dx = %d → <b>x = %d</b>." % (m, dd, rhs - x, m - 1, rhs - x + dd, x)
        a, w = x, [Fr(rhs - x - dd, m - 1), Fr(rhs - x + dd, m + 1), rhs - x]
    return M(q, str(a) if not isinstance(a, str) else a, [str(fq(v)) if not isinstance(v, str) else v for v in w], e)


def main():
    seen = set()
    sets = [
        ("Equazioni intere", mix(R, seen, [(m3e.s2_due_membri, 10), (m3e.s3_parentesi, 10)])),
        ("Con i prodotti notevoli", mix(R, seen, [(s1_notev, 10), (s1_prod, 10)])),
        ("Con le frazioni e casi particolari", mix(R, seen, [(s2_fraz, 12), (m3e.s5_tipo, 8)])),
        ("Legge di annullamento del prodotto", mix(R, seen, [(s3_annul, 20)])),
        ("Problemi con le equazioni", mix(R, seen, [(s4_probl, 20)])),
    ]
    body = L(["Un’equazione è <b>lineare</b> (di primo grado) se, dopo aver sviluppato e ridotto, diventa ax = b. Se a ≠ 0 è <b>determinata</b> (x = b/a); se 0x = b con b ≠ 0 è <b>impossibile</b>; se 0x = 0 è <b>indeterminata</b>.",
              "Ordine: sviluppa i prodotti (attenzione ai prodotti notevoli), elimina i denominatori moltiplicando per il m.c.m., porta le x a sinistra cambiando segno, riduci e dividi.",
              "<b>Legge di annullamento del prodotto</b>: A · B = 0 se e solo se A = 0 oppure B = 0. Così si risolvono anche equazioni di grado superiore, dopo averle scomposte.",
              "Nei problemi: scegli l’incognita, scrivi l’equazione, risolvi e controlla che la soluzione abbia senso."],
             [("(x + 3)² − (x − 1)² = 24", ["x² + 6x + 9 − x² + 2x − 1 = 24", "8x = 16"], "x = 2"),
              ("x² − 5x = 0", ["x(x − 5) = 0"], "x = 0 ∨ x = 5")],
             [["(x + 3)² = x² + 9", "Serve il doppio prodotto: x² + 6x + 9."],
              ["− (x − 1)² = − x² − 2x + 1", "Il segno − cambia tutti i termini: −x² + 2x − 1."],
              ["x² = 5x → x = 5", "Dividendo per x si perde la soluzione x = 0: scomponi x(x − 5) = 0."]])
    faq = [("Che cosa vuol dire che un’equazione è impossibile?", "Che non esiste nessun numero che la renda vera: dopo le riduzioni si arriva a 0x = b con b ≠ 0, cioè a un’uguaglianza falsa come 0 = 3."),
           ("Perché non si può dividere per x?", "Perché x potrebbe valere 0 e non si divide per 0. In x² = 5x si perde la soluzione x = 0: meglio portare tutto a sinistra e scomporre.")]
    unit(G, R, "equazioni-lineari", "A",
         "Equazioni di primo grado; legge di annullamento del prodotto; risolvere problemi con le equazioni",
         "Equazioni lineari", "Equazioni lineari",
         "Schede di matematica per la prima liceo sulle equazioni lineari: equazioni intere, con prodotti notevoli e frazioni, determinate, impossibili e indeterminate, legge di annullamento del prodotto, problemi. 100 esercizi con soluzioni.",
         "A · B = 0 ⟺ A = 0 ∨ B = 0", "Sviluppa, togli i denominatori, porta le x a sinistra, dividi per il coefficiente.",
         body, faq, sets, 7)


if __name__ == "__main__":
    main()
