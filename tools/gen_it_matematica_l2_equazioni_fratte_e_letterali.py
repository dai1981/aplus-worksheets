# -*- coding: utf-8 -*-
"""
Italia Matematica seconda liceo: Equazioni fratte e letterali (Aritmetica e algebra)
  python3 tools/gen_it_matematica_l2_equazioni_fratte_e_letterali.py
Equazioni fratte: condizioni di esistenza, m.c.m., soluzioni da scartare; equazioni letterali intere con discussione
(determinata, impossibile, indeterminata al variare del parametro); formule inverse.
Errori: non controllare le C.E., dividere per un parametro che può essere 0, sbagliare i segni nelle formule inverse.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, P, show, mul, FR, ex

R = random.Random(72202)
G = "seconda-liceo"


def lx(a, c=1, v="x"):
    return show(P([(c, {v: 1}), (-a, {})]))


def s1_semplice():
    p, q = R.sample([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 0], 2)
    a, b = R.sample([2, 3, 4, 5, 6, 7], 2)
    # a/(x − p) = b/(x − q) → a(x − q) = b(x − p) → (a − b)x = a q − b p
    x = Fr(a * q - b * p, a - b)
    if x in (p, q) or x.denominator > 4:
        return None
    w = [Fr(a * q + b * p, a - b), Fr(b * q - a * p, a - b), Fr(a * p - b * q, a - b), -x, Fr(a * q - b * p, a + b)]
    return M("Risolvi: %s = %s" % (FR(str(a), lx(p)), FR(str(b), lx(q))), ex(x), [ex(v) for v in w if v != x],
             "C.E.: x ≠ %s, x ≠ %s. Moltiplico in croce: %d(%s) = %d(%s) → <b>x = %s</b>, accettabile." % (fq(p), fq(q), a, lx(q), b, lx(p), fq(x)))


def s1_tipo2():
    a = R.randint(1, 6)
    r = R.choice([v for v in range(-6, 7) if v not in (a, -a)])
    # x/(x − a) + c/(x + a) = N/(x² − a²)  con soluzione r
    c = nz(R, -4, 4)
    N = r * (r + a) + c * (r - a)
    num_lhs = "%s + %s" % (FR("x", lx(a)), FR(str(c), lx(-a))) if c > 0 else "%s − %s" % (FR("x", lx(a)), FR(str(-c), lx(-a)))
    # x(x + a) + c(x − a) = N → x² + (a + c)x − ca − N = 0 : altre radici
    bb, cc = a + c, -c * a - N
    disc = bb * bb - 4 * cc
    import math
    sq = math.isqrt(disc) if disc >= 0 else -1
    if sq * sq != disc:
        return None
    rs = sorted(set([Fr(-bb + sq, 2), Fr(-bb - sq, 2)]))
    ok = [t for t in rs if t not in (a, -a)]
    if not ok:
        return None
    from it_liceo import sol
    ans = sol(ok)
    rej = [t for t in rs if t in (a, -a)]
    w = [sol(rs) if rej else sol([-t for t in ok]), "impossibile", sol([ok[0] + 1]) if len(ok) == 1 else sol(ok[:1])]
    return M("Risolvi: %s = %s" % (num_lhs, FR(str(N) if N >= 0 else "−%d" % -N, show(P([(1, {"x": 2}), (-a * a, {})])))), ans, [x for x in w if x != ans] + [sol(rej + [99])[:0] or "x = 0"] if False else [x for x in w if x != ans],
             "C.E.: x ≠ ±%d. m.c.m. x² − %d: x(x + %d) %s %d(x − %d) = %s → %s. %s" % (a, a * a, a, "+" if c > 0 else "−", abs(c), a, fq(N), sol(rs), ("Scarto %s perché non rispetta le C.E. Soluzione: <b>%s</b>." % (sol(rej), ans)) if rej else "Le soluzioni sono accettabili: <b>%s</b>." % ans))


def s2_imposs():
    a = R.randint(1, 6)
    # (x + k)/(x − a) = (a + k)/(x − a) → x = a non accettabile
    k = nz(R, -5, 5)
    if a + k == 0:
        return None
    q = "%s = %s" % (FR(show(P([(1, {"x": 1}), (k, {})])), lx(a)), FR(fq(a + k), lx(a)))
    return M("Risolvi: %s" % q, "impossibile (x = %d non è accettabile)" % a, [ex(a), ex(-a), "indeterminata"],
             "C.E.: x ≠ %d. Moltiplicando per (x − %d) si trova x = %d, che va scartato: l’equazione è <b>impossibile</b>." % (a, a, a))


def s3_lett():
    k = R.choice(["base", "fatt", "diff"])
    a = R.choice(["a", "k", "m"])
    if k == "base":
        c = nz(R, -5, 5)
        q = "%s%s = %s" % (a, "x", show(P([(c, {a: 1})])) if True else "")
        q = "%sx = %s" % (a, show(P([(1, {a: 2}), (c, {a: 1})])))
        ans = "se %s ≠ 0: x = %s; se %s = 0: indeterminata" % (a, show(P([(1, {a: 1}), (c, {})])), a)
        w = ["x = %s per ogni %s" % (show(P([(1, {a: 1}), (c, {})])), a), "se %s ≠ 0: x = %s; se %s = 0: impossibile" % (a, show(P([(1, {a: 1}), (c, {})])), a), "x = %s" % show(P([(1, {a: 2}), (c, {a: 1})]))]
        e = "Divido per %s solo se %s ≠ 0: x = %s. Se %s = 0 resta 0x = 0: indeterminata." % (a, a, show(P([(1, {a: 1}), (c, {})])), a)
    elif k == "fatt":
        b = R.randint(1, 5)
        q = "(%s)x = %s" % (show(P([(1, {a: 1}), (-b, {})])), show(P([(1, {a: 2}), (-b * b, {})])))
        ans = "se %s ≠ %d: x = %s; se %s = %d: indeterminata" % (a, b, show(P([(1, {a: 1}), (b, {})])), a, b)
        w = ["x = %s per ogni %s" % (show(P([(1, {a: 1}), (b, {})])), a), "se %s ≠ %d: x = %s; se %s = %d: impossibile" % (a, b, show(P([(1, {a: 1}), (b, {})])), a, b), "se %s ≠ %d: x = %s; se %s = %d: indeterminata" % (a, b, show(P([(1, {a: 1}), (-b, {})])), a, b)]
        e = "%s = (%s)(%s). Se %s ≠ %d divido: x = %s. Se %s = %d: 0x = 0, indeterminata." % (show(P([(1, {a: 2}), (-b * b, {})])), show(P([(1, {a: 1}), (-b, {})])), show(P([(1, {a: 1}), (b, {})])), a, b, show(P([(1, {a: 1}), (b, {})])), a, b)
    else:
        b = R.randint(1, 5)
        c = nz(R, -6, 6)
        if c == 0:
            return None
        q = "(%s)x = %d" % (show(P([(1, {a: 1}), (-b, {})])), c)
        ans = "se %s ≠ %d: x = %s; se %s = %d: impossibile" % (a, b, FR(str(c), show(P([(1, {a: 1}), (-b, {})]))), a, b)
        w = ["x = %s per ogni %s" % (FR(str(c), show(P([(1, {a: 1}), (-b, {})]))), a), "se %s ≠ %d: x = %s; se %s = %d: indeterminata" % (a, b, FR(str(c), show(P([(1, {a: 1}), (-b, {})]))), a, b), "se %s ≠ %d: x = %d(%s)" % (a, b, c, show(P([(1, {a: 1}), (-b, {})])))]
        e = "Se %s ≠ %d divido per %s. Se %s = %d resta 0x = %d: impossibile." % (a, b, show(P([(1, {a: 1}), (-b, {})])), a, b, c)
    return M("Risolvi e discuti l’equazione letterale nell’incognita x: %s" % q, ans, w, e)


FORM = [("v = s/t (velocità)", "t", "t = s/v", ["t = v · s", "t = v/s", "t = s − v"]),
        ("A = b · h/2 (area del triangolo)", "h", "h = 2A/b", ["h = A/(2b)", "h = 2b/A", "h = A − b/2"]),
        ("P = 2(a + b) (perimetro del rettangolo)", "b", "b = P/2 − a", ["b = P/2 + a", "b = (P − a)/2", "b = 2P − a"]),
        ("F = m · a (secondo principio)", "m", "m = F/a", ["m = F · a", "m = a/F", "m = F − a"]),
        ("y = mx + q (retta)", "x", "x = (y − q)/m", ["x = y/m − q", "x = (y + q)/m", "x = m(y − q)"]),
        ("A = (B + b) · h/2 (area del trapezio)", "h", "h = 2A/(B + b)", ["h = A/(B + b)", "h = 2A − (B + b)", "h = (B + b)/(2A)"]),
        ("C = 2πr (circonferenza)", "r", "r = C/(2π)", ["r = 2πC", "r = C − 2π", "r = 2C/π"]),
        ("d = m/V (densità)", "V", "V = m/d", ["V = m · d", "V = d/m", "V = m − d"]),
        ("s = v<sub>0</sub>t + ½at² (moto uniformemente accelerato)", "a", "a = 2(s − v<sub>0</sub>t)/t²", ["a = (s − v<sub>0</sub>t)/(2t²)", "a = 2s/t² − v<sub>0</sub>t", "a = (2s − v<sub>0</sub>)/t²"]),
        ("E = ½mv² (energia cinetica)", "m", "m = 2E/v²", ["m = E/(2v²)", "m = 2Ev²", "m = 2v²/E"]),
        ("S = C(1 + rt) (montante con interesse semplice)", "t", "t = (S − C)/(Cr)", ["t = (S − C)/r", "t = S/(Cr) − 1", "t = (S + C)/(Cr)"])]


def s4_form():
    f, v, a, w = R.choice(FORM)
    return M("Dalla formula %s ricava %s." % (f, v), a, w, "Isolo %s con i principi di equivalenza (le altre lettere sono diverse da 0): <b>%s</b>." % (v, a))


def s5_lett_num():
    a = R.choice([2, 3, 4, 5, -2, -3])
    b = R.randint(1, 6)
    # equazione letterale con il parametro dato: (a − 1)x = a + b
    x = Fr(a + b, a - 1) if a != 1 else None
    if x is None or x.denominator > 5:
        return None
    return M("Nell’equazione (k − 1)x = k + %d, quanto vale x per k = %s?" % (b, fq(a)), ex(x), [ex(t) for t in (Fr(a - 1, a + b), Fr(a + b, a + 1), -x, x + 1) if t != x],
             "Sostituisco k = %s: %s = %s → <b>x = %s</b>." % (fq(a), show(P([(a - 1, {"x": 1})])), fq(a + b), fq(x)))


def main():
    seen = set()
    sets = [
        ("Equazioni fratte", mix(R, seen, [(s1_semplice, 20)])),
        ("Fratte con soluzioni da scartare", mix(R, seen, [(s1_tipo2, 14), (s2_imposs, 6)])),
        ("Equazioni letterali", mix(R, seen, [(s3_lett, 14), (s5_lett_num, 6)])),
        ("Formule inverse", mix(R, seen, [(s4_form, 11), (s1_semplice, 9)])),
        ("Riepilogo", mix(R, seen, [(s1_tipo2, 6), (s3_lett, 6), (s2_imposs, 4), (s5_lett_num, 4)])),
    ]
    body = L(["In un’equazione <b>fratta</b> l’incognita compare al denominatore. Si scrivono le <b>C.E.</b> (denominatori ≠ 0), si moltiplica per il m.c.m. e si risolve.",
              "Alla fine si <b>controlla</b> ogni soluzione con le C.E.: quelle che annullano un denominatore si scartano. Se si scartano tutte, l’equazione è impossibile.",
              "In un’equazione <b>letterale</b> compaiono altre lettere (parametri). Si arriva ad Ax = B e si <b>discute</b>: se A ≠ 0, x = B/A; se A = 0 e B ≠ 0 è impossibile; se A = 0 e B = 0 è indeterminata.",
              "Le <b>formule inverse</b> sono equazioni letterali: si isola la lettera richiesta."],
             [("x/(x − 2) = 2/(x − 2) + 3", ["C.E. x ≠ 2", "x = 2 + 3(x − 2) → x = 2"], "impossibile (x = 2 si scarta)"),
              ("(a − 2)x = a² − 4", ["Se a ≠ 2: x = a + 2", "Se a = 2: 0x = 0"], "indeterminata per a = 2")],
             [["Non controllare le C.E.", "Una soluzione che annulla un denominatore non è accettabile."],
              ["Dividere per a senza condizioni", "Si divide per un parametro solo se è diverso da 0; il caso a = 0 si studia a parte."],
              ["Da v = s/t scrivere t = v · s", "Moltiplico per t e divido per v: t = s/v."]])
    faq = [("Perché in un’equazione fratta alcune soluzioni si scartano?", "Perché moltiplicando per il m.c.m. si passa a un’equazione intera che può avere soluzioni in più: quelle che annullano un denominatore non risolvono l’equazione di partenza."),
           ("Che cosa vuol dire discutere un’equazione letterale?", "Studiare, al variare del parametro, se l’equazione è determinata, impossibile o indeterminata, distinguendo i valori che annullano il coefficiente di x.")]
    unit(G, R, "equazioni-fratte-e-letterali", "A",
         "Equazioni fratte e letterali; risolvere problemi e ricavare formule inverse",
         "Equazioni fratte e letterali", "Equazioni fratte e letterali",
         "Schede di matematica per la seconda liceo sulle equazioni fratte e letterali: condizioni di esistenza, soluzioni da scartare, equazioni impossibili, discussione delle equazioni letterali, formule inverse. 100 esercizi con soluzioni.",
         "Controlla le soluzioni con le C.E.", "Nelle letterali: se il coefficiente di x può essere 0, discuti i casi.",
         body, faq, sets, 2)


if __name__ == "__main__":
    main()
