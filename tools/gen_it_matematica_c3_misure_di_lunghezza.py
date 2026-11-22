# -*- coding: utf-8 -*-
"""
Italia Matematica classe terza: Le misure di lunghezza (Misure)
  python3 tools/gen_it_matematica_c3_misure_di_lunghezza.py
Il metro, multipli (dam, hm, km) e sottomultipli (dm, cm, mm), scegliere l’unità, equivalenze, confrontare,
misurare con il righello, problemi.
Errori: 1 m = 10 cm, confrontare senza trasformare, leggere il righello partendo da 1.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, Kids, relabel, NB, table
import gen_fr_maths_ce2_longueurs_et_perimetres as FRL

R = random.Random(70313)
K = Kids(R)
OBJ = [("Una matita è lunga", 15, "cm"), ("Una gomma è lunga", 4, "cm"), ("Una formica è lunga", 5, "mm"), ("Una coccinella è lunga", 7, "mm"),
       ("L’aula è lunga", 9, "m"), ("Il viaggio in auto da Roma a Firenze è di", 275, "km"), ("Un francobollo è lungo", 25, "mm"),
       ("Una porta è alta", 2, "m"), ("Un autobus è lungo", 12, "m"), ("Una piscina olimpica è lunga", 50, "m"), ("Un libro è lungo", 24, "cm"),
       ("Un’unghia è larga", 1, "cm"), ("Un filone di pane è lungo", 40, "cm"), ("Una pista di atletica è lunga", 400, "m"),
       ("Una tappa del Giro d’Italia è di", 180, "km"), ("Un chicco di riso è lungo", 6, "mm"), ("Un letto è lungo", 2, "m"),
       ("Un righello è lungo", 30, "cm"), ("Il fiume Po è lungo", 652, "km"), ("Una moneta da 1 € è larga", 23, "mm"),
       ("Un tavolo è alto", 75, "cm"), ("Una maratona è di", 42, "km"), ("Un campo da calcio è lungo", 105, "m"), ("Una giraffa è alta", 5, "m")]
UNITS = ["mm", "cm", "m", "km"]


def L(v, u):
    return "%s%s%s" % (num(v), NB, u)


def regle(a, b):
    return relabel(FRL.regle(a, b), "righello in centimetri e un segmento rosso")


def s1_unita():
    o, v, u = R.choice(OBJ)
    return mcq("Quale unità di misura è giusta? %s circa %s …" % (o, num(v)), u, [x for x in UNITS if x != u],
               "%s circa %s <b>%s</b>." % (o, num(v), u))


def s1_quale():
    k = R.choice(["m", "dm", "cm", "mm", "km", "dam", "hm"])
    info = {"m": ("il metro", "l’unità principale delle lunghezze"), "dm": ("il decimetro", "1 m diviso in 10 parti"),
            "cm": ("il centimetro", "1 m diviso in 100 parti"), "mm": ("il millimetro", "1 m diviso in 1000 parti"),
            "km": ("il chilometro", "1000 m"), "dam": ("il decametro", "10 m"), "hm": ("l’ettometro", "100 m")}
    ok = info[k][1]
    return mcq("Che cosa misura %s (%s)?" % (info[k][0], k), ok, [info[x][1] for x in info if x != k],
               "%s (%s) è <b>%s</b>." % (info[k][0].capitalize(), k, ok))


def s2_equiv():
    k = R.choice(["m_cm", "km_m", "cm_mm", "m_dm", "dm_cm", "mcm", "m_mm", "dam_m", "hm_m", "cm_m", "dm_m"])
    a = R.randint(2, 9)
    if k == "m_cm":
        return mcq("Completa l’equivalenza: %s = … cm" % L(a, "m"), num(a * 100), [num(a * 10), num(a * 1000), num(a + 100)], "1 m = 100 cm, quindi %d m = <b>%s cm</b>." % (a, num(a * 100)))
    if k == "km_m":
        return mcq("Completa l’equivalenza: %s = … m" % L(a, "km"), num(a * 1000), [num(a * 100), num(a * 10), num(a * 10000)], "1 km = 1000 m, quindi %d km = <b>%s m</b>." % (a, num(a * 1000)))
    if k == "cm_mm":
        a = R.randint(2, 40)
        return mcq("Completa l’equivalenza: %s = … mm" % L(a, "cm"), num(a * 10), [num(a * 100), num(a + 10), str(a)], "1 cm = 10 mm, quindi %d cm = <b>%s mm</b>." % (a, num(a * 10)))
    if k == "m_dm":
        return mcq("Completa l’equivalenza: %s = … dm" % L(a, "m"), num(a * 10), [num(a * 100), str(a), num(a * 1000)], "1 m = 10 dm, quindi %d m = <b>%s dm</b>." % (a, num(a * 10)))
    if k == "dm_cm":
        a = R.randint(2, 15)
        return mcq("Completa l’equivalenza: %s = … cm" % L(a, "dm"), num(a * 10), [num(a * 100), str(a), num(a + 10)], "1 dm = 10 cm, quindi %d dm = <b>%s cm</b>." % (a, num(a * 10)))
    if k == "m_mm":
        return mcq("Completa l’equivalenza: %s = … mm" % L(a, "m"), num(a * 1000), [num(a * 100), num(a * 10), num(a * 10000)], "1 m = 1000 mm, quindi %d m = <b>%s mm</b>." % (a, num(a * 1000)))
    if k == "dam_m":
        return mcq("Completa l’equivalenza: %s = … m" % L(a, "dam"), num(a * 10), [num(a * 100), str(a), num(a * 1000)], "1 dam = 10 m, quindi %d dam = <b>%s m</b>." % (a, num(a * 10)))
    if k == "hm_m":
        return mcq("Completa l’equivalenza: %s = … m" % L(a, "hm"), num(a * 100), [num(a * 10), num(a * 1000), str(a)], "1 hm = 100 m, quindi %d hm = <b>%s m</b>." % (a, num(a * 100)))
    if k == "cm_m":
        return mcq("Completa l’equivalenza: %s = … m" % L(a * 100, "cm"), str(a), [num(a * 10), num(a * 1000), num(a * 100)], "100 cm = 1 m, quindi %s cm = <b>%d m</b>." % (num(a * 100), a))
    if k == "dm_m":
        return mcq("Completa l’equivalenza: %s = … m" % L(a * 10, "dm"), str(a), [num(a * 100), num(a * 10), str(a * 10 + 1)], "10 dm = 1 m, quindi %d dm = <b>%d m</b>." % (a * 10, a))
    b = R.randint(5, 95)
    return mcq("Completa l’equivalenza: %s %s = … cm" % (L(a, "m"), L(b, "cm")), num(a * 100 + b), [num(a + b), num(a * 10 + b), num(a * 1000 + b)],
               "%d m = %d cm, e %d + %d = <b>%s cm</b>." % (a, a * 100, a * 100, b, num(a * 100 + b)))


def s3_confronta():
    k = R.choice(["mcm", "kmm", "cmmm", "dmcm"])
    if k == "mcm":
        a, b = R.randint(1, 5), R.randint(5, 95)
        x = a * 100 + b
        y = x + R.choice([-30, -9, 9, 30, 45, -45])
        if y <= 0 or y == x:
            return None
        A, B = "%s %s" % (L(a, "m"), L(b, "cm")), L(y, "cm")
    elif k == "kmm":
        a = R.randint(1, 6)
        x = a * 1000
        y = R.choice([a * 100, a * 1000 + R.choice([-150, 150, 900]), a * 1000 - 900])
        if y == x or y <= 0:
            return None
        A, B = L(a, "km"), L(y, "m")
    elif k == "cmmm":
        a = R.randint(3, 40)
        x = a * 10
        y = x + R.choice([-6, -15, 7, 15, 40])
        if y <= 0 or y == x:
            return None
        A, B = L(a, "cm"), L(y, "mm")
    else:
        a = R.randint(2, 9)
        x = a * 10
        y = x + R.choice([-5, -3, 2, 4, 8])
        A, B = L(a, "dm"), L(y, "cm")
    big = A if x > y else B
    small = B if big == A else A
    return mcq("Qual è la lunghezza maggiore: %s o %s?" % (A, B), big, [small, "sono uguali", "non si possono confrontare"],
               "Prima trasforma nella stessa unità, poi confronta: %s e %s. La maggiore è <b>%s</b>." % (A, B, big))


def s4_righello():
    a = R.choice([0, 0, 0, 10, 20, 30])
    b = a + R.choice([10, 20, 30, 40, 50, 60, 70, 80, 90]) + R.choice([0, 0, 5])
    if b > 140:
        return None
    ln = b - a
    fmt = lambda m: "%d cm" % (m // 10) if m % 10 == 0 else "%d cm %d mm" % (m // 10, m % 10)
    w = [fmt(b), fmt(ln + 10), fmt(ln - 10) if ln > 10 else fmt(ln + 20), "%d mm" % (ln // 10)]
    return mcq(regle(a, b) + "Quanto è lungo il segmento rosso?", fmt(ln), [x for x in w if x != fmt(ln)],
               "Il segmento va da %s a %s: %s." % (fmt(a) if a else "0", fmt(b), "<b>%s</b>" % fmt(ln)))


def s4_ordine():
    vals = [(R.randint(1, 3), "m"), (R.randint(110, 390), "cm"), (R.randint(12, 39), "dm"), (R.randint(1100, 3900), "mm")]
    cm = {"m": 100, "dm": 10, "cm": 1, "mm": 0.1}
    vs = [(v * cm[u], L(v, u)) for v, u in vals]
    if len({x[0] for x in vs}) < 4:
        return None
    big = max(vs)[1]
    return mcq("Quale lunghezza è la più grande? %s" % ", ".join(x[1] for x in vs), big, [x[1] for x in vs if x[1] != big],
               "In centimetri: %s. La più grande è <b>%s</b>." % (", ".join("%s = %s cm" % (x[1], num(int(x[0])) if x[0] == int(x[0]) else ("%.1f" % x[0]).replace(".", ",")) for x in vs), big))


def s5_problema():
    p = K.next()
    k = R.choice(["nastro", "salto", "strada", "piante", "cm", "corsa"])
    if k == "nastro":
        a, b = R.randint(2, 5), R.randint(20, 80)
        r = a * 100 - b
        return mcq("%s ha un nastro di %d m. Ne taglia %d cm. Quanti centimetri restano?" % (p[0], a, b), "%s cm" % num(r),
                   ["%d cm" % (a - b) if a > b else "%d cm" % (a * 10 - b if a * 10 > b else r + 10), "%s cm" % num(a * 100 + b), "%s cm" % num(r + 10)],
                   "%d m = %s cm; %s − %d = <b>%s cm</b>." % (a, num(a * 100), num(a * 100), b, num(r)))
    if k == "salto":
        a, b = R.randint(180, 260), R.randint(10, 40)
        return mcq("%s salta %d cm. Il suo amico salta %d cm in più. Quanto salta l’amico?" % (p[0], a, b), "%d cm" % (a + b),
                   ["%d cm" % (a - b), "%d cm" % (a + b + 10), "%d m" % (a + b)], "%d + %d = <b>%d cm</b>." % (a, b, a + b))
    if k == "strada":
        a, b = R.randint(1, 4), R.choice([200, 300, 500, 600, 800])
        return mcq("Da casa a scuola ci sono %d km e %d m. Quanti metri sono?" % (a, b), "%s m" % num(a * 1000 + b),
                   ["%s m" % num(a * 100 + b), "%s m" % num(a + b), "%s m" % num(a * 1000 + b * 10)],
                   "%d km = %s m; %s + %d = <b>%s m</b>." % (a, num(a * 1000), num(a * 1000), b, num(a * 1000 + b)))
    if k == "piante":
        n, d = R.randint(4, 9), R.choice([2, 3, 5])
        return mcq("In un viale ci sono %d alberi in fila, uno ogni %d m. Quanti metri ci sono dal primo all’ultimo albero?" % (n, d), "%d m" % ((n - 1) * d),
                   ["%d m" % (n * d), "%d m" % (n + d), "%d m" % ((n - 2) * d)],
                   "Tra %d alberi ci sono %d spazi: %d × %d = <b>%d m</b>." % (n, n - 1, n - 1, d, (n - 1) * d))
    if k == "cm":
        n, l = R.randint(3, 8), R.randint(12, 25)
        return mcq("%s mette in fila %d matite lunghe %d cm. Quanto è lunga la fila?" % (p[0], n, l), "%d cm" % (n * l),
                   ["%d cm" % (n + l), "%d cm" % (n * l + l), "%d m" % (n * l)], "%d × %d = <b>%d cm</b>." % (n, l, n * l))
    g = R.randint(3, 6)
    m = R.choice([200, 400, 500])
    return mcq("Ogni giorno %s corre %d m. Quanti metri corre in %d giorni? È più o meno di 1 km?" % (p[0], m, g),
               "%s m, più di 1 km" % num(m * g) if m * g > 1000 else "%s m, esattamente 1 km" % num(m * g) if m * g == 1000 else "%s m, meno di 1 km" % num(m * g),
               ["%s m, meno di 1 km" % num(m * g) if m * g > 1000 else "%s m, più di 1 km" % num(m * g), "%s m, più di 1 km" % num(m + g), "%s m, meno di 1 km" % num(m * g // 10)],
               "%d × %d = %s m; 1 km = 1000 m. <b>%s m</b>." % (m, g, num(m * g), num(m * g)))


def main():
    seen = set()
    sets = [
        ("Il metro e le unità di misura", mix(R, seen, [(s1_unita, 14), (s1_quale, 6)])),
        ("Equivalenze", mix(R, seen, [(s2_equiv, 20)])),
        ("Confrontare le lunghezze", mix(R, seen, [(s3_confronta, 14), (s4_ordine, 6)])),
        ("Misurare con il righello", mix(R, seen, [(s4_righello, 20)])),
        ("Problemi", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["L’unità di misura delle lunghezze è il <b>metro</b> (m).",
         "I <b>sottomultipli</b> sono più piccoli: 1 m = 10 dm = 100 cm = 1000 mm. I <b>multipli</b> sono più grandi: 1 dam = 10 m, 1 hm = 100 m, 1 km = 1000 m.",
         "Ogni unità è 10 volte più grande di quella alla sua destra: km, hm, dam, <b>m</b>, dm, cm, mm.",
         "Per confrontare due lunghezze trasformale prima nella stessa unità. Con il righello parti sempre dallo 0."],
        [("3 m 45 cm = … cm", ["3 m = 300 cm", "300 + 45 = 345"], "345 cm"),
         ("Qual è più lungo: 2 dm o 18 cm?", ["2 dm = 20 cm", "20 cm &gt; 18 cm"], "2 dm")],
        [["1 m = 10 cm", "1 m = 100 cm (e 10 dm)."],
         ["Pensare che 18 cm sia più di 2 dm perché 18 &gt; 2", "Trasforma: 2 dm = 20 cm."],
         ["Leggere il righello partendo da 1", "Metti lo 0 all’inizio del segmento."]],
        table(["km", "hm", "dam", "m", "dm", "cm", "mm"], [["1000 m", "100 m", "10 m", "1 m", "1/10 m", "1/100 m", "1/1000 m"]]))
    faq = [("Che cosa sono le equivalenze?", "Sono uguaglianze tra misure scritte con unità diverse, come 3 m = 300 cm. Per passare a un’unità più piccola si moltiplica per 10, 100, 1000."),
           ("Come ricordo l’ordine delle unità?", "km, hm, dam, m, dm, cm, mm: ogni passo verso destra si moltiplica per 10.")]
    make_unit(R, "misure-di-lunghezza", "M",
              "Misurare lunghezze utilizzando sia unità arbitrarie sia unità e strumenti convenzionali (metro, righello); conoscere multipli e sottomultipli del metro ed eseguire semplici equivalenze",
              "Le misure di lunghezza: metro, multipli e sottomultipli", "Misure di lunghezza",
              "Schede di matematica per la classe terza sulle misure di lunghezza: metro, multipli e sottomultipli, scegliere l’unità, equivalenze, confronti, righello e problemi. 100 esercizi con soluzioni.",
              "1 m = 10 dm = 100 cm = 1000 mm.", "Ogni unità vale 10 volte quella alla sua destra.",
              body, faq, sets, 13)


if __name__ == "__main__":
    main()
