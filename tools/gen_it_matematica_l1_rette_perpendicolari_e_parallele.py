# -*- coding: utf-8 -*-
"""
Italia Matematica prima liceo: Rette perpendicolari e parallele (Geometria)
  python3 tools/gen_it_matematica_l1_rette_perpendicolari_e_parallele.py
Angoli formati da due rette e una trasversale (alterni, corrispondenti, coniugati), criterio di parallelismo,
somma degli angoli interni di un triangolo, angolo esterno, somma degli angoli interni ed esterni di un poligono,
poligoni regolari, criteri di congruenza dei triangoli rettangoli, distanza punto-retta.
Errori: angoli coniugati congruenti invece che supplementari, angolo esterno = 180° − un solo interno, (n − 2) · 180° con n − 1.
"""
import math
import random
from it_liceo import M, L, unit, mix, table, W, fq, figure

R = random.Random(72112)
G = "prima-liceo"
INK, BLUE, RED = "#1f2937", "#1f6fd1", "#dc2626"


def trasv(a):
    """due parallele tagliate da una trasversale; angolo a in alto a destra (1) segnato"""
    from ws_common import line, text
    import it_common
    W_, H_ = 340, 200
    t = math.radians(a)
    s = [line(20, 60, 320, 60, INK, 2.2), line(20, 140, 320, 140, INK, 2.2)]
    cx1, cx2 = 170 + 40 / math.tan(t), 170 - 40 / math.tan(t)
    dx = 100 / math.tan(t)
    s.append(line(cx1 + dx * 0.6, 60 - 60, cx2 - dx * 0.6, 200, BLUE, 2))
    s.append(text(330, 64, "r", 16, italic=True) + text(330, 144, "s", 16, italic=True))
    lab = [(1, cx1 + 22, 50), (2, cx1 - 22, 50), (3, cx1 - 22, 80), (4, cx1 + 22, 80), (5, cx2 + 22, 130), (6, cx2 - 22, 130), (7, cx2 - 22, 160), (8, cx2 + 22, 160)]
    for n, x, y in lab:
        s.append(text(x, y, str(n), 15, col=RED if n == 1 else INK, weight=700))
    return it_common.wrap(W_, H_, "".join(s), "due rette parallele r e s tagliate da una trasversale", lg=True) if hasattr(it_common, "wrap") else ""


PAIRS = {(1, 5): ("corrispondenti", "="), (2, 6): ("corrispondenti", "="), (3, 7): ("corrispondenti", "="), (4, 8): ("corrispondenti", "="),
         (3, 5): ("alterni interni", "="), (4, 6): ("alterni interni", "="), (1, 7): ("alterni esterni", "="), (2, 8): ("alterni esterni", "="),
         (3, 6): ("coniugati interni", "s"), (4, 5): ("coniugati interni", "s"), (1, 8): ("coniugati esterni", "s"), (2, 7): ("coniugati esterni", "s"),
         (1, 3): ("opposti al vertice", "="), (2, 4): ("opposti al vertice", "="), (1, 2): ("adiacenti", "s"), (5, 7): ("opposti al vertice", "=")}
# angoli 1,3,5,7 uguali ad a ; 2,4,6,8 = 180 − a  (1 in alto a destra: acuto se a < 90)


def val(n, a):
    return a if n in (1, 3, 5, 7) else 180 - a


def s1_nome():
    (p, q), (nm, _) = R.choice(sorted(PAIRS.items()))
    a = R.choice([50, 55, 60, 65, 70, 75])
    fig = trasv(a)
    opts = ["alterni interni", "corrispondenti", "coniugati interni", "alterni esterni", "coniugati esterni", "opposti al vertice"]
    return M("%sLe rette r e s sono parallele. Come si chiamano gli angoli %d e %d?" % (fig, p, q), nm, [o for o in opts if o != nm][:3] if nm != "adiacenti" else ["alterni interni", "corrispondenti", "coniugati esterni"],
             "Gli angoli %d e %d sono <b>%s</b>." % (p, q, nm))


def s1_val():
    a = R.choice(range(40, 81, 5))
    n = R.randint(2, 8)
    v = val(n, a)
    fig = trasv(a)
    return M("%sLe rette r e s sono parallele e l’angolo 1 misura %d°. Quanto misura l’angolo %d?" % (fig, a, n), "%d°" % v, ["%d°" % x for x in (180 - v, 90 - a if v == a else a - 10, 360 - v, v + 10) if x != v],
             "Con due parallele, gli angoli alterni e corrispondenti sono congruenti, i coniugati supplementari: l’angolo %d misura <b>%d°</b>." % (n, v))


def s2_par():
    a = R.randint(40, 85)
    k = R.choice(["si", "no"])
    if k == "si":
        b = R.choice([a, 180 - a])
        tipo = "alterni interni" if b == a else "coniugati interni"
    else:
        b = a + R.choice([-3, -2, 2, 3])
        tipo = "alterni interni"
    ok = (tipo == "alterni interni" and b == a) or (tipo == "coniugati interni" and a + b == 180)
    ans = "sì" if ok else "no"
    return M("Due rette tagliate da una trasversale formano due angoli %s di %d° e %d°. Le rette sono parallele?" % (tipo, a, b), ans, ["no" if ok else "sì", "solo se gli angoli sono retti", "non si può stabilire"],
             "Le rette sono parallele se gli alterni interni sono congruenti (o i coniugati interni supplementari): %s → <b>%s</b>." % ("%d° e %d° %s" % (a, b, "sono congruenti" if a == b else "hanno somma 180°" if a + b == 180 else "non lo sono"), ans))


def s2_tri():
    a, b = R.randint(20, 100), R.randint(20, 100)
    c = 180 - a - b
    if c <= 5:
        return None
    k = R.choice(["terzo", "est"])
    if k == "terzo":
        return M("In un triangolo due angoli misurano %d° e %d°. Quanto misura il terzo?" % (a, b), "%d°" % c, ["%d°" % x for x in (360 - a - b, 180 - a, a + b) if x != c and x > 0],
                 "La somma degli angoli interni è 180°: 180° − %d° − %d° = <b>%d°</b>." % (a, b, c))
    return M("In un triangolo ABC gli angoli A e B misurano %d° e %d°. Quanto misura l’angolo esterno in C?" % (a, b), "%d°" % (a + b), ["%d°" % x for x in (c, 180 - a, 360 - a - b) if x != a + b],
             "L’angolo esterno è uguale alla somma dei due angoli interni non adiacenti: %d° + %d° = <b>%d°</b>." % (a, b, a + b))


def s3_pol():
    n = R.randint(5, 12)
    k = R.choice(["somma", "reg", "est", "lati"])
    s = (n - 2) * 180
    names = {5: "pentagono", 6: "esagono", 7: "ettagono", 8: "ottagono", 9: "ennagono", 10: "decagono", 11: "endecagono", 12: "dodecagono"}
    if k == "somma":
        return M("Quanto vale la somma degli angoli interni di un %s?" % names[n], "%d°" % s, ["%d°" % x for x in ((n - 1) * 180, n * 180, 360)],
                 "Somma = (n − 2) · 180° = %d · 180° = <b>%d°</b>." % (n - 2, s))
    if k == "reg":
        if s % n:
            return None
        return M("Quanto misura ciascun angolo interno di un %s regolare?" % names[n], "%d°" % (s // n), ["%s°" % x for x in W(360 // n if 360 % n == 0 else None, (n - 1) * 180 // n if (n - 1) * 180 % n == 0 else None, 180 - s // n, s, s // n + 10)],
                 "(%d − 2) · 180° : %d = %d° : %d = <b>%d°</b>." % (n, n, s, n, s // n))
    if k == "est":
        if 360 % n:
            return None
        return M("Quanto misura ciascun angolo esterno di un %s regolare?" % names[n], "%d°" % (360 // n), ["%d°" % x for x in (s // n if s % n == 0 else 180 - 360 // n + 5, 180 // n if 180 % n == 0 else 360 // n + 5, 360 // n + 10)],
                 "La somma degli angoli esterni di ogni poligono è 360°: 360° : %d = <b>%d°</b>." % (n, 360 // n))
    ang = R.choice([108, 120, 135, 140, 144, 150, 156, 160, 162, 165])
    nn = 360 // (180 - ang)
    return M("Ogni angolo interno di un poligono regolare misura %d°. Quanti lati ha?" % ang, str(nn), [str(x) for x in (nn + 1, nn - 1, 360 // ang if 360 // ang > 2 else nn + 2)],
             "L’angolo esterno è 180° − %d° = %d°; i lati sono 360° : %d° = <b>%d</b>." % (ang, 180 - ang, 180 - ang, nn))


RETT = [("le due ipotenuse e un cateto", "sì (criterio particolare dei triangoli rettangoli)"),
        ("i due cateti", "sì (due cateti: è il criterio LAL)"),
        ("un cateto e l’angolo acuto adiacente", "sì (è il criterio ALA)"),
        ("l’ipotenusa e un angolo acuto", "sì (ipotenusa e un angolo acuto)"),
        ("i due angoli acuti", "no (gli angoli da soli non bastano)")]


def s4_rett():
    hyp, ans = R.choice(RETT)
    opts = ["sì (criterio particolare dei triangoli rettangoli)", "no (gli angoli da soli non bastano)", "no (serve sempre conoscere tutti i lati)", "solo se sono isosceli"]
    if ans not in opts:
        opts = [ans] + opts
    return M("Due triangoli rettangoli hanno congruenti %s. Sono congruenti?" % hyp, ans, [o for o in opts if o != ans][:3],
             "Nei triangoli rettangoli l’angolo retto è già uguale: bastano due elementi, purché almeno uno sia un lato. Qui: <b>%s</b>." % ans)


TEO = [("Per un punto esterno a una retta, quante parallele alla retta passano?", "una e una sola (V postulato di Euclide)", ["nessuna", "due", "infinite"]),
       ("Per un punto P si conducono le perpendicolari a una retta r. Quante sono?", "una e una sola", ["nessuna", "due", "infinite"]),
       ("La distanza di un punto P da una retta r è…", "la lunghezza del segmento di perpendicolare da P a r", ["la lunghezza di un segmento qualsiasi da P a r", "l’angolo tra PO e r", "la distanza di P dall’origine"]),
       ("Due rette perpendicolari alla stessa retta (nello stesso piano) sono…", "parallele tra loro", ["perpendicolari tra loro", "incidenti", "coincidenti sempre"]),
       ("In un triangolo rettangolo, gli angoli acuti sono…", "complementari", ["supplementari", "congruenti", "esplementari"]),
       ("Un triangolo può avere due angoli ottusi?", "no, la somma supererebbe 180°", ["sì, se è isoscele", "sì, se è scaleno", "solo se è equilatero"]),
       ("Quanto misura ciascun angolo di un triangolo equilatero?", "60°", ["90°", "45°", "120°"]),
       ("La somma degli angoli esterni di un esagono (uno per vertice) è…", "360°", ["720°", "1080°", "180°"])]


def s5_teo():
    q, a, w = R.choice(TEO)
    return M(q, a, w, "%s <b>%s</b>." % (q.rstrip("?…").rstrip(), a))


def s5_probl():
    x = R.randint(10, 40)
    k = R.choice(["doppio", "piu"])
    if k == "doppio":
        if 4 * x >= 180:
            return None
        c = 180 - 4 * x
        q = "In un triangolo l’angolo B è il triplo dell’angolo A, e l’angolo C misura %d°. Quanto misura A?" % c
        return M(q, "%d°" % x, ["%s°" % v for v in W(3 * x, (180 - c) // 3, 180 - c - x, 180 - c, x + 10)], "x + 3x + %d° = 180° → 4x = %d° → <b>x = %d°</b>." % (c, 180 - c, x))
    dd = R.randint(5, 30)
    if 3 * x + 3 * dd >= 180 or (180 - 3 * dd) % 3:
        return None
    a = (180 - 3 * dd) // 3
    q = "Gli angoli di un triangolo sono x, x + %d° e x + %d°. Quanto misura il minore?" % (dd, 2 * dd)
    return M(q, "%d°" % a, ["%s°" % v for v in W(a + dd, 60, a + 2 * dd, (180 - dd) // 3, a - dd)], "3x + %d° = 180° → <b>x = %d°</b>." % (3 * dd, a))


def main():
    seen = set()
    sets = [
        ("Angoli formati da due parallele e una trasversale", mix(R, seen, [(s1_nome, 10), (s1_val, 10)])),
        ("Criterio di parallelismo e angoli del triangolo", mix(R, seen, [(s2_par, 8), (s2_tri, 12)])),
        ("Angoli dei poligoni", mix(R, seen, [(s3_pol, 20)])),
        ("Triangoli rettangoli e teoremi", mix(R, seen, [(s4_rett, 5), (s5_teo, 8), (s1_val, 7)])),
        ("Problemi con gli angoli", mix(R, seen, [(s5_probl, 12), (s2_tri, 8)])),
    ]
    body = L(["Due rette tagliate da una trasversale formano 8 angoli: <b>alterni</b> (da parti opposte della trasversale), <b>corrispondenti</b> (nella stessa posizione), <b>coniugati</b> (dalla stessa parte).",
              "Le rette sono <b>parallele</b> se e solo se gli alterni sono congruenti, i corrispondenti sono congruenti, i coniugati sono supplementari.",
              "Da qui: la somma degli angoli interni di un triangolo è <b>180°</b> e ogni angolo esterno è uguale alla somma dei due interni non adiacenti.",
              "In un poligono di n lati la somma degli angoli interni è (n − 2) · 180°; la somma degli angoli esterni è sempre 360°."],
             [("Angolo interno di un ottagono regolare", ["(8 − 2) · 180° = 1080°", "1080° : 8"], "135°"),
              ("Triangolo con A = 50° e B = 70°: angolo esterno in C", ["50° + 70°"], "120°")],
             [["Coniugati congruenti", "Con le parallele i coniugati sono supplementari (somma 180°)."],
              ["Angolo esterno = 180° − A", "È 180° meno l’angolo interno adiacente, cioè A + B."],
              ["Somma degli angoli interni (n − 1) · 180°", "Un poligono si divide in n − 2 triangoli: (n − 2) · 180°."]])
    faq = [("Perché la somma degli angoli di un triangolo è 180°?", "Si traccia per un vertice la parallela al lato opposto: i due angoli che si formano sono alterni interni agli altri due angoli del triangolo, e i tre angoli insieme formano un angolo piatto."),
           ("Che cosa dice il quinto postulato di Euclide?", "Per un punto esterno a una retta passa una e una sola parallela a quella retta. Da questo postulato si ricavano le proprietà degli angoli formati da due parallele.")]
    unit(G, R, "rette-perpendicolari-e-parallele", "G",
         "Rette perpendicolari e parallele; angoli formati da due rette e una trasversale; somma degli angoli di un triangolo e di un poligono",
         "Rette perpendicolari e parallele", "Rette perpendicolari e parallele",
         "Schede di matematica per la prima liceo su rette perpendicolari e parallele: angoli alterni, corrispondenti e coniugati, criterio di parallelismo, angoli del triangolo e angolo esterno, angoli dei poligoni, triangoli rettangoli. 100 esercizi con soluzioni.",
         "Somma degli angoli di un triangolo: 180°", "In un poligono di n lati: (n − 2) · 180°; gli esterni sommano 360°.",
         body, faq, sets, 12)


if __name__ == "__main__":
    main()
