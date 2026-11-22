# -*- coding: utf-8 -*-
"""
Italia Matematica classe quinta: Solidi e volume (Spazio e figure)
  python3 tools/gen_it_matematica_c5_solidi_e_volume.py
Poliedri e solidi di rotazione, facce, spigoli e vertici (prisma, piramide), sviluppi, volume con i cubetti,
volume del parallelepipedo e del cubo (cm³, dm³, m³), dm³ e litri, superficie laterale e totale del cubo, problemi.
Errori: confondere area e volume, cm² invece di cm³, 1 dm³ = 10 cm³, contare solo i cubetti visibili.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, Kids, solido_svg, wrap, line, text, INK, GREEN, NB, FOIS, DIV, table

R = random.Random(70519)
G = "classe-quinta"
K = Kids(R)


def cubetti(a, b, c):
    """parallelepipedo di cubetti a (largh.) × b (prof.) × c (alt.) in assonometria"""
    s = []
    u, dx, dy = 22, 11, 9
    W = a * u + b * dx + 20
    H = c * u + b * dy + 20
    ox, oy = 10, 10 + b * dy + c * u

    def face(pts, col):
        s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='1.2'/>" % (" ".join("%.1f,%.1f" % p for p in pts), col, INK))
    for k in range(c):
        for i in range(a):
            x, y = ox + i * u, oy - (k + 1) * u
            face([(x, y), (x + u, y), (x + u, y + u), (x, y + u)], "#cfe6d6")
    for j in range(b):
        for i in range(a):
            x, y = ox + i * u + j * dx, oy - c * u - j * dy
            face([(x, y), (x + u, y), (x + u + dx, y - dy), (x + dx, y - dy)], "#e7f3ea")
    for j in range(b):
        for k in range(c):
            x, y = ox + a * u + j * dx, oy - (k + 1) * u - j * dy
            face([(x, y), (x + dx, y - dy), (x + dx, y - dy + u), (x, y + u)], "#a9d3b5")
    return wrap(W, H, "".join(s), "parallelepipedo fatto di cubetti", lg=True)


SOL = [("cubo", "un cubo", (6, 12, 8), "poliedro"), ("parallelepipedo", "un parallelepipedo", (6, 12, 8), "poliedro"), ("piramide", "una piramide a base quadrata", (5, 8, 5), "poliedro"),
       ("cilindro", "un cilindro", None, "solido di rotazione"), ("cono", "un cono", None, "solido di rotazione"), ("sfera", "una sfera", None, "solido di rotazione")]
PRISMI = [("un prisma a base triangolare", 5, 9, 6), ("un prisma a base pentagonale", 7, 15, 10), ("un prisma a base esagonale", 8, 18, 12),
          ("una piramide a base triangolare", 4, 6, 4), ("una piramide a base pentagonale", 6, 10, 6), ("una piramide a base esagonale", 7, 12, 7),
          ("un cubo", 6, 12, 8), ("una piramide a base quadrata", 5, 8, 5)]


def s1_tipo():
    k, nome, _, t = R.choice(SOL)
    return mcq(solido_svg(k, R.choice([28, 32, 36]), R.choice(["#cfe6d6", "#f6d6a8", "#c9dcf2"])) + "Questo solido è un poliedro o un solido di rotazione?", t,
               ["poliedro" if t != "poliedro" else "solido di rotazione", "una figura piana", "un poligono"],
               "È %s: %s." % (nome, "ha solo facce piane, è un <b>poliedro</b>" if t == "poliedro" else "ha superfici curve e si ottiene facendo ruotare una figura piana: è un <b>solido di rotazione</b>"))


def s1_fsv():
    nome, f, sp, v = R.choice(PRISMI)
    i = R.randint(0, 2)
    word = ["facce", "spigoli", "vertici"][i]
    val = (f, sp, v)[i]
    return mcq("%s %s ha %s?" % ("Quante" if i == 0 else "Quanti", word, nome), str(val), [str(x) for x in (f, sp, v) if x != val] + [str(val + 2), str(val - 1)],
               "%s ha %d facce, %d spigoli e %d vertici: <b>%d %s</b>." % (nome[0].upper() + nome[1:], f, sp, v, val, word))


def s2_cubetti():
    a, b, c = R.randint(2, 5), R.randint(2, 4), R.randint(2, 4)
    v = a * b * c
    vis = a * c + a * b + b * c - a - b - c + 1
    return mcq(cubetti(a, b, c) + "Il solido è pieno di cubetti tutti uguali. Quanti cubetti ci sono?", str(v), [str(vis), str(a * b + b * c + a * c), str(a + b + c), str(v + a)],
               "Ogni strato ha %d %s %d = %d cubetti; gli strati sono %d: %d %s %d = <b>%d</b>." % (a, FOIS, b, a * b, c, a * b, FOIS, c, v))


def s3_volume():
    k = R.choice(["para", "para", "cubo"])
    if k == "para":
        a, b, c = R.randint(2, 15), R.randint(2, 10), R.randint(2, 12)
        v = a * b * c
        return mcq("Un parallelepipedo misura %d cm %s %d cm %s %d cm. Qual è il suo volume?" % (a, FOIS, b, FOIS, c), "%s%scm³" % (num(v), NB),
                   ["%s%scm²" % (num(v), NB), "%s%scm³" % (num(a + b + c), NB), "%s%scm³" % (num(2 * (a * b + b * c + a * c)), NB), "%s%scm³" % (num(a * b), NB)],
                   "V = lunghezza %s larghezza %s altezza = %d %s %d %s %d = <b>%s cm³</b>." % (FOIS, FOIS, a, FOIS, b, FOIS, c, num(v)))
    l = R.randint(2, 12)
    return mcq("Un cubo ha lo spigolo di %d cm. Qual è il suo volume?" % l, "%s%scm³" % (num(l ** 3), NB),
               ["%s%scm³" % (num(l * l), NB), "%s%scm³" % (num(l * 3), NB) if l * 3 != l ** 3 else "%s%scm³" % (num(l * 12), NB), "%s%scm³" % (num(6 * l * l), NB) if 6 * l * l != l ** 3 else "%s%scm³" % (num(l * 4), NB)],
               "V = spigolo %s spigolo %s spigolo = %d %s %d %s %d = <b>%s cm³</b>." % (FOIS, FOIS, l, FOIS, l, FOIS, l, num(l ** 3)))


def s4_misure():
    k = R.choice(["dm_l", "l_dm", "cm_ml", "m_dm", "dm_cm", "sup"])
    a = R.randint(2, 30)
    if k == "dm_l":
        return mcq("Quanti litri sono %d dm³?" % a, "%d l" % a, ["%d l" % (a * 10), "%d l" % (a * 1000), "%s l" % ("%d,%d" % (a // 10, a % 10) if a % 10 else str(a // 10))], "1 dm³ = 1 litro: <b>%d l</b>." % a)
    if k == "l_dm":
        return mcq("Una bottiglia contiene %d litri. Quanti dm³ sono?" % a, "%d dm³" % a, ["%d dm³" % (a * 10), "%d dm³" % (a * 100), "%s dm³" % num(a * 1000)], "1 l = 1 dm³: <b>%d dm³</b>." % a)
    if k == "cm_ml":
        a = R.randint(50, 900)
        return mcq("Quanti ml sono %d cm³?" % a, "%d ml" % a, ["%d ml" % (a * 10), "%s ml" % num(a * 1000), "%d ml" % (a // 10)], "1 cm³ = 1 ml: <b>%d ml</b>." % a)
    if k == "m_dm":
        a = R.randint(2, 9)
        return mcq("Quanti dm³ sono %d m³?" % a, "%s dm³" % num(a * 1000), ["%d dm³" % (a * 10), "%d dm³" % (a * 100), "%s dm³" % num(a * 10 ** 6)], "Nel volume ogni passo vale 1000: 1 m³ = 1000 dm³. <b>%s dm³</b>." % num(a * 1000))
    if k == "dm_cm":
        a = R.randint(2, 9)
        return mcq("Quanti cm³ sono %d dm³?" % a, "%s cm³" % num(a * 1000), ["%d cm³" % (a * 10), "%d cm³" % (a * 100), "%s cm³" % num(a * 10 ** 6)], "1 dm³ = 1000 cm³: <b>%s cm³</b>." % num(a * 1000))
    l = R.randint(2, 12)
    return mcq("Un cubo ha lo spigolo di %d cm. Qual è la sua superficie totale?" % l, "%s%scm²" % (num(6 * l * l), NB),
               ["%s%scm²" % (num(4 * l * l), NB), "%s%scm³" % (num(l ** 3), NB), "%s%scm²" % (num(l * l), NB)], "6 facce quadrate: 6 %s %d %s %d = <b>%s cm²</b>." % (FOIS, l, FOIS, l, num(6 * l * l)))


def s5():
    p = K.next()
    k = R.choice(["acquario", "scatola", "piscina", "cubetti", "sabbia", "regalo"])
    if k == "acquario":
        a, b, c = R.choice([(6, 3, 4), (5, 4, 3), (8, 3, 4), (10, 4, 5), (6, 5, 4)])
        return mcq("Un acquario misura %d dm %s %d dm %s %d dm. Quanti litri d’acqua contiene quando è pieno?" % (a, FOIS, b, FOIS, c), "%d l" % (a * b * c), ["%d l" % (a * b), "%d l" % (a * b * c * 10), "%d l" % (a + b + c)],
                   "V = %d %s %d %s %d = %d dm³ = <b>%d litri</b>." % (a, FOIS, b, FOIS, c, a * b * c, a * b * c))
    if k == "scatola":
        a, b, c, l = R.choice([(20, 10, 10, 5), (30, 20, 10, 10), (40, 20, 20, 10), (12, 8, 6, 2), (15, 10, 5, 5)])
        n = (a // l) * (b // l) * (c // l)
        return mcq("Una scatola misura %d cm %s %d cm %s %d cm. Quanti cubetti con lo spigolo di %d cm ci stanno?" % (a, FOIS, b, FOIS, c, l), num(n), [num(a * b * c), num((a + b + c) // l), num(n // 2)],
                   "%d %s %d %s %d = %d cubetti (oppure %s : %d)." % (a // l, FOIS, b // l, FOIS, c // l, n, num(a * b * c), l ** 3) + " <b>%s</b>." % num(n))
    if k == "piscina":
        a, b, c = R.choice([(10, 5, 2), (12, 6, 2), (20, 10, 2), (8, 4, 1)])
        return mcq("Una piscina misura %d m %s %d m ed è profonda %d m. Quanti m³ d’acqua contiene?" % (a, FOIS, b, c), "%d m³" % (a * b * c), ["%d m²" % (a * b), "%d m³" % (a * b), "%d m³" % (a + b + c)],
                   "V = %d %s %d %s %d = <b>%d m³</b>." % (a, FOIS, b, FOIS, c, a * b * c))
    if k == "cubetti":
        l = R.randint(2, 5)
        return mcq("%s costruisce un cubo con cubetti di 1 cm: lo spigolo è di %d cm. Quanti cubetti usa?" % (p[0], l), str(l ** 3), [str(l * l), str(l * 12), str(6 * l * l)],
                   "%d %s %d %s %d = <b>%d</b>." % (l, FOIS, l, FOIS, l, l ** 3))
    if k == "sabbia":
        a, b, c = R.choice([(2, 1, 1), (3, 2, 1), (4, 2, 1)])
        return mcq("Un camion ha il cassone di %d m %s %d m %s %d m. Quanti m³ di sabbia può trasportare?" % (a, FOIS, b, FOIS, c), "%d m³" % (a * b * c), ["%d m³" % (a + b + c), "%d m²" % (a * b * c), "%d m³" % (2 * (a * b + b * c + a * c))],
                   "%d %s %d %s %d = <b>%d m³</b>." % (a, FOIS, b, FOIS, c, a * b * c))
    l = R.randint(10, 30)
    return mcq("%s incarta un regalo a forma di cubo con lo spigolo di %d cm. Quanta carta serve almeno per coprire tutte le facce?" % (p[0], l), "%s cm²" % num(6 * l * l),
               ["%s cm²" % num(4 * l * l), "%s cm³" % num(l ** 3), "%s cm²" % num(l * l)], "6 %s %d %s %d = <b>%s cm²</b>." % (FOIS, l, FOIS, l, num(6 * l * l)))


def main():
    seen = set()
    sets = [
        ("Poliedri e solidi di rotazione", mix(R, seen, [(s1_tipo, 10), (s1_fsv, 10)])),
        ("Contare i cubetti", mix(R, seen, [(s2_cubetti, 20)])),
        ("Volume di parallelepipedo e cubo", mix(R, seen, [(s3_volume, 20)])),
        ("Misure di volume e capacità", mix(R, seen, [(s4_misure, 20)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["I <b>poliedri</b> hanno solo facce piane (cubo, parallelepipedo, prismi, piramidi). I <b>solidi di rotazione</b> hanno superfici curve (cilindro, cono, sfera).",
         "Il <b>volume</b> è lo spazio occupato da un solido: si misura in cubetti, cioè in cm³, dm³, m³.",
         "Parallelepipedo: V = lunghezza %s larghezza %s altezza. Cubo: V = spigolo %s spigolo %s spigolo." % (FOIS, FOIS, FOIS, FOIS),
         "Nel volume ogni passo vale 1000: 1 m³ = 1000 dm³. E 1 dm³ = 1 litro, 1 cm³ = 1 ml."],
        [("Parallelepipedo 5 cm %s 4 cm %s 3 cm" % (FOIS, FOIS), ["strato: 5 %s 4 = 20 cubetti" % FOIS, "3 strati: 20 %s 3 = 60" % FOIS], "60 cm³")],
        [["Confondere area e volume", "L’area misura una superficie (cm²), il volume lo spazio (cm³)."],
         ["Contare solo i cubetti visibili", "Conta gli strati: anche quelli dentro e dietro."],
         ["1 dm³ = 10 cm³", "1 dm³ = 10 %s 10 %s 10 = 1000 cm³." % (FOIS, FOIS)]],
        table(["Solido", "Facce", "Spigoli", "Vertici"], [["cubo", "6", "12", "8"], ["prisma a base triangolare", "5", "9", "6"], ["piramide a base quadrata", "5", "8", "5"]]))
    faq = [("Che relazione c’è tra dm³ e litri?", "Un cubo di 1 dm di spigolo contiene esattamente 1 litro d’acqua: 1 dm³ = 1 l."),
           ("Perché il volume si misura in cm³?", "Perché si conta quanti cubetti di 1 cm di spigolo servono per riempire il solido.")]
    make_unit(R, "solidi-e-volume", "S",
              "Riconoscere, denominare e descrivere figure solide (poliedri e solidi di rotazione); determinare il volume di parallelepipedi e cubi contando unità cubiche e con le formule; relazioni tra dm³ e litro",
              "Solidi e volume: poliedri, cubo e parallelepipedo", "Solidi e volume",
              "Schede di matematica per la classe quinta su solidi e volume: poliedri e solidi di rotazione, facce, spigoli e vertici, cubetti, volume del cubo e del parallelepipedo, dm³ e litri, problemi. 100 esercizi con soluzioni.",
              "Volume = lunghezza × larghezza × altezza.", "1 dm³ = 1 litro.",
              body, faq, sets, 19, grade=G)


if __name__ == "__main__":
    main()
