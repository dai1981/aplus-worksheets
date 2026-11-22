# -*- coding: utf-8 -*-
"""
Italia Matematica classe seconda: L’orologio e il calendario (Misure)
  python3 tools/gen_it_matematica_c2_orologio_e_calendario.py
Leggere l’orologio: ore intere, e mezza, e un quarto, meno un quarto; un’ora dopo, un’ora prima; momenti della
giornata; giorni della settimana, mesi, stagioni; quanto dura (ore intere).
Errori: scambiare le lancette, «e mezza» con la lancetta corta sull’ora dopo, sbagliare l’ordine dei mesi.
"""
import random
from it_common import mcq, lesson, make_unit, mix, Kids, orologio, ora
import it_c2 as C

R = random.Random(70213)
G = "classe-seconda"
K = Kids(R)
SETT = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]
MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]
STAG = [("inverno", ["dicembre", "gennaio", "febbraio"]), ("primavera", ["marzo", "aprile", "maggio"]), ("estate", ["giugno", "luglio", "agosto"]), ("autunno", ["settembre", "ottobre", "novembre"])]


def parole(h, m):
    nome = ["", "l’una", "le due", "le tre", "le quattro", "le cinque", "le sei", "le sette", "le otto", "le nove", "le dieci", "le undici", "le dodici"]
    if m == 0:
        return nome[h]
    if m == 30:
        return nome[h] + " e mezza"
    if m == 15:
        return nome[h] + " e un quarto"
    return nome[h % 12 + 1] + " meno un quarto"


def s1_ore():
    h = R.randint(1, 12)
    m = R.choice([0, 0, 30])
    w = [ora(12 if m == 0 else 6, h * 5 % 60) if m == 0 else ora(h % 12 + 1, 30), ora(h % 12 + 1, m), ora(h - 1 if h > 1 else 12, m), ora(h, 30 if m == 0 else 0)]
    return mcq(orologio(h, m) + "Che ore sono?", ora(h, m), w, "La lancetta corta indica le ore, la lunga i minuti. Sono %s: <b>%s</b>." % (parole(h, m), ora(h, m)))


def s2_quarti():
    h = R.randint(1, 12)
    m = R.choice([15, 45, 30, 15, 45])
    hh = h if m != 45 else h
    w = [ora(h % 12 + 1, m), ora(h, (m + 30) % 60), ora(h, 9 if m == 45 else 3)]
    return mcq(orologio(h, m) + "Che ore sono?", ora(h, m), w, "La lancetta lunga è sul %d: sono %s, <b>%s</b>." % (m // 5, parole(h, m), ora(h, m)))


def s2_parole():
    h = R.randint(1, 11)
    m = R.choice([0, 15, 30, 45])
    t = parole(h, m)
    return mcq("Sono %s. Come si scrive?" % t if not t.startswith("l’una") else "È %s. Come si scrive?" % t, ora(h, m),
               [ora(h % 12 + 1, m), ora(h, (m + 15) % 60), ora(h, m // 15 * 10) if m else ora(h, 30), ora(h + 1, 45 if m == 45 else 0) if m == 45 else ora(h, 45)],
               "%s = <b>%s</b>." % (t[0].upper() + t[1:], ora(h, m)))


def s3_dopo():
    h = R.randint(1, 11)
    d = R.randint(1, 4)
    p = K.next()
    if R.random() < 0.5:
        return mcq(orologio(h, 0) + "%s comincia a giocare a quest’ora e gioca per %d %s. A che ora finisce?" % (p[0], d, "ora" if d == 1 else "ore"), ora((h + d - 1) % 12 + 1, 0),
                   [ora((h - d - 1) % 12 + 1, 0), ora(h, d * 10 % 60) if d * 10 % 60 else ora(h, 30), ora((h + d) % 12 + 1, 0)], "%s + %d %s = <b>%s</b>." % (ora(h, 0), d, "ora" if d == 1 else "ore", ora((h + d - 1) % 12 + 1, 0)))
    a, b = R.randint(1, 8), None
    b = a + d
    return mcq("Un film comincia alle %s e finisce alle %s. Quante ore dura?" % (ora(a, 0), ora(b, 0)), "%d %s" % (d, "ora" if d == 1 else "ore"),
               ["%d ore" % (d + 1), "%d ore" % (a + b), "%d minuti" % d], "Dalle %d alle %d passano <b>%d %s</b>." % (a, b, d, "ora" if d == 1 else "ore"))


def s3_giornata():
    ev, t = R.choice([("fai colazione", "la mattina"), ("pranzi", "a mezzogiorno"), ("vai a dormire", "la sera"), ("fai merenda", "il pomeriggio"), ("ti svegli", "la mattina"),
                      ("vedi la luna e le stelle", "la notte"), ("ceni", "la sera"), ("entri a scuola", "la mattina"), ("esci da scuola e fai i compiti", "il pomeriggio")])
    return mcq("Di solito quando %s?" % ev, t, [x for x in ("la mattina", "a mezzogiorno", "il pomeriggio", "la sera", "la notte") if x != t][:3], "Di solito %s <b>%s</b>." % (ev, t))


def s4_settimana():
    i = R.randrange(7)
    k = R.choice(["dopo", "prima", "dopodomani", "quanti"])
    if k == "dopo":
        return mcq("Che giorno viene dopo %s?" % SETT[i], SETT[(i + 1) % 7], [SETT[i - 1], SETT[(i + 2) % 7], SETT[(i + 3) % 7]], "Dopo %s viene <b>%s</b>." % (SETT[i], SETT[(i + 1) % 7]))
    if k == "prima":
        return mcq("Che giorno viene prima di %s?" % SETT[i], SETT[i - 1], [SETT[(i + 1) % 7], SETT[i - 2], SETT[(i + 3) % 7]], "Prima di %s viene <b>%s</b>." % (SETT[i], SETT[i - 1]))
    if k == "dopodomani":
        return mcq("Oggi è %s. Che giorno sarà dopodomani?" % SETT[i], SETT[(i + 2) % 7], [SETT[(i + 1) % 7], SETT[i - 2], SETT[(i + 3) % 7]], "Domani %s, dopodomani <b>%s</b>." % (SETT[(i + 1) % 7], SETT[(i + 2) % 7]))
    q, a, w = R.choice([("Quanti giorni ha una settimana?", "7", ["5", "10", "12"]), ("Quanti mesi ha un anno?", "12", ["10", "7", "4"]), ("Quante stagioni ci sono in un anno?", "4", ["3", "12", "2"]),
                        ("Quante ore ha un giorno?", "24", ["12", "60", "10"]), ("Quanti minuti ha un’ora?", "60", ["100", "30", "24"]), ("Quanti giorni ha il fine settimana?", "2", ["1", "3", "5"])])
    return mcq(q, a, w, "Risposta: <b>%s</b>." % a)


def s4_mesi():
    i = R.randrange(12)
    k = R.choice(["dopo", "prima", "stagione", "stagione"])
    if k == "dopo":
        return mcq("Quale mese viene dopo %s?" % MESI[i], MESI[(i + 1) % 12], [MESI[i - 1], MESI[(i + 2) % 12], MESI[(i + 6) % 12]], "Dopo %s viene <b>%s</b>." % (MESI[i], MESI[(i + 1) % 12]))
    if k == "prima":
        return mcq("Quale mese viene prima di %s?" % MESI[i], MESI[i - 1], [MESI[(i + 1) % 12], MESI[i - 2], MESI[(i + 5) % 12]], "Prima di %s viene <b>%s</b>." % (MESI[i], MESI[i - 1]))
    s, ms = R.choice(STAG)
    m = R.choice(ms)
    return mcq("In Italia, %s è un mese di quale stagione?" % m, s, [x for x, _ in STAG if x != s], "%s è in <b>%s</b>." % (m[0].upper() + m[1:], s))


def main():
    seen = set()
    sets = [
        ("Ore intere e mezze ore", mix(R, seen, [(s1_ore, 20)])),
        ("Un quarto e tre quarti", mix(R, seen, [(s2_quarti, 10), (s2_parole, 10)])),
        ("Prima, dopo e quanto dura", mix(R, seen, [(s3_dopo, 12), (s3_giornata, 8)])),
        ("La settimana", mix(R, seen, [(s4_settimana, 20)])),
        ("I mesi e le stagioni", mix(R, seen, [(s4_mesi, 20)])),
    ]
    body = lesson(
        ["Nell’orologio la <b>lancetta corta</b> indica le ore, la <b>lancetta lunga</b> i minuti.",
         "Lancetta lunga sul 12: ora esatta. Sul 6: <b>e mezza</b>. Sul 3: <b>e un quarto</b>. Sul 9: <b>meno un quarto</b> dell’ora dopo.",
         "Una settimana ha 7 giorni; un anno ha 12 mesi e 4 stagioni."],
        [("La lancetta corta è tra il 4 e il 5, la lunga sul 6.", ["ore: 4", "minuti: 30"], "le quattro e mezza, 4:30")],
        [["Scambiare le lancette", "La corta indica le ore."],
         ["Leggere 4:30 come 5:30", "Alle 4 e mezza la lancetta corta ha superato il 4, ma non è ancora sul 5."],
         ["Sbagliare l’ordine dei mesi", "Ripeti: gennaio, febbraio, marzo…"]],
        orologio(4, 30))
    faq = [("Come si impara a leggere l’orologio?", "Con un orologio vero: prima le ore intere, poi le mezze ore, infine i quarti."),
           ("Come si ricordano i giorni dei mesi?", "Con la filastrocca «Trenta giorni ha novembre, con april, giugno e settembre; di ventotto ce n’è uno, tutti gli altri ne han trentuno».")]
    make_unit(R, "orologio-e-calendario", "M",
              "Leggere l’orologio (ore, mezze ore, quarti d’ora); conoscere la successione dei giorni, dei mesi e delle stagioni; misurare la durata di semplici eventi",
              "L’orologio e il calendario", "Orologio e calendario",
              "Schede di matematica per la classe seconda su orologio e calendario: ore intere, mezze ore e quarti, prima e dopo, momenti della giornata, settimana, mesi e stagioni. 100 esercizi con soluzioni.",
              "Lancetta corta: ore. Lancetta lunga: minuti.", "Sul 6 è «e mezza», sul 3 «e un quarto».",
              body, faq, sets, 13, grade=G)


if __name__ == "__main__":
    main()
