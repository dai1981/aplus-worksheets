# -*- coding: utf-8 -*-
"""
Italia Matematica classe quarta: I numeri entro il milione (Numeri)
  python3 tools/gen_it_matematica_c4_numeri_entro_il_milione.py
Classe delle migliaia e classe delle unità semplici (uk, dak, hk, u, da, h), valore posizionale, leggere e
scrivere in cifre e in lettere, scomporre, confrontare e ordinare, arrotondare, + e − 1000, 10 000, 100 000.
Errori: dimenticare gli zeri, confondere cifra e valore, ordinare guardando solo la prima cifra.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, table, lettere

R = random.Random(70401)
G = "classe-quarta"
POS = [("unità", 1), ("decine", 10), ("centinaia", 100), ("unità di migliaia", 1000), ("decine di migliaia", 10 ** 4), ("centinaia di migliaia", 10 ** 5)]


def big(lo=5, hi=6, zeros=0.3):
    k = R.randint(lo, hi)
    ds = [R.randint(1, 9)] + [0 if R.random() < zeros else R.randint(0, 9) for _ in range(k - 1)]
    return int("".join(map(str, ds)))


def tab(n):
    s = str(n).rjust(6, " ")
    top = "<tr><th colspan='3'>migliaia</th><th colspan='3'>unità semplici</th></tr>"
    head = ["hk", "dak", "uk", "h", "da", "u"]
    return ("<table class='sn-table' style='width:auto;margin:6px 0'><thead>%s<tr>%s</tr></thead><tbody><tr>%s</tr></tbody></table>"
            % (top, "".join("<th>%s</th>" % h for h in head), "".join("<td style='text-align:center;min-width:28px'>%s</td>" % c.strip() for c in s)))


def near(n):
    s = str(n)
    out = []
    if "0" in s:
        out.append(int(s.replace("0", "", 1)))
    out.append(n * 10 if n < 100000 else n // 10)
    if len(s) >= 4:
        out.append(int(s[:2] + s[3:]))
    out += [n + 10 ** (len(s) - 2), n // 10, int(s[::-1]) if s[-1] != "0" else None]
    return [num(x) for x in out if x and x != n and x < 10 ** 6]


def s1_tabella():
    n = big()
    return mcq(tab(n) + "Quale numero è scritto nella tabella?", num(n), near(n),
               "Prima la classe delle migliaia, poi quella delle unità semplici: <b>%s</b>." % num(n))


def s1_valore():
    n = big(5, 6, 0.1)
    s = str(n)
    i = R.randrange(len(s) - 1)
    d = int(s[i])
    if d == 0:
        return None
    name, v = POS[len(s) - 1 - i]
    return mcq("Nel numero %s quanto vale la cifra <b>%d</b> che sta nelle %s?" % (num(n), d, name),
               num(d * v), [num(d * v * 10), num(d * v // 10), str(d), num(d * v * 100) if d * v * 100 < 10 ** 7 else None],
               "%d %s valgono <b>%s</b>." % (d, name, num(d * v)))


def s1_cifra():
    n = big(5, 6, 0.15)
    s = str(n)
    p = R.randrange(1, min(len(s), 6))
    name, _ = POS[p]
    d = s[len(s) - 1 - p]
    others = sorted({c for c in s if c != d})
    return mcq("Nel numero %s qual è la cifra delle <b>%s</b>?" % (num(n), name), d, others + [str((int(d) + 1) % 10)],
               "Conta i posti da destra: u, da, h, uk, dak, hk. La cifra è <b>%s</b>." % d)


def parola(n):
    return lettere(n)


def s2_lettere():
    n = big(4, 6, 0.4)
    w = parola(n)
    return mcq("Scrivi in cifre: <b>%s</b>" % w, num(n), near(n), "«%s» si scrive <b>%s</b>." % (w, num(n)))


def s2_in_lettere():
    n = big(4, 6, 0.4)
    ws = []
    for m in near(n)[:4]:
        v = int(m.replace(" ", ""))
        ws.append(parola(v))
    return mcq("Come si scrive in lettere %s?" % num(n), parola(n), ws,
               "Leggi prima le migliaia (%s mila), poi il resto: <b>%s</b>." % (num(n // 1000), parola(n)))


def s2_scomponi():
    n = big(5, 6, 0.4)
    s = str(n)
    parts = [int(c) * 10 ** (len(s) - 1 - i) for i, c in enumerate(s) if c != "0"]
    if len(parts) < 3:
        return None
    sh = " + ".join(num(x) for x in parts)
    if R.random() < 0.5:
        return mcq("Quale numero è uguale a %s?" % sh, num(n), near(n), "%s = <b>%s</b>." % (sh, num(n)))
    w1 = " + ".join(num(x // 10) if j == 0 else num(x) for j, x in enumerate(parts))
    w2 = " + ".join(num(x * 10) if j == len(parts) - 1 else num(x) for j, x in enumerate(parts))
    w3 = " + ".join(str(int(c)) for c in s if c != "0")
    return mcq("Qual è la scomposizione di %s?" % num(n), sh, [w1, w2, w3], "Ogni cifra vale secondo il suo posto: <b>%s</b>." % sh)


def s3_confronta():
    a = big(5, 6, 0.2)
    if R.random() < 0.5 and a >= 100000:
        b = int(str(a)[:-1])
    else:
        s = list(str(a))
        i = R.randrange(1, len(s))
        s[i] = str((int(s[i]) + R.randint(1, 9)) % 10)
        b = int("".join(s))
    if a == b:
        return None
    big_ = max(a, b)
    return mcq("Qual è il numero maggiore: %s o %s?" % (num(a), num(b)), num(big_), [num(min(a, b)), "sono uguali", "non si può sapere"],
               "%s. Il maggiore è <b>%s</b>." % ("Ha più cifre" if len(str(a)) != len(str(b)) else "Hanno lo stesso numero di cifre: confronta da sinistra la prima cifra diversa", num(big_)))


def s3_simbolo():
    a = big(5, 6, 0.2)
    k = R.choice([1, 10, 100, 1000, 10000])
    b = a + R.choice([-1, 1]) * k * R.randint(1, 3)
    if R.random() < 0.15:
        b = a
    if b <= 0:
        return None
    s = "&lt;" if a < b else "&gt;" if a > b else "="
    return mcq("Quale segno va tra %s e %s?" % (num(a), num(b)), s, ["&lt;", "&gt;", "=", "non si può sapere"],
               "%s %s %s." % (num(a), "<b>&lt;</b>" if s == "&lt;" else "<b>&gt;</b>" if s == "&gt;" else "<b>=</b>", num(b)))


def s3_ordina():
    base = big(6, 6, 0.1)
    if base > 900000:
        return None
    ns = sorted({base + R.choice([-1, 1]) * R.randint(1, 9) * 10 ** R.randint(1, 4) for _ in range(6)})[:4]
    if len(ns) < 4:
        return None
    f = lambda L: "; ".join(num(x) for x in L)
    sh = ns[:]
    R.shuffle(sh)
    w = ns[:]
    w[1], w[2] = w[2], w[1]
    return mcq("Metti in ordine crescente: %s" % f(sh), f(ns), [f(ns[::-1]), f(w), f(ns[1:] + ns[:1])],
               "Dal più piccolo al più grande: <b>%s</b>." % f(ns))


def s4_arrotonda():
    n = big(5, 6, 0.1)
    v, t = R.choice([(10, "alle decine"), (100, "alle centinaia"), (1000, "alle migliaia"), (10 ** 4, "alle decine di migliaia")])
    r = (n + v // 2) // v * v
    other = n // v * v if r != n // v * v else r + v
    return mcq("Arrotonda %s %s." % (num(n), t), num(r), [num(other), num((n + v * 5) // (v * 10) * v * 10), num(r + v) if r + v < 10 ** 6 else None, num(n // v * v + v * 10) if n // v * v + v * 10 < 10 ** 6 else None, num(n)],
               "Guarda la cifra subito a destra: %s. <b>%s</b>." % ("5 o più, arrotondi per eccesso" if r > n else "meno di 5, arrotondi per difetto", num(r)))


def s4_piu():
    n = big(5, 6, 0.4)
    v = R.choice([1000, 10 ** 4, 10 ** 5])
    name = {1000: "unità di migliaia", 10 ** 4: "decine di migliaia", 10 ** 5: "centinaia di migliaia"}[v]
    if R.random() < 0.5:
        if n + v >= 10 ** 6:
            return None
        return mcq("Quanto fa %s + %s?" % (num(n), num(v)), num(n + v), [num(n + v // 10), num(n + v * 10) if n + v * 10 < 10 ** 6 else None, num(n + 1), num(n + v // 100)],
                   "Aggiungi 1 alle %s: <b>%s</b>." % (name, num(n + v)))
    if n < v * 2:
        return None
    return mcq("Quanto fa %s − %s?" % (num(n), num(v)), num(n - v), [num(n - v // 10), num(n + v), num(n - 1), num(n - v // 100)],
               "Togli 1 alle %s: <b>%s</b>." % (name, num(n - v)))


def s4_vicini():
    n = big(5, 6, 0.5)
    n = n // 10 * 10
    if R.random() < 0.5:
        return mcq("Qual è il numero che viene subito prima di %s?" % num(n), num(n - 1), [num(n + 1), num(n - 10), num(n - 11), num(n // 10 * 10 - 1 + 10)],
                   "Il precedente si trova togliendo 1: <b>%s</b>." % num(n - 1))
    m = (n // 1000) * 1000 + 999
    return mcq("Qual è il numero che viene subito dopo %s?" % num(m), num(m + 1), [num(m + 10), num(m - 1), num(m + 1 + 1000), num(m + 1 - 1000 + 100)],
               "Il successivo si trova aggiungendo 1: <b>%s</b>." % num(m + 1))


CITTA = [("Bologna", 390000), ("Firenze", 360000), ("Bari", 316000), ("Catania", 300000), ("Verona", 255000), ("Venezia", 250000),
         ("Messina", 220000), ("Padova", 207000), ("Trieste", 199000), ("Parma", 196000), ("Brescia", 196000), ("Prato", 195000)]


def s5():
    k = R.choice(["citta", "citta", "stadio", "km", "libri", "auto", "cifre"])
    if k == "citta":
        (a, x), (b, y) = R.sample(CITTA, 2)
        if x == y:
            return None
        if x < y:
            (a, x), (b, y) = (b, y), (a, x)
        if R.random() < 0.5:
            return mcq("%s ha circa %s abitanti e %s circa %s. Quale città ha più abitanti?" % (b, num(y), a, num(x)), a, [b, "hanno gli stessi abitanti", "non si può sapere"],
                       "%s &gt; %s: <b>%s</b>." % (num(x), num(y), a))
        return mcq("%s ha circa %s abitanti e %s circa %s. Quanti abitanti ha in più %s?" % (a, num(x), b, num(y), a), num(x - y),
                   [num(x + y), num(x - y + 10000), num(x - y - 1000)], "%s − %s = <b>%s</b>." % (num(x), num(y), num(x - y)))
    if k == "stadio":
        a = R.randint(30, 70) * 1000 + R.randint(1, 999)
        return mcq("Allo stadio ci sono %s spettatori. Arrotonda alle migliaia: circa quanti sono?" % num(a), num((a + 500) // 1000 * 1000),
                   [num(a // 1000 * 1000 + (1000 if (a + 500) // 1000 * 1000 == a // 1000 * 1000 else 0)), num((a + 5000) // 10000 * 10000), num(a // 100 * 100)],
                   "Guarda le centinaia: %d. <b>%s</b>." % (a // 100 % 10, num((a + 500) // 1000 * 1000)))
    if k == "km":
        a = R.randint(12, 98) * 1000 + R.randint(100, 999)
        return mcq("Il contachilometri di un’auto segna %s km. Dopo un viaggio di 1000 km, che cosa segna?" % num(a), num(a + 1000) + " km",
                   [num(a + 100) + " km", num(a + 10000) + " km", num(a + 1) + " km"], "%s + 1000 = <b>%s km</b>." % (num(a), num(a + 1000)))
    if k == "libri":
        h, d = R.randint(1, 9), R.randint(1, 9)
        n = h * 100000 + d * 1000
        return mcq("Una biblioteca ha %d centinaia di migliaia e %d migliaia di libri. Quanti libri ha?" % (h, d), num(n),
                   [num(h * 10000 + d * 1000), num(h * 100000 + d * 100), num(h * 1000 + d)], "%s + %s = <b>%s</b>." % (num(h * 100000), num(d * 1000), num(n)))
    if k == "auto":
        a = R.randint(120, 480) * 1000
        return mcq("Una fabbrica produce %s auto all’anno. Quante migliaia di auto sono?" % num(a), num(a // 1000),
                   [num(a // 100), num(a // 10000), num(a)], "%s = <b>%s</b> migliaia." % (num(a), num(a // 1000)))
    ds = R.sample(range(1, 10), 3) + [0]
    hi = int("".join(map(str, sorted(ds, reverse=True))))
    lo_ds = sorted(ds)
    lo_ds[0], lo_ds[1] = lo_ds[1], lo_ds[0]
    lo = int("".join(map(str, lo_ds)))
    if R.random() < 0.5:
        return mcq("Con le cifre %s (usate una volta sola) qual è il numero più grande di quattro cifre?" % ", ".join(map(str, sorted(ds))), num(hi),
                   [num(lo), num(int(str(hi)[::-1].lstrip("0") or 0)), num(int(str(hi)[:2] + str(hi)[3] + str(hi)[2]))],
                   "Metti le cifre dalla più grande alla più piccola: <b>%s</b>." % num(hi))
    return mcq("Con le cifre %s (usate una volta sola) qual è il numero più piccolo di quattro cifre?" % ", ".join(map(str, sorted(ds))), num(lo),
               [num(int("".join(map(str, sorted(ds)[1:])))), num(hi), num(lo + 9) if lo % 10 == 0 else num(lo + 1)],
               "Lo 0 non può stare all’inizio: metti la cifra più piccola diversa da 0, poi lo 0, poi le altre: <b>%s</b>." % num(lo))


def main():
    seen = set()
    sets = [
        ("Migliaia e unità semplici", mix(R, seen, [(s1_tabella, 8), (s1_valore, 6), (s1_cifra, 6)])),
        ("Leggere, scrivere e scomporre", mix(R, seen, [(s2_lettere, 7), (s2_in_lettere, 6), (s2_scomponi, 7)])),
        ("Confrontare e ordinare", mix(R, seen, [(s3_confronta, 7), (s3_simbolo, 7), (s3_ordina, 6)])),
        ("Arrotondare, precedente e successivo", mix(R, seen, [(s4_arrotonda, 10), (s4_piu, 6), (s4_vicini, 4)])),
        ("Problemi con i grandi numeri", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Le cifre si raggruppano a tre a tre, da destra: la classe delle <b>unità semplici</b> (h, da, u) e la classe delle <b>migliaia</b> (hk, dak, uk).",
         "Ogni posto vale 10 volte quello alla sua destra: 10 unità di migliaia = 1 decina di migliaia.",
         "Il numero più grande con sei cifre è 999 999. Aggiungendo 1 si arriva a <b>1 000 000</b>, un milione.",
         "Per confrontare guarda prima quante cifre ha il numero; se sono uguali, confronta le cifre da sinistra."],
        [("Scrivi in cifre: trecentoquattromilaventi.", ["migliaia: trecentoquattro → 304", "unità semplici: venti → 020"], "304 020")],
        [["Scrivere 34 020 come 3420", "Ogni classe ha tre posti: metti gli zeri."],
         ["Confondere cifra e valore", "In 708 000 la cifra 7 vale 700 000."],
         ["Ordinare guardando solo la prima cifra", "Prima conta le cifre: 98 000 &lt; 120 000."]],
        table(["migliaia", "", "", "unità semplici", "", ""], [["hk", "dak", "uk", "h", "da", "u"], ["3", "0", "4", "0", "2", "0"]]))
    faq = [("Che cosa vuol dire hk, dak, uk?", "Sono le centinaia di migliaia (hk), le decine di migliaia (dak) e le unità di migliaia (uk): i tre posti della classe delle migliaia."),
           ("Perché si lascia uno spazio nei numeri grandi?", "Per leggerli meglio: 304 020 si legge subito «trecentoquattromilaventi». Nei numeri di quattro cifre lo spazio di solito non si mette.")]
    make_unit(R, "numeri-entro-il-milione", "N",
              "Leggere, scrivere, confrontare numeri naturali entro il milione, conoscendo il valore posizionale delle cifre; arrotondare",
              "I numeri entro il milione: migliaia e unità semplici", "Numeri entro il milione",
              "Schede di matematica per la classe quarta sui numeri entro il milione: classe delle migliaia, valore posizionale, leggere e scrivere in lettere, scomporre, confrontare, ordinare, arrotondare e problemi. 100 esercizi con soluzioni.",
              "Le cifre si leggono a gruppi di tre: migliaia e unità semplici.", "Ogni posto vale 10 volte quello alla sua destra.",
              body, faq, sets, 1, grade=G)


if __name__ == "__main__":
    main()
