# -*- coding: utf-8 -*-
"""
Italia Matematica seconda liceo: Circonferenza e poligoni inscritti e circoscritti (Geometria)
  python3 tools/gen_it_matematica_l2_circonferenza_e_poligoni_inscritti.py
Corde e distanza dal centro, posizioni di una retta e di due circonferenze, tangenti (perpendicolari al raggio, segmenti di tangenza),
angoli al centro e alla circonferenza, angolo inscritto in una semicirconferenza, quadrilateri inscritti e circoscritti,
punti notevoli del triangolo (circocentro, incentro, baricentro, ortocentro).
Errori: angolo alla circonferenza = angolo al centro, baricentro nel punto medio della mediana, quadrilatero inscritto con angoli opposti congruenti.
"""
import math
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, d, figure

R = random.Random(72209)
G = "seconda-liceo"


def circ_fig(angc):
    """circonferenza con angolo al centro AOB e angolo alla circonferenza APB"""
    from ws_common import line, text
    import it_common
    W_, H_ = 240, 220
    cx, cy, r = 120, 112, 80
    a1, a2 = math.radians(200), math.radians(200 + angc)
    A = (cx + r * math.cos(a1), cy - r * math.sin(a1))
    B = (cx + r * math.cos(a2), cy - r * math.sin(a2))
    pm = math.radians(200 + angc + (360 - angc) / 2)
    Pp = (cx + r * math.cos(pm), cy - r * math.sin(pm))
    s = ["<circle cx='%d' cy='%d' r='%d' fill='none' stroke='#1f2937' stroke-width='2'/>" % (cx, cy, r)]
    for (x1, y1), (x2, y2), col in ((A, (cx, cy), "#1f6fd1"), (B, (cx, cy), "#1f6fd1"), (A, Pp, "#dc2626"), (B, Pp, "#dc2626")):
        s.append(line(x1, y1, x2, y2, col, 2))
    for (x, y), n in ((A, "A"), (B, "B"), (Pp, "P")):
        dx, dy = x - cx, y - cy
        L_ = math.hypot(dx, dy)
        s.append(text(x + dx / L_ * 14, y + dy / L_ * 14 + 5, n, 15))
    s.append("<circle cx='%d' cy='%d' r='3' fill='#1f2937'/>" % (cx, cy) + text(cx + 10, cy + 16, "O", 15))
    return it_common.wrap(W_, H_, "".join(s), "circonferenza con angolo al centro e angolo alla circonferenza", lg=True)


def s1_angoli():
    c = R.choice(range(40, 161, 4))
    fig = circ_fig(c)
    if R.random() < 0.5:
        return M("%sL’angolo al centro AÔB misura %d°. Quanto misura l’angolo alla circonferenza APB che insiste sullo stesso arco?" % (fig, c), "%d°" % (c // 2), ["%d°" % x for x in (c, 2 * c, 180 - c)],
                 "L’angolo alla circonferenza è la <b>metà</b> dell’angolo al centro corrispondente: %d° : 2 = <b>%d°</b>." % (c, c // 2))
    return M("%sL’angolo alla circonferenza APB misura %d°. Quanto misura l’angolo al centro AÔB che insiste sullo stesso arco?" % (fig, c // 2), "%d°" % c, ["%d°" % x for x in (c // 2, c // 4 if c % 4 == 0 else c + 10, 180 - c // 2)],
             "L’angolo al centro è il <b>doppio</b> dell’angolo alla circonferenza: 2 · %d° = <b>%d°</b>." % (c // 2, c))


def s1_semi():
    a = R.randint(20, 70)
    return M("AB è un diametro e C è un punto della circonferenza. L’angolo CAB misura %d°. Quanto misura l’angolo CBA?" % a, "%d°" % (90 - a), ["%s°" % x for x in W(180 - a, a, 180 - 2 * a, 90 + a, 90)],
             "Un angolo inscritto in una semicirconferenza è retto: ACB = 90°, quindi CBA = 90° − %d° = <b>%d°</b>." % (a, 90 - a))


def s2_corda():
    a, b, c = R.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 16, 20), (7, 24, 25)])
    k = R.choice(["corda", "dist", "r"])
    if k == "corda":
        return M("In una circonferenza di raggio %d cm una corda dista %d cm dal centro. Quanto è lunga la corda?" % (c, a), "%d cm" % (2 * b), ["%s cm" % x for x in W(b, c + a, 2 * c - a, 2 * a, 2 * c)],
                 "La perpendicolare dal centro divide a metà la corda: metà corda = √(%d² − %d²) = %d, corda = <b>%d cm</b>." % (c, a, b, 2 * b))
    if k == "dist":
        return M("In una circonferenza di raggio %d cm una corda è lunga %d cm. Quanto dista dal centro?" % (c, 2 * b), "%d cm" % a, ["%s cm" % x for x in W(c - b, 2 * b - c if 2 * b > c else c + 1, b, c + b, 2 * a)],
                 "Metà corda %d cm: distanza = √(%d² − %d²) = <b>%d cm</b>." % (b, c, b, a))
    return M("Una corda lunga %d cm dista %d cm dal centro. Quanto misura il raggio?" % (2 * b, a), "%d cm" % c, ["%d cm" % x for x in (a + b, 2 * b, a + 2 * b)],
             "r = √(%d² + %d²) = <b>%d cm</b>." % (b, a, c))


def s2_tang():
    a, b, c = R.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (20, 21, 29)])
    k = R.choice(["tg", "seg"])
    if k == "tg":
        return M("Da un punto P distante %d cm dal centro di una circonferenza di raggio %d cm si conduce una tangente. Quanto è lungo il segmento di tangenza?" % (c, a), "%d cm" % b, ["%d cm" % x for x in (c - a, c + a, int(round(math.sqrt(c * c + a * a))))],
                 "La tangente è perpendicolare al raggio nel punto di contatto: √(%d² − %d²) = <b>%d cm</b>." % (c, a, b))
    t = R.randint(4, 15)
    return M("Da un punto P esterno si conducono le due tangenti PA e PB a una circonferenza. Se PA = %d cm, quanto misura PB?" % t, "%d cm" % t, ["%d cm" % x for x in (2 * t, t // 2 if t % 2 == 0 else t + 1, t + 2)],
             "I segmenti di tangenza condotti da un punto esterno sono congruenti: <b>%d cm</b>." % t)


def s3_pos():
    r = R.randint(3, 12)
    dd = R.choice([r - R.randint(1, r - 1), r, r + R.randint(1, 6)])
    ans = "secante" if dd < r else "tangente" if dd == r else "esterna"
    return M("Una circonferenza ha raggio %d cm e una retta dista %d cm dal centro. Com’è la retta rispetto alla circonferenza?" % (r, dd), ans, [o for o in ["secante", "tangente", "esterna", "diametrale"] if o != ans],
             "Confronto la distanza d = %d con il raggio r = %d: d %s r, quindi la retta è <b>%s</b>." % (dd, r, "&lt;" if dd < r else "=" if dd == r else "&gt;", ans))


def s3_due():
    r1, r2 = R.randint(2, 9), R.randint(2, 9)
    if r1 == r2:
        return None
    s, df = r1 + r2, abs(r1 - r2)
    dd, ans = R.choice([(s + R.randint(1, 5), "esterne"), (s, "tangenti esternamente"), (R.randint(df + 1, s - 1) if s - 1 > df else s + 2, "secanti"), (df, "tangenti internamente"), (R.randint(0, df - 1) if df > 0 else s + 3, "una interna all’altra")])
    real = "esterne" if dd > s else "tangenti esternamente" if dd == s else "secanti" if dd > df else "tangenti internamente" if dd == df else "una interna all’altra"
    return M("Due circonferenze hanno raggi %d cm e %d cm e i centri distano %d cm. Come sono?" % (r1, r2, dd), real, [o for o in ["esterne", "tangenti esternamente", "secanti", "tangenti internamente", "una interna all’altra"] if o != real][:3],
             "Confronto d = %d con r<sub>1</sub> + r<sub>2</sub> = %d e |r<sub>1</sub> − r<sub>2</sub>| = %d: <b>%s</b>." % (dd, s, df, real))


def s4_quad():
    k = R.choice(["insc", "circ"])
    if k == "insc":
        a = R.randint(50, 130)
        return M("Un quadrilatero ABCD è inscritto in una circonferenza e l’angolo A misura %d°. Quanto misura l’angolo C?" % a, "%d°" % (180 - a), ["%d°" % x for x in (a, 360 - a, 90 + a // 2 if 90 + a // 2 != 180 - a else a + 10)],
                 "In un quadrilatero inscritto gli angoli opposti sono supplementari: 180° − %d° = <b>%d°</b>." % (a, 180 - a))
    a, b, c = R.randint(4, 15), R.randint(4, 15), R.randint(4, 15)
    dd = a + c - b
    if dd <= 0:
        return None
    return M("Un quadrilatero ABCD è circoscritto a una circonferenza. AB = %d cm, BC = %d cm, CD = %d cm. Quanto misura DA?" % (a, b, c), "%d cm" % dd, ["%s cm" % x for x in W(a + b - c, b + c - a, a + b + c - dd * 0 if False else (a + c + b) // 3)],
             "In un quadrilatero circoscritto le somme dei lati opposti sono uguali: AB + CD = BC + DA → DA = %d + %d − %d = <b>%d cm</b>." % (a, c, b, dd))


PN = [("il punto d’incontro degli assi dei lati", "circocentro (centro della circonferenza circoscritta)"),
      ("il punto d’incontro delle bisettrici degli angoli", "incentro (centro della circonferenza inscritta)"),
      ("il punto d’incontro delle mediane", "baricentro"),
      ("il punto d’incontro delle altezze", "ortocentro")]
PNs = [p[1] for p in PN]


def s5_punti():
    a, b = R.choice(PN)
    if R.random() < 0.5:
        return M("Come si chiama %s di un triangolo?" % a, b, [x for x in PNs if x != b], "%s è il <b>%s</b>." % (a[0].upper() + a[1:], b))
    qs = [("In un triangolo rettangolo dove si trova il circocentro?", "nel punto medio dell’ipotenusa", ["nel vertice dell’angolo retto", "fuori dal triangolo", "nel baricentro"]),
          ("In un triangolo ottusangolo dove si trova l’ortocentro?", "fuori dal triangolo", ["dentro il triangolo", "su un lato", "nel punto medio del lato maggiore"]),
          ("In un triangolo equilatero, circocentro, incentro, baricentro e ortocentro…", "coincidono", ["sono allineati ma distinti", "formano un quadrato", "stanno sui vertici"]),
          ("L’incentro di un triangolo si trova sempre…", "dentro il triangolo", ["fuori dal triangolo", "su un lato", "su un vertice"])]
    q, aa, w = R.choice(qs)
    return M(q, aa, w, "%s <b>%s</b>." % (q.rstrip("?…"), aa))


def s5_bar():
    m = R.choice([6, 9, 12, 15, 18, 21, 24, 27, 30])
    k = R.choice(["vert", "lato"])
    if k == "vert":
        return M("Una mediana di un triangolo misura %d cm. Quanto dista il baricentro dal vertice da cui parte la mediana?" % m, "%d cm" % (2 * m // 3), ["%s cm" % d(Fr(m, 2)), "%d cm" % (m // 3), "%d cm" % m],
                 "Il baricentro divide ogni mediana in due parti, una doppia dell’altra (2 : 1, la parte maggiore verso il vertice): 2/3 · %d = <b>%d cm</b>." % (m, 2 * m // 3))
    return M("Una mediana di un triangolo misura %d cm. Quanto dista il baricentro dal lato (dal punto medio)?" % m, "%d cm" % (m // 3), ["%s cm" % d(Fr(m, 2)), "%d cm" % (2 * m // 3), "%d cm" % (m // 4) if m % 4 == 0 else "%d cm" % (m // 3 + 1)],
             "Il baricentro divide la mediana nel rapporto 2 : 1: verso il lato resta 1/3 · %d = <b>%d cm</b>." % (m, m // 3))


def main():
    seen = set()
    sets = [
        ("Angoli al centro e alla circonferenza", mix(R, seen, [(s1_angoli, 14), (s1_semi, 6)])),
        ("Corde e tangenti", mix(R, seen, [(s2_corda, 12), (s2_tang, 8)])),
        ("Posizioni reciproche", mix(R, seen, [(s3_pos, 10), (s3_due, 10)])),
        ("Quadrilateri inscritti e circoscritti", mix(R, seen, [(s4_quad, 14), (s1_semi, 6)])),
        ("Punti notevoli del triangolo", mix(R, seen, [(s5_punti, 8), (s5_bar, 12)])),
    ]
    body = L(["La perpendicolare dal centro a una corda la divide a metà; corde congruenti hanno la stessa distanza dal centro. La <b>tangente</b> è perpendicolare al raggio nel punto di contatto.",
              "Retta e circonferenza: secante se d &lt; r, tangente se d = r, esterna se d &gt; r. Due circonferenze si confrontano con r<sub>1</sub> + r<sub>2</sub> e |r<sub>1</sub> − r<sub>2</sub>|.",
              "L’<b>angolo alla circonferenza</b> è la metà dell’angolo al centro che insiste sullo stesso arco. Un angolo inscritto in una semicirconferenza è retto.",
              "Un quadrilatero è <b>inscrivibile</b> se gli angoli opposti sono supplementari, <b>circoscrivibile</b> se le somme dei lati opposti sono uguali. Punti notevoli: circocentro (assi), incentro (bisettrici), baricentro (mediane, rapporto 2 : 1), ortocentro (altezze)."],
             [("Angolo al centro 110°", ["Alla circonferenza: 110° : 2"], "55°"),
              ("Raggio 13, corda 24", ["Metà corda 12", "√(169 − 144)"], "distanza 5")],
             [["Angolo alla circonferenza = angolo al centro", "È la metà."],
              ["Baricentro nel punto medio della mediana", "La divide 2 : 1, a 2/3 dal vertice."],
              ["Inscritto: angoli opposti congruenti", "Sono supplementari (somma 180°)."]])
    faq = [("Perché l’angolo inscritto in una semicirconferenza è retto?", "Perché l’angolo al centro corrispondente è un angolo piatto (180°) e l’angolo alla circonferenza ne è la metà: 90°."),
           ("Ogni triangolo si può inscrivere in una circonferenza?", "Sì: il circocentro è equidistante dai tre vertici ed è il centro della circonferenza circoscritta. Ogni triangolo ha anche una circonferenza inscritta, con centro nell’incentro.")]
    unit(G, R, "circonferenza-e-poligoni-inscritti", "G",
         "La circonferenza: corde, tangenti, angoli al centro e alla circonferenza; poligoni inscritti e circoscritti; punti notevoli del triangolo",
         "Circonferenza e poligoni inscritti e circoscritti", "Circonferenza e poligoni inscritti",
         "Schede di matematica per la seconda liceo su circonferenza e poligoni: corde e tangenti, posizioni di rette e circonferenze, angoli al centro e alla circonferenza, quadrilateri inscritti e circoscritti, punti notevoli del triangolo. 100 esercizi con soluzioni.",
         "Angolo alla circonferenza = ½ angolo al centro", "Quadrilatero inscritto: angoli opposti supplementari.",
         body, faq, sets, 9)


if __name__ == "__main__":
    main()
