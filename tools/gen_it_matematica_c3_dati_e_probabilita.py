# -*- coding: utf-8 -*-
"""
Italia Matematica classe terza: Dati e probabilità (Relazioni, dati e previsioni)
  python3 tools/gen_it_matematica_c3_dati_e_probabilita.py
Indagini e tabelle di frequenza, tacche, istogrammi, ideogrammi (ogni simbolo vale 2 o 5), la moda,
classificare con il diagramma di Venn, eventi certi, possibili e impossibili, più e meno probabile.
Errori: contare i simboli dell’ideogramma senza guardare la legenda, leggere l’istogramma a occhio, confondere possibile e certo.
"""
import random
from it_common import pl, mcq, lesson, make_unit, mix, table, istogramma, wrap, text, line, INK, GREEN, FILL, RED, BLUE, FOIS

R = random.Random(70321)
TEMI = [("Frutta preferita della classe", "frutta", ["mela", "banana", "fragola", "arancia", "kiwi"], "bambini"),
        ("Animali dei bambini della classe", "animale", ["gatto", "cane", "coniglio", "pesce", "criceto"], "bambini"),
        ("Libri presi in prestito in biblioteca", "giorno", ["lunedì", "martedì", "giovedì", "venerdì"], "libri"),
        ("Sport preferiti", "sport", ["calcio", "nuoto", "danza", "basket", "tennis"], "bambini"),
        ("Colori preferiti", "colore", ["rosso", "blu", "verde", "giallo", "viola"], "bambini"),
        ("Gelati venduti in un giorno", "gusto", ["cioccolato", "fragola", "limone", "pistacchio"], "gelati")]


def dati(lo=2, hi=15, n=None):
    t, key, cats, u = R.choice(TEMI)
    cats = cats[: n or R.randint(3, len(cats))]
    vals = R.sample(range(lo, hi + 1), len(cats))
    return t, key, cats, vals, u


def chiedi(cats, vals, u, kind):
    i = R.randrange(len(cats))
    if kind == "val":
        return ("Quanti %s per «%s»?" % (u, cats[i]), str(vals[i]), [str(x) for x in (vals[(i + 1) % len(vals)], vals[i - 1], vals[i] + 1, vals[i] - 1)],
                "Leggi il valore di «%s»: <b>%d</b>." % (cats[i], vals[i]))
    if kind == "moda":
        m = vals.index(max(vals))
        return ("Qual è la moda, cioè la risposta più frequente?", cats[m], [cats[j] for j in range(len(cats)) if j != m],
                "Il valore più alto è %d: la moda è <b>%s</b>." % (vals[m], cats[m]))
    if kind == "min":
        m = vals.index(min(vals))
        return ("Quale risposta ha avuto meno %s?" % u, cats[m], [cats[j] for j in range(len(cats)) if j != m],
                "Il valore più basso è %d: <b>%s</b>." % (vals[m], cats[m]))
    if kind == "diff":
        a, b = R.sample(range(len(cats)), 2)
        if vals[a] < vals[b]:
            a, b = b, a
        d = vals[a] - vals[b]
        return ("Quanti %s in più per «%s» che per «%s»?" % (u, cats[a], cats[b]), str(d), [str(x) for x in (vals[a] + vals[b], vals[a], d + 1, d - 1 if d > 1 else d + 2)],
                "Calcola la differenza: %d − %d = <b>%d</b>." % (vals[a], vals[b], d))
    tot = sum(vals)
    return ("Quanti %s in tutto?" % u, str(tot), [str(x) for x in (tot - vals[-1], tot + 1, max(vals) * len(vals), tot - 1)],
            "Somma tutti i valori: %s = <b>%d</b>." % (" + ".join(map(str, vals)), tot))


def tab(key, u, cats, vals):
    return table([key.capitalize(), "Numero di %s" % u], [[c, str(v)] for c, v in zip(cats, vals)])


def tacche(n):
    g, r = divmod(n, 5)
    return " ".join(["<s>||||</s>"] * g + (["|" * r] if r else []))


def s1_tabella():
    t, key, cats, vals, u = dati()
    q, a, w, e = chiedi(cats, vals, u, R.choice(["val", "val", "moda", "min"]))
    return mcq("%s<br>%s<br>%s" % (t, tab(key, u, cats, vals), q), a, w, e)


def s1_tacche():
    n = R.randint(6, 23)
    return mcq("Durante una votazione si contano i voti con le tacche. Ogni gruppo barrato vale 5. Quanti voti ci sono?<br><span style='font-size:1.4em;letter-spacing:2px'>%s</span>" % tacche(n),
               str(n), [str(x) for x in (n + 5 if n % 5 else n - 1, n // 5 + n % 5, n - 1, n + 1)],
               ("%s da 5 e %s: %d %s 5 + %d = <b>%d</b>." % (pl(n // 5, "gruppo", "gruppi"), pl(n % 5, "tacca", "tacche"), n // 5, FOIS, n % 5, n)) if n % 5 else
               "%s da 5: %d %s 5 = <b>%d</b>." % (pl(n // 5, "gruppo", "gruppi"), n // 5, FOIS, n))


def s2_istogramma():
    t, key, cats, vals, u = dati(2, 18)
    q, a, w, e = chiedi(cats, vals, u, R.choice(["val", "val", "val", "moda", "min"]))
    return mcq(istogramma(list(zip(cats, vals)), "numero di %s" % u) + "%s. %s" % (t, q), a, w,
               e + " Leggi all’altezza della cima della colonna, sulla scala a sinistra.")


SIMB = "<circle cx='%.1f' cy='%.1f' r='9' fill='#f2c94c' stroke='%s' stroke-width='1.2'/>"


def ideogramma(cats, vals, k):
    rows = len(cats)
    W, H = 380, 30 + rows * 30
    s = []
    for i, (c, v) in enumerate(zip(cats, vals)):
        y = 26 + i * 30
        s.append(text(80, y + 5, c, 13, anchor="end", weight=600))
        full, half = divmod(v, k)
        for j in range(full):
            s.append(SIMB % (100 + j * 24, y, INK))
        if half:
            s.append("<path d='M%.1f %.1f a9 9 0 0 0 0 18 Z' fill='#f2c94c' stroke='%s' stroke-width='1.2'/>" % (100 + full * 24, y - 9, INK))
    return wrap(W, H, "".join(s), "ideogramma: ogni cerchio vale %d" % k, lg=True)


def s2_ideogramma():
    t, key, cats, vals, u = dati(1, 8, R.choice([3, 4]))
    k = R.choice([2, 2, 5, 10])
    vals = [v * k for v in vals]
    if k == 2 and R.random() < 0.4:
        i = R.randrange(len(vals))
        vals[i] += 1
    q, a, w, e = chiedi(cats, vals, u, R.choice(["val", "val", "tot", "diff"]))
    i = R.randrange(len(cats))
    if R.random() < 0.6:
        v = vals[i]
        n = v // k
        mezzo = v % k != 0
        return mcq(ideogramma(cats, vals, k) + "%s. Ogni cerchio vale %d %s%s. Quanti %s per «%s»?" % (t, k, u, ", mezzo cerchio vale %d" % (k // 2) if k == 2 else "", u, cats[i]), str(v),
                   [str(x) for x in (n + (1 if mezzo else 0), v + k, v - k if v > k else v + 2 * k, v + 1)],
                   "Ci sono %s%s: %d %s %d%s = <b>%d</b>. Guarda sempre la legenda!" % (pl(n, "cerchio", "cerchi"), " e mezzo" if mezzo else "", n, FOIS, k, " + %d" % (k // 2) if mezzo else "", v))
    return mcq(ideogramma(cats, vals, k) + "%s. Ogni cerchio vale %d %s%s. %s" % (t, k, u, ", mezzo cerchio vale %d" % (k // 2) if k == 2 else "", q), a, w, e)


GRID = [("Bambini della scuola che mangiano in mensa", ["classe prima", "classe seconda", "classe terza"], ["femmine", "maschi"]),
        ("Medaglie vinte dalla squadra", ["oro", "argento", "bronzo"], ["2024", "2025"]),
        ("Gelati venduti", ["vaniglia", "cioccolato", "fragola"], ["sabato", "domenica"]),
        ("Biglietti venduti per lo spettacolo", ["adulti", "bambini"], ["venerdì", "sabato", "domenica"])]


def s3_doppia():
    t, rows, cols = R.choice(GRID)
    vals = [[R.randint(4, 35) for _ in cols] for _ in rows]
    tb = table([""] + cols, [[r] + [str(v) for v in vs] for r, vs in zip(rows, vals)])
    i, j = R.randrange(len(rows)), R.randrange(len(cols))
    k = R.choice(["cella", "cella", "riga", "col"])
    if k == "cella":
        v = vals[i][j]
        return mcq("%s<br>%s<br>Quanti per «%s» e «%s»?" % (t, tb, rows[i], cols[j]), str(v),
                   [str(x) for x in (vals[(i + 1) % len(rows)][j], vals[i][(j + 1) % len(cols)], v + 1, sum(vals[i]))],
                   "Cerca la casella dove si incrociano la riga «%s» e la colonna «%s»: <b>%d</b>." % (rows[i], cols[j], v))
    if k == "riga":
        tot = sum(vals[i])
        return mcq("%s<br>%s<br>Quanti in tutto per «%s»?" % (t, tb, rows[i]), str(tot), [str(x) for x in (sum(vals[x][0] for x in range(len(rows))), tot + 1, vals[i][0], tot - 1)],
                   "Somma la riga «%s»: %s = <b>%d</b>." % (rows[i], " + ".join(map(str, vals[i])), tot))
    tot = sum(vals[x][j] for x in range(len(rows)))
    return mcq("%s<br>%s<br>Quanti in tutto per «%s»?" % (t, tb, cols[j]), str(tot), [str(x) for x in (sum(vals[0]), tot + 1, vals[0][j], tot - 2)],
               "Somma la colonna «%s»: %s = <b>%d</b>." % (cols[j], " + ".join(str(vals[x][j]) for x in range(len(rows))), tot))


def venn(a_only, both, b_only, fuori, la, lb):
    s = ["<rect x='4' y='4' width='352' height='172' rx='8' fill='none' stroke='%s' stroke-width='1.5'/>" % INK,
         "<circle cx='135' cy='92' r='70' fill='#cfe6d6' fill-opacity='0.6' stroke='%s' stroke-width='2'/>" % GREEN,
         "<circle cx='225' cy='92' r='70' fill='#c9dcf2' fill-opacity='0.6' stroke='%s' stroke-width='2'/>" % BLUE,
         text(110, 18, la, 13, weight=700), text(250, 18, lb, 13, weight=700)]
    for (cx, cy, items) in ((100, 92, a_only), (180, 92, both), (262, 92, b_only), (330, 160, fuori)):
        for k, it in enumerate(items):
            s.append(text(cx, cy - 10 * (len(items) - 1) + 20 * k, it, 13))
    return wrap(360, 180, "".join(s), "diagramma di Venn con due insiemi", lg=True)


def s3_venn():
    nums = R.sample(range(1, 31), 9)
    pa = lambda n: n % 2 == 0
    k = R.choice([3, 5, 10])
    pb = lambda n: n % k == 0
    if not any(pa(n) and pb(n) for n in nums):
        nums[0] = 2 * k
    a_only = [str(n) for n in nums if pa(n) and not pb(n)]
    both = [str(n) for n in nums if pa(n) and pb(n)]
    b_only = [str(n) for n in nums if pb(n) and not pa(n)]
    fuori = [str(n) for n in nums if not pa(n) and not pb(n)][:2]
    if len(a_only) > 4 or len(b_only) > 4 or len(both) > 3 or not a_only or not b_only:
        return None
    pic = venn(a_only, both, b_only, fuori, "pari", "multipli di %d" % k)
    q = R.choice(["entrambi", "solo_a", "fuori"])
    if q == "entrambi":
        ans = str(len(both))
        return mcq(pic + "Quanti numeri sono pari <b>e</b> multipli di %d?" % k, ans, [str(len(a_only) + len(both)), str(len(b_only) + len(both)), str(len(both) + 1)],
                   "Sono i numeri nella parte comune ai due cerchi: %s. Sono <b>%s</b>." % (", ".join(both), ans))
    if q == "solo_a":
        ans = str(len(a_only))
        return mcq(pic + "Quanti numeri sono pari ma <b>non</b> multipli di %d?" % k, ans, [str(len(a_only) + len(both)), str(len(b_only)), str(len(a_only) + 1)],
                   "Sono i numeri nel cerchio «pari» fuori dalla parte comune: %s. Sono <b>%s</b>." % (", ".join(a_only), ans))
    n = R.choice([x for x in range(1, 40) if x % 2 and x % k])
    return mcq(pic + "Dove va scritto il numero %d?" % n, "fuori dai due cerchi", ["nel cerchio «pari»", "nel cerchio «multipli di %d»" % k, "nella parte comune"],
               "%d non è pari e non è multiplo di %d: va <b>fuori dai due cerchi</b>." % (n, k))


def sacchetto(r, b, g):
    s = ["<path d='M30 40 Q20 150 60 170 L200 170 Q240 150 230 40 Z' fill='#f3ead7' stroke='%s' stroke-width='2'/>" % INK]
    pos = []
    for i in range(r + b + g):
        pos.append((60 + (i % 6) * 28, 70 + (i // 6) * 30))
    cols = ["#e05a5a"] * r + ["#4a7fd4"] * b + ["#57b36a"] * g
    order = list(range(len(cols)))
    R.shuffle(order)
    for (x, y), i in zip(pos, order):
        s.append("<circle cx='%d' cy='%d' r='11' fill='%s' stroke='%s' stroke-width='1.2'/>" % (x, y, cols[i], INK))
    return wrap(260, 180, "".join(s), "un sacchetto con %d palline rosse, %d blu e %d verdi" % (r, b, g))


def s4_sacchetto():
    r, b, g = R.randint(0, 6), R.randint(0, 6), R.randint(0, 5)
    if r + b + g < 4 or r + b + g > 15 or len({r, b, g}) < 3:
        return None
    pic = sacchetto(r, b, g)
    cnt = {"rosso": r, "blu": b, "verde": g}
    FEM = {"rosso": "rossa", "blu": "blu", "verde": "verde"}
    k = R.choice(["evento", "evento", "piu", "meno"])
    if k == "piu":
        c = max(cnt, key=cnt.get)
        return mcq(pic + "Peschi una pallina senza guardare. Quale colore è <b>più probabile</b>?", c, [x for x in cnt if x != c] + ["sono tutti ugualmente probabili"],
                   "Le palline %s sono le più numerose (%d): <b>%s</b> è il colore più probabile." % ({"rosso": "rosse", "blu": "blu", "verde": "verdi"}[c], cnt[c], c))
    if k == "meno":
        c = min((x for x in cnt if cnt[x] > 0), key=cnt.get)
        return mcq(pic + "Peschi una pallina senza guardare. Quale colore è <b>meno probabile</b> (ma possibile)?", c, [x for x in cnt if x != c] + ["nessuno"],
                   "Le palline %s sono le meno numerose (%d): <b>%s</b> è il colore meno probabile." % ({"rosso": "rosse", "blu": "blu", "verde": "verdi"}[c], cnt[c], c))
    c = R.choice(list(cnt))
    PL = {"rosso": "rosse", "blu": "blu", "verde": "verdi"}
    if cnt[c] == 0:
        ans, e = "impossibile", "Nel sacchetto non ci sono palline %s: è <b>impossibile</b>." % PL[c]
    elif cnt[c] == r + b + g:
        ans, e = "certo", "Tutte le palline sono %s: è <b>certo</b>." % PL[c]
    else:
        ans, e = "possibile", "Ci sono palline %s, ma anche di altri colori: è <b>possibile</b>." % PL[c]
    return mcq(pic + "Peschi una pallina senza guardare. Pescare una pallina %s è certo, possibile o impossibile?" % FEM[c], ans,
               [x for x in ("certo", "possibile", "impossibile") if x != ans] + ["non si può dire"], e)


EVENTI = [("Domani il sole sorgerà.", "certo"), ("Lanciando un dado esce il 7.", "impossibile"), ("Lanciando un dado esce un numero pari.", "possibile"),
          ("Lanciando una moneta esce testa.", "possibile"), ("Dopo il lunedì viene il martedì.", "certo"), ("Un gatto parlerà in italiano.", "impossibile"),
          ("Lanciando un dado esce un numero minore di 7.", "certo"), ("Domani pioverà.", "possibile"), ("Una settimana ha 8 giorni.", "impossibile"),
          ("Pescando una carta da un mazzo con solo carte rosse, esce una carta rossa.", "certo"), ("Oggi incontrerò un amico.", "possibile"),
          ("Un mese ha 40 giorni.", "impossibile"), ("Lanciando un dado esce il 6.", "possibile"), ("Un’ora dura 60 minuti.", "certo")]


def s4_eventi():
    ev, ans = R.choice(EVENTI)
    w = [x for x in ("certo", "possibile", "impossibile") if x != ans] + ["non si può dire"]
    why = {"certo": "succede sicuramente", "possibile": "può succedere oppure no", "impossibile": "non può succedere"}[ans]
    return mcq("«%s» È un evento certo, possibile o impossibile?" % ev, ans, w, "Questo evento %s: è <b>%s</b>." % (why, ans))


def s5():
    k = R.choice(["mancante", "mancante", "indagine", "moda_lista"])
    if k == "mancante":
        t, key, cats, vals, u = dati(3, 18, 4)
        i = R.randrange(len(cats))
        tot = sum(vals)
        rows = [[c, "?" if j == i else str(v)] for j, (c, v) in enumerate(zip(cats, vals))] + [["Totale", str(tot)]]
        known = tot - vals[i]
        return mcq("%s<br>%s<br>Quale numero manca nella tabella?" % (t, table([key.capitalize(), "Numero di %s" % u], rows)), str(vals[i]),
                   [str(x) for x in (tot + known, known, vals[i] + 1, vals[i] - 1)],
                   "Togli dal totale i valori che conosci: %d − %d = <b>%d</b>." % (tot, known, vals[i]))
    if k == "indagine":
        t, key, cats, vals, u = dati(3, 20)
        q, a, w, e = chiedi(cats, vals, u, R.choice(["diff", "tot"]))
        if R.random() < 0.5:
            return mcq(istogramma(list(zip(cats, vals)), "numero di %s" % u) + "%s. %s" % (t, q), a, w, e)
        return mcq("%s<br>%s<br>%s" % (t, tab(key, u, cats, vals), q), a, w, e)
    pool = ["mela", "pera", "banana", "uva"]
    m = R.choice(pool)
    lst = [m] * R.randint(4, 6) + [x for x in pool if x != m for _ in range(R.randint(1, 3))]
    R.shuffle(lst)
    if sorted(lst).count(m) <= max(lst.count(x) for x in pool if x != m):
        return None
    return mcq("Alla domanda «Qual è il tuo frutto preferito?» i bambini rispondono: %s. Qual è la moda?" % ", ".join(lst), m,
               [x for x in pool if x != m],
               "La moda è la risposta che compare più volte: <b>%s</b> (%d volte)." % (m, lst.count(m)))


def main():
    seen = set()
    sets = [
        ("Tabelle e tacche", mix(R, seen, [(s1_tabella, 14), (s1_tacche, 6)])),
        ("Istogrammi e ideogrammi", mix(R, seen, [(s2_istogramma, 10), (s2_ideogramma, 10)])),
        ("Tabelle a doppia entrata e Venn", mix(R, seen, [(s3_doppia, 12), (s3_venn, 8)])),
        ("Certo, possibile, impossibile", mix(R, seen, [(s4_sacchetto, 10), (s4_eventi, 10)])),
        ("Indagini e problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Con un’<b>indagine</b> si raccolgono dati: si fa una domanda e si contano le risposte con le tacche, poi si scrive una <b>tabella</b>.",
         "I dati si rappresentano con un <b>istogramma</b> (colonne) o con un <b>ideogramma</b> (simboli). Nell’ideogramma guarda sempre la legenda: quanto vale un simbolo?",
         "La <b>moda</b> è la risposta che compare più volte.",
         "Un evento è <b>certo</b> se succede sicuramente, <b>possibile</b> se può succedere oppure no, <b>impossibile</b> se non può succedere."],
        [("In un ideogramma ogni cerchio vale 2. Ci sono 4 cerchi e mezzo.", ["4 %s 2 = 8" % FOIS, "mezzo cerchio = 1", "8 + 1 = 9"], "9")],
        [["Contare i simboli senza guardare la legenda", "Moltiplica il numero di simboli per il valore di un simbolo."],
         ["Leggere l’istogramma a occhio", "Segui con il righello la cima della colonna fino alla scala."],
         ["Dire «certo» quando è solo possibile", "È certo solo se non può succedere nient’altro."]])
    faq = [("Che cos’è la moda?", "È il dato più frequente: in un’indagine sul frutto preferito è il frutto scelto da più bambini."),
           ("Che differenza c’è tra istogramma e ideogramma?", "Nell’istogramma l’altezza delle colonne dice il numero; nell’ideogramma lo dice il numero di simboli, ognuno con il suo valore.")]
    make_unit(R, "dati-e-probabilita", "D",
              "Raccogliere dati e rappresentarli con tabelle e grafici (istogrammi, ideogrammi); leggere e interpretare rappresentazioni; classificare in base a una o più proprietà; riconoscere eventi certi, possibili e impossibili",
              "Dati e probabilità: tabelle, grafici e previsioni", "Dati e probabilità",
              "Schede di matematica per la classe terza su dati e probabilità: indagini, tabelle e tacche, istogrammi, ideogrammi, moda, diagramma di Venn, eventi certi, possibili e impossibili. 100 esercizi con soluzioni.",
              "Nell’ideogramma guarda sempre quanto vale un simbolo.", "Certo, possibile o impossibile?",
              body, faq, sets, 21)


if __name__ == "__main__":
    main()
