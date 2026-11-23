# -*- coding: utf-8 -*-
"""
Italia Matematica terza liceo: L’iperbole (Geometria)
  python3 tools/gen_it_matematica_l3_iperbole.py
Iperbole con centro nell’origine: x²/a² − y²/b² = 1 e −x²/a² + y²/b² = 1, vertici, fuochi (c² = a² + b²), asintoti y = ±(b/a)x,
eccentricità, iperbole equilatera x² − y² = a² e xy = k, funzione omografica y = (ax + b)/(cx + d) con asintoti e centro.
Errori: c² = a² − b² come nell’ellisse, asintoti y = ±(a/b)x, asintoto orizzontale della omografica y = b/d.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, FR, simp_root, P2

R = random.Random(72308)
G = "terza-liceo"


def rt(n):
    k, m = simp_root(int(n))
    return str(k) if m == 1 else ("" if k == 1 else str(k)) + "√" + str(m)


def ip(a2, b2, verso="x"):
    if verso == "x":
        return "%s − %s = 1" % ((FR("x²", str(a2)) if a2 != 1 else "x²"), (FR("y²", str(b2)) if b2 != 1 else "y²"))
    return "%s − %s = −1" % ((FR("x²", str(a2)) if a2 != 1 else "x²"), (FR("y²", str(b2)) if b2 != 1 else "y²"))


def ab():
    return R.choice([(3, 4), (4, 3), (6, 8), (5, 12), (12, 5), (8, 6), (2, 1), (1, 2), (2, 3), (3, 1), (2, 5), (4, 1)])


def s1_vert():
    a, b = ab()
    v = R.choice(["x", "y"])
    ans = "(±%d; 0)" % a if v == "x" else "(0; ±%d)" % b
    w = ["(0; ±%d)" % b if v == "x" else "(±%d; 0)" % a, "(±%d; 0)" % (a * a) if v == "x" else "(0; ±%d)" % (b * b), "(±%d; 0) e (0; ±%d)" % (a, b), "(±%d; 0)" % (a + b) if v == "x" else "(0; ±%d)" % (a + b)]
    return M("Quali sono i vertici dell’iperbole %s?" % ip(a * a, b * b, v), ans, [x for x in w if x != ans],
             "%s: <b>%s</b>." % ("L’iperbole taglia l’asse x (con = 1 i vertici sono reali sull’asse x)" if v == "x" else "Con = −1 l’iperbole taglia l’asse y", ans))


def s2_fuochi():
    a, b = ab()
    v = R.choice(["x", "x", "y"])
    c2 = a * a + b * b
    ans = "(±%s; 0)" % rt(c2) if v == "x" else "(0; ±%s)" % rt(c2)
    wr = rt(abs(a * a - b * b)) if a != b else "0"
    w = ["(±%s; 0)" % wr if v == "x" else "(0; ±%s)" % wr, "(0; ±%s)" % rt(c2) if v == "x" else "(±%s; 0)" % rt(c2), "(±%d; 0)" % c2 if v == "x" else "(0; ±%d)" % c2]
    return M("Quali sono i fuochi dell’iperbole %s?" % ip(a * a, b * b, v), ans, [x for x in w if x != ans],
             "Nell’iperbole c² = a² + b² = %d, c = %s; i fuochi stanno sull’asse dei vertici: <b>%s</b>." % (c2, rt(c2), ans))


def s2_asint():
    a, b = ab()
    v = R.choice(["x", "y"])
    m = Fr(b, a)
    ans = "y = ±%sx" % ("" if m == 1 else fq(m))
    w = ["y = ±%sx" % ("" if m == 1 else fq(1 / m)) if m != 1 else "y = ±2x", "y = ±%sx" % fq(Fr(b * b, a * a)) if b != a else "y = ±x + 1", "x = ±%d" % a]
    return M("Quali sono gli asintoti dell’iperbole %s?" % ip(a * a, b * b, v), ans, [x for x in w if x != ans],
             "Asintoti y = ±(b/a)x con a = %d e b = %d (sono gli stessi per = 1 e = −1): <b>%s</b>." % (a, b, ans))


def s3_ecc():
    a, b = ab()
    c2 = a * a + b * b
    k, m = simp_root(c2)
    e = FR(rt(c2), str(a)) if m != 1 else fq(Fr(k, a))
    return M("Calcola l’eccentricità dell’iperbole %s." % ip(a * a, b * b), e, [x for x in [fq(Fr(b, a)), FR(rt(abs(a * a - b * b)), str(a)) if a != b else "0", fq(Fr(a, k)) if m == 1 else FR(str(a), rt(c2))] if x != e],
             "e = c/a con c = √(a² + b²) = %s: e = <b>%s</b> (nell’iperbole e &gt; 1)." % (rt(c2), e))


def s3_scrivi():
    a, b = ab()
    c2 = a * a + b * b
    t = R.choice(["vf", "va"])
    ans = ip(a * a, b * b)
    if t == "vf":
        return M("Un’iperbole con centro nell’origine ha i vertici in (±%d; 0) e i fuochi in (±%s; 0). Qual è la sua equazione?" % (a, rt(c2)), ans, [ip(a * a, c2), ip(a * a, abs(c2 - 2 * a * a)) if c2 != 2 * a * a else ip(a, b), ip(b * b, a * a) if a != b else ip(a, b)],
                 "a = %d, c² = %d: b² = c² − a² = %d. <b>%s</b>." % (a, c2, b * b, ans))
    m = Fr(b, a)
    return M("Un’iperbole con centro nell’origine ha i vertici in (±%d; 0) e gli asintoti y = ±%sx. Qual è la sua equazione?" % (a, "" if m == 1 else fq(m)), ans, [ip(b * b, a * a) if a != b else ip(a, b), ip(a, b), ip(a * a, b * b).replace("−", "+", 1)],
             "b/a = %s con a = %d, quindi b = %d: <b>%s</b>." % (fq(m), a, b, ans))


def s4_equi():
    k = R.choice(["xy", "x2"])
    if k == "xy":
        kk = nz(R, -12, 12)
        t = R.choice(["asint", "quad"])
        if t == "asint":
            return M("Quali sono gli asintoti dell’iperbole equilatera xy = %s?" % fq(kk), "gli assi cartesiani (x = 0 e y = 0)", ["y = ±x", "x = %s e y = %s" % (fq(kk), fq(kk)), "y = %sx" % fq(kk)],
                     "L’iperbole xy = k è riferita ai propri asintoti: sono <b>gli assi cartesiani</b>.")
        ans = "primo e terzo quadrante" if kk > 0 else "secondo e quarto quadrante"
        return M("In quali quadranti sta l’iperbole xy = %s?" % fq(kk), ans, ["secondo e quarto quadrante" if kk > 0 else "primo e terzo quadrante", "primo e secondo quadrante", "in tutti i quadranti"],
                 "x e y hanno segno %s: <b>%s</b>." % ("concorde (k &gt; 0)" if kk > 0 else "discorde (k &lt; 0)", ans))
    a = R.randint(1, 6)
    return M("Quali sono gli asintoti dell’iperbole equilatera x² − y² = %d?" % (a * a), "y = ±x", ["y = ±%dx" % a if a > 1 else "y = ±2x", "x = ±%d" % a, "gli assi cartesiani"],
             "È equilatera (a = b = %d): gli asintoti sono le bisettrici <b>y = ±x</b>." % a)


def s5_omog():
    a, c = nz(R, -4, 4), nz(R, -3, 3)
    b, dd = R.randint(-6, 6), R.randint(-6, 6)
    if a * dd - b * c == 0:
        return None
    f = "y = %s" % FR(P2(0, a, b), P2(0, c, dd))
    t = R.choice(["v", "o", "C"])
    xv, yo = Fr(-dd, c), Fr(a, c)
    if t == "v":
        return M("Qual è l’asintoto verticale della funzione omografica %s?" % f, "x = %s" % fq(xv), ["x = %s" % fq(v) for v in W(-xv if xv else 1, Fr(-b, a), yo) if v != xv] + ["y = %s" % fq(xv)],
                 "Si annulla il denominatore: %s = 0 → <b>x = %s</b>." % (P2(0, c, dd), fq(xv)))
    if t == "o":
        return M("Qual è l’asintoto orizzontale della funzione omografica %s?" % f, "y = %s" % fq(yo), ["y = %s" % fq(v) for v in W(Fr(b, dd) if dd else Fr(b), Fr(c, a), -yo) if v != yo] + ["x = %s" % fq(yo)],
                 "Asintoto orizzontale y = a/c (rapporto dei coefficienti di x) = <b>%s</b>." % fq(yo))
    ans = "(%s; %s)" % (fq(xv), fq(yo))
    return M("Qual è il centro di simmetria della funzione omografica %s?" % f, ans, ["(%s; %s)" % (fq(yo), fq(xv)) if xv != yo else "(%s; %s)" % (fq(xv), fq(-yo)), "(%s; %s)" % (fq(-xv), fq(yo)) if xv else "(1; %s)" % fq(yo), "(%s; %s)" % (fq(Fr(-b, a)), fq(Fr(b, dd) if dd else 0))],
             "Il centro è l’intersezione degli asintoti x = %s e y = %s: <b>%s</b>." % (fq(xv), fq(yo), ans))


def main():
    seen = set()
    sets = [
        ("Vertici e fuochi", mix(R, seen, [(s1_vert, 8), (s2_fuochi, 12)])),
        ("Asintoti ed eccentricità", mix(R, seen, [(s2_asint, 12), (s3_ecc, 8)])),
        ("Equazione dell’iperbole", mix(R, seen, [(s3_scrivi, 20)])),
        ("Iperbole equilatera", mix(R, seen, [(s4_equi, 12), (s2_asint, 8)])),
        ("Funzione omografica", mix(R, seen, [(s5_omog, 20)])),
    ]
    body = L(["L’<b>iperbole</b> è il luogo dei punti per cui la differenza (in valore assoluto) delle distanze da due fuochi è costante. Con centro nell’origine e fuochi sull’asse x: x²/a² − y²/b² = 1.",
              "Vertici (±a; 0), fuochi (±c; 0) con <b>c² = a² + b²</b>, asintoti y = ±(b/a)x, eccentricità e = c/a &gt; 1. Con = −1 i vertici e i fuochi sono sull’asse y.",
              "L’iperbole <b>equilatera</b> ha a = b: x² − y² = a² ha asintoti y = ±x; ruotata, diventa xy = k, con asintoti gli assi.",
              "La <b>funzione omografica</b> y = (ax + b)/(cx + d) è un’iperbole equilatera traslata: asintoti x = −d/c e y = a/c, centro nel loro punto d’incontro."],
             [("x²/9 − y²/16 = 1", ["a = 3, b = 4, c = 5"], "fuochi (±5; 0), asintoti y = ±4/3 x"),
              ("y = (2x + 1)/(x − 3)", ["x − 3 = 0", "a/c = 2"], "asintoti x = 3 e y = 2")],
             [["c² = a² − b²", "Questa è l’ellisse; nell’iperbole c² = a² + b²."],
              ["Asintoti y = ±(a/b)x", "Sono y = ±(b/a)x: b sopra, a sotto."],
              ["Asintoto orizzontale y = b/d", "È y = a/c, il rapporto dei coefficienti di x."]])
    faq = [("Perché nell’iperbole e &gt; 1?", "Perché c² = a² + b² &gt; a², quindi c &gt; a e il rapporto c/a è maggiore di 1."),
           ("Che cosa sono gli asintoti?", "Rette a cui il grafico si avvicina sempre di più senza toccarle, allontanandosi dal centro. Si disegnano con il rettangolo di lati 2a e 2b: sono le sue diagonali.")]
    unit(G, R, "iperbole", "G",
         "Le coniche nel piano cartesiano: l’iperbole come luogo geometrico, equazione canonica, asintoti, iperbole equilatera, funzione omografica",
         "L’iperbole", "Iperbole",
         "Schede di matematica per la terza liceo sull’iperbole: vertici, fuochi, asintoti, eccentricità, equazione dell’iperbole, iperbole equilatera, funzione omografica. 100 esercizi con soluzioni.",
         "x²/a² − y²/b² = 1, c² = a² + b²", "Asintoti y = ±(b/a)x; omografica: x = −d/c e y = a/c.",
         body, faq, sets, 8)


if __name__ == "__main__":
    main()
