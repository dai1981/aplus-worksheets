# -*- coding: utf-8 -*-
"""
Italia Matematica classe terza: L’orologio e il tempo (Misure)
  python3 tools/gen_it_matematica_c3_orologio_e_tempo.py
Leggere l’orologio a lancette, «e un quarto», «e mezza», «meno un quarto», ore del pomeriggio (da 0 a 24),
ore, minuti e secondi, giorni, settimane, mesi, durata di un’attività, problemi.
Errori: scambiare lancetta delle ore e dei minuti, 1 h = 100 min, contare le durate come numeri normali (9:50 → 10:10 = 60 min).
"""
import random
from it_common import mcq, lesson, make_unit, mix, Kids, orologio, ora, dur, FOIS, DIV

R = random.Random(70316)
K = Kids(R)
ORE = ["l’una", "le due", "le tre", "le quattro", "le cinque", "le sei", "le sette", "le otto", "le nove", "le dieci", "le undici", "mezzogiorno"]
MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]
GIORNI_M = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
SETT = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]


def s1():
    h = R.randint(1, 12)
    m = R.choice([0, 15, 30, 45, 5, 10, 20, 25, 35, 40, 50, 55])
    if R.random() < 0.4:
        m = R.choice([0, 15, 30, 45])
    sh, sm = (m // 5 if m else 12), (h % 12) * 5
    wr = [ora(sh, sm) if (sh, sm) != (h, m) else None, ora(h % 12 + 1, m), ora(h - 1 if h > 1 else 12, m), ora(h, (m + 30) % 60)]
    return mcq(orologio(h, m) + "Che ore sono (di mattina o di sera)?", ora(h, m), [w for w in wr if w and w != ora(h, m)],
               "La lancetta corta indica le ore, quella lunga i minuti (ogni numero vale 5 minuti). %s<b>%s</b>." % ("È l’" if h == 1 else "Sono le ", ora(h, m)))


def s2_parole():
    h = R.randint(2, 11)
    k = R.choice(["quarto", "mezza", "meno", "meno"])
    w = ORE[h - 1]
    if k == "quarto":
        return mcq("Sono %s e un quarto. Come si scrive?" % w, ora(h, 15), [ora(h, 25), ora(h, 45), ora(h - 1, 45)],
                   "E un quarto = 15 minuti dopo l’ora: <b>%s</b>." % ora(h, 15))
    if k == "mezza":
        return mcq("Sono %s e mezza. Come si scrive?" % w, ora(h, 30), [ora(h, 50), ora(h - 1, 30), ora(h, 15)],
                   "E mezza = 30 minuti dopo l’ora: <b>%s</b>." % ora(h, 30))
    return mcq("Sono %s meno un quarto. Come si scrive?" % w, ora(h - 1, 45), [ora(h, 45), ora(h, 15), ora(h - 1, 15)],
               "Meno un quarto = 15 minuti prima delle %d: <b>%s</b>." % (h, ora(h - 1, 45)))


POM = ["La lezione di nuoto comincia", "La merenda è", "La biblioteca apre", "La partita di pallavolo comincia"]
SERA = ["La cena è", "Lo spettacolo comincia", "Il treno arriva", "Il cartone animato comincia"]


def s2_pomeriggio():
    h = R.randint(1, 10)
    m = R.choice([0, 0, 15, 30, 45, 20, 40])
    ev, lab = (R.choice(POM), "del pomeriggio") if h <= 5 else (R.choice(SERA), "di sera")
    return mcq("%s alle %s %s. Come si scrive con le ore da 0 a 24?" % (ev, ora(h, m), lab), ora(h + 12, m), [ora(h + 10, m), ora(h, m), ora(h + 2, m)],
               "Il pomeriggio e la sera si aggiunge 12: %d + 12 = %d. Sono le <b>%s</b>." % (h, h + 12, ora(h + 12, m)))


def s3():
    k = R.choice(["h_min", "hm_min", "min_hm", "mezz", "quarto", "giorno", "sett", "min_s", "mesi", "anno"])
    if k == "h_min":
        a = R.randint(2, 5)
        return mcq("Quanti minuti ci sono in %d ore?" % a, "%d min" % (a * 60), ["%d min" % (a * 100), "%d min" % (a * 10), "%d min" % (a * 60 + 60)],
                   "1 h = 60 min, quindi %d h = %d %s 60 = <b>%d min</b>." % (a, a, FOIS, a * 60))
    if k == "hm_min":
        a, b = R.randint(1, 3), R.choice([5, 10, 15, 20, 25, 30, 40, 45, 50])
        return mcq("Completa: %s = … min" % dur(a * 60 + b), "%d min" % (a * 60 + b), ["%d min" % (a * 100 + b), "%d min" % (a + b), "%d min" % (a * 10 + b)],
                   "%d h = %d min; %d + %d = <b>%d min</b>." % (a, a * 60, a * 60, b, a * 60 + b))
    if k == "min_hm":
        n = R.choice([70, 75, 80, 90, 100, 110, 125, 135, 150, 165])
        return mcq("Completa: %d min = … h … min" % n, dur(n),
                   ["%d h %d min" % (n // 100, n % 100) if n >= 100 and 0 < n % 100 < 60 else dur(n + 10), "%d h %d min" % (n // 60 + 1, n % 60) if n % 60 else "%d h" % (n // 60 + 1), dur(n - 5)],
                   "60 min = 1 h. %d min = %d min + %d min = <b>%s</b>." % (n, (n // 60) * 60, n % 60, dur(n)))
    if k == "mezz":
        a = R.randint(1, 4)
        return mcq("Quanti minuti sono %s e mezza?" % ("un’ora" if a == 1 else "%d ore" % a), "%d min" % (a * 60 + 30), ["%d min" % (a * 60 + 50), "%d min" % (a * 100 + 50), "%d min" % (a * 60 + 15)],
                   "Mezz’ora = 30 min. %d %s 60 + 30 = <b>%d min</b>." % (a, FOIS, a * 60 + 30))
    if k == "quarto":
        n = R.choice([1, 3])
        return mcq("Quanti minuti sono %s d’ora?" % ("un quarto" if n == 1 else "tre quarti"), "%d min" % (15 * n), ["%d min" % (25 * n), "%d min" % (4 * n), "%d min" % (15 * n + 15)],
                   "Un’ora = 60 min; un quarto d’ora = 60 %s 4 = 15 min%s. Risposta: <b>%d min</b>." % (DIV, "" if n == 1 else "; 3 %s 15 = 45" % FOIS, 15 * n))
    if k == "giorno":
        a = R.randint(2, 4)
        return mcq("Quante ore ci sono in %d giorni?" % a, "%d h" % (a * 24), ["%d h" % (a * 12), "%d h" % (a * 60), "%d h" % (a * 24 + 24)],
                   "1 giorno = 24 h, quindi %d %s 24 = <b>%d h</b>." % (a, FOIS, a * 24))
    if k == "sett":
        a = R.randint(2, 6)
        return mcq("Quanti giorni ci sono in %d settimane?" % a, "%d giorni" % (a * 7), ["%d giorni" % (a * 5), "%d giorni" % (a * 10), "%d giorni" % (a + 7)],
                   "1 settimana = 7 giorni: %d %s 7 = <b>%d giorni</b>." % (a, FOIS, a * 7))
    if k == "mesi":
        i = R.randrange(12)
        if i == 1:
            return None
        g = GIORNI_M[i]
        return mcq("Quanti giorni ha il mese di %s?" % MESI[i], str(g), [str(61 - g), "28", "32", "29"],
                   "%s ha <b>%d</b> giorni (puoi contarli con le nocche della mano)." % (MESI[i].capitalize(), g))
    if k == "anno":
        a = R.randint(2, 4)
        return mcq("Quanti mesi ci sono in %d anni?" % a, "%d mesi" % (a * 12), ["%d mesi" % (a * 10), "%d mesi" % (a * 7), "%d mesi" % (a + 12)],
                   "1 anno = 12 mesi: %d %s 12 = <b>%d mesi</b>." % (a, FOIS, a * 12))
    a = R.randint(2, 5)
    return mcq("Quanti secondi ci sono in %d minuti?" % a, "%d s" % (a * 60), ["%d s" % (a * 100), "%d s" % (a * 10), "%d s" % (a * 60 + 60)],
               "1 min = 60 s, quindi %d %s 60 = <b>%d s</b>." % (a, FOIS, a * 60))


def s4():
    h1 = R.randint(8, 16)
    m1 = R.choice([0, 10, 15, 20, 30, 40, 45])
    d = R.choice([20, 25, 35, 40, 45, 50, 75, 80, 90, 105, 110, 135, 150])
    h2, m2 = divmod(h1 * 60 + m1 + d, 60)
    wr = [dur(d + 40) if m2 < m1 else dur(d + 10), dur(abs((h2 - h1) * 100 + m2 - m1)) if (h2 - h1) * 100 + m2 - m1 > 0 else None, dur(d - 5), dur(d + 60)]
    q = ("Un film comincia alle %s e finisce alle %s. Quanto dura?" % (ora(h1, m1), ora(h2, m2)) if d >= 75 else
         "La lezione di nuoto comincia alle %s e finisce alle %s. Quanto dura?" % (ora(h1, m1), ora(h2, m2)))
    return mcq(q, dur(d), [w for w in wr if w and w != dur(d)],
               "Dalle %s alle %s passano <b>%s</b>. Conta prima fino all’ora esatta, poi il resto." % (ora(h1, m1), ora(h2, m2), dur(d)))


def s5():
    p = K.next()
    k = R.choice(["fine", "inizio", "torta", "viaggio", "data", "giorno"])
    if k in ("fine", "torta"):
        h1, m1 = R.randint(8, 17), R.choice([0, 5, 15, 20, 30, 35, 45, 50])
        d = R.choice([25, 35, 40, 45, 50, 55, 70, 85, 95])
        h2, m2 = divmod(h1 * 60 + m1 + d, 60)
        q = ("%s comincia i compiti alle %s e lavora per %s. A che ora finisce?" % (p[0], ora(h1, m1), dur(d)) if k == "fine" else
             "Una torta va in forno alle %s e cuoce per %s. A che ora si deve togliere?" % (ora(h1, m1), dur(d)))
        bad = ora(h2 - 1, m2) if h2 > h1 else ora(h2, (m2 + 20) % 60)
        return mcq(q, ora(h2, m2), [bad, ora(h2 + 1, m2), ora(h2, (m2 + 10) % 60)], "%s + %s = <b>%s</b>." % (ora(h1, m1), dur(d), ora(h2, m2)))
    if k == "inizio":
        h2, m2 = R.randint(10, 18), R.choice([0, 10, 15, 30, 45])
        d = R.choice([30, 45, 50, 75, 90, 105, 120])
        h1, m1 = divmod(h2 * 60 + m2 - d, 60)
        return mcq("La partita finisce alle %s ed è durata %s. A che ora è cominciata?" % (ora(h2, m2), dur(d)), ora(h1, m1),
                   [ora(*divmod(h2 * 60 + m2 + d, 60)), ora(h1 + 1, m1), ora(h1, (m1 + 30) % 60)],
                   "Torna indietro di %s: %s − %s = <b>%s</b>." % (dur(d), ora(h2, m2), dur(d), ora(h1, m1)))
    if k == "viaggio":
        a, b = R.choice([15, 20, 25, 30, 35]), R.choice([10, 15, 20, 25, 40, 45])
        return mcq("%s va a piedi alla stazione in %d min, poi prende il treno per %d min. Quanto dura il viaggio?" % (p[0], a, b), dur(a + b),
                   [dur(a + b + 40) if a + b >= 60 else dur(a + b + 10), "1 h %d min" % (a + b) if a + b < 60 else dur(a + b - 10), dur(abs(a - b)) if a != b else dur(a + b + 5)],
                   "%d + %d = %d min = <b>%s</b>." % (a, b, a + b, dur(a + b)))
    if k == "data":
        d, n = R.randint(1, 18), R.randint(3, 10)
        mese = R.choice(["marzo", "maggio", "giugno", "ottobre"])
        return mcq("Oggi è il %d %s. La gita è fra %d giorni. Che giorno sarà?" % (d, mese, n), "il %d %s" % (d + n, mese),
                   ["il %d %s" % (d + n - 1, mese), "il %d %s" % (d + n + 1, mese), "il %d %s" % (n, mese) if n != d + n else "il %d %s" % (d, mese)],
                   "%d + %d = %d: <b>il %d %s</b>." % (d, n, d + n, d + n, mese))
    i = R.randrange(7)
    n = R.randint(2, 12)
    j = (i + n) % 7
    return mcq("Oggi è %s. Che giorno della settimana sarà fra %d giorni?" % (SETT[i], n), SETT[j],
               [SETT[(j + 1) % 7], SETT[(j - 1) % 7], SETT[(i + n + 2) % 7]],
               "Ogni 7 giorni torna lo stesso giorno. Conta %d giorni dopo %s: <b>%s</b>." % (n, SETT[i], SETT[j]))


def main():
    seen = set()
    sets = [
        ("Leggere l’orologio", mix(R, seen, [(s1, 20)])),
        ("E un quarto, e mezza, pomeriggio", mix(R, seen, [(s2_parole, 10), (s2_pomeriggio, 10)])),
        ("Ore, minuti, giorni e mesi", mix(R, seen, [(s3, 20)])),
        ("Quanto dura?", mix(R, seen, [(s4, 20)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Nell’orologio a lancette la <b>lancetta corta</b> indica le ore, la <b>lancetta lunga</b> i minuti. Ogni numero vale 5 minuti.",
         "«E un quarto» = 15 minuti, «e mezza» = 30 minuti, «meno un quarto» = 15 minuti prima dell’ora.",
         "Un giorno ha 24 ore. Dopo mezzogiorno si può contare da 13 a 24: le 3 del pomeriggio sono le 15:00.",
         "1 h = 60 min, 1 min = 60 s. Per una <b>durata</b> conta prima fino all’ora esatta e poi aggiungi il resto."],
        [("Dalle 9:40 alle 11:15 quanto passa?", ["9:40 → 10:00 = 20 min", "10:00 → 11:00 = 1 h", "11:00 → 11:15 = 15 min"], "1 h 35 min")],
        [["Scambiare le due lancette", "La lancetta corta indica le ore; la lunga i minuti."],
         ["1 h = 100 min", "Un’ora ha 60 minuti."],
         ["Da 9:50 a 10:10 = 60 min", "Conta fino alle 10:00 (10 min) e poi 10 min: 20 min."]],
        orologio(9, 45))
    faq = [("Come si dicono le ore del pomeriggio?", "Si può dire «le 3 del pomeriggio» oppure «le 15». Per passare da una forma all’altra si aggiunge o si toglie 12."),
           ("Come si calcola quanto dura un’attività?", "Si parte dall’ora di inizio, si arriva all’ora esatta successiva e poi si aggiungono le ore e i minuti che mancano alla fine.")]
    make_unit(R, "orologio-e-tempo", "M",
              "Leggere l’orologio; misurare il tempo con unità convenzionali (ore, minuti, secondi, giorni, settimane, mesi); calcolare la durata di semplici eventi",
              "L’orologio e la misura del tempo", "Orologio e tempo",
              "Schede di matematica per la classe terza sull’orologio e il tempo: leggere l’orologio, e un quarto e mezza, ore del pomeriggio, ore e minuti, giorni e mesi, durate e problemi. 100 esercizi con soluzioni.",
              "La lancetta corta indica le ore, la lunga i minuti.", "1 ora = 60 minuti.",
              body, faq, sets, 16)


if __name__ == "__main__":
    main()
