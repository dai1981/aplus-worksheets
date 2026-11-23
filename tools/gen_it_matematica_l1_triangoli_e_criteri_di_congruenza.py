# -*- coding: utf-8 -*-
"""
Italia Matematica prima liceo: Triangoli e criteri di congruenza (Geometria)
  python3 tools/gen_it_matematica_l1_triangoli_e_criteri_di_congruenza.py
Enti geometrici e definizioni, angoli complementari, supplementari, esplementari, opposti al vertice, classificazione dei triangoli,
criteri di congruenza (LAL, ALA, LLL), triangolo isoscele, disuguaglianza triangolare, relazione tra lati e angoli.
Errori: LLA come criterio, angoli alla base dell’isoscele, accettare 3, 4, 8 come lati di un triangolo.
"""
import random
from it_liceo import M, L, unit, mix, table, W, fq, figure

R = random.Random(72111)
G = "prima-liceo"


def s1_ang():
    a = R.randint(10, 170)
    k = R.choice(["compl", "suppl", "espl", "opp"])
    if k == "compl":
        a = R.randint(5, 85)
        v, w, e = 90 - a, [180 - a, 360 - a, a], "Complementari: la somma è 90°, quindi 90° − %d° = <b>%d°</b>." % (a, 90 - a)
        q = "Qual è il complementare di un angolo di %d°?" % a
    elif k == "suppl":
        v, w, e = 180 - a, [abs(90 - a), 360 - a, a, 90 + a if a < 90 else a - 45], "Supplementari: la somma è 180°, quindi 180° − %d° = <b>%d°</b>." % (a, 180 - a)
        q = "Qual è il supplementare di un angolo di %d°?" % a
    elif k == "espl":
        v, w, e = 360 - a, [180 - a, 90 + a, a + 180], "Esplementari: la somma è 360°, quindi 360° − %d° = <b>%d°</b>." % (a, 360 - a)
        q = "Qual è l’esplementare di un angolo di %d°?" % a
    else:
        v, w, e = a, [180 - a, 90 - a if a < 90 else a - 90, 360 - a], "Gli angoli opposti al vertice sono congruenti: <b>%d°</b>." % a
        q = "Due rette si incontrano e formano un angolo di %d°. Quanto misura l’angolo opposto al vertice?" % a
    return M(q, "%d°" % v, ["%d°" % x for x in w if x != v and x > 0], e)


def s1_ang2():
    k = R.choice(["doppio", "diff"])
    if k == "doppio":
        m = R.choice([2, 3, 4, 5])
        tot = R.choice([90, 180])
        x = tot / (m + 1)
        if x != int(x):
            return None
        x = int(x)
        q = "Due angoli %s sono uno il %s dell’altro. Quanto misura il minore?" % ("complementari" if tot == 90 else "supplementari", {2: "doppio", 3: "triplo", 4: "quadruplo", 5: "quintuplo"}[m])
        return M(q, "%d°" % x, ["%d°" % v for v in (m * x, tot // m, tot - m * x if tot - m * x != x else x + 10)], "x + %dx = %d° → x = <b>%d°</b>." % (m, tot, x))
    tot = R.choice([90, 180])
    dd = R.choice([10, 20, 30, 40, 50]) if tot == 180 else R.choice([10, 20, 30, 40])
    x = (tot - dd) // 2
    q = "Due angoli %s differiscono di %d°. Quanto misura il maggiore?" % ("complementari" if tot == 90 else "supplementari", dd)
    return M(q, "%d°" % (x + dd), ["%d°" % v for v in (x, tot - dd, (tot + dd) // 2 + dd, tot - x - dd + 10)], "x + (x + %d°) = %d° → x = %d°: il maggiore è <b>%d°</b>." % (dd, tot, x, x + dd))


def s2_class():
    k = R.choice(["lati", "ang"])
    if k == "lati":
        t = R.choice(["equi", "iso", "scal"])
        a = R.randint(3, 12)
        sides = {"equi": (a, a, a), "iso": (a, a, R.choice([x for x in range(2, 2 * a) if x != a])), "scal": tuple(sorted(R.sample(range(3, 14), 3)))}[t]
        if t == "scal" and sides[0] + sides[1] <= sides[2]:
            return None
        ans = {"equi": "equilatero", "iso": "isoscele", "scal": "scaleno"}[t]
        return M("Un triangolo ha i lati di %d cm, %d cm e %d cm. Com’è rispetto ai lati?" % sides, ans, [x for x in ["equilatero", "isoscele", "scaleno", "rettangolo"] if x != ans],
                 "Lati tutti uguali: equilatero; due uguali: isoscele; tutti diversi: scaleno. Qui è <b>%s</b>." % ans)
    t = R.choice(["acut", "rett", "ott"])
    if t == "rett":
        a = R.randint(20, 70)
        angs = (90, a, 90 - a)
    elif t == "acut":
        a, b = R.randint(50, 85), R.randint(50, 85)
        if 180 - a - b >= 90 or 180 - a - b <= 0:
            return None
        angs = (a, b, 180 - a - b)
    else:
        a = R.randint(95, 150)
        b = R.randint(5, 180 - a - 5)
        angs = (a, b, 180 - a - b)
    ang = list(angs)
    R.shuffle(ang)
    ans = {"acut": "acutangolo", "rett": "rettangolo", "ott": "ottusangolo"}[t]
    return M("Due angoli di un triangolo misurano %d° e %d°. Com’è il triangolo rispetto agli angoli?" % (ang[0], ang[1]), ans, [x for x in ["acutangolo", "rettangolo", "ottusangolo", "equiangolo"] if x != ans],
             "Il terzo angolo è 180° − %d° − %d° = %d°. %s: <b>%s</b>." % (ang[0], ang[1], ang[2], "Un angolo retto" if t == "rett" else "Un angolo ottuso" if t == "ott" else "Tutti gli angoli acuti", ans))


CRIT = [("AB ≅ A′B′, AC ≅ A′C′ e l’angolo A ≅ A′", "primo criterio (LAL)"),
        ("BC ≅ B′C′, l’angolo B ≅ B′ e l’angolo C ≅ C′", "secondo criterio (ALA)"),
        ("AB ≅ A′B′, BC ≅ B′C′ e AC ≅ A′C′", "terzo criterio (LLL)"),
        ("BA ≅ B′A′, BC ≅ B′C′ e l’angolo B ≅ B′", "primo criterio (LAL)"),
        ("AB ≅ A′B′, l’angolo A ≅ A′ e l’angolo B ≅ B′", "secondo criterio (ALA)"),
        ("AB ≅ A′B′, AC ≅ A′C′ e l’angolo B ≅ B′", "nessun criterio (due lati e un angolo non compreso)"),
        ("l’angolo A ≅ A′, l’angolo B ≅ B′ e l’angolo C ≅ C′", "nessun criterio (tre angoli non bastano)"),
        ("CA ≅ C′A′, CB ≅ C′B′ e l’angolo C ≅ C′", "primo criterio (LAL)"),
        ("AC ≅ A′C′, l’angolo A ≅ A′ e l’angolo C ≅ C′", "secondo criterio (ALA)")]
ALL_C = ["primo criterio (LAL)", "secondo criterio (ALA)", "terzo criterio (LLL)", "nessun criterio (due lati e un angolo non compreso)"]


def s2_crit():
    hyp, ans = R.choice(CRIT)
    w = [c for c in ALL_C if c != ans]
    if ans.startswith("nessun") and "tre angoli" in ans:
        w = ALL_C[:3]
    pts = {"A": (0, 0), "B": (5, 0), "C": (1.6, 3.2)}
    fig = figure(pts, [("A", "B"), ("B", "C"), ("C", "A")], W=260, H=170, label="triangolo ABC")
    return M("%sNei triangoli ABC e A′B′C′ si sa che %s. Quale criterio permette di dire che sono congruenti?" % (fig, hyp), ans, w,
             "LAL: due lati e l’angolo <b>compreso</b>; ALA: un lato e i due angoli <b>adiacenti</b>; LLL: tre lati. Qui: <b>%s</b>." % ans)


def s3_iso():
    k = R.choice(["vert", "base", "ext"])
    if k == "vert":
        v = R.choice(range(20, 160, 2))
        b = (180 - v) // 2
        return M("In un triangolo isoscele l’angolo al vertice misura %d°. Quanto misura ciascun angolo alla base?" % v, "%d°" % b, ["%d°" % x for x in (180 - v, v, 90 - v // 2 + 10 if 90 - v // 2 + 10 != b else b + 5)],
                 "Gli angoli alla base sono congruenti: (180° − %d°) : 2 = <b>%d°</b>." % (v, b))
    if k == "base":
        b = R.choice([x for x in range(20, 86) if x != 60])
        v = 180 - 2 * b
        return M("In un triangolo isoscele un angolo alla base misura %d°. Quanto misura l’angolo al vertice?" % b, "%d°" % v, ["%d°" % x for x in (180 - b, b, 90 - b if 90 - b != v else v + 10)],
                 "Gli angoli alla base sono due e congruenti: 180° − 2 · %d° = <b>%d°</b>." % (b, v))
    a = R.randint(3, 15)
    b = R.randint(2, 2 * a - 1)
    per = 2 * a + b
    return M("Un triangolo isoscele ha perimetro %d cm e base %d cm. Quanto misura ciascun lato obliquo?" % (per, b), "%s cm" % fq(a), ["%s cm" % fq(x) for x in (per - b, per // 3 if per // 3 != a else a + 1, b)],
             "(%d − %d) : 2 = <b>%d cm</b>." % (per, b, a))


def s4_dis():
    k = R.choice(["si", "terzo"])
    if k == "si":
        a, b = R.randint(2, 12), R.randint(2, 12)
        c = R.choice([a + b, a + b + R.randint(1, 4), abs(a - b) + R.randint(1, max(1, a + b - abs(a - b) - 1))])
        ok = abs(a - b) < c < a + b
        ans = "sì" if ok else "no"
        return M("Esiste un triangolo con i lati di %d cm, %d cm e %d cm?" % tuple(sorted([a, b, c])), ans, ["no" if ok else "sì", "solo se è rettangolo", "solo se è isoscele"],
                 "Disuguaglianza triangolare: ogni lato è minore della somma degli altri due. %s: <b>%s</b>." % ("Vale per tutti i lati" if ok else "Il lato maggiore (%d) non è minore di %d + %d" % (max(a, b, c), sorted([a, b, c])[0], sorted([a, b, c])[1]), ans))
    a, b = sorted(R.sample(range(3, 15), 2))
    ans = "%d cm &lt; c &lt; %d cm" % (b - a, a + b)
    w = ["%d cm ≤ c ≤ %d cm" % (b - a, a + b), "0 cm &lt; c &lt; %d cm" % (a + b), "%d cm &lt; c &lt; %d cm" % (a, b)]
    return M("Due lati di un triangolo misurano %d cm e %d cm. Quali valori può avere il terzo lato c?" % (a, b), ans, w,
             "Il terzo lato è maggiore della differenza e minore della somma: <b>%s</b>." % ans)


def s4_rel():
    a, b, c = sorted(R.sample(range(4, 20), 3))
    if a + b <= c:
        return None
    names = R.sample(["AB", "BC", "AC"], 3)
    opp = {"AB": "C", "BC": "A", "AC": "B"}
    L_ = dict(zip(names, (a, b, c)))
    big = max(L_, key=L_.get)
    sm = min(L_, key=L_.get)
    k = R.choice(["max", "min"])
    if k == "max":
        ans = "l’angolo %s" % opp[big]
        return M("Nel triangolo ABC: %s. Qual è l’angolo maggiore?" % ", ".join("%s = %d cm" % (n, L_[n]) for n in sorted(L_)), ans,
                 ["l’angolo %s" % v for v in "ABC" if v != opp[big]] + ["sono tutti uguali"],
                 "L’angolo maggiore è opposto al lato maggiore (%s): <b>%s</b>." % (big, ans))
    ans = "l’angolo %s" % opp[sm]
    return M("Nel triangolo ABC: %s. Qual è l’angolo minore?" % ", ".join("%s = %d cm" % (n, L_[n]) for n in sorted(L_)), ans,
             ["l’angolo %s" % v for v in "ABC" if v != opp[sm]] + ["sono tutti uguali"],
             "L’angolo minore è opposto al lato minore (%s): <b>%s</b>." % (sm, ans))


DEF = [("Che cosa sono il punto, la retta e il piano?", "enti primitivi (non si definiscono)", ["teoremi", "postulati da dimostrare", "figure composte da segmenti"]),
       ("Che cos’è un teorema?", "un’affermazione che si dimostra a partire da ipotesi, assiomi e teoremi già noti", ["un’affermazione vera che si accetta senza dimostrarla", "una definizione", "un disegno che mostra una proprietà"]),
       ("Che cos’è un assioma (postulato)?", "una proprietà che si accetta come vera senza dimostrarla", ["un teorema già dimostrato", "una definizione di un ente primitivo", "il contrario di un teorema"]),
       ("Quante rette passano per due punti distinti?", "una e una sola", ["infinite", "due", "nessuna"]),
       ("Due figure sono congruenti se…", "si possono sovrapporre con un movimento rigido", ["hanno la stessa area", "hanno lo stesso perimetro", "hanno gli stessi angoli"]),
       ("Che cos’è la bisettrice di un angolo?", "la semiretta che divide l’angolo in due angoli congruenti", ["la retta perpendicolare a un lato", "il segmento che unisce il vertice al punto medio", "un lato dell’angolo"]),
       ("Che cos’è la mediana di un triangolo?", "il segmento dal vertice al punto medio del lato opposto", ["la perpendicolare dal vertice al lato opposto", "la bisettrice di un angolo", "la retta perpendicolare al lato nel suo punto medio"]),
       ("Che cos’è l’altezza di un triangolo?", "il segmento perpendicolare condotto da un vertice alla retta del lato opposto", ["il lato più lungo", "il segmento dal vertice al punto medio del lato opposto", "la bisettrice dell’angolo al vertice"]),
       ("In una dimostrazione, che cosa sono l’ipotesi e la tesi?", "ciò che si suppone vero e ciò che si deve dimostrare", ["due teoremi", "due assiomi", "la figura e il disegno"]),
       ("Due segmenti sono consecutivi se…", "hanno in comune solo un estremo", ["stanno sulla stessa retta", "sono congruenti", "si incontrano nel punto medio"])]


def s5_def():
    q, a, w = R.choice(DEF)
    return M(q, a, w, "%s: <b>%s</b>." % (q.rstrip("?…"), a))


def main():
    seen = set()
    sets = [
        ("Enti geometrici e angoli", mix(R, seen, [(s5_def, 8), (s1_ang, 12)])),
        ("Problemi con gli angoli e classificazione", mix(R, seen, [(s1_ang2, 10), (s2_class, 10)])),
        ("Criteri di congruenza", mix(R, seen, [(s2_crit, 9), (s3_iso, 11)])),
        ("Disuguaglianza triangolare", mix(R, seen, [(s4_dis, 14), (s1_ang, 6)])),
        ("Lati e angoli", mix(R, seen, [(s4_rel, 12), (s3_iso, 8)])),
    ]
    body = L(["La geometria euclidea parte da <b>enti primitivi</b> (punto, retta, piano) e da <b>assiomi</b> accettati senza dimostrazione; le altre proprietà, i <b>teoremi</b>, si dimostrano.",
              "Angoli <b>complementari</b>: somma 90°; <b>supplementari</b>: 180°; <b>esplementari</b>: 360°. Gli angoli <b>opposti al vertice</b> sono congruenti.",
              "Due triangoli sono congruenti se hanno: due lati e l’angolo compreso (<b>LAL</b>), un lato e i due angoli adiacenti (<b>ALA</b>), tre lati (<b>LLL</b>). Tre angoli non bastano.",
              "Nel triangolo isoscele gli angoli alla base sono congruenti. Ogni lato è minore della somma degli altri due; l’angolo maggiore è opposto al lato maggiore."],
             [("Lati 4 cm e 9 cm: il terzo lato?", ["9 − 4 &lt; c &lt; 9 + 4"], "5 cm &lt; c &lt; 13 cm"),
              ("Isoscele con angolo al vertice 40°", ["(180° − 40°) : 2"], "70° alla base")],
             [["Usare due lati e un angolo qualsiasi", "Nel primo criterio l’angolo deve essere compreso tra i due lati."],
              ["Lati 3, 4, 8 formano un triangolo", "4 + 3 &lt; 8: non esiste."],
              ["Confondere complementare e supplementare", "Complementare: fino a 90°; supplementare: fino a 180°."]])
    faq = [("Perché tre angoli uguali non bastano per la congruenza?", "Perché un triangolo grande e uno piccolo con la stessa forma hanno gli stessi angoli ma lati diversi: sono simili, non congruenti."),
           ("A che cosa servono i criteri di congruenza?", "A dimostrare che due triangoli sono congruenti senza controllare tutti i lati e gli angoli; da qui si ricavano altre uguaglianze (lati e angoli corrispondenti).")]
    unit(G, R, "triangoli-e-criteri-di-congruenza", "G",
         "Gli enti fondamentali della geometria e il significato dei termini postulato, assioma, definizione, teorema, dimostrazione; congruenza dei triangoli",
         "Triangoli e criteri di congruenza", "Triangoli e congruenza",
         "Schede di matematica per la prima liceo sui triangoli: enti geometrici, angoli complementari e supplementari, classificazione dei triangoli, criteri di congruenza, triangolo isoscele, disuguaglianza triangolare. 100 esercizi con soluzioni.",
         "LAL, ALA, LLL", "Due lati e l’angolo compreso, un lato e i due angoli adiacenti, tre lati.",
         body, faq, sets, 11)


if __name__ == "__main__":
    main()
