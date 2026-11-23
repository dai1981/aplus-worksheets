# -*- coding: utf-8 -*-
"""
Italia Matematica terza liceo: L’ellisse (Geometria)
  python3 tools/gen_it_matematica_l3_ellisse.py
Ellisse con centro nell’origine e assi sugli assi cartesiani: equazione x²/a² + y²/b² = 1, forma 4x² + 9y² = 36,
semiassi e vertici, fuochi (c² = a² − b², sull’asse x o sull’asse y), eccentricità, equazione dati semiassi o fuochi,
appartenenza di un punto, posizione di una retta.
Errori: c² = a² + b², semiassi a² e b² invece di a e b, fuochi sull’asse sbagliato.
"""
import math
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, FR, simp_root, P2

R = random.Random(72307)
G = "terza-liceo"


def rt(n):
    k, m = simp_root(int(n))
    return str(k) if m == 1 else ("" if k == 1 else str(k)) + "√" + str(m)


def ell(a2, b2):
    return "%s + %s = 1" % ((FR("x²", str(a2)) if a2 != 1 else "x²"), (FR("y²", str(b2)) if b2 != 1 else "y²"))


def s1_semi():
    a, b = R.sample(range(2, 9), 2)
    t = R.choice(["vert", "semi"])
    if t == "semi":
        return M("Quanto misurano i semiassi dell’ellisse %s?" % ell(a * a, b * b), "%d e %d" % (a, b), ["%d e %d" % (a * a, b * b), "%d e %d" % (2 * a, 2 * b), "%s e %s" % (rt(a), rt(b))],
                 "a² = %d e b² = %d: i semiassi sono <b>%d e %d</b> (gli assi misurano %d e %d)." % (a * a, b * b, a, b, 2 * a, 2 * b))
    ans = "(±%d; 0) e (0; ±%d)" % (a, b)
    return M("Quali sono i vertici dell’ellisse %s?" % ell(a * a, b * b), ans, ["(±%d; 0) e (0; ±%d)" % (b, a), "(±%d; 0) e (0; ±%d)" % (a * a, b * b), "(±%d; 0) e (0; ±%d)" % (a + b, abs(a - b))],
             "Intersezioni con gli assi: y = 0 → x = ±%d; x = 0 → y = ±%d: <b>%s</b>." % (a, b, ans))


def trip():
    return R.choice([(5, 4, 3), (5, 3, 4), (10, 6, 8), (10, 8, 6), (13, 12, 5), (13, 5, 12), (3, 2, None), (4, 2, None), (6, 4, None), (5, 2, None), (3, 1, None), (7, 3, None)])


def s2_fuochi():
    a, b, c = trip()
    c2 = a * a - b * b
    cc = rt(c2)
    sw = R.random() < 0.4
    if not sw:
        q = ell(a * a, b * b)
        ans = "(±%s; 0)" % cc
        w = ["(0; ±%s)" % cc, "(±%s; 0)" % rt(a * a + b * b), "(±%d; 0)" % c2]
    else:
        q = ell(b * b, a * a)
        ans = "(0; ±%s)" % cc
        w = ["(±%s; 0)" % cc, "(0; ±%s)" % rt(a * a + b * b), "(0; ±%d)" % c2]
    return M("Quali sono i fuochi dell’ellisse %s?" % q, ans, [x for x in w if x != ans],
             "Il semiasse maggiore è sull’asse %s; c² = %d − %d = %d, c = %s: <b>%s</b>." % ("x" if not sw else "y", a * a, b * b, c2, cc, ans))


def s2_ecc():
    a, b, c = trip()
    c2 = a * a - b * b
    k, m = simp_root(c2)
    e_txt = FR(rt(c2), str(a)) if m != 1 else fq(Fr(k, a))
    return M("Calcola l’eccentricità dell’ellisse %s." % ell(a * a, b * b), e_txt, [x for x in [fq(Fr(b, a)), FR(rt(a * a + b * b), str(a)), fq(Fr(c2, a * a)) if Fr(c2, a * a) != Fr(k, a) else fq(Fr(a, b))] if x != e_txt],
             "e = c/a con c = √(a² − b²) = %s: e = <b>%s</b> (sempre tra 0 e 1)." % (rt(c2), e_txt))


def s3_scrivi():
    a, b, c = trip()
    t = R.choice(["semi", "fuoco"])
    if t == "semi":
        ans = ell(a * a, b * b)
        return M("Scrivi l’equazione dell’ellisse con centro nell’origine, semiasse %d sull’asse x e %d sull’asse y." % (a, b), ans, [ell(a, b), ell(b * b, a * a), ell(2 * a, 2 * b)],
                 "x²/a² + y²/b² = 1 con a = %d, b = %d: <b>%s</b>." % (a, b, ans))
    c2 = a * a - b * b
    ans = ell(a * a, b * b)
    return M("Un’ellisse con centro nell’origine ha un vertice in (%d; 0) e un fuoco in (%s; 0). Qual è la sua equazione?" % (a, rt(c2)), ans, [ell(a * a, a * a + c2), ell(a * a, c2), ell(b * b, a * a)],
             "a = %d, c² = %d: b² = a² − c² = %d. <b>%s</b>." % (a, c2, b * b, ans))


def s3_canon():
    a, b = R.sample([2, 3, 4, 5, 6], 2)
    A, B = b * b, a * a
    k = R.choice([1, 2]) if False else 1
    q = "%s = %d" % (P2(0, 0, 0).replace("0", "") + "%dx² + %dy²" % (A, B), A * B)
    ans = ell(a * a, b * b)
    return M("Scrivi in forma canonica l’ellisse %s." % q, ans, [ell(A, B), ell(a, b), ell(a * a, b * b).replace("= 1", "= %d" % (A * B))],
             "Divido tutto per %d: <b>%s</b>." % (A * B, ans))


def s4_punto():
    a, b = R.sample(range(2, 7), 2)
    t = R.choice(["si", "no"])
    if t == "si":
        x0 = R.choice([0, a, -a])
        y0 = 0 if x0 else R.choice([b, -b])
    else:
        x0, y0 = R.randint(-a, a), R.randint(-b, b)
    v = Fr(x0 * x0, a * a) + Fr(y0 * y0, b * b)
    ans = "sull’ellisse" if v == 1 else "interno" if v < 1 else "esterno"
    return M("Il punto P(%s; %s) rispetto all’ellisse %s è…" % (fq(x0), fq(y0), ell(a * a, b * b)), ans, [o for o in ["sull’ellisse", "interno", "esterno", "un fuoco"] if o != ans],
             "x²/a² + y²/b² = %s %s 1: <b>%s</b>." % (fq(v), "=" if v == 1 else "&lt;" if v < 1 else "&gt;", ans))


def s4_retta():
    a, b = R.sample([2, 3, 4, 5], 2)
    k = R.choice(["vert", "oriz"])
    t = R.randint(1, 7)
    if k == "vert":
        ans = "secante" if t < a else "tangente" if t == a else "esterna"
        rq = "x = %d" % t
        e = "La retta x = %d va confrontata con il semiasse a = %d: <b>%s</b>." % (t, a, ans)
    else:
        ans = "secante" if t < b else "tangente" if t == b else "esterna"
        rq = "y = %d" % t
        e = "La retta y = %d va confrontata con il semiasse b = %d: <b>%s</b>." % (t, b, ans)
    return M("Com’è la retta %s rispetto all’ellisse %s?" % (rq, ell(a * a, b * b)), ans, [o for o in ["secante", "tangente", "esterna", "asse di simmetria"] if o != ans], e)


def s5_area():
    a, b = R.sample(range(2, 10), 2)
    return M("L’area di un’ellisse di semiassi a e b è πab. Quanto vale l’area dell’ellisse %s?" % ell(a * a, b * b), "%dπ" % (a * b), ["%dπ" % (a * a * b * b), "%dπ" % (2 * a * b), "%dπ" % (a + b)],
             "Semiassi %d e %d: π · %d · %d = <b>%dπ</b>." % (a, b, a, b, a * b))


def main():
    seen = set()
    sets = [
        ("Semiassi e vertici", mix(R, seen, [(s1_semi, 14), (s5_area, 6)])),
        ("Fuochi", mix(R, seen, [(s2_fuochi, 20)])),
        ("Eccentricità e forma canonica", mix(R, seen, [(s2_ecc, 10), (s3_canon, 10)])),
        ("Equazione dell’ellisse", mix(R, seen, [(s3_scrivi, 20)])),
        ("Punti e rette", mix(R, seen, [(s4_punto, 10), (s4_retta, 10)])),
    ]
    body = L(["L’<b>ellisse</b> è il luogo dei punti per cui la somma delle distanze da due punti fissi (i <b>fuochi</b>) è costante. Con centro nell’origine: x²/a² + y²/b² = 1.",
              "a e b sono i <b>semiassi</b>; i vertici sono (±a; 0) e (0; ±b). Se a &gt; b i fuochi sono sull’asse x in (±c; 0) con c² = a² − b²; se b &gt; a sono sull’asse y con c² = b² − a².",
              "L’<b>eccentricità</b> e = c/(semiasse maggiore) è compresa tra 0 e 1: vicina a 0 l’ellisse è quasi una circonferenza, vicina a 1 è molto schiacciata.",
              "Una forma come 4x² + 9y² = 36 si porta alla forma canonica dividendo per il termine noto."],
             [("x²/25 + y²/9 = 1", ["a = 5, b = 3", "c² = 25 − 9 = 16"], "fuochi (±4; 0), e = 4/5"),
              ("4x² + 9y² = 36", ["Divido per 36"], "x²/9 + y²/4 = 1")],
             [["c² = a² + b²", "Nell’ellisse c² = a² − b² (con a semiasse maggiore)."],
              ["Semiassi 25 e 9", "Sono le radici: 5 e 3."],
              ["Fuochi sempre sull’asse x", "Stanno sull’asse del semiasse maggiore."]])
    faq = [("Che cosa vuol dire che l’ellisse è il luogo dei punti con somma delle distanze costante?", "Per ogni punto P dell’ellisse PF<sub>1</sub> + PF<sub>2</sub> = 2a, la lunghezza dell’asse maggiore. È il metodo del giardiniere: una corda fissata in due chiodi."),
           ("Quando un’ellisse è una circonferenza?", "Quando a = b: allora c = 0, i fuochi coincidono con il centro ed e = 0.")]
    unit(G, R, "ellisse", "G",
         "Le coniche nel piano cartesiano: l’ellisse come luogo geometrico, equazione canonica, semiassi, fuochi, eccentricità",
         "L’ellisse", "Ellisse",
         "Schede di matematica per la terza liceo sull’ellisse: equazione canonica, semiassi e vertici, fuochi, eccentricità, equazione dati semiassi o fuochi, posizione di punti e rette, area. 100 esercizi con soluzioni.",
         "x²/a² + y²/b² = 1, c² = a² − b²", "I fuochi stanno sull’asse del semiasse maggiore; e = c/a.",
         body, faq, sets, 7)


if __name__ == "__main__":
    main()
