# -*- coding: utf-8 -*-
"""
Italia Matematica seconda media: Trasformazioni isometriche (Spazio e figure)
  python3 tools/gen_it_matematica_m2_trasformazioni_isometriche.py
Traslazione di vettore v(a; b), simmetria assiale rispetto a rette parallele agli assi e alla bisettrice y = x,
simmetria centrale, rotazione di 90° e 180° intorno a un punto, proprietà (lunghezze e angoli invarianti, punti uniti),
assi e centri di simmetria dei poligoni, composizione di isometrie.
Errori: scambiare le componenti del vettore, ruotare in senso orario invece che antiorario, contare gli assi del rettangolo come 4.
"""
import random
from it_media import M, L, unit, mix, table, W, Kids
import gen_it_matematica_c5_trasformazioni_e_piano_cartesiano as X
from it_common import GREEN, FILL

R = random.Random(71210)
G = "seconda-media"
K = Kids(R)
X.R = R
P = X.P


def ok(*pts):
    return all(0 <= x <= 10 and 0 <= y <= 10 for x, y in pts)


def tri():
    while True:
        pts = [(R.randint(1, 5), R.randint(1, 5)) for _ in range(3)]
        (a, b), (c, d_), (e, f) = pts
        if len(set(pts)) == 3 and (c - a) * (f - b) - (d_ - b) * (e - a) != 0:
            return pts


def s1_trasla():
    T = tri()
    a, b = R.randint(1, 5), R.randint(1, 5)
    i = R.randrange(3)
    x, y = T[i]
    if not ok((x + a, y + b)):
        return None
    n = "ABC"[i]
    names = [(p[0], p[1], "ABC"[j]) for j, p in enumerate(T)]
    pic = X.piano(names, [(T, FILL)])
    return M("%sIl triangolo ABC viene traslato del vettore v(%d; %d). Quali sono le coordinate di %s′?" % (pic, a, b, n), P(x + a, y + b), W(P(x + b, y + a) if a != b else P(x + a + 1, y + b), P(x + a, y), P(x, y + b), P(x - a, y + b) if x >= a else P(x + a, y + b + 1)),
             "Si somma il vettore: (%d + %d; %d + %d) = <b>%s′%s</b>." % (x, a, y, b, n, P(x + a, y + b)))


def s1_vettore():
    x, y = R.randint(0, 5), R.randint(0, 5)
    a, b = R.randint(1, 5), R.randint(1, 5)
    if R.random() < 0.3:
        x, a = x + 5, -a
    if R.random() < 0.3:
        y, b = y + 5, -b
    if not ok((x + a, y + b)):
        return None
    sgn = lambda v: str(v).replace("-", "−")
    v = "v(%s; %s)" % (sgn(a), sgn(b))
    return M("Una traslazione porta A%s in A′%s. Qual è il vettore della traslazione?" % (P(x, y), P(x + a, y + b)), v,
             W("v(%s; %s)" % (sgn(b), sgn(a)) if a != b else "v(%s; %s)" % (sgn(a + 1), sgn(b)), "v(%s; %s)" % (sgn(-a), sgn(-b)), "v(%d; %d)" % (x + a, y + b), "v(%s; %s)" % (sgn(a), sgn(-b))),
             "v = (%d − %d; %d − %d) = <b>%s</b>." % (x + a, x, y + b, y, v))


def s2_assiale():
    k = R.choice(["x", "y", "bis"])
    if k == "bis":
        x, y = R.randint(0, 10), R.randint(0, 10)
        if x == y:
            return None
        return M("Qual è il simmetrico di A%s rispetto alla bisettrice y = x?" % P(x, y), P(y, x), W(P(10 - x, y), P(x, 10 - y), P(y, 10 - x), P(10 - y, 10 - x) if (10 - y, 10 - x) != (y, x) else P(y + 1, x)),
                 "Rispetto alla bisettrice y = x le coordinate si scambiano: <b>%s</b>." % P(y, x))
    c = R.randint(3, 7)
    if k == "x":
        x, y = R.randint(max(0, 2 * c - 10), min(10, 2 * c)), R.randint(1, 9)
        if x == c:
            return None
        pic = X.piano([(x, y, "A")], vline=c)
        return M("%sQual è il simmetrico di A%s rispetto alla retta x = %d?" % (pic, P(x, y), c), P(2 * c - x, y), W(P(x, 2 * c - y) if 0 <= 2 * c - y <= 10 and 2 * c - y != y else P(c, y), P(c, y), P(2 * c - x + 1, y) if 2 * c - x < 10 else P(2 * c - x - 1, y), P(y, x)),
                 "La distanza da x = %d è %d: il simmetrico ha ascissa %d %s %d = %d. <b>%s</b>." % (c, abs(x - c), c, "+" if x < c else "−", abs(x - c), 2 * c - x, P(2 * c - x, y)))
    y, x = R.randint(max(0, 2 * c - 10), min(10, 2 * c)), R.randint(1, 9)
    if y == c:
        return None
    return M("Qual è il simmetrico di A%s rispetto alla retta y = %d?" % (P(x, y), c), P(x, 2 * c - y), W(P(2 * c - x, y) if 0 <= 2 * c - x <= 10 and 2 * c - x != x else P(x, c), P(x, c), P(x, 2 * c - y + 1) if 2 * c - y < 10 else P(x, 2 * c - y - 1), P(y, x)),
             "La retta y = %d è orizzontale: l’ascissa resta %d, l’ordinata diventa %d. <b>%s</b>." % (c, x, 2 * c - y, P(x, 2 * c - y)))


def s3_centrale():
    c1, c2 = R.randint(3, 7), R.randint(3, 7)
    x, y = R.randint(max(0, 2 * c1 - 10), min(10, 2 * c1)), R.randint(max(0, 2 * c2 - 10), min(10, 2 * c2))
    if (x, y) == (c1, c2):
        return None
    A2 = (2 * c1 - x, 2 * c2 - y)
    if R.random() < 0.6:
        pic = X.piano([(x, y, "A"), (c1, c2, "O")])
        return M("%sQual è il simmetrico di A%s rispetto al centro O%s?" % (pic, P(x, y), P(c1, c2)), P(*A2), W(P(2 * c1 - x, y), P(x, 2 * c2 - y), P(c1 + (c1 - x) + 1, A2[1]) if A2[0] < 10 else P(A2[0] - 1, A2[1]), P(c1 - x + c1 - 1, c2) if 0 <= 2 * c1 - x - 1 else P(c1, c2)),
                 "O è il punto medio di AA′: x′ = 2 × %d − %d = %d, y′ = 2 × %d − %d = %d. <b>%s</b>." % (c1, x, A2[0], c2, y, A2[1], P(*A2)))
    return M("Nella simmetria centrale di centro O il punto A%s va in A′%s. Quali sono le coordinate di O?" % (P(x, y), P(*A2)), P(c1, c2), W(P(abs(A2[0] - x), abs(A2[1] - y)), P(x + A2[0], y + A2[1]) if ok((x + A2[0], y + A2[1])) else P(c1 + 1, c2), P(c2, c1) if c1 != c2 else P(c1, c2 + 1), P(c1, c2 - 1)),
             "O è il punto medio: ((%d + %d) : 2; (%d + %d) : 2) = <b>%s</b>." % (x, A2[0], y, A2[1], P(c1, c2)))


def s4_rot():
    c1, c2 = R.randint(3, 7), R.randint(3, 7)
    dx, dy = R.randint(-3, 3), R.randint(-3, 3)
    if dx == 0 and dy == 0:
        return None
    x, y = c1 + dx, c2 + dy
    k = R.choice([90, 90, 180, 270])
    if k == 90:
        A2, w = (c1 - dy, c2 + dx), [(c1 + dy, c2 - dx), (c1 - dx, c2 - dy), (c1 + dx, c2 - dy)]
        t = "di 90° in senso antiorario"
    elif k == 270:
        A2, w = (c1 + dy, c2 - dx), [(c1 - dy, c2 + dx), (c1 - dx, c2 - dy), (c1 - dx, c2 + dy)]
        t = "di 90° in senso orario"
    else:
        A2, w = (c1 - dx, c2 - dy), [(c1 - dy, c2 + dx), (c1 + dx, c2 - dy), (c1 - dx, c2 + dy)]
        t = "di 180°"
    w = w + [(c1 + dy, c2 + dx), (x, y), (c1 - dx, c2 + dy), (c1 + dx, c2 - dy)]
    pic = X.piano([(x, y, "A"), (c1, c2, "O")])
    e = "Rispetto a O, A è a (%d; %d). " % (dx, dy)
    e = e.replace("-", "−")
    if k == 180:
        e += "Ruotando di 180° diventa (%d; %d)" % (-dx, -dy)
    elif k == 90:
        e += "Ruotando di 90° in senso antiorario diventa (%d; %d)" % (-dy, dx)
    else:
        e += "Ruotando di 90° in senso orario diventa (%d; %d)" % (dy, -dx)
    e = e.replace("-", "−") + ": A′ = <b>%s</b>." % P(*A2)
    return M("%sIl punto A%s ruota intorno a O%s %s. Dove arriva?" % (pic, P(x, y), P(c1, c2), t), P(*A2), W(*[P(*p) for p in w if p != A2 and ok(p)]), e)


QZ = [("Un’isometria conserva…", "le lunghezze e gli angoli", ["solo le lunghezze", "solo gli angoli", "solo la forma"]),
      ("Quanti assi di simmetria ha un rettangolo (non quadrato)?", "2", ["4", "1", "0"]),
      ("Quanti assi di simmetria ha un quadrato?", "4", ["2", "1", "8"]),
      ("Quanti assi di simmetria ha un rombo (non quadrato)?", "2", ["4", "1", "0"]),
      ("Quanti assi di simmetria ha un triangolo equilatero?", "3", ["1", "6", "0"]),
      ("Quanti assi di simmetria ha un triangolo isoscele (non equilatero)?", "1", ["2", "3", "0"]),
      ("Quanti assi di simmetria ha un esagono regolare?", "6", ["3", "12", "2"]),
      ("Quanti assi di simmetria ha un triangolo scaleno?", "0", ["1", "3", "2"]),
      ("Quanti assi di simmetria ha un trapezio isoscele?", "1", ["2", "0", "4"]),
      ("Quale di questi poligoni ha un centro di simmetria ma nessun asse?", "il parallelogramma (non rombo, non rettangolo)", ["il triangolo equilatero", "il trapezio isoscele", "il triangolo isoscele"]),
      ("Il triangolo equilatero ha un centro di simmetria?", "no", ["sì", "solo se è grande", "sì, il vertice"]),
      ("Nella simmetria assiale, i punti uniti (che non si spostano) sono…", "i punti dell’asse", ["nessuno", "solo il centro", "tutti i punti"]),
      ("Nella simmetria centrale l’unico punto unito è…", "il centro", ["nessuno", "un vertice", "tutti i punti dell’asse"]),
      ("Nella traslazione (con vettore non nullo) quanti punti uniti ci sono?", "nessuno", ["uno", "infiniti", "due"]),
      ("Due simmetrie assiali con assi paralleli, una dopo l’altra, equivalgono a…", "una traslazione", ["una simmetria centrale", "una rotazione di 90°", "una simmetria assiale"]),
      ("Due simmetrie assiali con assi perpendicolari, una dopo l’altra, equivalgono a…", "una simmetria centrale", ["una traslazione", "una simmetria assiale", "nessuna trasformazione"]),
      ("La simmetria centrale equivale a una rotazione di…", "180°", ["90°", "360°", "45°"]),
      ("Quale isometria «ribalta» la figura (cambia il verso dei vertici)?", "la simmetria assiale", ["la traslazione", "la rotazione", "la simmetria centrale"]),
      ("Quanti assi di simmetria ha un pentagono regolare?", "5", ["10", "1", "2"]),
      ("Quanti assi di simmetria ha un cerchio?", "infiniti", ["1", "2", "4"])]


def s5_quiz():
    q, a, w = R.choice(QZ)
    return M(q, a, w, "Risposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Traslazioni", mix(R, seen, [(s1_trasla, 12), (s1_vettore, 8)])),
        ("Simmetria assiale", mix(R, seen, [(s2_assiale, 20)])),
        ("Simmetria centrale", mix(R, seen, [(s3_centrale, 20)])),
        ("Rotazioni", mix(R, seen, [(s4_rot, 20)])),
        ("Proprietà, assi e composizioni", mix(R, seen, [(s5_quiz, 20)])),
    ]
    body = L(["Un’<b>isometria</b> sposta una figura senza deformarla: lunghezze e angoli restano uguali. Le isometrie sono traslazione, rotazione, simmetria assiale e simmetria centrale.",
              "<b>Traslazione</b> di vettore v(a; b): (x; y) → (x + a; y + b).",
              "<b>Simmetria assiale</b>: il punto e il suo simmetrico sono alla stessa distanza dall’asse, sulla perpendicolare. Rispetto a x = k: (x; y) → (2k − x; y). Rispetto a y = x le coordinate si scambiano.",
              "<b>Simmetria centrale</b> di centro O: O è il punto medio tra A e A′. È come una rotazione di 180°.",
              "<b>Rotazione</b> di 90° in senso antiorario intorno all’origine: (x; y) → (−y; x)."],
             [("A(2; 5), simmetria rispetto a x = 4", ["distanza 2", "4 + 2 = 6"], "A′(6; 5)"), ("A(1; 3), centro O(4; 4)", ["2 × 4 − 1 = 7", "2 × 4 − 3 = 5"], "A′(7; 5)")],
             [["Scambiare le componenti del vettore", "v(3; 2): 3 in orizzontale, 2 in verticale."],
              ["Ruotare nel verso sbagliato", "Antiorario: il verso contrario alle lancette."],
              ["Il rettangolo ha 4 assi", "Le diagonali del rettangolo non sono assi: gli assi sono 2."]],
             table(["Isometria", "Punti uniti"], [["traslazione", "nessuno"], ["simmetria assiale", "i punti dell’asse"], ["simmetria centrale", "il centro"], ["rotazione", "il centro"]]))
    faq = [("Che differenza c’è tra simmetria centrale e rotazione?", "La simmetria centrale è una rotazione di 180°; le altre rotazioni hanno angoli diversi."),
           ("Le diagonali del rettangolo sono assi di simmetria?", "No: piegando il rettangolo lungo una diagonale le due parti non coincidono. Gli assi sono le due rette per i punti medi dei lati.")]
    unit(G, R, "trasformazioni-isometriche", "S",
         "Riconoscere e costruire figure ottenute da altre mediante traslazioni, rotazioni e simmetrie; conoscere le proprietà delle isometrie e usarle nel piano cartesiano",
         "Trasformazioni isometriche", "Isometrie",
         "Schede di matematica per la seconda media sulle trasformazioni isometriche: traslazione con vettore, simmetria assiale e centrale, rotazioni, assi di simmetria e composizione nel piano cartesiano. 100 esercizi con soluzioni.",
         "Le isometrie conservano lunghezze e angoli.", "Simmetria centrale = rotazione di 180°.",
         body, faq, sets, 10)


if __name__ == "__main__":
    main()
