# -*- coding: utf-8 -*-
"""
Italia Matematica classe seconda: Linee, confini e regioni (Spazio e figure)
  python3 tools/gen_it_matematica_c2_linee_e_regioni.py
Linee rette, curve, spezzate e miste; linee aperte e chiuse; il confine, la regione interna e la regione esterna;
linee orizzontali, verticali e oblique; contare i segmenti di una linea spezzata.
Errori: chiamare chiusa una linea che quasi si chiude, pensare che il confine sia dentro la regione, confondere verticale e orizzontale.
"""
import random
from it_common import mcq, lesson, make_unit, mix, wrap, text, line, INK, RED, BLUE, GREEN, FILL
import gen_it_matematica_c3_linee_e_angoli as L3

R = random.Random(70215)
G = "classe-seconda"


def path(d, col=INK, w=3, fill="none"):
    return "<path d='%s' fill='%s' stroke='%s' stroke-width='%s' stroke-linecap='round' stroke-linejoin='round'/>" % (d, fill, col, w)


def s1_tipo():
    return L3.s1_linee()


def chiusa_o_aperta(closed):
    import math
    n = R.randint(5, 8)
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n + R.uniform(-0.2, 0.2)
        rr = R.uniform(0.6, 1.0)
        pts.append((110 + 85 * rr * math.cos(t), 65 + 48 * rr * math.sin(t)))
    smooth = R.random() < 0.5
    if not closed:
        pts = pts[:-1] if R.random() < 0.5 else pts
    if smooth:
        m = [((pts[i][0] + pts[(i + 1) % len(pts)][0]) / 2, (pts[i][1] + pts[(i + 1) % len(pts)][1]) / 2) for i in range(len(pts))]
        if closed:
            d = "M%.0f %.0f " % m[-1] + " ".join("Q%.0f %.0f %.0f %.0f" % (pts[i][0], pts[i][1], m[i][0], m[i][1]) for i in range(len(pts))) + " Z"
        else:
            d = "M%.0f %.0f " % pts[0] + " ".join("Q%.0f %.0f %.0f %.0f" % (pts[i][0], pts[i][1], m[i][0], m[i][1]) for i in range(1, len(pts) - 1))
    else:
        d = "M" + " L".join("%.0f %.0f" % p_ for p_ in pts) + (" Z" if closed else "")
    return wrap(220, 130, path(d), "una linea")


def s1_chiusa():
    c = R.random() < 0.5
    ans = "chiusa" if c else "aperta"
    return mcq(chiusa_o_aperta(c) + "Questa linea è aperta o chiusa?", ans, ["aperta" if c else "chiusa", "retta", "né aperta né chiusa"],
               "%s: è <b>%s</b>." % ("Torna al punto di partenza e non ha estremi liberi" if c else "Ha due estremi che non si toccano", ans))


def regione(pos):
    """pos: 'dentro', 'fuori', 'confine'"""
    s = [path("M40 75 C40 15 200 10 210 70 C220 130 60 140 40 75 Z", INK, 3, "#e7f3ea")]
    pt = {"dentro": (R.randint(90, 160), R.randint(55, 95)), "fuori": R.choice([(240, 30), (250, 120), (25, 20), (120, 140)]), "confine": R.choice([(40, 75), (210, 70)])}[pos]
    s.append("<circle cx='%d' cy='%d' r='7' fill='%s'/>" % (pt[0] if pt[0] < 265 else 255, pt[1], RED))
    return wrap(270, 150, "".join(s), "una regione con un punto rosso")


def s2_regione():
    pos = R.choice(["dentro", "fuori", "confine"])
    ans = {"dentro": "nella regione interna", "fuori": "nella regione esterna", "confine": "sul confine"}[pos]
    pic = regione(pos)
    return mcq(pic + "Dove si trova il punto rosso?", ans, [x for x in ("nella regione interna", "nella regione esterna", "sul confine") if x != ans] + ["in nessun posto"],
               "Il punto è %s: <b>%s</b>." % ({"dentro": "dentro la linea chiusa", "fuori": "fuori dalla linea chiusa", "confine": "proprio sulla linea"}[pos], ans))


REG = [("Il confine divide il piano in…", "una regione interna e una regione esterna", ["due linee", "tre regioni", "niente"]),
       ("Quale linea ha una regione interna?", "una linea chiusa", ["una linea aperta", "una linea retta", "un segmento"]),
       ("La recinzione di un giardino è…", "il confine", ["la regione esterna", "la regione interna", "una linea aperta"]),
       ("I fiori dentro il recinto sono…", "nella regione interna", ["sul confine", "nella regione esterna", "fuori"]),
       ("Le auto in strada, fuori dal recinto del parco, sono…", "nella regione esterna", ["nella regione interna", "sul confine", "dentro"]),
       ("Per entrare in una regione chiusa…", "devi attraversare il confine", ["non devi attraversare niente", "devi saltare due confini", "non si può mai"]),
       ("Una linea aperta ha…", "due estremi liberi", ["nessun estremo", "un estremo", "una regione interna"]),
       ("Il bordo del lago è…", "il confine del lago", ["la regione interna", "una linea aperta", "la regione esterna"])]


def s2_quiz():
    q, a, w = R.choice(REG)
    return mcq(q, a, w, "Risposta: <b>%s</b>." % a)


def dir_svg(kind):
    if kind == "orizzontale":
        y = R.randint(40, 90)
        s = line(30, y, 190, y, BLUE, 4)
    elif kind == "verticale":
        x = R.randint(60, 160)
        s = line(x, 15, x, 115, BLUE, 4)
    else:
        s = line(40, R.choice([20, 110]), 180, R.choice([110, 20]), BLUE, 4) if R.random() < 0.5 else line(50, 110, 170, 30, BLUE, 4)
    return wrap(220, 130, "<rect x='4' y='4' width='212' height='122' fill='none' stroke='%s' stroke-width='1' stroke-dasharray='4 4'/>" % INK + s, "una linea dentro un riquadro")


def s3_direzione():
    k = R.choice(["orizzontale", "verticale", "obliqua"])
    return mcq(dir_svg(k) + "Come è questa linea?", k, [x for x in ("orizzontale", "verticale", "obliqua") if x != k] + ["curva"],
               "%s: è <b>%s</b>." % ({"orizzontale": "È distesa come l’orizzonte", "verticale": "Sta in piedi come un palo", "obliqua": "È inclinata"}[k], k))


def spezzata(n):
    pts = [(20 + i * (200 // n), R.choice([25, 55, 95, 115]) if i % 2 else R.choice([30, 70, 105])) for i in range(n + 1)]
    for i in range(1, len(pts)):
        if pts[i][1] == pts[i - 1][1]:
            pts[i] = (pts[i][0], pts[i][1] + 30 if pts[i][1] < 80 else pts[i][1] - 30)
    d = "M" + " L".join("%d %d" % p for p in pts)
    dots = "".join("<circle cx='%d' cy='%d' r='4' fill='%s'/>" % (x, y, RED) for x, y in pts)
    return wrap(240, 130, path(d) + dots, "una linea spezzata")


def s3_segmenti():
    n = R.randint(2, 7)
    return mcq(spezzata(n) + "Da quanti segmenti è formata questa linea spezzata?", str(n), [str(n + 1), str(n - 1), str(n + 2)],
               "Conta i pezzi dritti tra un punto rosso e l’altro: <b>%d</b>." % n)


def s5_vita():
    q, a, w = R.choice([("Il filo per stendere i panni, tirato bene, è una linea…", "retta", ["curva", "chiusa", "spezzata"]),
                        ("Il bordo di un piatto rotondo è una linea…", "curva chiusa", ["retta", "spezzata aperta", "curva aperta"]),
                        ("Il percorso di uno scivolo a onde è una linea…", "curva aperta", ["retta", "curva chiusa", "spezzata chiusa"]),
                        ("I denti di una sega formano una linea…", "spezzata", ["curva", "retta", "mista chiusa"]),
                        ("Il bordo di un quaderno è una linea…", "spezzata chiusa", ["curva", "spezzata aperta", "curva chiusa"]),
                        ("La corda di un aquilone che sventola è una linea…", "curva", ["retta", "spezzata", "chiusa"]),
                        ("Il contorno di una fetta di pizza è una linea…", "mista chiusa", ["retta", "curva aperta", "spezzata aperta"]),
                        ("Le righe del quaderno sono linee…", "orizzontali", ["verticali", "oblique", "curve"]),
                        ("Il palo della luce è una linea…", "verticale", ["orizzontale", "obliqua", "curva"]),
                        ("Uno scivolo dritto è una linea…", "obliqua", ["orizzontale", "verticale", "chiusa"]),
                        ("La linea di partenza di una corsa è…", "una linea retta aperta", ["una linea chiusa", "una regione", "un confine chiuso"]),
                        ("Il recinto di un campo di calcio è una linea…", "chiusa", ["aperta", "curva aperta", "obliqua"])])
    return mcq(q, a, w, "Risposta: <b>%s</b>." % a)


def main():
    L3.R = R
    seen = set()
    sets = [
        ("Linee rette, curve e spezzate", mix(R, seen, [(s1_tipo, 20)])),
        ("Linee aperte e chiuse", mix(R, seen, [(s1_chiusa, 20)])),
        ("Confine e regioni", mix(R, seen, [(s2_regione, 12), (s2_quiz, 8)])),
        ("Orizzontale, verticale, obliqua", mix(R, seen, [(s3_direzione, 10), (s3_segmenti, 10)])),
        ("Linee intorno a noi", mix(R, seen, [(s5_vita, 12), (s3_segmenti, 4), (s2_regione, 4)])),
    ]
    body = lesson(
        ["Le linee possono essere <b>rette</b>, <b>curve</b>, <b>spezzate</b> (fatte di segmenti) o <b>miste</b>.",
         "Una linea <b>chiusa</b> torna al punto di partenza; una linea <b>aperta</b> ha due estremi liberi.",
         "Una linea chiusa è un <b>confine</b>: divide il foglio in <b>regione interna</b> (dentro) e <b>regione esterna</b> (fuori).",
         "Una linea può essere <b>orizzontale</b> (distesa), <b>verticale</b> (in piedi) o <b>obliqua</b> (inclinata)."],
        [("Un recinto intorno alle pecore", ["il recinto è il confine", "le pecore sono dentro"], "le pecore sono nella regione interna")],
        [["Chiamare chiusa una linea che quasi si chiude", "Guarda bene: se c’è un’apertura, è aperta."],
         ["Pensare che il confine sia dentro la regione", "Il confine è la linea stessa: non è dentro né fuori."],
         ["Confondere verticale e orizzontale", "Verticale come un albero, orizzontale come il pavimento."]],
        regione("dentro"))
    faq = [("Che cos’è una regione?", "È una parte del piano: una linea chiusa forma una regione interna (dentro) e una esterna (fuori)."),
           ("Perché in seconda si studiano le linee?", "Perché preparano le figure geometriche: i poligoni sono linee spezzate chiuse.")]
    make_unit(R, "linee-e-regioni", "S",
              "Riconoscere, denominare e descrivere linee (rette, curve, spezzate, aperte, chiuse); riconoscere confine, regione interna e regione esterna",
              "Linee, confini e regioni", "Linee e regioni",
              "Schede di matematica per la classe seconda su linee, confini e regioni: linee rette, curve, spezzate e miste, aperte e chiuse, regione interna ed esterna, orizzontale, verticale e obliqua. 100 esercizi con soluzioni.",
              "Una linea chiusa forma un confine.", "Dentro: regione interna. Fuori: regione esterna.",
              body, faq, sets, 15, grade=G)


if __name__ == "__main__":
    main()
