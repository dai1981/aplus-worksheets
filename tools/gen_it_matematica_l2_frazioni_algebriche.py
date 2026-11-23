# -*- coding: utf-8 -*-
"""
Italia Matematica seconda liceo: Frazioni algebriche (Aritmetica e algebra)
  python3 tools/gen_it_matematica_l2_frazioni_algebriche.py
Condizioni di esistenza, semplificazione (scomponendo), m.c.m. dei denominatori, somma e differenza, prodotto e quoziente,
potenza, valore di una frazione algebrica.
Errori: semplificare termini e non fattori, C.E. solo del denominatore finale, nel quoziente C.E. anche del numeratore del divisore.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, P, show, mul, add, FR

R = random.Random(72201)
G = "seconda-liceo"


def lx(a, c=1):
    """c·x − a"""
    return show(P([(c, {"x": 1}), (-a, {})]))


def fx(*roots):
    """prodotto di fattori (x − r) come testo"""
    out = ""
    for r in roots:
        out += "(%s)" % lx(r) if len(roots) > 1 or True else lx(r)
    return out


def pf(*roots):
    p = P([(1, {})])
    for r in roots:
        p = mul(p, P([(1, {"x": 1}), (-r, {})]))
    return p


def ce(rs):
    rs = sorted(set(rs))
    if len(rs) == 2 and rs[0] == -rs[1]:
        return "x ≠ ±%s" % fq(rs[1])
    return " ∧ ".join("x ≠ %s" % fq(r) for r in rs)


def s1_ce():
    k = R.choice(["lin", "diff", "trin", "x"])
    if k == "lin":
        a = nz(R, -9, 9)
        den, rs = show(pf(a)), [a]
        w = [ce([-a]), "ℝ", "x ≠ 0"]
    elif k == "diff":
        a = R.randint(1, 8)
        den, rs = show(pf(a, -a)), [a, -a]
        w = ["x ≠ %d" % a, "x ≠ %d" % (a * a), "ℝ", "x ≠ −%d" % a, "x ≠ 0"]
    elif k == "trin":
        a, b = R.sample([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6], 2)
        den, rs = show(pf(a, b)), [a, b]
        w = [ce([-a, -b]), ce([a]), ce([a * b]) if a * b not in (a, b) else "ℝ"]
    else:
        a = nz(R, -6, 6)
        den, rs = show(mul(P([(1, {"x": 1})]), pf(a))), [0, a]
        w = [ce([a]), ce([0, -a]), "x ≠ 0"]
    n = show(P([(R.randint(1, 5), {"x": 1}), (R.randint(-6, 6), {})]))
    return M("Quali sono le condizioni di esistenza della frazione %s?" % FR(n, den), ce(rs), w,
             "Il denominatore non deve annullarsi: scompongo %s e pongo ogni fattore ≠ 0: <b>%s</b>." % (den, ce(rs)))


def s1_sempl():
    a, b, c = R.sample([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 0], 3)
    n, dd = pf(a, b), pf(a, c)
    ans = FR(lx(b), lx(c))
    wrong_terms = FR(show(add(n, P([(-1, {"x": 2})]))) if False else lx(b), lx(-c))
    w = [FR(lx(-b), lx(-c)), FR(lx(c), lx(b)), "%s" % FR(show(add(n, P([(-1, {"x": 2})]))), show(add(dd, P([(-1, {"x": 2})])))) if show(add(n, P([(-1, {"x": 2})]))) != "0" else FR(lx(b), lx(a))]
    return M("Semplifica: %s" % FR(show(n), show(dd)), ans, [x for x in w if x != ans],
             "Scompongo: %s. Semplifico il <b>fattore</b> comune (%s): <b>%s</b> (con %s)." % (FR("(%s)(%s)" % (lx(a), lx(b)), "(%s)(%s)" % (lx(a), lx(c))), lx(a), ans, ce([a, c])))


def s2_somma():
    a, b = R.sample([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5], 2)
    p, q = nz(R, -4, 4), R.randint(1, 4)
    s = R.choice([1, -1])
    num = add(mul(P([(p, {})]), pf(b)), mul(P([(s * q, {})]), pf(a)))
    if not num or len(num) < 1:
        return None
    den = "(%s)(%s)" % (lx(a), lx(b))
    ans = FR(show(num), den)
    wrong = add(mul(P([(p, {})]), pf(b)), mul(P([(q, {})]), pf(a)), 1) if s < 0 else add(mul(P([(p, {})]), pf(a)), mul(P([(q, {})]), pf(b)))
    w = [FR(show(wrong), den), FR(fq(p + s * q), den), FR(fq(p + s * q), show(add(pf(a), pf(b))))]
    return M("Calcola: %s %s %s" % (FR(fq(p), lx(a)), "+" if s > 0 else "−", FR(fq(q), lx(b))), ans, [x for x in w if x != ans],
             "m.c.m. dei denominatori: %s. Numeratore: %s(%s) %s %s(%s) = %s: <b>%s</b>." % (den, fq(p), lx(b), "+" if s > 0 else "−", fq(q), lx(a), show(num), ans))


def s2_somma_x():
    a = R.randint(1, 6)
    k = R.choice(["diff", "same"])
    if k == "diff":
        ans = FR(show(P([(2, {"x": 1})])), show(pf(a, -a)))
        w = [FR("2", show(pf(a, -a))), FR("2", "2x"), FR(fq(2 * a), show(pf(a, -a))), FR("2x", show(P([(1, {"x": 2}), (a * a, {})])))]
        return M("Calcola: %s + %s" % (FR("1", lx(a)), FR("1", lx(-a))), ans, w,
                 "Denominatore comune (x − %d)(x + %d) = x² − %d; numeratore (x + %d) + (x − %d) = 2x: <b>%s</b>." % (a, a, a * a, a, a, ans))
    b = R.randint(1, 6)
    return M("Calcola: %s − %s" % (FR("x", lx(b)), FR(fq(b), lx(b))), "1", ["0", FR("x + %d" % b if b > 0 else "x − %d" % -b, lx(b)), "x"],
             "Stesso denominatore: %s = <b>1</b> (con x ≠ %s)." % (FR(lx(b), lx(b)), fq(b)))


def s3_prod():
    a, b, c = R.sample([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5], 3)
    k = nz(R, -4, 4)
    # [(x−a)(x−b)/(x−c)] · [k/(x−a)] = k(x−b)/(x−c)
    ans = FR(show(mul(P([(k, {})]), pf(b))), lx(c))
    w = [FR(show(mul(P([(k, {})]), pf(a, b))), "(%s)(%s)" % (lx(c), lx(a))), FR(show(pf(b)), lx(c)), FR(show(mul(P([(k, {})]), pf(-b))), lx(-c)), FR(show(mul(P([(k, {})]), pf(b))), lx(a))]
    return M("Calcola: %s · %s" % (FR(show(pf(a, b)), lx(c)), FR(fq(k), lx(a))), ans, [x for x in w if x != ans],
             "Scompongo e semplifico in croce il fattore (%s): <b>%s</b>." % (lx(a), ans))


def s3_quoz():
    a, b = R.sample([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5], 2)
    c = R.choice([2, 3, 4, 5])
    # (x² − a²)/c : (x + a)/(c x) ... semplice: [(x−a)(x−b)]/c : (x−a)/(c·x)  = x(x−b)
    ans = show(mul(P([(1, {"x": 1})]), pf(b)))
    w = [FR("(%s)²(%s)" % (lx(a), lx(b)), "%dx" % (c * c)) if False else FR("(%s)" % lx(b), "x"), show(pf(b)), show(mul(P([(c * c, {"x": 1})]), pf(b)))]
    return M("Calcola: %s : %s" % (FR(show(pf(a, b)), str(c)), FR(lx(a), "%dx" % c)), ans, [x for x in w if x != ans],
             "Si moltiplica per l’inversa del divisore: %s · %s = <b>%s</b>. C.E.: x ≠ 0 e x ≠ %s (anche il numeratore del divisore non deve annullarsi)." % (FR(show(pf(a, b)), str(c)), FR("%dx" % c, lx(a)), ans, fq(a)))


def s4_val():
    a, b = R.sample([-4, -3, -2, -1, 1, 2, 3, 4], 2)
    x = R.choice([v for v in range(-5, 6) if v not in (a, b)])
    n = P([(1, {"x": 1}), (-a, {})])
    dd = mul(P([(1, {"x": 1}), (-a, {})]), P([(1, {"x": 1}), (-b, {})]))
    v = Fr(x - a, (x - a) * (x - b)) if x != a else None
    if v is None:
        return None
    if R.random() < 0.3:
        x = a
        return M("La frazione %s esiste per x = %s?" % (FR(show(n), show(dd)), fq(x)), "no, il denominatore si annulla", ["sì, vale 0", "sì, vale 1", "sì, vale %s" % fq(Fr(1, a - b) if a != b else 1)],
                 "Per x = %s il denominatore vale 0, quindi la frazione non esiste (anche se semplificata sembra calcolabile): <b>no</b>." % fq(x))
    return M("Calcola il valore di %s per x = %s." % (FR(show(n), show(dd)), fq(x)), fq(v), [fq(t) for t in (Fr(1, x + b) if x + b else Fr(2), Fr(x - a), -v, v + 1) if t != v],
             "Semplifico: %s, poi sostituisco: 1/(%s − %s) = <b>%s</b>." % (FR("1", lx(b)), fq(x), "(%s)" % fq(b) if b < 0 else fq(b), fq(v)))


def s5_mcm():
    a, b = R.sample([1, 2, 3, 4, 5, 6], 2)
    k = R.choice(["d", "t"])
    if k == "d":
        dens = [show(pf(a, -a)), lx(a) if R.random() < 0.5 else lx(-a), show(mul(P([(2, {})]), pf(a)))]
        ans = "2(%s)(%s)" % (lx(-a), lx(a))
        w = ["(%s)(%s)" % (lx(-a), lx(a)), "2(%s)²(%s)" % (lx(a), lx(-a)), "2(%s)" % show(pf(a, -a)) + "(%s)" % lx(a)]
    else:
        dens = [show(pf(a, b)), show(pf(a)), show(pf(b, -b)) if b != a else show(pf(-a))]
        rs = sorted(set([a, b, -b]))
        ans = "".join("(%s)" % lx(r) for r in rs)
        w = ["(%s)(%s)" % (lx(a), lx(b)), "".join("(%s)" % lx(r) for r in [a, a, b, b, -b]), "".join("(%s)" % lx(r) for r in sorted(set([a, b])))]
        w = [x for x in w if x != ans] + ["(%s)²(%s)" % (lx(a), lx(b))]
    return M("Qual è il m.c.m. dei denominatori %s?" % "; ".join(dens), ans, [x for x in w if x != ans],
             "Scompongo ogni denominatore e prendo tutti i fattori, comuni e non comuni, una volta con il massimo esponente: <b>%s</b>." % ans)


def main():
    seen = set()
    sets = [
        ("Condizioni di esistenza", mix(R, seen, [(s1_ce, 20)])),
        ("Semplificazione", mix(R, seen, [(s1_sempl, 14), (s4_val, 6)])),
        ("m.c.m. e somma", mix(R, seen, [(s5_mcm, 8), (s2_somma, 8), (s2_somma_x, 4)])),
        ("Somma e differenza", mix(R, seen, [(s2_somma, 14), (s2_somma_x, 6)])),
        ("Prodotto e quoziente", mix(R, seen, [(s3_prod, 10), (s3_quoz, 10)])),
    ]
    body = L(["Una <b>frazione algebrica</b> ha un polinomio al numeratore e al denominatore. Prima di tutto si scrivono le <b>condizioni di esistenza</b> (C.E.): il denominatore non deve annullarsi.",
              "Per <b>semplificare</b> si scompongono numeratore e denominatore e si dividono i <b>fattori</b> comuni (mai i singoli termini).",
              "Per <b>sommare</b> si usa il m.c.m. dei denominatori scomposti, come con le frazioni numeriche. Per <b>moltiplicare</b> si semplifica in croce; per <b>dividere</b> si moltiplica per l’inversa (C.E. anche per il numeratore del divisore)."],
             [("Semplifica (x² − 9)/(x² + 3x).", ["(x + 3)(x − 3)/[x(x + 3)]", "C.E.: x ≠ 0, x ≠ −3"], "(x − 3)/x"),
              ("1/(x − 2) + 1/(x + 2)", ["m.c.m. (x − 2)(x + 2)", "(x + 2) + (x − 2) = 2x"], "2x/(x² − 4)")],
             [["(x + 3)/x = 3", "x non è un fattore del numeratore: non si semplifica."],
              ["Dimenticare le C.E.", "Si scrivono prima di semplificare, sul denominatore di partenza."],
              ["a/b − (c − d)/b = (a − c − d)/b", "Il − davanti alla frazione cambia tutti i segni: (a − c + d)/b."]])
    faq = [("Perché le condizioni di esistenza si scrivono prima di semplificare?", "Perché dopo la semplificazione un fattore sparisce dal denominatore, ma la frazione di partenza non esisteva comunque per il valore che lo annullava."),
           ("Si possono semplificare due termini uguali in una somma?", "No: si semplificano solo i fattori di un prodotto. In (x + 3)/(x + 5) non si può togliere x.")]
    unit(G, R, "frazioni-algebriche", "A",
         "Calcolo con le frazioni algebriche: condizioni di esistenza, semplificazione, operazioni",
         "Frazioni algebriche", "Frazioni algebriche",
         "Schede di matematica per la seconda liceo sulle frazioni algebriche: condizioni di esistenza, semplificazione, m.c.m. dei denominatori, somma e differenza, prodotto e quoziente, valore. 100 esercizi con soluzioni.",
         "Si semplificano i fattori, non i termini.", "Prima le condizioni di esistenza: il denominatore non deve annullarsi.",
         body, faq, sets, 1)


if __name__ == "__main__":
    main()
