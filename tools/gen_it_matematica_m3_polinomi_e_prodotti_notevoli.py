# -*- coding: utf-8 -*-
"""
Italia Matematica terza media: Polinomi e prodotti notevoli (Relazioni e funzioni)
  python3 tools/gen_it_matematica_m3_polinomi_e_prodotti_notevoli.py
Polinomi: grado, termine noto, polinomi ordinati; somma e differenza; prodotto monomio × polinomio e polinomio × polinomio;
prodotti notevoli: quadrato di un binomio, somma per differenza, cubo di un binomio; raccoglimento a fattor comune.
Errori: (a + b)² = a² + b², sbagliare il segno togliendo la parentesi preceduta da −, dimenticare il doppio prodotto.
"""
import random
from it_media import M, L, unit, mix, table, W, sgn, Kids
from it_m3 import P, show, mul, add, mono

R = random.Random(71304)
G = "terza-media"
K = Kids(R)


def nz(lo=-9, hi=9):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def px(*cs):
    """coefficienti dal grado più alto: px(2, −3, 1) = 2x² − 3x + 1"""
    n = len(cs) - 1
    return P([(c, {"x": n - i}) for i, c in enumerate(cs)])


def par(p):
    return "(%s)" % show(p)


def s1_grado():
    cs = [nz(-7, 7)] + [R.randint(-7, 7) for _ in range(R.randint(2, 3))]
    p = px(*cs)
    n = len(cs) - 1
    k = R.choice(["grado", "noto", "coef"])
    if k == "grado":
        return M("Qual è il grado del polinomio %s?" % show(p), str(n), W(str(n + 1), str(len(p)), str(sum(range(n + 1))) if sum(range(n + 1)) != n else str(n - 1), str(n - 1), str(n + 2)), "Il grado è il grado massimo dei suoi termini: <b>%d</b>." % n)
    if k == "noto":
        c0 = cs[-1]
        return M("Qual è il termine noto del polinomio %s?" % show(p), sgn(c0) if c0 else "0", W(sgn(cs[0]), sgn(-c0) if c0 else "+1", str(n), sgn(cs[-2]) if cs[-2] and cs[-2] != c0 else "+1"), "Il termine noto è il termine senza lettere: <b>%s</b>." % (sgn(c0) if c0 else "0 (manca)"))
    c1 = cs[-2]
    return M("Qual è il coefficiente di x nel polinomio %s?" % show(p), sgn(c1) if c1 else "0", W(sgn(cs[0]), sgn(cs[-1]) if cs[-1] else "+1", sgn(-c1) if c1 else "+1", "1", sgn(cs[1]) if cs[1] else "+2", sgn(2 * c1) if c1 else "+2"), "Il termine in x è %s: coefficiente <b>%s</b>." % (show(P([(c1, {"x": 1})])) if c1 else "assente", sgn(c1) if c1 else "0"))


def s2_somma():
    p = px(nz(-6, 6), R.randint(-9, 9), R.randint(-9, 9))
    q = px(nz(-6, 6), R.randint(-9, 9), R.randint(-9, 9))
    op = R.choice(["+", "−"])
    r = add(p, q, 1 if op == "+" else -1)
    if len(r) < 2:
        return None
    wrong = add(p, q, -1 if op == "+" else 1)
    w2 = {k: (c if dict(k).get("x", 0) == 2 else c) for k, c in r.items()}
    w3 = dict(r)
    if op == "−":
        # errore: cambiare segno solo al primo termine di q
        k2 = sorted(q, key=lambda k: -sum(e for _, e in k))[0]
        w3 = add(p, {kk: (-c if kk == k2 else c) for kk, c in q.items()})
    else:
        w3 = add(p, {kk: -c for kk, c in q.items() if dict(kk).get("x", 0) == 0}) if any(dict(kk).get("x", 0) == 0 for kk in q) else add(r, px(1, 0, 0))
    return M("Calcola: %s %s %s" % (par(p), op, par(q)), show(r), W(show(wrong), show(w3) if w3 != r else None, show(add(r, px(0, 1, 0))) if show(add(r, px(0, 1, 0))) != show(r) else None, show(add(r, px(0, 0, 2)))),
             ("Si sommano i termini simili: <b>%s</b>." % show(r)) if op == "+" else "Si toglie la parentesi preceduta da − cambiando il segno a <b>tutti</b> i termini: <b>%s</b>." % show(r))


def s3_prodotto():
    k = R.choice(["mono", "poli"])
    if k == "mono":
        m = P([(nz(-5, 5), {"x": R.randint(1, 2)})])
        q = px(nz(-6, 6), R.randint(-9, 9), nz(-9, 9))
        r = mul(m, q)
        k0 = list(q)
        wrong = add(mul(m, P([(c, dict(kk)) for kk, c in q.items() if dict(kk).get("x", 0) == 2])), {kk: c for kk, c in q.items() if dict(kk).get("x", 0) < 2})
        return M("Calcola: %s · %s" % (show(m), par(q)), show(r), W(show(wrong), show(mul(P([(-c, dict(kk)) for kk, c in m.items()]), q)), show(add(r, px(0, 0, 1, 0)))),
                 "Si moltiplica %s per ogni termine del polinomio: <b>%s</b>." % (show(m), show(r)))
    a, b, c, dd = nz(-5, 5), nz(-9, 9), nz(-5, 5), nz(-9, 9)
    if abs(a) > 3 or abs(c) > 3:
        return None
    p, q = px(a, b), px(c, dd)
    r = mul(p, q)
    wrong = px(a * c, b * dd)
    w2 = px(a * c, a * dd - b * c, b * dd)
    w3 = px(a * c, a * dd + b * c, -b * dd)
    return M("Calcola: %s%s" % (par(p), par(q)), show(r), W(show(wrong), show(w2) if w2 != r else None, show(w3) if w3 != r else None, show(add(r, px(0, 1, 0)))),
             "Ogni termine del primo per ogni termine del secondo: %s · %s, %s · %s, %s · %s, %s · %s; poi si riducono i simili: <b>%s</b>." % (
                 show(px(a, 0)), show(px(c, 0)), show(px(a, 0)), sgn(dd), sgn(b), show(px(c, 0)), sgn(b), sgn(dd), show(r)))


def bin_(a, b, va="x", vb=None):
    """a·va + b (vb: seconda lettera)"""
    if vb:
        return P([(a, {va: 1}), (b, {vb: 1})])
    return P([(a, {va: 1}), (b, {})])


def s4_quadrato():
    a = R.choice([1, 1, 2, 3, 4, 5])
    b = nz(-9, 9)
    vb = R.choice([None, None, "y"])
    p = bin_(a, b, "x", vb)
    r = mul(p, p)
    wrong = add(mul(P([(a, {"x": 1})]), P([(a, {"x": 1})])), P([(b * b, {vb: 2} if vb else {})]))
    w2 = add(wrong, P([(a * b, {"x": 1, vb: 1} if vb else {"x": 1})]))
    w3 = add(wrong, P([(-2 * a * b, {"x": 1, vb: 1} if vb else {"x": 1})]))
    first = show(P([(a, {"x": 1})]))
    second = show(P([(abs(b), {vb: 1} if vb else {})]))
    return M("Sviluppa il quadrato del binomio: %s²" % par(p), show(r), W(show(wrong), show(w2), show(w3)),
             "(A %s B)² = A² %s 2AB + B² con A = %s e B = %s: <b>%s</b>." % ("+" if b > 0 else "−", "+" if b > 0 else "−", first, second, show(r)))


def s4_sxd():
    a = R.choice([1, 1, 2, 3, 5])
    b = R.randint(1, 9)
    vb = R.choice([None, None, "y"])
    p, q = bin_(a, b, "x", vb), bin_(a, -b, "x", vb)
    r = mul(p, q)
    ax2 = P([(a * a, {"x": 2})])
    b2 = P([(b * b, {vb: 2} if vb else {})])
    return M("Calcola con la somma per differenza: %s%s" % (par(p), par(q)), show(r), W(show(add(ax2, b2)), show(add(add(ax2, b2, -1), P([(-2 * a * b, {"x": 1, vb: 1} if vb else {"x": 1})]))), show(add(P([(a, {"x": 2})]), b2, -1)) if a != 1 else show(add(ax2, P([(b, {vb: 2} if vb else {})]), -1)) if b != 1 else None, show(add(b2, ax2, -1))),
             "(A + B)(A − B) = A² − B²: <b>%s</b>." % show(r))


def s4_cubo():
    b = nz(-4, 4)
    p = bin_(1, b)
    r = mul(mul(p, p), p)
    return M("Sviluppa il cubo del binomio: %s³" % par(p), show(r), W(show(px(1, 0, 0, b ** 3)), show(px(1, 3 * b, 3 * b, b ** 3)) if b != 1 else show(px(1, 3, 3, 3)), show(px(1, 3 * b, 3 * b * b, b ** 3 * -1)), show(px(1, b, b * b, b ** 3))),
             "(A + B)³ = A³ + 3A²B + 3AB² + B³ con A = x e B = %s: <b>%s</b>." % (sgn(b), show(r)))


def s5_racc():
    k = nz(-6, 6)
    if abs(k) == 1:
        return None
    e = R.randint(0, 2)
    inner = px(nz(-5, 5), R.randint(-7, 7), nz(-7, 7))
    m = P([(k, {"x": e})])
    full = mul(m, inner)
    ans = "%s%s" % (show(m) if show(m) not in ("1",) else "", par(inner))
    wrong_inner = add(inner, px(0, 0, 1))
    return M("Raccogli a fattor comune: %s" % show(full), ans, W("%s%s" % (show(m), par(wrong_inner)), "%s%s" % (show(P([(k, {"x": e + 1})])), par(inner)) if e < 2 and dict(list(inner)[0]).get("x", 0) >= 1 else None, "%s%s" % (show(P([(-k, {"x": e})])), par(inner)), "%s%s" % (show(P([(k * 2, {"x": e})])), par(inner))),
             "Il fattore comune è %s; dividendo ogni termine per %s si ottiene %s. <b>%s</b>." % (show(m), show(m), show(inner), ans))


def main():
    seen = set()
    sets = [
        ("Polinomi: grado e termini", mix(R, seen, [(s1_grado, 20)])),
        ("Somma e differenza di polinomi", mix(R, seen, [(s2_somma, 20)])),
        ("Prodotto di polinomi", mix(R, seen, [(s3_prodotto, 20)])),
        ("Prodotti notevoli", mix(R, seen, [(s4_quadrato, 9), (s4_sxd, 8), (s4_cubo, 3)])),
        ("Prodotti notevoli e raccoglimento", mix(R, seen, [(s4_quadrato, 6), (s4_sxd, 4), (s5_racc, 10)])),
    ]
    body = L(["Un <b>polinomio</b> è una somma algebrica di monomi non simili: 3x² − 5x + 2. Il <b>grado</b> è il grado più alto dei suoi termini; il <b>termine noto</b> è quello senza lettere.",
              "Per <b>sommare</b> polinomi si riducono i termini simili. Una parentesi preceduta da − si toglie cambiando il segno a tutti i termini.",
              "Per <b>moltiplicare</b> si moltiplica ogni termine del primo per ogni termine del secondo, poi si riducono i simili.",
              "<b>Prodotti notevoli</b>: (A + B)² = A² + 2AB + B²; (A + B)(A − B) = A² − B²; (A + B)³ = A³ + 3A²B + 3AB² + B³."],
             [("(x + 3)²", ["x² + 2 · x · 3 + 3²"], "x² + 6x + 9"), ("(2x + 5)(2x − 5)", ["(2x)² − 5²"], "4x² − 25")],
             [["(a + b)² = a² + b²", "Manca il doppio prodotto 2ab."],
              ["−(x − 3) = −x − 3", "Si cambia il segno a tutti i termini: −x + 3."],
              ["(x − 4)² = x² − 8x − 16", "B² è sempre positivo: + 16."]],
             table(["Prodotto notevole", "Sviluppo"], [["(A + B)²", "A² + 2AB + B²"], ["(A − B)²", "A² − 2AB + B²"], ["(A + B)(A − B)", "A² − B²"], ["(A + B)³", "A³ + 3A²B + 3AB² + B³"]]))
    faq = [("Perché si chiamano prodotti notevoli?", "Perché sono prodotti che compaiono spesso e hanno uno sviluppo che si può scrivere subito, senza fare tutte le moltiplicazioni."),
           ("Come si verifica un raccoglimento?", "Si moltiplica il fattore raccolto per la parentesi: si deve ottenere il polinomio di partenza.")]
    unit(G, R, "polinomi-e-prodotti-notevoli", "F",
         "Interpretare, costruire e trasformare formule che contengono lettere; operare con i polinomi e utilizzare i prodotti notevoli",
         "Polinomi e prodotti notevoli", "Polinomi",
         "Schede di matematica per la terza media sui polinomi: grado, somma e differenza, prodotto, quadrato di un binomio, somma per differenza, cubo di un binomio e raccoglimento a fattor comune. 100 esercizi con soluzioni.",
         "(A + B)² = A² + 2AB + B²", "(A + B)(A − B) = A² − B²",
         body, faq, sets, 4)


if __name__ == "__main__":
    main()
