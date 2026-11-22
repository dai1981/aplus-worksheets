# -*- coding: utf-8 -*-
"""
Italia Matematica seconda media: Area dei poligoni (Spazio e figure)
  python3 tools/gen_it_matematica_m2_area_dei_poligoni.py
Equivalenze di superficie (× 100), area di rettangolo, quadrato, parallelogramma, triangolo, rombo, trapezio anche con i decimali,
area del quadrato dalla diagonale, poligoni regolari (apotema = lato × numero fisso, A = p × a : 2), formule inverse,
figure equivalenti e figure composte.
Errori: × 10 invece di × 100 nelle equivalenze, dimenticare : 2, sommare le basi del trapezio senza moltiplicare per l’altezza.
"""
import random
from fractions import Fraction as Fr
from it_media import M, L, unit, mix, table, W, num, d, dk, Kids, NB
import gen_it_matematica_c5_perimetro_e_area_dei_poligoni as X

R = random.Random(71207)
G = "seconda-media"
K = Kids(R)
X.R = R
X.cm = lambda v: "%s%scm" % (d(v), NB)


def c2(v, u="cm²"):
    return "%s%s%s" % (d(v), NB, u)


def eu(x):
    x = Fr(x)
    return "%s €" % (d(x) if x.denominator == 1 else dk(x, 2))


def dm(lo, hi, step=Fr(1, 2)):
    n = R.randint(int(lo / step), int(hi / step))
    return n * step


UN = ["mm²", "cm²", "dm²", "m²", "dam²", "hm²", "km²"]


def s1_equiv():
    i = R.randrange(len(UN) - 1)
    j = R.choice([k for k in range(len(UN)) if k != i and abs(k - i) <= 2])
    v = R.choice([Fr(R.randint(2, 99)), Fr(R.randint(11, 999), 10), Fr(R.randint(101, 9999), 100), Fr(R.randint(2, 9))])
    r = v * Fr(100) ** (i - j)
    try:
        ans = c2(r, UN[j])
        w = [c2(v * Fr(10) ** (i - j), UN[j]), c2(v * Fr(100) ** (j - i), UN[j]), c2(v * Fr(1000) ** (i - j), UN[j])]
    except ValueError:
        return None
    if len(ans) > 22:
        return None
    return M("%s = … %s" % (c2(v, UN[i]), UN[j]), ans, W(*w), "Ogni unità di superficie è 100 volte la successiva: si %s per %s. <b>%s</b>." % ("moltiplica" if i > j else "divide", num(100 ** abs(i - j)), ans))


def s2_base():
    k = R.choice(["rett", "para", "tri", "quad"])
    a = dm(2, 14)
    b = dm(2, 10)
    if k == "quad":
        A = a * a
        return M("%sCalcola l’area del quadrato di lato %s." % (X.fig("quad", a), X.cm(a)), c2(A), W(c2(4 * a), c2(2 * a), c2(A / 2), c2(A * 2)), "A = l × l = %s × %s = <b>%s</b>." % (d(a), d(a), c2(A)))
    if k == "rett":
        A = a * b
        if a == b:
            return None
        return M("%sCalcola l’area del rettangolo." % X.fig("rett", max(a, b), min(a, b)), c2(A), W(c2(2 * (a + b)), c2(a + b), c2(A / 2)), "A = b × h = %s × %s = <b>%s</b>." % (d(max(a, b)), d(min(a, b)), c2(A)))
    if k == "para":
        A = a * b
        c = b + R.choice([Fr(1, 2), 1, Fr(3, 2), 2])
        return M("%sCalcola l’area del parallelogramma (il lato obliquo misura %s)." % (X.fig("para", a, b, c), X.cm(c)), c2(A), W(c2(a * c), c2(A / 2), c2(2 * (a + c))), "A = b × h = %s × %s = <b>%s</b>. Il lato obliquo non serve." % (d(a), d(b), c2(A)))
    A = a * b / 2
    return M("%sCalcola l’area del triangolo." % X.fig("tri", a, b), c2(A), W(c2(a * b), c2(a + b), c2(A / 2)), "A = b × h : 2 = %s × %s : 2 = <b>%s</b>." % (d(a), d(b), c2(A)))


NF = [("triangolo equilatero", 3, Fr(289, 1000)), ("quadrato", 4, Fr(1, 2)), ("pentagono regolare", 5, Fr(688, 1000)), ("esagono regolare", 6, Fr(866, 1000)), ("ottagono regolare", 8, Fr(1207, 1000))]


def s3_altri():
    k = R.choice(["rombo", "trap", "diag", "reg", "reg"])
    if k == "rombo":
        D, dd = sorted([R.randint(4, 30), R.randint(4, 30)], reverse=True)
        if D == dd:
            return None
        A = Fr(D * dd, 2)
        return M("%sCalcola l’area del rombo." % X.fig("rombo", D, dd), c2(A), W(c2(D * dd), c2(D + dd), c2(2 * (D + dd))), "A = D × d : 2 = %d × %d : 2 = <b>%s</b>." % (D, dd, c2(A)))
    if k == "trap":
        B = R.randint(8, 24)
        b = R.randint(3, B - 2)
        h = R.randint(3, 15)
        A = Fr((B + b) * h, 2)
        return M("%sCalcola l’area del trapezio." % X.fig("trap", B, b, h), c2(A), W(c2((B + b) * h), c2(B * b * h), c2(B + b + h), c2(Fr(B * h, 2) + b)), "A = (B + b) × h : 2 = (%d + %d) × %d : 2 = <b>%s</b>." % (B, b, h, c2(A)))
    if k == "diag":
        dd = R.randint(3, 20)
        return M("La diagonale di un quadrato misura %d cm. Qual è l’area del quadrato?" % dd, c2(Fr(dd * dd, 2)), W(c2(dd * dd), c2(4 * dd), c2(2 * dd)), "Il quadrato è un rombo con diagonali uguali: A = d × d : 2 = %d × %d : 2 = <b>%s</b>." % (dd, dd, c2(Fr(dd * dd, 2))))
    nm, n, f = R.choice(NF[2:])
    l = R.randint(2, 20)
    a = l * f
    p = n * l
    A = p * a / 2
    return M("Un %s ha il lato di %d cm (numero fisso %s). Calcola l’apotema e l’area." % (nm, l, d(f)), "a = %s; A = %s" % (X.cm(a), c2(A)),
             W("a = %s; A = %s" % (X.cm(a), c2(p * a)), "a = %s; A = %s" % (X.cm(a * 2), c2(p * a)), "a = %s; A = %s" % (X.cm(a), c2(l * a / 2))),
             "a = l × f = %d × %s = %s; p = %d × %d = %d cm; A = p × a : 2 = %d × %s : 2 = <b>%s</b>." % (l, d(f), d(a), n, l, p, p, d(a), c2(A)))


def s4_inverse():
    k = R.choice(["tri_h", "tri_b", "para_h", "rombo_d", "trap_h", "trap_s", "rett_b", "quad_l"])
    if k == "tri_h":
        b, h = R.randint(4, 30), R.randint(3, 25)
        A = Fr(b * h, 2)
        return M("Un triangolo ha area %s e base %d cm. Quanto misura l’altezza?" % (c2(A), b), X.cm(h), W(X.cm(A / b) if (A / b).denominator in (1, 2, 4, 5, 10) else None, X.cm(A * 2 * b) if A * 2 * b < 2000 else None, X.cm(A - b) if A > b else None, X.cm(h * 2)),
                 "h = A × 2 : b = %s × 2 : %d = <b>%s</b>." % (d(A), b, X.cm(h)))
    if k == "tri_b":
        b, h = R.randint(4, 30), R.randint(3, 25)
        A = Fr(b * h, 2)
        return M("Un triangolo ha area %s e altezza %d cm. Quanto misura la base?" % (c2(A), h), X.cm(b), W(X.cm(A / h) if (A / h).denominator in (1, 2, 4, 5, 10) else None, X.cm(b * 2), X.cm(A - h) if A > h else None, X.cm(b + 1)),
                 "b = A × 2 : h = %s × 2 : %d = <b>%s</b>." % (d(A), h, X.cm(b)))
    if k == "para_h":
        b, h = R.randint(4, 25), R.randint(3, 20)
        return M("Un parallelogramma ha area %s e base %d cm. Quanto misura l’altezza?" % (c2(b * h), b), X.cm(h), W(X.cm(h * 2), X.cm(Fr(h, 2)), X.cm(b * h - b), X.cm(h + 1)), "h = A : b = %d : %d = <b>%s</b>." % (b * h, b, X.cm(h)))
    if k == "rombo_d":
        D, dd = R.randint(6, 30), R.randint(4, 20)
        A = Fr(D * dd, 2)
        return M("Un rombo ha area %s e una diagonale di %d cm. Quanto misura l’altra diagonale?" % (c2(A), D), X.cm(dd), W(X.cm(A / D) if (A / D).denominator in (1, 2, 4, 5, 10) else None, X.cm(dd * 2), X.cm(A - D) if A > D else None, X.cm(dd + 2)),
                 "d = A × 2 : D = %s × 2 : %d = <b>%s</b>." % (d(A), D, X.cm(dd)))
    if k == "trap_h":
        B, b, h = R.randint(10, 30), R.randint(3, 9), R.randint(3, 16)
        A = Fr((B + b) * h, 2)
        return M("Un trapezio ha area %s e le basi di %d cm e %d cm. Quanto misura l’altezza?" % (c2(A), B, b), X.cm(h), W(X.cm(A / (B + b)) if (A / (B + b)).denominator in (1, 2, 4, 5, 10) else None, X.cm(h * 2), X.cm(h + 1), X.cm(h - 1)),
                 "h = A × 2 : (B + b) = %s × 2 : %d = <b>%s</b>." % (d(A), B + b, X.cm(h)))
    if k == "trap_s":
        B, b, h = R.randint(10, 30), R.randint(3, 9), R.randint(3, 16)
        A = Fr((B + b) * h, 2)
        return M("Un trapezio ha area %s e altezza %d cm. Quanto vale la somma delle basi?" % (c2(A), h), X.cm(B + b), W(X.cm(A / h) if (A / h).denominator in (1, 2, 4, 5, 10) else None, X.cm((B + b) * 2), X.cm(B + b + h), X.cm(B + b - 1)),
                 "B + b = A × 2 : h = %s × 2 : %d = <b>%s</b>." % (d(A), h, X.cm(B + b)))
    if k == "rett_b":
        b, h = R.randint(4, 30), R.randint(3, 20)
        if b == h:
            return None
        return M("Un rettangolo ha area %s e altezza %d cm. Quanto misura la base?" % (c2(b * h), h), X.cm(b), W(X.cm(b * h - h), X.cm(b * 2), X.cm(Fr(b, 2)), X.cm(b + 1)), "b = A : h = %d : %d = <b>%s</b>." % (b * h, h, X.cm(b)))
    l = R.randint(3, 30)
    return M("Un quadrato ha area %s. Quanto misura il lato?" % c2(l * l), X.cm(l), W(X.cm(Fr(l * l, 2)), X.cm(Fr(l * l, 4)) if l * l % 4 == 0 else None, X.cm(l + 1), X.cm(l * 2)),
             "l = √A = √%d = <b>%s</b>." % (l * l, X.cm(l)))


def s5():
    p = K.next()
    k = R.choice(["pavimento", "cornice", "equiv", "prato", "terreno", "piastrelle"])
    if k == "pavimento":
        a, b = R.choice([(Fr(9, 2), 4), (5, Fr(7, 2)), (6, Fr(9, 2)), (Fr(11, 2), 4), (7, 5), (8, Fr(9, 2))])
        pr = R.choice([18, 22, 25, 30, 35])
        A = Fr(a) * b
        return M("Il pavimento di una stanza rettangolare misura %s m × %s m. Il parquet costa %d € al m². Quanto si spende?" % (d(a), d(b), pr), eu(A * pr),
                 W(eu(2 * (a + b) * pr), eu((Fr(a) + b) * pr), eu(A), eu(A * pr / 2)), "A = %s × %s = %s m²; %s × %d = <b>%s</b>." % (d(a), d(b), d(A), d(A), pr, eu(A * pr)))
    if k == "cornice":
        a, b = R.randint(20, 50), R.randint(15, 40)
        c = R.choice([2, 3, 4, 5])
        A = (a + 2 * c) * (b + 2 * c) - a * b
        return M("Una foto di %d cm × %d cm ha una cornice larga %d cm tutto intorno. Qual è l’area della cornice?" % (a, b, c), c2(A), W(c2((a + c) * (b + c) - a * b), c2((a + 2 * c) * (b + 2 * c)), c2(2 * (a + b) * c), c2(A + 4 * c * c)),
                 "Rettangolo esterno: %d × %d = %d cm²; foto: %d cm²; cornice: %d − %d = <b>%s</b>." % (a + 2 * c, b + 2 * c, (a + 2 * c) * (b + 2 * c), a * b, (a + 2 * c) * (b + 2 * c), a * b, c2(A)))
    if k == "equiv":
        b, h = R.randint(4, 20), R.randint(3, 15)
        b2 = R.choice([v for v in range(2, 41) if (b * h) % v == 0 and v != b])
        return M("Un rettangolo di %d cm × %d cm è equivalente (stessa area) a un parallelogramma con base %d cm. Quanto misura l’altezza del parallelogramma?" % (b, h, b2), X.cm(b * h // b2),
                 W(X.cm(h), X.cm(b * h // b2 * 2), X.cm(Fr(b * h, 2 * b2)) if Fr(b * h, 2 * b2).denominator in (1, 2) else None, X.cm(b * h // b2 + 1)),
                 "Area: %d × %d = %d cm²; h = %d : %d = <b>%s</b>." % (b, h, b * h, b * h, b2, X.cm(b * h // b2)))
    if k == "prato":
        B, b, h = R.randint(30, 80), R.randint(10, 29), R.randint(10, 40)
        s = R.choice([Fr(1, 40), Fr(1, 50), Fr(1, 20)])
        A = Fr((B + b) * h, 2)
        g = A * s * 1000
        return M("Un prato a forma di trapezio ha le basi di %d m e %d m e l’altezza di %d m. Per seminarlo servono %s g di semi al m². Quanti grammi di semi servono?" % (B, b, h, d(s * 1000)), "%s g" % d(g),
                 W("%s g" % d(g * 2), "%s g" % d(Fr((B + b) * h) * s * 1000 / 4), "%s g" % d(A), "%s g" % d(Fr(B * b * h, 2) * s * 1000) if (Fr(B * b * h, 2) * s * 1000).denominator in (1, 2, 4, 5, 10) else None),
                 "A = (%d + %d) × %d : 2 = %s m²; %s × %s = <b>%s g</b>." % (B, b, h, d(A), d(A), d(s * 1000), d(g)))
    if k == "terreno":
        D, dd = R.randint(20, 80), R.randint(10, 60)
        pr = R.choice([5, 8, 10, 12, 15])
        A = Fr(D * dd, 2)
        return M("Un terreno a forma di rombo ha le diagonali di %d m e %d m. Viene venduto a %d € al m². Quanto costa?" % (D, dd, pr), "%s €" % d(A * pr), W("%s €" % d(D * dd * pr), "%s €" % d((D + dd) * pr), "%s €" % d(A)), "A = %d × %d : 2 = %s m²; × %d = <b>%s €</b>." % (D, dd, d(A), pr, d(A * pr)))
    l = R.choice([20, 25, 30, 40, 50])
    a, b = R.choice([(3, 4), (4, 5), (5, 6), (3, 5), (6, 4), (2, 3)])
    n = a * b * 10000 // (l * l)
    if a * b * 10000 % (l * l):
        return None
    return M("Una stanza di %d m × %d m si piastrella con piastrelle quadrate di %d cm di lato. Quante piastrelle servono?" % (a, b, l), num(n), W(num(n * 2), num(a * b * 100 // l) if a * b * 100 % l == 0 else None, num(n // 2), num(a * b * 10000 // l)),
             "Stanza: %d m² = %s cm²; piastrella: %d cm²; %s : %d = <b>%s</b>." % (a * b, num(a * b * 10000), l * l, num(a * b * 10000), l * l, num(n)))


def main():
    seen = set()
    sets = [
        ("Unità di misura di superficie", mix(R, seen, [(s1_equiv, 20)])),
        ("Rettangolo, quadrato, parallelogramma, triangolo", mix(R, seen, [(s2_base, 20)])),
        ("Rombo, trapezio e poligoni regolari", mix(R, seen, [(s3_altri, 20)])),
        ("Formule inverse", mix(R, seen, [(s4_inverse, 20)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = L(["L’<b>area</b> misura la superficie. Le unità di superficie vanno di <b>100 in 100</b>: 1 m² = 100 dm² = 10 000 cm².",
              "Rettangolo e parallelogramma: A = b × h. Triangolo: A = b × h : 2. Rombo: A = D × d : 2. Trapezio: A = (B + b) × h : 2.",
              "Poligono regolare: apotema a = l × numero fisso; A = perimetro × apotema : 2.",
              "Le <b>formule inverse</b> si ottengono «tornando indietro»: nel triangolo h = A × 2 : b."],
             [("Trapezio B = 12 cm, b = 8 cm, h = 5 cm", ["(12 + 8) × 5 : 2"], "50 cm²"),
              ("3,5 m² in dm²", ["× 100"], "350 dm²")],
             [["× 10 invece di × 100", "1 dm² = 100 cm²: ogni passaggio vale 100."],
              ["Dimenticare : 2", "Triangolo, rombo e trapezio hanno «: 2» nella formula."],
              ["Usare il lato obliquo come altezza", "L’altezza è perpendicolare alla base."]],
             table(["Figura", "Area", "Formula inversa"], [["triangolo", "b × h : 2", "h = A × 2 : b"], ["rombo", "D × d : 2", "d = A × 2 : D"], ["trapezio", "(B + b) × h : 2", "h = A × 2 : (B + b)"], ["poligono regolare", "p × a : 2", "a = A × 2 : p"]]))
    faq = [("Che cos’è il numero fisso?", "È il rapporto tra apotema e lato, uguale in tutti i poligoni regolari con lo stesso numero di lati: per l’esagono è 0,866."),
           ("Quando due figure sono equivalenti?", "Quando hanno la stessa area, anche se hanno forme diverse.")]
    unit(G, R, "area-dei-poligoni", "S",
         "Calcolare l’area di semplici figure scomponendole in figure elementari; determinare l’area dei poligoni utilizzando le più comuni formule; usare le unità di misura di superficie",
         "Area dei poligoni", "Area dei poligoni",
         "Schede di matematica per la seconda media sull’area dei poligoni: equivalenze, rettangolo, parallelogramma, triangolo, rombo, trapezio, poligoni regolari, formule inverse e problemi. 100 esercizi con soluzioni.",
         "Triangolo, rombo e trapezio: non dimenticare : 2.", "1 m² = 100 dm² = 10 000 cm².",
         body, faq, sets, 7)


if __name__ == "__main__":
    main()
