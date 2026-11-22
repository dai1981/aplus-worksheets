# -*- coding: utf-8 -*-
"""
Italia Matematica terza media: Circonferenza e cerchio (Spazio e figure)
  python3 tools/gen_it_matematica_m3_circonferenza_e_cerchio.py
Elementi (raggio, diametro, corda, arco, settore, segmento circolare), posizioni di una retta e di due circonferenze,
angoli al centro e alla circonferenza (metà), angolo inscritto in una semicirconferenza (retto), tangente perpendicolare
al raggio, corde e distanza dal centro (Pitagora), quadrilateri inscritti (angoli opposti supplementari).
Errori: angolo alla circonferenza = angolo al centro, confondere cerchio e circonferenza, usare il diametro al posto del raggio.
"""
import math
import random
from it_media import M, L, unit, mix, table, W, Kids
from it_common import wrap, line, text, INK, BLUE, RED

R = random.Random(71308)
G = "terza-media"
K = Kids(R)
TERNE = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 16, 20), (7, 24, 25)]


def circ_svg(center_deg, arc_pts, label):
    """circonferenza con centro O, punti A, B (arco) e P sulla circonferenza; mostra l’angolo al centro AOB e alla circonferenza APB"""
    cx, cy, r = 130, 125, 95
    s = ["<circle cx='%d' cy='%d' r='%d' fill='none' stroke='%s' stroke-width='2.2'/>" % (cx, cy, r, INK)]
    P = {}
    for k, a in arc_pts.items():
        P[k] = (cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a)))
    P["O"] = (cx, cy)
    for a, b in (("O", "A"), ("O", "B")):
        s.append(line(P[a][0], P[a][1], P[b][0], P[b][1], BLUE, 2))
    if "P" in P:
        for a, b in (("P", "A"), ("P", "B")):
            s.append(line(P[a][0], P[a][1], P[b][0], P[b][1], RED, 2))
    for k, (x, y) in P.items():
        dx, dy = x - cx, y - cy
        L_ = math.hypot(dx, dy) or 1
        off = 16 if k != "O" else 0
        s.append("<circle cx='%.1f' cy='%.1f' r='3.5' fill='%s'/>" % (x, y, INK))
        s.append(text(x + dx / L_ * off + (0 if k != "O" else -12), y + dy / L_ * off + 5 + (0 if k != "O" else 14), k, 15, weight=600))
    return wrap(260, 250, "".join(s), label, lg=True)


def s1_elementi():
    q, a, w = R.choice([
        ("Il segmento che unisce due punti della circonferenza si chiama…", "corda", ["raggio", "arco", "tangente"]),
        ("La corda che passa per il centro si chiama…", "diametro", ["raggio", "arco", "secante"]),
        ("La parte di circonferenza compresa tra due punti si chiama…", "arco", ["corda", "settore", "segmento"]),
        ("La parte di cerchio compresa tra due raggi e un arco si chiama…", "settore circolare", ["segmento circolare", "corona circolare", "corda"]),
        ("La parte di cerchio compresa tra una corda e un arco si chiama…", "segmento circolare", ["settore circolare", "corona circolare", "diametro"]),
        ("La parte di piano compresa tra due circonferenze concentriche si chiama…", "corona circolare", ["settore circolare", "segmento circolare", "arco"]),
        ("La differenza tra circonferenza e cerchio è che…", "la circonferenza è la linea, il cerchio è la superficie", ["sono la stessa cosa", "il cerchio è la linea", "la circonferenza è più grande"]),
        ("La corda più lunga di una circonferenza è…", "il diametro", ["il raggio", "una tangente", "un arco"]),
        ("Una retta che tocca la circonferenza in un solo punto si chiama…", "tangente", ["secante", "esterna", "corda"]),
        ("La tangente in un punto della circonferenza è sempre…", "perpendicolare al raggio in quel punto", ["parallela al raggio", "uguale al diametro", "passante per il centro"]),
        ("Due circonferenze con lo stesso centro si chiamano…", "concentriche", ["tangenti", "secanti", "congruenti"]),
        ("Per tre punti non allineati passa…", "una e una sola circonferenza", ["nessuna circonferenza", "infinite circonferenze", "due circonferenze"]),
    ])
    return M(q, a, w, "Risposta: <b>%s</b>." % a)


def s1_posizioni():
    r = R.randint(3, 20)
    k = R.choice(["retta", "retta", "due"])
    if k == "retta":
        dd = r + R.choice([-2, -1, 0, 0, 1, 3]) * R.randint(1, 2)
        if dd < 0:
            return None
        ans = "secante" if dd < r else "tangente" if dd == r else "esterna"
        return M("Una circonferenza ha raggio %d cm. Una retta dista %d cm dal centro. La retta è…" % (r, dd), ans, [v for v in ["secante", "tangente", "esterna"] if v != ans] + ["un diametro"],
                 "Distanza %s raggio: retta <b>%s</b>." % ("&lt;" if dd < r else "=" if dd == r else "&gt;", ans))
    r2 = R.randint(2, 12)
    dd = R.choice([r + r2, abs(r - r2) + 1 if abs(r - r2) + 1 < r + r2 else r + r2, r + r2 + R.randint(1, 5)])
    if r == r2:
        return None
    ans = "tangenti esternamente" if dd == r + r2 else "secanti" if abs(r - r2) < dd < r + r2 else "esterne"
    return M("Due circonferenze hanno raggi %d cm e %d cm; la distanza tra i centri è %d cm. Le circonferenze sono…" % (r, r2, dd), ans, [v for v in ["tangenti esternamente", "secanti", "esterne", "concentriche"] if v != ans],
             "Somma dei raggi: %d cm. Distanza %s: <b>%s</b>." % (r + r2, "= somma" if dd == r + r2 else "&gt; somma" if dd > r + r2 else "tra la differenza e la somma", ans))


def s2_angoli():
    c = R.choice(range(40, 181, 10)) if R.random() < 0.8 else R.choice([60, 80, 100, 120, 140])
    a1 = R.randint(200, 240)
    a2 = a1 + c
    pa = (a1 + a2) / 2.0 + 180
    pic = circ_svg(c, {"A": a1, "B": a2, "P": pa + R.choice([-25, 0, 25])}, "angolo al centro AOB e angolo alla circonferenza APB")
    if R.random() < 0.5:
        return M("%sL’angolo al centro AÔB misura %d°. Quanto misura l’angolo alla circonferenza APB (che insiste sullo stesso arco)?" % (pic, c), "%d°" % (c // 2), W("%d°" % c, "%d°" % (2 * c) if 2 * c < 360 else "%d°" % (180 - c), "%d°" % (180 - c // 2), "%d°" % (90 - c // 2) if c < 180 else "45°"),
                 "L’angolo alla circonferenza è la metà dell’angolo al centro: %d : 2 = <b>%d°</b>." % (c, c // 2))
    return M("%sL’angolo alla circonferenza APB misura %d°. Quanto misura l’angolo al centro AÔB?" % (pic, c // 2), "%d°" % c, W("%d°" % (c // 2), "%d°" % (c // 4) if c % 4 == 0 else "%d°" % (c + 10), "%d°" % (180 - c // 2), "%d°" % (360 - c)),
             "L’angolo al centro è il doppio: %d × 2 = <b>%d°</b>." % (c // 2, c))


def s2_semicirc():
    k = R.choice(["retto", "tri", "quad"])
    if k == "retto":
        a = R.randint(20, 70)
        return M("Il triangolo ABC è inscritto in una circonferenza e AB è un diametro. L’angolo in A misura %d°. Quanto misura l’angolo in B?" % a, "%d°" % (90 - a), W("%d°" % (180 - a), "%d°" % a, "90°", "%d°" % (180 - 2 * a) if 180 - 2 * a > 0 else "45°"),
                 "Un angolo inscritto in una semicirconferenza è retto: C = 90°. B = 180° − 90° − %d° = <b>%d°</b>." % (a, 90 - a))
    if k == "tri":
        a, b, c = R.choice(TERNE)
        return M("Un triangolo rettangolo ha i cateti di %d cm e %d cm ed è inscritto in una circonferenza. Quanto misura il raggio?" % (a, b), "%s cm" % (str(c / 2).replace(".", ",").replace(",0", "")), W("%d cm" % c, "%s cm" % str((a + b) / 2).replace(".", ",").replace(",0", ""), "%d cm" % (c * 2), "%s cm" % str(a / 2).replace(".", ",").replace(",0", "")),
                 "L’ipotenusa è un diametro: √(%d² + %d²) = %d cm; raggio = %d : 2 = <b>%s cm</b>." % (a, b, c, c, str(c / 2).replace(".", ",").replace(",0", "")))
    a = R.randint(50, 130)
    return M("Un quadrilatero ABCD è inscritto in una circonferenza. L’angolo in A misura %d°. Quanto misura l’angolo opposto in C?" % a, "%d°" % (180 - a), W("%d°" % a, "%d°" % (360 - a), "%d°" % (90 - a) if a < 90 else "%d°" % (a - 90), "%d°" % (a // 2)),
             "In un quadrilatero inscritto gli angoli opposti sono supplementari: 180° − %d° = <b>%d°</b>." % (a, 180 - a))


def s3_corde():
    a, b, c = R.choice(TERNE)
    k = R.choice(["corda", "dist", "tang", "tang2"])
    if k == "corda":
        return M("In una circonferenza di raggio %d cm una corda dista %d cm dal centro. Quanto è lunga la corda?" % (c, a), "%d cm" % (2 * b), W("%d cm" % b, "%d cm" % (2 * c - a), "%d cm" % (c + a), "%d cm" % (2 * a)),
                 "La distanza dal centro divide la corda a metà: metà corda = √(%d² − %d²) = %d cm; corda = <b>%d cm</b>." % (c, a, b, 2 * b))
    if k == "dist":
        return M("In una circonferenza di raggio %d cm una corda è lunga %d cm. Quanto dista dal centro?" % (c, 2 * b), "%d cm" % a, W("%d cm" % b, "%d cm" % (c - b), "%d cm" % int(math.isqrt(abs(c * c - 4 * b * b))) if c * c > 4 * b * b and math.isqrt(c * c - 4 * b * b) ** 2 == c * c - 4 * b * b else "%d cm" % (a + 1), "%d cm" % (2 * a)),
                 "Metà corda: %d cm; distanza = √(%d² − %d²) = <b>%d cm</b>." % (b, c, b, a))
    if k == "tang":
        return M("Da un punto P esterno, distante %d cm dal centro di una circonferenza di raggio %d cm, si traccia una tangente. Quanto è lungo il segmento di tangente da P al punto di contatto?" % (c, a), "%d cm" % b, W("%d cm" % (c - a), "%d cm" % (c + a), "%d cm" % c, "%d cm" % (b + 1)),
                 "Il raggio è perpendicolare alla tangente: √(%d² − %d²) = <b>%d cm</b>." % (c, a, b))
    return M("Il segmento di tangente da un punto P alla circonferenza è %d cm e il raggio è %d cm. Quanto dista P dal centro?" % (b, a), "%d cm" % c, W("%d cm" % (a + b), "%d cm" % (b - a) if b > a else "%d cm" % (a - b), "%d cm" % (c + 1), "%d cm" % (c * c)), "√(%d² + %d²) = <b>%d cm</b>." % (b, a, c))


def s4_poligoni():
    q, a, w = R.choice([
        ("Un poligono è inscritto in una circonferenza se…", "tutti i suoi vertici stanno sulla circonferenza", ["tutti i lati sono tangenti alla circonferenza", "il centro è un vertice", "ha almeno un lato uguale al raggio"]),
        ("Un poligono è circoscritto a una circonferenza se…", "tutti i suoi lati sono tangenti alla circonferenza", ["tutti i vertici stanno sulla circonferenza", "ha il centro fuori", "è regolare"]),
        ("Un quadrilatero si può inscrivere in una circonferenza se…", "gli angoli opposti sono supplementari", ["i lati opposti sono uguali", "ha un angolo retto", "le diagonali sono uguali"]),
        ("Un quadrilatero si può circoscrivere a una circonferenza se…", "la somma di due lati opposti è uguale alla somma degli altri due", ["gli angoli opposti sono supplementari", "è un rettangolo", "ha i lati paralleli"]),
        ("Ogni triangolo…", "si può inscrivere e circoscrivere a una circonferenza", ["si può solo inscrivere", "si può solo circoscrivere", "non si può inscrivere"]),
        ("Il centro della circonferenza circoscritta a un triangolo è…", "il circocentro (incontro degli assi)", ["l’incentro", "il baricentro", "l’ortocentro"]),
        ("Il centro della circonferenza inscritta in un triangolo è…", "l’incentro (incontro delle bisettrici)", ["il circocentro", "il baricentro", "l’ortocentro"]),
        ("In un esagono regolare inscritto, il lato è uguale…", "al raggio della circonferenza", ["al diametro", "alla metà del raggio", "all’apotema"]),
        ("Quale di questi quadrilateri si può sempre inscrivere in una circonferenza?", "il rettangolo", ["il rombo (non quadrato)", "il parallelogramma qualsiasi", "il trapezio rettangolo"]),
        ("Quale di questi quadrilateri si può sempre circoscrivere a una circonferenza?", "il rombo", ["il rettangolo (non quadrato)", "il parallelogramma qualsiasi", "il trapezio rettangolo qualsiasi"]),
    ])
    return M(q, a, w, "Risposta: <b>%s</b>." % a)


def s4_reg():
    n = R.choice([3, 4, 5, 6, 8, 9, 10, 12])
    k = R.choice(["centro", "interno"])
    if k == "centro":
        return M("Un poligono regolare di %d lati è inscritto in una circonferenza. Quanto misura ciascun angolo al centro (tra due raggi consecutivi)?" % n, "%s°" % str(360 / n).replace(".0", "").replace(".", ","), W("%d°" % (180 * (n - 2) // n) if 180 * (n - 2) % n == 0 else None, "%s°" % str(180 / n).replace(".0", "").replace(".", ","), "%d°" % (360 - 360 // n), "%d°" % n),
                     "360° : %d = <b>%s°</b>." % (n, str(360 / n).replace(".0", "").replace(".", ",")))
    if 180 * (n - 2) % n:
        return None
    return M("Quanto misura ciascun angolo interno di un poligono regolare di %d lati?" % n, "%d°" % (180 * (n - 2) // n), W("%s°" % str(360 / n).replace(".0", "").replace(".", ","), "%d°" % (180 * (n - 2)), "%d°" % (180 - 180 * (n - 2) // n) if n != 4 else "60°", "%d°" % (180 * n // (n + 2)) if 180 * n % (n + 2) == 0 else None, "%d°" % (180 * (n - 2) // n - 10), "%d°" % (180 * (n - 1) // n) if 180 * (n - 1) % n == 0 else "%d°" % (180 * (n - 2) // n + 10)),
             "Somma degli angoli interni: 180° × (%d − 2) = %d°; %d° : %d = <b>%d°</b>." % (n, 180 * (n - 2), 180 * (n - 2), n, 180 * (n - 2) // n))


def main():
    seen = set()
    sets = [
        ("Elementi della circonferenza", mix(R, seen, [(s1_elementi, 12), (s1_posizioni, 8)])),
        ("Angoli al centro e alla circonferenza", mix(R, seen, [(s2_angoli, 20)])),
        ("Semicirconferenza e quadrilateri inscritti", mix(R, seen, [(s2_semicirc, 14), (s1_posizioni, 6)])),
        ("Corde e tangenti", mix(R, seen, [(s3_corde, 20)])),
        ("Poligoni inscritti e circoscritti", mix(R, seen, [(s4_poligoni, 10), (s4_reg, 10)])),
    ]
    body = L(["La <b>circonferenza</b> è la linea formata dai punti che hanno la stessa distanza (il <b>raggio</b>) dal centro; il <b>cerchio</b> è la parte di piano che essa racchiude.",
              "Una retta è <b>esterna</b>, <b>tangente</b> o <b>secante</b> se la sua distanza dal centro è maggiore, uguale o minore del raggio. La tangente è perpendicolare al raggio nel punto di contatto.",
              "Un <b>angolo alla circonferenza</b> è la metà dell’angolo al centro che insiste sullo stesso arco. Se insiste su una semicirconferenza è <b>retto</b>.",
              "La perpendicolare dal centro a una corda la divide a metà: raggio, metà corda e distanza formano un triangolo rettangolo."],
             [("Raggio 10 cm, corda a 6 cm dal centro", ["metà corda = √(100 − 36) = 8 cm"], "corda = 16 cm")],
             [["Angolo alla circonferenza = angolo al centro", "È la metà: se al centro è 80°, alla circonferenza è 40°."],
              ["Usare il diametro al posto del raggio", "Il raggio è metà del diametro."],
              ["Dimenticare di raddoppiare la metà corda", "Pitagora dà metà corda: la corda intera è il doppio."]],
             table(["Distanza d dal centro", "Retta"], [["d &lt; r", "secante"], ["d = r", "tangente"], ["d &gt; r", "esterna"]]))
    faq = [("Perché l’angolo inscritto in una semicirconferenza è retto?", "Perché insiste su un arco il cui angolo al centro è 180° (l’angolo piatto); la metà di 180° è 90°."),
           ("Un rombo si può inscrivere in una circonferenza?", "Solo se è un quadrato: negli altri rombi gli angoli opposti sono uguali ma non supplementari.")]
    unit(G, R, "circonferenza-e-cerchio", "S",
         "Conoscere definizioni e proprietà significative delle principali figure piane; conoscere le proprietà della circonferenza e del cerchio, degli angoli al centro e alla circonferenza, dei poligoni inscritti e circoscritti",
         "Circonferenza e cerchio", "Circonferenza e cerchio",
         "Schede di matematica per la terza media sulla circonferenza e il cerchio: elementi, posizioni di rette e circonferenze, angoli al centro e alla circonferenza, corde, tangenti, poligoni inscritti e circoscritti. 100 esercizi con soluzioni.",
         "Angolo alla circonferenza = metà dell’angolo al centro.", "La tangente è perpendicolare al raggio.",
         body, faq, sets, 8)


if __name__ == "__main__":
    main()
