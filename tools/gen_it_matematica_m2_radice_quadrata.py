# -*- coding: utf-8 -*-
"""
Italia Matematica seconda media: La radice quadrata (Numeri)
  python3 tools/gen_it_matematica_m2_radice_quadrata.py
Quadrati perfetti, radice quadrata come operazione inversa del quadrato, radice esatta e approssimata (per difetto e
per eccesso), radice di un prodotto e di un quoziente, radice di una frazione, numeri irrazionali, problemi con i quadrati.
Errori: √(a + b) = √a + √b, confondere la radice con la metà, approssimare per eccesso quando si chiede per difetto.
"""
import math
import random
from fractions import Fraction as Fr
from it_media import M, L, unit, mix, table, W, num, fq, d, dk, FOIS, DIV, fr

R = random.Random(71202)
G = "seconda-media"


def s1_esatta():
    n = R.randint(2, 30)
    sq = n * n
    if R.random() < 0.6:
        return M("Quanto fa √%s?" % num(sq), str(n), W(sq // 2, n + 1, n - 1, n * 2 if n * 2 != sq // 2 else None), "%d × %d = %s, quindi √%s = <b>%d</b>." % (n, n, num(sq), num(sq), n))
    return M("Quanto fa %d²?" % n, num(sq), W(num(2 * n), num(sq + n), num((n + 1) ** 2)), "%d × %d = <b>%s</b>." % (n, n, num(sq)))


def s1_perfetto():
    cands = sorted(set([R.randint(2, 30) ** 2] + [R.randint(10, 900) for _ in range(5)]))
    sq = [x for x in cands if int(math.isqrt(x)) ** 2 == x]
    non = [x for x in cands if x not in sq]
    if len(sq) != 1 or len(non) < 3:
        return None
    x = sq[0]
    return M("Quale di questi numeri è un quadrato perfetto: %s?" % ", ".join(num(c) for c in sorted([x] + non[:3])), num(x), [num(c) for c in non[:3]],
             "%s = %d², gli altri no: <b>%s</b>." % (num(x), math.isqrt(x), num(x)))


def s2_appross():
    n = R.randint(5, 900)
    r = math.isqrt(n)
    if r * r == n:
        return None
    k = R.choice(["difetto", "eccesso", "decimi"])
    if k == "difetto":
        return M("Qual è la radice quadrata di %s approssimata all’unità per difetto?" % num(n), str(r), W(r + 1, n // 2, r - 1), "%d² = %d &lt; %s &lt; %d² = %d: <b>%d</b>." % (r, r * r, num(n), r + 1, (r + 1) ** 2, r))
    if k == "eccesso":
        return M("Qual è la radice quadrata di %s approssimata all’unità per eccesso?" % num(n), str(r + 1), W(r, r + 2, n // 2), "%d² &lt; %s &lt; %d²: per eccesso <b>%d</b>." % (r, num(n), r + 1, r + 1))
    v = math.sqrt(n)
    t = int(v * 10) / 10.0
    return M("√%s ≈ ? (approssimata ai decimi per difetto)" % num(n), dk(Fr(int(v * 10), 10), 1), W(dk(Fr(int(v * 10) + 1, 10), 1), dk(Fr(n, 2), 1) if n < 100 else str(r), dk(Fr(int(v * 10) - 1, 10), 1)),
             "%s² = %s &lt; %s &lt; %s² = %s." % (dk(Fr(int(v * 10), 10), 1), d(Fr(int(v * 10), 10) ** 2), num(n), dk(Fr(int(v * 10) + 1, 10), 1), d(Fr(int(v * 10) + 1, 10) ** 2)))


def s3_prop():
    k = R.choice(["prod", "quoz", "fraz", "somma"])
    if k == "prod":
        a, b = R.choice([4, 9, 16, 25, 36, 49]), R.choice([4, 9, 16, 25, 36])
        return M("Calcola con le proprietà: √(%d × %d)" % (a, b), str(math.isqrt(a * b)), W(a + b, math.isqrt(a) + math.isqrt(b), a * b // 2), "√%d × √%d = %d × %d = <b>%d</b>." % (a, b, math.isqrt(a), math.isqrt(b), math.isqrt(a * b)))
    if k == "quoz":
        a, b = R.choice([(144, 4), (400, 16), (900, 25), (196, 4), (324, 9), (256, 16), (225, 9)])
        return M("Calcola: √(%d : %d)" % (a, b), str(math.isqrt(a // b)), W(a // b, math.isqrt(a) - math.isqrt(b), math.isqrt(a // b) + 1), "√%d : √%d = %d : %d = <b>%d</b>." % (a, b, math.isqrt(a), math.isqrt(b), math.isqrt(a // b)))
    if k == "fraz":
        a, b = R.randint(1, 9), R.randint(2, 12)
        if a >= b or math.gcd(a, b) != 1:
            return None
        return M("Calcola: √(%s)" % fr(a * a, b * b), fr(a, b), W(fr(a * a, b), fr(a, b * b), fr(a * a // 2 or 1, b * b // 2)), "√%d / √%d = <b>%d/%d</b>." % (a * a, b * b, a, b))
    a, b = R.choice([(9, 16), (36, 64), (25, 144), (64, 36), (144, 81)])
    s = math.isqrt(a + b) if math.isqrt(a + b) ** 2 == a + b else None
    if s is None:
        return None
    return M("Quanto fa √(%d + %d)?" % (a, b), str(s), W(math.isqrt(a) + math.isqrt(b), a + b, s + 1), "Prima la somma: %d + %d = %d; √%d = <b>%d</b> (non %d + %d!)." % (a, b, a + b, a + b, s, math.isqrt(a), math.isqrt(b)))


def s4_irraz():
    q, a, w = R.choice([("√2 è un numero…", "irrazionale (infinite cifre non periodiche)", ["intero", "periodico", "decimale limitato"]),
                        ("Quale di questi è un numero irrazionale?", "√7", ["√49", "0,<span class='ov'>7</span>", "7/9"]),
                        ("Quale di questi è un numero razionale?", "√64", ["√3", "√5", "√10"]),
                        ("Tra quali interi consecutivi è compresa √50?", "7 e 8", ["6 e 7", "8 e 9", "25 e 26"]),
                        ("Tra quali interi consecutivi è compresa √20?", "4 e 5", ["3 e 4", "5 e 6", "10 e 11"]),
                        ("La radice quadrata di un numero naturale che non è un quadrato perfetto è…", "un numero irrazionale", ["un numero periodico", "sempre un intero", "un decimale limitato"]),
                        ("√0 = ?", "0", ["1", "non esiste", "10"]), ("√1 = ?", "1", ["0", "2", "non esiste"])])
    return M(q, a, w, "Risposta: <b>%s</b>." % a)


def s5():
    k = R.choice(["lato", "tappeto", "piastrelle", "giardino"])
    n = R.randint(4, 30)
    if k == "lato":
        return M("Un quadrato ha l’area di %s cm². Quanto misura il lato?" % num(n * n), "%d cm" % n, W("%d cm" % (n * n // 2), "%d cm" % (n * n // 4) if n * n % 4 == 0 else "%d cm" % (n + 1), "%d cm" % (n * 2)),
                 "lato = √area = √%s = <b>%d cm</b>." % (num(n * n), n))
    if k == "tappeto":
        return M("Un tappeto quadrato ha l’area di %s dm². Qual è il suo perimetro?" % num(n * n), "%d dm" % (4 * n), W("%d dm" % n, "%d dm" % (n * n // 4) if n * n % 4 == 0 else "%d dm" % (4 * n + 4), "%d dm" % (2 * n)),
                 "Lato = √%s = %d dm; perimetro = 4 × %d = <b>%d dm</b>." % (num(n * n), n, n, 4 * n))
    if k == "piastrelle":
        return M("Per coprire un pavimento quadrato servono %s piastrelle quadrate uguali. Quante piastrelle ci sono su ogni lato?" % num(n * n), str(n), W(n * n // 4 if n * n % 4 == 0 else n + 2, n * 2, n + 1),
                 "√%s = <b>%d</b>." % (num(n * n), n))
    return M("Un giardino quadrato ha la stessa area di un rettangolo di %d m × %d m. Quanto misura il lato del giardino?" % (4 * n, n), "%d m" % (2 * n), W("%d m" % (5 * n // 2) if n % 2 == 0 else "%d m" % (5 * n), "%d m" % (4 * n * n // 2), "%d m" % n),
             "Area: %d × %d = %s m²; lato = √%s = <b>%d m</b>." % (4 * n, n, num(4 * n * n), num(4 * n * n), 2 * n))


def main():
    seen = set()
    sets = [
        ("Quadrati e radici esatte", mix(R, seen, [(s1_esatta, 14), (s1_perfetto, 6)])),
        ("Radici approssimate", mix(R, seen, [(s2_appross, 20)])),
        ("Proprietà delle radici", mix(R, seen, [(s3_prop, 20)])),
        ("Numeri irrazionali e stime", mix(R, seen, [(s4_irraz, 8), (s2_appross, 12)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = L(["La <b>radice quadrata</b> di un numero è il numero che, elevato al quadrato, dà il numero dato: √49 = 7 perché 7² = 49. È l’operazione inversa dell’elevamento al quadrato.",
              "I numeri come 1, 4, 9, 16, 25… sono <b>quadrati perfetti</b>: hanno radice esatta. Per gli altri si trova una radice <b>approssimata</b> per difetto o per eccesso: 6² = 36 &lt; 40 &lt; 49 = 7², quindi 6 &lt; √40 &lt; 7.",
              "Proprietà: √(a × b) = √a × √b e √(a : b) = √a : √b. Attenzione: √(a + b) <b>non</b> è √a + √b.",
              "La radice di un numero naturale che non è un quadrato perfetto è un numero <b>irrazionale</b>: ha infinite cifre decimali non periodiche."],
             [("√(16 × 25)", ["√16 × √25", "4 × 5"], "20")],
             [["√(9 + 16) = 3 + 4 = 7", "Prima la somma: √25 = 5."],
              ["Pensare che √36 = 18", "La radice non è la metà: 6 × 6 = 36."],
              ["Dare per difetto un numero troppo grande", "Per difetto il quadrato deve essere minore del numero."]],
             table(["n", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], [["n²"] + [str(i * i) for i in range(1, 11)]]))
    faq = [("Esiste la radice quadrata di un numero negativo?", "Non tra i numeri studiati alle medie: il quadrato di un numero non è mai negativo."),
           ("Come si calcola una radice con le tavole numeriche?", "Si cerca il numero nella colonna n e si legge il valore nella colonna √n; per i numeri grandi si usa la scomposizione in fattori.")]
    unit(G, R, "radice-quadrata", "N",
         "Conoscere la radice quadrata come operatore inverso dell’elevamento al quadrato; dare stime della radice quadrata utilizzando solo la moltiplicazione; sapere che non si può trovare una frazione o un decimale che elevato al quadrato dà 2",
         "La radice quadrata: esatta e approssimata", "Radice quadrata",
         "Schede di matematica per la seconda media sulla radice quadrata: quadrati perfetti, radice esatta e approssimata per difetto e per eccesso, proprietà, numeri irrazionali e problemi. 100 esercizi con soluzioni.",
         "√49 = 7 perché 7² = 49.", "√(a + b) non è √a + √b.",
         body, faq, sets, 2)


if __name__ == "__main__":
    main()
