# -*- coding: utf-8 -*-
"""
Italia Matematica terza media: Problemi con le equazioni (Relazioni e funzioni)
  python3 tools/gen_it_matematica_m3_problemi_con_le_equazioni.py
Tradurre una frase in un’equazione, problemi sui numeri (consecutivi, doppio, triplo), sull’età, sulla geometria
(perimetro, angoli del triangolo), sul denaro e sulle percentuali; scegliere l’equazione giusta e risolverla.
Errori: scegliere male l’incognita, «il triplo di un numero aumentato di 5» = 3(x + 5), dimenticare di rispondere alla domanda.
"""
import random
from it_media import M, L, unit, mix, table, W, num, Kids

R = random.Random(71306)
G = "terza-media"
K = Kids(R)


def s1_tradurre():
    a, b = R.randint(2, 9), R.randint(2, 20)
    k = R.choice(["dop", "tri_aum", "tri_par", "meta", "succ", "diff"])
    if k == "dop":
        return M("Quale equazione traduce: «Il doppio di un numero diminuito di %d è uguale a %d»?" % (b, a * 2 + 10), "2x − %d = %d" % (b, a * 2 + 10), ["2(x − %d) = %d" % (b, a * 2 + 10), "x − %d = 2 · %d" % (b, a * 2 + 10), "2x + %d = %d" % (b, a * 2 + 10)],
                 "«Il doppio di un numero» è 2x; «diminuito di %d» toglie %d: <b>2x − %d = %d</b>." % (b, b, b, a * 2 + 10))
    if k == "tri_aum":
        return M("Quale equazione traduce: «Il triplo di un numero, aumentato di %d, dà %d»?" % (b, 3 * a + b), "3x + %d = %d" % (b, 3 * a + b), ["3(x + %d) = %d" % (b, 3 * a + b), "x + 3 · %d = %d" % (b, 3 * a + b), "3x = %d + %d" % (b, 3 * a + b)],
                 "Prima il triplo (3x), poi si aggiunge %d: <b>3x + %d = %d</b>." % (b, b, 3 * a + b))
    if k == "tri_par":
        return M("Quale equazione traduce: «Il triplo della somma di un numero e %d è %d»?" % (b, 3 * (a + b)), "3(x + %d) = %d" % (b, 3 * (a + b)), ["3x + %d = %d" % (b, 3 * (a + b)), "x + 3 · %d = %d" % (b, 3 * (a + b)), "3 + x + %d = %d" % (b, 3 * (a + b))],
                 "Prima la somma (x + %d), poi il triplo: <b>3(x + %d) = %d</b>." % (b, b, 3 * (a + b)))
    if k == "meta":
        return M("Quale equazione traduce: «La metà di un numero aumentata di %d è %d»?" % (b, a + b), "x/2 + %d = %d" % (b, a + b), ["(x + %d)/2 = %d" % (b, a + b), "2x + %d = %d" % (b, a + b), "x/2 = %d + %d" % (b, a + b)],
                 "La metà è x/2, poi + %d: <b>x/2 + %d = %d</b>." % (b, b, a + b))
    if k == "succ":
        s = 2 * a + 1 + 2 * b
        return M("Quale equazione traduce: «La somma di due numeri consecutivi è %d»?" % s, "x + (x + 1) = %d" % s, ["x + x = %d" % s, "x · (x + 1) = %d" % s, "x + 1 = %d" % s],
                 "Due consecutivi: x e x + 1. <b>x + (x + 1) = %d</b>." % s)
    return M("Quale equazione traduce: «Un numero supera di %d il suo quinto»?" % (4 * a), "x − x/5 = %d" % (4 * a), ["x/5 − x = %d" % (4 * a), "x = %d · x/5" % (4 * a), "x + x/5 = %d" % (4 * a)],
             "«Supera di %d il suo quinto»: x − x/5 = %d. <b>x − x/5 = %d</b>." % (4 * a, 4 * a, 4 * a))


def s2_numeri():
    k = R.choice(["cons2", "cons3", "doppio", "pari", "diff"])
    if k == "cons2":
        x = R.randint(10, 80)
        s = 2 * x + 1
        return M("La somma di due numeri consecutivi è %d. Qual è il numero minore?" % s, num(x), W(num(x + 1), num(s // 2 + 1) if s // 2 + 1 != x + 1 else None, num(x - 1), num(s - 1)), "x + x + 1 = %d → 2x = %d → <b>x = %d</b> (e l’altro è %d)." % (s, s - 1, x, x + 1))
    if k == "cons3":
        x = R.randint(10, 60)
        s = 3 * x + 3
        return M("La somma di tre numeri consecutivi è %d. Qual è il maggiore?" % s, num(x + 2), W(num(x), num(x + 1), num(s // 3 + 2) if s // 3 + 2 != x + 2 else num(x + 3)), "x + (x + 1) + (x + 2) = %d → 3x = %d → x = %d; il maggiore è <b>%d</b>." % (s, s - 3, x, x + 2))
    if k == "doppio":
        x = R.randint(5, 50)
        m = R.choice([2, 3, 4])
        s = x + m * x
        return M("Un numero sommato al suo %s dà %d. Qual è il numero?" % ({2: "doppio", 3: "triplo", 4: "quadruplo"}[m], s), num(x), W(num(s // m), num(s - m), num(m * x), num(s // 2) if s % 2 == 0 and s // 2 != x else None), "x + %dx = %d → %dx = %d → <b>x = %d</b>." % (m, s, m + 1, s, x))
    if k == "pari":
        x = R.randint(5, 40) * 2
        s = 2 * x + 2
        return M("La somma di due numeri pari consecutivi è %d. Quali sono?" % s, "%d e %d" % (x, x + 2), W("%d e %d" % (s // 2, s // 2 + 1), "%d e %d" % (x - 2, x), "%d e %d" % (x + 2, x + 4)), "x + (x + 2) = %d → 2x = %d → x = %d: <b>%d e %d</b>." % (s, s - 2, x, x, x + 2))
    a = R.randint(5, 40)
    dlt = R.randint(3, 25)
    s = 2 * a + dlt
    return M("Due numeri hanno somma %d e differenza %d. Qual è il maggiore?" % (s, dlt), num(a + dlt), W(num(a), num(s - dlt), num((s + dlt) // 2 + dlt) if (s + dlt) // 2 + dlt != a + dlt else None, num(s // 2) if s // 2 not in (a, a + dlt) else None),
             "x + (x − %d) = %d → 2x = %d → <b>x = %d</b>." % (dlt, s, s + dlt, a + dlt))


def s3_eta():
    p = K.next()
    k = R.choice(["padre", "fra", "anni_fa"])
    if k == "padre":
        x = R.randint(8, 15)
        m = R.choice([3, 4])
        return M("Il padre di %s ha il %s dei suoi anni. Insieme hanno %d anni. Quanti anni ha %s?" % (p[0], "triplo" if m == 3 else "quadruplo", (m + 1) * x, p[0]), num(x), W(num(m * x), num((m + 1) * x // m) if (m + 1) * x % m == 0 else num(x + 2), num((m + 1) * x // 2) if (m + 1) * x % 2 == 0 else num(x - 2)),
                 "x + %dx = %d → %dx = %d → <b>x = %d</b>; il padre ha %d anni." % (m, (m + 1) * x, m + 1, (m + 1) * x, x, m * x))
    if k == "fra":
        x = R.randint(5, 14)
        dlt = R.randint(2, 6)
        s = 2 * x + dlt
        q = K.next()
        return M("%s ha %d anni più di %s. La somma delle loro età è %d. Quanti anni ha %s?" % (p[0], dlt, q[0], s, q[0]), num(x), W(num(x + dlt), num(s // 2) if s // 2 != x else None, num(s - dlt), num(x - dlt) if x > dlt else None), "x + (x + %d) = %d → 2x = %d → <b>x = %d</b>." % (dlt, s, s - dlt, x))
    x = R.randint(6, 14)
    y = R.randint(14, 24)
    # padre oggi P; tra y anni il padre avrà il doppio dell'età del figlio: P + y = 2(x + y)
    Pd = 2 * (x + y) - y
    return M("Oggi %s ha %d anni e il padre %d. Tra quanti anni il padre avrà il doppio degli anni di %s?" % (p[0], x, Pd, p[0]), num(y), W(num(Pd - 2 * x) if Pd - 2 * x != y else None, num(y + 1), num(Pd - x), num(y * 2)), "%d + t = 2(%d + t) → %d + t = %d + 2t → <b>t = %d</b>." % (Pd, x, Pd, 2 * x, y))


def s4_geo():
    k = R.choice(["rett", "tri", "angoli", "iso"])
    if k == "rett":
        b = R.randint(5, 30)
        dlt = R.randint(2, 12)
        h = b + dlt
        p = 2 * (b + h)
        return M("In un rettangolo l’altezza supera la base di %d cm e il perimetro è %d cm. Quanto misura la base?" % (dlt, p), "%d cm" % b, W("%d cm" % h, "%d cm" % ((p - dlt) // 2) if (p - dlt) % 2 == 0 else "%d cm" % (b + 1), "%d cm" % (p // 4), "%d cm" % (p // 2 - dlt)), "2(x + x + %d) = %d → 4x + %d = %d → 4x = %d → <b>x = %d cm</b>." % (dlt, p, 2 * dlt, p, p - 2 * dlt, b))
    if k == "tri":
        x = R.randint(4, 20)
        a, b = R.randint(1, 6), R.randint(2, 3)
        p = x + (x + a) + b * x
        return M("I lati di un triangolo misurano x, x + %d e %dx (in cm). Il perimetro è %d cm. Quanto misura il lato maggiore?" % (a, b, p), "%d cm" % max(x, x + a, b * x), W("%d cm" % x, "%d cm" % (x + a) if x + a != max(x, x + a, b * x) else "%d cm" % (b * x + 1), "%d cm" % (p // 3), "%d cm" % (b * x + a)),
                 "x + x + %d + %dx = %d → %dx = %d → x = %d; i lati sono %d, %d, %d cm: il maggiore è <b>%d cm</b>." % (a, b, p, b + 2, p - a, x, x, x + a, b * x, max(x, x + a, b * x)))
    if k == "angoli":
        x = R.choice([v for v in range(15, 60, 5)])
        a = R.choice([2, 3])
        c = 180 - x - a * x
        if c <= 0 or c == x or c == a * x:
            return None
        return M("In un triangolo un angolo misura x, un altro %dx e il terzo %d°. Quanto misura x?" % (a, c), "%d°" % x, W("%d°" % (a * x), "%d°" % ((180 - c) // 2) if (180 - c) % 2 == 0 and (180 - c) // 2 != x else None, "%d°" % (180 - c), "%d°" % (x + 10)), "x + %dx + %d = 180 → %dx = %d → <b>x = %d°</b>." % (a, c, a + 1, 180 - c, x))
    b = R.randint(6, 20)
    lo = b + R.randint(2, 10)
    p = b + 2 * lo
    return M("Un triangolo isoscele ha il perimetro di %d cm e ciascun lato obliquo supera la base di %d cm. Quanto misura la base?" % (p, lo - b), "%d cm" % b, W("%d cm" % lo, "%d cm" % (p // 3), "%d cm" % ((p - (lo - b)) // 2) if (p - (lo - b)) % 2 == 0 else "%d cm" % (b + 2), "%d cm" % (b - 1)),
             "x + 2(x + %d) = %d → 3x = %d → <b>x = %d cm</b>." % (lo - b, p, p - 2 * (lo - b), b))


def s5_soldi():
    p, q = K.next(), K.next()
    k = R.choice(["divid", "risp", "biglietti", "sconto"])
    if k == "divid":
        x = R.randint(5, 60)
        m = R.choice([2, 3])
        t = x + m * x
        return M("%s %s %s hanno in tutto %d €. %s ha il %s di %s. Quanti euro ha %s?" % (p[0], "ed" if q[0][0] in "AEIOU" else "e", q[0], t, p[0], "doppio" if m == 2 else "triplo", q[0], q[0]), "%d €" % x, W("%d €" % (m * x), "%d €" % (t // 2) if t % 2 == 0 and t // 2 != x else None, "%d €" % (t - m), "%d €" % (t // m) if t % m == 0 and t // m != x else None, "%d €" % (x + 10), "%d €" % (x - 3)),
                 "x + %dx = %d → %dx = %d → <b>x = %d €</b>." % (m, t, m + 1, t, x))
    if k == "risp":
        s0 = R.randint(2, 10) * 10
        w_ = R.randint(3, 15)
        n = R.randint(4, 20)
        tot = s0 + w_ * n
        return M("%s ha già %d € e risparmia %d € a settimana. Dopo quante settimane avrà %d €?" % (p[0], s0, w_, tot), num(n), W(num(tot // w_) if tot % w_ == 0 and tot // w_ != n else None, num(n + 1), num((tot + s0) // w_) if (tot + s0) % w_ == 0 else num(n - 1), num(tot - s0)), "%d + %dx = %d → %dx = %d → <b>x = %d</b>." % (s0, w_, tot, w_, tot - s0, n))
    if k == "biglietti":
        a, b = R.choice([(8, 5), (12, 7), (10, 6), (15, 9)])
        n = R.randint(20, 60)
        x = R.randint(5, n - 5)
        tot = a * x + b * (n - x)
        return M("Per una gita si vendono %d biglietti: gli interi costano %d €, i ridotti %d €. L’incasso è %d €. Quanti biglietti interi sono stati venduti?" % (n, a, b, tot), num(x), W(num(n - x), num(tot // a) if tot // a != x else None, num(x + 1), num((tot - b * n) // a) if (tot - b * n) // a != x else None),
                 "%dx + %d(%d − x) = %d → %dx = %d → <b>x = %d</b>." % (a, b, n, tot, a - b, tot - b * n, x))
    pr = R.randint(2, 30) * 10
    sc = R.choice([10, 20, 25, 30, 40])
    if pr * sc % 100:
        return None
    fin = pr * (100 - sc) // 100
    return M("Dopo uno sconto del %d%% un paio di scarpe costa %d €. Quanto costava prima?" % (sc, fin), "%d €" % pr, W("%d €" % (fin + fin * sc // 100) if fin + fin * sc // 100 != pr else None, "%d €" % (fin + sc), "%d €" % (fin * 100 // sc) if fin * 100 % sc == 0 else None, "%d €" % (pr + 10)),
             "x − %d/100 · x = %d → %d/100 · x = %d → <b>x = %d €</b>." % (sc, fin, 100 - sc, fin, pr))


def main():
    seen = set()
    sets = [
        ("Dalle parole all’equazione", mix(R, seen, [(s1_tradurre, 20)])),
        ("Problemi sui numeri", mix(R, seen, [(s2_numeri, 20)])),
        ("Problemi sull’età", mix(R, seen, [(s3_eta, 20)])),
        ("Problemi di geometria", mix(R, seen, [(s4_geo, 20)])),
        ("Problemi con il denaro", mix(R, seen, [(s5_soldi, 20)])),
    ]
    body = L(["1. Leggi bene e scegli l’<b>incognita</b> x (di solito ciò che il problema chiede o la quantità più piccola).",
              "2. Esprimi le altre quantità con x (il doppio: 2x; 5 in più: x + 5).",
              "3. Scrivi l’<b>equazione</b> usando la relazione data (la somma, il perimetro, il totale…).",
              "4. Risolvi, <b>verifica</b> e rispondi alla domanda (a volte bisogna calcolare anche le altre quantità)."],
             [("La somma di due numeri consecutivi è 45", ["x + (x + 1) = 45", "2x = 44"], "x = 22 e 23")],
             [["«Il triplo di un numero aumentato di 5» = 3(x + 5)", "È 3x + 5: prima il triplo, poi si aggiunge 5."],
              ["Fermarsi a x", "Se si chiede il lato maggiore, calcolalo dopo aver trovato x."],
              ["Dimenticare le unità di misura", "Scrivi la risposta con cm, €, anni…"]],
             table(["Frase", "In simboli"], [["il doppio di un numero", "2x"], ["un numero aumentato di 5", "x + 5"], ["il numero successivo", "x + 1"], ["la metà di un numero", "x/2"]]))
    faq = [("Quale quantità conviene chiamare x?", "Di solito quella da cui dipendono le altre (la più piccola o quella «di riferimento»): così le altre si scrivono senza frazioni."),
           ("Come si verifica la soluzione di un problema?", "Si controlla che i numeri trovati rispettino tutte le condizioni del testo, non solo l’equazione.")]
    unit(G, R, "problemi-con-le-equazioni", "P",
         "Esplorare e risolvere problemi utilizzando equazioni di primo grado",
         "Problemi con le equazioni", "Problemi con le equazioni",
         "Schede di matematica per la terza media sui problemi risolti con le equazioni di primo grado: tradurre le frasi, problemi sui numeri, sull’età, di geometria e con il denaro. 100 esercizi con soluzioni.",
         "Incognita → equazione → soluzione → verifica.", "Rispondi sempre alla domanda del problema.",
         body, faq, sets, 6)


if __name__ == "__main__":
    main()
