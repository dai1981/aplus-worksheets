# -*- coding: utf-8 -*-
"""
Italia Matematica classe quarta: I quadrilateri (Spazio e figure)
  python3 tools/gen_it_matematica_c4_quadrilateri.py
Trapezi (isoscele, rettangolo, scaleno), parallelogrammi, rombi, rettangoli, quadrati; lati paralleli, angoli e
diagonali; la somma degli angoli interni è 360°; relazioni tra i quadrilateri (il quadrato è anche rettangolo e rombo).
Errori: credere che il quadrato non sia un rettangolo, confondere rombo e quadrato «girato», sommare gli angoli a 180°.
"""
import random
from it_common import mcq, lesson, make_unit, mix, table, relabel, fig
import gen_au_maths_y5_angles as AU

R = random.Random(70416)
G = "classe-quarta"
NOMI = ["quadrato", "rettangolo", "rombo", "parallelogramma", "trapezio isoscele", "trapezio rettangolo", "trapezio scaleno"]


def shape(k, rot=0):
    if k == "quadrato":
        s = R.choice([90, 100, 110])
        pts, rights, ticks = [(0, 0), (s, 0), (s, -s), (0, -s)], (0, 1, 2, 3), ((0, 1), (1, 1), (2, 1), (3, 1))
    elif k == "rettangolo":
        w, h = R.choice([(150, 80), (160, 70), (130, 90), (170, 60)])
        pts, rights, ticks = [(0, 0), (w, 0), (w, -h), (0, -h)], (0, 1, 2, 3), ((0, 1), (2, 1), (1, 2), (3, 2))
    elif k == "rombo":
        a, b = R.choice([(70, 45), (55, 75), (80, 40)])
        pts, rights, ticks = [(0, 0), (a, -b), (0, -2 * b), (-a, -b)], (), ((0, 1), (1, 1), (2, 1), (3, 1))
    elif k == "parallelogramma":
        w, h, d = R.choice([(130, 70, 45), (140, 60, 55), (120, 80, 40)])
        pts, rights, ticks = [(0, 0), (w, 0), (w + d, -h), (d, -h)], (), ((0, 1), (2, 1), (1, 2), (3, 2))
    elif k == "trapezio isoscele":
        w, h, d = R.choice([(170, 70, 40), (160, 80, 35), (180, 65, 50)])
        pts, rights, ticks = [(0, 0), (w, 0), (w - d, -h), (d, -h)], (), ((1, 1), (3, 1))
    elif k == "trapezio rettangolo":
        w, h, d = R.choice([(160, 80, 60), (170, 70, 50), (150, 90, 55)])
        pts, rights, ticks = [(0, 0), (w, 0), (w - d, -h), (0, -h)], (0, 3), ()
    else:
        w, h, d1, d2 = R.choice([(180, 70, 70, 25), (170, 80, 25, 70), (190, 65, 80, 30)])
        pts, rights, ticks = [(0, 0), (w, 0), (w - d1, -h), (d2, -h)], (), ()
    if rot:
        pts = AU.rot_all(pts, rot)
    return fig(relabel(AU.shape_svg(pts, {}, "un quadrilatero", rights=rights, ticks=ticks), "un quadrilatero"))


def s1_nome():
    k = R.choice(NOMI)
    rot = R.choice([0, 0, 0, 20, -20]) if k != "quadrato" else R.choice([0, 0, 45])
    w = [x for x in NOMI if x != k]
    R.shuffle(w)
    near = {"quadrato": ["rombo", "rettangolo"], "rettangolo": ["quadrato", "parallelogramma"], "rombo": ["quadrato", "parallelogramma"],
            "parallelogramma": ["rombo", "rettangolo"], "trapezio isoscele": ["trapezio scaleno", "parallelogramma"],
            "trapezio rettangolo": ["rettangolo", "trapezio scaleno"], "trapezio scaleno": ["trapezio isoscele", "parallelogramma"]}[k]
    why = {"quadrato": "4 lati uguali e 4 angoli retti", "rettangolo": "4 angoli retti e i lati opposti uguali", "rombo": "4 lati uguali ma nessun angolo retto",
           "parallelogramma": "due coppie di lati paralleli, lati opposti uguali, nessun angolo retto", "trapezio isoscele": "una sola coppia di lati paralleli e i lati obliqui uguali",
           "trapezio rettangolo": "una sola coppia di lati paralleli e due angoli retti", "trapezio scaleno": "una sola coppia di lati paralleli e i lati obliqui diversi"}[k]
    return mcq(shape(k, rot) + "Come si chiama questo quadrilatero? (i trattini indicano lati uguali)", k, near + w, "Ha %s: è un <b>%s</b>." % (why, k))


PROP = [("Quale quadrilatero ha una sola coppia di lati paralleli?", "il trapezio", ["il parallelogramma", "il rombo", "il rettangolo"]),
        ("Quale quadrilatero ha 4 lati uguali ma nessun angolo retto?", "il rombo", ["il quadrato", "il rettangolo", "il trapezio"]),
        ("Quale quadrilatero ha 4 angoli retti e i lati non tutti uguali?", "il rettangolo", ["il quadrato", "il rombo", "il trapezio rettangolo"]),
        ("Quale quadrilatero ha 4 lati uguali e 4 angoli retti?", "il quadrato", ["il rombo", "il rettangolo", "il parallelogramma"]),
        ("Quante coppie di lati paralleli ha un parallelogramma?", "2", ["1", "0", "4"]),
        ("Quante coppie di lati paralleli ha un trapezio?", "1", ["2", "0", "4"]),
        ("Quanti angoli retti ha un trapezio rettangolo?", "2", ["1", "4", "3"]),
        ("Quante diagonali ha un quadrilatero?", "2", ["4", "1", "3"]),
        ("In quale quadrilatero le diagonali sono perpendicolari ma non uguali?", "nel rombo", ["nel rettangolo", "nel quadrato", "nel trapezio scaleno"]),
        ("In quale quadrilatero le diagonali sono uguali ma non perpendicolari?", "nel rettangolo", ["nel rombo", "nel quadrato", "nel parallelogramma"]),
        ("In quale quadrilatero le diagonali sono uguali e perpendicolari?", "nel quadrato", ["nel rombo", "nel rettangolo", "nel trapezio"]),
        ("Nel parallelogramma, come sono gli angoli opposti?", "uguali", ["supplementari", "sempre retti", "sempre acuti"]),
        ("Nel trapezio isoscele, come sono i lati obliqui?", "uguali", ["paralleli", "perpendicolari", "uno doppio dell’altro"]),
        ("Come si chiamano i due lati paralleli di un trapezio?", "base maggiore e base minore", ["cateti", "diagonali", "lati obliqui"])]


def s2_prop():
    q, a, w = R.choice(PROP)
    return mcq(q, a, w, "Risposta: <b>%s</b>." % a)


REL = [("Il quadrato è anche un rettangolo?", "sì, ha 4 angoli retti", ["no, ha i lati uguali", "solo se è grande", "no, mai"]),
       ("Il quadrato è anche un rombo?", "sì, ha 4 lati uguali", ["no, ha gli angoli retti", "solo se è girato", "no, mai"]),
       ("Il rombo è un parallelogramma?", "sì, ha due coppie di lati paralleli", ["no, ha i lati uguali", "solo se ha angoli retti", "no, mai"]),
       ("Il rettangolo è un parallelogramma?", "sì, ha due coppie di lati paralleli", ["no, ha gli angoli retti", "solo se è lungo", "no, mai"]),
       ("Ogni rettangolo è un quadrato?", "no, solo se ha i 4 lati uguali", ["sì, sempre", "sì, se ha 4 angoli", "no, mai"]),
       ("Ogni rombo è un quadrato?", "no, solo se ha gli angoli retti", ["sì, sempre", "sì, se è girato", "no, mai"]),
       ("Il trapezio è un parallelogramma?", "no, ha una sola coppia di lati paralleli", ["sì, sempre", "sì, se è isoscele", "solo se è rettangolo"]),
       ("Quale quadrilatero è insieme rettangolo e rombo?", "il quadrato", ["il trapezio", "il parallelogramma", "nessuno"])]


def s3_rel():
    q, a, w = R.choice(REL)
    return mcq(q, a, w, "Risposta: <b>%s</b>." % a)


def s3_conta():
    k = R.choice(NOMI)
    if R.random() < 0.5:
        n = 1 if k.startswith("trapezio") else 2
        return mcq(shape(k) + "Quante coppie di lati paralleli ha questo quadrilatero?", str(n), [str(3 - n), "0", "4"],
                   "È un %s: ha <b>%d</b> %s di lati paralleli." % (k, n, "coppia" if n == 1 else "coppie"))
    n = {"quadrato": 4, "rettangolo": 4, "trapezio rettangolo": 2}.get(k, 0)
    return mcq(shape(k) + "Quanti angoli retti ha questo quadrilatero?", str(n), [str(x) for x in (0, 1, 2, 4) if x != n],
               "È un %s: %s." % (k, "ha <b>%d</b> angoli retti" % n if n else "<b>nessun</b> angolo retto"))


def s4_angoli():
    k = R.choice(["quarto", "quarto", "para", "trap", "rett"])
    if k == "quarto":
        a, b, c = R.randint(60, 130), R.randint(60, 130), R.randint(50, 120)
        d = 360 - a - b - c
        if not 30 <= d <= 160:
            return None
        return mcq("In un quadrilatero tre angoli misurano %d°, %d° e %d°. Quanto misura il quarto angolo?" % (a, b, c), "%d°" % d,
                   ["%d°" % (180 - a - b - c) if 180 - a - b - c > 0 else "%d°" % (d + 20), "%d°" % (d + 10), "%d°" % (a + b + c)],
                   "La somma degli angoli di un quadrilatero è 360°: 360° − %d° − %d° − %d° = <b>%d°</b>." % (a, b, c, d))
    if k == "para":
        a = R.choice([40, 50, 55, 60, 65, 70, 75, 80, 110, 120, 125, 130])
        return mcq("In un parallelogramma un angolo misura %d°. Quanto misura l’angolo vicino (sullo stesso lato)?" % a, "%d°" % (180 - a),
                   ["%d°" % a, "%d°" % (360 - a), "%d°" % (90 - a) if a < 90 else "%d°" % (a - 90)], "Due angoli vicini di un parallelogramma sono supplementari: 180° − %d° = <b>%d°</b>." % (a, 180 - a))
    if k == "trap":
        a = R.choice([50, 55, 60, 65, 70, 75, 80])
        return mcq("In un trapezio isoscele un angolo alla base maggiore misura %d°. Quanto misura ciascun angolo alla base minore?" % a, "%d°" % (180 - a),
                   ["%d°" % a, "%d°" % (360 - 2 * a), "%d°" % (90 - a)], "Gli angoli sullo stesso lato obliquo fanno 180°: 180° − %d° = <b>%d°</b>." % (a, 180 - a))
    a = R.choice([50, 60, 65, 70, 75, 80, 110, 115, 120, 125, 130])
    return mcq("Un trapezio rettangolo ha due angoli retti e un angolo di %d°. Quanto misura il quarto angolo?" % a, "%d°" % (180 - a),
               ["%d°" % (360 - a), "%d°" % a, "%d°" % (270 - a)], "360° − 90° − 90° − %d° = <b>%d°</b>." % (a, 180 - a))


def s5_perimetro():
    k = R.choice(["quad", "rett", "rombo", "para", "trap"])
    if k == "quad":
        l = R.randint(5, 60)
        return mcq("Un quadrato ha il lato di %d cm. Qual è il perimetro?" % l, "%d cm" % (4 * l), ["%d cm" % (2 * l), "%d cm" % (l * l), "%d cm" % (l + 4)], "%d × 4 = <b>%d cm</b>." % (l, 4 * l))
    if k == "rett":
        a, b = R.randint(10, 60), R.randint(4, 30)
        if a == b:
            return None
        return mcq("Un rettangolo ha i lati di %d cm e %d cm. Qual è il perimetro?" % (a, b), "%d cm" % (2 * (a + b)), ["%d cm" % (a + b), "%d cm" % (a * b), "%d cm" % (2 * a + b)],
                   "(%d + %d) × 2 = <b>%d cm</b>." % (a, b, 2 * (a + b)))
    if k == "rombo":
        p = R.randint(5, 40) * 4
        return mcq("Il perimetro di un rombo è %d cm. Quanto è lungo un lato?" % p, "%d cm" % (p // 4), ["%d cm" % (p // 2), "%d cm" % (p * 4), "%d cm" % (p - 4)], "Il rombo ha 4 lati uguali: %d : 4 = <b>%d cm</b>." % (p, p // 4))
    if k == "para":
        a, b = R.randint(10, 40), R.randint(5, 25)
        p = 2 * (a + b)
        return mcq("Il perimetro di un parallelogramma è %d cm e un lato misura %d cm. Quanto misura il lato vicino?" % (p, a), "%d cm" % b, ["%d cm" % (p - a), "%d cm" % (p // 4), "%d cm" % (p - 2 * a)],
                   "Metà perimetro: %d : 2 = %d; %d − %d = <b>%d cm</b>." % (p, a + b, a + b, a, b))
    B, b, l = R.randint(20, 40), R.randint(8, 18), R.randint(8, 16)
    return mcq("Un trapezio isoscele ha la base maggiore di %d cm, la base minore di %d cm e i lati obliqui di %d cm. Qual è il perimetro?" % (B, b, l), "%d cm" % (B + b + 2 * l),
               ["%d cm" % (B + b + l), "%d cm" % (2 * (B + b) + l), "%d cm" % (B * b)], "%d + %d + %d + %d = <b>%d cm</b>." % (B, b, l, l, B + b + 2 * l))


def main():
    seen = set()
    sets = [
        ("Riconoscere i quadrilateri", mix(R, seen, [(s1_nome, 20)])),
        ("Lati, angoli e diagonali", mix(R, seen, [(s2_prop, 14), (s3_rel, 6)])),
        ("Lati paralleli e angoli retti", mix(R, seen, [(s3_conta, 18), (s3_rel, 2)])),
        ("Gli angoli dei quadrilateri", mix(R, seen, [(s4_angoli, 20)])),
        ("Problemi sul perimetro", mix(R, seen, [(s5_perimetro, 20)])),
    ]
    body = lesson(
        ["Un <b>quadrilatero</b> ha 4 lati, 4 angoli e 2 diagonali. La somma dei suoi angoli è <b>360°</b>.",
         "Il <b>trapezio</b> ha una sola coppia di lati paralleli (le basi). Può essere isoscele, rettangolo o scaleno.",
         "Il <b>parallelogramma</b> ha due coppie di lati paralleli. Sono parallelogrammi anche il <b>rombo</b> (4 lati uguali), il <b>rettangolo</b> (4 angoli retti) e il <b>quadrato</b> (4 lati uguali e 4 angoli retti).",
         "Il quadrato è quindi anche un rettangolo e anche un rombo."],
        [("Tre angoli di un quadrilatero: 90°, 90°, 70°", ["90° + 90° + 70° = 250°", "360° − 250° = 110°"], "110°")],
        [["Dire che il quadrato non è un rettangolo", "Ha 4 angoli retti: è un rettangolo speciale."],
         ["Chiamare «rombo» un quadrato girato", "Se ha gli angoli retti resta un quadrato."],
         ["Sommare gli angoli a 180°", "In un quadrilatero la somma è 360° (due triangoli)."]],
        table(["Quadrilatero", "Lati paralleli", "Lati uguali", "Angoli retti"],
              [["trapezio", "1 coppia", "—", "0 o 2"], ["parallelogramma", "2 coppie", "opposti", "0"], ["rombo", "2 coppie", "tutti", "0"], ["rettangolo", "2 coppie", "opposti", "4"], ["quadrato", "2 coppie", "tutti", "4"]]))
    faq = [("Perché la somma degli angoli di un quadrilatero è 360°?", "Una diagonale divide il quadrilatero in due triangoli: 180° + 180° = 360°."),
           ("Come si riconosce un rombo?", "Ha 4 lati uguali e le diagonali perpendicolari; se ha anche gli angoli retti è un quadrato.")]
    make_unit(R, "quadrilateri", "S",
              "Descrivere, denominare e classificare figure geometriche, identificando elementi significativi (lati paralleli, angoli, diagonali); classificare i quadrilateri",
              "I quadrilateri: trapezi e parallelogrammi", "Quadrilateri",
              "Schede di matematica per la classe quarta sui quadrilateri: trapezi, parallelogrammi, rombi, rettangoli e quadrati, lati paralleli, diagonali, somma degli angoli e problemi sul perimetro. 100 esercizi con soluzioni.",
              "La somma degli angoli di un quadrilatero è 360°.", "Il quadrato è anche un rettangolo e un rombo.",
              body, faq, sets, 16, grade=G)


if __name__ == "__main__":
    main()
