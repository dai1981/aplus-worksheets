# -*- coding: utf-8 -*-
"""
Italia Matematica prima media: Le potenze e le loro proprietà (Numeri)
  python3 tools/gen_it_matematica_m1_potenze.py
Potenza come prodotto di fattori uguali, casi particolari (esponente 0 e 1, base 0, 1 e 10), proprietà delle potenze
(prodotto e quoziente di potenze con la stessa base, potenza di potenza, prodotto e quoziente con lo stesso esponente),
notazione scientifica e ordine di grandezza, quadrati e cubi.
Errori: 3⁴ = 12, sommare gli esponenti nella potenza di potenza, applicare le proprietà a basi diverse con esponenti diversi.
"""
import random
from it_media import M, L, unit, mix, table, W, num, FOIS, DIV, Kids
import gen_it_matematica_c5_potenze as P5

R = random.Random(71104)
G = "prima-media"
pw = P5.pw


def s1_calc():
    return P5.calc(R.randint(2, 12), 2) if R.random() < 0.4 else P5.calc(R.randint(2, 6), 3) if R.random() < 0.6 else P5.calc(R.choice([2, 3]), R.randint(4, 7))


def s1_casi():
    b = R.randint(2, 30)
    k = R.choice(["zero", "uno", "base1", "base0", "dieci"])
    if k == "zero":
        return M("Quanto fa %s?" % pw(b, 0), "1", W(0, b, 10), "Ogni numero diverso da 0 con esponente 0 dà <b>1</b>.")
    if k == "uno":
        return M("Quanto fa %s?" % pw(b, 1), str(b), W(1, 0, b * b), "Con esponente 1 il risultato è la base: <b>%d</b>." % b)
    if k == "base1":
        e = R.randint(5, 50)
        return M("Quanto fa %s?" % pw(1, e), "1", W(e, 0, 10), "1 moltiplicato per sé stesso resta sempre <b>1</b>.")
    if k == "base0":
        e = R.randint(2, 20)
        return M("Quanto fa %s?" % pw(0, e), "0", W(1, e, 10), "0 moltiplicato per sé stesso dà sempre <b>0</b>.")
    e = R.randint(2, 8)
    return M("Quanto fa %s?" % pw(10, e), num(10 ** e), W(num(10 * e), num(10 ** (e - 1)), num(10 ** (e + 1))), "1 seguito da %d zeri: <b>%s</b>." % (e, num(10 ** e)))


def s2_prop():
    a = R.randint(2, 9)
    m, n = R.randint(2, 9), R.randint(2, 9)
    k = R.choice(["prod", "quoz", "pp", "pe", "qe"])
    if k == "prod":
        return M("Scrivi come un’unica potenza: %s %s %s" % (pw(a, m), FOIS, pw(a, n)), pw(a, m + n), W(pw(a, m * n), pw(a * a, m + n), pw(a, abs(m - n)) if m != n else pw(2 * a, m)),
                 "Stessa base: si <b>sommano</b> gli esponenti, %d + %d = %d. <b>%s</b>." % (m, n, m + n, pw(a, m + n)))
    if k == "quoz":
        if m <= n:
            m, n = n + R.randint(1, 4), m
        return M("Scrivi come un’unica potenza: %s %s %s" % (pw(a, m), DIV, pw(a, n)), pw(a, m - n), W(pw(a, m + n), pw(a, m // n) if m % n == 0 and m // n != m - n else pw(1, m - n), pw(a, m * n)),
                 "Stessa base: si <b>sottraggono</b> gli esponenti, %d − %d = %d. <b>%s</b>." % (m, n, m - n, pw(a, m - n)))
    if k == "pp":
        m, n = R.randint(2, 5), R.randint(2, 4)
        return M("Scrivi come un’unica potenza: (%s)%s" % (pw(a, m), str(n).translate(P5.SUP)), pw(a, m * n), W(pw(a, m + n), pw(a * n, m), pw(a, m ** n) if m ** n < 100 else pw(a, m * n + 1)),
                 "Potenza di potenza: si <b>moltiplicano</b> gli esponenti, %d %s %d = %d. <b>%s</b>." % (m, FOIS, n, m * n, pw(a, m * n)))
    b = R.randint(2, 6)
    if a == b:
        return None
    if k == "pe":
        return M("Scrivi come un’unica potenza: %s %s %s" % (pw(a, m), FOIS, pw(b, m)), pw(a * b, m), W(pw(a * b, 2 * m), pw(a + b, m), pw(a, m + m)),
                 "Stesso esponente: si moltiplicano le basi, %d %s %d = %d. <b>%s</b>." % (a, FOIS, b, a * b, pw(a * b, m)))
    return M("Scrivi come un’unica potenza: %s %s %s" % (pw(a * b, m), DIV, pw(b, m)), pw(a, m), W(pw(a, 0), pw(a * b - b, m), pw(a, 2 * m)),
             "Stesso esponente: si dividono le basi, %d %s %d = %d. <b>%s</b>." % (a * b, DIV, b, a, pw(a, m)))


def s3_espr():
    a = R.randint(2, 5)
    m, n, p = R.randint(3, 6), R.randint(2, 5), R.randint(2, 6)
    if m + n <= p:
        return None
    r = m + n - p
    q = "[%s %s %s] %s %s" % (pw(a, m), FOIS, pw(a, n), DIV, pw(a, p))
    v = a ** r
    return M("Calcola con le proprietà: %s" % q, num(v) if v < 10 ** 6 else pw(a, r), W(num(a ** (m * n - p)) if m * n > p and a ** (m * n - p) < 10 ** 6 else None, num(a ** (r + 1)), num(a * r), num(a ** (r - 1)) if r > 1 else "1"),
             "%s %s %s = %s; %s %s %s = %s = <b>%s</b>." % (pw(a, m), FOIS, pw(a, n), pw(a, m + n), pw(a, m + n), DIV, pw(a, p), pw(a, r), num(v)))


def s4_scient():
    k = R.choice(["scrivi", "leggi", "ordine"])
    if k == "scrivi":
        c = R.randint(11, 99)
        e = R.randint(3, 8)
        n = c * 10 ** (e - 1)
        ok = "%s %s %s" % ("%d,%d" % (c // 10, c % 10) if c % 10 else str(c // 10), FOIS, pw(10, e))
        return M("Come si scrive %s in notazione scientifica?" % num(n), ok, W("%d %s %s" % (c, FOIS, pw(10, e - 1)), "%s %s %s" % ("%d,%d" % (c // 10, c % 10) if c % 10 else str(c // 10), FOIS, pw(10, e - 1)), "%s %s %s" % ("%d,%d" % (c // 10, c % 10) if c % 10 else str(c // 10), FOIS, pw(10, e + 1))),
                 "Il primo fattore deve essere tra 1 e 10: la virgola si sposta di %d posti. <b>%s</b>." % (e, ok))
    if k == "leggi":
        c, e = R.randint(2, 9), R.randint(3, 7)
        return M("Quanto vale %d %s %s?" % (c, FOIS, pw(10, e)), num(c * 10 ** e), W(num(c * 10 ** (e - 1)), num(c * 10 ** (e + 1)), num(c * 10 * e)), "%d seguito da %d zeri: <b>%s</b>." % (c, e, num(c * 10 ** e)))
    q, a, w = R.choice([("La distanza Terra-Sole è circa 150 000 000 km. Qual è il suo ordine di grandezza?", pw(10, 8) + " km", [pw(10, 7) + " km", pw(10, 9) + " km", pw(10, 15) + " km"]),
                        ("In Italia vivono circa 59 000 000 persone. In notazione scientifica…", "5,9 %s %s" % (FOIS, pw(10, 7)), ["59 %s %s" % (FOIS, pw(10, 7)), "5,9 %s %s" % (FOIS, pw(10, 6)), "5,9 %s %s" % (FOIS, pw(10, 8))]),
                        ("Un milione si scrive…", pw(10, 6), [pw(10, 5), pw(10, 7), pw(6, 10)]), ("Un miliardo si scrive…", pw(10, 9), [pw(10, 6), pw(10, 12), pw(9, 10)])])
    return M(q, a, w, "Risposta: <b>%s</b>." % a)


def s5():
    return P5.s5() if R.random() < 0.6 else s3_espr()


def main():
    P5.R = R
    P5.K = Kids(R)
    seen = set()
    sets = [
        ("Calcolare le potenze", mix(R, seen, [(s1_calc, 14), (s1_casi, 6)])),
        ("Esponente 0 e 1, base 0, 1 e 10", mix(R, seen, [(s1_casi, 10), (P5.s4_confronta, 10)])),
        ("Le proprietà delle potenze", mix(R, seen, [(s2_prop, 20)])),
        ("Espressioni con le potenze", mix(R, seen, [(s3_espr, 12), (s2_prop, 8)])),
        ("Notazione scientifica e problemi", mix(R, seen, [(s4_scient, 10), (P5.s5, 10)])),
    ]
    body = L(["La <b>potenza</b> a<sup>n</sup> è il prodotto di n fattori uguali ad a: 3<sup>4</sup> = 3 × 3 × 3 × 3 = 81. a è la <b>base</b>, n l’<b>esponente</b>.",
              "a<sup>1</sup> = a; a<sup>0</sup> = 1 (con a ≠ 0); 1<sup>n</sup> = 1; 0<sup>n</sup> = 0; 10<sup>n</sup> = 1 seguito da n zeri.",
              "Stessa base: a<sup>m</sup> × a<sup>n</sup> = a<sup>m+n</sup>; a<sup>m</sup> : a<sup>n</sup> = a<sup>m−n</sup>; (a<sup>m</sup>)<sup>n</sup> = a<sup>m×n</sup>.",
              "Stesso esponente: a<sup>n</sup> × b<sup>n</sup> = (a × b)<sup>n</sup>; a<sup>n</sup> : b<sup>n</sup> = (a : b)<sup>n</sup>.",
              "Notazione scientifica: un numero tra 1 e 10 per una potenza di 10 (3,8 × 10<sup>5</sup>)."],
             [("2<sup>3</sup> × 2<sup>4</sup> : 2<sup>5</sup>", ["2<sup>3+4</sup> = 2<sup>7</sup>", "2<sup>7−5</sup> = 2<sup>2</sup>"], "4")],
             [["Calcolare 3<sup>4</sup> = 12", "Non è 3 × 4: è 3 × 3 × 3 × 3 = 81."],
              ["(2<sup>3</sup>)<sup>2</sup> = 2<sup>5</sup>", "Potenza di potenza: si moltiplicano gli esponenti, 2<sup>6</sup>."],
              ["Usare le proprietà con basi ed esponenti diversi", "2<sup>3</sup> × 5<sup>2</sup> non si può scrivere come un’unica potenza."]],
             table(["Proprietà", "Regola"], [["prodotto, stessa base", "si sommano gli esponenti"], ["quoziente, stessa base", "si sottraggono gli esponenti"], ["potenza di potenza", "si moltiplicano gli esponenti"], ["stesso esponente", "si moltiplicano (dividono) le basi"]]))
    faq = [("Perché a⁰ = 1?", "Per la proprietà del quoziente: a³ : a³ = a⁰, ma un numero diviso per sé stesso dà 1."),
           ("A che cosa serve la notazione scientifica?", "A scrivere in modo breve numeri molto grandi (distanze tra pianeti) o molto piccoli (dimensioni delle cellule).")]
    unit(G, R, "potenze", "N",
         "Utilizzare la notazione usuale per le potenze con esponente intero positivo, consapevoli del significato, e le proprietà delle potenze per semplificare calcoli e notazioni",
         "Le potenze e le loro proprietà", "Potenze",
         "Schede di matematica per la prima media sulle potenze: calcolo, esponente 0 e 1, proprietà delle potenze (prodotto, quoziente, potenza di potenza), espressioni, notazione scientifica e problemi. 100 esercizi con soluzioni.",
         "Stessa base: × somma gli esponenti, : li sottrae.", "Potenza di potenza: si moltiplicano gli esponenti.",
         body, faq, sets, 4)


if __name__ == "__main__":
    main()
