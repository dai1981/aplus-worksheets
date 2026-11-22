# -*- coding: utf-8 -*-
"""
Italia Matematica seconda media: Applicazioni del teorema di Pitagora (Spazio e figure)
  python3 tools/gen_it_matematica_m2_applicazioni_del_teorema_di_pitagora.py
Diagonale del rettangolo e del quadrato (d = l × √2 ≈ l × 1,414), altezza del triangolo isoscele ed equilatero
(h ≈ l × 0,866), lato del rombo dalle diagonali, lato obliquo del trapezio rettangolo e isoscele,
distanza tra due punti nel piano cartesiano, problemi con perimetro e area.
Errori: usare la diagonale intera nel rombo, usare la base intera nel triangolo isoscele, dimenticare la differenza delle basi nel trapezio.
"""
import math
import random
from fractions import Fraction as Fr
from it_media import M, L, unit, mix, table, W, num, d, dk, figure, kosy, Kids

R = random.Random(71209)
G = "seconda-media"
K = Kids(R)
TERNE = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)]


def terna(maxc=60):
    while True:
        a, b, c = R.choice(TERNE)
        k = R.choice([1, 2, 3, 4, 5])
        if c * k <= maxc:
            return a * k, b * k, c * k


def cm(v):
    return "%s cm" % d(v)


def c2(v):
    return "%s cm²" % d(v)


def s1_rett():
    a, b, c = terna()
    if R.random() < 0.5:
        a, b = b, a
    pts = {"A": (0, 0), "B": (a, 0), "C": (a, b), "D": (0, b)}
    pic = figure(pts, [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("A", "C")], [("A", "B", cm(a)), ("B", "C", cm(b)), ("A", "C", "d")], right=[("B", "A", "C")], label="rettangolo con la diagonale")
    if R.random() < 0.6:
        return M("%sCalcola la diagonale del rettangolo con base %d cm e altezza %d cm." % (pic, a, b), cm(c), W(cm(a + b), cm(c + 1), cm(a * a + b * b), cm(2 * (a + b))), "d = √(%d² + %d²) = √%d = <b>%s</b>." % (a, b, c * c, cm(c)))
    return M("Un rettangolo ha la diagonale di %d cm e la base di %d cm. Calcola il perimetro." % (c, a), cm(2 * (a + b)), W(cm(2 * (a + c)), cm(a + b), cm(a * b), cm(2 * (a + b) + 2)),
             "h = √(%d² − %d²) = %d cm; 2p = 2 × (%d + %d) = <b>%s</b>." % (c, a, b, a, b, cm(2 * (a + b))))


def s1_quad():
    l = R.randint(2, 30)
    if R.random() < 0.6:
        return M("Calcola la diagonale di un quadrato di lato %d cm (usa √2 ≈ 1,414)." % l, cm(l * Fr(1414, 1000)), W(cm(l * 2), cm(l * Fr(1732, 1000)), cm(l + Fr(1414, 1000)), cm(l * Fr(707, 1000))),
                 "d = l × √2 = %d × 1,414 = <b>%s</b>." % (l, cm(l * Fr(1414, 1000))))
    dd = R.randint(2, 30)
    return M("La diagonale di un quadrato misura %d cm. Quanto misura il lato (usa √2 ≈ 1,414, arrotonda ai decimi)?" % dd, "%s cm" % dk(Fr(dd * 1000, 1414), 1), W("%s cm" % dk(Fr(dd * 1414, 1000), 1), "%s cm" % dk(Fr(dd, 2), 1), "%s cm" % dk(Fr(dd * 1000, 1414) + 1, 1)),
             "l = d : √2 = %d : 1,414 ≈ <b>%s cm</b>." % (dd, dk(Fr(dd * 1000, 1414), 1)))


def s2_isoscele():
    a, b, c = terna()
    half, h, l = (a, b, c) if R.random() < 0.5 else (b, a, c)
    pts = {"A": (0, 0), "B": (2 * half, 0), "C": (half, h), " ": (half, 0)}
    pic = figure(pts, [("A", "B"), ("B", "C"), ("C", "A")], [("B", "C", cm(l))], right=[(" ", "B", "C")], label="triangolo isoscele con l’altezza", dashed=[("C", " ")], ticks=[("A", "C", 1), ("B", "C", 1)])
    if R.random() < 0.5:
        return M("%sUn triangolo isoscele ha la base di %d cm e i lati obliqui di %d cm. Calcola l’altezza." % (pic, 2 * half, l), cm(h), W(cm(int(math.isqrt(l * l - 4 * half * half))) if l > 2 * half and math.isqrt(l * l - 4 * half * half) ** 2 == l * l - 4 * half * half else None, cm(l - half), cm(h + 1), cm(l + half)),
                 "Metà base: %d cm; h = √(%d² − %d²) = √%d = <b>%s</b>." % (half, l, half, h * h, cm(h)))
    return M("Un triangolo isoscele ha la base di %d cm e l’altezza di %d cm. Calcola il perimetro." % (2 * half, h), cm(2 * half + 2 * l), W(cm(2 * half + l), cm(2 * half + 2 * h), cm(half * h), cm(2 * half + 2 * l + 2)),
             "Lato obliquo: √(%d² + %d²) = %d cm; 2p = %d + 2 × %d = <b>%s</b>." % (half, h, l, 2 * half, l, cm(2 * half + 2 * l)))


def s2_equi():
    l = R.randint(2, 30)
    if R.random() < 0.5:
        return M("Calcola l’altezza di un triangolo equilatero di lato %d cm (usa h = l × 0,866)." % l, cm(l * Fr(866, 1000)), W(cm(l * Fr(1414, 1000)), cm(Fr(l, 2)), cm(l * Fr(866, 100)), cm(l * Fr(433, 1000))),
                 "h = %d × 0,866 = <b>%s</b>." % (l, cm(l * Fr(866, 1000))))
    l = R.randint(1, 10) * 2
    h = l * Fr(866, 1000)
    A = l * h / 2
    return M("Calcola l’area di un triangolo equilatero di lato %d cm (usa h = l × 0,866)." % l, c2(A), W(c2(l * h), c2(Fr(l * l, 2)), c2(A + l)), "h = %d × 0,866 = %s cm; A = %d × %s : 2 = <b>%s</b>." % (l, d(h), l, d(h), c2(A)))


def s3_rombo():
    a, b, c = terna()
    D, dd = 2 * max(a, b), 2 * min(a, b)
    pts = {"A": (0, 0), "B": (D / 2, -dd / 2), "C": (D, 0), "D": (D / 2, dd / 2), " ": (D / 2, 0)}
    pic = figure(pts, [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")], [], right=[(" ", "C", "D")], label="rombo con le diagonali", dashed=[("A", "C"), ("B", "D")])
    if R.random() < 0.6:
        return M("%sUn rombo ha le diagonali di %d cm e %d cm. Calcola il lato." % (pic, D, dd), cm(c), W(cm(int(math.isqrt(D * D + dd * dd))) if math.isqrt(D * D + dd * dd) ** 2 == D * D + dd * dd else cm(2 * c), cm(Fr(D + dd, 2)), cm(c + 1), cm(4 * c)),
                 "Le diagonali si dividono a metà: %d cm e %d cm. l = √(%d² + %d²) = √%d = <b>%s</b>." % (D // 2, dd // 2, D // 2, dd // 2, c * c, cm(c)))
    return M("Un rombo ha le diagonali di %d cm e %d cm. Calcola il perimetro." % (D, dd), cm(4 * c), W(cm(2 * (D + dd)), cm(4 * c * 2), cm(c), cm(Fr(D * dd, 2))),
             "Lato: √(%d² + %d²) = %d cm; 2p = 4 × %d = <b>%s</b>." % (D // 2, dd // 2, c, c, cm(4 * c)))


def s3_trapezio():
    a, b, c = terna(40)
    k = R.choice(["rett", "iso"])
    if k == "rett":
        dif, h = (a, b) if R.random() < 0.5 else (b, a)
        bb = R.randint(3, 20)
        B = bb + dif
        pts = {"A": (0, 0), "B": (B, 0), "C": (bb, h), "D": (0, h)}
        pic = figure(pts, [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")], [("A", "B", cm(B)), ("D", "C", cm(bb)), ("A", "D", cm(h))], right=[("A", "B", "D"), ("D", "A", "C")], label="trapezio rettangolo")
        return M("%sIn un trapezio rettangolo le basi misurano %d cm e %d cm e l’altezza %d cm. Calcola il lato obliquo." % (pic, B, bb, h), cm(c), W(cm(int(math.isqrt(B * B + h * h))) if math.isqrt(B * B + h * h) ** 2 == B * B + h * h else cm(B + h - bb), cm(dif + h), cm(c + 1), cm(B - bb)),
                 "Proiezione del lato obliquo: %d − %d = %d cm; l = √(%d² + %d²) = <b>%s</b>." % (B, bb, dif, dif, h, cm(c)))
    pr, h = (a, b) if R.random() < 0.5 else (b, a)
    bb = R.randint(3, 20)
    B = bb + 2 * pr
    pts = {"A": (0, 0), "B": (B, 0), "C": (pr + bb, h), "D": (pr, h)}
    pic = figure(pts, [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")], [("A", "B", cm(B)), ("D", "C", cm(bb)), ("B", "C", cm(c))], label="trapezio isoscele", ticks=[("A", "D", 1), ("B", "C", 1)])
    return M("%sIn un trapezio isoscele le basi misurano %d cm e %d cm e i lati obliqui %d cm. Calcola l’altezza." % (pic, B, bb, c), cm(h), W(cm(int(math.isqrt(c * c - (B - bb) ** 2))) if c > B - bb and math.isqrt(c * c - (B - bb) ** 2) ** 2 == c * c - (B - bb) ** 2 else cm(c - pr), cm(h + 1), cm(c - pr) if c - pr != h else cm(h + 2), cm(B - bb)),
             "Proiezione: (%d − %d) : 2 = %d cm; h = √(%d² − %d²) = <b>%s</b>." % (B, bb, pr, c, pr, cm(h)))


def s4_distanza():
    a, b, c = R.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (4, 3, 5), (8, 6, 10), (12, 5, 13), (9, 12, 15), (12, 9, 15)])
    if a > 9 or b > 9:
        x1, y1 = R.randint(0, 10 - min(a, 10)), R.randint(0, 10 - min(b, 10))
        if x1 + a > 12 or y1 + b > 12:
            return None
        pic = ""
    else:
        x1, y1 = R.randint(0, 10 - a), R.randint(0, 10 - b)
        pic = kosy([], [(x1, y1, "A"), (x1 + a, y1 + b, "B")], 0, 10, 26, "piano cartesiano con due punti")
    x2, y2 = x1 + a, y1 + b
    return M("%sCalcola la distanza tra A(%d; %d) e B(%d; %d)." % (pic, x1, y1, x2, y2), str(c), W(a + b, c + 1, c * c, abs(a - b) + c),
             "Differenze: %d − %d = %d e %d − %d = %d. AB = √(%d² + %d²) = √%d = <b>%d</b>." % (x2, x1, a, y2, y1, b, a, b, c * c, c))


def s5():
    k = R.choice(["recinto", "cornice", "tetto", "aiuola", "giardino"])
    if k == "recinto":
        a, b, c = terna(50)
        pr = R.choice([5, 8, 10, 12])
        return M("Un giardino a forma di triangolo rettangolo ha i cateti di %d m e %d m. Una rete costa %d € al metro. Quanto costa recintarlo?" % (a, b, pr), "%s €" % num((a + b + c) * pr), W("%s €" % num((a + b) * pr), "%s €" % num(a * b // 2 * pr) if a * b % 2 == 0 else None, "%s €" % num((a + b + c) * pr + pr), "%s €" % num(c * pr)),
                 "Ipotenusa: %d m; perimetro: %d + %d + %d = %d m; %d × %d = <b>%s €</b>." % (c, a, b, c, a + b + c, a + b + c, pr, num((a + b + c) * pr)))
    if k == "tetto":
        a, b, c = R.choice([(3, 4, 5), (4, 3, 5), (6, 8, 10), (5, 12, 13)])
        return M("Il tetto di una casetta ha la sezione di un triangolo isoscele: la base è larga %d m e la falda è lunga %d m. Quanto è alto il tetto?" % (2 * a, c), "%d m" % b, W("%d m" % (c - a), "%d m" % (c + a), "%d m" % (b + 1)), "Metà base: %d m; h = √(%d² − %d²) = <b>%d m</b>." % (a, c, a, b))
    if k == "aiuola":
        a, b, c = terna(40)
        return M("Un’aiuola ha la forma di un rombo con le diagonali di %d m e %d m. Si mette una bordura tutto intorno. Quanti metri di bordura servono?" % (2 * a, 2 * b), "%d m" % (4 * c), W("%d m" % (2 * (2 * a + 2 * b)), "%d m" % c, "%d m" % (4 * c + 4)), "Lato: √(%d² + %d²) = %d m; perimetro: 4 × %d = <b>%d m</b>." % (a, b, c, c, 4 * c))
    if k == "cornice":
        a, b, c = R.choice([(30, 40, 50), (24, 32, 40), (36, 48, 60), (45, 60, 75)])
        return M("Una cornice rettangolare deve avere una barra di rinforzo lungo la diagonale. La cornice misura %d cm × %d cm. Quanto è lunga la barra?" % (b, a), cm(c), W(cm(a + b), cm(b - a), cm(c + 5)), "√(%d² + %d²) = √%s = <b>%s</b>." % (b, a, num(c * c), cm(c)))
    a, b, c = terna(40)
    return M("Un giardino rettangolare ha la diagonale di %d m e un lato di %d m. Calcola l’area." % (c, a), "%s m²" % num(a * b), W("%s m²" % num(a * c), "%s m²" % num(2 * (a + b)), "%s m²" % num(a * b // 2) if a * b % 2 == 0 else None, "%s m²" % num(c * c)),
             "Altro lato: √(%d² − %d²) = %d m; A = %d × %d = <b>%s m²</b>." % (c, a, b, a, b, num(a * b)))


def main():
    seen = set()
    sets = [
        ("Rettangolo e quadrato", mix(R, seen, [(s1_rett, 12), (s1_quad, 8)])),
        ("Triangolo isoscele ed equilatero", mix(R, seen, [(s2_isoscele, 12), (s2_equi, 8)])),
        ("Rombo e trapezio", mix(R, seen, [(s3_rombo, 10), (s3_trapezio, 10)])),
        ("Distanza tra due punti", mix(R, seen, [(s4_distanza, 20)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = L(["In molte figure si trova un <b>triangolo rettangolo</b> nascosto: lo si individua e si applica il teorema di Pitagora.",
              "Rettangolo: la diagonale è l’ipotenusa, base e altezza sono i cateti. Quadrato: d = l × √2 ≈ l × 1,414.",
              "Triangolo isoscele: l’altezza divide la base a metà. Triangolo equilatero: h ≈ l × 0,866.",
              "Rombo: le diagonali si tagliano a metà e sono perpendicolari: il lato è l’ipotenusa con cateti D/2 e d/2.",
              "Trapezio: la proiezione del lato obliquo è la differenza delle basi (rettangolo) o la sua metà (isoscele)."],
             [("Rombo con diagonali 16 cm e 12 cm", ["metà: 8 cm e 6 cm", "√(64 + 36)"], "lato 10 cm")],
             [["Usare le diagonali intere nel rombo", "Si usano le metà delle diagonali."],
              ["Usare la base intera nel triangolo isoscele", "L’altezza cade a metà della base."],
              ["Nel trapezio isoscele non dividere per 2", "Proiezione = (B − b) : 2."]],
             table(["Figura", "Triangolo rettangolo", "Ipotenusa"], [["rettangolo", "b, h", "diagonale"], ["triangolo isoscele", "base/2, h", "lato obliquo"], ["rombo", "D/2, d/2", "lato"], ["trapezio isoscele", "(B − b)/2, h", "lato obliquo"]]))
    faq = [("Come si calcola la distanza tra due punti del piano cartesiano?", "Si calcolano le differenze delle ascisse e delle ordinate: sono i cateti di un triangolo rettangolo; la distanza è l’ipotenusa."),
           ("Da dove viene 0,866 nel triangolo equilatero?", "Con Pitagora: h = √(l² − (l/2)²) = l × √3 : 2 ≈ l × 0,866.")]
    unit(G, R, "applicazioni-del-teorema-di-pitagora", "S",
         "Conoscere il teorema di Pitagora e le sue applicazioni in matematica e in situazioni concrete; calcolare perimetri e aree di figure piane",
         "Applicazioni del teorema di Pitagora", "Applicazioni di Pitagora",
         "Schede di matematica per la seconda media sulle applicazioni del teorema di Pitagora: diagonale di rettangolo e quadrato, triangolo isoscele ed equilatero, rombo, trapezio, distanza tra due punti e problemi. 100 esercizi con soluzioni.",
         "Trova il triangolo rettangolo nascosto nella figura.", "Rombo: metà delle diagonali. Isoscele: metà della base.",
         body, faq, sets, 9)


if __name__ == "__main__":
    main()
