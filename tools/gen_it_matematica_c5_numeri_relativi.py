# -*- coding: utf-8 -*-
"""
Italia Matematica classe quinta: I numeri relativi (Numeri)
  python3 tools/gen_it_matematica_c5_numeri_relativi.py
Numeri positivi e negativi nella realtà (temperature, piani, altitudine, saldo), retta dei numeri relativi,
confrontare e ordinare, variazioni di temperatura (salire e scendere), differenza tra due temperature.
Errori: −8 > −3 perché 8 > 3, contare lo zero due volte, salire di 5 da −2 dà −7.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, retta, Kids

R = random.Random(70502)
G = "classe-quinta"
K = Kids(R)


def z(n):
    return ("+" if n > 0 else "") + num(n)


def gr(n):
    return z(n) + " °C"


def M(q, a, w, e):
    return mcq(q, a, w, e, neg=True)


def s1_realta():
    k = R.choice(["temp", "piano", "mare", "saldo"])
    n = R.randint(1, 12)
    if k == "temp":
        return M("La temperatura è di %d gradi sotto lo zero. Come si scrive?" % n, gr(-n), [gr(n), "%d °C" % (n * 10), gr(-(n + 1))],
                 "Sotto lo zero si usa il segno meno: <b>%s</b>." % gr(-n))
    if k == "piano":
        n = R.randint(1, 3)
        return M("In un palazzo il piano terra è lo 0. Il garage è %d %s sotto il piano terra. Che numero ha?" % (n, "piano" if n == 1 else "piani"), num(-n),
                 [z(n), "0", num(-(n + 1))], "Sotto il piano terra i piani sono negativi: <b>%s</b>." % num(-n))
    if k == "mare":
        n = R.randint(2, 9) * 10
        return M("Un sub si trova a %d m sotto il livello del mare. Come si indica la sua posizione?" % n, num(-n) + " m", [z(n) + " m", num(-n // 10) + " m", "0 m"],
                 "Il livello del mare è 0; sotto si usa il meno: <b>%s m</b>." % num(-n))
    n = R.randint(5, 60)
    return M("Sul conto della famiglia mancano %d €: il conto è «in rosso». Come si scrive il saldo?" % n, num(-n) + " €", [z(n) + " €", "0 €", num(-(n + 10)) + " €"],
             "Un debito si scrive con il meno: <b>%s €</b>." % num(-n))


def s1_retta():
    lo = R.choice([-10, -8, -6, -5])
    hi = lo + 10 if R.random() < 0.6 else lo + 12
    v = R.randint(lo + 1, hi - 1)
    if v == 0:
        return None
    return M(retta(lo, hi, 1, [(v, "A")], [lo, 0, hi]) + "Quale numero indica la freccia A?", num(v),
             [num(-v), num(v + 1), num(v - 1)], "Conta le tacche partendo dallo 0: A è <b>%s</b>." % num(v))


def s2_confronta():
    a, b = R.sample(range(-15, 16), 2)
    if R.random() < 0.6:
        a, b = -abs(a) or -1, -abs(b) or -2
        if a == b:
            return None
    g = max(a, b)
    return M("Qual è il numero maggiore: %s o %s?" % (num(a), num(b)), num(g), [num(min(a, b)), "sono uguali", "non si può sapere"],
             "Sulla retta è più grande il numero più a destra. <b>%s</b> &gt; %s.%s" % (num(g), num(min(a, b)), " Tra due negativi è maggiore quello più vicino allo zero." if g < 0 else ""))


def s2_ordina():
    ns = R.sample(range(-12, 13), 4)
    if sum(1 for x in ns if x < 0) < 2:
        return None
    o = sorted(ns)
    f = lambda L: "; ".join(num(x) for x in L)
    sh = ns[:]
    R.shuffle(sh)
    return M("Metti in ordine crescente: %s" % f(sh), f(o), [f(sorted(ns, key=abs)), f(o[::-1]), f(sorted([x for x in o if x >= 0]) + sorted([x for x in o if x < 0], key=abs)), f([o[1], o[0]] + o[2:]), f(o[:2] + [o[3], o[2]])],
             "Dal più piccolo al più grande, come sulla retta da sinistra a destra: <b>%s</b>." % f(o))


def s2_freddo():
    cs = R.sample(["Bolzano", "Aosta", "Trento", "Cortina", "Sestriere", "Livigno", "Belluno"], 4)
    ts = R.sample(range(-12, 4), 4)
    i = ts.index(min(ts))
    return M("Temperature di una mattina d’inverno: %s. Dove fa più freddo?" % ", ".join("%s %s" % (c, gr(t)) for c, t in zip(cs, ts)), cs[i],
             [c for c in cs if c != cs[i]], "La temperatura più bassa è %s: fa più freddo a <b>%s</b>." % (gr(ts[i]), cs[i]))


def s3_variazione():
    t = R.randint(-8, 6)
    d = R.randint(2, 9)
    up = R.random() < 0.5
    r = t + d if up else t - d
    w = [t - d if up else t + d, -(abs(t) + d) if up and t < 0 else r + 2, r - 1, -r if r else 3]
    return M("Alle 7 ci sono %s. La temperatura %s di %d gradi. Quale temperatura c’è ora?" % (gr(t), "sale" if up else "scende", d), gr(r),
             [gr(x) for x in w if x != r], "Parti da %s e conta %d passi %s sulla retta: <b>%s</b>." % (gr(t), d, "a destra" if up else "a sinistra", gr(r)))


def s3_differenza():
    a = R.randint(-9, -1)
    b = R.randint(1, 12)
    d = b - a
    return M("Di notte ci sono %s, a mezzogiorno %s. Di quanti gradi è salita la temperatura?" % (gr(a), gr(b)), "%d gradi" % d,
             ["%d gradi" % (b + a) if b + a > 0 else "%d gradi" % (d + 2), "%d gradi" % (d - 1), "%d gradi" % abs(a)],
             "Da %s a 0 ci sono %d gradi, da 0 a %s altri %d: %d + %d = <b>%d gradi</b>." % (gr(a), -a, gr(b), b, -a, b, d))


def s4_conta():
    a, b = sorted(R.sample(range(-9, 10), 2))
    if a >= 0 or b <= 0:
        return None
    n = b - a - 1
    return M("Quanti numeri interi ci sono tra %s e %s (esclusi)?" % (num(a), num(b)), str(n), [str(n + 1), str(n + 2), str(b + a) if b + a > 0 and b + a != n else str(n - 1)],
             "Da %s a %s: %s. Sono <b>%d</b> (ricordati dello zero)." % (num(a + 1), num(b - 1), ", ".join(num(x) for x in range(a + 1, b)) if n <= 12 else "…", n))


def s4_opposto():
    n = R.randint(1, 30) * R.choice([1, -1])
    return M("Qual è l’opposto di %s?" % z(n), z(-n), [z(n), "0", z(-n * 10)],
             "L’opposto ha la stessa distanza dallo zero ma il segno contrario: <b>%s</b>." % z(-n))


def s5():
    p = K.next()
    k = R.choice(["ascensore", "frigo", "saldo", "monte", "anni", "gioco"])
    if k == "ascensore":
        a, b = R.randint(-3, -1), R.randint(2, 7)
        return M("%s prende l’ascensore al piano %s e sale di %d piani. A che piano arriva?" % (p[0], num(a), b), num(a + b),
                 [num(a - b), num(b - a), num(a + b + 1)], "%s + %d = <b>%s</b>." % (num(a), b, num(a + b)))
    if k == "frigo":
        a, b = R.randint(3, 6), R.randint(15, 22)
        return M("Nel frigorifero ci sono +%d °C, nel congelatore −%d °C. Quanti gradi di differenza ci sono?" % (a, b), "%d gradi" % (a + b),
                 ["%d gradi" % (b - a), "%d gradi" % (a + b + 1), "%d gradi" % b], "%d gradi fino a 0 e %d sotto lo zero: %d + %d = <b>%d gradi</b>." % (a, b, a, b, a + b))
    if k == "saldo":
        a, b = R.randint(20, 80), R.randint(90, 150)
        return M("%s ha 0 € e deve %d € alla sorella (−%d €). Poi riceve %d €. Quanti euro ha dopo aver pagato il debito?" % (p[0], a, a, b), "%d €" % (b - a),
                 ["%d €" % (a + b), num(a - b) + " €", "%d €" % b], "%s + %d = <b>%d €</b>." % (num(-a), b, b - a))
    if k == "monte":
        a, b = R.randint(500, 1500), R.randint(10, 80)
        return M("Un rifugio è a %s m sul livello del mare; un lago ha il fondo a −%d m. Quanti metri di dislivello ci sono?" % (num(a), b), "%s m" % num(a + b),
                 ["%s m" % num(a - b), "%s m" % num(a), "%s m" % num(a + b + 100)], "%s + %d = <b>%s m</b>." % (num(a), b, num(a + b)))
    if k == "anni":
        a = R.choice([753, 509, 323, 264, 146, 44])
        b = R.choice([476, 800, 1492])
        return M("Un evento storico avvenne nel %d a.C. e un altro nel %d d.C. Quanti anni passarono (senza anno zero)?" % (a, b), num(a + b - 1),
                 [num(b - a), num(a + b), num(a + b + 1)], "Dal %d a.C. al 1 d.C. passano %d anni, poi altri %d: %d + %d − 1 = <b>%s</b>." % (a, a, b, a, b, num(a + b - 1)))
    a, b, c = R.randint(3, 9), R.randint(5, 12), R.randint(2, 6)
    return M("In un gioco %s ha %d punti, poi ne perde %d e poi ne vince %d. Quanti punti ha alla fine?" % (p[0], a, b, c), num(a - b + c),
             [num(a + b + c), num(a - b - c), num(b - a + c)], "%d − %d + %d = <b>%s</b>." % (a, b, c, num(a - b + c)))


def main():
    seen = set()
    sets = [
        ("I numeri relativi intorno a noi", mix(R, seen, [(s1_realta, 12), (s1_retta, 8)])),
        ("Confrontare e ordinare", mix(R, seen, [(s2_confronta, 10), (s2_ordina, 6), (s2_freddo, 4)])),
        ("Salire e scendere", mix(R, seen, [(s3_variazione, 12), (s3_differenza, 8)])),
        ("Sulla retta: contare e opposti", mix(R, seen, [(s4_conta, 10), (s4_opposto, 10)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["I <b>numeri relativi</b> hanno un segno: + (positivi) e − (negativi). Lo zero non è né positivo né negativo.",
         "Si usano per temperature sotto lo zero, piani sotto terra, profondità sotto il mare, debiti.",
         "Sulla retta i negativi sono a sinistra dello zero. È maggiore il numero più a destra: −3 &gt; −8.",
         "Quando la temperatura sale ti sposti a destra, quando scende a sinistra."],
        [("Ci sono −4 °C e la temperatura sale di 6 gradi.", ["da −4 a 0: 4 gradi", "altri 2 gradi: +2"], "+2 °C")],
        [["Dire che −8 è maggiore di −3", "Tra due negativi è maggiore quello più vicino allo zero: −3."],
         ["Dimenticare lo zero contando", "Sulla retta lo zero è un passo come gli altri."],
         ["Da −2 salire di 5 e scrivere −7", "Salire vuol dire andare verso destra: −2 + 5 = +3."]],
        retta(-6, 6, 1, [], [-6, -3, 0, 3, 6]))
    faq = [("Lo zero è positivo o negativo?", "Nessuno dei due: lo zero separa i numeri positivi da quelli negativi."),
           ("Perché −3 è maggiore di −8?", "Perché sulla retta −3 è più a destra: con −3 °C fa meno freddo che con −8 °C.")]
    make_unit(R, "numeri-relativi", "N",
              "Interpretare i numeri interi negativi in contesti concreti (temperature, piani, altitudini, debiti); rappresentarli sulla retta, confrontarli e ordinarli",
              "I numeri relativi: positivi e negativi", "Numeri relativi",
              "Schede di matematica per la classe quinta sui numeri relativi: positivi e negativi, temperature, retta, confronti, salire e scendere, opposti e problemi. 100 esercizi con soluzioni.",
              "Sulla retta è maggiore il numero più a destra.", "−3 è maggiore di −8.",
              body, faq, sets, 2, grade=G)


if __name__ == "__main__":
    main()
