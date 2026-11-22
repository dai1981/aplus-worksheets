# -*- coding: utf-8 -*-
"""
Italia Matematica classe quinta: Misure ed equivalenze (Misure)
  python3 tools/gen_it_matematica_c5_misure_ed_equivalenze.py
Sistema metrico decimale: lunghezza (km … mm), peso (Mg, q, kg … mg), capacità (hl … ml), superficie (km² … mm²,
ogni passo × 100), equivalenze con i numeri decimali, confrontare misure, misure di tempo, problemi.
Errori: spostare la virgola nel verso sbagliato, superfici di 1 posto invece di 2, 1 h = 100 min.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, Kids, table, NB, FOIS

R = random.Random(70516)
G = "classe-quinta"
K = Kids(R)
LUN = ["km", "hm", "dam", "m", "dm", "cm", "mm"]
PES = ["Mg", "q", "kg", "hg", "dag", "g", "dg", "cg", "mg"]
CAP = ["hl", "dal", "l", "dl", "cl", "ml"]
SUP = ["km²", "hm²", "dam²", "m²", "dm²", "cm²", "mm²"]
PES_STEP = {("Mg", "q"): 10, ("q", "kg"): 100}


def D(n, p):
    neg = n < 0
    ip, fp_ = divmod(abs(n), 10 ** p)
    s = (str(fp_).rjust(p, "0") if p else "").rstrip("0")
    return num(ip) + ("," + s if s else "")


def conv(scale, a, b, step=1):
    """esponente di 10 da a a b"""
    return (scale.index(b) - scale.index(a)) * step


def peso_exp(a, b):
    """Mg e q non sono a passo 10: Mg = 1000 kg, q = 100 kg"""
    val = {"Mg": 6, "q": 5, "kg": 3, "hg": 2, "dag": 1, "g": 0, "dg": -1, "cg": -2, "mg": -3}
    return val[a] - val[b]


def eq(scale, step=1, peso=False):
    i, j = R.sample(range(len(scale)), 2)
    a, b = scale[i], scale[j]
    e = peso_exp(a, b) if peso else (j - i) * step
    if abs(e) > 4 or e == 0:
        return None
    # valore con al massimo 2 decimali
    p = R.choice([0, 0, 1, 2])
    n = R.randint(2, 999) if p == 0 else R.randint(11, 9999)
    if n % 10 == 0 and p:
        n += 3
    # risultato: n * 10^(e - p)
    ex = e - p
    if ex >= 0:
        r = D(n * 10 ** ex, 0)
    else:
        r = D(n, -ex)
    shift = lambda k: D(n * 10 ** (ex + k), 0) if ex + k >= 0 else D(n, -(ex + k))
    w = ([shift(-e // 2)] if step == 2 else []) + [shift(-2 * e) if abs(e) <= 3 else shift(-1), shift(1), shift(-1), shift(2)]
    v = D(n, p)
    return mcq("Completa l’equivalenza: %s%s%s = … %s" % (v, NB, a, b), r, [x for x in w if x != r],
               "Da %s a %s%s: la virgola si sposta di %d %s verso %s. <b>%s %s</b>." % (a, b, (" c’è 1 passo da %s" % ("100" if step == 2 else "10") if abs(e) == step else " ci sono %d passi da %s" % (abs(e) // step, "100" if step == 2 else "10")) if not peso else "", abs(e), "posto" if abs(e) == 1 else "posti",
                                                                                       "destra (unità più piccola)" if e > 0 else "sinistra (unità più grande)", r, b))


def s1():
    return eq(LUN)


def s2():
    return eq(PES, peso=True) if R.random() < 0.5 else eq(CAP)


def s3_sup():
    return eq(SUP, step=2)


def s3_confronta():
    k = R.choice([(LUN, 1, False), (PES[2:6], 1, False), (CAP, 1, False)])
    sc = k[0]
    i, j = R.sample(range(len(sc)), 2)
    a, b = sc[i], sc[j]
    e = j - i
    x = R.randint(2, 90)
    if e > 0:
        y = x * 10 ** e + R.choice([-1, 1]) * R.randint(1, 9) * 10 ** max(e - 1, 0)
    else:
        y = R.randint(1, 9)
        x = y * 10 ** (-e) + R.choice([-1, 1]) * R.randint(1, 9) * 10 ** max(-e - 1, 0)
    if x <= 0 or y <= 0:
        return None
    A, B = "%s %s" % (num(x), a), "%s %s" % (num(y), b)
    va = x * 10 ** (len(sc) - i)
    vb = y * 10 ** (len(sc) - j)
    if va == vb:
        return None
    g, s_ = (A, B) if va > vb else (B, A)
    return mcq("Qual è la misura maggiore: %s o %s?" % (A, B), g, [s_, "sono uguali", "non si possono confrontare"],
               "Trasforma nella stessa unità e confronta: è maggiore <b>%s</b>." % g)


def s4_tempo():
    k = R.choice(["hmin", "minh", "gh", "secoli", "minsec", "giorni"])
    if k == "hmin":
        h, m = R.randint(1, 5), R.randint(5, 55)
        return mcq("Quanti minuti sono %d h e %d min?" % (h, m), "%d min" % (h * 60 + m), ["%d min" % (h * 100 + m), "%d min" % (h + m), "%d min" % (h * 60)],
                   "1 h = 60 min: %d %s 60 + %d = <b>%d min</b>." % (h, FOIS, m, h * 60 + m))
    if k == "minh":
        n = R.randint(70, 400)
        if n % 60 == 0:
            return None
        return mcq("Quante ore e minuti sono %d minuti?" % n, "%d h %d min" % (n // 60, n % 60), ["%d h %d min" % (n // 100, n % 100), "%d h %d min" % (n // 60 + 1, n % 60), "%d h" % (n // 60)],
                   "%d %s 60 = %d con resto %d: <b>%d h %d min</b>." % (n, ":", n // 60, n % 60, n // 60, n % 60))
    if k == "gh":
        g = R.randint(2, 7)
        return mcq("Quante ore ci sono in %d giorni?" % g, "%d h" % (g * 24), ["%d h" % (g * 12), "%d h" % (g * 60), "%d h" % (g * 24 + 24)], "1 giorno = 24 h: %d %s 24 = <b>%d h</b>." % (g, FOIS, g * 24))
    if k == "secoli":
        a = R.randint(2, 9)
        return mcq("Quanti anni sono %d secoli?" % a, "%d anni" % (a * 100), ["%d anni" % (a * 10), "%d anni" % (a * 1000), "%d anni" % (a * 100 + 100)], "1 secolo = 100 anni: <b>%d anni</b>." % (a * 100))
    if k == "minsec":
        m, s_ = R.randint(1, 9), R.randint(5, 55)
        return mcq("Quanti secondi sono %d min e %d s?" % (m, s_), "%d s" % (m * 60 + s_), ["%d s" % (m * 100 + s_), "%d s" % (m + s_), "%d s" % (m * 60)], "%d %s 60 + %d = <b>%d s</b>." % (m, FOIS, s_, m * 60 + s_))
    w = R.randint(2, 9)
    return mcq("Quanti giorni sono %d settimane e 3 giorni?" % w, str(w * 7 + 3), [str(w * 10 + 3), str(w + 3), str(w * 7)], "%d %s 7 + 3 = <b>%d</b>." % (w, FOIS, w * 7 + 3))


def s5():
    p = K.next()
    k = R.choice(["corsa", "camion", "bottiglie", "stoffa", "pavimento", "medicina"])
    if k == "corsa":
        a, b = R.randint(2, 9), R.randint(100, 900)
        return mcq("%s corre %d km e %d m. Quanti metri sono?" % (p[0], a, b), "%s m" % num(a * 1000 + b), ["%s m" % num(a * 100 + b), "%s m" % num(a + b), "%s m" % num(a * 1000 + b * 10)],
                   "%d km = %s m; + %d = <b>%s m</b>." % (a, num(a * 1000), b, num(a * 1000 + b)))
    if k == "camion":
        s_ = R.choice([5, 10, 20, 25, 50])
        q = R.randint(10, 40)
        n = q * 100 // s_
        return mcq("Un camion trasporta %d quintali di patate in sacchi da %d kg. Quanti sacchi?" % (q, s_), num(n), [num(q * 10 // s_) if q * 10 // s_ else num(n + 1), num(q * s_), num(q * 1000 // s_)],
                   "1 q = 100 kg: %d q = %s kg; %s : %d = <b>%s</b>." % (q, num(q * 100), num(q * 100), s_, num(n)))
    if k == "bottiglie":
        l, c = R.choice([(3, 25), (6, 50), (9, 75), (2, 20), (5, 25), (4, 40)])
        return mcq("Con %d l di succo si riempiono bottigliette da %d cl. Quante bottigliette?" % (l, c), str(l * 100 // c), [str(l * 10 // c) if l * 10 // c else str(l * 100 // c + 1), str(l * c), str(l * 1000 // c)],
                   "%d l = %d cl; %d : %d = <b>%d</b>." % (l, l * 100, l * 100, c, l * 100 // c))
    if k == "stoffa":
        m, cm = R.randint(3, 9), R.choice([25, 50, 75, 40, 60])
        return mcq("Una sarta ha %d m di stoffa e ne usa %d cm per ogni cuscino. Quanti cuscini al massimo?" % (m, cm), str(m * 100 // cm),
                   [str(m * 10 // cm) if m * 10 // cm else str(m * 100 // cm + 1), str(m * cm), str(m * 100 // cm + 1)], "%d m = %d cm; %d : %d = %d%s: <b>%d</b> cuscini." % (m, m * 100, m * 100, cm, m * 100 // cm, " con resto %d" % (m * 100 % cm) if m * 100 % cm else "", m * 100 // cm))
    if k == "pavimento":
        a = R.randint(2, 9)
        return mcq("Un pavimento misura %d m². Quanti dm² sono?" % a, "%d dm²" % (a * 100), ["%d dm²" % (a * 10), "%d dm²" % (a * 1000), "%d dm²" % (a * 100 + 100)],
                   "1 m² = 100 dm² (nelle superfici ogni passo vale 100): <b>%d dm²</b>." % (a * 100))
    d, n = R.choice([(5, 3), (10, 2), (5, 4), (2, 3)])
    return mcq("Il pediatra dice di dare %d ml di sciroppo %d volte al giorno per 5 giorni. Quanti cl in tutto?" % (d, n), "%s cl" % D(d * n * 5, 1), ["%d cl" % (d * n * 5), "%s cl" % D(d * n * 5, 2), "%d cl" % (d * n)],
               "%d %s %d %s 5 = %d ml; 10 ml = 1 cl: <b>%s cl</b>." % (d, FOIS, n, FOIS, d * n * 5, D(d * n * 5, 1)))


def main():
    seen = set()
    sets = [
        ("Misure di lunghezza", mix(R, seen, [(s1, 20)])),
        ("Peso e capacità", mix(R, seen, [(s2, 20)])),
        ("Misure di superficie e confronti", mix(R, seen, [(s3_sup, 12), (s3_confronta, 8)])),
        ("Misure di tempo", mix(R, seen, [(s4_tempo, 20)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Nel sistema metrico ogni unità è <b>10 volte</b> quella alla sua destra: km, hm, dam, m, dm, cm, mm. Lo stesso per i litri e i grammi.",
         "Peso: 1 Mg (tonnellata) = 1000 kg; 1 q (quintale) = 100 kg; 1 kg = 1000 g.",
         "Nelle <b>superfici</b> ogni passo vale <b>100</b>: 1 m² = 100 dm² = 10 000 cm².",
         "Per passare a un’unità più piccola sposta la virgola a destra; a un’unità più grande, a sinistra. Il tempo invece va a 60: 1 h = 60 min."],
        [("3,45 m = … cm", ["da m a cm: 2 passi", "virgola 2 posti a destra"], "345 cm"),
         ("2,5 m² = … dm²", ["1 passo da 100", "virgola 2 posti a destra"], "250 dm²")],
        [["Spostare la virgola dalla parte sbagliata", "Unità più piccola → numero più grande."],
         ["1 m² = 10 dm²", "Nelle superfici ogni passo vale 100."],
         ["1 h = 100 min", "1 h = 60 min: il tempo non è decimale."]],
        table(["km", "hm", "dam", "m", "dm", "cm", "mm"], [["1000 m", "100 m", "10 m", "1 m", "0,1 m", "0,01 m", "0,001 m"]]))
    faq = [("Perché le superfici vanno di 100 in 100?", "Perché un quadrato di 1 m di lato contiene 10 file da 10 quadratini di 1 dm: 10 × 10 = 100 dm²."),
           ("Quanto vale un quintale?", "Un quintale (q) vale 100 kg; una tonnellata (Mg o t) vale 1000 kg.")]
    make_unit(R, "misure-ed-equivalenze", "M",
              "Utilizzare le principali unità di misura per lunghezze, angoli, aree, capacità, intervalli temporali, masse, pesi per effettuare misure e stime; passare da un’unità di misura a un’altra, limitatamente alle unità di uso più comune, anche nel contesto del sistema monetario",
              "Misure ed equivalenze: lunghezza, peso, capacità, superficie, tempo", "Misure ed equivalenze",
              "Schede di matematica per la classe quinta su misure ed equivalenze: lunghezza, peso, capacità, superficie, tempo, confronti e problemi. 100 esercizi con soluzioni.",
              "Ogni unità vale 10 volte quella a destra (superfici: 100).", "Unità più piccola → la virgola va a destra.",
              body, faq, sets, 16, grade=G)


if __name__ == "__main__":
    main()
