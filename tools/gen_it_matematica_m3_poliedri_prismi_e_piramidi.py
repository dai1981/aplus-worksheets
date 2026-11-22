# -*- coding: utf-8 -*-
"""
Italia Matematica terza media: Poliedri, prismi e piramidi (Spazio e figure)
  python3 tools/gen_it_matematica_m3_poliedri_prismi_e_piramidi.py
Poliedri (facce, vertici, spigoli, relazione di Eulero), cubo e parallelepipedo (area laterale, totale, volume, diagonale),
prisma retto (Al = 2p × h), piramide retta (Al = p × a : 2, V = Ab × h : 3, apotema con Pitagora), unità di volume e
capacità (1 dm³ = 1 l), peso specifico (P = V × ps).
Errori: V della piramide senza «: 3», usare l’altezza invece dell’apotema nell’area laterale, × 100 invece di × 1000 nei volumi.
"""
import math
import random
from fractions import Fraction as Fr
from it_media import M, L, unit, mix, table, W, d, num, Kids

R = random.Random(71310)
G = "terza-media"
K = Kids(R)
TERNE = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17), (12, 16, 20)]


def u(v, s):
    return "%s %s" % (d(v), s)


def s1_eulero():
    k = R.choice(["quiz", "calc"])
    if k == "quiz":
        nm, F_, V_, S_ = R.choice([("cubo", 6, 8, 12), ("parallelepipedo", 6, 8, 12), ("tetraedro", 4, 4, 6), ("prisma triangolare", 5, 6, 9), ("piramide a base quadrata", 5, 5, 8),
                                    ("prisma pentagonale", 7, 10, 15), ("piramide esagonale", 7, 7, 12), ("prisma esagonale", 8, 12, 18), ("ottaedro", 8, 6, 12), ("piramide pentagonale", 6, 6, 10)])
        what = R.choice(["facce", "vertici", "spigoli"])
        v = {"facce": F_, "vertici": V_, "spigoli": S_}[what]
        return M("Quanti %s ha un %s?" % (what, nm), str(v), W(str(F_), str(V_), str(S_), str(v + 1), str(v - 1)), "Il %s ha %d facce, %d vertici e %d spigoli: <b>%d</b> %s." % (nm, F_, V_, S_, v, what))
    n = R.randint(3, 12)
    kind = R.choice(["prisma", "piramide"])
    F_, V_, S_ = (n + 2, 2 * n, 3 * n) if kind == "prisma" else (n + 1, n + 1, 2 * n)
    miss = R.choice(["F", "V", "S"])
    gv = {"F": F_, "V": V_, "S": S_}
    shown = ", ".join("%s = %d" % (x, gv[x]) for x in "FVS" if x != miss)
    return M("Un poliedro ha %s. Usando la relazione di Eulero (F + V = S + 2), quanto vale %s?" % (shown, miss), str(gv[miss]), W(str(gv[miss] + 2), str(gv[miss] - 2), str(gv[miss] + 4)),
             "F + V = S + 2 → %s = <b>%d</b>." % (miss, gv[miss]))


def s2_parall():
    a, b, c = R.sample(range(2, 16), 3)
    k = R.choice(["V", "At", "Al", "diag", "cubo"])
    if k == "V":
        return M("Calcola il volume di un parallelepipedo con dimensioni %d cm, %d cm e %d cm." % (a, b, c), u(a * b * c, "cm³"), W(u(2 * (a * b + b * c + a * c), "cm³"), u(a + b + c, "cm³"), u(a * b * c // 2, "cm³") if a * b * c % 2 == 0 else u(a * b * c + 1, "cm³"), u(a * b * c * 2, "cm³")),
                 "V = a × b × c = %d × %d × %d = <b>%s cm³</b>." % (a, b, c, num(a * b * c)))
    if k == "At":
        At = 2 * (a * b + b * c + a * c)
        return M("Calcola l’area totale di un parallelepipedo con dimensioni %d cm, %d cm e %d cm." % (a, b, c), u(At, "cm²"), W(u(a * b * c, "cm²"), u(At // 2, "cm²"), u(2 * (a + b) * c, "cm²"), u(At + 2 * a * b, "cm²")),
                 "At = 2(ab + bc + ac) = 2(%d + %d + %d) = <b>%s cm²</b>." % (a * b, b * c, a * c, num(At)))
    if k == "Al":
        return M("Un parallelepipedo ha base %d cm × %d cm e altezza %d cm. Calcola l’area laterale." % (a, b, c), u(2 * (a + b) * c, "cm²"), W(u(2 * (a * b + b * c + a * c), "cm²"), u((a + b) * c, "cm²"), u(a * b * c, "cm²"), u(2 * (a + b) * c + 2 * a * b, "cm²")),
                 "Al = perimetro di base × h = %d × %d = <b>%s cm²</b>." % (2 * (a + b), c, num(2 * (a + b) * c)))
    if k == "diag":
        x, y, z, w = R.choice([(2, 3, 6, 7), (1, 4, 8, 9), (4, 4, 7, 9), (2, 6, 9, 11), (6, 6, 7, 11), (3, 4, 12, 13), (2, 10, 11, 15), (4, 8, 8, 12), (6, 10, 15, 19), (8, 9, 12, 17)])
        return M("Calcola la diagonale di un parallelepipedo con dimensioni %d cm, %d cm e %d cm." % (x, y, z), "%d cm" % w, W("%d cm" % (x + y + z), "%d cm" % (w * w), "%d cm" % (w + 1), "%d cm" % (z + 1) if z + 1 != w else "%d cm" % (z + 2)),
                 "d = √(%d² + %d² + %d²) = √%d = <b>%d cm</b>." % (x, y, z, w * w, w))
    l_ = R.randint(2, 15)
    q = R.choice(["V", "At"])
    if q == "V":
        return M("Calcola il volume di un cubo con spigolo %d cm." % l_, u(l_ ** 3, "cm³"), W(u(6 * l_ * l_, "cm³"), u(3 * l_, "cm³"), u(l_ * l_, "cm³"), u(12 * l_, "cm³")), "V = l³ = %d³ = <b>%s cm³</b>." % (l_, num(l_ ** 3)))
    return M("Calcola l’area totale di un cubo con spigolo %d cm." % l_, u(6 * l_ * l_, "cm²"), W(u(l_ ** 3, "cm²"), u(4 * l_ * l_, "cm²"), u(6 * l_, "cm²"), u(l_ * l_, "cm²")), "At = 6l² = 6 × %d = <b>%s cm²</b>." % (l_ * l_, num(6 * l_ * l_)))


def s3_prisma():
    k = R.choice(["tri", "quad", "esag"])
    h = R.randint(4, 20)
    if k == "tri":
        a, b, c = R.choice(TERNE)
        Ab = Fr(a * b, 2)
        p = a + b + c
        q = R.choice(["Al", "V", "At"])
        base = "un triangolo rettangolo con cateti %d cm e %d cm" % (a, b)
        if q == "Al":
            return M("Un prisma retto ha per base %s e altezza %d cm. Calcola l’area laterale." % (base, h), u(p * h, "cm²"), W(u((a + b) * h, "cm²"), u(Ab * h, "cm²"), u(p * h + 2 * Ab, "cm²"), u(p + h, "cm²")),
                     "Ipotenusa: %d cm; 2p = %d cm; Al = 2p × h = %d × %d = <b>%s cm²</b>." % (c, p, p, h, num(p * h)))
        if q == "V":
            return M("Un prisma retto ha per base %s e altezza %d cm. Calcola il volume." % (base, h), u(Ab * h, "cm³"), W(u(a * b * h, "cm³"), u(Ab * h / 3, "cm³") if (Ab * h / 3 * 10).denominator == 1 else None, u(p * h, "cm³"), u(Ab + h, "cm³")),
                     "Ab = %d × %d : 2 = %s cm²; V = Ab × h = %s × %d = <b>%s cm³</b>." % (a, b, d(Ab), d(Ab), h, d(Ab * h)))
        return M("Un prisma retto ha per base %s e altezza %d cm. Calcola l’area totale." % (base, h), u(p * h + 2 * Ab, "cm²"), W(u(p * h, "cm²"), u(p * h + Ab, "cm²"), u(Ab * h, "cm²"), u((a + b) * h + 2 * Ab, "cm²")),
                 "Al = %d × %d = %d cm²; 2Ab = %s cm²; At = <b>%s cm²</b>." % (p, h, p * h, d(2 * Ab), d(p * h + 2 * Ab)))
    if k == "quad":
        l_ = R.randint(3, 15)
        return M("Un prisma retto a base quadrata ha lo spigolo di base %d cm e l’altezza %d cm. Calcola l’area totale." % (l_, h), u(4 * l_ * h + 2 * l_ * l_, "cm²"), W(u(4 * l_ * h, "cm²"), u(4 * l_ * h + l_ * l_, "cm²"), u(l_ * l_ * h, "cm²"), u(2 * l_ * h + 2 * l_ * l_, "cm²")),
                 "Al = 4 × %d × %d = %d cm²; Ab = %d cm²; At = %d + 2 × %d = <b>%s cm²</b>." % (l_, h, 4 * l_ * h, l_ * l_, 4 * l_ * h, l_ * l_, num(4 * l_ * h + 2 * l_ * l_)))
    l_ = R.randint(2, 10)
    a = l_ * Fr(866, 1000)
    Ab = 6 * l_ * a / 2
    return M("Un prisma retto ha per base un esagono regolare di lato %d cm (apotema = lato × 0,866) e altezza %d cm. Calcola il volume." % (l_, h), u(Ab * h, "cm³"), W(u(6 * l_ * h, "cm³"), u(Ab * h / 3, "cm³"), u(6 * l_ * a * h, "cm³"), u(Ab, "cm³")),
             "a = %s cm; Ab = 2p × a : 2 = %d × %s : 2 = %s cm²; V = %s × %d = <b>%s cm³</b>." % (d(a), 6 * l_, d(a), d(Ab), d(Ab), h, d(Ab * h)))


def s4_piramide():
    k = R.choice(["V", "apot", "Al", "At", "h"])
    a2, h, ap = R.choice(TERNE)
    l_ = 2 * a2
    if k == "V":
        return M("Una piramide retta a base quadrata ha lo spigolo di base %d cm e l’altezza %d cm. Calcola il volume." % (l_, h), u(Fr(l_ * l_ * h, 3), "cm³"), W(u(l_ * l_ * h, "cm³"), u(Fr(l_ * l_ * h, 2), "cm³"), u(Fr(4 * l_ * h, 3), "cm³") if (Fr(4 * l_ * h, 3) * 10).denominator == 1 else u(4 * l_ * h, "cm³"), u(Fr(l_ * h, 3), "cm³") if (Fr(l_ * h, 3) * 10).denominator == 1 else u(l_ * h, "cm³")),
                 "V = Ab × h : 3 = %d × %d : 3 = <b>%s cm³</b>." % (l_ * l_, h, d(Fr(l_ * l_ * h, 3))) ) if (Fr(l_ * l_ * h, 3) * 10).denominator == 1 else None
    if k == "apot":
        return M("Una piramide retta a base quadrata ha lo spigolo di base %d cm e l’altezza %d cm. Quanto misura l’apotema della piramide?" % (l_, h), "%d cm" % ap, W("%d cm" % (h + a2), "%d cm" % int(math.isqrt(l_ * l_ + h * h)) if math.isqrt(l_ * l_ + h * h) ** 2 == l_ * l_ + h * h else "%d cm" % (ap + 2), "%d cm" % (ap + 1), "%d cm" % (h - a2) if h > a2 else "%d cm" % (a2 - h + ap)),
                 "Apotema di base (metà lato): %d cm; apotema = √(%d² + %d²) = <b>%d cm</b>." % (a2, h, a2, ap))
    if k == "Al":
        return M("Una piramide retta a base quadrata ha lo spigolo di base %d cm e l’apotema %d cm. Calcola l’area laterale." % (l_, ap), u(2 * l_ * ap, "cm²"), W(u(4 * l_ * ap, "cm²"), u(l_ * ap, "cm²"), u(2 * l_ * h, "cm²"), u(2 * l_ * ap + l_ * l_, "cm²")),
                 "Al = perimetro di base × apotema : 2 = %d × %d : 2 = <b>%s cm²</b>." % (4 * l_, ap, num(2 * l_ * ap)))
    if k == "At":
        return M("Una piramide retta a base quadrata ha lo spigolo di base %d cm e l’altezza %d cm. Calcola l’area totale." % (l_, h), u(2 * l_ * ap + l_ * l_, "cm²"), W(u(2 * l_ * h + l_ * l_, "cm²"), u(2 * l_ * ap, "cm²"), u(4 * l_ * ap + l_ * l_, "cm²"), u(2 * l_ * ap + 2 * l_ * l_, "cm²")),
                 "Apotema: √(%d² + %d²) = %d cm; Al = %d × %d : 2 = %d cm²; At = %d + %d = <b>%s cm²</b>." % (h, a2, ap, 4 * l_, ap, 2 * l_ * ap, 2 * l_ * ap, l_ * l_, num(2 * l_ * ap + l_ * l_)))
    V = Fr(l_ * l_ * h, 3)
    if V.denominator != 1:
        return None
    return M("Una piramide a base quadrata ha volume %s cm³ e spigolo di base %d cm. Quanto misura l’altezza?" % (num(int(V)), l_), "%d cm" % h, W("%s cm" % d(V / (l_ * l_)), "%d cm" % (h * 3) if h * 3 != h else None, "%s cm" % d(V * 3 / l_) if (V * 3 / l_).denominator == 1 else None, "%d cm" % (h + 1)),
             "h = V × 3 : Ab = %s × 3 : %d = <b>%d cm</b>." % (num(int(V)), l_ * l_, h))


def s5():
    k = R.choice(["acqua", "unita", "peso", "piscina", "scatola"])
    if k == "acqua":
        a, b, c = R.randint(2, 8) * 10, R.randint(2, 6) * 10, R.randint(2, 5) * 10
        V = a * b * c
        return M("Un acquario ha dimensioni interne %d cm × %d cm × %d cm. Quanti litri d’acqua contiene quando è pieno?" % (a, b, c), "%s l" % d(Fr(V, 1000)), W("%s l" % d(Fr(V, 100)), "%s l" % d(Fr(V, 10000)), "%s l" % num(V), "%s l" % d(Fr(V, 2000))),
                 "V = %s cm³ = %s dm³ = <b>%s l</b> (1 dm³ = 1 l)." % (num(V), d(Fr(V, 1000)), d(Fr(V, 1000))))
    if k == "unita":
        v = R.choice([Fr(R.randint(2, 900), 10), Fr(R.randint(1, 99)), Fr(R.randint(101, 999), 100)])
        i = R.choice([("m³", "dm³"), ("dm³", "cm³"), ("cm³", "dm³"), ("m³", "l")])
        f = {("m³", "dm³"): 1000, ("dm³", "cm³"): 1000, ("cm³", "dm³"): Fr(1, 1000), ("dm³", "l"): 1, ("m³", "l"): 1000, ("cm³", "ml"): 1}[i]
        if f == 1:
            return None
        r = v * f
        return M("%s %s = … %s" % (d(v), i[0], i[1]), "%s %s" % (d(r), i[1]), W("%s %s" % (d(v * (100 if f > 1 else Fr(1, 100))), i[1]), "%s %s" % (d(v / f), i[1]), "%s %s" % (d(v * (10 if f > 1 else Fr(1, 10))), i[1])),
                 "Le unità di volume vanno di 1000 in 1000: <b>%s %s</b>." % (d(r), i[1]))
    if k == "peso":
        l_ = R.randint(2, 10)
        ps, mat = R.choice([(Fr(78, 10), "ferro"), (Fr(27, 10), "alluminio"), (Fr(19, 1), "oro"), (Fr(7, 10), "legno"), (Fr(113, 10), "piombo")])
        V = l_ ** 3
        return M("Un cubo di %s ha lo spigolo di %d cm. Il peso specifico del %s è %s g/cm³. Quanto pesa?" % (mat, l_, mat, d(ps)), "%s g" % d(V * ps), W("%s g" % d(6 * l_ * l_ * ps), "%s g" % d(V / ps) if (V / ps * 100).denominator == 1 else None, "%s g" % num(V), "%s g" % d(V * ps * 10)),
                 "V = %d³ = %s cm³; P = V × ps = %s × %s = <b>%s g</b>." % (l_, num(V), num(V), d(ps), d(V * ps)))
    if k == "piscina":
        a, b = R.choice([(25, 10), (20, 8), (12, 6), (50, 20), (15, 8)])
        h = R.choice([Fr(3, 2), Fr(2), Fr(6, 5), Fr(9, 5)])
        V = a * b * h
        return M("Una piscina è lunga %d m, larga %d m e profonda %s m. Quanti litri d’acqua contiene?" % (a, b, d(h)), "%s l" % num(int(V * 1000)), W("%s l" % num(int(V * 100)), "%s l" % d(V), "%s l" % num(int(V * 10000)), "%s l" % num(int(2 * (a * b + b * h + a * h) * 1000)) if (2 * (a * b + b * h + a * h) * 1000).denominator == 1 else None),
                 "V = %d × %d × %s = %s m³ = <b>%s l</b> (1 m³ = 1000 l)." % (a, b, d(h), d(V), num(int(V * 1000))))
    a, b, c = R.randint(10, 40), R.randint(10, 30), R.randint(5, 20)
    return M("Per costruire una scatola chiusa a forma di parallelepipedo (%d cm × %d cm × %d cm) quanto cartone serve, senza sprechi?" % (a, b, c), u(2 * (a * b + b * c + a * c), "cm²"), W(u(a * b * c, "cm²"), u(a * b + b * c + a * c, "cm²"), u(2 * (a + b) * c, "cm²"), u(2 * (a * b + b * c + a * c) - a * b, "cm²")),
             "Serve l’area totale: 2(%d + %d + %d) = <b>%s cm²</b>." % (a * b, b * c, a * c, num(2 * (a * b + b * c + a * c))))


def main():
    seen = set()
    sets = [
        ("Poliedri e relazione di Eulero", mix(R, seen, [(s1_eulero, 20)])),
        ("Cubo e parallelepipedo", mix(R, seen, [(s2_parall, 20)])),
        ("Prismi", mix(R, seen, [(s3_prisma, 20)])),
        ("Piramidi", mix(R, seen, [(s4_piramide, 20)])),
        ("Volume, capacità e peso", mix(R, seen, [(s5, 20)])),
    ]
    body = L(["Un <b>poliedro</b> è un solido limitato da poligoni (facce). Per i poliedri convessi vale la <b>relazione di Eulero</b>: F + V = S + 2.",
              "<b>Prisma retto</b>: Al = 2p × h; At = Al + 2Ab; V = Ab × h. Cubo: At = 6l², V = l³. Parallelepipedo: V = a × b × c, diagonale d = √(a² + b² + c²).",
              "<b>Piramide retta</b>: Al = 2p × apotema : 2; At = Al + Ab; V = Ab × h : 3. L’apotema si trova con Pitagora: altezza e apotema di base sono i cateti.",
              "Le unità di volume vanno di 1000 in 1000: 1 m³ = 1000 dm³. 1 dm³ = 1 l, 1 cm³ = 1 ml. Peso = volume × peso specifico."],
             [("Piramide quadrata: spigolo 12 cm, altezza 8 cm", ["apotema = √(8² + 6²) = 10 cm", "V = 144 × 8 : 3"], "V = 384 cm³")],
             [["Volume della piramide senza : 3", "La piramide ha un terzo del volume del prisma con stessa base e altezza."],
              ["Usare l’altezza invece dell’apotema nell’area laterale", "Le facce sono triangoli con altezza uguale all’apotema."],
              ["1 m³ = 100 dm³", "Nei volumi si moltiplica per 1000."]],
             table(["Solido", "Area laterale", "Volume"], [["prisma retto", "2p × h", "Ab × h"], ["cubo", "4l²", "l³"], ["piramide retta", "2p × a : 2", "Ab × h : 3"]]))
    faq = [("Che cos’è l’apotema di una piramide?", "È l’altezza di una faccia laterale (un triangolo): va dal vertice della piramide al punto medio di un lato di base."),
           ("Perché 1 dm³ = 1 litro?", "Per definizione il litro è la capacità di un cubo di 1 dm di spigolo.")]
    unit(G, R, "poliedri-prismi-e-piramidi", "S",
         "Visualizzare oggetti tridimensionali a partire da rappresentazioni bidimensionali; calcolare l’area e il volume delle figure solide più comuni e darne stime di oggetti della vita quotidiana",
         "Poliedri, prismi e piramidi", "Prismi e piramidi",
         "Schede di matematica per la terza media sui poliedri: relazione di Eulero, cubo, parallelepipedo, prismi e piramidi (area laterale, totale e volume), unità di volume, capacità e peso specifico. 100 esercizi con soluzioni.",
         "Prisma: V = Ab × h. Piramide: V = Ab × h : 3.", "1 dm³ = 1 litro.",
         body, faq, sets, 10)


if __name__ == "__main__":
    main()
