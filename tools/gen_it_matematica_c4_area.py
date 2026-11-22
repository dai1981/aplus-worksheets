# -*- coding: utf-8 -*-
"""
Italia Matematica classe quarta: L’area (Spazio e figure)
  python3 tools/gen_it_matematica_c4_area.py
Superficie misurata con i quadretti, unità di misura di superficie (cm², dm², m²) ed equivalenze (passi da 100),
area del rettangolo e del quadrato, formule inverse, figure equiestese, area e perimetro a confronto, problemi.
Errori: confondere area e perimetro, scrivere cm invece di cm², contare passi da 10 nelle misure di superficie.
"""
import random
from it_common import mcq, lesson, make_unit, mix, table, Kids, FOIS, DIV, NB, num
import gen_it_matematica_c3_figure_piane_e_perimetro as F3
import gen_it_matematica_c5_perimetro_e_area_dei_poligoni as PA5

R = random.Random(70418)
G = "classe-quarta"
SUP = ["km²", "hm²", "dam²", "m²", "dm²", "cm²", "mm²"]


def u2(v, u="cm²"):
    return "%s%s%s" % (num(v), NB, u)


def s1_quadretti():
    it = F3.s4_quadretti()
    return it if it and "superficie" in it["q"] else None


def s2_unita():
    k = R.choice(["eq", "eq", "eq", "quale"])
    if k == "quale":
        o, u = R.choice([("il pavimento di una cucina", "m²"), ("la copertina di un quaderno", "cm²"), ("un francobollo", "cm²"), ("un campo da calcio", "m²"),
                         ("il piano di un banco", "dm²"), ("una regione italiana", "km²"), ("la pagina di un libro", "cm²"), ("un parcheggio", "m²"), ("un lago", "km²")])
        return mcq("Quale unità di misura è più adatta per l’area di %s?" % o, u, [x for x in ("cm²", "dm²", "m²", "km²", "cm") if x != u],
                   "Per %s la misura più comoda è in <b>%s</b>." % (o, u))
    i = R.randrange(3, 6)
    a, b = SUP[i], SUP[i + 1]
    n = R.randint(2, 90)
    if R.random() < 0.5:
        return mcq("Completa: %d %s = … %s" % (n, a, b), u2(n * 100, b), [u2(n * 10, b), u2(n * 1000, b), u2(n, b)],
                   "Nelle misure di superficie ogni passo vale <b>100</b>: %d %s 100 = <b>%s</b>." % (n, FOIS, u2(n * 100, b)))
    return mcq("Completa: %s = … %s" % (u2(n * 100, b), a), u2(n, a), [u2(n * 10, a), u2(n * 100 // 1000 if n * 100 >= 1000 else n * 1000, a), u2(n * 10000, a)],
               "Da %s a %s (unità più grande) si divide per 100: <b>%s</b>." % (b, a, u2(n, a)))


def s3_area():
    it = PA5.s2_area()
    if it and "parallelogramma" in it["q"]:
        return None
    return it


def s3_inversa():
    k = R.choice(["base", "lato", "base"])
    if k == "base":
        b, h = R.randint(4, 25), R.randint(3, 15)
        return mcq("Un rettangolo ha l’area di %s e l’altezza di %d cm. Quanto misura la base?" % (u2(b * h), h), "%d%scm" % (b, NB),
                   ["%d%scm" % (b * h - h, NB), "%d%scm" % (b * h // 2, NB) if b * h // 2 != b else "%d%scm" % (b + h, NB), "%d%scm" % (b * h * h, NB) if b * h * h < 2000 else "%d%scm" % (b + 1, NB)],
                   "base = area %s altezza = %d %s %d = <b>%d cm</b>." % (DIV, b * h, DIV, h, b))
    a = R.randint(2, 12)
    return mcq("Un quadrato ha l’area di %s. Quanto misura il lato?" % u2(a * a), "%d%scm" % (a, NB), ["%d%scm" % (a * a // 2, NB) if a * a // 2 != a else "%d%scm" % (a + 2, NB), "%d%scm" % (a * a // 4 if a * a // 4 not in (a, a * a // 2) else a + 1, NB), "%d%scm" % (a * a, NB)],
               "Cerca il numero che moltiplicato per sé stesso dà %d: %d %s %d. <b>%d cm</b>." % (a * a, a, FOIS, a, a))


def s4_confronto():
    k = R.choice(["equi", "equi", "ap", "ap", "quiz"])
    if k == "equi":
        A = R.choice([12, 16, 18, 20, 24, 30, 36, 40, 48])
        ds = [(d, A // d) for d in range(1, A + 1) if A % d == 0 and d <= A // d]
        ok = R.choice(ds)
        bad = []
        for d in range(2, 12):
            for e in range(d, 15):
                if d * e != A and abs(d * e - A) <= 8 and len(bad) < 6:
                    bad.append((d, e))
        R.shuffle(bad)
        f = lambda t: "%d cm × %d cm" % t
        return mcq("Quale rettangolo ha la stessa area di un rettangolo di %s (cioè è equiesteso)?" % f((ds[-1] if ds[-1] != ok else ds[0])), f(ok), [f(x) for x in bad],
                   "L’area deve essere %d cm²: %d %s %d = %d. <b>%s</b>." % (A, ok[0], FOIS, ok[1], A, f(ok)))
    if k == "ap":
        a, b = R.randint(2, 12), R.randint(2, 12)
        if a == b:
            return None
        if R.random() < 0.5:
            return mcq("Un rettangolo misura %d cm × %d cm. Qual è la sua area?" % (a, b), u2(a * b), ["%d%scm" % (2 * (a + b), NB), u2(2 * (a + b)), u2(a + b)],
                       "Area = base %s altezza = <b>%s</b> (il perimetro sarebbe %d cm)." % (FOIS, u2(a * b), 2 * (a + b)))
        return mcq("Un rettangolo misura %d cm × %d cm. Qual è il suo perimetro?" % (a, b), "%d%scm" % (2 * (a + b), NB), [u2(a * b), "%d%scm" % (a + b, NB), "%d%scm" % (a * b, NB)],
                   "Perimetro = (base + altezza) %s 2 = <b>%d cm</b> (l’area sarebbe %d cm²)." % (FOIS, 2 * (a + b), a * b))
    q, a, w = R.choice([("Due figure con la stessa area si chiamano…", "equiestese", ["isoperimetriche", "congruenti", "parallele"]),
                        ("Se raddoppi il lato di un quadrato, l’area…", "diventa 4 volte più grande", ["raddoppia", "resta uguale", "diventa la metà"]),
                        ("Un quadrato di 1 m di lato quanti dm² misura?", "100 dm²", ["10 dm²", "1000 dm²", "4 dm²"]),
                        ("Con quale unità si misura l’area?", "in unità quadrate (cm², m²…)", ["in cm", "in litri", "in grammi"]),
                        ("Un rettangolo 6 cm × 4 cm e un quadrato di lato 5 cm: quale ha l’area maggiore?", "il quadrato (25 cm²)", ["il rettangolo (24 cm²)", "sono uguali", "non si può sapere"]),
                        ("Se tagli una figura e ricomponi i pezzi in un altro modo, l’area…", "resta la stessa", ["aumenta", "diminuisce", "raddoppia"])])
    return mcq(q, a, w, "Risposta: <b>%s</b>." % a)


def s5():
    k = R.choice(["piastrelle", "tappeto", "prato", "vernice", "cartoncino", "orto"])
    if k == "piastrelle":
        a, b = R.randint(3, 8), R.randint(3, 6)
        pr = R.choice([15, 20, 25, 30])
        return mcq("Il pavimento di una stanza misura %d m × %d m. Le piastrelle costano %d € al m². Quanto si spende?" % (a, b, pr), "%s €" % num(a * b * pr),
                   ["%s €" % num(2 * (a + b) * pr), "%s €" % num(a * b), "%s €" % num((a + b) * pr)], "Area: %d %s %d = %d m²; %d %s %d = <b>%s €</b>." % (a, FOIS, b, a * b, a * b, FOIS, pr, num(a * b * pr)))
    if k == "tappeto":
        a = R.randint(2, 4)
        return mcq("Un tappeto quadrato ha il lato di %d m. Quanti m² di pavimento copre?" % a, u2(a * a, "m²"), [u2(4 * a, "m²") if 4 * a != a * a else u2(2 * a, "m²"), u2(2 * a, "m²") if 2 * a != a * a else u2(a + 1, "m²"), "%d%sm" % (4 * a, NB)],
                   "%d %s %d = <b>%s</b>." % (a, FOIS, a, u2(a * a, "m²")))
    if k == "prato":
        a, b = R.randint(10, 40), R.randint(6, 25)
        k2 = R.choice([2, 3, 4])
        return mcq("Un prato rettangolare misura %d m × %d m. Per ogni m² servono %d g di semi. Quanti grammi di semi servono?" % (a, b, k2), "%s g" % num(a * b * k2),
                   ["%s g" % num(2 * (a + b) * k2), "%s g" % num(a * b), "%s g" % num((a + b) * k2)], "Area: %d m²; %d %s %d = <b>%s g</b>." % (a * b, a * b, FOIS, k2, num(a * b * k2)))
    if k == "vernice":
        a, b = R.randint(3, 6), R.randint(2, 3)
        lit = R.choice([2, 4, 5])
        A = a * b
        if A % lit:
            return None
        return mcq("Una parete misura %d m × %d m. Con 1 litro di vernice si dipingono %d m². Quanti litri servono?" % (a, b, lit), "%d litri" % (A // lit) if A // lit != 1 else "1 litro",
                   ["%d litri" % (A * lit), "%d litri" % (A // lit + 1), "%d litri" % (2 * (a + b) // lit if 2 * (a + b) // lit not in (A // lit, A // lit + 1) else A)],
                   "Area: %d m²; %d %s %d = <b>%d</b>." % (A, A, DIV, lit, A // lit))
    if k == "cartoncino":
        a, b = R.randint(20, 40), R.randint(15, 30)
        c = R.randint(4, 10)
        return mcq("Da un cartoncino di %d cm × %d cm si ritaglia un quadrato di lato %d cm. Qual è l’area del cartoncino che resta?" % (a, b, c), u2(a * b - c * c),
                   [u2(a * b), u2(a * b - 4 * c), u2(c * c)], "%d %s %d = %d; %d %s %d = %d; %d − %d = <b>%s</b>." % (a, FOIS, b, a * b, c, FOIS, c, c * c, a * b, c * c, u2(a * b - c * c)))
    a = R.randint(8, 20)
    b = R.randint(4, 10)
    return mcq("Un orto rettangolare ha l’area di %d m² e un lato di %d m. Quanto misura l’altro lato?" % (a * b, b), "%d m" % a, ["%d m" % (a * b - b), "%d m" % (a * b // 2), "%d m" % (a * b * b) if a * b * b < 5000 else "%d m" % (a + 1)],
               "%d %s %d = <b>%d m</b>." % (a * b, DIV, b, a))


def main():
    for m in (F3, PA5):
        m.R = R
    PA5.K = Kids(R)
    seen = set()
    sets = [
        ("Misurare con i quadretti", mix(R, seen, [(s1_quadretti, 20)])),
        ("Unità di misura di superficie", mix(R, seen, [(s2_unita, 20)])),
        ("Area di rettangolo e quadrato", mix(R, seen, [(s3_area, 14), (s3_inversa, 6)])),
        ("Area e perimetro, figure equiestese", mix(R, seen, [(s4_confronto, 20)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["L’<b>area</b> misura la superficie, cioè lo spazio dentro una figura. Si misura in unità quadrate: cm², dm², m².",
         "1 cm² è un quadratino con il lato di 1 cm. Nelle misure di superficie ogni passo vale <b>100</b>: 1 m² = 100 dm² = 10 000 cm².",
         "Area del <b>rettangolo</b> = base %s altezza. Area del <b>quadrato</b> = lato %s lato." % (FOIS, FOIS),
         "Figure con la stessa area si chiamano <b>equiestese</b>: possono avere forme e perimetri diversi."],
        [("Rettangolo 8 cm × 5 cm", ["area: 8 %s 5 = 40 cm²" % FOIS, "perimetro: (8 + 5) %s 2 = 26 cm" % FOIS], "40 cm²")],
        [["Confondere area e perimetro", "Area: superficie (cm²). Perimetro: contorno (cm)."],
         ["Scrivere 40 cm invece di 40 cm²", "L’area si misura in unità quadrate."],
         ["Contare passi da 10 nelle equivalenze di superficie", "Ogni passo vale 100: 3 m² = 300 dm²."]],
        table(["m²", "dm²", "cm²"], [["1", "100", "10 000"], ["", "1", "100"]]))
    faq = [("Perché nelle misure di superficie i passi valgono 100?", "Perché un quadrato di 1 dm di lato contiene 10 file da 10 quadratini di 1 cm: 10 × 10 = 100 cm²."),
           ("Due figure con lo stesso perimetro hanno la stessa area?", "Non sempre: un rettangolo 9 × 1 e un quadrato 5 × 5 hanno perimetro 20 ma aree 9 e 25.")]
    make_unit(R, "area", "S",
              "Determinare l’area di rettangoli e figure per scomposizione o utilizzando le più comuni formule; conoscere le unità di misura di superficie; distinguere area e perimetro",
              "L’area di rettangolo e quadrato", "Area",
              "Schede di matematica per la classe quarta sull’area: superficie con i quadretti, cm², dm², m² ed equivalenze, area di rettangolo e quadrato, formule inverse, figure equiestese, problemi. 100 esercizi con soluzioni.",
              "Area del rettangolo = base × altezza.", "L’area si misura in cm², dm², m².",
              body, faq, sets, 18, grade=G)


if __name__ == "__main__":
    main()
