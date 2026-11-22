# -*- coding: utf-8 -*-
"""
Italia Matematica classe terza: Linee e angoli (Spazio e figure)
  python3 tools/gen_it_matematica_c3_linee_e_angoli.py
Linee curve, rette, spezzate e miste, aperte e chiuse; retta, semiretta e segmento; rette parallele, incidenti,
perpendicolari; angoli retto, acuto, ottuso, piatto e giro; angoli come rotazioni (giri, mezzi giri, quarti di giro).
Errori: credere che un angolo sia più grande se i lati sono più lunghi, confondere incidenti e perpendicolari, segmento e retta.
"""
import math
import random
from it_common import mcq, lesson, make_unit, mix, wrap, text, line, INK, RED, GREEN, BLUE
import gen_fr_maths_ce2_figures_planes_et_angles_droits as FRF

R = random.Random(70317)


def g(body, label, w=220, h=130):
    return wrap(w, h, body, label)


def path(d, col=INK, w=3):
    return "<path d='%s' fill='none' stroke='%s' stroke-width='%s' stroke-linecap='round' stroke-linejoin='round'/>" % (d, col, w)


def linea(kind):
    if kind == "retta":
        return g(path("M20 %d L200 %d" % (R.randint(30, 100), R.randint(30, 100))), "una linea")
    if kind == "curva":
        return g(path("M20 90 C60 %d 100 %d 200 60" % (R.randint(0, 40), R.randint(90, 130))), "una linea")
    if kind == "spezzata":
        pts = [(20, 100)] + [(20 + 45 * i, R.choice([20, 40, 100, 110])) for i in range(1, 5)]
        return g(path("M" + " L".join("%d %d" % p for p in pts)), "una linea")
    if kind == "mista":
        return g(path("M20 100 L80 30 C120 0 150 130 200 70"), "una linea")
    if kind == "chiusa":
        return g(path("M40 70 C40 10 180 10 180 70 C180 120 40 120 40 70 Z"), "una linea")
    return g(path("M30 100 L70 25 L130 95 L190 30 L190 110 Z"), "una linea")


LINEE = {"retta": "una linea retta", "curva": "una linea curva", "spezzata": "una linea spezzata", "mista": "una linea mista"}


def s1_linee():
    k = R.choice(list(LINEE) + ["chiusa", "spezzata_chiusa"])
    if k in ("chiusa", "spezzata_chiusa"):
        ok = "una linea chiusa"
        return mcq(linea(k) + "Che linea è?", ok, ["una linea aperta", "una linea retta", "una semiretta"],
                   "La linea non ha un inizio e una fine: torna al punto di partenza. È <b>una linea chiusa</b>.")
    ok = LINEE[k]
    why = {"retta": "va sempre nella stessa direzione", "curva": "cambia direzione piano piano, senza punte", "spezzata": "è fatta di pezzi dritti uniti da punte",
           "mista": "ha pezzi dritti e pezzi curvi"}[k]
    return mcq(linea(k) + "Che linea è?", ok, [v for x, v in LINEE.items() if x != k], "La linea %s: è <b>%s</b>." % (why, ok))


def segno(kind):
    y = R.randint(40, 80)
    s = []
    if kind == "segmento":
        s += [line(40, y, 180, y, INK, 3), "<circle cx='40' cy='%d' r='4' fill='%s'/>" % (y, RED), "<circle cx='180' cy='%d' r='4' fill='%s'/>" % (y, RED),
              text(40, y - 12, "A", 14), text(180, y - 12, "B", 14)]
    elif kind == "semiretta":
        s += [line(40, y, 205, y, INK, 3), "<path d='M212 %d l-12 -6 v12 Z' fill='%s'/>" % (y, INK), "<circle cx='40' cy='%d' r='4' fill='%s'/>" % (y, RED), text(40, y - 12, "O", 14)]
    else:
        s += [line(18, y, 202, y, INK, 3), "<path d='M212 %d l-12 -6 v12 Z' fill='%s'/>" % (y, INK), "<path d='M8 %d l12 -6 v12 Z' fill='%s'/>" % (y, INK)]
    return g("".join(s), "una linea retta", h=110)


def s1_retta():
    k = R.choice(["segmento", "semiretta", "retta"])
    names = {"segmento": "un segmento", "semiretta": "una semiretta", "retta": "una retta"}
    why = {"segmento": "ha un inizio e una fine (due estremi)", "semiretta": "ha un inizio ma non ha fine", "retta": "non ha né inizio né fine"}
    return mcq(segno(k) + "Che cosa è disegnato?", names[k], [v for x, v in names.items() if x != k] + ["una linea curva"],
               "Questa linea %s: è <b>%s</b>." % (why[k], names[k]))


def coppia(kind):
    s = []
    if kind == "parallele":
        a = R.uniform(-0.3, 0.3)
        for y in (40, 90):
            s.append(line(20, y, 200, y + 180 * math.tan(a), INK, 3))
    elif kind == "perpendicolari":
        a = R.choice([0, 0, R.uniform(-0.4, 0.4)])
        cx, cy = 110, 70
        for b in (a, a + math.pi / 2):
            dx, dy = 70 * math.cos(b), 70 * math.sin(b)
            s.append(line(cx - dx, cy - dy, cx + dx, cy + dy, INK, 3))
        s.append("<rect x='%d' y='%d' width='12' height='12' fill='none' stroke='%s' stroke-width='1.6' transform='rotate(%.1f %d %d)'/>" % (cx, cy - 12, RED, math.degrees(a), cx, cy))
    else:
        b = R.choice([0.45, 0.6, 0.8, 1.0, 2.2, 2.5])
        cx, cy = 110, 70
        for t in (0, b):
            dx, dy = 85 * math.cos(t), 55 * math.sin(t)
            s.append(line(cx - dx, cy - dy, cx + dx, cy + dy, INK, 3))
    return g("".join(s), "due rette", h=140)


def s2_rette():
    k = R.choice(["parallele", "perpendicolari", "incidenti"])
    names = {"parallele": "parallele", "perpendicolari": "perpendicolari", "incidenti": "incidenti (ma non perpendicolari)"}
    why = {"parallele": "non si incontrano mai, anche se le allunghi", "perpendicolari": "si incontrano formando 4 angoli retti",
           "incidenti": "si incontrano in un punto, ma gli angoli non sono retti"}
    return mcq(coppia(k) + "Come sono queste due rette?", names[k], [v for x, v in names.items() if x != k] + ["curve"],
               "Le due rette %s: sono <b>%s</b>." % (why[k], names[k]))


RETTE_Q = [("Due rette che non si incontrano mai si chiamano…", "parallele", ["perpendicolari", "incidenti", "spezzate"]),
           ("Due rette che si incontrano formando 4 angoli retti si chiamano…", "perpendicolari", ["parallele", "curve", "semirette"]),
           ("Le rotaie del treno sono un esempio di linee…", "parallele", ["perpendicolari", "incidenti", "curve"]),
           ("Il bordo verticale e il bordo orizzontale di un foglio sono…", "perpendicolari", ["parallele", "curve", "uguali"]),
           ("Quanti estremi ha un segmento?", "2", ["1", "0", "3"]),
           ("Quanti estremi ha una semiretta?", "1", ["2", "0", "3"]),
           ("Una retta ha un inizio e una fine?", "no, non ha né inizio né fine", ["sì, ha due estremi", "ha solo un inizio", "ha solo una fine"]),
           ("Due rette perpendicolari sono anche incidenti?", "sì, perché si incontrano", ["no, mai", "solo se sono lunghe", "solo se sono parallele"]),
           ("Quante rette passano per due punti?", "una sola", ["due", "nessuna", "infinite"]),
           ("Quante rette passano per un punto?", "infinite", ["una sola", "due", "nessuna"])]


def s2_quiz():
    q, a, w = R.choice(RETTE_Q)
    return mcq(q, a, w, "Risposta: <b>%s</b>." % a)


def angolo_svg(deg):
    if deg == 180:
        s = [line(30, 80, 210, 80, INK, 3), "<circle cx='120' cy='80' r='4' fill='%s'/>" % INK,
             "<path d='M150 80 A30 30 0 0 0 90 80' fill='none' stroke='%s' stroke-width='2'/>" % RED]
        return g("".join(s), "un angolo", w=240, h=130)
    if deg == 360:
        s = [line(120, 80, 210, 80, INK, 3), "<circle cx='120' cy='80' r='4' fill='%s'/>" % INK,
             "<circle cx='120' cy='80' r='30' fill='none' stroke='%s' stroke-width='2'/>" % RED]
        return g("".join(s), "un angolo", w=240, h=130)
    return FRF.angle_svg(deg).replace("aria-label='un angle'", "aria-label='un angolo'")


ANG = {"retto": "un angolo retto", "acuto": "un angolo acuto", "ottuso": "un angolo ottuso", "piatto": "un angolo piatto", "giro": "un angolo giro"}


def s3_angoli():
    deg = R.choice([90, 90, 180, 360] + list(range(25, 80, 5)) + list(range(105, 165, 5)))
    k = "retto" if deg == 90 else "acuto" if deg < 90 else "ottuso" if deg < 180 else "piatto" if deg == 180 else "giro"
    why = {"retto": "è come l’angolo di un foglio (un quarto di giro)", "acuto": "è più piccolo di un angolo retto", "ottuso": "è più grande di un angolo retto ma più piccolo di un angolo piatto",
           "piatto": "i due lati formano una linea retta (mezzo giro)", "giro": "un lato fa tutto il giro e torna sull’altro"}[k]
    return mcq(angolo_svg(deg) + "Che angolo è?", ANG[k], [v for x, v in ANG.items() if x != k],
               "Questo angolo %s: è <b>%s</b>." % (why, ANG[k]))


GIRI = [("Quanti angoli retti ci sono in un angolo piatto?", "2", ["1", "3", "4"]),
        ("Quanti angoli retti ci sono in un angolo giro?", "4", ["2", "3", "1"]),
        ("Un quarto di giro forma…", "un angolo retto", ["un angolo piatto", "un angolo giro", "un angolo acuto"]),
        ("Mezzo giro forma…", "un angolo piatto", ["un angolo retto", "un angolo giro", "un angolo ottuso"]),
        ("Un giro completo forma…", "un angolo giro", ["un angolo piatto", "un angolo retto", "un angolo acuto"]),
        ("Le lancette dell’orologio alle 3:00 formano…", "un angolo retto", ["un angolo piatto", "un angolo acuto", "un angolo ottuso"]),
        ("Le lancette dell’orologio alle 6:00 formano…", "un angolo piatto", ["un angolo retto", "un angolo giro", "un angolo acuto"]),
        ("Le lancette dell’orologio all’1:00 formano…", "un angolo acuto", ["un angolo ottuso", "un angolo retto", "un angolo piatto"]),
        ("Le lancette dell’orologio alle 5:00 formano…", "un angolo ottuso", ["un angolo acuto", "un angolo retto", "un angolo piatto"]),
        ("Quale strumento usi per controllare se un angolo è retto?", "la squadra", ["il compasso", "il righello", "la gomma"]),
        ("Se allunghi i lati di un angolo, l’angolo…", "resta uguale", ["diventa più grande", "diventa più piccolo", "diventa retto"]),
        ("Sei rivolto verso la lavagna e fai mezzo giro. Dove guardi?", "verso il fondo dell’aula", ["verso la lavagna", "verso la finestra a destra", "verso il soffitto"]),
        ("Un angolo più piccolo di un angolo retto si chiama…", "acuto", ["ottuso", "piatto", "giro"]),
        ("Un angolo più grande di un retto e più piccolo di un piatto si chiama…", "ottuso", ["acuto", "giro", "retto"]),
        ("Che cosa formano due rette perpendicolari?", "4 angoli retti", ["2 angoli piatti", "4 angoli acuti", "nessun angolo"])]


def s4_giri():
    q, a, w = R.choice(GIRI)
    return mcq(q, a, w, "Risposta: <b>%s</b>." % a)


def due_angoli(a, b, la, lb):
    out = []
    for i, (deg, L, name) in enumerate(((a, la, "A"), (b, lb, "B"))):
        x0, y0 = 30 + i * 230, 150
        t = math.radians(deg)
        x1, y1 = x0 + L * math.cos(-t), y0 + L * math.sin(-t)
        out += [line(x0, y0, x0 + L, y0, INK, 3), line(x0, y0, x1, y1, INK, 3),
                "<path d='M%.1f %.1f A24 24 0 0 0 %.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x0 + 24, y0, x0 + 24 * math.cos(-t), y0 + 24 * math.sin(-t), RED),
                text(x0 + 60, y0 + 24, name, 16, weight=700)]
    return "<g transform='translate(40,0)'>%s</g>" % "".join(out)


def s4_confronta():
    a, b = R.sample(list(range(30, 140, 10)), 2)
    if abs(a - b) < 20:
        return None
    big = "l’angolo A" if a > b else "l’angolo B"
    la, lb = (70, 140) if a > b else (140, 70)
    pic = wrap(520, 180, due_angoli(a, b, la, lb), "due angoli A e B")
    return mcq(pic + "Quale angolo è più grande?", big,
               ["l’angolo B" if big == "l’angolo A" else "l’angolo A", "sono uguali", "quello con i lati più lunghi"],
               "Conta quanto è aperto l’angolo, non quanto sono lunghi i lati: è più grande <b>%s</b>." % big)


def s5():
    k = R.choice(["count", "count", "figure"])
    if k == "count":
        n, v = R.choice(FRF.SHAPES_RA)
        name = {"carré": "un quadrato", "rectangle": "un rettangolo", "triangle rectangle": "un triangolo rettangolo", "losange": "un rombo", "triangle": "un triangolo"}[n]
        pic = FRF.shape(n).replace("aria-label='une figure plane'", "aria-label='una figura piana'")
        return mcq(pic + "Quanti angoli retti ha questa figura?", str(v), [str(x) for x in (0, 1, 2, 3, 4) if x != v],
                   "Controlla ogni angolo con la squadra: <b>%d</b>. È %s." % (v, name))
    pic, v = FRF.trapeze() if R.random() < 0.5 else FRF.maison()
    pic = pic.replace("aria-label='une figure plane'", "aria-label='una figura piana'")
    return mcq(pic + "Quanti angoli retti ha questa figura?", str(v), [str(x) for x in (0, 1, 3, 4) if x != v],
               "Controlla ogni angolo con la squadra: ci sono <b>%d</b> angoli retti." % v)


def main():
    FRF.R = R
    seen = set()
    sets = [
        ("Le linee", mix(R, seen, [(s1_linee, 12), (s1_retta, 8)])),
        ("Rette parallele, incidenti, perpendicolari", mix(R, seen, [(s2_rette, 10), (s2_quiz, 10)])),
        ("Che angolo è?", mix(R, seen, [(s3_angoli, 20)])),
        ("Angoli e giri", mix(R, seen, [(s4_giri, 14), (s4_confronta, 6)])),
        ("Angoli retti nelle figure", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Le linee possono essere <b>rette</b>, <b>curve</b>, <b>spezzate</b> o <b>miste</b>, aperte o chiuse.",
         "La <b>retta</b> non ha né inizio né fine; la <b>semiretta</b> ha un inizio; il <b>segmento</b> ha due estremi.",
         "Due rette sono <b>parallele</b> se non si incontrano mai, <b>incidenti</b> se si incontrano, <b>perpendicolari</b> se si incontrano formando 4 angoli retti.",
         "Un angolo è una rotazione: un quarto di giro è un angolo <b>retto</b>, mezzo giro un angolo <b>piatto</b>, un giro intero un angolo <b>giro</b>. Più piccolo del retto è <b>acuto</b>, tra retto e piatto è <b>ottuso</b>."],
        [("Alle 3:00 le lancette formano un angolo…", ["dal 12 al 3 c’è un quarto di giro"], "retto")],
        [["Pensare che un angolo con i lati lunghi sia più grande", "Conta solo quanto è aperto l’angolo."],
         ["Chiamare perpendicolari tutte le rette che si incontrano", "Sono perpendicolari solo se formano angoli retti."],
         ["Confondere segmento e retta", "Il segmento ha due estremi, la retta non finisce mai."]],
        coppia("perpendicolari"))
    faq = [("Come controllo se un angolo è retto?", "Con la squadra o con l’angolo di un foglio piegato in quattro: se combacia, l’angolo è retto."),
           ("Che differenza c’è tra incidenti e perpendicolari?", "Le rette incidenti si incontrano in un punto. Le perpendicolari sono incidenti speciali: formano 4 angoli retti.")]
    make_unit(R, "linee-e-angoli", "S",
              "Riconoscere, denominare e descrivere linee (rette, curve, spezzate, aperte, chiuse), rette parallele, incidenti e perpendicolari; riconoscere l’angolo come cambiamento di direzione e classificare gli angoli",
              "Linee e angoli: rette, semirette, segmenti e angoli", "Linee e angoli",
              "Schede di matematica per la classe terza su linee e angoli: linee rette, curve e spezzate, retta, semiretta e segmento, rette parallele e perpendicolari, angoli retto, acuto, ottuso, piatto e giro. 100 esercizi con soluzioni.",
              "Un quarto di giro è un angolo retto.", "Le rette perpendicolari formano 4 angoli retti.",
              body, faq, sets, 17)


if __name__ == "__main__":
    main()
