# -*- coding: utf-8 -*-
"""
Italia Matematica quarta liceo: Trigonometria — risoluzione dei triangoli (Geometria)
  python3 tools/gen_it_matematica_l4_trigonometria.py
Teoremi sui triangoli rettangoli (cateto = ipotenusa · sen dell’angolo opposto = altro cateto · tg), area di un triangolo
(½ab sen γ), teorema della corda, teorema dei seni, teorema del coseno (di Carnot), problemi con altezze e distanze.
Errori: usare il coseno dell’angolo opposto, Carnot con + 2ab cos γ, area con il coseno.
"""
import math
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, d, FR, figure, simp_root

R = random.Random(72407)
G = "quarta-liceo"


def rt(n):
    n = int(n)
    k, m = simp_root(n)
    return str(k) if m == 1 else ("" if k == 1 else str(k)) + "√" + str(m)


def kr(k, r):
    """k·√r testo"""
    if r == 1:
        return fq(k)
    kk = Fr(k)
    if kk.denominator == 1:
        return ("" if kk == 1 else fq(kk)) + "√%d" % r
    return FR(("" if kk.numerator == 1 else str(kk.numerator)) + "√%d" % r, str(kk.denominator))


SPEC = {30: (Fr(1, 2), 1, Fr(1, 2), 3), 45: (Fr(1, 2), 2, Fr(1, 2), 2), 60: (Fr(1, 2), 3, Fr(1, 2), 1)}
# sen = SPEC[0]·√SPEC[1], cos = SPEC[2]·√SPEC[3]
SEN = {30: (Fr(1, 2), 1), 45: (Fr(1, 2), 2), 60: (Fr(1, 2), 3)}
COS = {30: (Fr(1, 2), 3), 45: (Fr(1, 2), 2), 60: (Fr(1, 2), 1)}
TG = {30: (Fr(1, 3), 3), 45: (Fr(1), 1), 60: (Fr(1), 3)}


def rfig(ang):
    return figure({"A": (0, 0), "B": (4, 0), "C": (4, 4 * math.tan(math.radians(ang)) if ang < 70 else 4)}, [("A", "B"), ("B", "C"), ("C", "A")], right=[("B", "A", "C")],
                  W=260, H=190, label="triangolo rettangolo in B")


def s1_rett():
    ang = R.choice([30, 45, 60])
    i = R.choice([2, 4, 6, 8, 10, 12, 20])
    k = R.choice(["opp", "adi"])
    if k == "opp":
        c, r = SEN[ang]
        v = kr(c * i, r)
        w = [kr(COS[ang][0] * i, COS[ang][1]), kr(TG[ang][0] * i, TG[ang][1]), fq(i * 2), kr(c * i * 2, r)]
        e = "Cateto opposto = ipotenusa · sen α = %d · sen %d° = <b>%s</b>." % (i, ang, v)
        q = "In un triangolo rettangolo l’ipotenusa misura %d e un angolo acuto α = %d°. Quanto misura il cateto opposto ad α?" % (i, ang)
    else:
        c, r = COS[ang]
        v = kr(c * i, r)
        w = [kr(SEN[ang][0] * i, SEN[ang][1]), kr(TG[ang][0] * i, TG[ang][1]), fq(Fr(i, 2)) if v != fq(Fr(i, 2)) else fq(i), kr(c * i * 2, r)]
        e = "Cateto adiacente = ipotenusa · cos α = %d · cos %d° = <b>%s</b>." % (i, ang, v)
        q = "In un triangolo rettangolo l’ipotenusa misura %d e un angolo acuto α = %d°. Quanto misura il cateto adiacente ad α?" % (i, ang)
    return M(q, v, [x for x in W(*w) if x != v], e)


def s1_tg():
    ang = R.choice([30, 45, 60])
    a = R.choice([3, 6, 9, 12, 2, 4])
    c, r = TG[ang]
    v = kr(c * a, r)
    w = [kr(Fr(a, 1) / c / (r if r == 3 else 1), r) if r == 3 else fq(a + 1), kr(SEN[ang][0] * a, SEN[ang][1]), kr(COS[ang][0] * a, COS[ang][1]), kr(a, 2), fq(2 * a)]
    return M("In un triangolo rettangolo un cateto misura %d e l’angolo acuto adiacente a esso misura %d°. Quanto misura l’altro cateto?" % (a, ang), v, [x for x in W(*w) if x != v],
             "Altro cateto = cateto · tg α = %d · tg %d° = <b>%s</b>." % (a, ang, v))


def s2_area():
    a, b = R.randint(3, 12), R.randint(3, 12)
    ang = R.choice([30, 45, 60, 90, 120, 135, 150])
    s_ = {30: (Fr(1, 2), 1), 45: (Fr(1, 2), 2), 60: (Fr(1, 2), 3), 90: (Fr(1), 1), 120: (Fr(1, 2), 3), 135: (Fr(1, 2), 2), 150: (Fr(1, 2), 1)}[ang]
    v = kr(Fr(a * b, 2) * s_[0], s_[1])
    c_ = {30: (Fr(1, 2), 3), 45: (Fr(1, 2), 2), 60: (Fr(1, 2), 1), 90: (Fr(0), 1), 120: (Fr(1, 2), 1), 135: (Fr(1, 2), 2), 150: (Fr(1, 2), 3)}[ang]
    w = [kr(a * b * s_[0], s_[1]), kr(Fr(a * b, 2) * c_[0], c_[1]) if c_[0] else "0", fq(Fr(a * b, 2)) if s_ != (Fr(1), 1) else fq(a * b), fq(a * b), fq(Fr(a * b, 4)), fq(a + b)]
    return M("Due lati di un triangolo misurano %d cm e %d cm e formano un angolo di %d°. Quanto vale l’area (in cm²)?" % (a, b, ang), v, [x for x in W(*w) if x != v],
             "Area = ½ · a · b · sen γ = ½ · %d · %d · sen %d° = <b>%s</b>." % (a, b, ang, v))


def s3_seni():
    k = R.choice(["lato", "R"])
    A, B = R.choice([(30, 45), (45, 30), (30, 60), (60, 30), (45, 60), (60, 45), (30, 90), (90, 30), (45, 90), (120, 30), (30, 120), (135, 30)])
    sv = {30: (Fr(1, 2), 1), 45: (Fr(1, 2), 2), 60: (Fr(1, 2), 3), 90: (Fr(1), 1), 120: (Fr(1, 2), 3), 135: (Fr(1, 2), 2)}
    if k == "lato":
        a = R.choice([2, 4, 6, 8, 10, 12])
        # b = a · sen B / sen A
        (ca, ra), (cb, rb) = sv[A], sv[B]
        # (cb √rb)/(ca √ra) = (cb/ca) √(rb/ra) = (cb/ca)/ra · √(rb·ra)
        coef = Fr(a) * cb / ca / ra
        rr = rb * ra
        k2, m2 = simp_root(rr)
        coef *= k2
        v = kr(coef, m2)
        coefw = Fr(a) * ca / cb / rb
        k3, m3 = simp_root(ra * rb)
        w = [kr(coefw * k3, m3), fq(a), kr(Fr(a) * cb / ca, rb), fq(2 * a), kr(Fr(a, 2), 3), kr(a, 2)]
        return M("Nel triangolo ABC, a = BC = %d, l’angolo A = %d° e l’angolo B = %d°. Quanto misura b = AC?" % (a, A, B), v, [x for x in W(*w) if x != v],
                 "Teorema dei seni: a / sen A = b / sen B → b = a · sen B / sen A = %d · sen %d° / sen %d° = <b>%s</b>." % (a, B, A, v))
    a = R.choice([2, 3, 4, 6, 8, 10])
    ca, ra = sv[A]
    # 2R = a / sen A → R = a / (2 sen A)
    coef = Fr(a) / (2 * ca) / ra
    k2, m2 = simp_root(ra)
    v = kr(coef * k2, m2) if ra != 1 else fq(Fr(a) / (2 * ca))
    w = [kr(coef * k2 * 2, m2) if ra != 1 else fq(Fr(a) / ca), fq(Fr(a, 2)), fq(a), kr(Fr(a) * ca, ra), fq(2 * a), kr(Fr(a, 2), 3)]
    return M("Nel triangolo ABC il lato a = %d è opposto all’angolo A = %d°. Quanto misura il raggio R della circonferenza circoscritta?" % (a, A), v, [x for x in W(*w) if x != v],
             "Teorema dei seni (della corda): a / sen A = 2R → R = %d / (2 sen %d°) = <b>%s</b>." % (a, A, v))


def s4_carnot():
    a, b = R.randint(2, 9), R.randint(2, 9)
    ang = R.choice([60, 120, 90, 60, 120])
    cosv = {60: Fr(1, 2), 120: Fr(-1, 2), 90: Fr(0)}[ang]
    c2 = a * a + b * b - 2 * a * b * cosv
    v = rt(c2)
    w = [rt(a * a + b * b + 2 * a * b * cosv) if cosv else rt(a * a + b * b + a * b), rt(a * a + b * b), rt(abs(a * a - b * b)) if a != b else str(a + b), str(a + b)]
    return M("In un triangolo due lati misurano %d e %d e l’angolo compreso è di %d°. Quanto misura il terzo lato?" % (a, b, ang), v, [x for x in W(*w) if x != v],
             "Teorema del coseno: c² = a² + b² − 2ab cos γ = %d + %d − 2 · %d · %d · (%s) = %s → <b>c = %s</b>." % (a * a, b * b, a, b, fq(cosv), fq(c2), v))


def s4_ang():
    a, b, c = R.choice([(3, 5, 7), (5, 7, 8), (3, 7, 8), (5, 8, 7), (7, 8, 13), (3, 8, 7), (5, 3, 7), (1, 1, 1), (8, 5, 7)])
    cosg = Fr(a * a + b * b - c * c, 2 * a * b)
    ang = {Fr(1, 2): 60, Fr(-1, 2): 120, Fr(0): 90}.get(cosg)
    if ang is None:
        return None
    return M("Un triangolo ha i lati a = %d, b = %d, c = %d. Quanto misura l’angolo γ opposto a c?" % (a, b, c), "%d°" % ang, ["%d°" % x for x in W(180 - ang, 90 if ang != 90 else 45, 30 if ang != 30 else 150)],
             "cos γ = (a² + b² − c²)/(2ab) = (%d + %d − %d)/%d = %s → <b>γ = %d°</b>." % (a * a, b * b, c * c, 2 * a * b, fq(cosg), ang))


def s5_probl():
    k = R.choice(["torre", "scala", "fiume"])
    ang = R.choice([30, 45, 60])
    dd = R.choice([10, 20, 30, 40, 50, 60])
    if k == "torre":
        c, r = TG[ang]
        v = kr(c * dd, r)
        return M("Da un punto a %d m dalla base di una torre si vede la cima con un angolo di elevazione di %d°. Quanto è alta la torre (in m)?" % (dd, ang), v, [x for x in W(kr(SEN[ang][0] * dd, SEN[ang][1]), kr(COS[ang][0] * dd, COS[ang][1]), kr(Fr(dd) / c / (r if r == 3 else 1), r) if r == 3 else fq(dd * 2), fq(dd), kr(dd, 3), kr(dd, 2)) if x != v],
                     "h = distanza · tg %d° = %d · tg %d° = <b>%s m</b>." % (ang, dd, ang, v))
    if k == "scala":
        L_ = R.choice([4, 6, 8, 10])
        c, r = SEN[ang]
        v = kr(c * L_, r)
        return M("Una scala lunga %d m è appoggiata a un muro e forma con il pavimento un angolo di %d°. A che altezza arriva sul muro (in m)?" % (L_, ang), v, [x for x in W(kr(COS[ang][0] * L_, COS[ang][1]), kr(TG[ang][0] * L_, TG[ang][1]), fq(L_), fq(Fr(L_, 2)), kr(L_, 2))  if x != v],
                     "L’altezza è il cateto opposto all’angolo: %d · sen %d° = <b>%s m</b>." % (L_, ang, v))
    c, r = TG[ang]
    v = kr(c * dd, r)
    return M("Per misurare la larghezza di un fiume, da un punto A si cammina lungo la riva per %d m fino a B; da B si vede l’albero C, sulla riva opposta di fronte ad A, con l’angolo ABC = %d°. Quanto è largo il fiume (in m)?" % (dd, ang), v,
             [x for x in W(kr(SEN[ang][0] * dd, SEN[ang][1]), kr(COS[ang][0] * dd, COS[ang][1]), fq(dd), kr(dd, 3), kr(Fr(dd, 3), 3)) if x != v], "Il triangolo è rettangolo in A: AC = AB · tg %d° = <b>%s m</b>." % (ang, v))


def main():
    seen = set()
    sets = [
        ("Triangoli rettangoli", mix(R, seen, [(s1_rett, 12), (s1_tg, 8)])),
        ("Area e teorema della corda", mix(R, seen, [(s2_area, 14), (s3_seni, 6)])),
        ("Teorema dei seni", mix(R, seen, [(s3_seni, 20)])),
        ("Teorema del coseno", mix(R, seen, [(s4_carnot, 14), (s4_ang, 6)])),
        ("Problemi di trigonometria", mix(R, seen, [(s5_probl, 14), (s1_rett, 6)])),
    ]
    body = L(["Nel triangolo rettangolo: un cateto è uguale all’ipotenusa per il <b>seno dell’angolo opposto</b> (o per il coseno dell’angolo adiacente); un cateto è uguale all’altro cateto per la <b>tangente dell’angolo opposto</b> al primo.",
              "L’area di un triangolo è ½ · a · b · sen γ, con γ angolo compreso tra i lati a e b.",
              "<b>Teorema dei seni</b>: a / sen A = b / sen B = c / sen C = 2R (R raggio della circonferenza circoscritta).",
              "<b>Teorema del coseno</b> (Carnot): c² = a² + b² − 2ab cos γ. Generalizza Pitagora e serve con due lati e l’angolo compreso, o con tre lati."],
             [("Ipotenusa 10, α = 30°: cateto opposto", ["10 · sen 30° = 10 · ½"], "5"),
              ("a = 5, b = 8, γ = 60°", ["c² = 25 + 64 − 2 · 5 · 8 · ½ = 49"], "c = 7")],
             [["Cateto opposto = ipotenusa · cos α", "Con l’angolo opposto si usa il seno."],
              ["c² = a² + b² + 2ab cos γ", "Il segno è meno; con γ ottuso cos γ &lt; 0 e il lato viene più lungo."],
              ["Area = ½ ab cos γ", "Nell’area c’è il seno dell’angolo compreso."]])
    faq = [("Quando si usa il teorema dei seni e quando quello del coseno?", "Il teorema dei seni quando si conoscono un lato e l’angolo opposto (più un altro elemento). Il teorema del coseno quando si conoscono due lati e l’angolo compreso, oppure i tre lati."),
           ("Il teorema del coseno contiene il teorema di Pitagora?", "Sì: se γ = 90°, cos γ = 0 e resta c² = a² + b².")]
    unit(G, R, "trigonometria", "G",
         "Teoremi dei seni e del coseno; risoluzione dei triangoli; applicazioni a problemi di misura",
         "Trigonometria e risoluzione dei triangoli", "Trigonometria",
         "Schede di matematica per la quarta liceo sulla trigonometria: triangoli rettangoli, area con il seno, teorema dei seni e della corda, teorema del coseno (Carnot), problemi con altezze e distanze. 100 esercizi con soluzioni.",
         "c² = a² + b² − 2ab cos γ", "a / sen A = b / sen B = 2R; area = ½ ab sen γ.",
         body, faq, sets, 7)


if __name__ == "__main__":
    main()
