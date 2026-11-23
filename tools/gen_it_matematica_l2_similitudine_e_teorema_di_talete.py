# -*- coding: utf-8 -*-
"""
Italia Matematica seconda liceo: Similitudine e teorema di Talete (Geometria)
  python3 tools/gen_it_matematica_l2_similitudine_e_teorema_di_talete.py
Grandezze proporzionali, teorema di Talete (parallela a un lato di un triangolo), teorema della bisettrice,
criteri di similitudine dei triangoli, rapporto di similitudine per lati, perimetri e aree,
teoremi delle corde, delle secanti e della tangente, ombre e altezze.
Errori: rapporto delle aree uguale a k, proporzione con i lati non corrispondenti, teorema delle corde con le somme.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, d, figure

R = random.Random(72211)
G = "seconda-liceo"


def dd(x):
    try:
        return d(x)
    except ValueError:
        return None


def s1_tri():
    a, b, c = R.choice([(4, 6, 8), (5, 7, 9), (3, 5, 6), (6, 8, 10), (4, 5, 7), (2, 3, 4)])
    k = R.choice([Fr(3, 2), Fr(2), Fr(5, 2), Fr(3), Fr(1, 2)])
    which = R.choice(["b", "c"])
    A2 = a * k
    if A2.denominator != 1 and dd(A2) is None:
        return None
    v = (b if which == "b" else c) * k
    if dd(v) is None:
        return None
    return M("I triangoli ABC e A′B′C′ sono simili (A corrisponde ad A′, B a B′, C a C′). AB = %d cm, %s = %d cm e A′B′ = %s cm. Quanto misura %s?" % (a, "BC" if which == "b" else "AC", b if which == "b" else c, d(A2), "B′C′" if which == "b" else "A′C′"),
             "%s cm" % d(v), ["%s cm" % x for x in [dd(v + 1), dd((b if which == "b" else c) + A2 - a), dd((b if which == "b" else c) / k), dd(v * 2), dd(Fr(v, 2) + 1)] if x and x != d(v)],
             "Rapporto di similitudine k = A′B′ : AB = %s : %d = %s; il lato corrispondente misura %d · %s = <b>%s cm</b>." % (d(A2), a, d(k), b if which == "b" else c, d(k), d(v)))


def s1_rapp():
    k = R.choice([2, 3, 4, 5, Fr(3, 2), Fr(1, 2), Fr(2, 3)])
    t = R.choice(["per", "area"])
    v0 = R.choice([12, 18, 24, 30, 36, 40, 48, 54])
    if t == "per":
        v = v0 * k
        if dd(v) is None:
            return None
        return M("Due poligoni simili hanno rapporto di similitudine %s. Il perimetro del primo è %d cm. Quanto misura il perimetro del secondo?" % (fq(k), v0), "%s cm" % d(v), ["%s cm" % x for x in [dd(v0 * k * k), dd(v0 + k), dd(v0 / k), dd(v * 2)] if x and x != d(v)],
                 "I perimetri stanno nello stesso rapporto dei lati: %d · %s = <b>%s cm</b>." % (v0, fq(k), d(v)))
    v = v0 * k * k
    if dd(v) is None:
        return None
    return M("Due poligoni simili hanno rapporto di similitudine %s. L’area del primo è %d cm². Quanto misura l’area del secondo?" % (fq(k), v0), "%s cm²" % d(v), ["%s cm²" % x for x in [dd(v0 * k), dd(v0 * k * 2), dd(v0 / (k * k)), dd(v0 + k * k)] if x and x != d(v)],
             "Le aree stanno nel rapporto dei quadrati: k² = %s, quindi %d · %s = <b>%s cm²</b>." % (fq(k * k), v0, fq(k * k), d(v)))


CRIT = [("hanno due angoli rispettivamente congruenti", "primo criterio (AA)"),
        ("hanno due lati in proporzione e l’angolo compreso congruente", "secondo criterio (LAL)"),
        ("hanno i tre lati in proporzione", "terzo criterio (LLL)"),
        ("hanno un angolo di 40° e un angolo di 75° ciascuno", "primo criterio (AA)"),
        ("hanno lati 3, 4, 6 e 6, 8, 12", "terzo criterio (LLL)"),
        ("hanno AB/A′B′ = AC/A′C′ = 2 e l’angolo A congruente ad A′", "secondo criterio (LAL)")]


def s2_crit():
    t, a = R.choice(CRIT)
    return M("Due triangoli %s. Con quale criterio sono simili?" % t, a, [x for x in ["primo criterio (AA)", "secondo criterio (LAL)", "terzo criterio (LLL)", "non sono simili"] if x != a],
             "Similitudine: due angoli congruenti (AA), due lati in proporzione e l’angolo compreso (LAL), tre lati in proporzione (LLL). Qui: <b>%s</b>." % a)


def s2_talete():
    AD, DB = R.randint(2, 9), R.randint(2, 9)
    AE = R.randint(2, 12)
    EC = Fr(AE * DB, AD)
    if dd(EC) is None:
        return None
    fig = figure({"A": (2, 4), "B": (0, 0), "C": (6, 0), "D": (2 - 2 * AD / (AD + DB), 4 - 4 * AD / (AD + DB)), "E": (2 + 4 * AD / (AD + DB), 4 - 4 * AD / (AD + DB))},
                 [("A", "B"), ("B", "C"), ("C", "A"), ("D", "E")], W=260, H=180, label="triangolo con una parallela a un lato")
    return M("%sNel triangolo ABC la retta DE è parallela a BC. AD = %d cm, DB = %d cm, AE = %d cm. Quanto misura EC?" % (fig, AD, DB, AE), "%s cm" % d(EC), ["%s cm" % x for x in [dd(Fr(AE * AD, DB)), dd(Fr(DB + AE - AD)) if DB + AE > AD else None, dd(Fr(AE * (AD + DB), AD)), dd(EC * 2), dd(Fr(AE * AD, AD + DB))] if x and x != d(EC)],
             "Teorema di Talete: AD : DB = AE : EC → %d : %d = %d : EC → EC = <b>%s cm</b>." % (AD, DB, AE, d(EC)))


def s3_bis():
    AB, AC = R.sample(range(4, 16), 2)
    BC = R.randint(abs(AB - AC) + 1, AB + AC - 1)
    BD = Fr(BC * AB, AB + AC)
    if dd(BD) is None:
        return None
    return M("Nel triangolo ABC, AB = %d cm, AC = %d cm, BC = %d cm. La bisettrice dell’angolo A incontra BC in D. Quanto misura BD?" % (AB, AC, BC), "%s cm" % d(BD), ["%s cm" % x for x in [dd(Fr(BC, 2)), dd(Fr(BC * AC, AB + AC)), dd(Fr(AB * AC, BC)), dd(Fr(BC * AB, AC)), dd(BD + 1)] if x and x != d(BD)],
             "Teorema della bisettrice: BD : DC = AB : AC = %d : %d. BD = %d · %d/%d = <b>%s cm</b>." % (AB, AC, BC, AB, AB + AC, d(BD)))


def s4_corde():
    k = R.choice(["corde", "secanti", "tang"])
    if k == "corde":
        a, b = R.randint(2, 12), R.randint(2, 12)
        c = R.choice([x for x in range(2, 13) if (a * b) % x == 0] or [a])
        dv = Fr(a * b, c)
        return M("Due corde AB e CD si incontrano in P. PA = %d cm, PB = %d cm, PC = %d cm. Quanto misura PD?" % (a, b, c), "%s cm" % d(dv), ["%s cm" % x for x in [dd(Fr(a + b - c)) if a + b > c else None, dd(Fr(a * c, b)), dd(Fr(b * c, a))] if x and x != d(dv)],
                 "Teorema delle corde: PA · PB = PC · PD → %d · %d = %d · PD → <b>PD = %s cm</b>." % (a, b, c, d(dv)))
    if k == "secanti":
        pa, ab = R.randint(2, 8), R.randint(2, 10)
        pb = pa + ab
        cands = [x for x in range(2, 15) if (pa * pb) % x == 0 and x not in (pa, pb)]
        if not cands:
            return None
        pc = R.choice(cands)
        pd = Fr(pa * pb, pc)
        return M("Da un punto P esterno a una circonferenza partono due secanti: una incontra la circonferenza in A e B (PA = %d cm, PB = %d cm), l’altra in C e D con PC = %d cm. Quanto misura PD?" % (pa, pb, pc), "%s cm" % d(pd), ["%s cm" % x for x in [dd(Fr(pa * ab, pc)), dd(Fr(pc * pb, pa)), dd(Fr(pa + pb - pc)) if pa + pb > pc else None] if x and x != d(pd)],
                 "Teorema delle secanti: PA · PB = PC · PD → %d · %d = %d · PD → <b>PD = %s cm</b>." % (pa, pb, pc, d(pd)))
    pa, pb = R.choice([(1, 4), (2, 8), (4, 9), (3, 12), (4, 16), (1, 9), (2, 18), (9, 16), (5, 20)])
    t = int((pa * pb) ** 0.5)
    return M("Da un punto P si conducono una tangente PT e una secante che incontra la circonferenza in A e B, con PA = %d cm e PB = %d cm. Quanto misura PT?" % (pa, pb), "%d cm" % t, ["%s cm" % x for x in [dd(Fr(pa + pb, 2)), pb - pa, t + 1] if x and str(x) != str(t)],
             "Teorema della tangente e della secante: PT² = PA · PB = %d → <b>PT = %d cm</b>." % (pa * pb, t))


def s5_ombre():
    h1, o1 = R.choice([(2, 3), (1, 2), (3, 4), (2, 5), (4, 3), (1, 3)])
    o2 = o1 * R.randint(2, 8)
    h2 = Fr(h1 * o2, o1)
    obj = R.choice(["un albero", "un lampione", "un campanile", "un palazzo"])
    return M("Un bastone alto %d m proietta un’ombra di %d m. Nello stesso momento %s proietta un’ombra di %d m. Quanto è alto?" % (h1, o1, obj, o2), "%s m" % d(h2), ["%s m" % x for x in [dd(Fr(o2 * o1, h1)), dd(Fr(o2 + h1 - o1)) if o2 + h1 > o1 else None, dd(h2 + 1), dd(h2 * 2), dd(Fr(o2, h1))] if x and x != d(h2)],
             "I raggi del Sole sono paralleli: i triangoli sono simili. %d : %d = h : %d → h = <b>%s m</b>." % (h1, o1, o2, d(h2)))


def main():
    seen = set()
    sets = [
        ("Triangoli simili", mix(R, seen, [(s1_tri, 14), (s2_crit, 6)])),
        ("Perimetri e aree", mix(R, seen, [(s1_rapp, 20)])),
        ("Teorema di Talete e della bisettrice", mix(R, seen, [(s2_talete, 10), (s3_bis, 10)])),
        ("Corde, secanti e tangenti", mix(R, seen, [(s4_corde, 20)])),
        ("Problemi di similitudine", mix(R, seen, [(s5_ombre, 10), (s1_tri, 6), (s2_talete, 4)])),
    ]
    body = L(["Due figure sono <b>simili</b> se hanno gli angoli congruenti e i lati corrispondenti in proporzione. Il rapporto costante k è il <b>rapporto di similitudine</b>.",
              "Due triangoli sono simili se hanno: due angoli congruenti (AA), due lati in proporzione e l’angolo compreso congruente (LAL), tre lati in proporzione (LLL).",
              "I perimetri stanno nel rapporto k, le aree nel rapporto <b>k²</b>. <b>Talete</b>: una parallela a un lato di un triangolo taglia gli altri due lati in parti proporzionali.",
              "Nella circonferenza: <b>corde</b> PA · PB = PC · PD; <b>secanti</b> PA · PB = PC · PD; <b>tangente</b> PT² = PA · PB."],
             [("k = 3, area 10 cm²", ["Le aree stanno come k² = 9"], "90 cm²"),
              ("AD = 4, DB = 6, AE = 6 con DE ∥ BC", ["4 : 6 = 6 : EC"], "EC = 9")],
             [["Aree nel rapporto k", "Le aree si moltiplicano per k²."],
              ["Proporzione con lati non corrispondenti", "Abbina i lati opposti ad angoli congruenti."],
              ["PA + PB = PC + PD", "Nel teorema delle corde ci sono i prodotti."]])
    faq = [("Perché le aree stanno nel rapporto k²?", "Perché l’area è il prodotto di due lunghezze (base e altezza), e ciascuna è moltiplicata per k: l’area è moltiplicata per k · k = k²."),
           ("Due triangoli congruenti sono simili?", "Sì, con rapporto di similitudine k = 1. La congruenza è un caso particolare della similitudine.")]
    unit(G, R, "similitudine-e-teorema-di-talete", "G",
         "Grandezze proporzionali e teorema di Talete; similitudine dei triangoli e dei poligoni; teoremi delle corde, delle secanti e della tangente",
         "Similitudine e teorema di Talete", "Similitudine e Talete",
         "Schede di matematica per la seconda liceo su similitudine e teorema di Talete: triangoli simili e criteri, rapporto tra perimetri e aree, teorema di Talete e della bisettrice, teoremi delle corde, delle secanti e della tangente, problemi. 100 esercizi con soluzioni.",
         "Lati: k. Aree: k².", "Due angoli congruenti bastano per la similitudine di due triangoli.",
         body, faq, sets, 11)


if __name__ == "__main__":
    main()
