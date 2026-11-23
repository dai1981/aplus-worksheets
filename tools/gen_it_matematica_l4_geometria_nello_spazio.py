# -*- coding: utf-8 -*-
"""
Italia Matematica quarta liceo: Geometria nello spazio (Geometria)
  python3 tools/gen_it_matematica_l4_geometria_nello_spazio.py
Posizioni reciproche di rette e piani (rette sghembe), perpendicolarità, relazione di Eulero per i poliedri,
diagonale del parallelepipedo, aree e volumi di prisma, piramide, cilindro, cono, sfera (in forma esatta con π),
rapporti tra solidi simili (aree k², volumi k³).
Errori: rette non incidenti = parallele, volume della piramide senza 1/3, superficie sferica πr², volumi simili con k².
"""
import math
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, d, simp_root

R = random.Random(72409)
G = "quarta-liceo"


def rt(n):
    k, m = simp_root(int(n))
    return str(k) if m == 1 else ("" if k == 1 else str(k)) + "√" + str(m)


def pi(v):
    v = Fr(v)
    if v.denominator == 1:
        return ("" if v == 1 else d(v)) + "π"
    return "%sπ/%d" % ("" if v.numerator == 1 else v.numerator, v.denominator)


POS = [("Due rette nello spazio che non si incontrano e non sono parallele si dicono…", "sghembe", ["incidenti", "perpendicolari", "complanari"]),
       ("Due rette sghembe…", "non stanno su uno stesso piano", ["si incontrano in un punto", "sono parallele", "formano un angolo retto"]),
       ("Se una retta è perpendicolare a due rette incidenti di un piano, allora è…", "perpendicolare al piano", ["parallela al piano", "contenuta nel piano", "sghemba rispetto al piano"]),
       ("Due piani distinti non paralleli si incontrano in…", "una retta", ["un punto", "due rette", "un piano"]),
       ("Quanti piani passano per tre punti non allineati?", "uno solo", ["infiniti", "nessuno", "tre"]),
       ("Due rette perpendicolari allo stesso piano sono…", "parallele tra loro", ["sghembe", "incidenti", "perpendicolari tra loro"]),
       ("In un cubo ABCDEFGH, gli spigoli AB e CG sono…", "sghembi", ["paralleli", "incidenti", "coincidenti"]),
       ("Una retta parallela a un piano…", "non ha punti in comune con il piano oppure vi è contenuta", ["lo incontra in un punto", "è sempre perpendicolare al piano", "lo incontra in due punti"])]


def s1_pos():
    q, a, w = R.choice(POS)
    return M(q, a, w, "%s <b>%s</b>." % (q.rstrip("?…").rstrip(), a))


POLI = [("cubo", 8, 12, 6), ("tetraedro", 4, 6, 4), ("ottaedro", 6, 12, 8), ("prisma a base pentagonale", 10, 15, 7), ("piramide a base esagonale", 7, 12, 7),
        ("prisma a base triangolare", 6, 9, 5), ("piramide a base quadrata", 5, 8, 5), ("dodecaedro", 20, 30, 12), ("icosaedro", 12, 30, 20), ("prisma a base esagonale", 12, 18, 8)]


def s1_eulero():
    nm, V, S, F = R.choice(POLI)
    miss = R.choice(["V", "S", "F"])
    q = {"V": "ha %d spigoli e %d facce. Quanti vertici ha?" % (S, F), "S": "ha %d vertici e %d facce. Quanti spigoli ha?" % (V, F), "F": "ha %d vertici e %d spigoli. Quante facce ha?" % (V, S)}[miss]
    v = {"V": V, "S": S, "F": F}[miss]
    alt = {"V": S - F, "S": V + F, "F": S - V}[miss]
    return M("Un %s %s" % (nm, q), str(v), [str(x) for x in W(alt, v + 1, v - 1, v + 2) if x != v],
             "Relazione di Eulero: V − S + F = 2. %s" % ("<b>%d</b>." % v))


def s2_diag():
    a, b, c = R.choice([(1, 2, 2), (2, 3, 6), (1, 4, 8), (2, 6, 9), (3, 4, 12), (2, 10, 11), (4, 4, 7), (6, 6, 7)]) if R.random() < 0.6 else (R.randint(1, 6), R.randint(1, 6), R.randint(1, 6))
    n = a * a + b * b + c * c
    v = rt(n)
    if R.random() < 0.3:
        l = R.randint(2, 9)
        return M("Quanto misura la diagonale di un cubo di spigolo %d cm?" % l, "%d√3 cm" % l, ["%d√2 cm" % l, "%d cm" % (3 * l), "%d cm" % (l * l)],
                 "d = √(3l²) = <b>%d√3 cm</b>." % l)
    return M("Quanto misura la diagonale di un parallelepipedo rettangolo con spigoli %d, %d e %d cm?" % (a, b, c), "%s cm" % v, ["%s cm" % x for x in W(str(a + b + c), rt(a * a + b * b), rt(n + 1)) if x != v],
             "d = √(a² + b² + c²) = √(%d + %d + %d) = √%d = <b>%s cm</b>." % (a * a, b * b, c * c, n, v))


def s3_vol():
    k = R.choice(["prisma", "piramide", "cilindro", "cono", "sfera", "cubo"])
    if k == "prisma":
        a, b, h = R.randint(2, 9), R.randint(2, 9), R.randint(2, 12)
        v = a * b * h
        return M("Un prisma retto ha per base un rettangolo di lati %d cm e %d cm e altezza %d cm. Qual è il volume?" % (a, b, h), "%s cm³" % d(v), ["%s cm³" % d(x) for x in W(Fr(v, 3), 2 * (a * b + a * h + b * h), v * 2)],
                 "V = area di base · altezza = %d · %d = <b>%s cm³</b>." % (a * b, h, d(v)))
    if k == "piramide":
        l, h = R.randint(2, 10), R.choice([3, 6, 9, 12, 4, 5])
        v = Fr(l * l * h, 3)
        return M("Una piramide ha base quadrata di lato %d cm e altezza %d cm. Qual è il volume?" % (l, h), "%s cm³" % fq(v), ["%s cm³" % fq(x) for x in W(l * l * h, Fr(l * l * h, 2), Fr(l * h, 3)) if x != v],
                 "V = (area di base · altezza)/3 = %d · %d / 3 = <b>%s cm³</b>." % (l * l, h, fq(v)))
    if k == "cilindro":
        r, h = R.randint(1, 8), R.randint(2, 12)
        v = r * r * h
        return M("Un cilindro ha raggio %d cm e altezza %d cm. Qual è il volume?" % (r, h), "%s cm³" % pi(v), ["%s cm³" % pi(x) for x in W(2 * r * h, Fr(v, 3), r * h * h if r != h else 2 * v, 2 * v, r * h) if x != v],
                 "V = πr²h = π · %d · %d = <b>%s cm³</b>." % (r * r, h, pi(v)))
    if k == "cono":
        r, h = R.randint(1, 8), R.choice([3, 6, 9, 12, 4])
        v = Fr(r * r * h, 3)
        return M("Un cono ha raggio %d cm e altezza %d cm. Qual è il volume?" % (r, h), "%s cm³" % pi(v), ["%s cm³" % pi(x) for x in W(r * r * h, Fr(r * h, 3), Fr(r * r * h, 2)) if x != v],
                 "V = πr²h/3 = π · %d · %d / 3 = <b>%s cm³</b>." % (r * r, h, pi(v)))
    if k == "sfera":
        r = R.randint(1, 9)
        t = R.choice(["V", "S"])
        if t == "V":
            v = Fr(4 * r ** 3, 3)
            return M("Qual è il volume di una sfera di raggio %d cm?" % r, "%s cm³" % pi(v), ["%s cm³" % pi(x) for x in W(4 * r * r, Fr(4 * r * r, 3), r ** 3, 4 * r ** 3, Fr(r ** 3, 3)) if x != v],
                     "V = (4/3)πr³ = (4/3)π · %d = <b>%s cm³</b>." % (r ** 3, pi(v)))
        v = 4 * r * r
        return M("Qual è la superficie di una sfera di raggio %d cm?" % r, "%s cm²" % pi(v), ["%s cm²" % pi(x) for x in W(r * r, Fr(4 * r ** 3, 3), 2 * r * r) if x != v],
                 "S = 4πr² = 4π · %d = <b>%s cm²</b>." % (r * r, pi(v)))
    l = R.randint(2, 9)
    return M("Qual è la superficie totale di un cubo di spigolo %d cm?" % l, "%d cm²" % (6 * l * l), ["%d cm²" % x for x in W(l ** 3, 4 * l * l, 12 * l, 8 * l * l, 6 * l)],
             "S = 6l² = 6 · %d = <b>%d cm²</b>." % (l * l, 6 * l * l))


def s4_lat():
    k = R.choice(["cil", "cono"])
    if k == "cil":
        r, h = R.randint(1, 8), R.randint(2, 10)
        v = 2 * r * h
        return M("Qual è la superficie laterale di un cilindro di raggio %d cm e altezza %d cm?" % (r, h), "%s cm²" % pi(v), ["%s cm²" % pi(x) for x in W(r * h, r * r * h, 2 * r * h + 2 * r * r, 4 * r * h) if x != v],
                 "S<sub>L</sub> = 2πrh = 2π · %d · %d = <b>%s cm²</b>." % (r, h, pi(v)))
    r, h, a = R.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 6, 10), (4, 3, 5), (9, 12, 15)])
    v = r * a
    return M("Un cono ha raggio %d cm e altezza %d cm. Qual è la superficie laterale?" % (r, h), "%s cm²" % pi(v), ["%s cm²" % pi(x) for x in W(r * h, 2 * r * a, r * a + r * r) if x != v],
             "Apotema a = √(%d² + %d²) = %d; S<sub>L</sub> = πra = <b>%s cm²</b>." % (r, h, a, pi(v)))


def s5_simili():
    k = R.choice([2, 3, Fr(1, 2), 4, Fr(3, 2)])
    t = R.choice(["vol", "area"])
    v0 = R.choice([8, 12, 16, 24, 54, 27, 40])
    if t == "vol":
        v = v0 * k ** 3
        return M("Due solidi simili hanno rapporto di similitudine %s. Il primo ha volume %d cm³. Qual è il volume del secondo?" % (fq(k), v0), "%s cm³" % fq(v), ["%s cm³" % fq(x) for x in W(v0 * k, v0 * k * k, v0 + k) if x != v],
                 "I volumi stanno come k³ = %s: %d · %s = <b>%s cm³</b>." % (fq(k ** 3), v0, fq(k ** 3), fq(v)))
    v = v0 * k * k
    return M("Due solidi simili hanno rapporto di similitudine %s. Il primo ha superficie %d cm². Qual è la superficie del secondo?" % (fq(k), v0), "%s cm²" % fq(v), ["%s cm²" % fq(x) for x in W(v0 * k, v0 * k ** 3, v0 + k) if x != v],
             "Le superfici stanno come k² = %s: <b>%s cm²</b>." % (fq(k * k), fq(v)))


def main():
    seen = set()
    sets = [
        ("Rette e piani nello spazio", mix(R, seen, [(s1_pos, 8), (s1_eulero, 12)])),
        ("Diagonali", mix(R, seen, [(s2_diag, 20)])),
        ("Volumi", mix(R, seen, [(s3_vol, 20)])),
        ("Superfici", mix(R, seen, [(s4_lat, 12), (s3_vol, 8)])),
        ("Solidi simili", mix(R, seen, [(s5_simili, 14), (s4_lat, 6)])),
    ]
    body = L(["Nello spazio due rette possono essere incidenti, parallele o <b>sghembe</b> (non complanari). Una retta è perpendicolare a un piano se è perpendicolare a due rette incidenti del piano.",
              "Nei poliedri convessi vale la <b>relazione di Eulero</b>: V − S + F = 2 (vertici, spigoli, facce). La diagonale del parallelepipedo rettangolo è √(a² + b² + c²).",
              "Volumi: prisma e cilindro V = B · h; piramide e cono V = B · h / 3; sfera V = (4/3)πr³. Superfici: cilindro S<sub>L</sub> = 2πrh, cono S<sub>L</sub> = πra, sfera S = 4πr².",
              "In due solidi simili con rapporto k, le aree stanno come k² e i volumi come k³."],
             [("Cono r = 3, h = 4", ["Apotema 5", "S<sub>L</sub> = π · 3 · 5, V = π · 9 · 4 / 3"], "S<sub>L</sub> = 15π, V = 12π"),
              ("Parallelepipedo 2, 3, 6", ["√(4 + 9 + 36)"], "diagonale 7")],
             [["Rette che non si incontrano sono parallele", "Possono essere sghembe: parallele solo se stanno sullo stesso piano."],
              ["Volume della piramide = B · h", "Serve il fattore 1/3: V = B · h / 3."],
              ["Volume dei simili moltiplicato per k²", "I volumi si moltiplicano per k³."]])
    faq = [("Perché la piramide ha volume un terzo del prisma?", "Un cubo si può dividere in tre piramidi congruenti con la stessa base e la stessa altezza; in generale il principio di Cavalieri lo estende a ogni piramide."),
           ("Che cosa dice il principio di Cavalieri?", "Due solidi tagliati da piani paralleli in sezioni di area uguale, alla stessa altezza, hanno lo stesso volume.")]
    unit(G, R, "geometria-nello-spazio", "G",
         "Elementi di geometria dello spazio: posizioni di rette e piani, poliedri, solidi di rotazione, aree e volumi",
         "Geometria nello spazio", "Geometria nello spazio",
         "Schede di matematica per la quarta liceo sulla geometria nello spazio: rette e piani, rette sghembe, relazione di Eulero, diagonale del parallelepipedo, volumi e superfici di prisma, piramide, cilindro, cono e sfera, solidi simili. 100 esercizi con soluzioni.",
         "V − S + F = 2", "Piramide e cono: V = B · h / 3. Sfera: V = (4/3)πr³, S = 4πr².",
         body, faq, sets, 9)


if __name__ == "__main__":
    main()
