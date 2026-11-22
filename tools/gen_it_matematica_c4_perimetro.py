# -*- coding: utf-8 -*-
"""
Italia Matematica classe quarta: Il perimetro (Spazio e figure)
  python3 tools/gen_it_matematica_c4_perimetro.py
Perimetro di poligoni, rettangoli, quadrati, poligoni regolari; perimetro sulla carta a quadretti; dal perimetro
al lato (formule inverse); figure isoperimetriche; problemi (recinti, cornici, giri di campo).
Errori: sommare solo due lati del rettangolo, confondere perimetro e area, dimenticare di trasformare le unità.
"""
import random
from it_common import mcq, lesson, make_unit, mix, table, Kids, FOIS, DIV, NB
import gen_it_matematica_c3_figure_piane_e_perimetro as F3
import gen_it_matematica_c5_perimetro_e_area_dei_poligoni as PA5

R = random.Random(70417)
G = "classe-quarta"


def cm(v):
    return "%d%scm" % (v, NB)


def s2_quadretti():
    it = F3.s4_quadretti()
    return it if it and "perimetro" in it["q"] else None


def s3_inverso():
    k = R.choice(["quad", "rett", "eq", "rombo", "pent", "esag"])
    if k == "quad":
        a = R.randint(3, 40)
        return mcq("Un quadrato ha il perimetro di %s. Quanto misura il lato?" % cm(4 * a), cm(a), [cm(2 * a), cm(4 * a - 4), cm(a + 4)], "lato = perimetro %s 4 = %d %s 4 = <b>%s</b>." % (DIV, 4 * a, DIV, cm(a)))
    if k == "rett":
        a, b = R.randint(3, 25), R.randint(8, 40)
        if a == b:
            return None
        p = 2 * (a + b)
        return mcq("Un rettangolo ha il perimetro di %s e la base di %s. Quanto misura l’altezza?" % (cm(p), cm(b)), cm(a), [cm(p - b), cm(p // 2), cm(p - 2 * b) if p - 2 * b != a else cm(a + b)],
                   "Base + altezza = metà perimetro: %d %s 2 = %d; altezza = %d − %d = <b>%s</b>." % (p, DIV, p // 2, p // 2, b, cm(a)))
    n, nome = {"eq": (3, "un triangolo equilatero"), "rombo": (4, "un rombo"), "pent": (5, "un pentagono regolare"), "esag": (6, "un esagono regolare")}[k]
    a = R.randint(3, 30)
    return mcq("Il perimetro di %s è %s. Quanto misura un lato?" % (nome, cm(n * a)), cm(a), [cm(n * a // 2) if n * a % 2 == 0 else cm(a + 2), cm(a + n), cm(n * a - n)],
               "Ha %d lati uguali: %d %s %d = <b>%s</b>." % (n, n * a, DIV, n, cm(a)))


def s4_iso():
    p = R.choice([12, 16, 20, 24, 28, 30, 36, 40])
    s = p // 2
    ok = R.randint(1, s - 1)
    if ok * 2 == s:
        ok = 1
    good = "%d cm e %d cm" % (ok, s - ok)
    bad = []
    for _ in range(10):
        x = R.randint(1, s)
        y = R.randint(1, s)
        if x + y != s and x <= y and "%d cm e %d cm" % (x, y) not in bad:
            bad.append("%d cm e %d cm" % (x, y))
    if R.random() < 0.5:
        return mcq("Quale rettangolo ha il perimetro di %s? (sono indicate la base e l’altezza)" % cm(p), good, bad,
                   "Base + altezza deve fare %d %s 2 = %d: <b>%s</b>." % (p, DIV, s, good))
    q, a, w = R.choice([("Due figure con lo stesso perimetro si chiamano…", "isoperimetriche", ["equiestese", "congruenti", "simmetriche"]),
                        ("Un quadrato e un rettangolo hanno lo stesso perimetro. Hanno anche la stessa forma?", "no, possono avere forme diverse", ["sì, sempre", "sì, se sono grandi", "solo se sono quadrati"]),
                        ("Con uno spago lungo %d cm formi un quadrato. Quanto è lungo il lato?" % p, cm(p // 4), [cm(p // 2), cm(p), cm(p * 4)]),
                        ("Un rettangolo di %s × %s e un quadrato di lato %s: quale perimetro è maggiore?" % (cm(s - 2), cm(2), cm(s // 2)),
                         "sono uguali" if 4 * (s // 2) == p else "il rettangolo", ["il quadrato", "non si può sapere", "il rettangolo" if 4 * (s // 2) == p else "sono uguali"])])
    return mcq(q, a, w, "Risposta: <b>%s</b>." % a)


def s5():
    k = R.choice(["recinto", "cornice", "campo", "nastro", "giardino", "piastrelle"])
    if k == "recinto":
        a, b = R.randint(8, 40), R.randint(5, 25)
        pr = R.choice([3, 4, 5, 6])
        if a == b:
            return None
        return mcq("Un orto rettangolare misura %d m × %d m. La rete costa %d € al metro. Quanto si spende per recintarlo?" % (a, b, pr), "%d €" % (2 * (a + b) * pr),
                   ["%d €" % ((a + b) * pr), "%d €" % (a * b * pr), "%d €" % (2 * (a + b))], "Perimetro: (%d + %d) %s 2 = %d m; %d %s %d = <b>%d €</b>." % (a, b, FOIS, 2 * (a + b), 2 * (a + b), FOIS, pr, 2 * (a + b) * pr))
    if k == "cornice":
        a, b = R.randint(15, 60), R.randint(10, 40)
        if a == b:
            return None
        return mcq("Un quadro rettangolare misura %d cm × %d cm. Quanti centimetri di cornice servono per contornarlo?" % (a, b), cm(2 * (a + b)),
                   [cm(a + b), cm(a * b), cm(4 * a)], "(%d + %d) %s 2 = <b>%s</b>." % (a, b, FOIS, cm(2 * (a + b))))
    if k == "campo":
        a, b = R.choice([(100, 60), (90, 50), (105, 68), (40, 20), (28, 15)])
        g = R.randint(2, 5)
        return mcq("Un campo rettangolare misura %d m × %d m. Luca fa %d giri del campo correndo lungo il bordo. Quanti metri percorre?" % (a, b, g), "%d m" % (2 * (a + b) * g),
                   ["%d m" % (2 * (a + b)), "%d m" % ((a + b) * g), "%d m" % (a * b)], "Un giro = (%d + %d) %s 2 = %d m; %d %s %d = <b>%d m</b>." % (a, b, FOIS, 2 * (a + b), 2 * (a + b), FOIS, g, 2 * (a + b) * g))
    if k == "nastro":
        a = R.randint(10, 30)
        return mcq("Una scatola ha il coperchio quadrato con il lato di %d cm. Si mette un nastro tutto intorno al coperchio e servono altri 30 cm per il fiocco. Quanti cm di nastro servono?" % a,
                   cm(4 * a + 30), [cm(4 * a), cm(a * a + 30), cm(2 * a + 30)], "%d %s 4 = %d; %d + 30 = <b>%s</b>." % (a, FOIS, 4 * a, 4 * a, cm(4 * a + 30)))
    if k == "giardino":
        a = R.randint(5, 20)
        n = R.choice([5, 6, 8])
        nome = {5: "pentagono", 6: "esagono", 8: "ottagono"}[n]
        return mcq("Un’aiuola ha la forma di un %s regolare con il lato di %d m. Quanti metri di bordura servono?" % (nome, a), "%d m" % (n * a),
                   ["%d m" % ((n - 1) * a), "%d m" % (4 * a), "%d m" % (n + a)], "%d lati: %d %s %d = <b>%d m</b>." % (n, a, FOIS, n, n * a))
    a, b = R.randint(3, 9), R.randint(2, 6)
    if a == b:
        return None
    return mcq("Un tavolo rettangolare misura %d dm × %d dm. Quanti centimetri misura il suo perimetro?" % (a, b), cm(2 * (a + b) * 10),
               [cm(2 * (a + b)), cm((a + b) * 10), cm(a * b * 10)], "Perimetro: (%d + %d) %s 2 = %d dm = <b>%s</b>." % (a, b, FOIS, 2 * (a + b), cm(2 * (a + b) * 10)))


def main():
    for m in (F3, PA5):
        m.R = R
    PA5.K = Kids(R)
    seen = set()
    sets = [
        ("Calcolare il perimetro", mix(R, seen, [(PA5.s1_perimetro, 12), (F3.s3_perimetro, 8)])),
        ("Perimetro con i quadretti", mix(R, seen, [(s2_quadretti, 20)])),
        ("Dal perimetro al lato", mix(R, seen, [(s3_inverso, 20)])),
        ("Figure isoperimetriche", mix(R, seen, [(s4_iso, 20)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Il <b>perimetro</b> è la lunghezza del contorno di una figura: si trova sommando tutti i lati.",
         "Rettangolo: P = (base + altezza) %s 2. Quadrato e poligoni regolari: P = lato %s numero dei lati." % (FOIS, FOIS),
         "Formule inverse: lato del quadrato = P %s 4; nel rettangolo base + altezza = P %s 2." % (DIV, DIV),
         "Figure con lo stesso perimetro si chiamano <b>isoperimetriche</b>; possono avere forme diverse."],
        [("Rettangolo 12 cm × 5 cm", ["(12 + 5) %s 2" % FOIS, "17 %s 2 = 34" % FOIS], "34 cm")],
        [["Sommare solo base e altezza", "Il rettangolo ha 4 lati: moltiplica per 2."],
         ["Confondere perimetro e area", "Il perimetro è il contorno (cm), l’area è la superficie (cm²)."],
         ["Sommare misure in unità diverse", "Prima trasforma tutto nella stessa unità."]],
        table(["Figura", "Perimetro", "Lato dal perimetro"], [["quadrato", "l %s 4" % FOIS, "P %s 4" % DIV], ["rettangolo", "(b + h) %s 2" % FOIS, "b = P %s 2 − h" % DIV], ["triangolo equilatero", "l %s 3" % FOIS, "P %s 3" % DIV]]))
    faq = [("A che cosa serve il perimetro nella vita di tutti i giorni?", "A sapere quanta rete serve per un recinto, quanta cornice per un quadro, quanta strada si fa a girare intorno a un campo."),
           ("Due rettangoli con lo stesso perimetro hanno la stessa area?", "No: 9 × 1 e 5 × 5 hanno lo stesso perimetro (20), ma aree diverse (9 e 25).")]
    make_unit(R, "perimetro", "S",
              "Determinare il perimetro di una figura utilizzando le più comuni formule o altri procedimenti; riconoscere figure isoperimetriche",
              "Il perimetro dei poligoni", "Perimetro",
              "Schede di matematica per la classe quarta sul perimetro: rettangolo, quadrato, poligoni regolari, carta a quadretti, formule inverse, figure isoperimetriche e problemi. 100 esercizi con soluzioni.",
              "Il perimetro è la lunghezza del contorno.", "Rettangolo: (base + altezza) × 2.",
              body, faq, sets, 17, grade=G)


if __name__ == "__main__":
    main()
