# -*- coding: utf-8 -*-
"""
Italia Matematica terza media: Equazioni di primo grado (Relazioni e funzioni)
  python3 tools/gen_it_matematica_m3_equazioni_di_primo_grado.py
Identità ed equazioni, soluzione e verifica, principi di equivalenza (trasporto con cambio di segno, divisione per il coefficiente),
equazioni ax + b = c, con l’incognita nei due membri, con le parentesi, con le frazioni (m.c.m.), equazioni determinate,
impossibili e indeterminate.
Errori: trasportare senza cambiare il segno, dividere solo un termine, togliere le parentesi senza distribuire.
"""
import math
import random
from fractions import Fraction as Fr
from it_media import M, L, unit, mix, table, W, fq, sgn, Kids
from it_m3 import P, show

R = random.Random(71305)
G = "terza-media"
K = Kids(R)


def nz(lo=-9, hi=9):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def lin(a, b):
    return show(P([(a, {"x": 1}), (b, {})]))


def xs(x):
    return "x = %s" % fq(x)


def s1_verifica():
    a, x = nz(-6, 6), nz(-6, 6)
    b = R.randint(-9, 9)
    c = a * x + b
    y = x + R.choice([-2, -1, 1, 2])
    cand = R.choice([x, y])
    ok = cand == x
    return M("x = %s è soluzione dell’equazione %s = %s?" % (sgn(cand), lin(a, b), sgn(c) if c else "0"), "sì" if ok else "no", ["no" if ok else "sì", "solo se x è positivo", "non si può verificare"],
             "Sostituisco: %s · (%s) %s %d = %s. %s." % (sgn(a), sgn(cand), "+" if b >= 0 else "−", abs(b), sgn(a * cand + b) if a * cand + b else "0", "È uguale al secondo membro: <b>sì</b>" if ok else "È diverso da %s: <b>no</b>" % (sgn(c) if c else "0")))


def s2_base():
    a, x = nz(-9, 9), nz(-12, 12)
    b = nz(-20, 20)
    c = a * x + b
    if abs(a) == 1 and R.random() < 0.6:
        return None
    q = "%s = %s" % (lin(a, b), sgn(c) if c else "0")
    w = [Fr(c + b, a), Fr(c - b) * a if abs((c - b) * a) < 200 else None, Fr(a, c - b) if c != b else None, -x]
    return M("Risolvi: %s" % q, xs(x), W(*[xs(v) for v in w if v is not None and v != x]),
             "%s = %s %s %d → %s = %s → x = %s : (%s) = <b>%s</b>." % (show(P([(a, {"x": 1})])), sgn(c) if c else "0", "−" if b > 0 else "+", abs(b), show(P([(a, {"x": 1})])), sgn(c - b), sgn(c - b), sgn(a), fq(x)))


def s2_due_membri():
    a, cc = nz(-8, 8), nz(-8, 8)
    if a == cc:
        return None
    x = nz(-10, 10)
    b = R.randint(-15, 15)
    dd = (a - cc) * x + b
    q = "%s = %s" % (lin(a, b), lin(cc, dd))
    w = [Fr(dd - b, a + cc) if a + cc else None, Fr(dd + b, a - cc), Fr(b - dd, a - cc) if b != dd else None, x + 1]
    return M("Risolvi: %s" % q, xs(x), W(*[xs(v) for v in w if v is not None and v != x]),
             "Porto le x a sinistra e i numeri a destra: %s = %s → %s = %s → <b>x = %s</b>." % (show(P([(a, {"x": 1}), (-cc, {"x": 1})])), "%s %s %d" % (sgn(dd) if dd else "0", "−" if b > 0 else "+", abs(b)), show(P([(a - cc, {"x": 1})])), sgn(dd - b) if dd - b else "0", fq(x)))


def s3_parentesi():
    k, a = nz(-5, 5), nz(-5, 5)
    if abs(k) == 1:
        return None
    x = nz(-8, 8)
    b = R.randint(-9, 9)
    c = R.randint(-9, 9)
    # k(x + a) + b·x = rhs
    rhs = k * (x + a) + c * x
    lhs = "%s(%s)%s" % (sgn(k) if k < 0 else str(k), lin(1, a), (" %s %s" % ("+" if c > 0 else "−", show(P([(abs(c), {"x": 1})]))) if c else ""))
    if k + c == 0:
        return None
    w = [Fr(rhs - a, k + c), Fr(rhs - k * a, k - c) if k != c else None, Fr(rhs + k * a, k + c), -x]
    return M("Risolvi: %s = %s" % (lhs, sgn(rhs) if rhs else "0"), xs(x), W(*[xs(v) for v in w if v is not None and v != x]),
             "Tolgo le parentesi: %s = %s → %s = %s → <b>x = %s</b>." % (show(P([(k, {"x": 1}), (k * a, {})])) + ((" %s %s" % ("+" if c > 0 else "−", show(P([(abs(c), {"x": 1})])))) if c else ""), sgn(rhs) if rhs else "0", show(P([(k + c, {"x": 1})])), sgn(rhs - k * a) if rhs - k * a else "0", fq(x)))


def s4_frazioni():
    d1, d2 = R.choice([(2, 3), (3, 4), (2, 5), (4, 6), (3, 5), (2, 4), (6, 4)])
    x = R.randint(-6, 12) * 1
    a = R.choice([1, 1, 2, 3])
    # x/d1 + a·x/d2 ... semplice: (x)/d1 + b = x/d2 ... uso: a x / d1 − x / d2 = c
    c = Fr(a * x, d1) - Fr(x, d2)
    if c.denominator != 1 and c.denominator not in (2, 3, 4, 5, 6) or Fr(a, d1) == Fr(1, d2) or x == 0 or math.gcd(a, d1) != 1:
        return None
    fa = "x" if a == 1 else "%dx" % a
    q = "<span class='fr'><span class='fn'>%s</span><span class='fd'>%d</span></span> − <span class='fr'><span class='fn'>x</span><span class='fd'>%d</span></span> = %s" % (fa, d1, d2, fq(c) if c >= 0 else "−" + fq(-c))
    m = d1 * d2 // math.gcd(d1, d2)
    w = [c * m, Fr(c) / (Fr(a, d1) + Fr(1, d2)) if Fr(a, d1) + Fr(1, d2) else None, c * (d1 - d2) if d1 != d2 else None, -Fr(x)]
    return M("Risolvi: %s" % q, xs(x), W(*[xs(v) for v in w if v is not None and v != x]),
             "m.c.m. = %d: %s − %s = %s → %s." % (m, show(P([(a * m // d1, {"x": 1})])), show(P([(m // d2, {"x": 1})])), fq(c * m) if c >= 0 else "−" + fq(-c * m), ("<b>x = %s</b>" % fq(x)) if a * m // d1 - m // d2 == 1 else "%s = %s → <b>x = %s</b>" % (show(P([(a * m // d1 - m // d2, {"x": 1})])), fq(c * m) if c >= 0 else "−" + fq(-c * m), fq(x))))


def s5_tipo():
    k = R.choice(["det", "imp", "ind"])
    a, b = nz(-6, 6), R.randint(-9, 9)
    if k == "imp":
        q = "%s = %s" % (lin(a, b), lin(a, b + nz(-5, 5)))
        ans, e = "impossibile", "Le x si eliminano e resta un’uguaglianza falsa (0 = numero diverso da 0): <b>impossibile</b>."
    elif k == "ind":
        m = nz(-3, 3)
        if abs(m) == 1:
            return None
        q = "%s(%s) = %s" % (m, lin(a, b), lin(a * m, b * m)) if m > 0 else "(%s)(%s) = %s" % (sgn(m), lin(a, b), lin(a * m, b * m))
        ans, e = "indeterminata", "Sviluppando, i due membri sono uguali (0 = 0): ogni numero è soluzione, <b>indeterminata</b>."
    else:
        c = nz(-6, 6)
        if c == a:
            return None
        q = "%s = %s" % (lin(a, b), lin(c, b + nz(-5, 5)))
        ans, e = "determinata", "Le x non si eliminano: c’è una sola soluzione, <b>determinata</b>."
    return M("L’equazione %s è…" % q, ans, [v for v in ["determinata", "impossibile", "indeterminata"] if v != ans] + ["un’identità falsa"], e)


def main():
    seen = set()
    sets = [
        ("Soluzione e verifica", mix(R, seen, [(s1_verifica, 10), (s2_base, 10)])),
        ("Equazioni ax + b = c", mix(R, seen, [(s2_base, 20)])),
        ("Incognita nei due membri", mix(R, seen, [(s2_due_membri, 20)])),
        ("Parentesi e frazioni", mix(R, seen, [(s3_parentesi, 12), (s4_frazioni, 8)])),
        ("Determinate, impossibili, indeterminate", mix(R, seen, [(s5_tipo, 12), (s4_frazioni, 8)])),
    ]
    body = L(["Un’<b>equazione</b> è un’uguaglianza con un’incognita (x) vera solo per alcuni valori: le <b>soluzioni</b>. Per verificare si sostituisce la soluzione e si controlla che i due membri siano uguali.",
              "<b>Primo principio</b>: si può aggiungere o togliere lo stesso numero ai due membri. Così un termine si «trasporta» nell’altro membro <b>cambiando il segno</b>.",
              "<b>Secondo principio</b>: si possono moltiplicare o dividere i due membri per lo stesso numero diverso da 0. Così si divide per il coefficiente di x.",
              "Ordine: togli le parentesi, elimina i denominatori (m.c.m.), porta le x a sinistra e i numeri a destra, riduci, dividi per il coefficiente."],
             [("3x − 5 = 2x + 4", ["3x − 2x = 4 + 5", "x = 9"], "x = 9"), ("2(x + 3) = 14", ["2x + 6 = 14", "2x = 8"], "x = 4")],
             [["Trasportare senza cambiare segno", "3x + 5 = 20 → 3x = 20 − 5, non 20 + 5."],
              ["Dividere per il coefficiente sbagliando il segno", "−4x = 12 → x = 12 : (−4) = −3."],
              ["2(x + 3) = 2x + 3", "Il 2 moltiplica tutti i termini della parentesi: 2x + 6."]],
             table(["Dopo le riduzioni", "Equazione"], [["ax = b con a ≠ 0", "determinata (una soluzione)"], ["0x = b con b ≠ 0", "impossibile"], ["0x = 0", "indeterminata (infinite soluzioni)"]]))
    faq = [("Che differenza c’è tra un’equazione e un’identità?", "Un’identità è vera per ogni valore delle lettere (come 2(x + 1) = 2x + 2); un’equazione solo per alcuni valori."),
           ("Perché si cambia il segno quando si trasporta?", "Perché in realtà si sottrae (o si somma) lo stesso numero ai due membri: in un membro il termine sparisce e nell’altro compare con il segno opposto.")]
    unit(G, R, "equazioni-di-primo-grado", "F",
         "Esplorare e risolvere problemi utilizzando equazioni di primo grado",
         "Equazioni di primo grado", "Equazioni di primo grado",
         "Schede di matematica per la terza media sulle equazioni di primo grado: verifica della soluzione, principi di equivalenza, incognita nei due membri, parentesi, frazioni, equazioni determinate, impossibili e indeterminate. 100 esercizi con soluzioni.",
         "Trasporto: cambia il segno.", "Dividi i due membri per il coefficiente di x.",
         body, faq, sets, 5)


if __name__ == "__main__":
    main()
