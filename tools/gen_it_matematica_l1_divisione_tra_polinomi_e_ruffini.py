# -*- coding: utf-8 -*-
"""
Italia Matematica prima liceo: Divisione tra polinomi e regola di Ruffini (Aritmetica e algebra)
  python3 tools/gen_it_matematica_l1_divisione_tra_polinomi_e_ruffini.py
Divisione con quoziente e resto, regola di Ruffini per (x − a), teorema del resto, teorema di Ruffini (x − a è un fattore se P(a) = 0),
ricerca del parametro, possibili radici intere (divisori del termine noto), scomposizione di polinomi di terzo grado.
Errori: dividere per (x − a) usando −a, dimenticare i termini mancanti (coefficiente 0), resto con il segno sbagliato.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, poly, sgn

R = random.Random(72106)
G = "prima-liceo"


def ev(cs, x):
    v = 0
    for c in cs:
        v = v * x + c
    return v


def ruff(cs, a):
    q = [cs[0]]
    for c in cs[1:]:
        q.append(c + q[-1] * a)
    return q[:-1], q[-1]


def pmul(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def xa(a):
    return poly([1, -a])


def rpoly(n):
    cs = [R.choice([1, 1, 2, 3, -1, -2])] + [R.randint(-6, 6) for _ in range(n)]
    return cs


def s1_ruff():
    n = R.randint(2, 3)
    cs = rpoly(n)
    a = nz(R, -3, 3)
    q, r = ruff(cs, a)
    qa, ra = ruff(cs, -a)
    ans = poly(q)
    w = [poly(qa), poly(cs[:-1]), poly(q[:-1] + [q[-1] + 1])]
    return M("Calcola con la regola di Ruffini il quoziente della divisione (%s) : (%s)." % (poly(cs), xa(a)), ans, w,
             "Con Ruffini si usa a = %s (lo zero di %s). I coefficienti %s danno il quoziente <b>%s</b> e il resto %s." % (fq(a), xa(a), "; ".join(fq(c) for c in q + [r]), ans, fq(r)))


def s1_resto():
    n = R.randint(2, 4)
    cs = rpoly(n)
    a = nz(R, -3, 3)
    r = ev(cs, a)
    if abs(r) > 400:
        return None
    w = [ev(cs, -a), ev(cs, a) + cs[-1] if cs[-1] else -r + 1, sum(cs)]
    return M("Qual è il resto della divisione (%s) : (%s)?" % (poly(cs), xa(a)), fq(r), [fq(x) for x in w if x != r] + [fq(-r)],
             "Teorema del resto: il resto è P(%s) = <b>%s</b>." % (fq(a), fq(r)))


def s2_fatt():
    a = nz(R, -4, 4)
    b = nz(R, -4, 4)
    c = R.randint(-5, 5)
    good = R.random() < 0.5
    base = pmul([1, -a], [1, b, c])
    if not good:
        base[-1] += nz(R, -3, 3)
    t = a if good else a
    v = ev(base, t)
    ans = "sì" if v == 0 else "no"
    return M("Il polinomio %s è divisibile per %s?" % (poly(base), xa(t)), ans, ["no" if ans == "sì" else "sì", "solo se il grado è pari", "non si può sapere senza dividere"],
             "Calcolo P(%s) = %s: %s" % (fq(t), fq(v), "è 0, quindi <b>sì</b> (teorema di Ruffini)." if v == 0 else "non è 0, quindi <b>no</b>."))


def s2_param():
    a = nz(R, -3, 3)
    cs = rpoly(R.randint(2, 3))
    # P(x) = cs + k  → P(a) + k = 0
    k = -ev(cs, a)
    if abs(k) > 60:
        return None
    cs2 = cs[:-1]
    c0 = cs[-1]
    q = "%s + k" % poly(cs2 + [c0]) if c0 else "%s + k" % poly(cs2 + [0])
    w = [-k, k + a, -ev(cs, -a), k - 1]
    return M("Per quale valore di k il polinomio %s è divisibile per %s?" % (q, xa(a)), "k = %s" % fq(k), ["k = %s" % fq(x) for x in w if x != k],
             "Deve essere P(%s) = 0: %s + k = 0, quindi <b>k = %s</b>." % (fq(a), fq(ev(cs, a)), fq(k)))


def divs(n):
    n = abs(n)
    return [d for d in range(1, n + 1) if n % d == 0]


def s3_cand():
    c = R.choice([6, 8, 10, 12, 15, 4, 9, 14, 18, 20])
    cs = [1, R.randint(-5, 5), R.randint(-9, 9), -c if R.random() < 0.5 else c]
    ds = divs(c)
    ans = "±" + ", ±".join(str(d) for d in ds)
    w = ["±" + ", ±".join(str(d) for d in ds if d != 1 and d != c), ", ".join(str(d) for d in ds), "±" + ", ±".join(str(d) for d in divs(abs(cs[1]) or 7) if True)]
    return M("Quali sono le possibili radici intere del polinomio %s?" % poly(cs), ans, [x for x in w if x != ans] + ["±1, ±%d" % c],
             "Le radici intere vanno cercate tra i divisori del termine noto %s, positivi e negativi: <b>%s</b>." % (fq(cs[-1]), ans))


def s4_scomp():
    a, b, c = R.sample([-4, -3, -2, -1, 1, 2, 3, 4, 5], 3)
    cs = pmul(pmul([1, -a], [1, -b]), [1, -c])
    rs = sorted([a, b, c])
    f = lambda xs: "".join("(%s)" % xa(x) for x in xs)
    ans = f(rs)
    w = [f([-x for x in rs]), f([rs[0], rs[1], -rs[2]]), "(%s)(%s)" % (xa(rs[0]), poly(pmul([1, -rs[1]], [1, rs[2]])))]
    return M("Scomponi con la regola di Ruffini: %s" % poly(cs), ans, w,
             "P(%s) = 0, quindi %s è un fattore; divido con Ruffini e scompongo il trinomio che resta: <b>%s</b>." % (fq(rs[0]), xa(rs[0]), ans))


def s5_div2():
    q = [R.choice([1, 2, 3]), R.randint(-5, 5)]
    dv = [1, R.randint(-4, 4), nz(R, -5, 5)]
    r = [R.randint(-6, 6), R.randint(-6, 6)]
    cs = pmul(q, dv)
    cs = cs[:-2] + [cs[-2] + r[0], cs[-1] + r[1]]
    k = R.choice(["Q", "R"])
    if k == "Q":
        ans = poly(q)
        w = [poly([q[0], -q[1]]), poly([q[0], q[1] + 1]), poly([q[0], 0, q[1]])]
        return M("Calcola il quoziente della divisione (%s) : (%s)." % (poly(cs), poly(dv)), ans, w,
                 "Divido il primo termine per x², moltiplico, sottraggo e ripeto: Q(x) = <b>%s</b>, R(x) = %s." % (ans, poly(r) if any(r) else "0"))
    ans = poly(r) if any(r) else "0"
    w = [poly([-r[0], -r[1]]) if any(r) else "1", poly([r[0], r[1] + 1]), poly([r[1], r[0]]) if r[1] else poly([r[0] + 1, 0])]
    return M("Calcola il resto della divisione (%s) : (%s)." % (poly(cs), poly(dv)), ans, w,
             "Q(x) = %s; il resto ha grado minore del divisore: R(x) = <b>%s</b>." % (poly(q), ans))


def s5_mancanti():
    n = 3
    a = nz(R, -3, 3)
    cs = [1, 0, R.randint(-6, 6), R.randint(-9, 9)] if R.random() < 0.5 else [1, R.randint(-5, 5), 0, R.randint(-9, 9)]
    q, r = ruff(cs, a)
    wrong_cs = [c for c in cs if c != 0]
    wq, _ = ruff(wrong_cs, a)
    ans = poly(q)
    w = [poly(wq), poly(ruff(cs, -a)[0]), poly(q[:-1] + [q[-1] - 1])]
    return M("Dividi con Ruffini (%s) : (%s). Qual è il quoziente?" % (poly(cs), xa(a)), ans, w,
             "Il termine mancante si scrive con coefficiente 0 nella tabella: %s. Quoziente <b>%s</b>, resto %s." % ("; ".join(fq(c) for c in cs), ans, fq(r)))


def main():
    seen = set()
    sets = [
        ("Regola di Ruffini", mix(R, seen, [(s1_ruff, 14), (s5_mancanti, 6)])),
        ("Teorema del resto", mix(R, seen, [(s1_resto, 14), (s5_mancanti, 6)])),
        ("Teorema di Ruffini e parametro", mix(R, seen, [(s2_fatt, 10), (s2_param, 10)])),
        ("Divisione per un polinomio di secondo grado", mix(R, seen, [(s5_div2, 14), (s3_cand, 6)])),
        ("Scomporre con Ruffini", mix(R, seen, [(s4_scomp, 14), (s3_cand, 6)])),
    ]
    body = L(["Dividere A(x) per B(x) vuol dire trovare Q(x) e R(x) con A = B · Q + R e grado di R minore del grado di B.",
              "Per dividere per (x − a) si usa la <b>regola di Ruffini</b>: si scrivono i coefficienti (anche gli 0 dei termini mancanti), si abbassa il primo, si moltiplica per a e si somma alla colonna successiva.",
              "<b>Teorema del resto</b>: il resto della divisione di P(x) per (x − a) è P(a). <b>Teorema di Ruffini</b>: P(x) è divisibile per (x − a) se e solo se P(a) = 0.",
              "Le radici intere si cercano tra i divisori del termine noto. Trovata una radice a, si divide per (x − a) e si scompone il quoziente."],
             [("Resto di (x³ − 2x + 5) : (x + 2)", ["a = −2: P(−2) = −8 + 4 + 5."], "1"),
              ("Scomponi x³ − 7x + 6.", ["P(1) = 0: divido per (x − 1) e ottengo x² + x − 6.", "x² + x − 6 = (x + 3)(x − 2)."], "(x − 1)(x − 2)(x + 3)")],
             [["Usare a = 2 per dividere per (x + 2)", "x + 2 = x − (−2): con Ruffini si usa −2."],
              ["Saltare i termini mancanti", "x³ + 5 ha coefficienti 1, 0, 0, 5."],
              ["Pensare che il resto sia P(−a)", "Dividendo per (x − a) il resto è P(a)."]])
    faq = [("Quando si può usare la regola di Ruffini?", "Quando il divisore è di primo grado con coefficiente di x uguale a 1, cioè della forma x − a. Per dividere per 2x − 4 si può dividere per x − 2 e poi aggiustare il quoziente."),
           ("Come si trovano le radici di un polinomio di terzo grado?", "Si provano i divisori del termine noto (positivi e negativi). Se P(a) = 0, con Ruffini si divide per x − a e resta un trinomio di secondo grado da scomporre.")]
    unit(G, R, "divisione-tra-polinomi-e-ruffini", "A",
         "Divisione tra polinomi, regola di Ruffini, teorema del resto e scomposizione di polinomi",
         "Divisione tra polinomi e regola di Ruffini", "Divisione tra polinomi e Ruffini",
         "Schede di matematica per la prima liceo sulla divisione tra polinomi: quoziente e resto, regola di Ruffini, teorema del resto, teorema di Ruffini, ricerca del parametro, scomposizione di polinomi di terzo grado. 100 esercizi con soluzioni.",
         "Resto di P(x) : (x − a) = P(a)", "Se P(a) = 0, il polinomio è divisibile per x − a.",
         body, faq, sets, 6)


if __name__ == "__main__":
    main()
