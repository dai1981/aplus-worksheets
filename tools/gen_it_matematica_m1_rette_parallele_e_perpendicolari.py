# -*- coding: utf-8 -*-
"""
Italia Matematica prima media: Rette parallele e perpendicolari (Spazio e figure)
  python3 tools/gen_it_matematica_m1_rette_parallele_e_perpendicolari.py
Rette parallele, incidenti, perpendicolari; distanza di un punto da una retta e tra rette parallele; asse di un segmento;
angoli formati da due parallele tagliate da una trasversale (alterni interni ed esterni, corrispondenti, coniugati).
Errori: pensare che angoli coniugati siano congruenti, misurare la distanza lungo un segmento obliquo.
"""
import math
import random
from it_media import M, L, unit, mix, table, W
from it_common import wrap, text, line, INK, RED, BLUE, GREEN

R = random.Random(71112)
G = "prima-media"
# Gli 8 angoli: intorno al punto sulla retta a (in alto) 1, 2, 3, 4 e sulla retta b (in basso) 5, 6, 7, 8,
# in senso antiorario a partire dalla semiretta verso destra. La trasversale sale verso destra con angolo alpha:
# gli angoli 1, 3, 5, 7 misurano alpha (acuti), 2, 4, 6, 8 misurano 180° − alpha.


def fig(alpha, marks):
    """alpha: angolo acuto tra la trasversale e le parallele (gradi). marks: {numero: testo}"""
    Wd, H = 380, 220
    ya, yb = 70, 150
    c = 1 / math.tan(math.radians(alpha))
    xa, xb = 190 + 40 * c, 190 - 40 * c
    s = [line(20, ya, Wd - 20, ya, BLUE, 2.4), line(20, yb, Wd - 20, yb, BLUE, 2.4),
         text(Wd - 12, ya - 6, "a", 16, col=BLUE), text(Wd - 12, yb - 6, "b", 16, col=BLUE),
         line(xa + 50 * c, ya - 50, xb - 50 * c, yb + 50, INK, 2.4)]
    mids = [alpha / 2.0, (alpha + 180) / 2.0, 180 + alpha / 2.0, (180 + alpha + 360) / 2.0]
    for (px, py), base in (((xa, ya), 0), ((xb, yb), 4)):
        for k in range(4):
            n = base + k + 1
            if n in marks:
                t = math.radians(mids[k])
                r = 30 if k in (0, 2) and alpha < 50 else 24
                s.append(text(px + r * math.cos(t), py - r * math.sin(t) + 5, marks[n], 14, col=RED, weight=700))
    return wrap(Wd, H, "".join(s), "due rette parallele a e b tagliate da una trasversale", lg=True)


def ang(n, alpha):
    return alpha if n in (1, 3, 5, 7) else 180 - alpha


NOMI = {frozenset({3, 5}): "alterni interni", frozenset({4, 6}): "alterni interni", frozenset({2, 8}): "alterni esterni", frozenset({1, 7}): "alterni esterni",
        frozenset({1, 5}): "corrispondenti", frozenset({2, 6}): "corrispondenti", frozenset({3, 7}): "corrispondenti", frozenset({4, 8}): "corrispondenti",
        frozenset({3, 6}): "coniugati interni", frozenset({4, 5}): "coniugati interni", frozenset({2, 7}): "coniugati esterni", frozenset({1, 8}): "coniugati esterni"}


def s2_nome():
    pair = R.choice(list(NOMI))
    a, b = sorted(pair)
    alpha = R.choice([40, 50, 55, 60, 65, 70])
    nm = NOMI[pair]
    return M(fig(alpha, {a: "α", b: "β"}) + "Come si chiamano gli angoli α e β?", nm, W(*[x for x in ("alterni interni", "alterni esterni", "corrispondenti", "coniugati interni", "coniugati esterni") if x != nm]),
             "Guarda dove stanno rispetto alle parallele (dentro o fuori) e alla trasversale (stessa parte o parti opposte): sono <b>%s</b>." % nm)


def s3_misura():
    pair = R.choice(list(NOMI))
    a, b = sorted(pair)
    alpha = R.choice([35, 40, 45, 50, 55, 60, 65, 70, 75])
    va, vb = ang(a, alpha), ang(b, alpha)
    nm = NOMI[pair]
    return M(fig(alpha, {a: "%d°" % va, b: "?"}) + "Le rette a e b sono parallele. Quanto misura l’angolo «?»?", "%d°" % vb, W("%d°" % (180 - vb), "%d°" % (90 - min(va, vb)) if min(va, vb) < 90 else None, "%d°" % (vb + 10), "%d°" % (360 - vb)),
             "Gli angoli sono %s: %s. <b>%d°</b>." % (nm, "sono supplementari, 180° − %d° = %d°" % (va, vb) if "coniugati" in nm else "sono congruenti", vb))


def s1_quiz():
    q, a, w = R.choice([("Due rette perpendicolari formano…", "quattro angoli retti", ["due angoli acuti e due ottusi", "quattro angoli acuti", "nessun angolo"]),
                        ("La distanza di un punto da una retta si misura…", "lungo la perpendicolare alla retta", ["lungo un segmento obliquo qualsiasi", "lungo la retta", "con il goniometro"]),
                        ("Per un punto esterno a una retta, quante parallele a essa si possono tracciare?", "una sola", ["infinite", "due", "nessuna"]),
                        ("Per un punto, quante perpendicolari a una retta si possono tracciare?", "una sola", ["infinite", "due", "nessuna"]),
                        ("Due rette parallele alla stessa retta sono…", "parallele tra loro", ["perpendicolari tra loro", "incidenti", "sempre coincidenti"]),
                        ("Due rette perpendicolari alla stessa retta sono…", "parallele tra loro", ["perpendicolari tra loro", "incidenti", "oblique"]),
                        ("L’asse di un segmento è…", "la perpendicolare passante per il punto medio", ["la retta che contiene il segmento", "una retta qualsiasi per un estremo", "la bisettrice"]),
                        ("I punti dell’asse di un segmento sono…", "equidistanti dagli estremi del segmento", ["sempre sul segmento", "più vicini a uno degli estremi", "alla stessa distanza dal punto medio"]),
                        ("La distanza tra due rette parallele…", "è la stessa in ogni punto", ["cambia da punto a punto", "è sempre 0", "non si può misurare"]),
                        ("Due angoli alterni interni formati da due parallele e una trasversale sono…", "congruenti", ["supplementari", "complementari", "sempre retti"]),
                        ("Due angoli coniugati interni formati da due parallele e una trasversale sono…", "supplementari", ["congruenti", "complementari", "esplementari"]),
                        ("Due angoli corrispondenti formati da due parallele e una trasversale sono…", "congruenti", ["supplementari", "complementari", "sempre acuti"])])
    return M(q, a, w, "Risposta: <b>%s</b>." % a)


def s4_problema():
    alpha = R.randint(25, 85)
    k = R.choice(["somma", "diff", "tutti"])
    if k == "somma":
        return M("Due parallele sono tagliate da una trasversale. Un angolo acuto misura %d°. Quanto fa la somma di due angoli coniugati interni?" % alpha, "180°", W("%d°" % (2 * alpha), "90°", "360°"),
                 "I coniugati interni sono sempre supplementari: <b>180°</b>.")
    if k == "diff":
        return M("Due parallele sono tagliate da una trasversale; un angolo misura %d°. Quanto misura il suo coniugato interno?" % alpha, "%d°" % (180 - alpha), W("%d°" % alpha, "%d°" % (90 - alpha), "%d°" % (360 - alpha)),
                 "180° − %d° = <b>%d°</b>." % (alpha, 180 - alpha))
    return M("Due parallele sono tagliate da una trasversale. Uno degli 8 angoli misura %d°. Quanti degli 8 angoli misurano %d°?" % (alpha, alpha), "4", W("2", "8", "1"),
             "Gli 8 angoli sono di due misure: 4 misurano %d° e 4 misurano %d°." % (alpha, 180 - alpha))


def main():
    seen = set()
    sets = [
        ("Parallele, perpendicolari e distanze", mix(R, seen, [(s1_quiz, 12), (s4_problema, 8)])),
        ("Riconoscere le coppie di angoli", mix(R, seen, [(s2_nome, 20)])),
        ("Trovare le misure", mix(R, seen, [(s3_misura, 20)])),
        ("Coppie di angoli e misure", mix(R, seen, [(s2_nome, 8), (s3_misura, 12)])),
        ("Problemi", mix(R, seen, [(s4_problema, 8), (s3_misura, 6), (s2_nome, 6)])),
    ]
    body = L(["Due rette del piano sono <b>parallele</b> se non hanno punti in comune, <b>incidenti</b> se ne hanno uno; sono <b>perpendicolari</b> se formano quattro angoli retti.",
              "La <b>distanza</b> di un punto da una retta è la lunghezza del segmento di perpendicolare. L’<b>asse</b> di un segmento è la perpendicolare nel suo punto medio.",
              "Due parallele tagliate da una trasversale formano 8 angoli: gli <b>alterni</b> (interni o esterni) e i <b>corrispondenti</b> sono congruenti; i <b>coniugati</b> sono supplementari.",
              "Quindi gli 8 angoli hanno solo due misure: α e 180° − α."],
             [("Un angolo è 65°; il coniugato interno?", ["coniugati: supplementari", "180° − 65°"], "115°")],
             [["Pensare che i coniugati siano congruenti", "I coniugati sono supplementari (somma 180°)."],
              ["Misurare la distanza lungo un segmento obliquo", "La distanza è sempre sulla perpendicolare: è il percorso più breve."],
              ["Usare le regole anche se le rette non sono parallele", "Le uguaglianze valgono solo per rette parallele."]],
             table(["Coppia", "Relazione"], [["alterni interni / esterni", "congruenti"], ["corrispondenti", "congruenti"], ["coniugati interni / esterni", "supplementari"]]))
    faq = [("Come si riconoscono gli angoli alterni?", "Stanno da parti opposte rispetto alla trasversale, tutti e due dentro (interni) o tutti e due fuori (esterni) dalle parallele."),
           ("Dove si usano queste proprietà?", "Per dimostrare che la somma degli angoli di un triangolo è 180° e per calcolare gli angoli dei parallelogrammi e dei trapezi.")]
    unit(G, R, "rette-parallele-e-perpendicolari", "S",
         "Conoscere definizioni e proprietà di rette parallele e perpendicolari; riconoscere gli angoli formati da due rette parallele tagliate da una trasversale e le loro relazioni",
         "Rette parallele, perpendicolari e trasversali", "Rette parallele e perpendicolari",
         "Schede di matematica per la prima media su rette parallele e perpendicolari: distanza, asse di un segmento, angoli alterni, corrispondenti e coniugati formati da due parallele e una trasversale, problemi. 100 esercizi con soluzioni.",
         "Alterni e corrispondenti: congruenti.", "Coniugati: supplementari.",
         body, faq, sets, 12)


if __name__ == "__main__":
    main()
