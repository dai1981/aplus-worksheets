# -*- coding: utf-8 -*-
"""
Italia Matematica terza media: Numeri relativi (Numeri)
  python3 tools/gen_it_matematica_m3_numeri_relativi.py
Numeri relativi interi e razionali (ℤ, ℚ), retta orientata, valore assoluto, numeri opposti e concordi/discordi,
confronto e ordinamento (anche con frazioni e decimali), numeri relativi nella realtà (temperature, altitudini, saldi).
Errori: −8 > −3 perché 8 > 3, |−5| = −5, confondere opposto e reciproco.
"""
import random
from fractions import Fraction as Fr
from it_media import M, L, unit, mix, table, W, fq, sgn, d, Kids
from it_common import retta

R = random.Random(71301)
G = "terza-media"
K = Kids(R)


def s1_retta():
    lo = R.choice([-10, -8, -6, -5])
    hi = lo + 12
    x = R.randint(lo + 1, hi - 1)
    if x == 0:
        return None
    pic = retta(lo, hi, 1, marks=[(x, "A")], every=2 if lo % 2 == 0 else 1)
    return M("%sQuale numero corrisponde al punto A?" % pic, sgn(x), W(sgn(-x), sgn(x + 1), sgn(x - 1)), "A si trova %s dello zero, a %d unità: <b>%s</b>." % ("a destra" if x > 0 else "a sinistra", abs(x), sgn(x)))


def s1_def():
    k = R.choice(["abs", "opp", "conc", "abs2"])
    if k == "abs":
        x = Fr(R.choice([-1, 1]) * R.randint(1, 30))
        if R.random() < 0.3:
            x = Fr(R.choice([-1, 1]) * R.randint(1, 9), R.choice([2, 3, 4, 5]))
        return M("Qual è il valore assoluto di %s?" % sgn(x), fq(abs(x)), W(sgn(-abs(x)), "0", fq(1 / abs(x)) if abs(x) != 1 else "2", fq(abs(x) + 1)),
                 "Il valore assoluto è il numero senza segno: |%s| = <b>%s</b>." % (sgn(x), fq(abs(x))))
    if k == "opp":
        x = Fr(R.choice([-1, 1]) * R.randint(1, 30))
        if R.random() < 0.4:
            x = Fr(R.choice([-1, 1]) * R.randint(1, 9), R.choice([2, 3, 4, 5, 7]))
            if x.denominator == 1:
                return None
        return M("Qual è l’opposto di %s?" % sgn(x), sgn(-x), W(sgn(1 / x), sgn(-1 / x), fq(abs(x)) if x > 0 else sgn(x - 1)),
                 "L’opposto ha lo stesso valore assoluto e segno contrario: <b>%s</b>." % sgn(-x))
    if k == "conc":
        a, b = R.randint(1, 20), R.randint(1, 20)
        sa, sb = R.choice([1, -1]), R.choice([1, -1])
        same = sa == sb
        ans = "concordi" if same else "discordi"
        return M("I numeri %s e %s sono…" % (sgn(sa * a), sgn(sb * b)), ans, ["discordi" if same else "concordi", "opposti", "uguali"],
                 "Hanno %s segno: <b>%s</b>." % ("lo stesso" if same else "segno diverso, cioè", ans) if same else "Hanno segno diverso: <b>discordi</b>.")
    a = R.randint(2, 15)
    return M("Quali numeri hanno valore assoluto %d?" % a, "+%d e −%d" % (a, a), ["solo +%d" % a, "solo −%d" % a, "+%d e 0" % a], "Sia +%d sia −%d distano %d dallo zero: <b>+%d e −%d</b>." % (a, a, a, a, a))


def s2_confronto():
    k = R.choice(["int", "int", "dec", "frac"])
    if k == "int":
        a, b = R.randint(-20, 20), R.randint(-20, 20)
    elif k == "dec":
        a, b = Fr(R.randint(-99, 99), 10), Fr(R.randint(-99, 99), 10)
    else:
        a, b = Fr(R.randint(-9, 9), R.choice([2, 3, 4, 5])), Fr(R.randint(-9, 9), R.choice([2, 3, 4, 5]))
    if a == b or (a >= 0 and b >= 0) or abs(a) == abs(b):
        return None
    rel = "&lt;" if a < b else "&gt;"
    show = lambda x: fq(x) if x.denominator not in (2, 5, 10) or k == "frac" else d(x)
    if k == "dec":
        show = lambda x: (("+" if x > 0 else "") + d(x)) if x != 0 else "0"
    else:
        show = lambda x: sgn(x) if x != 0 else "0"
    return M("Quale simbolo va tra %s ☐ %s ?" % (show(a), show(b)), rel, ["&gt;" if rel == "&lt;" else "&lt;", "=", "non si può dire"],
             "Sulla retta, %s sta più a %s di %s: %s <b>%s</b> %s." % (show(a), "sinistra" if a < b else "destra", show(b), show(a), rel, show(b)))


def s2_ordina():
    xs = sorted(R.sample(range(-15, 16), 4))
    if all(x >= 0 for x in xs) or all(x < 0 for x in xs):
        return None
    sh = xs[:]
    R.shuffle(sh)
    asc = R.random() < 0.6
    good = xs if asc else xs[::-1]
    f = lambda l: "; ".join(sgn(x) if x else "0" for x in l)
    wrong1 = sorted(xs, key=lambda x: (abs(x), x))
    wrong2 = good[::-1]
    wrong3 = sorted(xs, key=lambda x: -abs(x))
    return M("Ordina dal %s al %s: %s" % ("minore" if asc else "maggiore", "maggiore" if asc else "minore", f(sh)), f(good), W(f(wrong1), f(wrong2), f(wrong3), f(sh), f([good[0], good[2], good[1], good[3]]), f([good[1], good[0], good[2], good[3]])),
             "Sulla retta i numeri crescono da sinistra a destra: <b>%s</b>." % f(good))


def s3_insiemi():
    q, a, w = R.choice([
        ("Il numero −7 appartiene all’insieme…", "ℤ dei numeri interi relativi", ["ℕ dei numeri naturali", "solo ℚ ma non ℤ", "nessuno"]),
        ("Il numero −3/4 appartiene a…", "ℚ ma non a ℤ", ["ℤ ma non a ℚ", "ℕ", "ℤ e ℕ"]),
        ("Quale numero è intero relativo ma non naturale?", "−5", ["5", "1/2", "0"]),
        ("Quale di questi numeri non è razionale?", "√2", ["−3", "0,25", "−5/7"]),
        ("Tra due numeri negativi è maggiore…", "quello con il valore assoluto minore", ["quello con il valore assoluto maggiore", "sempre il primo", "non si può dire"]),
        ("Lo zero è…", "né positivo né negativo", ["positivo", "negativo", "sia positivo sia negativo"]),
        ("Un numero negativo è sempre…", "minore di qualsiasi numero positivo", ["maggiore di zero", "maggiore del suo opposto", "uguale al suo valore assoluto"]),
        ("Due numeri opposti hanno…", "lo stesso valore assoluto e segno diverso", ["lo stesso segno", "valore assoluto diverso", "somma 1"]),
        ("Quale numero è il più piccolo?", "−0,9", ["−0,09", "0", "−0,1"]),
        ("Quale numero è il più grande?", "−1/4", ["−1/2", "−3/4", "−1"]),
    ])
    return M(q, a, w, "Risposta: <b>%s</b>." % a)


def t(x):
    return sgn(x) if x else "0"


def s4_realta():
    p = K.next()
    k = R.choice(["temp", "alt", "saldo", "piani", "storia", "escursione"])
    if k == "temp":
        a = R.randint(-12, 8)
        v = R.randint(3, 15)
        up = R.random() < 0.5
        b = a + v if up else a - v
        return M("Alle 7 la temperatura è %s °C. Durante la giornata %s di %d gradi. Quanti gradi ci sono adesso?" % (t(a), "sale" if up else "scende", v), "%s °C" % t(b), W("%s °C" % t(a - v if up else a + v), "%s °C" % t(-b) if b else "+1 °C", "%s °C" % t(v), "%s °C" % t(b + 1)),
                 "%s %s %d = <b>%s °C</b>." % (t(a), "+" if up else "−", v, t(b)))
    if k == "escursione":
        mn, mx = R.randint(-15, -1), R.randint(1, 20)
        return M("In una giornata d’inverno la temperatura minima è stata %s °C e la massima +%d °C. Qual è stata l’escursione termica?" % (t(mn), mx), "%d °C" % (mx - mn), W("%d °C" % abs(mx + mn), "%d °C" % (mx - mn + 1), "%d °C" % abs(mn), "%d °C" % mx),
                 "Escursione: %d − (%s) = %d + %d = <b>%d °C</b>." % (mx, t(mn), mx, -mn, mx - mn))
    if k == "alt":
        a = R.randint(2, 40) * 50
        b = R.randint(1, 20) * 10
        return M("La cima di un monte è a %s m sul livello del mare e un sommergibile è a %d m sotto il livello del mare. Qual è la differenza di quota?" % (d(a), b), "%s m" % d(a + b), W("%s m" % d(a - b), "%s m" % d(b - a) if b > a else "%s m" % d(a), "%s m" % d(a + b + 10)),
                 "%s − (−%d) = %s + %d = <b>%s m</b>." % (d(a), b, d(a), b, d(a + b)))
    if k == "saldo":
        s0 = R.randint(20, 200)
        sp = s0 + R.randint(10, 150)
        return M("Sul conto di %s ci sono %d €. Paga una spesa di %d €. Qual è il saldo?" % (p[0], s0, sp), "%s €" % sgn(s0 - sp), W("%d €" % (sp - s0), "%s €" % sgn(s0 + sp), "%s €" % sgn(s0 - sp - 10)),
                 "%d − %d = <b>%s €</b> (saldo negativo)." % (s0, sp, sgn(s0 - sp)))
    if k == "piani":
        a = R.randint(-3, 2)
        v = R.randint(2, 8)
        b = a + v
        return M("Un ascensore parte dal piano %s e sale di %d piani. A che piano arriva?" % (sgn(a) if a else "0 (piano terra)", v), sgn(b) if b else "0", W(t(a - v), t(b + 1), t(v), t(-b), t(b - 1)),
                 "%s + %d = <b>%s</b>." % (sgn(a) if a else "0", v, sgn(b) if b else "0"))
    a = R.randint(100, 800)
    b = R.randint(1000, 2025)
    return M("Un evento storico è avvenuto nel %d a.C. (anno −%d) e un altro nel %d d.C. Quanti anni sono passati tra i due (senza anno zero)?" % (a, a, b), str(a + b - 1), W(str(b - a), str(a + b), str(a + b + 1)),
             "Da −%d a +%d ci sono %d + %d = %d anni, meno 1 perché non c’è l’anno zero: <b>%d</b>." % (a, b, a, b, a + b, a + b - 1))


def main():
    seen = set()
    sets = [
        ("La retta dei numeri relativi", mix(R, seen, [(s1_retta, 10), (s1_def, 10)])),
        ("Valore assoluto e opposto", mix(R, seen, [(s1_def, 20)])),
        ("Confrontare e ordinare", mix(R, seen, [(s2_confronto, 12), (s2_ordina, 8)])),
        ("Gli insiemi ℤ e ℚ", mix(R, seen, [(s3_insiemi, 10), (s2_confronto, 10)])),
        ("Numeri relativi nella realtà", mix(R, seen, [(s4_realta, 20)])),
    ]
    body = L(["I <b>numeri relativi</b> hanno un segno: positivi (+3) e negativi (−3). Gli interi relativi formano ℤ, i razionali relativi (anche frazioni e decimali) formano ℚ.",
              "Sulla <b>retta orientata</b> i positivi sono a destra dello zero, i negativi a sinistra. Più un numero è a destra, più è grande.",
              "Il <b>valore assoluto</b> è il numero senza segno: |−7| = 7. Due numeri sono <b>opposti</b> se hanno lo stesso valore assoluto e segno diverso (+5 e −5).",
              "Due numeri sono <b>concordi</b> se hanno lo stesso segno, <b>discordi</b> se hanno segno diverso."],
             [("Confronta −8 e −3", ["−8 è più a sinistra"], "−8 &lt; −3")],
             [["−8 &gt; −3 perché 8 &gt; 3", "Tra due negativi è maggiore quello più vicino allo zero."],
              ["|−5| = −5", "Il valore assoluto non è mai negativo."],
              ["Confondere opposto e reciproco", "L’opposto di 2 è −2; il reciproco di 2 è 1/2."]],
             table(["Numero", "Valore assoluto", "Opposto"], [["+4", "4", "−4"], ["−7", "7", "+7"], ["−2/3", "2/3", "+2/3"]]))
    faq = [("Lo zero è positivo o negativo?", "Nessuno dei due: lo zero è il punto di partenza della retta e non ha segno."),
           ("Perché −10 è minore di −2?", "Perché sulla retta −10 è più a sinistra: fa più freddo a −10 °C che a −2 °C.")]
    unit(G, R, "numeri-relativi", "N",
         "Eseguire operazioni, ordinamenti e confronti tra i numeri conosciuti (numeri naturali, numeri interi, frazioni e numeri decimali); rappresentare i numeri conosciuti sulla retta",
         "Numeri relativi", "Numeri relativi",
         "Schede di matematica per la terza media sui numeri relativi: retta orientata, valore assoluto, numeri opposti, concordi e discordi, confronto e ordinamento, insiemi ℤ e ℚ, problemi con temperature e quote. 100 esercizi con soluzioni.",
         "Sulla retta: più a destra, più grande.", "|−7| = 7; l’opposto di +5 è −5.",
         body, faq, sets, 1)


if __name__ == "__main__":
    main()
