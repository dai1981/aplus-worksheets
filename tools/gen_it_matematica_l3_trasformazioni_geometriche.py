# -*- coding: utf-8 -*-
"""
Italia Matematica terza liceo: Trasformazioni geometriche nel piano cartesiano (Geometria)
  python3 tools/gen_it_matematica_l3_trasformazioni_geometriche.py
Equazioni delle trasformazioni: traslazione di vettore v(a; b), simmetrie rispetto agli assi, all’origine, alla bisettrice y = x,
a una retta x = k o y = k, simmetria centrale, rotazione di 90° e 180° intorno all’origine, omotetia di centro O; immagine di
punti, di rette e di parabole; composizione; effetto sulle aree.
Errori: traslare la curva con x + a invece di x − a, simmetria rispetto a y = x senza scambiare le coordinate, area dell’omotetia con k.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, P2, P, show

R = random.Random(72309)
G = "terza-liceo"


def pt(x, y, n=""):
    return "%s(%s; %s)" % (n, fq(x), fq(y))


TR = [("la simmetria rispetto all’asse x", lambda x, y: (x, -y)),
      ("la simmetria rispetto all’asse y", lambda x, y: (-x, y)),
      ("la simmetria rispetto all’origine", lambda x, y: (-x, -y)),
      ("la simmetria rispetto alla bisettrice y = x", lambda x, y: (y, x)),
      ("la rotazione di 90° in senso antiorario intorno all’origine", lambda x, y: (-y, x)),
      ("la rotazione di 90° in senso orario intorno all’origine", lambda x, y: (y, -x))]


def s1_punto():
    x, y = nz(R, -6, 6), nz(R, -6, 6)
    if abs(x) == abs(y):
        return None
    nm, f = R.choice(TR)
    a = f(x, y)
    others = [g(x, y) for _, g in TR if g(x, y) != a]
    return M("Qual è l’immagine di %s nel%s?" % (pt(x, y, "P"), nm), pt(*a, "P′"), [pt(*o, "P′") for o in others[:3]],
             "Applico %s: <b>%s</b>." % (nm, pt(*a, "P′")))


def s1_trasl():
    x, y = R.randint(-6, 6), R.randint(-6, 6)
    a, b = nz(R, -5, 5), nz(R, -5, 5)
    t = R.choice(["img", "vett"])
    if t == "img":
        return M("Trasla il punto %s secondo il vettore v(%s; %s)." % (pt(x, y, "P"), fq(a), fq(b)), pt(x + a, y + b, "P′"), [pt(x - a, y - b, "P′"), pt(x + b, y + a, "P′") if a != b else pt(x + a, y - b, "P′"), pt(a, b, "P′") if (a, b) != (x + a, y + b) else pt(x, y + b, "P′"), pt(x + a, y, "P′")],
                 "x′ = x + a, y′ = y + b: <b>%s</b>." % pt(x + a, y + b, "P′"))
    return M("La traslazione porta %s in %s. Qual è il vettore di traslazione?" % (pt(x, y, "A"), pt(x + a, y + b, "A′")), "v(%s; %s)" % (fq(a), fq(b)), W("v(%s; %s)" % (fq(-a), fq(-b)), "v(%s; %s)" % (fq(x + a), fq(y + b)) if (x, y) != (0, 0) else "v(%s; %s)" % (fq(b), fq(a)), "v(%s; %s)" % (fq(b), fq(a)) if a != b else "v(%s; %s)" % (fq(a), fq(-b)), "v(%s; %s)" % (fq(a), fq(-b)), "v(%s; %s)" % (fq(-a), fq(b))),
             "v = A′ − A = (%s − %s; %s − %s) = <b>v(%s; %s)</b>." % (fq(x + a), "(%s)" % fq(x) if x < 0 else fq(x), fq(y + b), "(%s)" % fq(y) if y < 0 else fq(y), fq(a), fq(b)))


def s2_centr():
    x, y = R.randint(-6, 6), R.randint(-6, 6)
    cx, cy = R.randint(-3, 3), R.randint(-3, 3)
    if (cx, cy) == (0, 0) or x == cx or y == cy:
        return None
    t = R.choice(["C", "rx", "ry"])
    if t == "C":
        a = (2 * cx - x, 2 * cy - y)
        return M("Qual è il simmetrico di %s rispetto al punto %s?" % (pt(x, y, "P"), pt(cx, cy, "C")), pt(*a, "P′"), [pt(-x, -y, "P′") if (-x, -y) != a else pt(x, -y, "P′"), pt(cx - x, cy - y, "P′"), pt(Fr(x + cx, 2), Fr(y + cy, 2), "P′")],
                     "C è il punto medio di PP′: x′ = 2 · %s − %s, y′ = 2 · %s − %s: <b>%s</b>." % (fq(cx), "(%s)" % fq(x) if x < 0 else fq(x), fq(cy), "(%s)" % fq(y) if y < 0 else fq(y), pt(*a, "P′")))
    if t == "rx":
        a = (2 * cx - x, y)
        return M("Qual è il simmetrico di %s rispetto alla retta x = %s?" % (pt(x, y, "P"), fq(cx)), pt(*a, "P′"), [pt(x, 2 * cx - y, "P′") if (x, 2 * cx - y) != a else pt(-x, y, "P′"), pt(-x, y, "P′") if -x != a[0] else pt(x + cx, y, "P′"), pt(cx - x, y, "P′") if cx - x != a[0] else pt(a[0], -y, "P′")],
                     "La y resta uguale; x′ = 2 · %s − %s = %s: <b>%s</b>." % (fq(cx), "(%s)" % fq(x) if x < 0 else fq(x), fq(a[0]), pt(*a, "P′")))
    a = (x, 2 * cy - y)
    return M("Qual è il simmetrico di %s rispetto alla retta y = %s?" % (pt(x, y, "P"), fq(cy)), pt(*a, "P′"), [pt(2 * cy - x, y, "P′") if (2 * cy - x, y) != a else pt(x, -y, "P′"), pt(x, -y, "P′") if -y != a[1] else pt(x, y + cy, "P′"), pt(x, cy - y, "P′") if cy - y != a[1] else pt(-x, a[1], "P′")],
             "La x resta uguale; y′ = 2 · %s − %s = %s: <b>%s</b>." % (fq(cy), "(%s)" % fq(y) if y < 0 else fq(y), fq(a[1]), pt(*a, "P′")))


def s3_retta():
    m, q = nz(R, -3, 3), R.randint(-5, 5)
    t = R.choice(["trasl", "sx", "sy", "so"])
    if t == "trasl":
        a, b = nz(R, -4, 4), nz(R, -4, 4)
        q2 = q - m * a + b
        ans = "y = %s" % P2(0, m, q2)
        w = ["y = %s" % P2(0, m, q + m * a + b), "y = %s" % P2(0, m, q + a + b), "y = %s" % P2(0, m, q - m * a - b)]
        q_ = "Trova l’immagine della retta y = %s nella traslazione di vettore v(%s; %s)." % (P2(0, m, q), fq(a), fq(b))
        e = "Sostituisco x → x − %s e y → y − %s: y − %s = %s → <b>%s</b>." % (fq(a), fq(b), fq(b) if b > 0 else "(%s)" % fq(b), show(P([(m, {"x": 1}), (-m * a + q, {})])).replace("x", "x", 1) if False else "%s(x %s %s) %s %s" % (fq(m) if abs(m) != 1 else ("" if m == 1 else "−"), "−" if a > 0 else "+", fq(abs(a)), "+" if q >= 0 else "−", fq(abs(q))), ans)
    else:
        if t == "sx":
            ans, nm = "y = %s" % P2(0, -m, -q), "all’asse x"
        elif t == "sy":
            ans, nm = "y = %s" % P2(0, -m, q), "all’asse y"
        else:
            ans, nm = "y = %s" % P2(0, m, -q), "all’origine"
        all_ = ["y = %s" % P2(0, -m, -q), "y = %s" % P2(0, -m, q), "y = %s" % P2(0, m, -q), "y = %s" % P2(0, m, q)]
        w = [x for x in all_ if x != ans]
        q_ = "Trova la simmetrica della retta y = %s rispetto %s." % (P2(0, m, q), nm)
        e = "%s: <b>%s</b>." % ({"sx": "Simmetria rispetto all’asse x: y → −y", "sy": "Simmetria rispetto all’asse y: x → −x", "so": "Simmetria rispetto all’origine: x → −x e y → −y"}[t], ans)
    return M(q_, ans, [x for x in w if x != ans], e)


def s4_parab():
    a, b, c = R.choice([1, -1, 2]), R.randint(-4, 4), R.randint(-4, 4)
    h, k = nz(R, -3, 3), nz(R, -3, 3)
    # y − k = a(x − h)² + b(x − h) + c
    A, B, C = a, -2 * a * h + b, a * h * h - b * h + c + k
    ans = "y = %s" % P2(A, B, C)
    Bw, Cw = 2 * a * h + b, a * h * h + b * h + c + k
    w = ["y = %s" % P2(A, Bw, Cw), "y = %s" % P2(A, B, C - 2 * k), "y = %s" % P2(a, b, c + k + h)]
    return M("Trova l’immagine della parabola y = %s nella traslazione di vettore v(%s; %s)." % (P2(a, b, c), fq(h), fq(k)), ans, [x for x in w if x != ans],
             "Sostituisco x con x − %s e y con y − %s, poi sviluppo: <b>%s</b>." % ("(%s)" % fq(h) if h < 0 else fq(h), "(%s)" % fq(k) if k < 0 else fq(k), ans))


def s5_omot():
    k = R.choice([2, 3, -2, Fr(1, 2), -1, Fr(3, 2)])
    t = R.choice(["pt", "area", "lung"])
    if t == "pt":
        x, y = nz(R, -6, 6), nz(R, -6, 6)
        a = (k * x, k * y)
        return M("Qual è l’immagine di %s nell’omotetia di centro O e rapporto k = %s?" % (pt(x, y, "P"), fq(k)), pt(*a, "P′"), [pt(x + k, y + k, "P′"), pt(Fr(x) / k, Fr(y) / k, "P′") if k not in (1, -1) else pt(-x, y, "P′"), pt(-k * x, -k * y, "P′")],
                     "x′ = kx, y′ = ky: <b>%s</b>." % pt(*a, "P′"))
    if t == "area":
        A = R.choice([6, 8, 10, 12, 18, 20])
        v = A * k * k
        return M("Un triangolo ha area %d. Quanto misura l’area della sua immagine nell’omotetia di rapporto k = %s?" % (A, fq(k)), fq(v), [fq(x) for x in W(A * abs(k), A * k, A + k, A * abs(k) ** 3)  if x != v],
                 "Nell’omotetia le aree si moltiplicano per k² = %s: <b>%s</b>." % (fq(k * k), fq(v)))
    L_ = R.choice([4, 6, 8, 10, 12])
    v = L_ * abs(k)
    return M("Un segmento misura %d. Quanto misura la sua immagine nell’omotetia di rapporto k = %s?" % (L_, fq(k)), fq(v), [fq(x) for x in W(L_ * k * k, L_ * k if k < 0 else L_ + k, L_) if x != v],
             "Le lunghezze si moltiplicano per |k| = %s: <b>%s</b>." % (fq(abs(k)), fq(v)))


def s5_comp():
    x, y = nz(R, -5, 5), nz(R, -5, 5)
    if abs(x) == abs(y):
        return None
    (n1, f1), (n2, f2) = R.sample(TR[:4], 2)
    a = f2(*f1(x, y))
    w = [f1(*f2(x, y)), f1(x, y), f2(x, y), (-a[0], a[1])]
    w = [pt(*v, "P″") for v in w if v != a]
    return M("Al punto %s si applica prima %s e poi %s. Dove arriva?" % (pt(x, y, "P"), n1, n2), pt(*a, "P″"), list(dict.fromkeys(w))[:3] if len(set(w)) >= 3 else list(dict.fromkeys(w)) + [pt(a[1], a[0], "P″")],
             "Prima %s → %s, poi %s → <b>%s</b>." % (n1, pt(*f1(x, y), "P′"), n2, pt(*a, "P″")))


def main():
    seen = set()
    sets = [
        ("Simmetrie e rotazioni di punti", mix(R, seen, [(s1_punto, 20)])),
        ("Traslazioni", mix(R, seen, [(s1_trasl, 14), (s2_centr, 6)])),
        ("Simmetrie centrali e assiali", mix(R, seen, [(s2_centr, 14), (s5_comp, 6)])),
        ("Immagini di rette e parabole", mix(R, seen, [(s3_retta, 12), (s4_parab, 8)])),
        ("Omotetie e composizioni", mix(R, seen, [(s5_omot, 14), (s5_comp, 6)])),
    ]
    body = L(["Una trasformazione geometrica associa a ogni punto P(x; y) un punto P′(x′; y′). Le <b>isometrie</b> (traslazioni, simmetrie, rotazioni) conservano le distanze.",
              "<b>Traslazione</b> di vettore v(a; b): x′ = x + a, y′ = y + b. <b>Simmetria</b> rispetto all’asse x: (x; −y); all’asse y: (−x; y); all’origine: (−x; −y); alla bisettrice y = x: (y; x). <b>Rotazione</b> di 90° antioraria intorno a O: (−y; x).",
              "Per trovare l’immagine di una curva si usano le equazioni inverse: nella traslazione di v(a; b) si sostituisce x con x − a e y con y − b.",
              "<b>Omotetia</b> di centro O e rapporto k: (kx; ky). Le lunghezze si moltiplicano per |k|, le aree per k²."],
             [("Traslazione di y = x² secondo v(2; 1)", ["y − 1 = (x − 2)²"], "y = x² − 4x + 5"),
              ("Simmetrico di P(3; −2) rispetto a C(1; 1)", ["x′ = 2 − 3, y′ = 2 + 2"], "P′(−1; 4)")],
             [["Traslare y = f(x) con f(x + a)", "Per spostare a destra di a si scrive f(x − a)."],
              ["Simmetria rispetto a y = x: (−x; −y)", "Si scambiano le coordinate: (y; x)."],
              ["Area dell’omotetia moltiplicata per k", "Le aree si moltiplicano per k²."]])
    faq = [("Perché per trasformare una curva si usano le equazioni inverse?", "Perché un punto (x; y) sta sulla curva trasformata se il suo punto di partenza, cioè l’inverso, sta sulla curva iniziale."),
           ("L’omotetia è un’isometria?", "No, se |k| ≠ 1: cambia le lunghezze. È una similitudine: conserva la forma e gli angoli.")]
    unit(G, R, "trasformazioni-geometriche", "G",
         "Trasformazioni geometriche nel piano cartesiano: traslazioni, simmetrie, rotazioni, omotetie e loro equazioni",
         "Trasformazioni geometriche", "Trasformazioni geometriche",
         "Schede di matematica per la terza liceo sulle trasformazioni geometriche: traslazioni, simmetrie assiali e centrali, rotazioni, omotetie, immagini di punti, rette e parabole, composizione. 100 esercizi con soluzioni.",
         "Traslazione v(a; b): x → x − a, y → y − b nell’equazione", "Omotetia: lunghezze per |k|, aree per k².",
         body, faq, sets, 9)


if __name__ == "__main__":
    main()
