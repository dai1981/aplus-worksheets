# -*- coding: utf-8 -*-
"""
Italia Matematica classe quinta: I numeri decimali (Numeri)
  python3 tools/gen_it_matematica_c5_numeri_decimali.py
Decimi, centesimi, millesimi; frazioni decimali e numeri decimali; valore delle cifre; confrontare e ordinare;
arrotondare all’unità, al decimo, al centesimo; numeri decimali sulla retta; problemi con misure e prezzi.
Errori: 0,25 &gt; 0,3 perché 25 &gt; 3, 7/100 = 0,7, arrotondare guardando la cifra sbagliata.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, fr, retta, table, NB

R = random.Random(70504)
G = "classe-quinta"


def D(n, p, trim=True):
    """intero n con p cifre decimali → stringa (1234, 3 → 1,234)"""
    neg = n < 0
    n = abs(n)
    ip, fp_ = divmod(n, 10 ** p)
    s = str(fp_).rjust(p, "0") if p else ""
    if trim:
        s = s.rstrip("0")
    return ("−" if neg else "") + num(ip) + ("," + s if s else "")


NOMI = {1: ("decimo", "decimi"), 2: ("centesimo", "centesimi"), 3: ("millesimo", "millesimi")}


def tab(n, p):
    s = str(n).rjust(p + 2, "0")
    ip, fp_ = s[:-p], s[-p:]
    ip = str(int(ip)).rjust(2, " ")
    head = ["da", "u", "d", "c", "m"][:2 + p]
    cells = list(ip) + list(fp_)
    return ("<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr>%s</tr></thead><tbody><tr>%s</tr></tbody></table>"
            % ("".join("<th>%s</th>" % h for h in head), "".join("<td style='text-align:center;min-width:28px'>%s%s</td>" % (c.strip(), "," if i == 1 else "") for i, c in enumerate(cells))))


def s1_frazione():
    p = R.choice([1, 2, 3])
    k = R.randint(1, 10 ** p - 1)
    if k % 10 == 0 and p > 1:
        return None
    w = [D(k, p - 1) if p > 1 else D(k, 2), D(k, p + 1), "%d,%d" % (k, 10 ** p) if p == 1 else str(k), "%d,%d" % (10 ** p, k), D(k, p + 2)]
    return mcq("Come si scrive %s come numero decimale?" % fr(k, 10 ** p), D(k, p), w,
               "%s = %d %s: dopo la virgola ci devono essere %d %s. <b>%s</b>." % (fr(k, 10 ** p), k, NOMI[p][0 if k == 1 else 1], p, "cifra" if p == 1 else "cifre", D(k, p)))


def s1_tabella():
    p = R.choice([2, 3])
    n = R.randint(100, 99999 if p == 3 else 9999)
    if n % 10 == 0:
        return None
    return mcq(tab(n, p) + "Quale numero è scritto nella tabella?", D(n, p), [D(n, p - 1), D(n, p + 1), D(int(str(n)[::-1]), p) if str(n)[-1] != "0" else D(n + 1, p), str(n)],
               "Prima della virgola da e u, dopo la virgola d, c%s: <b>%s</b>." % (", m" if p == 3 else "", D(n, p)))


def s2_valore():
    n = R.randint(10001, 99999)
    v = D(n, 3, trim=False)
    ds = v.replace(",", "")
    i = R.randrange(len(ds))
    d = ds[i]
    if d == "0":
        return None
    names = ["decine", "unità", "decimi", "centesimi", "millesimi"]
    vals = [D(int(d) * 10, 0), d, D(int(d), 1), D(int(d), 2), D(int(d), 3)]
    return mcq("Nel numero %s quanto vale la cifra %s che sta nei %s?" % (v, d, names[i]) if i >= 2 else
               "Nel numero %s quanto vale la cifra %s che sta nelle %s?" % (v, d, names[i]), vals[i], [x for j, x in enumerate(vals) if j != i],
               "%s %s = <b>%s</b>." % (d, names[i], vals[i]))


def s2_equivalenti():
    k = R.choice(["dc", "cm", "zero"])
    a = R.randint(1, 9)
    if k == "dc":
        return mcq("%s decimi sono uguali a…" % a, "%d centesimi" % (a * 10), ["%d centesimi" % a, "%d millesimi" % (a * 10), "%d unità" % (a * 10)],
                   "1 decimo = 10 centesimi: <b>%d centesimi</b> (%s = %s)." % (a * 10, D(a, 1), D(a * 10, 2, trim=False)))
    if k == "cm":
        return mcq("%s centesimi sono uguali a…" % a, "%d millesimi" % (a * 10), ["%d millesimi" % a, "%d decimi" % (a * 10), "%d millesimi" % (a * 100)],
                   "1 centesimo = 10 millesimi: <b>%d millesimi</b>." % (a * 10))
    b = R.randint(1, 99)
    if b % 10 == 0:
        return None
    return mcq("Quale numero è uguale a %s?" % D(b, 2), D(b * 10, 3, trim=False), [D(b, 3), D(b, 1) if b < 10 else D(b * 100, 2), D(b + 1, 2)],
               "Uno zero alla fine della parte decimale non cambia il valore: %s = <b>%s</b>." % (D(b, 2), D(b * 10, 3, trim=False)))


def s3_confronta():
    k = R.choice(["lung", "lung", "stessa"])
    if k == "lung":
        a = R.randint(1, 9)
        b = R.randint(11, 99)
        if b // 10 == a or b % 10 == 0:
            return None
        A, B = D(a, 1), D(b, 2)
        va, vb = a * 10, b
        if R.random() < 0.5:
            A, B = D(a * 10 + R.randint(1, 9), 2), D(R.randint(100, 999), 3)
            va, vb = int(A.split(",")[1]) * 10, int(B.split(",")[1])
            if va == vb or B.endswith("0"):
                return None
    else:
        a, b = R.sample(range(101, 999), 2)
        A, B = D(a, 2), D(b, 2)
        va, vb = a, b
    g, s_ = (A, B) if va > vb else (B, A)
    return mcq("Qual è il numero maggiore: %s o %s?" % (A, B), g, [s_, "sono uguali", "non si può sapere"],
               "Confronta posto per posto: prima la parte intera, poi i decimi, i centesimi, i millesimi. <b>%s</b> è maggiore." % g)


def s3_ordina():
    base = R.randint(1, 9)
    vals = sorted(set(R.sample(range(base * 1000 + 1, base * 1000 + 999), 4)))
    strs = [D(v, 3) for v in vals]
    if any(s.count(",") == 0 for s in strs):
        return None
    f = lambda L: "; ".join(L)
    sh = strs[:]
    R.shuffle(sh)
    bylen = sorted(strs, key=lambda s: (len(s), s))
    return mcq("Metti in ordine crescente: %s" % f(sh), f(strs), [f(strs[::-1]), f(bylen), f([strs[1], strs[0]] + strs[2:]), f(strs[:2] + strs[:1:-1])],
               "Confronta i decimi, poi i centesimi, poi i millesimi: <b>%s</b>." % f(strs))


def s4_arrotonda():
    n = R.randint(1001, 99999)
    p = 3
    k = R.choice([(0, "all’unità"), (1, "al decimo"), (2, "al centesimo")])
    q, t = k
    step = 10 ** (p - q)
    r = (n + step // 2) // step * step
    if n % step == 0:
        return None
    w = [n // step * step if r != n // step * step else r + step, (n + step * 5) // (step * 10) * step * 10, r + step]
    fmt = lambda x: D(x // (10 ** (p - q)), q, trim=False) if q else num(x // 1000)
    return mcq("Arrotonda %s %s." % (D(n, 3, trim=False), t), fmt(r), [fmt(x) for x in w] + [D(n, 3, trim=False)],
               "Guarda la cifra subito a destra: %s. <b>%s</b>." % ("5 o più, arrotondi per eccesso" if r > n else "meno di 5, arrotondi per difetto", fmt(r)))


def s4_retta():
    a = R.randint(0, 8)
    step = R.choice([1, 1, 5])
    v = R.randint(1, 9) * (1 if step == 1 else 1)
    lo, hi = a * 10, a * 10 + 10
    mk = lo + v
    lab = lambda x: D(x, 1)
    pic = retta(lo, hi, 1, [(mk, "A")], [lo, hi]).replace(">%s<" % num(lo), ">%s<" % D(lo, 1)).replace(">%s<" % num(hi), ">%s<" % D(hi, 1))
    return mcq(pic + "Quale numero decimale indica la freccia A?", D(mk, 1), [D(mk + 1, 1), D(mk - 1, 1), D(mk, 2) if mk % 10 else D(mk + 2, 1), str(mk)],
               "Tra %s e %s ci sono 10 parti: ogni tacca vale 0,1. A = <b>%s</b>." % (D(lo, 1), D(hi, 1), D(mk, 1)))


def s5():
    k = R.choice(["salto", "salto", "prezzo", "corsa", "peso"])
    if k == "salto":
        cs = R.sample(["Luca", "Sofia", "Marco", "Giulia", "Pietro"], 3)
        ms = R.sample(range(280, 420), 3)
        i = ms.index(max(ms))
        return mcq("Nel salto in lungo: %s. Chi ha saltato di più?" % ", ".join("%s %s m" % (c, D(m, 2)) for c, m in zip(cs, ms)), cs[i],
                   [c for c in cs if c != cs[i]] + ["hanno saltato uguale"], "Il numero maggiore è %s m: <b>%s</b>." % (D(ms[i], 2), cs[i]))
    if k == "prezzo":
        n = R.randint(1601, 1999)
        if n % 10 == 0:
            return None
        r = (n + 5) // 10 * 10
        o = n // 10 * 10 if r != n // 10 * 10 else r + 10
        return mcq("Un litro di benzina costa %s €. Quanto costa arrotondato al centesimo?" % D(n, 3), D(r, 3, trim=False)[:-1] + " €",
                   [D(o, 3, trim=False)[:-1] + " €", D((n + 50) // 100, 1) + " €", D(n, 3) + " €"],
                   "Guarda i millesimi (%d): %s. <b>%s €</b>." % (n % 10, "arrotondi per eccesso" if n % 10 >= 5 else "arrotondi per difetto", D(r, 3, trim=False)[:-1]))
    if k == "corsa":
        ts = R.sample(range(1150, 1450), 4)
        cs = ["A", "B", "C", "D"]
        i = ts.index(min(ts))
        return mcq("Nei 100 metri: corsia A %s s, B %s s, C %s s, D %s s. Quale corsia ha vinto?" % tuple(D(t, 2) for t in ts), "la corsia " + cs[i],
                   ["la corsia " + c for c in cs if c != cs[i]], "Vince chi impiega meno tempo: %s s, <b>la corsia %s</b>." % (D(ts[i], 2), cs[i]))
    if k == "peso":
        a = R.randint(1100, 4900)
        if a % 10 == 0:
            return None
        return mcq("Un pacco pesa %s kg. Quanti grammi sono?" % D(a, 3), num(a) + " g", [num(a // 10) + " g", num(a * 10) + " g", D(a, 3) + " g"],
                   "1 kg = 1000 g: i millesimi di kg sono grammi. <b>%s g</b>." % num(a))
    n = R.randint(10, 99)
    return mcq("In una gara di nuoto il tempo di Anna è %s s. Quanti decimi di secondo sono?" % D(n, 1), "%d decimi" % n, ["%d decimi" % (n // 10), "%d decimi" % (n % 10), "%d decimi" % (n * 10)],
               "%s s = %d unità e %d decimi = <b>%d decimi</b>." % (D(n, 1), n // 10, n % 10, n))


def main():
    seen = set()
    sets = [
        ("Frazioni decimali e numeri decimali", mix(R, seen, [(s1_frazione, 12), (s1_tabella, 8)])),
        ("Valore delle cifre", mix(R, seen, [(s2_valore, 12), (s2_equivalenti, 8)])),
        ("Confrontare e ordinare", mix(R, seen, [(s3_confronta, 14), (s3_ordina, 6)])),
        ("Arrotondare e retta", mix(R, seen, [(s4_arrotonda, 12), (s4_retta, 8)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Dividendo l’unità in 10, 100, 1000 parti si ottengono <b>decimi</b>, <b>centesimi</b>, <b>millesimi</b>: %s = 0,1; %s = 0,01; %s = 0,001." % (fr(1, 10), fr(1, 100), fr(1, 1000)),
         "Dopo la virgola: 1º posto decimi (d), 2º centesimi (c), 3º millesimi (m).",
         "Per confrontare non guardare quante cifre ci sono: confronta posto per posto. 0,3 = 0,30 &gt; 0,25.",
         "Per arrotondare guarda la cifra subito a destra del posto richiesto: da 5 in su si arrotonda per eccesso."],
        [("Scrivi %s come numero decimale." % fr(45, 1000), ["millesimi: 3 cifre dopo la virgola", "45 → 045"], "0,045"),
         ("Arrotonda 3,476 al decimo.", ["cifra dei centesimi: 7, cioè 5 o più"], "3,5")],
        [["Pensare che 0,25 &gt; 0,3", "Aggiungi uno zero: 0,30 &gt; 0,25."],
         ["Scrivere %s = 0,7" % fr(7, 100), "Centesimi: due cifre dopo la virgola, 0,07."],
         ["Arrotondare al decimo guardando i millesimi", "Guarda la cifra subito dopo il decimo: i centesimi."]],
        table(["da", "u", "d", "c", "m"], [["10", "1", "0,1", "0,01", "0,001"]]))
    faq = [("Uno zero alla fine cambia un numero decimale?", "No: 2,5 = 2,50 = 2,500. Cambia invece se lo zero è subito dopo la virgola: 2,05 è diverso da 2,5."),
           ("Dove si usano i millesimi?", "Nelle misure (1,250 kg = 1 kg e 250 g), nei tempi delle gare e nei prezzi del carburante.")]
    make_unit(R, "numeri-decimali", "N",
              "Leggere, scrivere, confrontare numeri decimali fino ai millesimi; rappresentarli sulla retta; utilizzare numeri decimali e frazioni decimali per descrivere situazioni quotidiane",
              "I numeri decimali fino ai millesimi", "Numeri decimali",
              "Schede di matematica per la classe quinta sui numeri decimali: decimi, centesimi e millesimi, frazioni decimali, valore delle cifre, confronti, arrotondamenti, retta e problemi. 100 esercizi con soluzioni.",
              "Decimi, centesimi, millesimi: 1º, 2º e 3º posto dopo la virgola.", "0,3 = 0,30 è maggiore di 0,25.",
              body, faq, sets, 4, grade=G)


if __name__ == "__main__":
    main()
