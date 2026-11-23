# -*- coding: utf-8 -*-
"""
Italia Matematica prima liceo: Monomi e polinomi (Aritmetica e algebra)
  python3 tools/gen_it_matematica_l1_monomi_e_polinomi.py
Grado di un monomio e di un polinomio, monomi simili, somma algebrica, prodotto, quoziente e potenza di monomi,
MCD e mcm di monomi, somma e prodotto di polinomi, valore numerico.
Errori: sommare gli esponenti nella somma, moltiplicare gli esponenti nel prodotto, (2a)² = 2a², dimenticare un prodotto.
"""
import math
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, P, show, mul, add, evalp, par

R = R0 = random.Random(72103)
G = "prima-liceo"


def rex(vs="abx", lo=1, hi=4, k=None):
    k = k or R.randint(1, min(3, len(vs)))
    return {v: R.randint(lo, hi) for v in R.sample(vs, k)}


def m(c, ex):
    return show(P([(c, ex)]))


def flip(r, i=-1):
    ks = sorted(r, key=lambda k: -sum(e for _, e in k))
    k = ks[i]
    out = dict(r)
    out[k] = -out[k]
    return out


def s1_grado():
    ex = rex("abcxy", 1, 5, R.randint(2, 3))
    c = nz(R, -9, 9)
    tot = sum(ex.values())
    if R.random() < 0.5:
        v = R.choice(sorted(ex))
        e = ex[v]
        return M("Qual è il grado del monomio %s rispetto alla lettera %s?" % (m(c, ex), v), str(e), W(tot, e + 1, abs(c) if abs(c) != e else None, len(ex), e - 1 if e > 1 else None),
                 "Il grado rispetto a %s è l’esponente di %s: <b>%d</b>." % (v, v, e))
    return M("Qual è il grado (complessivo) del monomio %s?" % m(c, ex), str(tot), W(max(ex.values()), len(ex), tot + abs(c) if abs(c) > 1 else tot + 1, tot - 1),
             "Il grado complessivo è la somma degli esponenti delle lettere: %s = <b>%d</b> (il coefficiente non conta)." % (" + ".join(str(x) for _, x in sorted(ex.items())), tot))


def s1_somma():
    ex = rex("abxy", 1, 3, R.randint(1, 2))
    cs = [nz(R, -9, 9) for _ in range(R.randint(2, 3))]
    tot = sum(cs)
    if tot == 0:
        return None
    q = " ".join(("" if i == 0 else ("+ " if c > 0 else "− ")) + m(c if i == 0 else abs(c), ex) for i, c in enumerate(cs))
    ex2 = {k: v * len(cs) for k, v in ex.items()}
    w = [m(tot, ex2), m(sum(abs(c) for c in cs), ex), m(-tot, ex), m(tot + 1 if tot != -1 else tot - 1, ex)]
    return M("Calcola: %s" % q, m(tot, ex), W(*w), "Sono monomi simili: si sommano i coefficienti (%s) e la parte letterale resta uguale: <b>%s</b>." % (" + ".join(par(c) for c in cs), m(tot, ex)))


def s1_prod():
    e1, e2 = rex("abx", 1, 4, 2), rex("abx", 1, 4, 2)
    c1, c2 = nz(R, -6, 6), nz(R, -6, 6)
    if abs(c1) == 1 and abs(c2) == 1:
        return None
    pr = {k: e1.get(k, 0) + e2.get(k, 0) for k in set(e1) | set(e2)}
    wrong = {k: e1.get(k, 1) * e2.get(k, 1) for k in set(e1) | set(e2)}
    w = [m(c1 * c2, wrong) if wrong != pr else None, m(c1 + c2, pr) if c1 + c2 else None, m(-c1 * c2, pr)]
    return M("Calcola: (%s) · (%s)" % (m(c1, e1), m(c2, e2)), m(c1 * c2, pr), W(*w),
             "Si moltiplicano i coefficienti e, per ogni lettera, si sommano gli esponenti: <b>%s</b>." % m(c1 * c2, pr))


def s2_quoz():
    e2 = rex("abx", 1, 3, 2)
    extra = {k: R.randint(0, 3) for k in e2}
    e1 = {k: e2[k] + extra[k] for k in e2}
    c2 = nz(R, -6, 6)
    cq = nz(R, -5, 5)
    c1 = c2 * cq
    if abs(c2) == 1:
        return None
    qex = {k: v for k, v in extra.items() if v}
    if not qex:
        return None
    wr = {k: e1[k] + e2[k] for k in e2}
    w = [m(cq, wr), m(-cq, qex), m(c1 - c2, qex) if c1 != c2 else None, m(cq, {k: v for k, v in e1.items()})]
    return M("Calcola: (%s) : (%s)" % (m(c1, e1), m(c2, e2)), m(cq, qex), W(*w),
             "Si dividono i coefficienti (%s : %s = %s) e si sottraggono gli esponenti: <b>%s</b>." % (par(c1), par(c2), fq(cq), m(cq, qex)))


def s2_pot():
    ex = rex("abx", 1, 3, R.randint(1, 2))
    c = R.choice([-3, -2, 2, 3, Fr(1, 2), Fr(-1, 2), Fr(2, 3)])
    n = R.choice([2, 2, 3])
    pex = {k: v * n for k, v in ex.items()}
    w = [m(c * n, pex), m(c, pex), m(c ** n, {k: v + n for k, v in ex.items()}), m(-(c ** n), pex)]
    return M("Calcola: (%s)<sup>%d</sup>" % (m(c, ex), n), m(c ** n, pex), W(*w),
             "Si eleva il coefficiente (%s<sup>%d</sup> = %s) e si moltiplicano gli esponenti per %d: <b>%s</b>." % (par(c), n, fq(c ** n), n, m(c ** n, pex)))


def s3_mcd():
    vs = ["a", "b"] if R.random() < 0.6 else ["x", "y"]
    ms = []
    for _ in range(R.randint(2, 3)):
        ms.append((R.choice([2, 3, 4, 6, 8, 9, 10, 12, 15, 18]), {v: R.randint(0 if i else 1, 4) for i, v in enumerate(vs)}))
    g = math.gcd(*[c for c, _ in ms])
    l = 1
    for c, _ in ms:
        l = l * c // math.gcd(l, c)
    gex = {v: min(e.get(v, 0) for _, e in ms) for v in vs}
    lex = {v: max(e.get(v, 0) for _, e in ms) for v in vs}
    q = "; ".join(m(c, e) for c, e in ms)
    if R.random() < 0.5:
        return M("Calcola il MCD dei monomi %s." % q, m(g, gex), W(m(l, gex), m(g, lex), m(1, gex) if g != 1 else m(2, gex), m(g * 2, gex)),
                 "MCD: MCD dei coefficienti (%d) e lettere comuni con il minimo esponente: <b>%s</b>." % (g, m(g, gex)))
    return M("Calcola il mcm dei monomi %s." % q, m(l, lex), W(m(g, lex), m(l, gex), m(math.prod(c for c, _ in ms), lex) if math.prod(c for c, _ in ms) != l else m(l * 2, lex)),
             "mcm: mcm dei coefficienti (%d) e tutte le lettere con il massimo esponente: <b>%s</b>." % (l, m(l, lex)))


def rp(k=3, vs="x"):
    t = []
    es = sorted(R.sample(range(0, 4), k), reverse=True)
    for e in es:
        t.append((nz(R, -7, 7), {vs: e} if e else {}))
    return P(t)


def s3_gradop():
    p = add(add(P([(nz(R, -5, 5), rex("ab", 1, 4, 2))]), P([(nz(R, -5, 5), rex("ab", 1, 4, R.randint(1, 2)))])), P([(nz(R, -5, 5), {})]))
    if len(p) < 3:
        return None
    gr = max(sum(e for _, e in k) for k in p)
    alt = sorted(set(sum(e for _, e in k) for k in p))
    w = [len(p), alt[0] if alt[0] != gr else None, max(e for k in p for _, e in k), gr + 1]
    return M("Qual è il grado del polinomio %s?" % show(p), str(gr), W(*w), "Il grado di un polinomio è il grado più alto tra quelli dei suoi termini: <b>%d</b>." % gr)


def s4_somma():
    p, q = rp(3), rp(3)
    s_ = R.choice([1, -1])
    r = add(p, q, s_)
    if not r or len(r) < 2:
        return None
    wrong = add(p, {k: v if s_ == -1 and i == 0 else v * s_ for i, (k, v) in enumerate(q.items())}) if s_ == -1 else add(p, q, -1)
    w = [show(wrong), show(add(p, q, -s_)), show(flip(r)), show(flip(r, 0)), show(add(r, P([(1, {})])))]
    return M("Calcola: (%s) %s (%s)" % (show(p), "+" if s_ > 0 else "−", show(q)), show(r), W(*[x for x in w if x != show(r)]),
             "%s e sommo i termini simili: <b>%s</b>." % ("Tolgo le parentesi" if s_ > 0 else "Il segno − davanti alla parentesi cambia tutti i segni del secondo polinomio", show(r)))


def s4_monpol():
    c = nz(R, -5, 5)
    e = {"x": R.randint(1, 2)}
    p = rp(R.randint(2, 3))
    r = mul(P([(c, e)]), p)
    first = mul(P([(c, e)]), {list(p)[0]: p[list(p)[0]]})
    partial = add(first, {k: v for k, v in list(p.items())[1:]})
    w = [show(partial), show(mul(P([(-c, e)]), p)), show(mul(P([(c, {})]), p))]
    return M("Calcola: %s(%s)" % (m(c, e) if c > 0 else "(%s)" % m(c, e), show(p)), show(r), W(*[x for x in w if x != show(r)]),
             "Proprietà distributiva: il monomio moltiplica <b>ogni</b> termine del polinomio: <b>%s</b>." % show(r))


def s5_polpol():
    a, b = nz(R, -6, 6), nz(R, -6, 6)
    c, dd = R.choice([1, 1, 2, 3]), nz(R, -6, 6)
    p = P([(1, {"x": 1}), (a, {})])
    q = P([(c, {"x": 1}), (dd, {})])
    r = mul(p, q)
    w = [show(add(P([(c, {"x": 2})]), P([(a * dd, {})]))), show(add(r, P([(-(a * c + dd), {"x": 1})]))), show(mul(p, P([(c, {"x": 1}), (-dd, {})]))), show(mul(P([(1, {"x": 1}), (-a, {})]), q)), show(flip(r))]
    return M("Calcola: (%s)(%s)" % (show(p), show(q)), show(r), W(*[x for x in w if x != show(r)]),
             "Ogni termine del primo per ogni termine del secondo, poi sommo i simili: <b>%s</b>." % show(r))


def s5_val():
    p = add(rp(3), P([(nz(R, -3, 3), {"x": 1, "y": 1})]))
    x, y = nz(R, -3, 3), nz(R, -3, 3)
    v = evalp(p, {"x": x, "y": y})
    w = [evalp(p, {"x": -x, "y": y}), evalp(p, {"x": abs(x), "y": abs(y)}), v + 2, -v]
    return M("Calcola il valore del polinomio %s per x = %s e y = %s." % (show(p), fq(x), fq(y)), fq(v), [fq(t) for t in w if t != v],
             "Sostituisco le lettere tra parentesi e rispetto l’ordine delle operazioni: <b>%s</b>." % fq(v))


def main():
    seen = set()
    sets = [
        ("Grado e monomi simili", mix(R, seen, [(s1_grado, 10), (s1_somma, 10)])),
        ("Prodotto, quoziente, potenza", mix(R, seen, [(s1_prod, 7), (s2_quoz, 7), (s2_pot, 6)])),
        ("MCD e mcm di monomi", mix(R, seen, [(s3_mcd, 14), (s3_gradop, 6)])),
        ("Somma di polinomi e prodotto per un monomio", mix(R, seen, [(s4_somma, 10), (s4_monpol, 10)])),
        ("Prodotto di polinomi e valore numerico", mix(R, seen, [(s5_polpol, 12), (s5_val, 8)])),
    ]
    body = L(["Un <b>monomio</b> è un prodotto di numeri e lettere (−3a²b). Il <b>grado</b> è la somma degli esponenti delle lettere. Monomi <b>simili</b> hanno la stessa parte letterale.",
              "Somma di monomi simili: si sommano i coefficienti, la parte letterale non cambia. Prodotto: coefficienti per coefficienti e, per ogni lettera, si <b>sommano</b> gli esponenti. Potenza: si eleva il coefficiente e si <b>moltiplicano</b> gli esponenti.",
              "MCD di monomi: MCD dei coefficienti e lettere comuni con il minimo esponente. mcm: mcm dei coefficienti e tutte le lettere con il massimo esponente.",
              "Prodotto di polinomi: ogni termine del primo per ogni termine del secondo, poi si riducono i termini simili."],
             [("Calcola (−2a²b)³.", ["(−2)³ = −8; esponenti per 3."], "−8a⁶b³"),
              ("Calcola (x + 3)(2x − 5).", ["2x² − 5x + 6x − 15."], "2x² + x − 15")],
             [["3a² + 2a² = 5a⁴", "Nella somma gli esponenti non cambiano: 5a²."],
              ["a² · a³ = a⁶", "Nel prodotto si sommano gli esponenti: a⁵."],
              ["(2a)² = 2a²", "Si eleva anche il coefficiente: 4a²."],
              ["−(x − 3) = −x − 3", "Il segno − cambia tutti i segni: −x + 3."]])
    faq = [("Due monomi con lo stesso grado sono simili?", "No. Sono simili se hanno la stessa parte letterale (le stesse lettere con gli stessi esponenti): 3a²b e a²b sono simili, 3a²b e 3ab² no, anche se hanno lo stesso grado."),
           ("Si può sempre dividere un monomio per un altro?", "Il quoziente è un monomio solo se ogni lettera del divisore compare nel dividendo con esponente maggiore o uguale. Altrimenti si ottiene una frazione algebrica.")]
    unit(G, R, "monomi-e-polinomi", "A",
         "Calcolo con i monomi e i polinomi: operazioni, grado, MCD e mcm di monomi, valore numerico",
         "Monomi e polinomi", "Monomi e polinomi",
         "Schede di matematica per la prima liceo su monomi e polinomi: grado, monomi simili, somma, prodotto, quoziente e potenza di monomi, MCD e mcm, somma e prodotto di polinomi, valore numerico. 100 esercizi con soluzioni.",
         "Prodotto: si sommano gli esponenti.", "Potenza: si moltiplicano gli esponenti. Somma di monomi simili: gli esponenti restano uguali.",
         body, faq, sets, 3)


if __name__ == "__main__":
    main()
