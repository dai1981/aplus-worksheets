# -*- coding: utf-8 -*-
"""
Italia Matematica seconda media: Rapporti e proporzioni (Relazioni e funzioni)
  python3 tools/gen_it_matematica_m2_rapporti_e_proporzioni.py
Rapporto tra due numeri e tra grandezze (scala, velocità, densità), proporzioni: termini, proprietà fondamentale,
calcolo del termine incognito (estremo, medio, medio proporzionale), proprietà del comporre e dello scomporre, problemi.
Errori: invertire il rapporto, moltiplicare gli estremi tra loro e i medi tra loro in modo sbagliato, dimenticare l’unità di misura.
"""
import math
import random
from fractions import Fraction as Fr
from it_media import M, L, unit, mix, table, W, num, fq, d, FOIS, DIV, Kids

R = random.Random(71203)
G = "seconda-media"
K = Kids(R)


def prop(a, b, c, dd):
    return "%s : %s = %s : %s" % (a, b, c, dd)


def s1_rapporto():
    k = R.choice(["num", "scala", "vel", "classe"])
    if k == "num":
        a, b = R.randint(2, 60), R.randint(2, 60)
        r = Fr(a, b)
        if r.denominator == 1:
            return None
        return M("Qual è il rapporto tra %d e %d (ridotto ai minimi termini)?" % (a, b), fq(r), W(fq(1 / r), fq(Fr(a - b, 1)) if a > b else None, fq(r * 2), fq(Fr(a, b + 1))),
                 "%d : %d = %d/%d = <b>%s</b>." % (a, b, a, b, fq(r)))
    if k == "scala":
        sc = R.choice([100, 200, 500, 1000, 25000, 50000, 100000])
        c = R.randint(2, 15)
        real = c * sc
        u = "cm" if real < 100 else "m" if real < 100000 else "km"
        rv = Fr(real, 1) if u == "cm" else Fr(real, 100) if u == "m" else Fr(real, 100000)
        return M("Su una carta in scala 1 : %s una distanza misura %d cm. Quanto misura nella realtà?" % (num(sc), c), "%s %s" % (d(rv), u), W("%s %s" % (d(rv * 10), u), "%s %s" % (d(rv / 10), u), "%s cm" % num(c + sc)),
                 "%d × %s = %s cm = <b>%s %s</b>." % (c, num(sc), num(real), d(rv), u))
    if k == "vel":
        km, h = R.randint(60, 600), R.choice([2, 3, 4, 5])
        km = km // h * h
        return M("Un’auto percorre %d km in %d ore. Qual è la sua velocità media?" % (km, h), "%d km/h" % (km // h), W("%d km/h" % (km * h), "%d km/h" % (km + h), "%d km/h" % (km // h + 10)),
                 "velocità = spazio : tempo = %d : %d = <b>%d km/h</b>." % (km, h, km // h))
    m, f = R.randint(8, 16), R.randint(8, 16)
    if m == f:
        return None
    return M("In una classe ci sono %d maschi e %d femmine. Qual è il rapporto tra le femmine e tutti gli alunni?" % (m, f), fq(Fr(f, m + f)), W(fq(Fr(f, m)), fq(Fr(m, m + f)), fq(Fr(m + f, f))),
             "%d : %d = <b>%s</b>." % (f, m + f, fq(Fr(f, m + f))))


def s2_verifica():
    a, b = R.randint(2, 12), R.randint(2, 12)
    k = R.randint(2, 6)
    c, dd = a * k, b * k
    ok = R.random() < 0.5
    if not ok:
        dd += R.choice([-1, 1, 2])
    return M("%s è una proporzione?" % prop(a, b, c, dd), "sì" if ok else "no", W("no" if ok else "sì", "solo se i medi sono uguali", "non si può dire"),
             "Prodotto dei medi: %d × %d = %d; prodotto degli estremi: %d × %d = %d. %s." % (b, c, b * c, a, dd, a * dd, "Sono uguali: <b>sì</b>" if ok else "Sono diversi: <b>no</b>"))


def s2_termini():
    a, b, c, dd = 3, 4, 6, 8
    q, ans, w = R.choice([("Nella proporzione 3 : 4 = 6 : 8, quali sono gli estremi?", "3 e 8", ["4 e 6", "3 e 4", "6 e 8"]),
                          ("Nella proporzione 3 : 4 = 6 : 8, quali sono i medi?", "4 e 6", ["3 e 8", "3 e 6", "4 e 8"]),
                          ("La proprietà fondamentale delle proporzioni dice che…", "il prodotto dei medi è uguale al prodotto degli estremi", ["la somma dei medi è uguale alla somma degli estremi", "il rapporto è sempre 1", "i medi sono uguali"]),
                          ("Una proporzione continua ha…", "i medi uguali", ["gli estremi uguali", "tutti i termini uguali", "i rapporti diversi"]),
                          ("In 4 : x = x : 9, x si chiama…", "medio proporzionale", ["estremo", "antecedente", "conseguente"])])
    return M(q, ans, w, "Risposta: <b>%s</b>." % ans)


def s3_incognita():
    a, b = R.randint(2, 15), R.randint(2, 15)
    k = R.randint(2, 6)
    c, dd = a * k, b * k
    pos = R.randrange(4)
    t = [a, b, c, dd]
    x = t[pos]
    shown = [str(v) if i != pos else "x" for i, v in enumerate(t)]
    wrong = [t[(pos + 1) % 4] * t[(pos + 2) % 4] // max(1, t[(pos + 3) % 4]), x + 1, x * 2, x - 1 if x > 1 else x + 2]
    if pos in (0, 3):
        e = "Estremo incognito = prodotto dei medi : estremo noto = %d × %d : %d = <b>%d</b>." % (b, c, t[3 - pos], x)
    else:
        e = "Medio incognito = prodotto degli estremi : medio noto = %d × %d : %d = <b>%d</b>." % (a, dd, t[3 - pos], x)
    return M("Trova x: %s" % prop(*shown), str(x), W(*[v for v in wrong if v != x]), e)


def s3_medio():
    a, b = R.choice([(4, 9), (4, 25), (9, 16), (2, 8), (3, 12), (4, 16), (9, 25), (1, 36), (5, 20), (2, 18)])
    x = math.isqrt(a * b)
    return M("Trova il medio proporzionale: %d : x = x : %d" % (a, b), str(x), W(a * b, (a + b) // 2, x + 1, x * 2, x - 1), "x² = %d × %d = %d; x = √%d = <b>%d</b>." % (a, b, a * b, a * b, x))


def s4_comporre():
    k = R.randint(3, 12)
    a, b = R.randint(1, 7), R.randint(1, 7)
    if a == b or math.gcd(a, b) != 1:
        return None
    s = (a + b) * k
    return M("Due numeri x e y sono tali che x : y = %d : %d e x + y = %d. Quanto vale x?" % (a, b, s), str(a * k), W(b * k, s // 2 if s % 2 == 0 else None, a + k, s - a, k, (a + 1) * k), "Proprietà del comporre: x = %d : (%d + %d) × %d = %d × %d = <b>%d</b>." % (s, a, b, a, k, a, a * k))


def s5():
    p = K.next()
    k = R.choice(["ricetta", "mappa", "soldi", "vernice", "dividere"])
    if k == "ricetta":
        u, g = R.choice([(4, 300), (6, 450), (4, 200), (5, 250)])
        n = R.choice([2, 3, 8, 10, 12])
        if n == u:
            return None
        return M("Una ricetta per %d persone richiede %d g di farina. Quanta farina serve per %d persone?" % (u, g, n), "%s g" % num(g * n // u) if g * n % u == 0 else "%s g" % d(Fr(g * n, u)),
                 W("%d g" % (g + n - u), "%s g" % num(g * u // n) if g * u % n == 0 else "%d g" % (g * 2), "%d g" % (g * n)), "%d : %d = x : %d; x = %d × %d : %d = <b>%s g</b>." % (u, g, n, g, n, u, d(Fr(g * n, u))))
    if k == "mappa":
        a, b = R.randint(2, 12), R.choice([2, 4, 5])
        km = a * b * 5
        return M("Su una mappa 4 cm rappresentano %d km. Quanti km rappresentano %d cm?" % (b * 5, a),
                 "%s km" % d(Fr(a * b * 5, 4)), W("%s km" % d(Fr(a * b * 5, 2)), "%s km" % d(Fr(a * b * 5, 8)), "%d km" % (a * b * 5), "%d km" % (a + b * 5)), "4 : %d = %d : x; x = %d × %d : 4 = <b>%s km</b>." % (b * 5, a, b * 5, a, d(Fr(a * b * 5, 4))))
    if k == "soldi":
        a, b = R.randint(1, 5), R.randint(1, 5)
        if a == b:
            return None
        t = (a + b) * R.randint(5, 30)
        return M("%s e un amico dividono %d € in parti proporzionali a %d e %d. Quanto riceve %s?" % (p[0], t, a, b, p[0]), "%d €" % (t * a // (a + b)), W("%d €" % (t * b // (a + b)), "%d €" % (t // 2), "%d €" % (t * a // (a + b) + a)),
                     "Parte unitaria: %d : (%d + %d) = %d €; %d × %d = <b>%d €</b>." % (t, a, b, t // (a + b), t // (a + b), a, t * a // (a + b)))
    if k == "vernice":
        b, g = R.choice([(3, 2), (5, 3), (4, 1), (2, 1)])
        tot = (b + g) * R.randint(2, 6)
        return M("Per un colore si mescolano bianco e grigio nel rapporto %d : %d. Quanti litri di bianco servono per %d litri di colore?" % (b, g, tot), "%d l" % (tot * b // (b + g)), W("%d l" % (tot * g // (b + g)), "%d l" % (tot // 2), "%d l" % (tot * b // g) if tot * b % g == 0 else "%d l" % (tot - b)),
                     "Comporre: bianco = %d : %d × %d = <b>%d l</b>." % (tot, b + g, b, tot * b // (b + g)))
    a = R.randint(3, 12)
    return M("Il rapporto tra due segmenti è 3/5 e il maggiore misura %d cm. Quanto misura il minore?" % (5 * a), "%d cm" % (3 * a), W("%d cm" % (5 * a * 5 // 3) if 5 * a * 5 % 3 == 0 else "%d cm" % (2 * a), "%d cm" % (8 * a), "%d cm" % (5 * a - 3)), "x : %d = 3 : 5; x = %d × 3 : 5 = <b>%d cm</b>." % (5 * a, 5 * a, 3 * a))


def main():
    seen = set()
    sets = [
        ("Rapporti", mix(R, seen, [(s1_rapporto, 20)])),
        ("Proporzioni e proprietà fondamentale", mix(R, seen, [(s2_verifica, 15), (s2_termini, 5)])),
        ("Termine incognito", mix(R, seen, [(s3_incognita, 16), (s3_medio, 4)])),
        ("Medio proporzionale e comporre", mix(R, seen, [(s3_medio, 6), (s4_comporre, 14)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = L(["Il <b>rapporto</b> tra due numeri a e b (b ≠ 0) è il quoziente a : b. Tra grandezze omogenee è un numero puro (scala); tra grandezze diverse ha un’unità (velocità in km/h).",
              "Una <b>proporzione</b> è l’uguaglianza di due rapporti: a : b = c : d. a e d sono gli <b>estremi</b>, b e c i <b>medi</b>.",
              "<b>Proprietà fondamentale</b>: prodotto dei medi = prodotto degli estremi. Così si trova il termine incognito: estremo = medi moltiplicati : altro estremo; medio = estremi moltiplicati : altro medio.",
              "<b>Comporre</b>: (a + b) : a = (c + d) : c. Serve per dividere una quantità in parti proporzionali."],
             [("x : 12 = 5 : 4", ["x è un estremo", "x = 12 × 5 : 4"], "15")],
             [["Invertire il rapporto: 3 : 5 invece di 5 : 3", "Il primo nominato va sopra (antecedente)."],
              ["Moltiplicare un medio per un estremo", "Si moltiplicano tra loro i medi oppure gli estremi."],
              ["Dimenticare l’unità di misura", "Scala: numero puro; velocità: km/h."]],
             table(["Termine", "In 3 : 4 = 6 : 8"], [["estremi", "3 e 8"], ["medi", "4 e 6"], ["prodotto dei medi", "24"], ["prodotto degli estremi", "24"]]))
    faq = [("Che cosa vuol dire scala 1 : 50 000?", "Che 1 cm sulla carta corrisponde a 50 000 cm nella realtà, cioè 500 m."),
           ("Come si dividono 60 € in parti proporzionali a 2 e 3?", "Si sommano le parti (5), si trova il valore di una parte (60 : 5 = 12 €) e si moltiplica: 24 € e 36 €.")]
    unit(G, R, "rapporti-e-proporzioni", "F",
         "Comprendere il concetto di rapporto; usare le proporzioni e le loro proprietà per risolvere problemi; utilizzare la scala di riduzione",
         "Rapporti e proporzioni", "Rapporti e proporzioni",
         "Schede di matematica per la seconda media su rapporti e proporzioni: rapporto tra numeri e grandezze, scala, proprietà fondamentale, termine incognito, medio proporzionale, comporre e problemi. 100 esercizi con soluzioni.",
         "Prodotto dei medi = prodotto degli estremi.", "Estremo = medi moltiplicati : altro estremo.",
         body, faq, sets, 3)


if __name__ == "__main__":
    main()
