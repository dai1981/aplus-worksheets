# -*- coding: utf-8 -*-
"""
Italia Matematica seconda liceo: Sistemi lineari (Aritmetica e algebra)
  python3 tools/gen_it_matematica_l2_sistemi_lineari.py
Sistemi di due equazioni in due incognite: verifica, sostituzione, riduzione, regola di Cramer (determinanti),
sistemi determinati, impossibili e indeterminati, interpretazione grafica, sistemi di tre equazioni, problemi.
Errori: sostituire solo in parte, sbagliare il segno nella riduzione, D = ab′ + a′b, scambiare x e y nella soluzione.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, P, show

R = random.Random(72203)
G = "seconda-liceo"


def eq(a, b, c):
    return "%s = %s" % (show(P([(a, {"x": 1}), (b, {"y": 1})])), fq(c))


def sys2(e1, e2):
    return "<span class='sys'>%s<br>%s</span>" % (e1, e2)


def pr(x, y):
    return "(%s; %s)" % (fq(x), fq(y))


def gen():
    while True:
        x, y = R.randint(-6, 6), R.randint(-6, 6)
        a, b, a2, b2 = nz(R, -5, 5), nz(R, -5, 5), nz(R, -5, 5), nz(R, -5, 5)
        if a * b2 - a2 * b != 0 and (x, y) != (0, 0):
            return x, y, a, b, a * x + b * y, a2, b2, a2 * x + b2 * y


def s1_ver():
    x, y, a, b, c, a2, b2, c2 = gen()
    good = R.random() < 0.5
    cx, cy = (x, y) if good else R.choice([(y, x), (x, -y), (-x, y), (x + 1, y)])
    if (cx, cy) == (x, y) and not good:
        return None
    ok = a * cx + b * cy == c and a2 * cx + b2 * cy == c2
    ans = "sì" if ok else "no"
    return M("La coppia %s è soluzione del sistema %s?" % (pr(cx, cy), sys2(eq(a, b, c), eq(a2, b2, c2))), ans, ["no" if ok else "sì", "solo della prima equazione", "solo della seconda equazione"] if ok else ["sì", "sì, perché verifica una delle due equazioni", "non si può stabilire"],
             "Sostituisco x = %s e y = %s in <b>entrambe</b> le equazioni: %s." % (fq(cx), fq(cy), "sono verificate, <b>sì</b>" if ok else "almeno una non è verificata, <b>no</b>"))


def s1_sost():
    x, y = R.randint(-6, 6), R.randint(-6, 6)
    m, q = nz(R, -4, 4), R.randint(-6, 6)
    # y = m x + q  e  a x + b y = c
    y = m * x + q
    a, b = nz(R, -5, 5), nz(R, -5, 5)
    if a + b * m == 0:
        return None
    c = a * x + b * y
    e1 = "y = %s" % show(P([(m, {"x": 1}), (q, {})]))
    ans = pr(x, y)
    w = [pr(y, x), pr(x, m * x - q), pr(-x, -y) if (x, y) != (0, 0) else pr(1, 1), pr(Fr(c, a + b * m), y)]
    return M("Risolvi con il metodo di sostituzione: %s" % sys2(e1, eq(a, b, c)), ans, [t for t in w if t != ans],
             "Sostituisco y nella seconda: %s → x = %s, poi y = %s: <b>%s</b>." % ("%s = %s" % (show(P([(a + b * m, {"x": 1})])), fq(c - b * q)), fq(x), fq(y), ans))


def s2_rid():
    x, y = R.randint(-6, 6), R.randint(-6, 6)
    a, b = nz(R, -5, 5), nz(R, -5, 5)
    b2 = R.choice([-b, b])
    a2 = nz(R, -5, 5)
    if a * b2 - a2 * b == 0:
        return None
    c, c2 = a * x + b * y, a2 * x + b2 * y
    ans = pr(x, y)
    op = "sommo" if b2 == -b else "sottraggo"
    w = [pr(y, x), pr(Fr(c - c2, a + a2) if a + a2 else x + 1, y), pr(-x, y) if x else pr(1, y), pr(x, -y) if y else pr(x, 1)]
    return M("Risolvi con il metodo di riduzione: %s" % sys2(eq(a, b, c), eq(a2, b2, c2)), ans, [t for t in w if t != ans],
             "I coefficienti di y sono %s: %s le equazioni e la y sparisce: %s → x = %s; poi y = %s: <b>%s</b>." % ("opposti" if b2 == -b else "uguali", op, "%s = %s" % (show(P([((a + a2) if b2 == -b else (a - a2), {"x": 1})])), fq(c + c2 if b2 == -b else c - c2)), fq(x), fq(y), ans))


def det(a, b, c, d_):
    return a * d_ - b * c


def s3_cramer():
    x, y, a, b, c, a2, b2, c2 = gen()
    D = det(a, b, a2, b2)
    k = R.choice(["D", "Dx", "sol"])
    if k == "D":
        return M("Nel sistema %s calcola il determinante D dei coefficienti." % sys2(eq(a, b, c), eq(a2, b2, c2)), fq(D), [fq(v) for v in (a * b2 + a2 * b, a2 * b - a * b2, a * a2 - b * b2) if v != D],
                 "D = a · b′ − b · a′ = %s · %s − %s · %s = <b>%s</b>." % (fq(a), "(%s)" % fq(b2) if b2 < 0 else fq(b2), fq(b), "(%s)" % fq(a2) if a2 < 0 else fq(a2), fq(D)))
    if k == "Dx":
        Dx = det(c, b, c2, b2)
        return M("Nel sistema %s calcola D<sub>x</sub> (colonna di x sostituita dai termini noti)." % sys2(eq(a, b, c), eq(a2, b2, c2)), fq(Dx), [fq(v) for v in (det(a, c, a2, c2), c * b2 + c2 * b, D) if v != Dx],
                 "D<sub>x</sub> = c · b′ − b · c′ = <b>%s</b>; poi x = D<sub>x</sub>/D = %s." % (fq(Dx), fq(Fr(Dx, D))))
    ans = pr(x, y)
    return M("Risolvi con la regola di Cramer: %s" % sys2(eq(a, b, c), eq(a2, b2, c2)), ans, [t for t in (pr(y, x), pr(Fr(det(c, b, c2, b2), -D), Fr(det(a, c, a2, c2), -D)), pr(-x, -y) if (x, y) != (0, 0) else pr(1, 1), pr(x, -y), pr(-x, y), pr(x + 1, y)) if t != ans],
             "D = %s, D<sub>x</sub> = %s, D<sub>y</sub> = %s: x = D<sub>x</sub>/D, y = D<sub>y</sub>/D, quindi <b>%s</b>." % (fq(D), fq(det(c, b, c2, b2)), fq(det(a, c, a2, c2)), ans))


def s3_tipo():
    a, b = nz(R, -5, 5), nz(R, -5, 5)
    k = R.choice([2, 3, -2, -1])
    c = R.randint(-9, 9)
    t = R.choice(["det", "imp", "ind"])
    if t == "det":
        a2, b2 = nz(R, -5, 5), nz(R, -5, 5)
        if a * b2 == a2 * b:
            return None
        c2 = R.randint(-9, 9)
        ans, e = "determinato (una soluzione)", "a/a′ ≠ b/b′ (D ≠ 0): le rette sono incidenti, <b>determinato</b>."
    elif t == "imp":
        a2, b2, c2 = k * a, k * b, k * c + nz(R, -4, 4)
        ans, e = "impossibile (nessuna soluzione)", "a/a′ = b/b′ ≠ c/c′: le rette sono parallele distinte, <b>impossibile</b>."
    else:
        a2, b2, c2 = k * a, k * b, k * c
        ans, e = "indeterminato (infinite soluzioni)", "a/a′ = b/b′ = c/c′: le equazioni sono equivalenti, le rette coincidono, <b>indeterminato</b>."
    return M("Il sistema %s è…" % sys2(eq(a, b, c), eq(a2, b2, c2)), ans, [o for o in ["determinato (una soluzione)", "impossibile (nessuna soluzione)", "indeterminato (infinite soluzioni)", "determinato con soluzione (0; 0)"] if o != ans], e)


def s4_tre():
    x, y, z = R.randint(-4, 5), R.randint(-4, 5), R.randint(-4, 5)
    a = nz(R, -3, 3)
    b = nz(R, -3, 3)
    e1 = "x + y + z = %s" % fq(x + y + z)
    e2 = "%s = %s" % (show(P([(1, {"y": 1}), (a, {"z": 1})])), fq(y + a * z))
    e3 = "%s = %s" % (show(P([(b, {"z": 1})])), fq(b * z))
    ans = "(%s; %s; %s)" % (fq(x), fq(y), fq(z))
    w = ["(%s; %s; %s)" % (fq(z), fq(y), fq(x)), "(%s; %s; %s)" % (fq(x + y + z - (y + a * z) - z), fq(y + a * z), fq(z)) if a != 1 else "(%s; %s; %s)" % (fq(x + 1), fq(y), fq(z)), "(%s; %s; %s)" % (fq(-x), fq(y), fq(z)) if x else "(1; %s; %s)" % (fq(y), fq(z)), "(%s; %s; %s)" % (fq(x), fq(-y), fq(z)) if y else "(%s; 1; %s)" % (fq(x), fq(z)), "(%s; %s; %s)" % (fq(x + 2), fq(y), fq(z))]
    return M("Risolvi il sistema: <span class='sys'>%s<br>%s<br>%s</span>" % (e1, e2, e3), ans, [t for t in w if t != ans],
             "Dalla terza z = %s, dalla seconda y = %s, dalla prima x = %s: <b>%s</b>." % (fq(z), fq(y), fq(x), ans))


def s5_probl():
    k = R.choice(["biglietti", "monete", "eta", "cifre", "spesa"])
    if k == "biglietti":
        pi, pr_ = R.choice([(8, 5), (10, 6), (12, 7), (9, 4)])
        a, b = R.randint(10, 60), R.randint(10, 60)
        q = "A uno spettacolo sono stati venduti %d biglietti, interi a %d € e ridotti a %d €, per un incasso di %d €. Quanti biglietti interi?" % (a + b, pi, pr_, a * pi + b * pr_)
        e = "x + y = %d e %dx + %dy = %d: <b>x = %d</b> interi (y = %d ridotti)." % (a + b, pi, pr_, a * pi + b * pr_, a, b)
        return M(q, str(a), W(b, (a + b) // 2, a + 1, a - 1), e)
    if k == "monete":
        a, b = R.randint(3, 20), R.randint(3, 20)
        q = "In un salvadanaio ci sono %d monete da 1 € e da 2 €, per un totale di %d €. Quante sono le monete da 2 €?" % (a + b, a + 2 * b)
        e = "x + y = %d e x + 2y = %d: sottraendo, <b>y = %d</b>." % (a + b, a + 2 * b, b)
        return M(q, str(b), W(a, (a + 2 * b) // 2, b + 1), e)
    if k == "eta":
        f = R.randint(5, 15)
        m = R.randint(28, 45)
        t = R.randint(2, 8)
        if (m + t) % (f + t) != 0:
            return None
        r = (m + t) // (f + t)
        q = "La somma delle età di una madre e di una figlia è %d anni. Tra %d anni la madre avrà %s dell’età della figlia. Quanti anni ha la figlia?" % (m + f, t, {2: "il doppio", 3: "il triplo", 4: "il quadruplo", 5: "il quintuplo"}.get(r, "%d volte" % r))
        if r not in (2, 3, 4, 5):
            return None
        e = "x + y = %d e y + %d = %d(x + %d): <b>x = %d</b>." % (m + f, t, r, t, f)
        return M(q, "%d anni" % f, ["%d anni" % v for v in (m, (m + f) // (r + 1), f + t)], e)
    if k == "cifre":
        a, b = R.randint(1, 9), R.randint(0, 9)
        if a == b or b == 0:
            return None
        n = 10 * a + b
        q = "In un numero di due cifre la somma delle cifre è %d. Scambiando le cifre il numero %s di %d. Qual è il numero?" % (a + b, "aumenta" if b > a else "diminuisce", abs(9 * (b - a)))
        e = "Decine x, unità y: x + y = %d e (10y + x) − (10x + y) = %s → y − x = %s: <b>%d</b>." % (a + b, fq(9 * (b - a)), fq(b - a), n)
        return M(q, str(n), [str(10 * b + a), str(n + 9) if (n + 9) % 10 != 0 else str(n - 9), str(10 * a + b + 1)], e)
    pa, pb = R.choice([(2, 3), (3, 5), (4, 7), (6, 5)])
    a, b = R.randint(2, 8), R.randint(2, 8)
    a2, b2 = R.randint(1, 8), R.randint(1, 8)
    if a * b2 == a2 * b:
        return None
    q = "Giulia compra %d quaderni e %d penne e spende %d €; Marco compra %d quaderni e %d penne e spende %d €. Quanto costa un quaderno?" % (a, b, a * pa + b * pb, a2, b2, a2 * pa + b2 * pb)
    e = "%dx + %dy = %d e %dx + %dy = %d: <b>x = %d €</b> (una penna costa %d €)." % (a, b, a * pa + b * pb, a2, b2, a2 * pa + b2 * pb, pa, pb)
    return M(q, "%d €" % pa, ["%d €" % v for v in (pb, pa + 1, (a * pa + b * pb) // (a + b) if (a * pa + b * pb) // (a + b) not in (pa, pb) else pa + 2)], e)


def main():
    seen = set()
    sets = [
        ("Verifica e sostituzione", mix(R, seen, [(s1_ver, 6), (s1_sost, 14)])),
        ("Riduzione", mix(R, seen, [(s2_rid, 20)])),
        ("Regola di Cramer", mix(R, seen, [(s3_cramer, 20)])),
        ("Tipi di sistemi e tre equazioni", mix(R, seen, [(s3_tipo, 12), (s4_tre, 8)])),
        ("Problemi con i sistemi", mix(R, seen, [(s5_probl, 20)])),
    ]
    body = L(["Un <b>sistema</b> di due equazioni lineari in x e y cerca le coppie (x; y) che verificano <b>entrambe</b> le equazioni. Graficamente è l’intersezione di due rette.",
              "<b>Sostituzione</b>: ricavo un’incognita da un’equazione e la sostituisco nell’altra. <b>Riduzione</b>: sommo o sottraggo le equazioni (moltiplicate per numeri opportuni) per eliminare un’incognita.",
              "<b>Cramer</b>: D = ab′ − a′b, D<sub>x</sub> = cb′ − c′b, D<sub>y</sub> = ac′ − a′c. Se D ≠ 0: x = D<sub>x</sub>/D, y = D<sub>y</sub>/D.",
              "Se D = 0 il sistema è <b>impossibile</b> (rette parallele) o <b>indeterminato</b> (rette coincidenti)."],
             [("x + y = 5 e x − y = 1", ["Sommo: 2x = 6, x = 3", "y = 5 − 3 = 2"], "(3; 2)"),
              ("2x + 3y = 7 e 4x + 6y = 1", ["a/a′ = b/b′ = 1/2, ma c/c′ = 7"], "impossibile")],
             [["Scrivere la soluzione (y; x)", "La coppia si scrive sempre (x; y)."],
              ["D = ab′ + a′b", "Il determinante è una differenza: ab′ − a′b."],
              ["Verificare una sola equazione", "La soluzione deve verificare tutte le equazioni del sistema."]])
    faq = [("Quale metodo conviene usare?", "La sostituzione quando un’incognita ha coefficiente 1 o −1; la riduzione quando i coefficienti di un’incognita sono uguali o opposti; Cramer quando i numeri sono comodi o per discutere i casi."),
           ("Che cosa vuol dire un sistema indeterminato?", "Che le due equazioni sono equivalenti (una è multipla dell’altra): le rette coincidono e ogni punto della retta è una soluzione.")]
    unit(G, R, "sistemi-lineari", "A",
         "Sistemi di equazioni lineari: metodi di sostituzione, riduzione, Cramer; interpretazione grafica; problemi",
         "Sistemi lineari", "Sistemi lineari",
         "Schede di matematica per la seconda liceo sui sistemi lineari: verifica, metodo di sostituzione e di riduzione, regola di Cramer, sistemi determinati, impossibili e indeterminati, sistemi di tre equazioni, problemi. 100 esercizi con soluzioni.",
         "D = ab′ − a′b", "Se D ≠ 0 il sistema ha una sola soluzione: x = Dₓ/D, y = D_y/D.",
         body, faq, sets, 3)


if __name__ == "__main__":
    main()
