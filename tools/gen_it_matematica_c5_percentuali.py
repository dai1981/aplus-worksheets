# -*- coding: utf-8 -*-
"""
Italia Matematica classe quinta: Le percentuali (Numeri)
  python3 tools/gen_it_matematica_c5_percentuali.py
La percentuale come frazione con denominatore 100, percentuale ↔ frazione ↔ decimale, percentuali di un numero
(10%, 25%, 50%…), sconto e prezzo scontato, aumento, percentuale su un quadrato di 100 quadretti, grafici.
Errori: 25% di 80 = 25, dimenticare di togliere lo sconto, 5% = 0,5.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, Kids, fr, eur, wrap, GREEN, FILL, DIV, FOIS

R = random.Random(70513)
G = "classe-quinta"
K = Kids(R)


def griglia(k):
    s = []
    for i in range(100):
        x, y = i % 10, i // 10
        s.append("<rect x='%d' y='%d' width='18' height='18' fill='%s' stroke='%s' stroke-width='1'/>" % (4 + x * 20, 4 + y * 20, FILL if i < k else "#ffffff", GREEN))
    return wrap(206, 206, "".join(s), "quadrato di 100 quadretti, %d colorati" % k)


def pc(n):
    return "%s%%" % num(n)


def dec2(n):
    """n centesimi → decimale"""
    return "%d,%s" % (n // 100, str(n % 100).rjust(2, "0").rstrip("0")) if n % 100 else num(n // 100)


def s1_griglia():
    k = R.randint(3, 97)
    return mcq(griglia(k) + "Quale percentuale del quadrato è colorata?", pc(k), [pc(100 - k), pc(k * 10 % 100 or k + 1), "%d%%" % (k // 10 if k >= 10 else k + 10)],
               "Su 100 quadretti ne sono colorati %d: %s = <b>%s</b>." % (k, fr(k, 100), pc(k)))


def s1_conv():
    k = R.choice(["pf", "pd", "fp", "dp"])
    p = R.choice([5, 10, 20, 25, 30, 40, 50, 60, 75, 80, 1, 15, 35, 90])
    if k == "pf":
        return mcq("Scrivi %s come frazione con denominatore 100." % pc(p), fr(p, 100), [fr(p, 10), fr(100, p), fr(p, 1000)], "%s vuol dire %d su 100: <b>%s</b>." % (pc(p), p, fr(p, 100)))
    if k == "pd":
        return mcq("Scrivi %s come numero decimale." % pc(p), dec2(p), [dec2(p * 10) if p < 10 else num(p), "%d,%d" % (p // 10, p % 10) if p >= 10 else "0,%d" % p, dec2(p // 10) if p >= 10 and p % 10 == 0 else dec2(p + 1)],
                   "%s = %s = <b>%s</b>." % (pc(p), fr(p, 100), dec2(p)))
    simple = {50: (1, 2), 25: (1, 4), 75: (3, 4), 20: (1, 5), 10: (1, 10), 40: (2, 5), 60: (3, 5), 80: (4, 5), 5: (1, 20)}
    if k == "fp" and p in simple:
        n, d = simple[p]
        return mcq("Quale percentuale è uguale a %s?" % fr(n, d), pc(p), [pc(n * 10 + d) if n * 10 + d != p else pc(p + 5), pc(d), pc(100 // d + 1)],
                   "%s = %s = <b>%s</b>." % (fr(n, d), fr(p, 100), pc(p)))
    return mcq("Quale percentuale è uguale a %s?" % dec2(p), pc(p), [pc(p * 10) if p * 10 <= 1000 else pc(p + 1), pc(p // 10) if p >= 10 else pc(p * 100), pc(p + 10)],
               "%s = %s = <b>%s</b>." % (dec2(p), fr(p, 100), pc(p)))


def s2_di():
    p = R.choice([10, 20, 25, 50, 75, 5, 30, 40, 1, 15])
    base = {1: 100, 5: 20, 10: 10, 15: 20, 20: 5, 25: 4, 30: 10, 40: 5, 50: 2, 75: 4}[p]
    n = base * R.randint(2, 40)
    r = n * p // 100
    return mcq("Quanto fa %s di %s?" % (("l’" if p in (1, 8, 11, 80) else "il ") + pc(p), num(n)), num(r), [num(p), num(n - r), num(n * p // 10) if n * p % 10 == 0 else num(r + 1), num(r * 10)],
               "%s = %s: %s %s 100 %s %d = <b>%s</b>." % (pc(p), fr(p, 100), num(n), DIV, FOIS, p, num(r)))


def s3_sconto():
    p = R.choice([10, 20, 25, 30, 50, 40])
    pr = R.randint(2, 30) * 10 if p != 25 else R.randint(2, 30) * 4
    sc = pr * p // 100
    if R.random() < 0.5:
        return mcq("Un paio di scarpe costa %d €. Lo sconto è del %s. A quanto ammonta lo sconto?" % (pr, pc(p)), "%s €" % num(sc), ["%s €" % num(pr - sc), "%d €" % p, "%s €" % num(sc + 10)],
                   "%s di %d: %d %s 100 %s %d = <b>%s €</b>." % (pc(p), pr, pr, DIV, FOIS, p, num(sc)))
    return mcq("Un gioco costa %d €. Con lo sconto del %s, quanto si paga?" % (pr, pc(p)), "%s €" % num(pr - sc), ["%s €" % num(sc), "%d €" % (pr - p), "%s €" % num(pr - sc + 10)],
               "Sconto: %s €. Prezzo scontato: %d − %s = <b>%s €</b>." % (num(sc), pr, num(sc), num(pr - sc)))


def s3_aumento():
    p = R.choice([10, 20, 5, 50])
    pr = R.randint(2, 12) * 20
    a = pr * p // 100
    return mcq("L’abbonamento della palestra costava %d €; ora costa il %s in più. Quanto costa adesso?" % (pr, pc(p)), "%s €" % num(pr + a), ["%s €" % num(a), "%d €" % (pr + p), "%s €" % num(pr - a)],
               "Aumento: %s di %d = %s €. Nuovo prezzo: %d + %s = <b>%s €</b>." % (pc(p), pr, num(a), pr, num(a), num(pr + a)))


def s4_quale():
    n = R.choice([20, 25, 40, 50, 200, 10])
    k = R.randint(2, n - 1)
    if (k * 100) % n:
        return None
    p = k * 100 // n
    return mcq("%d bambini su %d portano gli occhiali. Che percentuale è?" % (k, n), pc(p), [pc(k), pc(n - k) if n - k != p else pc(p + 5), pc(100 - p) if 100 - p != p else pc(p + 10)],
               "%s = %s: <b>%s</b>." % (fr(k, n), fr(p, 100), pc(p)))


def s5():
    p = K.next()
    k = R.choice(["voti", "sconto2", "succo", "classe", "banca", "torta"])
    if k == "voti":
        n = R.choice([200, 300, 400, 500, 800])
        q = R.choice([40, 45, 55, 60, 35])
        return mcq("A un’elezione dei rappresentanti hanno votato %d alunni. Sofia ha avuto il %s dei voti. Quanti voti ha avuto?" % (n, pc(q)), num(n * q // 100),
                   [num(q), num(n - n * q // 100), num(n * q // 10)], "%d %s 100 %s %d = <b>%s</b>." % (n, DIV, FOIS, q, num(n * q // 100)))
    if k == "sconto2":
        pr = R.randint(3, 11) * 10
        sp = pr * 9 // 10
        return mcq("Al mercato una giacca costa %d €. Il venditore fa il 10%% di sconto e %s paga con 100 €. Quanto riceve di resto?" % (pr, p[0]),
                   "%s €" % num(100 - sp), ["%s €" % num(100 - pr), "%s €" % num(pr // 10), "%s €" % num(100 - sp + 10)],
                   "Prezzo scontato: %d − %d = %d €. Resto: 100 − %d = <b>%d €</b>." % (pr, pr // 10, sp, sp, 100 - sp))
    if k == "succo":
        ml = R.choice([200, 500, 1000, 1500])
        q = R.choice([10, 20, 25, 30])
        return mcq("Una bevanda da %d ml contiene il %s di succo di frutta. Quanti ml di succo contiene?" % (ml, pc(q)), "%s ml" % num(ml * q // 100), ["%d ml" % q, "%s ml" % num(ml - ml * q // 100), "%s ml" % num(ml * q // 10)],
                   "%d %s 100 %s %d = <b>%s ml</b>." % (ml, DIV, FOIS, q, num(ml * q // 100)))
    if k == "classe":
        n = R.choice([20, 25])
        b = R.randint(5, n - 5)
        if (b * 100) % n:
            return None
        return mcq("In una classe di %d alunni, %d sono maschi. Che percentuale sono le femmine?" % (n, b), pc((n - b) * 100 // n), [pc(b * 100 // n), pc(n - b), pc(100 - b)],
                   "Le femmine sono %d su %d: %s = <b>%s</b>." % (n - b, n, fr(n - b, n), pc((n - b) * 100 // n)))
    if k == "banca":
        c = R.choice([100, 200, 500, 1000])
        q = R.choice([1, 2, 3, 5])
        return mcq("La nonna mette %d € in banca. Dopo un anno riceve %s di interesse. Quanti euro ha in tutto?" % (c, ("l’" if q == 1 else "il ") + pc(q)), "%s €" % num(c + c * q // 100),
                   ["%s €" % num(c * q // 100), "%d €" % (c + q), "%s €" % num(c + c * q // 10)], "Interesse: %s €. Totale: %d + %s = <b>%s €</b>." % (num(c * q // 100), c, num(c * q // 100), num(c + c * q // 100)))
    g = R.choice([200, 400, 500, 300])
    q = R.choice([25, 50, 10, 20])
    return mcq("Un impasto pesa %d g; lo zucchero è il %s. Quanti grammi di zucchero ci sono?" % (g, pc(q)), "%s g" % num(g * q // 100), ["%d g" % q, "%s g" % num(g - g * q // 100), "%s g" % num(g * q // 10)],
               "%d %s 100 %s %d = <b>%s g</b>." % (g, DIV, FOIS, q, num(g * q // 100)))


def main():
    seen = set()
    sets = [
        ("Che cos’è la percentuale", mix(R, seen, [(s1_griglia, 10), (s1_conv, 10)])),
        ("Percentuale di un numero", mix(R, seen, [(s2_di, 20)])),
        ("Sconti e aumenti", mix(R, seen, [(s3_sconto, 14), (s3_aumento, 6)])),
        ("Quale percentuale?", mix(R, seen, [(s4_quale, 12), (s1_conv, 8)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["La <b>percentuale</b> indica quante parti su 100: 35%% = %s = 0,35." % fr(35, 100),
         "Per calcolare una percentuale di un numero: dividi per 100 e moltiplica per la percentuale. Il 20% di 150: 150 : 100 × 20 = 30.",
         "Scorciatoie: 50% = metà, 25% = un quarto, 10% = dividi per 10.",
         "<b>Prezzo scontato</b> = prezzo − sconto. Prezzo aumentato = prezzo + aumento."],
        [("Un libro costa 24 € con lo sconto del 25%.", ["25%% = %s: 24 : 4 = 6 €" % fr(1, 4), "24 − 6 = 18 €"], "18 €")],
        [["Il 25% di 80 è 25", "Il 25% è un quarto: 80 : 4 = 20."],
         ["Dimenticare di togliere lo sconto", "La domanda chiede quanto si paga? Fai prezzo − sconto."],
         ["5% = 0,5", "5% = 5 centesimi = 0,05."]],
        griglia(35))
    faq = [("Che cosa vuol dire «per cento»?", "Su cento: il 30% vuol dire 30 parti ogni 100. Il simbolo è %."),
           ("Come si calcola velocemente il 10%?", "Si divide per 10: il 10% di 250 € è 25 €.")]
    make_unit(R, "percentuali", "N",
              "Utilizzare frazioni e percentuali per descrivere situazioni quotidiane; interpretare e calcolare percentuali in contesti concreti (sconti)",
              "Le percentuali: sconti e aumenti", "Percentuali",
              "Schede di matematica per la classe quinta sulle percentuali: percentuale come frazione e numero decimale, percentuale di un numero, sconti, aumenti e problemi. 100 esercizi con soluzioni.",
              "Percentuale = parti su 100.", "Prezzo scontato = prezzo − sconto.",
              body, faq, sets, 13, grade=G)


if __name__ == "__main__":
    main()
