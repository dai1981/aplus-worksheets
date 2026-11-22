# -*- coding: utf-8 -*-
"""
Italia Matematica classe quinta: Trasformazioni e piano cartesiano (Spazio e figure)
  python3 tools/gen_it_matematica_c5_trasformazioni_e_piano_cartesiano.py
Coordinate di un punto (x; y) nel primo quadrante, trovare un punto, traslazione (vettore), simmetria rispetto a
una retta, rotazione di un quarto e di mezzo giro intorno all’origine o a un punto, ingrandimenti e riduzioni in scala.
Errori: scambiare x e y, contare i quadretti partendo da 1, nella simmetria spostare invece di ribaltare.
"""
import random
from it_common import mcq, lesson, make_unit, mix, wrap, text, line, INK, GREEN, RED, BLUE, FILL, FOIS

R = random.Random(70520)
G = "classe-quinta"
U = 28
N = 10


def P(x, y):
    return "(%d; %d)" % (x, y)


def piano(points=(), polys=(), vline=None):
    s = []
    ox, oy = 30, 30 + N * U
    for i in range(N + 1):
        s.append(line(ox + i * U, oy, ox + i * U, oy - N * U, "#d0dbe6", 1))
        s.append(line(ox, oy - i * U, ox + N * U, oy - i * U, "#d0dbe6", 1))
        s.append(text(ox + i * U, oy + 16, str(i), 11, weight=400))
        if i:
            s.append(text(ox - 8, oy - i * U + 4, str(i), 11, anchor="end", weight=400))
    s.append(line(ox, oy, ox + N * U + 8, oy, INK, 1.8))
    s.append(line(ox, oy, ox, oy - N * U - 8, INK, 1.8))
    s.append(text(ox + N * U + 14, oy + 4, "x", 13))
    s.append(text(ox, oy - N * U - 14, "y", 13))
    if vline is not None:
        s.append(line(ox + vline * U, oy + 4, ox + vline * U, oy - N * U - 4, RED, 2.2, "stroke-dasharray='6 4'"))
    for pts, col in polys:
        s.append("<polygon points='%s' fill='%s' fill-opacity='0.55' stroke='%s' stroke-width='2'/>" % (" ".join("%d,%d" % (ox + x * U, oy - y * U) for x, y in pts), col, INK))
    for x, y, lab in points:
        s.append("<circle cx='%d' cy='%d' r='4.5' fill='%s'/>" % (ox + x * U, oy - y * U, BLUE))
        s.append(text(ox + x * U + 8, oy - y * U - 7, lab, 13, anchor="start", col=BLUE))
    return wrap(N * U + 60, N * U + 56, "".join(s), "piano cartesiano con assi x e y da 0 a 10", lg=True)


def s1_leggi():
    x, y = R.randint(1, 9), R.randint(1, 9)
    if x == y:
        return None
    return mcq(piano([(x, y, "A")]) + "Quali sono le coordinate del punto A?", P(x, y), [P(y, x), P(x + 1, y + 1), P(x, y - 1) if y > 1 else P(x - 1, y)],
               "Prima si legge la x (in orizzontale), poi la y (in verticale): A = <b>%s</b>." % P(x, y))


def s1_trova():
    pts = []
    labs = "ABCD"
    while len(pts) < 4:
        p = (R.randint(1, 9), R.randint(1, 9))
        if p not in pts and (p[1], p[0]) not in pts:
            pts.append(p)
    k = R.randrange(4)
    x, y = pts[k]
    if x == y:
        return None
    others = [labs[i] for i in range(4) if i != k]
    return mcq(piano([(a, b, labs[i]) for i, (a, b) in enumerate(pts)]) + "Quale punto ha coordinate %s?" % P(x, y), labs[k], others,
               "Vai a destra di %d e in alto di %d: è il punto <b>%s</b>." % (x, y, labs[k]))


def s2_traslazione():
    x, y = R.randint(1, 6), R.randint(1, 6)
    a, b = R.randint(1, 3), R.randint(1, 3)
    dx, dy = R.choice([(a, b), (a, 0), (0, b), (a, -b) if y - b >= 0 else (a, b)])
    nx, ny = x + dx, y + dy
    if not (0 <= nx <= 10 and 0 <= ny <= 10):
        return None
    desc = []
    if dx:
        desc.append("%d %s a destra" % (dx, "quadretto" if dx == 1 else "quadretti"))
    if dy:
        desc.append("%d %s %s" % (abs(dy), "quadretto" if abs(dy) == 1 else "quadretti", "in alto" if dy > 0 else "in basso"))
    return mcq(piano([(x, y, "A")]) + "Il punto A viene traslato di %s. Quali sono le coordinate del nuovo punto?" % " e ".join(desc), P(nx, ny),
               [P(x + dy, y + dx) if (dx, dy) != (dy, dx) else P(nx + 1, ny), P(x - dx, y - dy) if x - dx >= 0 and y - dy >= 0 else P(nx, ny + 1), P(ny, nx) if nx != ny else P(nx + 1, ny + 1)],
               "Nella traslazione aggiungi %d alla x e %s alla y: <b>%s</b>." % (dx, ("%d" % dy) if dy >= 0 else "−%d" % -dy, P(nx, ny)))


def s2_tri():
    x, y = R.randint(1, 4), R.randint(1, 4)
    tri = [(x, y), (x + 2, y), (x, y + 2)]
    dx, dy = R.randint(2, 4), R.randint(1, 3)
    img = [(a + dx, b + dy) for a, b in tri]
    return mcq(piano(polys=[(tri, "#cfe6d6"), (img, "#c9dcf2")]) + "Il triangolo verde è stato traslato fino al triangolo blu. Di quanto si è spostato?",
               "%d a destra e %d in alto" % (dx, dy), ["%d a destra e %d in alto" % (dy, dx) if dx != dy else "%d a destra e %d in alto" % (dx + 1, dy), "%d a sinistra e %d in basso" % (dx, dy), "%d a destra e %d in alto" % (dx + 2, dy + 2)],
               "Segui un vertice: da %s a %s, cioè <b>%d a destra e %d in alto</b>. Tutti i punti si spostano allo stesso modo." % (P(*tri[0]), P(*img[0]), dx, dy))


def s3_simmetria():
    m = R.choice([4, 5, 6])
    x, y = R.randint(0, m - 1), R.randint(1, 9)
    nx = 2 * m - x
    if nx > 10:
        return None
    return mcq(piano([(x, y, "A")], vline=m) + "Qual è il simmetrico del punto A rispetto alla retta rossa (x = %d)?" % m, P(nx, y),
               [P(x + 2 * (m - x) - 1, y), P(x, 2 * m - y) if 0 <= 2 * m - y <= 10 and 2 * m - y != y else P(nx + 1, y), P(m + (m - x) + 2, y) if m + (m - x) + 2 <= 10 else P(nx - 2, y)],
               "A è a %d %s dalla retta: il simmetrico è dall’altra parte, alla stessa distanza. <b>%s</b>." % (m - x, "quadretto" if m - x == 1 else "quadretti", P(nx, y)))


ROT = [("Una figura ruota di un quarto di giro. Di quanti gradi ruota?", "90°", ["45°", "180°", "360°"]),
       ("Una figura ruota di mezzo giro. Di quanti gradi ruota?", "180°", ["90°", "360°", "120°"]),
       ("Dopo una rotazione di 360° la figura…", "torna nella posizione di partenza", ["è capovolta", "è spostata a destra", "è più grande"]),
       ("Nella rotazione la figura cambia forma o grandezza?", "no, resta uguale", ["sì, diventa più grande", "sì, diventa più piccola", "cambia forma"]),
       ("Nella traslazione tutti i punti si spostano…", "nella stessa direzione e della stessa lunghezza", ["in direzioni diverse", "girando intorno a un punto", "ribaltandosi"]),
       ("Quale trasformazione ribalta la figura come in uno specchio?", "la simmetria", ["la traslazione", "la rotazione", "l’ingrandimento"]),
       ("Quale trasformazione cambia la grandezza ma non la forma?", "l’ingrandimento o la riduzione in scala", ["la traslazione", "la simmetria", "la rotazione"]),
       ("La lancetta dei minuti in 15 minuti ruota di…", "90°", ["15°", "180°", "45°"]),
       ("La lancetta dei minuti in mezz’ora ruota di…", "180°", ["30°", "90°", "360°"]),
       ("La lancetta dei minuti in un’ora ruota di…", "360°", ["60°", "180°", "90°"]),
       ("Il punto (3; 0) ruota di mezzo giro intorno all’origine (0; 0). Dove arriva?", "(−3; 0)", ["(0; 3)", "(3; 0)", "(0; −3)"]),
       ("Quali trasformazioni non cambiano né forma né grandezza?", "traslazione, rotazione e simmetria", ["solo la traslazione", "ingrandimento e riduzione", "nessuna"])]


def s3_rotazione():
    q, a, w = R.choice(ROT)
    return mcq(q, a, w, "Risposta: <b>%s</b>." % a, neg=True)


def s4_scala():
    k = R.choice(["ingr", "rid", "fattore", "mappa"])
    a, b = R.randint(2, 8), R.randint(2, 6)
    if k == "ingr":
        f = R.randint(2, 4)
        return mcq("Un rettangolo di %d cm %s %d cm viene ingrandito %d volte (in scala %d : 1). Quali sono le nuove misure?" % (a, FOIS, b, f, f), "%d cm %s %d cm" % (a * f, FOIS, b * f),
                   ["%d cm %s %d cm" % (a + f, FOIS, b + f), "%d cm %s %d cm" % (a * f, FOIS, b), "%d cm %s %d cm" % (a * f * f, FOIS, b * f * f)],
                   "In un ingrandimento ogni lato si moltiplica per %d: <b>%d cm %s %d cm</b>. La forma resta uguale." % (f, a * f, FOIS, b * f))
    if k == "rid":
        f = R.choice([2, 3, 4])
        return mcq("Un disegno di %d cm %s %d cm viene ridotto in scala 1 : %d. Quali sono le nuove misure?" % (a * f, FOIS, b * f, f), "%d cm %s %d cm" % (a, FOIS, b),
                   ["%d cm %s %d cm" % (a * f - f, FOIS, b * f - f), "%d cm %s %d cm" % (a * f * f, FOIS, b * f * f), "%d cm %s %d cm" % (a, FOIS, b * f)],
                   "Ogni lato si divide per %d: <b>%d cm %s %d cm</b>." % (f, a, FOIS, b))
    if k == "fattore":
        f = R.randint(2, 5)
        return mcq("Un quadrato con il lato di %d cm diventa un quadrato con il lato di %d cm. In che scala è stato ingrandito?" % (a, a * f), "%d : 1" % f, ["1 : %d" % f, "%d : 1" % (a * f - a) if a * f - a != f else "%d : 1" % (f + 1), "%d : 1" % (a * f)],
                   "%d %s %d = %d: ingrandimento in scala <b>%d : 1</b>." % (a * f, ":", a, f, f))
    s_ = R.choice([100, 1000, 10000, 100000])
    cm = R.randint(2, 9)
    real = cm * s_
    unit = "%d cm" % real if real < 100 else "%d m" % (real // 100) if real < 100000 else "%d km" % (real // 100000)
    from it_common import num
    return mcq("Su una mappa in scala 1 : %s, una strada è lunga %d cm. Quanto è lunga nella realtà?" % (num(s_), cm), unit,
               ["%d cm" % (cm * 10), ("%d m" % (real // 1000) if real >= 1000 else "%d mm" % real), "%s cm" % num(cm + s_)],
               "1 cm sulla mappa = %s cm nella realtà: %d %s %s = %s cm = <b>%s</b>." % (num(s_), cm, FOIS, num(s_), num(real), unit))


def main():
    seen = set()
    sets = [
        ("Coordinate nel piano", mix(R, seen, [(s1_leggi, 12), (s1_trova, 8)])),
        ("Traslazioni", mix(R, seen, [(s2_traslazione, 12), (s2_tri, 8)])),
        ("Simmetria e rotazione", mix(R, seen, [(s3_simmetria, 10), (s3_rotazione, 10)])),
        ("Ingrandimenti e riduzioni in scala", mix(R, seen, [(s4_scala, 20)])),
        ("Trasformazioni miste", mix(R, seen, [(s1_leggi, 5), (s2_traslazione, 5), (s3_simmetria, 5), (s4_scala, 5)])),
    ]
    body = lesson(
        ["Nel <b>piano cartesiano</b> ogni punto ha due coordinate (x; y): prima quanto vai a destra (asse x), poi quanto sali (asse y). L’origine è (0; 0).",
         "<b>Traslazione</b>: tutti i punti si spostano nella stessa direzione e della stessa lunghezza. <b>Rotazione</b>: la figura gira intorno a un punto (90° = un quarto di giro).",
         "<b>Simmetria</b>: la figura si ribalta rispetto a una retta; ogni punto e il suo simmetrico sono alla stessa distanza dalla retta.",
         "Traslazione, rotazione e simmetria non cambiano forma e grandezza. Ingrandimenti e riduzioni in scala cambiano la grandezza ma non la forma."],
        [("A (2; 3) traslato di 4 a destra e 1 in alto", ["x: 2 + 4 = 6", "y: 3 + 1 = 4"], "(6; 4)")],
        [["Scambiare x e y", "Prima l’asse orizzontale (x), poi quello verticale (y)."],
         ["Contare i quadretti partendo da 1", "Si parte dall’origine 0."],
         ["Nella simmetria spostare la figura", "Ribalta: il punto più vicino alla retta resta il più vicino."]],
        piano([(2, 3, "A"), (6, 4, "A′")]))
    faq = [("Perché le coordinate si scrivono tra parentesi?", "Per indicare che i due numeri vanno insieme e in ordine: (3; 5) è diverso da (5; 3)."),
           ("Che cosa vuol dire scala 1 : 100?", "Che 1 cm sul disegno corrisponde a 100 cm (1 m) nella realtà.")]
    make_unit(R, "trasformazioni-e-piano-cartesiano", "S",
              "Utilizzare il piano cartesiano per localizzare punti; riconoscere figure ruotate, traslate e riflesse; riprodurre in scala una figura assegnata",
              "Trasformazioni e piano cartesiano", "Trasformazioni e piano cartesiano",
              "Schede di matematica per la classe quinta su trasformazioni e piano cartesiano: coordinate, traslazioni, simmetria, rotazioni, ingrandimenti, riduzioni e scale. 100 esercizi con soluzioni.",
              "Prima la x, poi la y.", "Traslazione, rotazione e simmetria non cambiano forma né grandezza.",
              body, faq, sets, 20, grade=G)


if __name__ == "__main__":
    main()
