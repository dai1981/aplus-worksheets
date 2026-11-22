# -*- coding: utf-8 -*-
"""
Italia Matematica classe quinta: Perimetro e area dei poligoni (Spazio e figure)
  python3 tools/gen_it_matematica_c5_perimetro_e_area_dei_poligoni.py
Perimetro di poligoni (e poligoni regolari), area di rettangolo, quadrato, parallelogramma, triangolo, rombo,
trapezio; formule inverse (lato dal perimetro, altezza dall’area), figure composte, problemi.
Errori: confondere perimetro e area, triangolo senza «: 2», usare il lato obliquo come altezza, unità cm invece di cm².
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, Kids, wrap, text, line, table, INK, GREEN, FILL, RED, NB, FOIS, DIV

R = random.Random(70517)
G = "classe-quinta"
K = Kids(R)


def poly(pts):
    return "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.2'/>" % (" ".join("%.1f,%.1f" % p for p in pts), FILL, GREEN)


def dash(x1, y1, x2, y2):
    return line(x1, y1, x2, y2, RED, 1.8, "stroke-dasharray='5 4'")


def lab(x, y, t, anchor="middle"):
    return text(x, y, t, 13, anchor=anchor, weight=600)


def cm(v):
    return "%s%scm" % (num(v), NB)


def fig(kind, a, b=None, c=None):
    """disegno con le misure; a, b, c in cm"""
    s = []
    if kind == "rett":
        sc = 180.0 / max(a, b)
        W, H = a * sc, b * sc
        s += [poly([(64, 20), (64 + W, 20), (64 + W, 20 + H), (64, 20 + H)]), lab(64 + W / 2, 14, cm(a)), lab(58, 24 + H / 2, cm(b), "end")]
        return wrap(W + 84, H + 32, "".join(s), "rettangolo", lg=True)
    if kind == "quad":
        s += [poly([(30, 20), (150, 20), (150, 140), (30, 140)]), lab(90, 14, cm(a))]
        return wrap(180, 150, "".join(s), "quadrato", lg=True)
    if kind == "tri":
        s += [poly([(20, 140), (220, 140), (150, 20)]), dash(150, 20, 150, 140), lab(120, 158, "base %s" % cm(a)), lab(144, 90, "h %s" % cm(b), "end")]
        return wrap(260, 166, "".join(s), "triangolo con base e altezza", lg=True)
    if kind == "para":
        s += [poly([(20, 130), (190, 130), (240, 30), (70, 30)]), dash(70, 30, 70, 130), lab(105, 148, "base %s" % cm(a)), lab(76, 85, "h %s" % cm(b), "start")]
        if c:
            s.append(lab(232, 90, cm(c), "start"))
        return wrap(300, 156, "".join(s), "parallelogramma con base e altezza", lg=True)
    if kind == "rombo":
        s += [poly([(130, 10), (230, 90), (130, 170), (30, 90)]), dash(30, 90, 230, 90), dash(130, 10, 130, 170), lab(80, 84, "D %s" % cm(a)), lab(136, 118, "d %s" % cm(b), "start")]
        return wrap(260, 180, "".join(s), "rombo con le diagonali", lg=True)
    s += [poly([(20, 140), (240, 140), (180, 40), (70, 40)]), dash(70, 40, 70, 140), lab(130, 158, "B %s" % cm(a)), lab(125, 32, "b %s" % cm(b)), lab(76, 95, "h %s" % cm(c), "start")]
    return wrap(260, 166, "".join(s), "trapezio con basi e altezza", lg=True)


def u2(v):
    return "%s%scm²" % (num(v), NB)


def s1_perimetro():
    k = R.choice(["rett", "quad", "reg", "tri"])
    if k == "rett":
        a, b = R.randint(5, 30), R.randint(3, 20)
        if a == b:
            return None
        return mcq(fig("rett", a, b) + "Qual è il perimetro del rettangolo?", cm(2 * (a + b)), [cm(a + b), u2(a * b), cm(2 * a + b)],
                   "P = (base + altezza) %s 2 = (%d + %d) %s 2 = <b>%s</b>." % (FOIS, a, b, FOIS, cm(2 * (a + b))))
    if k == "quad":
        a = R.randint(4, 30)
        return mcq(fig("quad", a) + "Qual è il perimetro del quadrato?", cm(4 * a), [cm(2 * a), u2(a * a) if a != 4 else cm(3 * a), cm(a)], "P = lato %s 4 = <b>%s</b>." % (FOIS, cm(4 * a)))
    if k == "reg":
        n, nome = R.choice([(5, "un pentagono"), (6, "un esagono"), (8, "un ottagono"), (3, "un triangolo equilatero")])
        a = R.randint(3, 25)
        return mcq("Qual è il perimetro di %s regolare con il lato di %s?" % (nome, cm(a)) if n != 3 else "Qual è il perimetro di un triangolo equilatero con il lato di %s?" % cm(a), cm(n * a),
                   [cm((n - 1) * a), cm(4 * a) if n != 4 else cm(5 * a), cm(n + a)], "Ha %d lati uguali: %d %s %d = <b>%s</b>." % (n, a, FOIS, n, cm(n * a)))
    a, b, c = R.randint(5, 20), R.randint(5, 20), R.randint(5, 20)
    if a + b <= c or a + c <= b or b + c <= a:
        return None
    return mcq("Un triangolo ha i lati di %s, %s e %s. Qual è il perimetro?" % (cm(a), cm(b), cm(c)), cm(a + b + c), [cm(a + b), cm(a * b // 2) if a * b % 2 == 0 else cm(a + b + c + 1), cm(3 * max(a, b, c))],
               "%d + %d + %d = <b>%s</b>." % (a, b, c, cm(a + b + c)))


def s2_area():
    k = R.choice(["rett", "quad", "para"])
    if k == "rett":
        a, b = R.randint(4, 25), R.randint(3, 15)
        if a == b:
            return None
        return mcq(fig("rett", a, b) + "Qual è l’area del rettangolo?", u2(a * b), [cm(a * b), u2(2 * (a + b)), u2(a + b)], "A = base %s altezza = %d %s %d = <b>%s</b>." % (FOIS, a, FOIS, b, u2(a * b)))
    if k == "quad":
        a = R.randint(3, 20)
        return mcq(fig("quad", a) + "Qual è l’area del quadrato?", u2(a * a), [u2(4 * a) if a != 4 else u2(2 * a), u2(2 * a), cm(a * a)], "A = lato %s lato = %d %s %d = <b>%s</b>." % (FOIS, a, FOIS, a, u2(a * a)))
    a, h = R.randint(6, 25), R.randint(4, 15)
    c = h + R.randint(1, 6)
    return mcq(fig("para", a, h, c) + "Qual è l’area del parallelogramma?", u2(a * h), [u2(a * c), u2(a * h // 2) if a * h % 2 == 0 else u2(a + h), u2(2 * (a + c))],
               "A = base %s altezza = %d %s %d = <b>%s</b> (il lato obliquo %d cm non serve)." % (FOIS, a, FOIS, h, u2(a * h), c))


def s3_area():
    k = R.choice(["tri", "tri", "rombo", "trap"])
    if k == "tri":
        a, h = R.randint(4, 24), R.randint(3, 18)
        if a * h % 2:
            a += 1
        return mcq(fig("tri", a, h) + "Qual è l’area del triangolo?", u2(a * h // 2), [u2(a * h), u2(a + h), u2(a * h // 4) if a * h % 4 == 0 else u2(a * h // 2 + 1)],
                   "A = base %s altezza %s 2 = %d %s %d %s 2 = <b>%s</b>." % (FOIS, DIV, a, FOIS, h, DIV, u2(a * h // 2)))
    if k == "rombo":
        D_, d = R.randint(6, 24), R.randint(4, 16)
        if D_ * d % 2 or D_ <= d:
            return None
        return mcq(fig("rombo", D_, d) + "Qual è l’area del rombo?", u2(D_ * d // 2), [u2(D_ * d), u2(D_ + d), u2(2 * (D_ + d))],
                   "A = diagonale maggiore %s diagonale minore %s 2 = %d %s %d %s 2 = <b>%s</b>." % (FOIS, DIV, D_, FOIS, d, DIV, u2(D_ * d // 2)))
    B, b, h = R.randint(10, 26), R.randint(4, 9), R.randint(4, 14)
    if (B + b) * h % 2:
        return None
    return mcq(fig("trap", B, b, h) + "Qual è l’area del trapezio?", u2((B + b) * h // 2), [u2((B + b) * h), u2(B * h // 2 + b) if B * h % 2 == 0 else u2(B * b), u2(B * b * h // 2) if B * b * h % 2 == 0 else u2(B + b + h)],
               "A = (base maggiore + base minore) %s altezza %s 2 = (%d + %d) %s %d %s 2 = <b>%s</b>." % (FOIS, DIV, B, b, FOIS, h, DIV, u2((B + b) * h // 2)))


def s4_inverse():
    k = R.choice(["latoP", "baseA", "hA", "latoA", "altro"])
    if k == "latoP":
        a = R.randint(3, 30)
        return mcq("Un quadrato ha il perimetro di %s. Quanto misura il lato?" % cm(4 * a), cm(a), [cm(2 * a), cm(4 * a * 4) if a < 10 else cm(a + 4), cm(a * a)], "lato = P %s 4 = %d %s 4 = <b>%s</b>." % (DIV, 4 * a, DIV, cm(a)))
    if k == "baseA":
        b, h = R.randint(4, 25), R.randint(3, 15)
        return mcq("Un rettangolo ha l’area di %s e l’altezza di %s. Quanto misura la base?" % (u2(b * h), cm(h)), cm(b), [cm(b * h * h) if b * h * h < 3000 else cm(b + h), cm(b * h - h), cm(b * h // 2)],
                   "base = A %s altezza = %d %s %d = <b>%s</b>." % (DIV, b * h, DIV, h, cm(b)))
    if k == "hA":
        b, h = R.randint(4, 20), R.randint(3, 16)
        if b * h % 2:
            b += 1
        A = b * h // 2
        return mcq("Un triangolo ha l’area di %s e la base di %s. Quanto misura l’altezza?" % (u2(A), cm(b)), cm(h), [cm(A // b) if A // b != h else cm(h + 2), cm(A * 2), cm(h * 2)],
                   "altezza = A %s 2 %s base = %d %s 2 %s %d = <b>%s</b>." % (FOIS, DIV, A, FOIS, DIV, b, cm(h)))
    if k == "latoA":
        a = R.randint(3, 15)
        return mcq("Un quadrato ha l’area di %s. Quanto misura il lato?" % u2(a * a), cm(a), [cm(a * a // 4) if a * a % 4 == 0 else cm(a + 1), cm(a * a // 2) if a * a % 2 == 0 else cm(a - 1), cm(a * 4)],
                   "Cerca il numero che moltiplicato per se stesso dà %d: %d %s %d = %d. <b>%s</b>." % (a * a, a, FOIS, a, a * a, cm(a)))
    a = R.randint(4, 20)
    b = 2 * a + R.randint(-3, 3) if R.random() < 0.5 else a + R.randint(2, 8)
    p = 2 * (a + b)
    return mcq("Un rettangolo ha il perimetro di %s e la base di %s. Quanto misura l’altezza?" % (cm(p), cm(b)), cm(a), [cm(p - b), cm(p // 2), cm(p - 2 * b)],
               "Semiperimetro: %d %s 2 = %d; altezza = %d − %d = <b>%s</b>." % (p, DIV, p // 2, p // 2, b, cm(a)))


def s5():
    p = K.next()
    k = R.choice(["piastrelle", "recinto", "prato", "composta", "vernice", "aiuola"])
    if k == "piastrelle":
        a, b = R.randint(3, 8), R.randint(2, 6)
        t = R.choice([20, 25, 50])
        n = (a * 100 // t) * (b * 100 // t)
        return mcq("Il pavimento di una stanza misura %d m %s %d m. Quante piastrelle quadrate di %d cm di lato servono?" % (a, FOIS, b, t), num(n), [num(a * b), num(a * b * 100 // t), num(2 * (a + b) * 100 // t)],
                   "Lungo un lato: %d %s %d = %d piastrelle; lungo l’altro: %d %s %d = %d; %d %s %d = <b>%s</b>." % (a * 100, DIV, t, a * 100 // t, b * 100, DIV, t, b * 100 // t, a * 100 // t, FOIS, b * 100 // t, num(n)))
    if k == "recinto":
        a, b, pr = R.randint(10, 40), R.randint(6, 25), R.randint(3, 9)
        return mcq("Un orto rettangolare misura %d m per %d m. La rete costa %d € al metro. Quanto si spende per recintarlo?" % (a, b, pr), "%s €" % num(2 * (a + b) * pr),
                   ["%s €" % num(a * b * pr), "%s €" % num((a + b) * pr), "%s €" % num(2 * (a + b))], "P = (%d + %d) %s 2 = %d m; %d %s %d = <b>%s €</b>." % (a, b, FOIS, 2 * (a + b), 2 * (a + b), FOIS, pr, num(2 * (a + b) * pr)))
    if k == "prato":
        a = R.randint(6, 20)
        g = R.choice([20, 25, 30, 40])
        return mcq("Un prato quadrato ha il lato di %d m. Per ogni m² servono %d g di semi. Quanti grammi di semi servono?" % (a, g), "%s g" % num(a * a * g), ["%s g" % num(4 * a * g), "%s g" % num(a * g), "%s g" % num(a * a + g)],
                   "A = %d %s %d = %d m²; %d %s %d = <b>%s g</b>." % (a, FOIS, a, a * a, a * a, FOIS, g, num(a * a * g)))
    if k == "composta":
        a, b, c, d = R.randint(8, 16), R.randint(6, 12), R.randint(2, 6), R.randint(2, 5)
        if c >= a or d >= b:
            return None
        return mcq("Una figura a forma di L si ottiene togliendo da un rettangolo di %d cm %s %d cm un rettangolo di %d cm %s %d cm in un angolo. Qual è l’area della figura?" % (a, FOIS, b, c, FOIS, d), u2(a * b - c * d),
                   [u2(a * b + c * d), u2(a * b), u2(a * b - c - d)], "%d %s %d − %d %s %d = %d − %d = <b>%s</b>." % (a, FOIS, b, c, FOIS, d, a * b, c * d, u2(a * b - c * d)))
    if k == "vernice":
        a, h = R.choice([(4, 3), (6, 4), (8, 3), (10, 4), (6, 3), (12, 3), (5, 4)])
        A = a * h
        n = A // 4
        return mcq("Una parete rettangolare è lunga %d m e alta %d m. Con 1 litro di vernice si dipingono 4 m². Quanti litri servono?" % (a, h), num(n),
                   [num(A), num(2 * (a + h) // 4) if (2 * (a + h)) % 4 == 0 and 2 * (a + h) // 4 != n else num(A // 2), num(n + 1)],
                   "A = %d %s %d = %d m²; %d %s 4 = <b>%s</b> litri." % (a, FOIS, h, A, A, DIV, num(n)))
    b, h = R.randint(4, 12), R.randint(2, 8)
    return mcq("%s disegna un’aiuola a forma di triangolo con base %d m e altezza %d m. Qual è l’area?" % (p[0], b * 2, h), "%d m²" % (b * h), ["%d m²" % (b * 2 * h), "%d m" % (b * h), "%d m²" % (b * 2 + h)],
               "A = %d %s %d %s 2 = <b>%d m²</b>." % (b * 2, FOIS, h, DIV, b * h))


def main():
    seen = set()
    sets = [
        ("Il perimetro", mix(R, seen, [(s1_perimetro, 20)])),
        ("Area di rettangolo, quadrato e parallelogramma", mix(R, seen, [(s2_area, 20)])),
        ("Area di triangolo, rombo e trapezio", mix(R, seen, [(s3_area, 20)])),
        ("Formule inverse", mix(R, seen, [(s4_inverse, 20)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Il <b>perimetro</b> è la lunghezza del contorno (cm, m). L’<b>area</b> è la misura della superficie (cm², m²).",
         "Rettangolo e parallelogramma: A = base %s altezza. Quadrato: A = lato %s lato." % (FOIS, FOIS),
         "Triangolo: A = base %s altezza %s 2. Rombo: A = D %s d %s 2. Trapezio: A = (B + b) %s h %s 2." % (FOIS, DIV, FOIS, DIV, FOIS, DIV),
         "L’<b>altezza</b> è perpendicolare alla base (linea tratteggiata), non è il lato obliquo. Per le formule inverse fai l’operazione contraria."],
        [("Triangolo: base 12 cm, altezza 7 cm", ["12 %s 7 = 84" % FOIS, "84 %s 2 = 42" % DIV], "42 cm²")],
        [["Confondere perimetro e area", "Perimetro = contorno (cm); area = superficie (cm²)."],
         ["Triangolo senza %s 2" % DIV, "Un triangolo è metà di un parallelogramma: dividi per 2."],
         ["Usare il lato obliquo come altezza", "L’altezza forma un angolo retto con la base."]],
        table(["Figura", "Area"], [["rettangolo", "b %s h" % FOIS], ["quadrato", "l %s l" % FOIS], ["parallelogramma", "b %s h" % FOIS], ["triangolo", "b %s h %s 2" % (FOIS, DIV)],
                                   ["rombo", "D %s d %s 2" % (FOIS, DIV)], ["trapezio", "(B + b) %s h %s 2" % (FOIS, DIV)]]))
    faq = [("Perché l’area del triangolo si divide per 2?", "Perché due triangoli uguali formano un parallelogramma: il triangolo è la sua metà."),
           ("Due figure con la stessa area hanno lo stesso perimetro?", "No: un rettangolo 6 × 1 e uno 3 × 2 hanno area 6, ma perimetro 14 e 10.")]
    make_unit(R, "perimetro-e-area-dei-poligoni", "S",
              "Determinare il perimetro di una figura utilizzando le più comuni formule o altri procedimenti; determinare l’area di rettangoli e triangoli e di altre figure per scomposizione o utilizzando le più comuni formule",
              "Perimetro e area dei poligoni: formule e problemi", "Perimetro e area dei poligoni",
              "Schede di matematica per la classe quinta su perimetro e area dei poligoni: rettangolo, quadrato, parallelogramma, triangolo, rombo, trapezio, formule inverse, figure composte e problemi. 100 esercizi con soluzioni.",
              "Perimetro: contorno in cm. Area: superficie in cm².", "Triangolo: base × altezza : 2.",
              body, faq, sets, 17, grade=G)


if __name__ == "__main__":
    main()
