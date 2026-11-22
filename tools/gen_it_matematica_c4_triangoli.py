# -*- coding: utf-8 -*-
"""
Italia Matematica classe quarta: I triangoli (Spazio e figure)
  python3 tools/gen_it_matematica_c4_triangoli.py
Classificare i triangoli rispetto ai lati (equilatero, isoscele, scaleno) e agli angoli (acutangolo, rettangolo,
ottusangolo); la somma degli angoli interni è 180°; condizione di esistenza; altezze; perimetro.
Errori: chiamare rettangolo un triangolo «dritto», sommare gli angoli a 360°, credere che ogni triangolo con un lato lungo sia ottusangolo.
"""
import random
from it_common import mcq, lesson, make_unit, mix, table, relabel, fig
import gen_au_maths_y5_angles as AU

R = random.Random(70415)
G = "classe-quarta"
LATI = ["equilatero", "isoscele", "scaleno"]
ANGOLI = ["acutangolo", "rettangolo", "ottusangolo"]


def tri(a, b, rot=0, texts=None, ticks=(), base=150):
    pts = AU.tri_pts(a, b, base, rot)
    c = 180 - a - b
    rights = tuple(i for i, v in enumerate((a, b, c)) if v == 90 and (not texts or i not in texts))
    return relabel(AU.shape_svg(pts, texts or {}, "un triangolo", rights=rights, ticks=ticks), "un triangolo")


def by_sides():
    k = R.choice(LATI)
    if k == "equilatero":
        return k, 60, 60, ((0, 1), (1, 1), (2, 1))
    if k == "isoscele":
        a = R.choice([35, 40, 50, 55, 65, 70, 75])
        return k, a, a, ((1, 1), (2, 1))
    while True:
        a, b = R.randint(30, 80), R.randint(30, 80)
        if abs(a - b) >= 12 and abs(180 - a - b - a) >= 12 and abs(180 - a - b - b) >= 12 and 180 - a - b != 90:
            return k, a, b, ()


def s1_lati():
    k, a, b, ticks = by_sides()
    if R.random() < 0.5:
        pic = fig(tri(a, b, R.choice([0, 0, 10, -10]), ticks=ticks))
        return mcq(pic + "I trattini indicano i lati uguali. Che triangolo è rispetto ai lati?", k, [x for x in LATI if x != k] + ["rettangolo"],
                   "%s: è <b>%s</b>." % ({"equilatero": "Tre lati uguali", "isoscele": "Due lati uguali", "scaleno": "Nessun lato uguale"}[k], k))
    if k == "equilatero":
        l = [R.randint(3, 12)] * 3
    elif k == "isoscele":
        x, y = R.sample(range(4, 13), 2)
        if 2 * x <= y:
            return None
        l = [x, x, y]
        R.shuffle(l)
    else:
        l = R.sample(range(4, 14), 3)
        if max(l) >= sum(l) - max(l):
            return None
    return mcq("Un triangolo ha i lati di %s cm. Che triangolo è?" % ", ".join(map(str, l)), k, [x for x in LATI if x != k] + ["ottusangolo"],
               "%s: è <b>%s</b>." % ({"equilatero": "Tre lati uguali", "isoscele": "Due lati uguali", "scaleno": "Tre lati diversi"}[k], k))


def s2_angoli():
    k = R.choice(ANGOLI)
    if k == "acutangolo":
        while True:
            a, b = R.randint(45, 80), R.randint(45, 80)
            if 180 - a - b < 90 and 180 - a - b >= 25:
                break
    elif k == "rettangolo":
        a, b = 90, R.randint(25, 65)
    else:
        a, b = R.randint(100, 130), R.randint(20, 40)
    c = 180 - a - b
    angs = [a, b, c]
    if R.random() < 0.5:
        rot = R.choice([0, 0, 15, -15])
        texts = {i: "%d°" % v for i, v in enumerate(angs) if v != 90}
        pic = fig(tri(a, b, rot, texts=texts))
        q = "Che triangolo è rispetto agli angoli?"
    else:
        R.shuffle(angs)
        pic = ""
        q = "Un triangolo ha gli angoli di %s. Che triangolo è rispetto agli angoli?" % ", ".join("%d°" % v for v in angs)
    return mcq(pic + q, k, [x for x in ANGOLI if x != k] + ["isoscele"],
               "%s: è <b>%s</b>." % ({"acutangolo": "Tre angoli acuti", "rettangolo": "Un angolo retto (90°)", "ottusangolo": "Un angolo ottuso (più di 90°)"}[k], k))


def s3_terzo():
    a, b = R.randint(25, 95), R.randint(25, 95)
    c = 180 - a - b
    if c < 15:
        return None
    if R.random() < 0.55 and 90 not in (a, b, c):
        pic = fig(tri(a, b, R.choice([0, 10, -10]), texts={0: "%d°" % a, 1: "%d°" % b, 2: "?"}))
        q = pic + "Quanto misura l’angolo indicato con «?»?"
    else:
        q = "In un triangolo due angoli misurano %d° e %d°. Quanto misura il terzo angolo?" % (a, b)
    return mcq(q, "%d°" % c, ["%d°" % (360 - a - b), "%d°" % (a + b), "%d°" % (c + 10), "%d°" % abs(a - b) if abs(a - b) != c else "%d°" % (c - 10)],
               "La somma degli angoli interni di un triangolo è 180°: 180° − %d° − %d° = <b>%d°</b>." % (a, b, c))


def s3_speciali():
    k = R.choice(["eq", "rett", "iso", "iso2"])
    if k == "eq":
        return mcq("Quanto misura ogni angolo di un triangolo equilatero?", "60°", ["90°", "45°", "180°"], "Tre angoli uguali: 180° : 3 = <b>60°</b>.")
    if k == "rett":
        a = R.randint(15, 75)
        return mcq("In un triangolo rettangolo un angolo acuto misura %d°. Quanto misura l’altro angolo acuto?" % a, "%d°" % (90 - a),
                   ["%d°" % (180 - a), "%d°" % (270 - a), "%d°" % a if a != 90 - a else "%d°" % (a + 10)], "180° − 90° − %d° = <b>%d°</b>." % (a, 90 - a))
    if k == "iso":
        v = R.choice([20, 30, 40, 50, 60, 70, 80, 100, 110, 120])
        if v == 60:
            return None
        return mcq("In un triangolo isoscele l’angolo al vertice (tra i due lati uguali) misura %d°. Quanto misura ciascun angolo alla base?" % v, "%d°" % ((180 - v) // 2),
                   ["%d°" % (180 - v), "%d°" % v, "%d°" % ((360 - v) // 2)], "I due angoli alla base sono uguali: (180° − %d°) : 2 = <b>%d°</b>." % (v, (180 - v) // 2))
    b = R.choice([30, 40, 45, 50, 55, 65, 70, 75])
    return mcq("In un triangolo isoscele ogni angolo alla base misura %d°. Quanto misura l’angolo al vertice?" % b, "%d°" % (180 - 2 * b),
               ["%d°" % (180 - b), "%d°" % b, "%d°" % (90 - b)], "180° − %d° − %d° = <b>%d°</b>." % (b, b, 180 - 2 * b))


QUIZ = [("Un triangolo può avere due angoli retti?", "no, la somma supererebbe 180°", ["sì, se è isoscele", "sì, se è grande", "solo se è equilatero"]),
        ("Un triangolo equilatero è anche…", "isoscele", ["scaleno", "rettangolo", "ottusangolo"]),
        ("Quante altezze ha un triangolo?", "3", ["1", "2", "4"]),
        ("In un triangolo rettangolo, come si chiamano i due lati che formano l’angolo retto?", "cateti", ["ipotenuse", "basi", "diagonali"]),
        ("In un triangolo rettangolo, come si chiama il lato opposto all’angolo retto?", "ipotenusa", ["cateto", "altezza", "diagonale"]),
        ("Un triangolo ottusangolo quanti angoli ottusi ha?", "1", ["2", "3", "nessuno"]),
        ("Che cos’è l’altezza di un triangolo?", "il segmento che parte da un vertice ed è perpendicolare al lato opposto", ["il lato più lungo", "la metà della base", "il segmento che unisce due vertici"]),
        ("Un triangolo può essere rettangolo e isoscele insieme?", "sì, con gli angoli di 90°, 45° e 45°", ["no, mai", "solo se è equilatero", "solo se i lati sono lunghi"]),
        ("Quanto fa la somma degli angoli interni di un triangolo?", "180°", ["360°", "90°", "270°"])]


def s4_quiz():
    q, a, w = R.choice(QUIZ)
    return mcq(q, a, w, "Risposta: <b>%s</b>." % a)


def s4_esiste():
    a, b = R.randint(3, 10), R.randint(3, 10)
    c = R.choice([a + b + R.randint(0, 4), abs(a - b) + R.randint(1, 3), R.randint(3, 12)])
    ok = max(a, b, c) < a + b + c - max(a, b, c)
    s = sorted([a, b, c])
    return mcq("Con tre bastoncini lunghi %d cm, %d cm e %d cm si può costruire un triangolo?" % (a, b, c), "sì" if ok else "no",
               ["no" if ok else "sì", "solo se sono tutti uguali", "solo se due bastoncini sono uguali"],
               "Il lato più lungo deve essere minore della somma degli altri due: %d %s %d + %d = %d. <b>%s</b>." % (s[2], "&lt;" if ok else "≥", s[0], s[1], s[0] + s[1], "Sì" if ok else "No"))


def s5():
    k = R.choice(["perim_eq", "perim_iso", "lato_eq", "lato_iso", "esiste"])
    if k == "perim_eq":
        l = R.randint(4, 35)
        return mcq("Un cartello stradale ha la forma di un triangolo equilatero con il lato di %d cm. Qual è il perimetro?" % l, "%d cm" % (3 * l),
                   ["%d cm" % (2 * l), "%d cm" % (l * l), "%d cm" % (l + 3)], "Tre lati uguali: %d × 3 = <b>%d cm</b>." % (l, 3 * l))
    if k == "perim_iso":
        x, y = R.randint(6, 30), R.randint(4, 25)
        if 2 * x <= y:
            return None
        return mcq("Un triangolo isoscele ha i lati uguali di %d cm e la base di %d cm. Qual è il perimetro?" % (x, y), "%d cm" % (2 * x + y),
                   ["%d cm" % (x + y), "%d cm" % (2 * y + x), "%d cm" % (x * y)], "%d + %d + %d = <b>%d cm</b>." % (x, x, y, 2 * x + y))
    if k == "lato_eq":
        l = R.randint(4, 40)
        return mcq("Il perimetro di un triangolo equilatero è %d cm. Quanto è lungo un lato?" % (3 * l), "%d cm" % l,
                   ["%d cm" % (3 * l * 3), "%d cm" % (3 * l // 2), "%d cm" % (l + 3)], "%d : 3 = <b>%d cm</b>." % (3 * l, l))
    if k == "lato_iso":
        x, y = R.randint(6, 30), R.randint(4, 25)
        if 2 * x <= y:
            return None
        p = 2 * x + y
        return mcq("Un triangolo isoscele ha il perimetro di %d cm e la base di %d cm. Quanto è lungo ciascun lato uguale?" % (p, y), "%d cm" % x,
                   ["%d cm" % (p - y), "%d cm" % ((p - y) * 2), "%d cm" % (p // 3)], "(%d − %d) : 2 = <b>%d cm</b>." % (p, y, x))
    return s4_esiste()


def main():
    seen = set()
    sets = [
        ("Rispetto ai lati", mix(R, seen, [(s1_lati, 20)])),
        ("Rispetto agli angoli", mix(R, seen, [(s2_angoli, 20)])),
        ("La somma degli angoli", mix(R, seen, [(s3_terzo, 12), (s3_speciali, 8)])),
        ("Proprietà dei triangoli", mix(R, seen, [(s4_quiz, 9), (s4_esiste, 11)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Rispetto ai <b>lati</b> un triangolo è <b>equilatero</b> (3 lati uguali), <b>isoscele</b> (2 lati uguali) o <b>scaleno</b> (3 lati diversi).",
         "Rispetto agli <b>angoli</b> è <b>acutangolo</b> (3 angoli acuti), <b>rettangolo</b> (un angolo retto) o <b>ottusangolo</b> (un angolo ottuso).",
         "La somma degli angoli interni di ogni triangolo è <b>180°</b>.",
         "Si può costruire un triangolo solo se il lato più lungo è minore della somma degli altri due."],
        [("Due angoli misurano 50° e 75°. Il terzo?", ["50° + 75° = 125°", "180° − 125° = 55°"], "55°")],
        [["Chiamare «rettangolo» un triangolo appoggiato su un lato", "Rettangolo vuol dire che ha un angolo di 90°."],
         ["Sommare gli angoli a 360°", "360° è per i quadrilateri; nel triangolo 180°."],
         ["Pensare che un equilatero non sia isoscele", "Ha anche due lati uguali (anzi tre)."]],
        table(["Lati / Angoli", "acutangolo", "rettangolo", "ottusangolo"], [["equilatero", "sì", "no", "no"], ["isoscele", "sì", "sì", "sì"], ["scaleno", "sì", "sì", "sì"]]))
    faq = [("Perché la somma degli angoli di un triangolo è sempre 180°?", "Se strappi i tre angoli di un triangolo di carta e li metti uno accanto all’altro, formano un angolo piatto."),
           ("Un triangolo rettangolo può essere equilatero?", "No: in un equilatero gli angoli misurano tutti 60°, quindi nessuno è retto.")]
    make_unit(R, "triangoli", "S",
              "Descrivere, denominare e classificare figure geometriche, identificando elementi significativi e simmetrie; classificare i triangoli rispetto ai lati e agli angoli",
              "I triangoli: classificazione e angoli", "Triangoli",
              "Schede di matematica per la classe quarta sui triangoli: equilatero, isoscele, scaleno, acutangolo, rettangolo, ottusangolo, somma degli angoli interni, condizione di esistenza e problemi sul perimetro. 100 esercizi con soluzioni.",
              "La somma degli angoli di un triangolo è 180°.", "Lati: equilatero, isoscele, scaleno. Angoli: acutangolo, rettangolo, ottusangolo.",
              body, faq, sets, 15, grade=G)


if __name__ == "__main__":
    main()
