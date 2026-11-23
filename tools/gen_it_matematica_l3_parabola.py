# -*- coding: utf-8 -*-
"""
Italia Matematica terza liceo: La parabola (Geometria)
  python3 tools/gen_it_matematica_l3_parabola.py
Parabola con asse parallelo all’asse y: y = ax² + bx + c, concavità, asse, vertice, fuoco e direttrice, intersezioni con gli assi,
equazione dato il vertice e un punto, posizione di una retta rispetto alla parabola (Δ del sistema), retta tangente in un punto,
lettura del grafico.
Errori: vertice con x = b/(2a), fuoco con 1 + Δ, concavità decisa da c.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, P2, kurve, relabel

R = random.Random(72305)
G = "terza-liceo"
BLUE, RED = "#1f6fd1", "#dc2626"


def pt(x, y, n=""):
    return "%s(%s; %s)" % (n, fq(x), fq(y))


def par():
    a = R.choice([1, 1, 2, -1, -2, Fr(1, 2), -Fr(1, 2)])
    h = R.randint(-4, 4)
    k = R.randint(-5, 5)
    b, c = -2 * a * h, a * h * h + k
    return Fr(a), Fr(b), Fr(c), h, k


def vf(a, h, k):
    """a(x − h)² + k"""
    xs = "x" if h == 0 else ("x − %s" % fq(h) if h > 0 else "x + %s" % fq(-h))
    t = ("" if a == 1 else "−" if a == -1 else fq(a)) + ("(%s)²" % xs if h else "x²")
    return t + ("" if k == 0 else (" + %s" % fq(k) if k > 0 else " − %s" % fq(-k)))


def eq(a, b, c):
    return "y = %s" % P2(a, b, c)


def s1_vert():
    a, b, c, h, k = par()
    if b.denominator != 1 or c.denominator != 1:
        return None
    t = R.choice(["V", "asse", "conc"])
    if t == "V":
        return M("Trova il vertice della parabola %s." % eq(a, b, c), pt(h, k, "V"), [pt(-h, k, "V") if h else pt(h, -k, "V"), pt(h, c, "V") if c != k else pt(h, k + 1, "V"), pt(Fr(-b, a), k, "V") if Fr(-b, a) != h else pt(h + 1, k, "V")],
                 "x<sub>V</sub> = −b/(2a) = %s; y<sub>V</sub> = f(%s) = %s: <b>%s</b>." % (fq(h), fq(h), fq(k), pt(h, k, "V")))
    if t == "asse":
        return M("Qual è l’asse di simmetria della parabola %s?" % eq(a, b, c), "x = %s" % fq(h), ["x = %s" % fq(v) for v in W(-h if h else 1, Fr(-b, a) if Fr(-b, a) != h else h + 2, k)] + ["y = %s" % fq(h)],
                 "L’asse è la retta verticale per il vertice: x = −b/(2a) = <b>%s</b>." % fq(h))
    ans = "verso l’alto" if a > 0 else "verso il basso"
    return M("La parabola %s ha la concavità rivolta…" % eq(a, b, c), ans, ["verso il basso" if a > 0 else "verso l’alto", "verso destra", "dipende dal segno di c"],
             "Conta il segno di a = %s: <b>%s</b>." % (fq(a), ans))


def s2_fuoco():
    a = R.choice([Fr(1, 4), Fr(-1, 4), Fr(1, 8), Fr(1, 2), Fr(-1, 2), Fr(1), Fr(-1), Fr(1, 12)])
    h, k = R.randint(-3, 3), R.randint(-4, 4)
    b, c = -2 * a * h, a * h * h + k
    D = b * b - 4 * a * c
    fy = (1 - D) / (4 * a)
    dy = -(1 + D) / (4 * a)
    t = R.choice(["F", "d"])
    if t == "F":
        return M("Trova il fuoco della parabola %s." % eq(a, b, c), pt(h, fy, "F"), [pt(h, dy, "F"), pt(h, -fy, "F") if fy else pt(h, 1, "F"), pt(h, k, "F")],
                 "F(−b/(2a); (1 − Δ)/(4a)) con Δ = %s: <b>%s</b> (il fuoco sta a distanza 1/(4|a|) = %s dal vertice, dalla parte della concavità)." % (fq(D), pt(h, fy, "F"), fq(abs(1 / (4 * a)))))
    return M("Trova la direttrice della parabola %s." % eq(a, b, c), "y = %s" % fq(dy), ["y = %s" % fq(v) for v in W(fy, -dy if dy else 1, k)] + ["x = %s" % fq(dy)],
             "Direttrice: y = −(1 + Δ)/(4a) con Δ = %s: <b>y = %s</b>." % (fq(D), fq(dy)))


def s2_assi():
    p, q = R.sample(range(-5, 6), 2)
    a = R.choice([1, -1, 2])
    b, c = -a * (p + q), a * p * q
    t = R.choice(["x", "y"])
    if t == "y":
        return M("In quale punto la parabola %s incontra l’asse y?" % eq(a, b, c), pt(0, c), [pt(c, 0), pt(0, b), pt(0, -c) if c else pt(0, 1)],
                 "Pongo x = 0: y = c = <b>%s</b>." % fq(c))
    lo, hi = sorted([p, q])
    ans = "%s e %s" % (pt(lo, 0), pt(hi, 0))
    return M("In quali punti la parabola %s incontra l’asse x?" % eq(a, b, c), ans, ["%s e %s" % (pt(-hi, 0), pt(-lo, 0)), "%s e %s" % (pt(0, lo), pt(0, hi)), "non incontra l’asse x"],
             "Pongo y = 0: %s = 0 → x = %s ∨ x = %s: <b>%s</b>." % (P2(a, b, c), fq(lo), fq(hi), ans))


def s3_scrivi():
    a, b, c, h, k = par()
    if b.denominator != 1 or c.denominator != 1:
        return None
    x1 = h + R.choice([1, 2, -1, -2])
    y1 = a * (x1 - h) ** 2 + k
    ans = eq(a, b, c)
    w = [eq(-a, -b, -c + 2 * k) if a else eq(1, 0, 0), eq(a, -b, c), eq(2 * a, 2 * b, c), eq(a, b, c + 1), eq(Fr(y1 - k), -2 * (y1 - k) * h, (y1 - k) * h * h + k) if (y1 - k) != a else eq(a, b, c + 1)]
    return M("Scrivi l’equazione della parabola con asse verticale, vertice %s e passante per %s." % (pt(h, k, "V"), pt(x1, y1, "P")), ans, [x for x in w if x != ans],
             "y = %s; sostituisco P: %s = a · %s %s %s → a = %s. Sviluppo: <b>%s</b>." % (vf(Fr(1), h, k).replace("(", "a(", 1) if h else ("ax²" + ((" + %s" % fq(k)) if k > 0 else (" − %s" % fq(-k)) if k else "")), fq(y1), fq((x1 - h) ** 2), "+" if k >= 0 else "−", fq(abs(k)), fq(a), ans))


def s4_retta():
    a = R.choice([1, -1, 1])
    b, c = R.randint(-4, 4), R.randint(-4, 4)
    m, q = R.randint(-3, 3), R.randint(-6, 6)
    # a x² + (b − m) x + (c − q) = 0
    D = (b - m) ** 2 - 4 * a * (c - q)
    ans = "secante (due punti in comune)" if D > 0 else "tangente" if D == 0 else "esterna"
    rr = "y = %s" % P2(0, m, q) if (m or q) else "y = 0"
    return M("Com’è la retta %s rispetto alla parabola %s?" % (rr, eq(a, b, c)), ans, [o for o in ["secante (due punti in comune)", "tangente", "esterna", "asse di simmetria"] if o != ans],
             "Metto a sistema: %s = 0, Δ = %s %s 0: <b>%s</b>." % (P2(a, b - m, c - q), fq(D), "&gt;" if D > 0 else "=" if D == 0 else "&lt;", ans))


def s4_tang():
    a = R.choice([1, -1, 2])
    b, c = R.randint(-4, 4), R.randint(-4, 4)
    x0 = R.randint(-3, 3)
    y0 = a * x0 * x0 + b * x0 + c
    m = 2 * a * x0 + b
    q = y0 - m * x0
    ans = "y = %s" % P2(0, m, q) if (m or q) else "y = 0"
    w = ["y = %s" % P2(0, -m, y0 + m * x0) if (m or y0) else "y = 1", "y = %s" % P2(0, a * x0 + b, y0 - (a * x0 + b) * x0), "y = %s" % P2(0, m, y0) if q != y0 else "y = %s" % P2(0, m, q + 1)]
    return M("Scrivi la retta tangente alla parabola %s nel suo punto di ascissa %s." % (eq(a, b, c), fq(x0)), ans, [x for x in w if x != ans],
             "Il punto è %s. Retta per il punto: y − %s = m(x − %s); a sistema con la parabola impongo Δ = 0 e trovo m = %s (= 2ax<sub>0</sub> + b): <b>%s</b>." % (pt(x0, y0), "(%s)" % fq(y0) if y0 < 0 else fq(y0), "(%s)" % fq(x0) if x0 < 0 else fq(x0), fq(m), ans))


def s5_graf():
    a = R.choice([1, -1])
    h, k = R.randint(-3, 3), R.randint(-3, 3)
    b, c = -2 * a * h, a * h * h + k
    f = lambda x, a=a, h=h, k=k: a * (x - h) ** 2 + k
    fig = relabel(kurve([(f, BLUE, "")], (-5, 5, 1), (-6, 6, 2), pts=[(h, k, "V")], W=300, H=280), "grafico di una parabola")
    ans = eq(a, b, c)
    w = [eq(-a, -b, -c), eq(a, -b, c) if b else eq(a, 1, c), eq(a, b, k if k != c else c + 1)]
    return M("%sQual è l’equazione della parabola del grafico (con a = %s)?" % (fig, fq(a)), ans, [x for x in w if x != ans],
             "Il vertice è %s e a = %s: y = %s = <b>%s</b>." % (pt(h, k, "V"), fq(a), vf(a, h, k), P2(a, b, c)))


def main():
    seen = set()
    sets = [
        ("Vertice, asse, concavità", mix(R, seen, [(s1_vert, 20)])),
        ("Fuoco e direttrice", mix(R, seen, [(s2_fuoco, 14), (s2_assi, 6)])),
        ("Intersezioni e equazione della parabola", mix(R, seen, [(s2_assi, 8), (s3_scrivi, 12)])),
        ("Rette e parabola", mix(R, seen, [(s4_retta, 12), (s4_tang, 8)])),
        ("Grafici", mix(R, seen, [(s5_graf, 14), (s4_tang, 6)])),
    ]
    body = L(["La <b>parabola</b> è il luogo dei punti equidistanti da un punto (il <b>fuoco</b>) e da una retta (la <b>direttrice</b>). Con asse verticale ha equazione y = ax² + bx + c.",
              "Se a &gt; 0 la concavità è verso l’alto, se a &lt; 0 verso il basso. Asse: x = −b/(2a). Vertice: V(−b/(2a); −Δ/(4a)).",
              "Fuoco: F(−b/(2a); (1 − Δ)/(4a)). Direttrice: y = −(1 + Δ)/(4a).",
              "Una retta e una parabola si studiano con il sistema: Δ &gt; 0 secante, Δ = 0 tangente, Δ &lt; 0 esterna."],
             [("y = x² − 4x + 3", ["x<sub>V</sub> = 4/2 = 2", "y<sub>V</sub> = 4 − 8 + 3 = −1"], "V(2; −1), asse x = 2"),
              ("Vertice (1; 2), passa per (3; 10)", ["y = a(x − 1)² + 2", "10 = 4a + 2 → a = 2"], "y = 2x² − 4x + 4")],
             [["x<sub>V</sub> = b/(2a)", "Il segno è meno: x<sub>V</sub> = −b/(2a)."],
              ["Concavità decisa da c", "La decide il segno di a; c è l’intersezione con l’asse y."],
              ["Confondere fuoco e direttrice", "Il fuoco sta dentro la concavità, la direttrice fuori, alla stessa distanza dal vertice."]])
    faq = [("Perché il vertice ha ordinata −Δ/(4a)?", "Perché sostituendo x = −b/(2a) nell’equazione si ottiene (4ac − b²)/(4a) = −Δ/(4a)."),
           ("Come si trova la tangente a una parabola in un suo punto?", "Si scrive il fascio di rette per il punto, lo si mette a sistema con la parabola e si impone Δ = 0. Per la parabola y = ax² + bx + c, nel punto di ascissa x<sub>0</sub> si trova m = 2ax<sub>0</sub> + b.")]
    unit(G, R, "parabola", "G",
         "Le coniche nel piano cartesiano: la parabola come luogo geometrico, equazione, elementi caratteristici, rette tangenti",
         "La parabola", "Parabola",
         "Schede di matematica per la terza liceo sulla parabola: concavità, asse, vertice, fuoco e direttrice, intersezioni con gli assi, equazione dato il vertice, posizione di una retta, retta tangente, grafici. 100 esercizi con soluzioni.",
         "V(−b/(2a); −Δ/(4a))", "Retta e parabola: Δ > 0 secante, Δ = 0 tangente, Δ < 0 esterna.",
         body, faq, sets, 5)


if __name__ == "__main__":
    main()
