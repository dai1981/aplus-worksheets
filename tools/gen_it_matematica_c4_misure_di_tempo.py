# -*- coding: utf-8 -*-
"""
Italia Matematica classe quarta: Misure di tempo (Misure)
  python3 tools/gen_it_matematica_c4_misure_di_tempo.py
Ore, minuti, secondi; giorni, settimane, mesi, anni, secoli; orario da 0 a 24; durate; calendario; problemi.
Errori: trattare le ore come se valessero 100 minuti, confondere 14:00 con le 4, sbagliare i mesi di 30 e 31 giorni.
"""
import random
from it_common import mcq, lesson, make_unit, mix, table, Kids, FOIS, dur, ora
import gen_it_matematica_c5_misure_ed_equivalenze as MS5
import gen_it_matematica_c3_orologio_e_tempo as O3

R = random.Random(70413)
G = "classe-quarta"
MESI = [("gennaio", 31), ("febbraio", 28), ("marzo", 31), ("aprile", 30), ("maggio", 31), ("giugno", 30), ("luglio", 31), ("agosto", 31),
        ("settembre", 30), ("ottobre", 31), ("novembre", 30), ("dicembre", 31)]


def s4_cal():
    k = R.choice(["giorni", "dopo", "trimestre", "anni", "bisest", "giorni2"])
    if k in ("giorni", "giorni2"):
        m, g = R.choice(MESI[:1] + MESI[2:])
        return mcq("Quanti giorni ha il mese di %s?" % m, str(g), [str(61 - g), "28", "29"] if g != 28 else ["30", "31", "29"],
                   "%s ha <b>%d</b> giorni." % (m.capitalize(), g))
    if k == "dopo":
        i = R.randrange(12)
        n = R.randint(2, 10)
        return mcq("Siamo a %s. Che mese sarà fra %d mesi?" % (MESI[i][0], n), MESI[(i + n) % 12][0], [MESI[(i + n + 1) % 12][0], MESI[(i + n - 1) % 12][0], MESI[(i + n + 3) % 12][0]],
                   "Conta %d mesi dopo %s: <b>%s</b>." % (n, MESI[i][0], MESI[(i + n) % 12][0]))
    if k == "trimestre":
        q, a, w = R.choice([("Quanti mesi ci sono in un trimestre?", "3", ["4", "6", "2"]), ("Quanti mesi ci sono in un semestre?", "6", ["3", "4", "12"]),
                            ("Quanti anni ci sono in un decennio?", "10", ["100", "12", "5"]), ("Quanti anni ci sono in un millennio?", "1000", ["100", "10", "10 000"]),
                            ("Quanti giorni ha un anno bisestile?", "366", ["365", "364", "360"]), ("Quanti mesi ci sono in un bimestre?", "2", ["3", "4", "6"])])
        return mcq(q, a, w, "Risposta: <b>%s</b>." % a)
    if k == "anni":
        a = R.randint(1, 9) * 100 + R.randint(1, 99)
        sec = (a - 1) // 100 + 1
        rom = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI"]
        return mcq("In quale secolo è l’anno %d?" % a, "nel %s secolo" % rom[sec - 1], ["nel %s secolo" % rom[sec - 2] if sec > 1 else "nel II secolo", "nel %s secolo" % rom[sec], "nel %s secolo" % rom[sec + 1]],
                   "Gli anni da %d a %d sono nel %s secolo." % ((sec - 1) * 100 + 1, sec * 100, rom[sec - 1]))
    y = R.choice([2024, 2025, 2026, 2027, 2028, 2030, 2032])
    b = y % 4 == 0
    return mcq("Il %d è un anno bisestile?" % y, "sì, febbraio ha 29 giorni" if b else "no, febbraio ha 28 giorni",
               ["no, febbraio ha 28 giorni" if b else "sì, febbraio ha 29 giorni", "sì, ha 365 giorni", "no, ha 366 giorni"],
               "%d %s divisibile per 4: <b>%s</b>." % (y, "è" if b else "non è", "è bisestile" if b else "non è bisestile"))


def main():
    for m in (MS5, O3):
        m.R = R
        m.K = Kids(R)
    seen = set()
    sets = [
        ("Ore, minuti e secondi", mix(R, seen, [(MS5.s4_tempo, 20)])),
        ("L’orario da 0 a 24", mix(R, seen, [(O3.s2_pomeriggio, 10), (O3.s3, 10)])),
        ("Quanto dura?", mix(R, seen, [(O3.s4, 20)])),
        ("Calendario, anni e secoli", mix(R, seen, [(s4_cal, 20)])),
        ("Problemi", mix(R, seen, [(O3.s5, 20)])),
    ]
    body = lesson(
        ["1 h = 60 min, 1 min = 60 s, 1 giorno = 24 h. Le misure di tempo <b>non</b> sono decimali: un’ora non vale 100 minuti.",
         "1 settimana = 7 giorni, 1 anno = 12 mesi = 365 giorni (366 nell’anno bisestile), 1 secolo = 100 anni.",
         "Nell’orario da 0 a 24, dopo mezzogiorno si aggiunge 12: le 3 del pomeriggio sono le 15:00.",
         "Per calcolare una durata conta prima fino all’ora esatta, poi aggiungi il resto."],
        [("Dalle 9:40 alle 11:15", ["9:40 → 10:00: 20 min", "10:00 → 11:00: 1 h", "11:00 → 11:15: 15 min"], "1 h 35 min")],
        [["Calcolare 11:15 − 9:40 = 1:75", "Le ore hanno 60 minuti: conta a salti."],
         ["Pensare che 2,5 h siano 2 h 50 min", "Mezz’ora sono 30 min: 2 h 30 min."],
         ["Contare 30 giorni per tutti i mesi", "«Trenta giorni ha novembre, con april, giugno e settembre…»."]],
        table(["Unità", "Equivale a"], [["1 minuto", "60 secondi"], ["1 ora", "60 minuti"], ["1 giorno", "24 ore"], ["1 anno", "12 mesi"], ["1 secolo", "100 anni"]]))
    faq = [("Perché un’ora ha 60 minuti e non 100?", "È una divisione molto antica, nata con i Babilonesi, che contavano a gruppi di 60."),
           ("Come si scrivono le ore della sera?", "Con le ore da 0 a 24: le 8 di sera sono le 20:00.")]
    make_unit(R, "misure-di-tempo", "M",
              "Conoscere le misure di tempo (ore, minuti, secondi, giorni, mesi, anni, secoli) ed effettuare equivalenze; calcolare durate",
              "Misure di tempo: ore, minuti, calendario e durate", "Misure di tempo",
              "Schede di matematica per la classe quarta sulle misure di tempo: ore, minuti e secondi, orario da 0 a 24, durate, calendario, anni bisestili e secoli, problemi. 100 esercizi con soluzioni.",
              "1 h = 60 min, 1 min = 60 s.", "Il tempo non è decimale: conta a gruppi di 60.",
              body, faq, sets, 13, grade=G)


if __name__ == "__main__":
    main()
