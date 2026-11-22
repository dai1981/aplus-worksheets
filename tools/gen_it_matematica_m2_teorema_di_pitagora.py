# -*- coding: utf-8 -*-
"""
Italia Matematica seconda media: Teorema di Pitagora (Spazio e figure)
  python3 tools/gen_it_matematica_m2_teorema_di_pitagora.py
Cateti e ipotenusa, i² = c₁² + c₂², calcolo dell’ipotenusa e di un cateto, terne pitagoriche, riconoscere un triangolo
rettangolo, radici approssimate a un decimale, problemi (scala, schermo, diagonale).
Errori: sommare i lati invece dei quadrati, dimenticare la radice, sommare i quadrati anche per trovare un cateto.
"""
import math
import random
from fractions import Fraction as Fr
from it_media import M, L, unit, mix, table, W, num, d, dk, figure, Kids

R = random.Random(71208)
G = "seconda-media"
K = Kids(R)
TERNE = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41), (12, 35, 37)]


def terna(maxc=60):
    while True:
        a, b, c = R.choice(TERNE)
        k = R.choice([1, 1, 2, 3, 4, 5, 10])
        if c * k <= maxc:
            if R.random() < 0.5:
                a, b = b, a
            return a * k, b * k, c * k


def r1(s):
    """√s arrotondata ai decimi (senza «,0»)"""
    t = dk(Fr(math.isqrt(s * 10000), 100), 1)
    return "%s cm" % (t[:-2] if t.endswith(",0") else t)


def cm(v):
    return "%s cm" % d(v)


def tri(a, b, lab_a, lab_b, lab_c):
    pts = {"A": (0, 0), "B": (a, 0), "C": (0, b)}
    sides = [(s_, t_, l) for s_, t_, l in (("A", "B", lab_a), ("A", "C", lab_b), ("B", "C", lab_c)) if l]
    return figure(pts, [("A", "B"), ("B", "C"), ("C", "A")], sides, right=[("A", "B", "C")], label="triangolo rettangolo")


def s1_ipot():
    a, b, c = terna()
    return M("%sCalcola l’ipotenusa del triangolo rettangolo con i cateti di %d cm e %d cm." % (tri(a, b, cm(a), cm(b), "?"), a, b), cm(c), W(cm(a + b), cm(a * a + b * b), cm(c + 1), cm(abs(b - a) + c) if b != a else None),
             "i = √(%d² + %d²) = √(%d + %d) = √%d = <b>%s</b>." % (a, b, a * a, b * b, c * c, cm(c)))


def s2_cateto():
    a, b, c = terna()
    return M("%sIn un triangolo rettangolo l’ipotenusa misura %d cm e un cateto %d cm. Quanto misura l’altro cateto?" % (tri(a, b, cm(a), "?", cm(c)), c, a), cm(b),
             W(cm(c - a), r1(c * c + a * a), cm(b + 1), cm(c * c - a * a)),
             "c = √(%d² − %d²) = √(%d − %d) = √%d = <b>%s</b>." % (c, a, c * c, a * a, b * b, cm(b)))


def s3_verifica():
    a, b, c = terna(50)
    ok = R.random() < 0.5
    if not ok:
        c += R.choice([-1, 1, 2])
    sa, sb, sc = sorted([a, b, c])
    return M("Un triangolo ha i lati di %d cm, %d cm e %d cm. È un triangolo rettangolo?" % tuple(R.sample([a, b, c], 3)), "sì" if ok else "no",
             ["no" if ok else "sì", "solo se è isoscele", "non si può sapere senza disegnarlo"],
             "%d² + %d² = %d + %d = %d; %d² = %d. %s." % (sa, sb, sa * sa, sb * sb, sa * sa + sb * sb, sc, sc * sc, "Sono uguali: <b>sì</b>" if ok else "Sono diversi: <b>no</b>"))


def s3_quiz():
    q, a, w = R.choice([
        ("In un triangolo rettangolo, il lato opposto all’angolo retto si chiama…", "ipotenusa", ["cateto maggiore", "base", "altezza"]),
        ("I due lati che formano l’angolo retto si chiamano…", "cateti", ["ipotenuse", "basi", "diagonali"]),
        ("Il teorema di Pitagora vale…", "solo nei triangoli rettangoli", ["in tutti i triangoli", "solo nei triangoli equilateri", "solo nei triangoli isosceli"]),
        ("Nel triangolo rettangolo il lato più lungo è sempre…", "l’ipotenusa", ["un cateto", "la base", "non si può dire"]),
        ("Quale di queste è una terna pitagorica?", "6, 8, 10", ["4, 5, 6", "2, 3, 4", "5, 6, 7"]),
        ("Quali tre numeri formano una terna pitagorica?", "5, 12, 13", ["5, 11, 13", "6, 12, 13", "4, 12, 13"]),
        ("Con quali lati (in cm) si costruisce un triangolo rettangolo?", "8, 15, 17", ["8, 14, 17", "7, 15, 17", "9, 15, 17"]),
        ("Per trovare un cateto si calcola…", "la radice della differenza tra i quadrati di ipotenusa e altro cateto", ["la radice della somma dei quadrati", "la differenza tra ipotenusa e cateto", "la somma dei due lati"]),
        ("Se i cateti misurano 3 e 4, l’area dei quadrati costruiti su di essi è 9 e 16. Quanto è l’area del quadrato costruito sull’ipotenusa?", "25", ["7", "12", "49"]),
    ])
    return M(q, a, w, "Risposta: <b>%s</b>." % a)


def s4_approx():
    k = R.choice(["ipot", "cat"])
    if k == "ipot":
        a, b = R.randint(2, 15), R.randint(2, 15)
        s = a * a + b * b
        if math.isqrt(s) ** 2 == s:
            return None
        r = dk(Fr(math.isqrt(s * 10000), 100), 1)
        return M("I cateti di un triangolo rettangolo misurano %d cm e %d cm. Calcola l’ipotenusa (arrotonda ai decimi)." % (a, b), "%s cm" % r, W("%d cm" % (a + b), "%s cm" % dk(Fr(math.isqrt(abs(a * a - b * b) * 10000), 100), 1) if a != b else None, "%s cm" % num(s), "%s cm" % dk(Fr(math.isqrt(s * 10000), 100) + Fr(1, 10), 1)),
                 "i = √(%d + %d) = √%d ≈ <b>%s cm</b>." % (a * a, b * b, s, r))
    c = R.randint(6, 20)
    a = R.randint(2, c - 1)
    s = c * c - a * a
    if math.isqrt(s) ** 2 == s:
        return None
    r = dk(Fr(math.isqrt(s * 10000), 100), 1)
    return M("L’ipotenusa di un triangolo rettangolo misura %d cm e un cateto %d cm. Calcola l’altro cateto (arrotonda ai decimi)." % (c, a), "%s cm" % r, W("%d cm" % (c - a), "%s cm" % dk(Fr(math.isqrt((c * c + a * a) * 10000), 100), 1), "%s cm" % num(s), "%s cm" % dk(Fr(math.isqrt(s * 10000), 100) - Fr(1, 10), 1)),
             "c = √(%d − %d) = √%d ≈ <b>%s cm</b>." % (c * c, a * a, s, r))


def s5():
    k = R.choice(["scala", "tv", "campo", "aquilone", "palo", "nave"])
    if k == "scala":
        a, b, c = R.choice([(6, 8, 10), (5, 12, 13), (9, 12, 15), (12, 16, 20), (3, 4, 5)])
        return M("Una scala lunga %s m è appoggiata a un muro; il piede della scala è a %s m dal muro. A che altezza arriva la scala?" % (d(Fr(c, 2)), d(Fr(a, 2))), "%s m" % d(Fr(b, 2)), W("%s m" % d(Fr(c - a, 2)), "%s m" % d(Fr(c + a, 2)), "%s m" % d(Fr(b + 1, 2))),
                 "h = √(%s² − %s²) = √(%s − %s) = <b>%s m</b>." % (d(Fr(c, 2)), d(Fr(a, 2)), d(Fr(c * c, 4)), d(Fr(a * a, 4)), d(Fr(b, 2))))
    if k == "tv":
        a, b, c = R.choice([(48, 36, 60), (64, 48, 80), (80, 60, 100), (96, 72, 120), (120, 90, 150)])
        return M("Lo schermo di un televisore è largo %d cm e alto %d cm. Quanto misura la diagonale?" % (a, b), "%d cm" % c, W("%d cm" % (a + b), "%d cm" % (a - b), "%d cm" % (c + 10)), "d = √(%d² + %d²) = √%s = <b>%d cm</b>." % (a, b, num(c * c), c))
    if k == "campo":
        a, b, c = R.choice([(40, 30, 50), (60, 80, 100), (90, 120, 150), (45, 60, 75), (36, 48, 60)])
        return M("Un campo rettangolare misura %d m × %d m. Quanti metri si risparmiano attraversandolo in diagonale invece che camminando lungo due lati?" % (a, b), "%d m" % (a + b - c), W("%d m" % c, "%d m" % (a + b), "%d m" % (c - a), "%d m" % (a + b - c + 10)),
                 "Diagonale: √(%d² + %d²) = %d m; lungo i lati: %d m; risparmio: %d − %d = <b>%d m</b>." % (a, b, c, a + b, a + b, c, a + b - c))
    if k == "aquilone":
        a, b, c = R.choice([(24, 32, 40), (30, 40, 50), (36, 48, 60), (15, 20, 25)])
        return M("Il filo di un aquilone è lungo %d m e l’aquilone è esattamente sopra un punto a %d m da chi lo tiene. A che altezza vola (trascura l’altezza della persona)?" % (c, a), "%d m" % b, W("%d m" % (c - a), "%d m" % (c + a), "%d m" % (b + 4)), "h = √(%d² − %d²) = √%s = <b>%d m</b>." % (c, a, num(c * c - a * a), b))
    if k == "palo":
        a, b, c = R.choice([(5, 12, 13), (8, 15, 17), (6, 8, 10), (9, 12, 15)])
        return M("Un palo alto %d m è tenuto da un cavo fissato in cima e a terra a %d m dalla base del palo. Quanto è lungo il cavo?" % (b, a), "%d m" % c, W("%d m" % (a + b), "%d m" % (b - a), "%d m" % (c + 1)), "√(%d² + %d²) = √%d = <b>%d m</b>." % (b, a, c * c, c))
    a, b, c = R.choice([(6, 8, 10), (9, 12, 15), (12, 16, 20), (15, 20, 25), (21, 28, 35)])
    return M("Una barca naviga %d km verso nord e poi %d km verso est. A che distanza si trova dal punto di partenza?" % (a, b), "%d km" % c, W("%d km" % (a + b), "%d km" % (b - a), "%d km" % (c + 2)), "d = √(%d² + %d²) = √%d = <b>%d km</b>." % (a, b, c * c, c))


def main():
    seen = set()
    sets = [
        ("Calcolare l’ipotenusa", mix(R, seen, [(s1_ipot, 20)])),
        ("Calcolare un cateto", mix(R, seen, [(s2_cateto, 20)])),
        ("Terne pitagoriche e triangoli rettangoli", mix(R, seen, [(s3_verifica, 12), (s3_quiz, 8)])),
        ("Radici approssimate", mix(R, seen, [(s4_approx, 20)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = L(["In un triangolo rettangolo i lati dell’angolo retto sono i <b>cateti</b>, il lato opposto è l’<b>ipotenusa</b> (il lato più lungo).",
              "<b>Teorema di Pitagora</b>: il quadrato costruito sull’ipotenusa è equivalente alla somma dei quadrati costruiti sui cateti: i² = c₁² + c₂².",
              "Ipotenusa: i = √(c₁² + c₂²). Cateto: c₁ = √(i² − c₂²).",
              "Se a² + b² = c², il triangolo è rettangolo. Tre numeri interi così si chiamano <b>terna pitagorica</b> (3, 4, 5)."],
             [("Cateti 6 cm e 8 cm", ["36 + 64 = 100", "√100"], "i = 10 cm"), ("Ipotenusa 13 cm, cateto 5 cm", ["169 − 25 = 144", "√144"], "c = 12 cm")],
             [["Sommare i lati: 6 + 8 = 14", "Si sommano i quadrati, poi si fa la radice."],
              ["Dimenticare la radice", "6² + 8² = 100 è il quadrato dell’ipotenusa, non l’ipotenusa."],
              ["Sommare i quadrati per trovare un cateto", "Per il cateto si sottrae: i² − c²."]],
             table(["Terna", "Multipli"], [["3, 4, 5", "6, 8, 10 · 9, 12, 15"], ["5, 12, 13", "10, 24, 26"], ["8, 15, 17", "16, 30, 34"], ["7, 24, 25", "14, 48, 50"]]))
    faq = [("Il teorema di Pitagora vale per tutti i triangoli?", "No, solo per i triangoli rettangoli. Ma se a² + b² = c², allora il triangolo è rettangolo (teorema inverso)."),
           ("Che cos’è una terna pitagorica?", "Tre numeri interi a, b, c con a² + b² = c², per esempio 3, 4, 5. Anche i multipli (6, 8, 10) sono terne pitagoriche.")]
    unit(G, R, "teorema-di-pitagora", "S",
         "Conoscere il teorema di Pitagora e le sue applicazioni in matematica e in situazioni concrete",
         "Teorema di Pitagora", "Teorema di Pitagora",
         "Schede di matematica per la seconda media sul teorema di Pitagora: ipotenusa e cateti, terne pitagoriche, triangoli rettangoli, radici approssimate e problemi. 100 esercizi con soluzioni.",
         "i² = c₁² + c₂²", "Ipotenusa: somma dei quadrati. Cateto: differenza.",
         body, faq, sets, 8)


if __name__ == "__main__":
    main()
