# -*- coding: utf-8 -*-
"""
Italia Matematica classe quinta: I grandi numeri (Numeri)
  python3 tools/gen_it_matematica_c5_grandi_numeri.py
Classi (unità semplici, migliaia, milioni, miliardi), valore posizionale, leggere e scrivere, scomporre,
confrontare e ordinare, arrotondare, + e − 1000 / 1 000 000, problemi con dati reali.
Errori: dimenticare gli zeri di una classe vuota, confondere cifra e valore, leggere a gruppi sbagliati.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, table

R = random.Random(70501)
G = "classe-quinta"
POS = [("unità", 1), ("decine", 10), ("centinaia", 100), ("unità di migliaia", 1000), ("decine di migliaia", 10 ** 4),
       ("centinaia di migliaia", 10 ** 5), ("unità di milioni", 10 ** 6), ("decine di milioni", 10 ** 7), ("centinaia di milioni", 10 ** 8), ("unità di miliardi", 10 ** 9)]


def big(lo=6, hi=9, zeros=0.3):
    k = R.randint(lo, hi)
    ds = [R.randint(1, 9)] + [0 if R.random() < zeros else R.randint(0, 9) for _ in range(k - 1)]
    return int("".join(map(str, ds)))


def tab(n):
    s = str(n).rjust(9, " ")
    head = ["h", "da", "u"] * 3
    top = "<tr><th colspan='3'>milioni</th><th colspan='3'>migliaia</th><th colspan='3'>unità semplici</th></tr>"
    return ("<table class='sn-table' style='width:auto;margin:6px 0'><thead>%s<tr>%s</tr></thead><tbody><tr>%s</tr></tbody></table>"
            % (top, "".join("<th>%s</th>" % h for h in head), "".join("<td style='text-align:center;min-width:24px'>%s</td>" % c.strip() for c in s)))


def near(n):
    s = str(n)
    out = []
    i = R.randrange(len(s))
    if len(s) > 4:
        out.append(int(s[:2] + s[3:]) if s[2] != "0" else int(s[:2] + "0" + s[2:]))
        out.append(int(s.replace("0", "", 1)) if "0" in s else n * 10)
    out += [n + 10 ** (len(s) - 2), n * 10, n // 10]
    return [num(x) for x in out if x != n and x > 0]


def s1_tabella():
    n = big(6, 9)
    return mcq(tab(n) + "Quale numero è scritto nella tabella?", num(n), near(n),
               "Leggi le classi da sinistra: milioni, migliaia, unità semplici. Il numero è <b>%s</b>." % num(n))


def s1_valore():
    n = big(6, 10, 0.1)
    s = str(n)
    i = R.randrange(len(s) - 1)
    d = int(s[i])
    if d == 0:
        return None
    p = len(s) - 1 - i
    name, v = POS[p]
    return mcq("Nel numero %s quanto vale la cifra <b>%d</b> che sta nelle %s?" % (num(n), d, name),
               num(d * v), [num(d * v * 10), num(d * v // 10) if v > 1 else num(d * 100), str(d), num(d * v * 100)],
               "%d %s valgono <b>%s</b>." % (d, name, num(d * v)))


MIL = [(10 ** 9, "miliardi", "miliardo"), (10 ** 6, "milioni", "milione"), (1000, "mila", "mille")]


def parole(n):
    out = []
    for v, p, s in MIL:
        k, n = divmod(n, v)
        if k:
            if v == 1000:
                out.append("mille" if k == 1 else "%s mila" % num(k))
            else:
                out.append("un %s" % s if k == 1 else "%s %s" % (num(k), p))
    if n:
        out.append(num(n))
    return " ".join(out)


def s2_lettere():
    n = big(7, 10, 0.5)
    w = parole(n)
    return mcq("Scrivi in cifre: <b>%s</b>" % w, num(n), near(n), "«%s» si scrive <b>%s</b>." % (w, num(n)))


def s2_scomponi():
    n = big(6, 8, 0.45)
    s = str(n)
    parts = [int(c) * 10 ** (len(s) - 1 - i) for i, c in enumerate(s) if c != "0"]
    if len(parts) < 3:
        return None
    sh = " + ".join(num(x) for x in parts)
    if R.random() < 0.5:
        return mcq("Quale numero è uguale a %s?" % sh, num(n), near(n), "%s = <b>%s</b>." % (sh, num(n)))
    w1 = " + ".join(num(x // 10) if j == 0 else num(x) for j, x in enumerate(parts))
    w2 = " + ".join(num(x * 10) if j == len(parts) - 1 else num(x) for j, x in enumerate(parts))
    w3 = " + ".join(num(x) for x in parts[:-1])
    return mcq("Qual è la scomposizione di %s?" % num(n), sh, [w1, w2, w3], "Ogni cifra diversa da 0 vale secondo il suo posto: <b>%s</b>." % sh)


def s3_confronta():
    a = big(6, 9, 0.2)
    k = R.choice(["cifre", "pos"])
    if k == "cifre":
        b = int(str(a)[:-1]) if R.random() < 0.5 else a * 10 + R.randint(0, 9)
    else:
        s = list(str(a))
        i = R.randrange(1, len(s))
        s[i] = str((int(s[i]) + R.randint(1, 9)) % 10)
        b = int("".join(s))
    if a == b:
        return None
    big_ = max(a, b)
    return mcq("Qual è il numero maggiore: %s o %s?" % (num(a), num(b)), num(big_), [num(min(a, b)), "sono uguali", "non si può sapere"],
               "%s. Il maggiore è <b>%s</b>." % ("Ha più cifre" if len(str(a)) != len(str(b)) else "Hanno le stesse cifre: confronta da sinistra la prima cifra diversa", num(big_)))


def s3_ordina():
    base = big(7, 7, 0.1)
    ns = sorted({base + R.choice([-1, 1]) * R.randint(1, 9) * 10 ** R.randint(2, 5) for _ in range(6)})[:4]
    if len(ns) < 4:
        return None
    f = lambda L: "; ".join(num(x) for x in L)
    sh = ns[:]
    R.shuffle(sh)
    w = ns[:]
    w[1], w[2] = w[2], w[1]
    return mcq("Metti in ordine crescente: %s" % f(sh), f(ns), [f(ns[::-1]), f(w), f(sorted(ns, key=lambda x: str(x)[::-1])), f(ns[:2] + ns[:1:-1]), f(ns[1:] + ns[:1])],
               "Dal più piccolo al più grande: <b>%s</b>." % f(ns))


def s4_arrotonda():
    n = big(6, 8, 0.1)
    k = R.choice([(1000, "alle migliaia"), (10 ** 4, "alle decine di migliaia"), (10 ** 5, "alle centinaia di migliaia"), (10 ** 6, "ai milioni")])
    v, t = k
    if v >= n:
        return None
    r = (n + v // 2) // v * v
    other = n // v * v if r != n // v * v else r + v
    return mcq("Arrotonda %s %s." % (num(n), t), num(r), [num(other), num((n + v * 5) // (v * 10) * v * 10), num((n + v // 20) // (v // 10) * (v // 10)), num(r + v), num(r - v) if r > v else None, num(n)],
               "Guarda la cifra a destra del posto richiesto: %s. <b>%s</b>." % ("5 o più, arrotondi per eccesso" if r > n else "meno di 5, arrotondi per difetto", num(r)))


def s4_piu():
    n = big(6, 8, 0.4)
    v = R.choice([1000, 10 ** 4, 10 ** 5, 10 ** 6])
    if R.random() < 0.5:
        r = n + v
        return mcq("Quanto fa %s + %s?" % (num(n), num(v)), num(r), [num(n + v // 10), num(n + v * 10), num(n + 1)],
                   "Aggiungi 1 al posto delle %s: <b>%s</b>." % ({1000: "unità di migliaia", 10 ** 4: "decine di migliaia", 10 ** 5: "centinaia di migliaia", 10 ** 6: "unità di milioni"}[v], num(r)))
    if n < v * 2:
        return None
    r = n - v
    return mcq("Quanto fa %s − %s?" % (num(n), num(v)), num(r), [num(n - v // 10), num(n - v * 10) if n > v * 10 else num(n + v), num(n - 1)],
               "Togli 1 al posto delle %s: <b>%s</b>." % ({1000: "unità di migliaia", 10 ** 4: "decine di migliaia", 10 ** 5: "centinaia di migliaia", 10 ** 6: "unità di milioni"}[v], num(r)))


DATI = [("Roma", 2750000), ("Milano", 1370000), ("Napoli", 910000), ("Torino", 850000), ("Palermo", 630000), ("Genova", 560000), ("Bologna", 390000), ("Firenze", 360000)]


def s5():
    k = R.choice(["citta", "citta", "distanza", "migliaia", "milioni", "visitatori"])
    if k == "citta":
        (a, x), (b, y) = R.sample(DATI, 2)
        if x < y:
            (a, x), (b, y) = (b, y), (a, x)
        return mcq("%s ha circa %s abitanti e %s circa %s. Quanti abitanti ha in più %s?" % (a, num(x), b, num(y), a), num(x - y),
                   [num(x + y), num(x - y + 100000), num(x - y - 10000)], "%s − %s = <b>%s</b>." % (num(x), num(y), num(x - y)))
    if k == "distanza":
        d = R.choice([149600000, 384400, 108200000, 227900000])
        name = {149600000: "il Sole", 384400: "la Luna", 108200000: "Venere dal Sole", 227900000: "Marte dal Sole"}[d]
        return mcq("La distanza media della Terra da %s è di circa %s km. Come si legge?" % (name, num(d)) if d in (149600000, 384400) else
                   "La distanza media di %s è di circa %s km. Come si legge?" % (name, num(d)), parole(d),
                   [parole(d * 10), parole(d // 10), parole(d + 1000000) if d > 10 ** 6 else parole(d + 1000)], "%s = <b>%s</b>." % (num(d), parole(d)))
    if k == "migliaia":
        n = R.randint(12, 950) * 1000
        return mcq("Un’azienda produce %s bottiglie. Le mette in casse da 1000. Quante casse riempie?" % num(n), num(n // 1000),
                   [num(n // 100), num(n // 10000) if n >= 10000 else num(n // 1000 + 1), num(n)], "%s : 1000 = <b>%s</b>." % (num(n), num(n // 1000)))
    if k == "milioni":
        a = R.randint(2, 9)
        b = R.choice([200000, 500000, 750000, 50000])
        return mcq("Un premio è di %s milioni e %s euro. Come si scrive in cifre?" % (a, num(b)), num(a * 10 ** 6 + b) + " €",
                   [num(a * 10 ** 5 + b) + " €", num(a * 10 ** 6 + b * 10) + " €", num(a * 10 ** 7 + b) + " €"],
                   "%d milioni = %s; più %s = <b>%s €</b>." % (a, num(a * 10 ** 6), num(b), num(a * 10 ** 6 + b)))
    a, b = R.randint(120000, 480000), R.randint(110000, 490000)
    return mcq("Un museo ha avuto %s visitatori nel 2024 e %s nel 2025. Quanti visitatori in tutto?" % (num(a), num(b)), num(a + b),
               [num(a + b + 100000), num(a + b - 10000), num(abs(a - b))], "%s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))


def main():
    seen = set()
    sets = [
        ("Classi e valore posizionale", mix(R, seen, [(s1_tabella, 10), (s1_valore, 10)])),
        ("Leggere, scrivere e scomporre", mix(R, seen, [(s2_lettere, 10), (s2_scomponi, 10)])),
        ("Confrontare e ordinare", mix(R, seen, [(s3_confronta, 12), (s3_ordina, 8)])),
        ("Arrotondare, + e − 1000, 1 000 000", mix(R, seen, [(s4_arrotonda, 12), (s4_piu, 8)])),
        ("Problemi con i grandi numeri", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Le cifre si raggruppano a tre a tre, da destra: <b>unità semplici</b>, <b>migliaia</b>, <b>milioni</b>, <b>miliardi</b>. Ogni classe ha h, da, u.",
         "Ogni posto vale 10 volte quello alla sua destra. 1 milione = 1000 migliaia = 1 000 000.",
         "Se una classe è vuota scrivi tre zeri: 3 milioni e 45 = 3 000 045.",
         "Per confrontare guarda prima quante cifre ha il numero; se sono uguali, confronta da sinistra."],
        [("Scrivi in cifre: 12 milioni 40 mila 7.", ["milioni: 012", "migliaia: 040", "unità: 007"], "12 040 007")],
        [["3 milioni e 45 scritto 345", "Ogni classe ha tre posti: 3 000 045."],
         ["Confondere cifra e valore", "La cifra 7 nelle centinaia di migliaia vale 700 000."],
         ["Leggere i gruppi da sinistra in modo sbagliato", "Separa le classi da destra, a tre a tre."]],
        table(["classe", "posti"], [["miliardi", "h da u"], ["milioni", "h da u"], ["migliaia", "h da u"], ["unità semplici", "h da u"]]))
    faq = [("Perché si lascia uno spazio tra i gruppi di cifre?", "Per leggere meglio i grandi numeri: 2 750 000 si legge subito «due milioni settecentocinquantamila»."),
           ("Quanti zeri ha un miliardo?", "Nove: 1 000 000 000. Un milione ne ha sei.")]
    make_unit(R, "grandi-numeri", "N",
              "Leggere, scrivere, confrontare numeri naturali oltre il milione, conoscendo il valore posizionale delle cifre; arrotondare",
              "I grandi numeri: milioni e miliardi", "Grandi numeri",
              "Schede di matematica per la classe quinta sui grandi numeri: classi, milioni e miliardi, valore posizionale, leggere e scrivere, scomporre, confrontare, arrotondare e problemi. 100 esercizi con soluzioni.",
              "Le cifre si leggono a gruppi di tre: milioni, migliaia, unità.", "Una classe vuota si scrive con tre zeri.",
              body, faq, sets, 1, grade=G)


if __name__ == "__main__":
    main()
