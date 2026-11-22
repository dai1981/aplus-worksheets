# -*- coding: utf-8 -*-
"""
Italia Matematica classe prima: Il tempo (Misure)
  python3 tools/gen_it_matematica_c1_il_tempo.py
Prima, adesso, dopo; ieri, oggi, domani; mattina, pomeriggio, sera, notte; i giorni della settimana;
i mesi e le stagioni; l’orologio: le ore intere.
Errori: confondere ieri e domani, pensare che la settimana cominci dalla domenica, scambiare lancetta corta e lunga.
"""
import random
from it_common import mcq, lesson, make_unit, mix, table, Kids
import gen_it_matematica_c2_orologio_e_calendario as O2

R = random.Random(70111)
G = "classe-prima"
SETT = O2.SETT


def s1_ieri():
    i = R.randrange(7)
    k = R.choice(["ieri", "domani", "ieri2", "domani2"])
    if k == "ieri":
        return mcq("Oggi è %s. Che giorno era ieri?" % SETT[i], SETT[i - 1], [SETT[(i + 1) % 7], SETT[i - 2], SETT[i]], "Ieri è il giorno prima di oggi: <b>%s</b>." % SETT[i - 1])
    if k == "domani":
        return mcq("Oggi è %s. Che giorno sarà domani?" % SETT[i], SETT[(i + 1) % 7], [SETT[i - 1], SETT[(i + 2) % 7], SETT[i]], "Domani è il giorno dopo oggi: <b>%s</b>." % SETT[(i + 1) % 7])
    if k == "ieri2":
        return mcq("Ieri era %s. Che giorno è oggi?" % SETT[i], SETT[(i + 1) % 7], [SETT[i - 1], SETT[(i + 2) % 7], SETT[i]], "Oggi viene dopo ieri: <b>%s</b>." % SETT[(i + 1) % 7])
    return mcq("Domani sarà %s. Che giorno è oggi?" % SETT[i], SETT[i - 1], [SETT[(i + 1) % 7], SETT[i - 2], SETT[i]], "Oggi viene prima di domani: <b>%s</b>." % SETT[i - 1])


STORIE = [["mi sveglio", "faccio colazione", "vado a scuola"], ["semino", "la piantina cresce", "spunta il fiore"], ["mescolo la farina", "metto la torta in forno", "mangio la torta"],
          ["metto le calze", "metto le scarpe", "allaccio le scarpe"], ["apro il libro", "leggo la storia", "chiudo il libro"], ["mi lavo le mani", "mangio", "sparecchio"],
          ["l’uovo", "il pulcino", "la gallina"], ["il bruco", "il bozzolo", "la farfalla"], ["mi metto il pigiama", "mi lavo i denti", "vado a letto"]]


def s5_ordine():
    st = R.choice(STORIE)
    k = R.choice(["prima", "dopo", "ultimo"])
    if k == "prima":
        return mcq("Che cosa viene <b>prima</b>: %s?" % ", ".join(sorted(st)), st[0], [x for x in st if x != st[0]] + ["succedono insieme"], "L’ordine è: %s. Prima viene <b>%s</b>." % (" → ".join(st), st[0]))
    if k == "ultimo":
        return mcq("Che cosa viene <b>per ultimo</b>: %s?" % ", ".join(sorted(st)), st[2], [x for x in st if x != st[2]] + ["succedono insieme"], "L’ordine è: %s. Per ultimo <b>%s</b>." % (" → ".join(st), st[2]))
    return mcq("Che cosa viene subito <b>dopo</b> «%s»?" % st[0], st[1], [st[2], "niente", "succedono insieme"], "L’ordine è: %s." % " → ".join(st))


def s4_ore():
    it = O2.s1_ore()
    return it if it and ":00?" not in it["q"] and ":30" not in it["c"][0] else None


def s4_dopo():
    it = O2.s3_dopo()
    return it if it and "film" not in it["q"] else None


def main():
    O2.R = R
    O2.K = Kids(R)
    seen = set()
    sets = [
        ("Ieri, oggi, domani", mix(R, seen, [(s1_ieri, 14), (O2.s3_giornata, 6)])),
        ("Prima e dopo", mix(R, seen, [(s5_ordine, 20)])),
        ("I giorni della settimana", mix(R, seen, [(O2.s4_settimana, 20)])),
        ("I mesi e le stagioni", mix(R, seen, [(O2.s4_mesi, 20)])),
        ("L’orologio: le ore intere", mix(R, seen, [(s4_ore, 12), (s4_dopo, 5), (O2.s3_giornata, 3)])),
    ]
    body = lesson(
        ["Le azioni succedono in un ordine: <b>prima</b>, <b>adesso</b>, <b>dopo</b>. Ieri è il giorno prima di oggi, domani il giorno dopo.",
         "La giornata ha la <b>mattina</b>, il <b>pomeriggio</b>, la <b>sera</b> e la <b>notte</b>.",
         "La settimana ha 7 giorni: lunedì, martedì, mercoledì, giovedì, venerdì, sabato, domenica. L’anno ha 12 mesi e 4 stagioni.",
         "Sull’orologio la lancetta <b>corta</b> segna le ore, la lancetta <b>lunga</b> i minuti. Quando la lunga è sul 12, è un’ora intera."],
        [("Oggi è mercoledì", ["ieri: martedì", "domani: giovedì"], "ieri martedì, domani giovedì")],
        [["Confondere ieri e domani", "Ieri è già passato, domani deve ancora venire."],
         ["Pensare che dopo domenica venga sabato", "Dopo domenica ricomincia la settimana: lunedì."],
         ["Leggere l’ora con la lancetta lunga", "Le ore le dice la lancetta corta."]],
        table(["Stagione", "Mesi"], [["primavera", "marzo, aprile, maggio"], ["estate", "giugno, luglio, agosto"], ["autunno", "settembre, ottobre, novembre"], ["inverno", "dicembre, gennaio, febbraio"]]))
    faq = [("Come si imparano i giorni della settimana?", "Con una filastrocca e con il calendario in classe: ogni mattina si dice che giorno è oggi, com’era ieri e come sarà domani."),
           ("Quando si impara a leggere l’orologio?", "In classe prima si leggono le ore intere; le mezz’ore e i quarti arrivano in seconda.")]
    make_unit(R, "il-tempo", "M",
              "Collocare nel tempo azioni ed eventi (prima, dopo, ieri, oggi, domani); conoscere i giorni della settimana, i mesi e le stagioni; leggere l’orologio alle ore intere",
              "Il tempo: giorni, mesi, stagioni e orologio", "Il tempo",
              "Schede di matematica per la classe prima sul tempo: ieri, oggi, domani, prima e dopo, mattina e sera, i giorni della settimana, i mesi e le stagioni, l’orologio con le ore intere. 100 esercizi con soluzioni.",
              "Ieri, oggi, domani.", "La lancetta corta segna le ore.",
              body, faq, sets, 11, grade=G)


if __name__ == "__main__":
    main()
