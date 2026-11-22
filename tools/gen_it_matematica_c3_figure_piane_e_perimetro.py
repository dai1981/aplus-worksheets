# -*- coding: utf-8 -*-
"""
Italia Matematica classe terza: Figure piane e perimetro (Spazio e figure)
  python3 tools/gen_it_matematica_c3_figure_piane_e_perimetro.py
Poligoni e non poligoni, lati, vertici e angoli, quadrato, rettangolo, rombo, triangoli, pentagono, esagono,
il perimetro (somma dei lati, quadrato e rettangolo), la superficie contando i quadretti, problemi.
Errori: dimenticare un lato nel perimetro, sommare solo due lati del rettangolo, confondere perimetro e superficie.
"""
import random
from it_common import mcq, lesson, make_unit, mix, wrap, text, line, INK, GREEN, FILL, NB, FOIS
import gen_fr_maths_ce2_figures_planes_et_angles_droits as FRF

R = random.Random(70318)
IT = {"carré": "quadrato", "rectangle": "rettangolo", "losange": "rombo", "triangle rectangle": "triangolo rettangolo", "triangle": "triangolo",
      "pentagone": "pentagono", "hexagone": "esagono"}
ART = {"quadrato": "un quadrato", "rettangolo": "un rettangolo", "rombo": "un rombo", "triangolo rettangolo": "un triangolo rettangolo",
       "triangolo": "un triangolo", "pentagono": "un pentagono", "esagono": "un esagono"}
CONF = {"quadrato": ["un rombo", "un rettangolo"], "rettangolo": ["un quadrato", "un rombo"], "rombo": ["un quadrato", "un rettangolo"],
        "triangolo rettangolo": ["un triangolo", "un rettangolo"], "triangolo": ["un triangolo rettangolo", "un rombo"],
        "pentagono": ["un esagono", "un quadrato"], "esagono": ["un pentagono", "un rombo"]}
WHY = {"quadrato": "4 lati uguali e 4 angoli retti", "rettangolo": "4 angoli retti e i lati opposti uguali", "rombo": "4 lati uguali ma nessun angolo retto",
       "triangolo rettangolo": "3 lati e un angolo retto", "triangolo": "3 lati, senza angoli retti", "pentagono": "5 lati", "esagono": "6 lati"}
NLATI = {"quadrato": 4, "rettangolo": 4, "rombo": 4, "triangolo rettangolo": 3, "triangolo": 3, "pentagono": 5, "esagono": 6}


def shape(fr_name):
    return FRF.shape(fr_name).replace("aria-label='une figure plane'", "aria-label='una figura piana'")


def s1_nome():
    k = R.choice(list(IT))
    n = IT[k]
    w = CONF[n] + [ART[x] for x in ART if ART[x] not in CONF[n] and x != n]
    return mcq(shape(k) + "Come si chiama questa figura?", ART[n], w, "Questa figura ha %s: è <b>%s</b>." % (WHY[n], ART[n]))


def s1_conta():
    k = R.choice(list(IT))
    n = IT[k]
    v = NLATI[n]
    word = R.choice(["lati", "vertici"])
    return mcq(shape(k) + "Quanti %s ha questa figura?" % word, str(v), [str(x) for x in (v - 1, v + 1, v + 2, 2 * v) if x != v and x > 0],
               "Conta i %s: <b>%d</b>. Un poligono ha tanti lati quanti vertici." % (word, v))


PROP = [("Quanti lati ha un pentagono?", "5", ["6", "4", "8"]), ("Quanti lati ha un esagono?", "6", ["5", "8", "4"]),
        ("Quanti vertici ha un triangolo?", "3", ["4", "2", "6"]), ("Quanti vertici ha un rettangolo?", "4", ["2", "8", "6"]),
        ("Quanti angoli retti ha un quadrato?", "4", ["2", "0", "1"]), ("Quanti angoli retti ha un triangolo rettangolo?", "1", ["2", "3", "0"]),
        ("Quale figura ha 4 lati uguali e 4 angoli retti?", "il quadrato", ["il rombo", "il rettangolo", "l’esagono"]),
        ("Quale figura ha 4 lati uguali ma nessun angolo retto?", "il rombo", ["il quadrato", "il rettangolo", "il triangolo"]),
        ("Quale figura ha 4 angoli retti e due lati lunghi e due corti?", "il rettangolo", ["il quadrato", "il rombo", "il pentagono"]),
        ("Come si chiama una figura chiusa fatta solo di segmenti?", "un poligono", ["un cerchio", "una retta", "un solido"]),
        ("Il cerchio è un poligono?", "no, perché il suo contorno è curvo", ["sì, ha tanti lati", "sì, è una figura chiusa", "solo se è grande"]),
        ("Il quadrato è anche un rettangolo?", "sì, ha 4 angoli retti", ["no, mai", "solo se è grande", "sì, perché ha 3 lati"]),
        ("Quanti lati ha un ottagono?", "8", ["6", "10", "7"]), ("Quanti lati ha un quadrilatero?", "4", ["3", "5", "8"]),
        ("Come si chiama un poligono con 3 lati?", "triangolo", ["quadrilatero", "pentagono", "esagono"]),
        ("Come si chiama il punto dove si incontrano due lati?", "vertice", ["centro", "diametro", "spigolo"]),
        ("Il cartello dello stop ha la forma di un…", "ottagono", ["esagono", "pentagono", "quadrato"]),
        ("Le celle degli alveari delle api hanno la forma di un…", "esagono", ["pentagono", "quadrato", "triangolo"])]


def s2_prop():
    q, a, w = R.choice(PROP)
    return mcq(q, a, w, "Risposta: <b>%s</b>." % a)


def rett_svg(a, b, u="cm", sq=False):
    sc = 160.0 / max(a, b)
    W, H = a * sc, b * sc
    s = ["<rect x='64' y='20' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='2.2'/>" % (W, H, FILL, GREEN),
         text(64 + W / 2, 14, "%d%s%s" % (a, NB, u), 13, weight=600)]
    if not sq:
        s.append(text(58, 24 + H / 2, "%d%s%s" % (b, NB, u), 13, weight=600, anchor="end"))
    return wrap(W + 84, H + 34, "".join(s), "rettangolo" if not sq else "quadrato", lg=True)


def s3_perimetro():
    k = R.choice(["rett", "quad", "tri", "poli"])
    if k == "rett":
        a, b = R.randint(4, 15), R.randint(2, 9)
        if a == b:
            return None
        p = 2 * (a + b)
        return mcq(rett_svg(a, b) + "Qual è il perimetro di questo rettangolo?", "%d%scm" % (p, NB),
                   ["%d%scm" % (a + b, NB), "%d%scm" % (a * b, NB), "%d%scm" % (2 * a + b, NB)],
                   "Il perimetro è la somma di tutti i lati: %d + %d + %d + %d = <b>%d cm</b>." % (a, b, a, b, p))
    if k == "quad":
        a = R.randint(3, 15)
        return mcq(rett_svg(a, a, sq=True) + "Qual è il perimetro di questo quadrato?", "%d%scm" % (4 * a, NB),
                   ["%d%scm" % (a, NB), "%d%scm" % (2 * a, NB), "%d%scm" % (a * a, NB) if a * a != 4 * a else "%d%scm" % (3 * a, NB)],
                   "Il quadrato ha 4 lati uguali: %d %s 4 = <b>%d cm</b>." % (a, FOIS, 4 * a))
    if k == "tri":
        a, b, c = sorted(R.sample(range(3, 15), 3))
        if a + b <= c:
            return None
        p = a + b + c
        return mcq("Un triangolo ha i lati lunghi %d cm, %d cm e %d cm. Qual è il suo perimetro?" % (a, b, c), "%d%scm" % (p, NB),
                   ["%d%scm" % (a + b, NB), "%d%scm" % (p + c, NB), "%d%scm" % (a * b, NB)],
                   "%d + %d + %d = <b>%d cm</b>." % (a, b, c, p))
    n = R.choice([5, 6])
    a = R.randint(3, 9)
    return mcq("Un %s regolare ha tutti i lati lunghi %d cm. Qual è il suo perimetro?" % ("pentagono" if n == 5 else "esagono", a), "%d%scm" % (n * a, NB),
               ["%d%scm" % ((n - 1) * a, NB), "%d%scm" % (4 * a, NB), "%d%scm" % (n + a, NB)],
               "Ha %d lati uguali: %d %s %d = <b>%d cm</b>." % (n, a, FOIS, n, n * a))


def quadretti(cells, W, H):
    c = 22
    s = []
    for x in range(W + 1):
        s.append(line(6 + x * c, 6, 6 + x * c, 6 + H * c, "#d0dbe6", 1))
    for y in range(H + 1):
        s.append(line(6, 6 + y * c, 6 + W * c, 6 + y * c, "#d0dbe6", 1))
    for x, y in cells:
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1'/>" % (6 + x * c, 6 + y * c, c, c, FILL, GREEN))
    return wrap(W * c + 12, H * c + 12, "".join(s), "figura su carta a quadretti", lg=True)


def figura_quadretti():
    w, h = R.randint(2, 6), R.randint(2, 4)
    cells = [(x, y) for x in range(w) for y in range(h)]
    if R.random() < 0.6:
        if w * h > 4:
            cut = R.sample([(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)], R.randint(1, 2))
            cells = [c for c in cells if c not in cut]
    return cells, w, h


def perim_cells(cells):
    S = set(cells)
    p = 0
    for x, y in cells:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + dx, y + dy) not in S:
                p += 1
    return p


def s4_quadretti():
    cells, w, h = figura_quadretti()
    a = len(cells)
    p = perim_cells(cells)
    pic = quadretti([(x + 1, y + 1) for x, y in cells], w + 2, h + 2)
    if R.random() < 0.55:
        return mcq(pic + "Quanti quadretti misura la superficie della figura colorata?", "%d quadretti" % a,
                   ["%d quadretti" % p if p != a else "%d quadretti" % (a + 2), "%d quadretti" % (a + 1), "%d quadretti" % (w * h) if w * h != a else "%d quadretti" % (a - 1)],
                   "Conta i quadretti colorati: <b>%d</b>. La superficie è lo spazio dentro la figura." % a)
    return mcq(pic + "Il lato di ogni quadretto misura 1 cm. Qual è il perimetro della figura?", "%d%scm" % (p, NB),
               ["%d%scm" % (a, NB) if a != p else "%d%scm" % (p + 2, NB), "%d%scm" % (p - 2, NB), "%d%scm" % (p + 1, NB)],
               "Conta i lati dei quadretti sul contorno: <b>%d cm</b>. Il perimetro è la lunghezza del contorno." % p)


def s5():
    k = R.choice(["recinto", "cornice", "giro", "lato", "nastro", "campo"])
    if k == "recinto":
        a, b = R.randint(8, 30), R.randint(5, 20)
        if a == b:
            return None
        return mcq("Un orto rettangolare è lungo %d m e largo %d m. Quanti metri di rete servono per recintarlo?" % (a, b), "%d m" % (2 * (a + b)),
                   ["%d m" % (a + b), "%d m" % (a * b), "%d m" % (2 * a + b)], "Perimetro: %d + %d + %d + %d = <b>%d m</b>." % (a, b, a, b, 2 * (a + b)))
    if k == "cornice":
        a = R.randint(10, 40)
        return mcq("Un quadro quadrato ha il lato di %d cm. Quanto è lunga la cornice tutto intorno?" % a, "%d cm" % (4 * a),
                   ["%d cm" % (2 * a), "%d cm" % a, "%d cm" % (4 * a + 4)], "%d %s 4 = <b>%d cm</b>." % (a, FOIS, 4 * a))
    if k == "giro":
        a, b, n = R.randint(20, 60), R.randint(10, 40), R.randint(2, 3)
        if a == b:
            return None
        p = 2 * (a + b)
        return mcq("Un cortile rettangolare misura %d m per %d m. Luca fa %d giri del cortile. Quanti metri percorre?" % (a, b, n), "%d m" % (n * p),
                   ["%d m" % p, "%d m" % (n * (a + b)), "%d m" % (p + n)], "Un giro: %d m. %d giri: %d %s %d = <b>%d m</b>." % (p, n, p, FOIS, n, n * p))
    if k == "lato":
        a = R.randint(3, 25)
        return mcq("Il perimetro di un quadrato è %d cm. Quanto misura un lato?" % (4 * a), "%d cm" % a,
                   ["%d cm" % (2 * a), "%d cm" % (4 * a), "%d cm" % (a + 4)], "%d : 4 = <b>%d cm</b>." % (4 * a, a))
    if k == "nastro":
        a, b, c = R.randint(10, 20), R.randint(10, 20), R.randint(10, 20)
        if a + b <= c or a + c <= b or b + c <= a:
            return None
        return mcq("Giulia incolla un nastro sul bordo di un triangolo con i lati di %d cm, %d cm e %d cm. Quanti centimetri di nastro usa?" % (a, b, c), "%d cm" % (a + b + c),
                   ["%d cm" % (a + b), "%d cm" % (a + b + c + 10), "%d cm" % (a * 3)], "%d + %d + %d = <b>%d cm</b>." % (a, b, c, a + b + c))
    a, p = R.randint(20, 50), None
    b = R.randint(10, a - 2)
    p = 2 * (a + b)
    return mcq("Il perimetro di un campo rettangolare è %d m. Il lato lungo misura %d m. Quanto misura il lato corto?" % (p, a), "%d m" % b,
               ["%d m" % (p - a), "%d m" % (p // 2), "%d m" % (p - 2 * a)], "Metà perimetro: %d : 2 = %d m; %d − %d = <b>%d m</b>." % (p, p // 2, p // 2, a, b))


def main():
    FRF.R = R
    seen = set()
    sets = [
        ("Riconoscere i poligoni", mix(R, seen, [(s1_nome, 12), (s1_conta, 8)])),
        ("Lati, vertici e angoli", mix(R, seen, [(s2_prop, 18), (s1_conta, 2)])),
        ("Il perimetro", mix(R, seen, [(s3_perimetro, 20)])),
        ("Perimetro e superficie con i quadretti", mix(R, seen, [(s4_quadretti, 20)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Un <b>poligono</b> è una figura piana chiusa fatta di segmenti: i <b>lati</b>. Dove due lati si incontrano c’è un <b>vertice</b>.",
         "Il <b>quadrato</b> ha 4 lati uguali e 4 angoli retti; il <b>rettangolo</b> 4 angoli retti e i lati opposti uguali; il <b>rombo</b> 4 lati uguali.",
         "Il <b>perimetro</b> è la lunghezza del contorno: si sommano tutti i lati. Quadrato: lato %s 4. Rettangolo: lato lungo + lato corto + lato lungo + lato corto." % FOIS,
         "La <b>superficie</b> è lo spazio dentro la figura: si può misurare contando i quadretti."],
        [("Rettangolo di 8 cm e 3 cm. Perimetro?", ["8 + 3 + 8 + 3 = 22"], "22 cm")],
        [["Dimenticare un lato", "Segna ogni lato mentre lo sommi."],
         ["Rettangolo: 8 + 3 = 11 cm", "I lati sono 4: 8 + 3 + 8 + 3 = 22 cm."],
         ["Confondere perimetro e superficie", "Il perimetro è il contorno (cm), la superficie è lo spazio dentro (quadretti)."]],
        rett_svg(8, 3))
    faq = [("Come si calcola il perimetro?", "Si sommano le lunghezze di tutti i lati. Nel quadrato basta fare lato × 4."),
           ("Due figure con la stessa superficie hanno lo stesso perimetro?", "Non sempre: con 6 quadretti puoi fare un rettangolo 6 × 1 (perimetro 14) o 3 × 2 (perimetro 10).")]
    make_unit(R, "figure-piane-e-perimetro", "S",
              "Riconoscere, denominare e descrivere figure geometriche piane; individuare lati, vertici e angoli; misurare il contorno (perimetro) e la superficie con unità arbitrarie e convenzionali",
              "Figure piane e perimetro: poligoni, lati e contorno", "Figure piane e perimetro",
              "Schede di matematica per la classe terza su figure piane e perimetro: poligoni, quadrato, rettangolo, rombo, triangoli, lati e vertici, perimetro, superficie con i quadretti e problemi. 100 esercizi con soluzioni.",
              "Il perimetro è la somma di tutti i lati.", "La superficie si misura contando i quadretti.",
              body, faq, sets, 18)


if __name__ == "__main__":
    main()
