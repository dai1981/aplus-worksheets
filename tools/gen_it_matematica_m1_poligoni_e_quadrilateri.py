# -*- coding: utf-8 -*-
"""
Italia Matematica prima media: Poligoni e quadrilateri (Spazio e figure)
  python3 tools/gen_it_matematica_m1_poligoni_e_quadrilateri.py
Poligoni convessi e concavi, regolari; numero delle diagonali n(n − 3) : 2; somma degli angoli interni (n − 2) × 180°;
somma degli angoli esterni 360°; angolo di un poligono regolare; quadrilateri (trapezi, parallelogrammi, rombi,
rettangoli, quadrati) e loro proprietà; perimetro.
Errori: contare due volte le diagonali, usare n × 180°, credere che un poligono con i lati uguali sia sempre regolare.
"""
import random
from it_media import M, L, unit, mix, table, W, FOIS, DIV
import gen_it_matematica_c4_quadrilateri as Q4

R = random.Random(71114)
G = "prima-media"
NOMI = {3: "triangolo", 4: "quadrilatero", 5: "pentagono", 6: "esagono", 7: "ettagono", 8: "ottagono", 9: "ennagono", 10: "decagono", 12: "dodecagono"}


def s1_diag():
    n = R.choice(list(NOMI))
    d = n * (n - 3) // 2
    if R.random() < 0.5:
        return M("Quante diagonali ha un %s (%d lati)?" % (NOMI[n], n), str(d), W(n * (n - 3), n - 3, n, d + 1), "n × (n − 3) : 2 = %d × %d : 2 = <b>%d</b>." % (n, n - 3, d))
    return M("Da un vertice di un %s quante diagonali partono?" % NOMI[n], str(n - 3), W(n - 2, n - 1, d, n), "Non si contano il vertice stesso e i due vicini: %d − 3 = <b>%d</b>." % (n, n - 3))


def s2_somma():
    n = R.choice(list(NOMI))
    s = (n - 2) * 180
    k = R.random()
    if k < 0.45:
        return M("Quanto misura la somma degli angoli interni di un %s?" % NOMI[n], "%d°" % s, W("%d°" % (n * 180), "%d°" % ((n - 1) * 180), "360°" if s != 360 else "180°", "%d°" % (n * 90)),
                 "(n − 2) × 180° = %d × 180° = <b>%d°</b>." % (n - 2, s))
    if k < 0.75:
        if s % n:
            return None
        return M("Quanto misura ciascun angolo interno di un %s regolare?" % NOMI[n], "%d°" % (s // n), W("%d°" % (360 // n) if 360 % n == 0 else None, "%d°" % (180 - s // n) if 180 - s // n != s // n else None, "%d°" % (s // (n - 1)) if s % (n - 1) == 0 else "%d°" % (s // n + 10), "%d°" % s),
                 "%d° : %d = <b>%d°</b>." % (s, n, s // n))
    if 360 % n:
        return None
    return M("Quanto misura ciascun angolo esterno di un %s regolare?" % NOMI[n], "%d°" % (360 // n), W("%d°" % (s // n) if s % n == 0 else None, "%d°" % (180 // n) if 180 % n == 0 else "%d°" % (360 // n + 10), "360°", "%d°" % (360 // n * 2)),
             "La somma degli angoli esterni è sempre 360°: 360° : %d = <b>%d°</b>." % (n, 360 // n))


def s2_inverso():
    n = R.choice([5, 6, 8, 9, 10, 12])
    s = (n - 2) * 180
    if R.random() < 0.5:
        return M("La somma degli angoli interni di un poligono è %d°. Quanti lati ha?" % s, str(n), W(n - 2, n + 2, s // 180, n + 1), "%d° : 180° = %d; %d + 2 = <b>%d</b> lati." % (s, n - 2, n - 2, n))
    a = s // n if s % n == 0 else None
    if a is None:
        return None
    return M("Ogni angolo interno di un poligono regolare misura %d°. Quanti lati ha?" % a, str(n), W(n + 1, n - 1, 360 // (180 - a) + 2 if 360 % (180 - a) == 0 else n + 2, 180 - a),
             "L’angolo esterno è 180° − %d° = %d°; 360° : %d° = <b>%d</b> lati." % (a, 180 - a, 180 - a, n))


def s3_quad():
    return Q4.s1_nome() if R.random() < 0.5 else Q4.s2_prop()


def s5():
    return Q4.s5_perimetro() if R.random() < 0.6 else Q4.s4_angoli()


QUIZ = [("Un poligono si dice regolare se…", "ha tutti i lati e tutti gli angoli congruenti", ["ha tutti i lati congruenti", "ha tutti gli angoli congruenti", "è convesso"]),
        ("Il rombo è un poligono regolare?", "no, ha i lati uguali ma gli angoli no", ["sì, ha i lati uguali", "sì, sempre", "solo se è grande"]),
        ("Un poligono è concavo se…", "il prolungamento di almeno un lato lo attraversa", ["ha almeno un angolo acuto", "ha tutti i lati uguali", "ha meno di 5 lati"]),
        ("Qual è il poligono con il minor numero di lati?", "il triangolo", ["il quadrilatero", "il segmento", "il pentagono"]),
        ("Quante diagonali ha un triangolo?", "nessuna", ["1", "3", "2"]),
        ("Che cosa hanno in comune un parallelogramma e un rettangolo?", "due coppie di lati paralleli", ["quattro angoli retti", "quattro lati uguali", "le diagonali perpendicolari"])]


def s4_quiz():
    q, a, w = R.choice(QUIZ)
    return M(q, a, w, "Risposta: <b>%s</b>." % a)


def main():
    Q4.R = R
    seen = set()
    sets = [
        ("Poligoni e diagonali", mix(R, seen, [(s1_diag, 14), (s4_quiz, 6)])),
        ("Angoli dei poligoni", mix(R, seen, [(s2_somma, 14), (s2_inverso, 6)])),
        ("Quadrilateri", mix(R, seen, [(s3_quad, 14), (Q4.s3_rel, 6)])),
        ("Angoli dei quadrilateri", mix(R, seen, [(Q4.s4_angoli, 14), (Q4.s3_conta, 6)])),
        ("Problemi", mix(R, seen, [(s5, 14), (s2_inverso, 6)])),
    ]
    body = L(["Un <b>poligono</b> è la parte di piano delimitata da una spezzata chiusa non intrecciata. È <b>regolare</b> se ha tutti i lati e tutti gli angoli congruenti.",
              "Un poligono di n lati ha <b>n × (n − 3) : 2</b> diagonali; da ogni vertice ne partono n − 3.",
              "Somma degli angoli interni: <b>(n − 2) × 180°</b>. Somma degli angoli esterni (convesso): sempre <b>360°</b>.",
              "Quadrilateri: il trapezio ha una coppia di lati paralleli, il parallelogramma due; rombo, rettangolo e quadrato sono parallelogrammi particolari."],
             [("Esagono regolare", ["somma interni: 4 × 180° = 720°", "angolo interno: 720° : 6 = 120°", "diagonali: 6 × 3 : 2 = 9"], "120° e 9 diagonali")],
             [["Contare n × (n − 3) diagonali", "Ogni diagonale si conta due volte: dividi per 2."],
              ["Calcolare la somma degli angoli con n × 180°", "Un poligono di n lati si divide in n − 2 triangoli."],
              ["Pensare che il rombo sia regolare", "Ha i lati uguali, ma gli angoli no (tranne il quadrato)."]],
             table(["Poligono", "Lati", "Somma angoli interni", "Diagonali"], [[NOMI[n], str(n), "%d°" % ((n - 2) * 180), str(n * (n - 3) // 2)] for n in (3, 4, 5, 6, 8)]))
    faq = [("Perché la somma degli angoli esterni è sempre 360°?", "Percorrendo il contorno di un poligono convesso si fa un giro completo: in ogni vertice si gira di un angolo esterno."),
           ("Come si ricorda la formula delle diagonali?", "Da ogni vertice partono n − 3 diagonali (non verso sé stesso né verso i due vicini); i vertici sono n e ogni diagonale si conta due volte.")]
    unit(G, R, "poligoni-e-quadrilateri", "S",
         "Conoscere definizioni e proprietà significative dei poligoni e dei quadrilateri (lati, angoli, diagonali); calcolare la somma degli angoli interni ed esterni",
         "Poligoni e quadrilateri: angoli e diagonali", "Poligoni e quadrilateri",
         "Schede di matematica per la prima media su poligoni e quadrilateri: poligoni regolari, diagonali, somma degli angoli interni ed esterni, trapezi, parallelogrammi, rombi, rettangoli, quadrati e problemi. 100 esercizi con soluzioni.",
         "Somma angoli interni: (n − 2) × 180°.", "Diagonali: n × (n − 3) : 2.",
         body, faq, sets, 14)


if __name__ == "__main__":
    main()
