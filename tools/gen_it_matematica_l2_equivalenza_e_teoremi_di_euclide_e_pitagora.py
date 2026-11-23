# -*- coding: utf-8 -*-
"""
Italia Matematica seconda liceo: Equivalenza delle superfici, teoremi di Euclide e di Pitagora (Geometria)
  python3 tools/gen_it_matematica_l2_equivalenza_e_teoremi_di_euclide_e_pitagora.py
Poligoni equivalenti (parallelogramma e rettangolo, triangolo, trapezio, rombo), teorema di Pitagora e inverso,
primo e secondo teorema di Euclide, altezza relativa all’ipotenusa, triangoli con angoli di 45° e di 30° e 60°.
Errori: primo teorema con il cateto sbagliato, altezza² = somma delle proiezioni, ipotenusa² = c₁ + c₂.
"""
import math
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, d, figure, simp_root

R = random.Random(72210)
G = "seconda-liceo"
TRIPLE = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 16, 20), (7, 24, 25), (15, 20, 25), (20, 21, 29), (9, 40, 41)]


def rt(n):
    k, m = simp_root(n)
    return str(k) if m == 1 else ("" if k == 1 else str(k)) + "√" + str(m)


def rfig(lab=("a", "b", "c")):
    return figure({"A": (0, 0), "B": (4, 0), "C": (0, 3)}, [("A", "B"), ("B", "C"), ("C", "A")], sides=[("A", "B", lab[0]), ("C", "A", lab[1]), ("B", "C", lab[2])], right=[("A", "B", "C")], W=260, H=180, label="triangolo rettangolo ABC")


def s1_pit():
    a, b, c = R.choice(TRIPLE)
    k = R.choice([1, 1, 2])
    a, b, c = a * k, b * k, c * k
    if R.random() < 0.5:
        return M("%sI cateti di un triangolo rettangolo misurano %d cm e %d cm. Quanto misura l’ipotenusa?" % (rfig(("%d cm" % b, "%d cm" % a, "?")), a, b), "%d cm" % c, ["%s cm" % x for x in W(a + b, c + 1, rt(a * a + b * b + 1) if False else c - 1, abs(b - a) * 3)],
                 "i = √(%d² + %d²) = √%d = <b>%d cm</b>." % (a, b, c * c, c))
    return M("%sUn triangolo rettangolo ha ipotenusa %d cm e un cateto di %d cm. Quanto misura l’altro cateto?" % (rfig(("?", "%d cm" % a, "%d cm" % c)), c, a), "%d cm" % b, ["%s cm" % x for x in W(c - a, rt(c * c + a * a), c + a, b + 1)],
             "c = √(%d² − %d²) = √%d = <b>%d cm</b>." % (c, a, b * b, b))


def s1_irr():
    a, b = R.randint(1, 9), R.randint(1, 9)
    n = a * a + b * b
    if math.isqrt(n) ** 2 == n:
        return None
    ans = rt(n)
    return M("I cateti di un triangolo rettangolo misurano %d cm e %d cm. Quanto misura l’ipotenusa (in forma esatta)?" % (a, b), "%s cm" % ans, ["%s cm" % x for x in (str(a + b), rt(abs(a * a - b * b)) if a != b else "2√%d" % a, rt(n + 2))],
             "i = √(%d + %d) = √%d = <b>%s cm</b>." % (a * a, b * b, n, ans))


def s1_inv():
    a, b, c = R.choice(TRIPLE)
    ok = R.random() < 0.5
    if not ok:
        c += R.choice([1, -1, 2])
    ans = "sì" if a * a + b * b == c * c else "no"
    return M("Un triangolo ha i lati di %d cm, %d cm e %d cm. È rettangolo?" % (a, b, c), ans, ["no" if ans == "sì" else "sì", "solo se è isoscele", "non si può stabilire senza gli angoli"],
             "Inverso del teorema di Pitagora: %d² + %d² = %d e %d² = %d. %s: <b>%s</b>." % (a, b, a * a + b * b, c, c * c, "Sono uguali" if ans == "sì" else "Sono diversi", ans))


def efig():
    return figure({"A": (0, 0), "B": (5, 0), "C": (1.8, 2.4), "H": (1.8, 0)}, [("A", "B"), ("B", "C"), ("C", "A")], right=[("C", "A", "B"), ("H", "B", "C")], dashed=[("C", "H")], W=280, H=180, label="triangolo rettangolo in C con l’altezza CH")


def s2_euclide1():
    a, b, c = R.choice(TRIPLE)
    if R.random() < 0.5:
        a, b = b, a
    kk = R.choice([1, 2, 3])
    a, b, c = a * kk, b * kk, c * kk
    # cateto a, ipotenusa c: proiezione = a²/c
    p = Fr(a * a, c)
    try:
        d(p)
    except ValueError:
        return None
    k = R.choice(["proi", "cat"])
    if k == "proi":
        return M("%sNel triangolo rettangolo ABC (retto in C) il cateto AC misura %d cm e l’ipotenusa AB %d cm. Quanto misura la proiezione AH di AC sull’ipotenusa?" % (efig(), a, c), "%s cm" % d(p), ["%s cm" % d(x) for x in W(Fr(b * b, c), Fr(a, c) * a + 1, c - a, Fr(c * c, a))],
                 "Primo teorema di Euclide: AC² = AB · AH → AH = %d² : %d = <b>%s cm</b>." % (a, c, d(p)))
    if p.denominator != 1:
        return None
    return M("%sNel triangolo rettangolo ABC (retto in C) l’ipotenusa AB misura %d cm e la proiezione AH del cateto AC misura %s cm. Quanto misura AC?" % (efig(), c, d(p)), "%d cm" % a, ["%s cm" % x for x in W(rt(int(c * c - p * p)) if (c * c - p * p).denominator == 1 else None, str(c - int(p)), rt(int(c + p)))],
             "AC² = AB · AH = %d · %s = %d → <b>AC = %d cm</b>." % (c, d(p), a * a, a))


def s2_euclide2():
    p, q = R.choice([(4, 9), (1, 4), (4, 16), (9, 16), (2, 8), (3, 12), (1, 9), (4, 25), (16, 9), (8, 18), (5, 20)])
    h = math.isqrt(p * q)
    if h * h != p * q:
        return None
    if R.random() < 0.6:
        return M("%sLe proiezioni dei cateti sull’ipotenusa misurano AH = %d cm e HB = %d cm. Quanto misura l’altezza CH?" % (efig(), p, q), "%d cm" % h, ["%s cm" % (d(x) if not isinstance(x, str) else x) for x in W(Fr(p + q, 2), p + q, rt(p * p + q * q), h + 1)],
                 "Secondo teorema di Euclide: CH² = AH · HB = %d · %d = %d → <b>CH = %d cm</b>." % (p, q, p * q, h))
    return M("%sL’altezza CH relativa all’ipotenusa misura %d cm e la proiezione AH misura %d cm. Quanto misura HB?" % (efig(), h, p), "%d cm" % q, ["%s cm" % fq(x) for x in W(h - p if h > p else h + p, h * h * p, Fr(p, h * h), h + p)],
             "CH² = AH · HB → HB = %d² : %d = <b>%d cm</b>." % (h, p, q))


def s3_alt():
    a, b, c = R.choice(TRIPLE)
    kk = R.choice([1, 2, 3, 4])
    a, b, c = a * kk, b * kk, c * kk
    h = Fr(a * b, c)
    try:
        d(h)
    except ValueError:
        return None
    return M("Un triangolo rettangolo ha i cateti di %d cm e %d cm. Quanto misura l’altezza relativa all’ipotenusa?" % (a, b), "%s cm" % d(h), ["%s cm" % d(x) for x in W(Fr(a + b, 2), Fr(c, 2), Fr(a * b, 2), Fr(a * a, c))],
             "L’area è %d · %d : 2 = %d cm²; ipotenusa %d cm; h = 2 · area : ipotenusa = %d : %d = <b>%s cm</b>." % (a, b, a * b // 2 if a * b % 2 == 0 else 0, c, a * b, c, d(h)) if a * b % 2 == 0 else
             "h = c<sub>1</sub> · c<sub>2</sub> : i = %d · %d : %d = <b>%s cm</b>." % (a, b, c, d(h)))


def s3_spec():
    k = R.choice(["quad", "equi", "3060"])
    l = R.randint(2, 12)
    if k == "quad":
        return M("Quanto misura la diagonale di un quadrato di lato %d cm?" % l, "%d√2 cm" % l if l > 1 else "√2 cm", ["%d cm" % (2 * l), "%d√3 cm" % l, "%d cm" % (l * l * 2)],
                 "Diagonale = lato · √2 (triangolo rettangolo isoscele): <b>%d√2 cm</b>." % l)
    if k == "equi":
        ans = ("%d√3" % (l // 2) if l % 2 == 0 else "%s√3" % fq(Fr(l, 2)).replace("<span class='fr'><span class='fn'>", "").replace("</span><span class='fd'>", "/").replace("</span></span>", "")) + " cm"
        if l % 2:
            ans = "<span class='fr'><span class='fn'>%d√3</span><span class='fd'>2</span></span> cm" % l
        if l == 2:
            ans = "√3 cm"
        return M("Quanto misura l’altezza di un triangolo equilatero di lato %d cm?" % l, ans, ["%d√3 cm" % l, "%d√2 cm" % l, "%s cm" % d(Fr(l, 2))],
                 "Altezza = lato · √3/2 (metà di un triangolo equilatero è un triangolo 30°–60°–90°): <b>%s</b>." % ans)
    return M("In un triangolo rettangolo con un angolo di 30°, l’ipotenusa misura %d cm. Quanto misura il cateto opposto all’angolo di 30°?" % (2 * l), "%d cm" % l, ["%d√3 cm" % l, "%d√2 cm" % l, "%d cm" % (2 * l)],
             "È metà di un triangolo equilatero: il cateto opposto a 30° è metà dell’ipotenusa, <b>%d cm</b>." % l)


def s4_equiv():
    k = R.choice(["par", "tri", "trap", "rombo"])
    a, b = R.randint(3, 16), R.randint(3, 16)
    if k == "par":
        return M("Un parallelogramma ha base %d cm e altezza %d cm. Quale rettangolo è equivalente (stessa area)?" % (a, b), "base %d cm e altezza %d cm" % (a, b), ["base %d cm e altezza %d cm" % (a, b + 2), "base %d cm e altezza %d cm" % (2 * a, 2 * b), "base %d cm e altezza %s cm" % (a, d(Fr(b, 2)))],
                 "Parallelogramma e rettangolo con la stessa base e la stessa altezza sono equivalenti: area %d cm², <b>base %d cm e altezza %d cm</b>." % (a * b, a, b))
    if k == "tri":
        return M("Un triangolo ha base %d cm e altezza %d cm. Quanto misura la sua area?" % (a, b), "%s cm²" % d(Fr(a * b, 2)), ["%d cm²" % (a * b), "%d cm²" % (a + b), "%s cm²" % d(Fr(a * b, 4)), "%d cm²" % (2 * a * b)],
                 "Un triangolo è equivalente a metà del parallelogramma con stessa base e altezza: %d · %d : 2 = <b>%s cm²</b>." % (a, b, d(Fr(a * b, 2))))
    if k == "trap":
        c = R.randint(2, a + 5)
        h = R.randint(2, 10)
        A = Fr((a + c) * h, 2)
        return M("Un trapezio ha le basi di %d cm e %d cm e l’altezza di %d cm. Quanto misura la sua area?" % (a + 5, c, h), "%s cm²" % d(Fr((a + 5 + c) * h, 2)), ["%d cm²" % ((a + 5 + c) * h), "%d cm²" % ((a + 5) * c * h // 2 if (a + 5) * c * h % 2 == 0 else (a + 5) * h), "%s cm²" % d(Fr((a + 5 - c) * h, 2))],
                 "Il trapezio è equivalente a un triangolo con base B + b: (%d + %d) · %d : 2 = <b>%s cm²</b>." % (a + 5, c, h, d(Fr((a + 5 + c) * h, 2))))
    return M("Un rombo ha le diagonali di %d cm e %d cm. Quanto misura la sua area?" % (a, b), "%s cm²" % d(Fr(a * b, 2)), ["%d cm²" % (a * b), "%d cm²" % (2 * (a + b)), "%s cm²" % d(Fr(a * b, 4))],
             "Il rombo è equivalente a metà del rettangolo che ha per lati le diagonali: %d · %d : 2 = <b>%s cm²</b>." % (a, b, d(Fr(a * b, 2))))


def s5_probl():
    a, b, c = R.choice(TRIPLE)
    k = R.choice(["rett", "rombo", "iso"])
    if k == "rett":
        return M("Un rettangolo ha i lati di %d cm e %d cm. Quanto misura la diagonale?" % (a, b), "%d cm" % c, ["%s cm" % x for x in W(a + b, c + 1, 2 * c, abs(b - a) + c)],
                 "La diagonale è l’ipotenusa: √(%d² + %d²) = <b>%d cm</b>." % (a, b, c))
    if k == "rombo":
        return M("Un rombo ha le diagonali di %d cm e %d cm. Quanto misura il lato?" % (2 * a, 2 * b), "%d cm" % c, ["%s cm" % x for x in W(a + b, 2 * c, c + 1, 2 * a + 2 * b)],
                 "Le diagonali si tagliano a metà e sono perpendicolari: lato = √(%d² + %d²) = <b>%d cm</b>." % (a, b, c))
    return M("Un triangolo isoscele ha la base di %d cm e i lati obliqui di %d cm. Quanto misura l’altezza relativa alla base?" % (2 * a, c), "%d cm" % b, ["%s cm" % x for x in W(c - a, rt(c * c + a * a), b + 1, 2 * b)],
             "L’altezza cade nel punto medio della base: √(%d² − %d²) = <b>%d cm</b>." % (c, a, b))


def main():
    seen = set()
    sets = [
        ("Equivalenza delle superfici", mix(R, seen, [(s4_equiv, 20)])),
        ("Teorema di Pitagora", mix(R, seen, [(s1_pit, 10), (s1_irr, 5), (s1_inv, 5)])),
        ("Primo teorema di Euclide", mix(R, seen, [(s2_euclide1, 16), (s3_alt, 4)])),
        ("Secondo teorema di Euclide", mix(R, seen, [(s2_euclide2, 14), (s3_alt, 6)])),
        ("Triangoli particolari e problemi", mix(R, seen, [(s3_spec, 10), (s5_probl, 10)])),
    ]
    body = L(["Due figure sono <b>equivalenti</b> se hanno la stessa area. Parallelogramma e rettangolo con stessa base e altezza sono equivalenti; un triangolo è equivalente a metà di un parallelogramma.",
              "<b>Pitagora</b>: in un triangolo rettangolo i² = c<sub>1</sub>² + c<sub>2</sub>². Vale anche l’inverso: se i lati verificano la relazione, il triangolo è rettangolo.",
              "<b>Primo teorema di Euclide</b>: il quadrato di un cateto è uguale al prodotto dell’ipotenusa per la proiezione del cateto sull’ipotenusa (AC² = AB · AH).",
              "<b>Secondo teorema di Euclide</b>: il quadrato dell’altezza relativa all’ipotenusa è uguale al prodotto delle proiezioni dei cateti (CH² = AH · HB)."],
             [("Cateto 6, ipotenusa 10: proiezione del cateto", ["36 = 10 · AH"], "AH = 3,6"),
              ("Proiezioni 4 e 9: altezza", ["CH² = 36"], "CH = 6")],
             [["AC² = AB · HB", "Si usa la proiezione dello <b>stesso</b> cateto: AC² = AB · AH."],
              ["CH² = AH + HB", "È il prodotto: CH² = AH · HB."],
              ["i = c<sub>1</sub> + c<sub>2</sub>", "i = √(c<sub>1</sub>² + c<sub>2</sub>²)."]])
    faq = [("Che cosa vuol dire equivalente in geometria?", "Due figure equivalenti hanno la stessa estensione (la stessa area), anche se hanno forme diverse. Figure congruenti sono sempre equivalenti, il contrario no."),
           ("Come si ricava il teorema di Pitagora dal primo teorema di Euclide?", "Sommando AC² = AB · AH e BC² = AB · HB si ottiene AC² + BC² = AB · (AH + HB) = AB².")]
    unit(G, R, "equivalenza-e-teoremi-di-euclide-e-pitagora", "G",
         "Equivalenza delle figure piane; teoremi di Euclide e di Pitagora",
         "Equivalenza, teoremi di Euclide e di Pitagora", "Teoremi di Euclide e di Pitagora",
         "Schede di matematica per la seconda liceo su equivalenza e teoremi di Euclide e di Pitagora: aree di parallelogramma, triangolo, trapezio e rombo, teorema di Pitagora e inverso, primo e secondo teorema di Euclide, triangoli particolari. 100 esercizi con soluzioni.",
         "AC² = AB · AH e CH² = AH · HB", "Primo teorema: cateto e sua proiezione. Secondo teorema: altezza e proiezioni.",
         body, faq, sets, 10)


if __name__ == "__main__":
    main()
