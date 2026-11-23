# -*- coding: utf-8 -*-
"""
Italia Matematica seconda liceo: Parallelogrammi e trapezi (Geometria)
  python3 tools/gen_it_matematica_l2_parallelogrammi_e_trapezi.py
Proprietà del parallelogramma (lati e angoli opposti, angoli consecutivi supplementari, diagonali che si dividono a metà),
rettangolo, rombo e quadrato (proprietà delle diagonali), trapezio e trapezio isoscele, teorema del segmento dei punti medi,
fascio di rette parallele (piccolo teorema di Talete), riconoscere i quadrilateri.
Errori: angoli consecutivi congruenti, diagonali del rombo congruenti, segmento dei punti medi uguale al terzo lato.
"""
import random
from it_liceo import M, L, unit, mix, table, W, fq, figure, d
from fractions import Fraction as Fr

R = random.Random(72208)
G = "seconda-liceo"


def para_fig(lab="ABCD"):
    pts = {lab[0]: (0, 0), lab[1]: (5, 0), lab[2]: (6.6, 2.6), lab[3]: (1.6, 2.6)}
    return figure(pts, [(lab[0], lab[1]), (lab[1], lab[2]), (lab[2], lab[3]), (lab[3], lab[0])], W=280, H=160, label="parallelogramma ABCD")


def s1_ang():
    a = R.randint(35, 85)
    fig = para_fig()
    k = R.choice(["B", "C", "D"])
    v = {"B": 180 - a, "C": a, "D": 180 - a}[k]
    return M("%sNel parallelogramma ABCD l’angolo A misura %d°. Quanto misura l’angolo %s?" % (fig, a, k), "%d°" % v, ["%d°" % x for x in (180 - v, 90 - a if 90 - a != v else 360 - v, 360 - 2 * a if 360 - 2 * a != v else v + 10)],
             "Angoli opposti congruenti, angoli consecutivi supplementari: l’angolo %s misura <b>%d°</b>." % (k, v))


def s1_lati():
    a, b = R.randint(3, 15), R.randint(3, 15)
    per = 2 * (a + b)
    k = R.choice(["per", "lato"])
    if k == "per":
        return M("Un parallelogramma ha i lati consecutivi di %d cm e %d cm. Quanto misura il perimetro?" % (a, b), "%d cm" % per, ["%d cm" % x for x in (a + b, a * b, 4 * a)],
                 "I lati opposti sono congruenti: 2 · (%d + %d) = <b>%d cm</b>." % (a, b, per))
    return M("Un parallelogramma ha perimetro %d cm e un lato di %d cm. Quanto misura il lato consecutivo?" % (per, a), "%d cm" % b, ["%s cm" % x for x in W(per - a, per // 2, per // 4 if per // 4 != b else b + 1, per - 2 * a)],
             "%d : 2 − %d = <b>%d cm</b>." % (per, a, b))


def s1_diag():
    a, b = R.randint(4, 20), R.randint(4, 20)
    if a == b:
        return None
    k = R.choice(["AO", "BO"])
    v = Fr(a, 2) if k == "AO" else Fr(b, 2)
    return M("Le diagonali di un parallelogramma ABCD misurano AC = %d cm e BD = %d cm e si incontrano in O. Quanto misura %s?" % (a, b, k), "%s cm" % d(v), ["%s cm" % d(x) for x in (Fr(a + b, 2) if Fr(a + b, 2) != v else a + b, a if k == "AO" else b, Fr(b, 2) if k == "AO" else Fr(a, 2))],
             "Le diagonali del parallelogramma si dividono scambievolmente a metà: %s = <b>%s cm</b>." % (k, d(v)))


PROP = [("Le diagonali sono congruenti", "rettangolo", ["rombo", "parallelogramma qualsiasi", "trapezio scaleno"]),
        ("Le diagonali sono perpendicolari e bisettrici degli angoli", "rombo", ["rettangolo", "parallelogramma qualsiasi", "trapezio isoscele"]),
        ("Le diagonali sono congruenti e perpendicolari", "quadrato", ["rettangolo", "rombo", "trapezio isoscele"]),
        ("Ha una sola coppia di lati paralleli", "trapezio", ["parallelogramma", "rombo", "rettangolo"]),
        ("Ha i lati obliqui congruenti e gli angoli alla base congruenti", "trapezio isoscele", ["trapezio rettangolo", "parallelogramma", "rombo"]),
        ("Ha quattro angoli retti ma i lati consecutivi diversi", "rettangolo", ["quadrato", "rombo", "trapezio rettangolo"]),
        ("Ha quattro lati congruenti ma non ha angoli retti", "rombo", ["quadrato", "rettangolo", "trapezio isoscele"]),
        ("Ha due lati paralleli e uno dei lati obliqui perpendicolare alle basi", "trapezio rettangolo", ["rettangolo", "trapezio isoscele", "parallelogramma"])]


def s2_quad():
    p, a, w = R.choice(PROP)
    return M("Quale quadrilatero ha questa proprietà? «%s»." % p, a, w, "È la proprietà caratteristica del <b>%s</b>." % a)


VF = [("Ogni quadrato è un rombo.", "vero"), ("Ogni rombo è un quadrato.", "falso"), ("Ogni rettangolo è un parallelogramma.", "vero"),
      ("Ogni parallelogramma è un rettangolo.", "falso"), ("Un parallelogramma con le diagonali congruenti è un rettangolo.", "vero"),
      ("Un parallelogramma con le diagonali perpendicolari è un rombo.", "vero"), ("Le diagonali di un trapezio isoscele sono congruenti.", "vero"),
      ("Le diagonali di un rombo sono congruenti.", "falso"), ("In un parallelogramma gli angoli consecutivi sono congruenti.", "falso"),
      ("Un quadrilatero con i lati opposti congruenti è un parallelogramma.", "vero"), ("Ogni trapezio ha due coppie di lati paralleli.", "falso"),
      ("Un rettangolo con le diagonali perpendicolari è un quadrato.", "vero")]


def s2_vf():
    t, v = R.choice(VF)
    return M("Vero o falso? %s" % t, v, ["falso" if v == "vero" else "vero", "dipende dalle misure", "solo nel piano cartesiano"],
             "%s: <b>%s</b>." % (t.rstrip("."), v))


def s3_trap():
    k = R.choice(["iso", "rett"])
    a = R.randint(40, 80)
    if k == "iso":
        t = R.choice(["base", "sup"])
        if t == "base":
            return M("In un trapezio isoscele un angolo alla base maggiore misura %d°. Quanto misura l’altro angolo alla base maggiore?" % a, "%d°" % a, ["%d°" % (180 - a), "%d°" % (90 - a), "%d°" % (360 - 2 * a)],
                     "Nel trapezio isoscele gli angoli adiacenti a ciascuna base sono congruenti: <b>%d°</b>." % a)
        return M("In un trapezio isoscele un angolo alla base maggiore misura %d°. Quanto misura ciascun angolo alla base minore?" % a, "%d°" % (180 - a), ["%d°" % a, "%d°" % (90 + a // 2), "%d°" % (360 - a)],
                 "Gli angoli adiacenti a un lato obliquo sono supplementari: 180° − %d° = <b>%d°</b>." % (a, 180 - a))
    return M("In un trapezio rettangolo l’angolo acuto misura %d°. Quanto misura l’angolo ottuso?" % a, "%d°" % (180 - a), ["%d°" % (90 + a), "%d°" % (90 - a + 90 if False else 270 - a), "%d°" % (360 - 2 * a - 90)],
             "Due angoli sono retti; l’angolo ottuso è supplementare all’acuto (stesso lato obliquo): <b>%d°</b>." % (180 - a))


def s4_medi():
    c = R.randint(6, 30)
    k = R.choice(["tri", "trap"])
    if k == "tri":
        fig = figure({"A": (0, 0), "B": (6, 0), "C": (2, 4), "M": (1, 2), "N": (4, 2)}, [("A", "B"), ("B", "C"), ("C", "A"), ("M", "N")], W=260, H=170, label="triangolo con il segmento dei punti medi", ticks=[("A", "M", 1), ("M", "C", 1), ("C", "N", 2), ("N", "B", 2)])
        return M("%sM e N sono i punti medi dei lati AC e BC del triangolo ABC e AB = %d cm. Quanto misura MN?" % (fig, c), "%s cm" % d(Fr(c, 2)), ["%d cm" % c, "%s cm" % d(Fr(c, 3)), "%d cm" % (2 * c)],
                 "Il segmento che unisce i punti medi di due lati è parallelo al terzo lato e ne è la <b>metà</b>: %s cm." % d(Fr(c, 2)))
    B, b = R.randint(10, 30), R.randint(4, 9)
    v = Fr(B + b, 2)
    return M("Un trapezio ha le basi di %d cm e %d cm. Quanto misura il segmento che unisce i punti medi dei lati obliqui?" % (B, b), "%s cm" % d(v), ["%s cm" % d(x) for x in (Fr(B - b, 2), B + b, Fr(B, 2))],
             "La congiungente dei punti medi dei lati obliqui è la semisomma delle basi: (%d + %d) : 2 = <b>%s cm</b>." % (B, b, d(v)))


def s5_talete():
    a, b = R.randint(2, 8), R.randint(2, 8)
    k = R.choice([2, 3, Fr(3, 2), Fr(5, 2)])
    A_, B_ = a * k, b * k
    if A_.denominator != 1 if isinstance(A_, Fr) else False:
        return None
    ans = d(Fr(B_))
    return M("Un fascio di rette parallele taglia due trasversali. Sulla prima i segmenti AB e BC misurano %d cm e %d cm; sulla seconda il segmento corrispondente ad AB misura %s cm. Quanto misura il corrispondente di BC?" % (a, b, d(Fr(A_))),
             "%s cm" % ans, ["%s cm" % d(x) for x in W(Fr(b), Fr(A_) + b - a, Fr(a * b, A_ if A_ else 1), Fr(B_) + 1)],
             "Teorema di Talete: i segmenti corrispondenti sono proporzionali, %d : %d = %s : x → <b>x = %s cm</b>." % (a, b, d(Fr(A_)), ans))


def s5_probl():
    a = R.randint(4, 15)
    k = R.choice(["rombo", "rett"])
    if k == "rombo":
        per = 4 * a
        return M("Un rombo ha il perimetro di %d cm. Quanto misura ciascun lato?" % per, "%d cm" % a, ["%d cm" % x for x in (per // 2, per - a, 2 * a)], "Il rombo ha i quattro lati congruenti: %d : 4 = <b>%d cm</b>." % (per, a))
    b = R.randint(2, 10)
    dd = R.randint(1, 6)
    per = 2 * (b + b + dd)
    return M("In un rettangolo la base supera l’altezza di %d cm e il perimetro è %d cm. Quanto misura la base?" % (dd, per), "%d cm" % (b + dd), ["%s cm" % x for x in W(b, per // 4, per // 2 - b, per // 2, b + 2 * dd)],
             "2(h + h + %d) = %d → h = %d: la base è <b>%d cm</b>." % (dd, per, b, b + dd))


def main():
    seen = set()
    sets = [
        ("Angoli e lati del parallelogramma", mix(R, seen, [(s1_ang, 10), (s1_lati, 10)])),
        ("Diagonali e quadrilateri particolari", mix(R, seen, [(s1_diag, 12), (s2_quad, 8)])),
        ("Vero o falso", mix(R, seen, [(s2_vf, 12), (s3_trap, 8)])),
        ("Trapezi e punti medi", mix(R, seen, [(s3_trap, 8), (s4_medi, 12)])),
        ("Talete e problemi", mix(R, seen, [(s5_talete, 10), (s5_probl, 10)])),
    ]
    body = L(["Un <b>parallelogramma</b> ha i lati opposti paralleli. Allora: lati opposti congruenti, angoli opposti congruenti, angoli consecutivi supplementari, diagonali che si tagliano a metà.",
              "<b>Rettangolo</b>: diagonali congruenti. <b>Rombo</b>: diagonali perpendicolari e bisettrici degli angoli. <b>Quadrato</b>: tutte e due le proprietà.",
              "Il <b>trapezio</b> ha una sola coppia di lati paralleli (le basi). Nel trapezio isoscele gli angoli adiacenti a ciascuna base sono congruenti e le diagonali sono congruenti.",
              "Il segmento che unisce i punti medi di due lati di un triangolo è parallelo al terzo lato e ne è la metà. Un fascio di parallele taglia su due trasversali segmenti proporzionali (Talete)."],
             [("Parallelogramma con A = 70°", ["B = 180° − 70°", "C = A"], "B = D = 110°, C = 70°"),
              ("Trapezio con basi 18 e 10", ["(18 + 10) : 2"], "congiungente dei punti medi: 14")],
             [["Angoli consecutivi congruenti", "Sono supplementari: la somma è 180°."],
              ["Diagonali del rombo congruenti", "Sono perpendicolari; congruenti solo nel quadrato."],
              ["MN = AB", "Il segmento dei punti medi è la metà del terzo lato."]])
    faq = [("Un quadrato è un rettangolo?", "Sì: ha quattro angoli retti, quindi è un rettangolo particolare. È anche un rombo, perché ha quattro lati congruenti."),
           ("Come si dimostra che un quadrilatero è un parallelogramma?", "Basta una di queste condizioni: lati opposti congruenti, oppure angoli opposti congruenti, oppure diagonali che si dividono a metà, oppure due lati opposti paralleli e congruenti.")]
    unit(G, R, "parallelogrammi-e-trapezi", "G",
         "Parallelogrammi e trapezi: proprietà e criteri; teorema del segmento dei punti medi; teorema di Talete per il fascio di parallele",
         "Parallelogrammi e trapezi", "Parallelogrammi e trapezi",
         "Schede di matematica per la seconda liceo su parallelogrammi e trapezi: angoli, lati e diagonali del parallelogramma, rettangolo, rombo e quadrato, trapezio isoscele, segmento dei punti medi, fascio di parallele. 100 esercizi con soluzioni.",
         "Angoli consecutivi supplementari, diagonali divise a metà.", "Rettangolo: diagonali congruenti. Rombo: diagonali perpendicolari.",
         body, faq, sets, 8)


if __name__ == "__main__":
    main()
