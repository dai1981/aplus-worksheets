# -*- coding: utf-8 -*-
"""
Italia Matematica prima liceo: Numeri naturali, interi e razionali (Aritmetica e algebra)
  python3 tools/gen_it_matematica_l1_numeri_naturali_interi_e_razionali.py
MCD e mcm con la scomposizione, potenze di numeri relativi, proprietà delle potenze, esponente zero e negativo,
operazioni ed espressioni con le frazioni, confronto, numeri decimali periodici e frazione generatrice, notazione scientifica.
Errori: (−2)⁴ e −2⁴, a⁻ⁿ negativo, sommare numeratori e denominatori, 0,(3) = 3/10.
"""
import math
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, d, nz, sup, FR, par

R = random.Random(72102)
G = "prima-liceo"


def pw(b, e):
    """potenza con la base tra parentesi se serve"""
    return "%s%s" % (par(b) if Fr(b) >= 0 and Fr(b).denominator == 1 else "(%s)" % fq(b), "<sup>%s</sup>" % ("−%d" % -e if e < 0 else e))


def s1_mcd():
    while True:
        g = R.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 18])
        a, b = g * R.randint(2, 9), g * R.randint(2, 9)
        if a != b and math.gcd(a, b) == g and a <= 200 and b <= 200:
            break
    l = a * b // g
    if R.random() < 0.5:
        return M("Calcola MCD(%d; %d)." % (a, b), str(g), W(l, g * 2 if a % (2 * g) == 0 and b % (2 * g) == 0 else None, min(a, b) // 2 if min(a, b) % 2 == 0 and min(a, b) // 2 != g else None, 1 if g != 1 else 2, a * b, abs(a - b) if abs(a - b) != g else None),
                 "Il MCD è il prodotto dei fattori primi comuni con il minimo esponente: MCD = <b>%d</b>." % g)
    return M("Calcola mcm(%d; %d)." % (a, b), num_(l), W(num_(a * b) if a * b != l else None, num_(g), num_(l // 2) if l % 2 == 0 and l // 2 % a == 0 and False else None, num_(l * 2), num_(max(a, b))),
             "Il mcm è il prodotto dei fattori primi comuni e non comuni con il massimo esponente: mcm = %d · %d : %d = <b>%s</b>." % (a, b, g, num_(l)))


def num_(n):
    return d(n)


def s1_pot():
    b = nz(R, -5, 5)
    if abs(b) == 1:
        return None
    e = R.randint(2, 4)
    k = R.choice(["par", "senza"])
    if k == "senza" and b < 0:
        v = -(abs(b) ** e)
        q = "−%d<sup>%d</sup>" % (abs(b), e)
        why = "L’esponente riguarda solo il %d: −(%d<sup>%d</sup>) = <b>%s</b>." % (abs(b), abs(b), e, fq(v))
        w = [abs(b) ** e, -abs(b) * e, -v, -(abs(b) ** (e + 1)), abs(b) * e]
    else:
        v = b ** e
        q = pw(b, e)
        why = "%s moltiplicato %d volte: %s (esponente %s, segno %s)." % (par(b), e, "<b>%s</b>" % fq(v), "pari" if e % 2 == 0 else "dispari", "+" if v > 0 else "−")
        w = [-v, b * e, abs(b) * e, b ** (e + 1), b + e, b ** (e - 1)]
    return M("Calcola %s." % q, fq(v), [fq(x) for x in w], why)


def s1_neg():
    b = R.choice([Fr(2), Fr(3), Fr(5), Fr(10), Fr(1, 2), Fr(2, 3), Fr(3, 4), Fr(-2), Fr(-3), Fr(-1, 2), Fr(4, 5)])
    e = -R.randint(1, 3)
    if e == -1 and b.denominator == 1 and R.random() < 0.5:
        e = -2
    v = b ** e
    w = [-(b ** -e), b ** -e, b * e, -v, Fr(1, 1) / (b * -e) if b * -e else None, b ** e * b]
    return M("Calcola %s." % pw(b, e), fq(v), [fq(x) for x in w if x is not None and x != v],
             "Esponente negativo: si capovolge la base e l’esponente diventa positivo: %s = <b>%s</b>." % (pw(1 / b, -e), fq(v)))


def s2_prop():
    b = R.choice([2, 3, 5, 7, 10])
    k = R.choice(["mul", "div", "pp", "mix"])
    m, n = R.randint(2, 9), R.randint(2, 7)
    if k == "mul":
        q, r, w = "%d<sup>%d</sup> · %d<sup>%d</sup>" % (b, m, b, n), m + n, [m * n, m - n if m != n else None, m + n + 1]
        why = "Stessa base: si sommano gli esponenti, %d + %d = %d" % (m, n, m + n)
    elif k == "div":
        if m <= n:
            m, n = n + R.randint(1, 4), m
        q, r, w = "%d<sup>%d</sup> : %d<sup>%d</sup>" % (b, m, b, n), m - n, [m + n, m // n if m % n == 0 else None, n - m]
        why = "Stessa base: si sottraggono gli esponenti, %d − %d = %d" % (m, n, m - n)
    elif k == "pp":
        q, r, w = "(%d<sup>%d</sup>)<sup>%d</sup>" % (b, m, n), m * n, [m + n, m ** n if m ** n < 100 else None, m * n + 1]
        why = "Potenza di potenza: si moltiplicano gli esponenti, %d · %d = %d" % (m, n, m * n)
    else:
        p = R.randint(2, 5)
        r = m + n - p
        if r <= 1:
            return None
        q, w = "%d<sup>%d</sup> · %d<sup>%d</sup> : %d<sup>%d</sup>" % (b, m, b, n, b, p), [m * n - p, m + n + p, m * n // p if (m * n) % p == 0 else None]
        why = "%d + %d − %d = %d" % (m, n, p, r)
    return M("Scrivi come unica potenza: %s" % q, "%d<sup>%s</sup>" % (b, ("−%d" % -r) if r < 0 else r),
             ["%d<sup>%s</sup>" % (b, ("−%d" % -x) if x < 0 else x) for x in w if x is not None and x != r] + ["%d<sup>%d</sup>" % (b * b, r) if r > 0 else None], "%s: <b>%d<sup>%s</sup></b>." % (why, b, ("−%d" % -r) if r < 0 else r))


def rfr(maxd=12):
    dd = R.randint(2, maxd)
    n = nz(R, -2 * dd, 2 * dd)
    f = Fr(n, dd)
    return f if f.denominator != 1 else None


def s2_fr():
    a, b = rfr(), rfr()
    if a is None or b is None or a.denominator == b.denominator and R.random() < 0.6:
        return None
    op = R.choice(["+", "−", "·", ":"])
    if op == "+":
        v = a + b
        wr = [Fr(a.numerator + b.numerator, a.denominator + b.denominator), a + b + 1, a - b]
    elif op == "−":
        v = a - b
        wr = [Fr(a.numerator - b.numerator, a.denominator + b.denominator) if a.denominator + b.denominator else None, a + b, b - a]
    elif op == "·":
        v = a * b
        wr = [a / b, -a * b, Fr(a.numerator * b.numerator, a.denominator + b.denominator)]
    else:
        v = a / b
        wr = [a * b, b / a, -a / b]
    if abs(v.numerator) > 200 or v.denominator > 150:
        return None
    return M("Calcola %s %s %s." % (fq(a) if a > 0 else "(%s)" % fq(a), op, fq(b) if b > 0 else "(%s)" % fq(b)), fq(v), [fq(x) for x in wr if x is not None and x != v],
             {"+": "Denominatore comune (mcm), poi si sommano i numeratori", "−": "Denominatore comune (mcm), poi si sottraggono i numeratori", "·": "Numeratore per numeratore e denominatore per denominatore (semplificando)", ":": "Si moltiplica per l’inversa della seconda frazione"}[op] + ": <b>%s</b>." % fq(v))


def s3_espr():
    a, b, c = rfr(6), rfr(6), rfr(6)
    if None in (a, b, c):
        return None
    k = R.choice([0, 1, 2])
    if k == 0:
        v, q, wv = a + b * c, "%s + %s · %s" % (fq(a), par(b), par(c)), (a + b) * c
    elif k == 1:
        v, q, wv = (a - b) * c, "(%s − %s) · %s" % (fq(a), par(b), par(c)), a - b * c
    else:
        e = R.choice([2, -1, -2])
        v, q, wv = a ** 2 + b ** e if b else None, "%s<sup>2</sup> + %s" % (par(a) if a > 0 else "(%s)" % fq(a), pw(b, e)), (a + b) ** 2
    if v is None or abs(v.numerator) > 300 or v.denominator > 200 or wv == v:
        return None
    return M("Calcola l’espressione: %s" % q, fq(v), [fq(wv), fq(-v), fq(v + 1)],
             "Prima le potenze, poi moltiplicazioni e divisioni, infine addizioni e sottrazioni (le parentesi per prime): <b>%s</b>." % fq(v))


def ov(s):
    return "<span class='ov'>%s</span>" % s


def s4_gen():
    k = R.choice(["pur", "mis", "int"])
    if k == "pur":
        n = R.choice([1, 2, 3, 4, 5, 7, 8, 12, 15, 23, 27, 45, 36])
        dig = len(str(n)) if n >= 10 else 1
        den = 10 ** dig - 1
        f = Fr(n, den)
        q = "0,%s" % ov(str(n).rjust(dig, "0"))
        w = [Fr(n, 10 ** dig), Fr(n, den + 2) if dig == 1 else Fr(n, 10 ** dig + 1), Fr(n + 1, den)]
        e = "Periodico semplice: periodo su tanti 9 quante sono le cifre del periodo, %d/%d = <b>%s</b>." % (n, den, fq(f))
    elif k == "mis":
        a, p = R.randint(1, 9), R.randint(1, 9)
        if a == p:
            return None
        f = Fr(10 * a + p - a, 90)
        q = "0,%d%s" % (a, ov(p))
        w = [Fr(10 * a + p, 90), Fr(10 * a + p, 99), Fr(10 * a + p - a, 99)]
        e = "Periodico misto: (%d − %d)/90 = %d/90 = <b>%s</b> (un 9 per la cifra del periodo, uno 0 per l’antiperiodo)." % (10 * a + p, a, 10 * a + p - a, fq(f))
    else:
        i, p = R.randint(1, 4), R.randint(1, 8)
        f = Fr(9 * i + p, 9)
        q = "%d,%s" % (i, ov(p))
        w = [Fr(10 * i + p, 10), Fr(10 * i + p, 9), Fr(i * 10 + p, 99)]
        e = "%d,%s = (%d − %d)/9 = %d/9 = <b>%s</b>." % (i, ov(p), 10 * i + p, i, 9 * i + p, fq(f))
    return M("Qual è la frazione generatrice di %s?" % q, fq(f), [fq(x) for x in w if x != f], e)


def s4_conf():
    a, b = rfr(9), rfr(9)
    if a is None or b is None or a == b:
        return None
    big = max(a, b)
    q = "Qual è il maggiore tra %s e %s?" % (fq(a), fq(b))
    return M(q, fq(big), [fq(min(a, b)), "sono uguali", fq(-big) if -big not in (a, b) else fq(abs(big) + 1)],
             "Riduco allo stesso denominatore (o confronto i prodotti in croce): il maggiore è <b>%s</b>." % fq(big))


def sci(m, e):
    return "%s · 10<sup>%s</sup>" % (d(m), ("−%d" % -e) if e < 0 else e)


def s5_sci():
    m = Fr(R.randint(11, 99), 10)
    if m.denominator == 1:
        return None
    e = R.choice([-6, -5, -4, -3, -2, 3, 4, 5, 6, 7, 8])
    v = m * Fr(10) ** e
    k = R.choice(["to", "from"])
    if k == "to":
        return M("Scrivi in notazione scientifica: %s" % d(v), sci(m, e), [sci(m, -e), sci(m * 10, e - 1), sci(m, e + (1 if e > 0 else -1))],
                 "Il numero davanti va da 1 a 10: %s = <b>%s</b>." % (d(v), sci(m, e)))
    return M("Scrivi in forma decimale: %s" % sci(m, e), d(v), [d(m * Fr(10) ** (e + 1)), d(m * Fr(10) ** (e - 1)), d(m * Fr(10) ** (-e)) if abs(e) < 7 else d(m * Fr(10) ** (e + 2))],
             "%s la virgola di %d posti verso %s: <b>%s</b>." % ("Sposto", abs(e), "destra" if e > 0 else "sinistra", d(v)))


def s5_sci_op():
    a, b = R.randint(2, 9), R.randint(2, 9)
    e1, e2 = R.randint(-5, 8), R.randint(-5, 8)
    op = R.choice(["·", ":"])
    if op == "·":
        m, e = Fr(a * b), e1 + e2
    else:
        if (Fr(a, b) * 10).denominator not in (1, 2, 4, 5):
            return None
        m, e = Fr(a, b), e1 - e2
    while m >= 10:
        m, e = m / 10, e + 1
    while m < 1:
        m, e = m * 10, e - 1
    if m.denominator not in (1, 2, 4, 5, 10, 20, 25, 50, 100):
        return None
    ans = sci(m, e)
    w = [sci(m, e1 * e2 if op == "·" else e1 + e2), sci(m * 10, e - 1) if m * 10 < 100 else None, sci(m, -e) if e else sci(m, e + 1), sci(m, e + 1), sci(m, e - 1)]
    return M("Calcola e scrivi in notazione scientifica: (%d · 10<sup>%s</sup>) %s (%d · 10<sup>%s</sup>)" % (a, ("−%d" % -e1) if e1 < 0 else e1, op, b, ("−%d" % -e2) if e2 < 0 else e2), ans, [x for x in w if x and x != ans],
             "%s i numeri e %s gli esponenti, poi porto il numero tra 1 e 10: <b>%s</b>." % ("Moltiplico" if op == "·" else "Divido", "sommo" if op == "·" else "sottraggo", ans))


def main():
    seen = set()
    sets = [
        ("MCD, mcm e potenze", mix(R, seen, [(s1_mcd, 8), (s1_pot, 6), (s1_neg, 6)])),
        ("Proprietà delle potenze", mix(R, seen, [(s2_prop, 12), (s1_neg, 8)])),
        ("Operazioni con le frazioni", mix(R, seen, [(s2_fr, 14), (s4_conf, 6)])),
        ("Espressioni e numeri periodici", mix(R, seen, [(s3_espr, 10), (s4_gen, 10)])),
        ("Notazione scientifica", mix(R, seen, [(s5_sci, 10), (s5_sci_op, 10)])),
    ]
    body = L(["<b>MCD</b>: fattori primi comuni con il minimo esponente. <b>mcm</b>: fattori comuni e non comuni con il massimo esponente. Vale MCD · mcm = a · b.",
              "Potenze: a<sup>m</sup> · a<sup>n</sup> = a<sup>m+n</sup>, a<sup>m</sup> : a<sup>n</sup> = a<sup>m−n</sup>, (a<sup>m</sup>)<sup>n</sup> = a<sup>m·n</sup>, a<sup>0</sup> = 1. Con l’esponente negativo si capovolge la base: a<sup>−n</sup> = 1/a<sup>n</sup>.",
              "Una base negativa con esponente pari dà un risultato positivo: (−2)<sup>4</sup> = 16, ma −2<sup>4</sup> = −16.",
              "Frazioni: per sommare serve il denominatore comune; per dividere si moltiplica per l’inversa.",
              "Ogni numero periodico è razionale: 0,<span class='ov'>3</span> = 3/9 = 1/3. In notazione scientifica il numero è a · 10<sup>n</sup> con 1 ≤ a &lt; 10."],
             [("Calcola (2/3)<sup>−2</sup>.", ["Capovolgo la base: (3/2)<sup>2</sup>."], "9/4"),
              ("Frazione generatrice di 0,1<span class='ov'>6</span>", ["(16 − 1)/90 = 15/90."], "1/6")],
             [["Calcolare −3<sup>2</sup> = 9", "L’esponente riguarda solo il 3: −3<sup>2</sup> = −9; (−3)<sup>2</sup> = 9."],
              ["Pensare che 2<sup>−3</sup> sia negativo", "2<sup>−3</sup> = 1/8: l’esponente negativo capovolge, non cambia il segno."],
              ["Sommare numeratori e denominatori", "1/2 + 1/3 = 3/6 + 2/6 = 5/6, non 2/5."],
              ["Scrivere 0,<span class='ov'>3</span> = 3/10", "Il periodo va diviso per 9: 0,<span class='ov'>3</span> = 3/9 = 1/3."]])
    faq = [("Perché a<sup>0</sup> = 1?", "Perché a<sup>n</sup> : a<sup>n</sup> = 1 e, per la proprietà delle potenze, è anche a<sup>n−n</sup> = a<sup>0</sup>. Vale per ogni a ≠ 0."),
           ("Un numero periodico è un numero razionale?", "Sì: ogni numero decimale finito o periodico si scrive come frazione (la frazione generatrice). I numeri decimali illimitati non periodici, come √2 e π, sono irrazionali.")]
    unit(G, R, "numeri-naturali-interi-e-razionali", "A",
         "Operazioni con i numeri interi e razionali e loro proprietà; potenze; MCD e mcm; frazioni e numeri decimali; notazione scientifica",
         "Numeri naturali, interi e razionali", "Numeri naturali, interi e razionali",
         "Schede di matematica per la prima liceo su numeri naturali, interi e razionali: MCD e mcm, potenze ed esponenti negativi, proprietà delle potenze, frazioni ed espressioni, frazione generatrice, notazione scientifica. 100 esercizi con soluzioni.",
         "a⁻ⁿ = 1/aⁿ", "Con l’esponente negativo si capovolge la base, il segno non cambia.",
         body, faq, sets, 2)


if __name__ == "__main__":
    main()
