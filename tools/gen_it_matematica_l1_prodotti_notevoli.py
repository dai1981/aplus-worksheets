# -*- coding: utf-8 -*-
"""
Italia Matematica prima liceo: Prodotti notevoli (Aritmetica e algebra)
  python3 tools/gen_it_matematica_l1_prodotti_notevoli.py
Quadrato di un binomio, somma per differenza, quadrato di un trinomio, cubo di un binomio, potenza di un binomio
e triangolo di Tartaglia, riconoscere un prodotto notevole, calcolo mentale (51 · 49, 99²).
Errori: (a + b)² = a² + b², dimenticare il doppio prodotto, segno del doppio prodotto, (a − b)³ con i segni sbagliati.
"""
import math
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, d, nz, P, show, mul, add

R = random.Random(72104)
G = "prima-liceo"


def term():
    """monomio a caso: (coeff, ex)"""
    v = R.choice(["x", "a", "y", "b"])
    c = R.choice([1, 1, 2, 3, 4, 5])
    e = R.choice([1, 1, 1, 2])
    return (c, {v: e})


def pair():
    v1, v2 = R.choice([("x", None), ("a", None), ("x", "y"), ("a", "b"), ("x", None)])
    c1, c2 = R.choice([1, 1, 2, 3, 4, 5]), R.choice([1, 2, 3, 4, 5, 6])
    e1 = R.choice([1, 1, 1, 2])
    t1 = (c1, {v1: e1})
    t2 = (c2, {v2: 1}) if v2 else (R.randint(1, 9), {})
    return t1, t2


def bino(t1, t2, s):
    return P([t1, (s * t2[0], t2[1])])


def pw(p, n):
    r = P([(1, {})])
    for _ in range(n):
        r = mul(r, p)
    return r


def drop_mid(r, p):
    """a² + b² senza i doppi prodotti"""
    out = {}
    for c, ex in p:
        out = add(out, mul(P([(c, ex)]), P([(c, ex)])))
    return out


def s1_quad():
    t1, t2 = pair()
    s = R.choice([1, -1])
    b = bino(t1, t2, s)
    r = pw(b, 2)
    sq_ = add(mul(P([t1]), P([t1])), mul(P([t2]), P([t2])))
    half = add(sq_, mul(P([(s, {})]), mul(P([t1]), P([t2]))))
    w = [show(sq_), show(add(sq_, mul(P([(-2 * s, {})]), mul(P([t1]), P([t2]))))), show(half), show(add(sq_, P([(-1, {})]) if False else {}) if s > 0 else add(mul(P([t1]), P([t1])), mul(P([(-1, {})]), mul(P([t2]), P([t2])))))]
    return M("Sviluppa: (%s)<sup>2</sup>" % show(b), show(r), W(*[x for x in w if x != show(r)]),
             "(A %s B)² = A² %s 2AB + B²: <b>%s</b>." % ("+" if s > 0 else "−", "+" if s > 0 else "−", show(r)))


def s1_spd():
    t1, t2 = pair()
    p, q = bino(t1, t2, 1), bino(t1, t2, -1)
    r = mul(p, q)
    A2, B2 = mul(P([t1]), P([t1])), mul(P([t2]), P([t2]))
    w = [show(add(A2, B2)), show(pw(q, 2)), show(add(B2, A2, -1)), show(add(P([(t1[0] ** 2, t1[1])]), B2, -1)) if t1[0] > 1 else show(pw(p, 2))]
    return M("Calcola: (%s)(%s)" % (show(p), show(q)), show(r), W(*[x for x in w if x != show(r)]),
             "Somma per differenza: (A + B)(A − B) = A² − B²: <b>%s</b>." % show(r))


def s2_cubo():
    v = R.choice(["x", "a"])
    c = R.choice([1, 1, 2])
    k = nz(R, -4, 4)
    b = P([(c, {v: 1}), (k, {})])
    r = pw(b, 3)
    w = [show(add(P([(c ** 3, {v: 3})]), P([(k ** 3, {})]))), show(add(pw(b, 2), {})), show(add(r, P([(-2 * 3 * c * c * k, {v: 2})])))]
    nosg = pw(P([(c, {v: 1}), (abs(k), {})]), 3)
    if k < 0:
        w.append(show(nosg))
    return M("Sviluppa: (%s)<sup>3</sup>" % show(b), show(r), W(*[x for x in w if x != show(r)]),
             "(A + B)³ = A³ + 3A²B + 3AB² + B³ (con B = %s, i segni si alternano se B è negativo): <b>%s</b>." % (fq(k), show(r)))


def s2_trin():
    k1, k2 = nz(R, -5, 5), nz(R, -5, 5)
    b = P([(1, {"x": 2}), (k1, {"x": 1}), (k2, {})]) if R.random() < 0.5 else P([(1, {"a": 1}), (k1, {"b": 1}), (k2, {})])
    r = pw(b, 2)
    terms = list(b.items())
    sq_ = {}
    for kk, c in terms:
        sq_ = add(sq_, mul({kk: c}, {kk: c}))
    w = [show(sq_), show(add(r, mul(P([(-1, {})]), mul(dict([terms[0]]), dict([terms[2]]))))) , show(add(sq_, mul(P([(2, {})]), mul(dict([terms[0]]), dict([terms[1]])))))]
    return M("Sviluppa: (%s)<sup>2</sup>" % show(b), show(r), W(*[x for x in w if x != show(r)]),
             "(A + B + C)² = A² + B² + C² + 2AB + 2AC + 2BC: <b>%s</b>." % show(r))


def binom(n, k):
    return math.comb(n, k)


def s3_tart():
    n = R.randint(4, 7)
    k = R.randint(1, n - 1)
    a = R.choice([1, 1, 2])
    c = binom(n, k) * a ** (n - k) if False else binom(n, k)
    if R.random() < 0.5:
        return M("Nello sviluppo di (x + 1)<sup>%d</sup>, qual è il coefficiente di x<sup>%d</sup>?" % (n, k) if k > 1 else "Nello sviluppo di (x + 1)<sup>%d</sup>, qual è il coefficiente di x?" % n,
                 str(c), W(n + 1, binom(n - 1, k), n * k, binom(n, k + 1) if binom(n, k + 1) != c else binom(n, k - 1) + 1, k * n),
                 "I coefficienti sono la riga %d del triangolo di Tartaglia (%s): il coefficiente è <b>%d</b>." % (n, ", ".join(str(binom(n, j)) for j in range(n + 1)), c))
    row = [binom(n, j) for j in range(n + 1)]
    wr = [[binom(n - 1, j) for j in range(n)], [binom(n, j) for j in range(n + 1)][:-1] + [n], [1] + [n] * (n - 1) + [1]]
    return M("Quali sono i coefficienti dello sviluppo di (a + b)<sup>%d</sup>?" % n, ", ".join(map(str, row)), [", ".join(map(str, x)) for x in wr],
             "Ogni numero del triangolo di Tartaglia è la somma dei due sopra di lui: riga %d = <b>%s</b>." % (n, ", ".join(map(str, row))))


def s4_ric():
    a = R.choice([1, 2, 3, 4, 5])
    b = R.choice([1, 2, 3, 4, 5, 6, 7])
    v = R.choice(["x", "a", "y"])
    s = R.choice([1, -1])
    k = R.choice(["q", "d"])
    if k == "q":
        p = P([(a * a, {v: 2}), (s * 2 * a * b, {v: 1}), (b * b, {})])
        ans = "(%s)²" % show(P([(a, {v: 1}), (s * b, {})]))
        w = ["(%s)²" % show(P([(a, {v: 1}), (-s * b, {})])), "(%s)²" % show(P([(a * a, {v: 1}), (s * b, {})])) if a > 1 else "(%s)²" % show(P([(a, {v: 1}), (s * 2 * b, {})])),
             "(%s)(%s)" % (show(P([(a, {v: 1}), (b, {})])), show(P([(a, {v: 1}), (-b, {})])))]
        e = "Ci sono due quadrati (%s e %d) e il doppio prodotto %s: è <b>%s</b>." % (show(P([(a * a, {v: 2})])), b * b, show(P([(s * 2 * a * b, {v: 1})])), ans)
    else:
        p = P([(a * a, {v: 2}), (-b * b, {})])
        ans = "(%s)(%s)" % (show(P([(a, {v: 1}), (b, {})])), show(P([(a, {v: 1}), (-b, {})])))
        w = ["(%s)²" % show(P([(a, {v: 1}), (-b, {})])), "(%s)²" % show(P([(a, {v: 1}), (b, {})])), "(%s)(%s)" % (show(P([(a, {v: 1}), (b * b, {})])), show(P([(a, {v: 1}), (-b * b, {})]))), "(%s)(%s)" % (show(P([(a * a, {v: 1}), (b, {})])), show(P([(a * a, {v: 1}), (-b, {})]))) if a > 1 else "(%s)(%s)" % (show(P([(1, {v: 1}), (2 * b, {})])), show(P([(1, {v: 1}), (-2 * b, {})])))]
        e = "Differenza di due quadrati: A² − B² = (A + B)(A − B): <b>%s</b>." % ans
    return M("Quale prodotto notevole dà %s?" % show(p), ans, w, e)


def s5_mente():
    k = R.choice(["spd", "q+", "q-"])
    if k == "spd":
        b = R.choice([20, 30, 40, 50, 60, 70, 80, 100])
        a = R.randint(1, 4)
        v = b * b - a * a
        q = "%d · %d" % (b + a, b - a)
        e = "(%d + %d)(%d − %d) = %d² − %d² = %s − %d = <b>%s</b>." % (b, a, b, a, b, a, d(b * b), a * a, d(v))
        w = [b * b, b * b + a * a, b * b - 2 * a, b * b - a]
    else:
        b = R.choice([20, 30, 40, 50, 60, 70, 100])
        a = R.randint(1, 3)
        n = b + a if k == "q+" else b - a
        v = n * n
        q = "%d²" % n
        e = "(%d %s %d)² = %s %s %d + %d = <b>%s</b>." % (b, "+" if k == "q+" else "−", a, d(b * b), "+" if k == "q+" else "−", 2 * a * b, a * a, d(v))
        w = [b * b + a * a, b * b + (2 * a * b if k == "q+" else -2 * a * b), b * b - a * a if k == "q-" else b * b + a * b]
    return M("Calcola a mente con un prodotto notevole: %s" % q, d(v), [d(x) for x in w if x != v], e)


def s5_espr():
    t1, t2 = pair()
    p, q = bino(t1, t2, 1), bino(t1, t2, -1)
    r = add(pw(p, 2), pw(q, 2), -1)
    w = [show(add(pw(p, 2), pw(q, 2))), "0", show(mul(P([(2, {})]), mul(P([t1]), P([t2]))))]
    return M("Semplifica: (%s)<sup>2</sup> − (%s)<sup>2</sup>" % (show(p), show(q)), show(r), W(*[x for x in w if x != show(r)]),
             "Restano solo i doppi prodotti: 2AB − (−2AB) = 4AB = <b>%s</b>." % show(r))


def main():
    seen = set()
    sets = [
        ("Quadrato di un binomio", mix(R, seen, [(s1_quad, 20)])),
        ("Somma per differenza", mix(R, seen, [(s1_spd, 14), (s1_quad, 6)])),
        ("Cubo di un binomio e quadrato di un trinomio", mix(R, seen, [(s2_cubo, 10), (s2_trin, 10)])),
        ("Triangolo di Tartaglia e riconoscere", mix(R, seen, [(s3_tart, 10), (s4_ric, 10)])),
        ("Calcolo mentale ed espressioni", mix(R, seen, [(s5_mente, 10), (s5_espr, 5), (s4_ric, 5)])),
    ]
    body = L(["Alcuni prodotti si sviluppano subito con una regola. <b>Quadrato di un binomio</b>: (A + B)² = A² + 2AB + B², (A − B)² = A² − 2AB + B².",
              "<b>Somma per differenza</b>: (A + B)(A − B) = A² − B². <b>Cubo di un binomio</b>: (A + B)³ = A³ + 3A²B + 3AB² + B³.",
              "<b>Quadrato di un trinomio</b>: (A + B + C)² = A² + B² + C² + 2AB + 2AC + 2BC.",
              "I coefficienti di (A + B)<sup>n</sup> si leggono nella riga n del <b>triangolo di Tartaglia</b>: 1; 1 1; 1 2 1; 1 3 3 1; 1 4 6 4 1 …"],
             [("Sviluppa (3x − 2)².", ["A = 3x, B = 2: 9x² − 2 · 3x · 2 + 4."], "9x² − 12x + 4"),
              ("Calcola 52 · 48.", ["(50 + 2)(50 − 2) = 2500 − 4."], "2496")],
             [["(a + b)² = a² + b²", "Manca il doppio prodotto: a² + 2ab + b²."],
              ["(3x)² = 3x²", "Si eleva anche il coefficiente: 9x²."],
              ["(a − b)² = a² − 2ab − b²", "B² è un quadrato: è sempre positivo, a² − 2ab + b²."],
              ["(a − 2)³ = a³ − 8", "Servono i quattro termini: a³ − 6a² + 12a − 8."]],
             table(["Prodotto", "Sviluppo"], [["(A + B)²", "A² + 2AB + B²"], ["(A + B)(A − B)", "A² − B²"], ["(A + B)³", "A³ + 3A²B + 3AB² + B³"], ["(A + B + C)²", "A² + B² + C² + 2AB + 2AC + 2BC"]]))
    faq = [("Perché si chiamano prodotti notevoli?", "Perché compaiono spesso e hanno uno sviluppo fisso: imparando la regola si evita di moltiplicare termine per termine. Le stesse regole, lette al contrario, servono per scomporre."),
           ("Come si costruisce il triangolo di Tartaglia?", "Ogni riga comincia e finisce con 1; ogni altro numero è la somma dei due numeri che gli stanno sopra. La riga n contiene i coefficienti di (A + B)<sup>n</sup>.")]
    unit(G, R, "prodotti-notevoli", "A",
         "Calcolo con i polinomi: prodotti notevoli, potenza di un binomio e triangolo di Tartaglia",
         "Prodotti notevoli", "Prodotti notevoli",
         "Schede di matematica per la prima liceo sui prodotti notevoli: quadrato di un binomio, somma per differenza, cubo di un binomio, quadrato di un trinomio, triangolo di Tartaglia, calcolo mentale. 100 esercizi con soluzioni.",
         "(A + B)² = A² + 2AB + B²", "Non dimenticare il doppio prodotto; (A + B)(A − B) = A² − B².",
         body, faq, sets, 4)


if __name__ == "__main__":
    main()
