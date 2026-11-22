# -*- coding: utf-8 -*-
"""
Italia Matematica classe quinta: Statistica e probabilità (Relazioni, dati e previsioni)
  python3 tools/gen_it_matematica_c5_statistica_e_probabilita.py
Frequenza, moda, media aritmetica, mediana, campo di variazione; leggere istogrammi e aerogrammi (percentuali),
probabilità come frazione (dado, sacchetto, ruota), eventi certi, impossibili, più probabili.
Errori: mediana senza ordinare i dati, media = somma senza dividere, probabilità con il denominatore sbagliato.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, Kids, fr, istogramma, wrap, text, INK, DIV, table
import math

R = random.Random(70521)
G = "classe-quinta"
K = Kids(R)
SPORT = ["calcio", "nuoto", "pallavolo", "basket", "danza", "tennis", "judo"]


def s1_moda_media():
    k = R.choice(["moda", "media", "mediana", "campo"])
    n = R.choice([5, 7]) if k == "mediana" else R.randint(5, 7)
    vals = [R.randint(2, 30) for _ in range(n)]
    if k == "moda":
        m = R.choice(vals)
        vals += [m, m]
        R.shuffle(vals)
        from collections import Counter
        c = Counter(vals).most_common()
        if len(c) > 1 and c[0][1] == c[1][1]:
            return None
        mo = c[0][0]
        return mcq("Dati: %s. Qual è la moda?" % ", ".join(map(str, vals)), str(mo), [str(max(vals)) if max(vals) != mo else str(min(vals)), str(sorted(vals)[len(vals) // 2]) if sorted(vals)[len(vals) // 2] != mo else str(mo + 1), str(c[0][1])],
                   "La moda è il dato che compare più volte: %d compare %d volte. <b>%d</b>." % (mo, c[0][1], mo))
    if k == "media":
        m = R.randint(5, 25)
        vals = [m + d for d in R.sample(range(-5, 6), n - 1)]
        vals.append(m * n - sum(vals))
        if vals[-1] <= 0 or vals[-1] in vals[:-1]:
            return None
        R.shuffle(vals)
        return mcq("Dati: %s. Qual è la media aritmetica?" % ", ".join(map(str, vals)), str(m), [str(sum(vals)), str(sorted(vals)[n // 2]) if sorted(vals)[n // 2] != m else str(m + 1), str(m - 1), str(sum(vals) // (n + 1))],
                   "Somma: %d; numero dei dati: %d. Media = %d %s %d = <b>%d</b>." % (sum(vals), n, sum(vals), DIV, n, m))
    if k == "mediana":
        if len(set(vals)) < n:
            return None
        o = sorted(vals)
        me = o[n // 2]
        return mcq("Dati: %s. Qual è la mediana?" % ", ".join(map(str, vals)), str(me), [str(vals[n // 2]) if vals[n // 2] != me else str(o[n // 2 + 1]), str(o[n // 2 - 1]), str(sum(vals) // n) if sum(vals) // n != me else str(me + 1)],
                   "Ordina i dati: %s. Il dato centrale è <b>%d</b>." % (", ".join(map(str, o)), me))
    return mcq("Dati: %s. Qual è il campo di variazione (differenza tra il dato più grande e il più piccolo)?" % ", ".join(map(str, vals)), str(max(vals) - min(vals)),
               [str(max(vals)), str(max(vals) + min(vals)), str(vals[-1] - vals[0]) if vals[-1] - vals[0] > 0 and vals[-1] - vals[0] != max(vals) - min(vals) else str(max(vals) - min(vals) + 1)],
               "%d − %d = <b>%d</b>." % (max(vals), min(vals), max(vals) - min(vals)))


def s2_grafico():
    cats = R.sample(SPORT, 4)
    vals = R.sample(range(3, 16), 4)
    data = list(zip(cats, vals))
    k = R.choice(["moda", "tot", "media", "diff"])
    pic = istogramma(data, "numero di bambini")
    if k == "moda":
        i = vals.index(max(vals))
        return mcq(pic + "Sport preferito dei bambini di una classe. Qual è la moda?", cats[i], [c for c in cats if c != cats[i]], "La colonna più alta è %s (%d): la moda è <b>%s</b>." % (cats[i], vals[i], cats[i]))
    if k == "tot":
        return mcq(pic + "Sport preferito dei bambini. Quanti bambini hanno risposto?", str(sum(vals)), [str(sum(vals) - vals[0]), str(max(vals) * 4), str(sum(vals) + 1)],
                   "%s = <b>%d</b>." % (" + ".join(map(str, vals)), sum(vals)))
    if k == "media":
        if sum(vals) % 4:
            return None
        return mcq(pic + "In media, quanti bambini per ogni sport?", str(sum(vals) // 4), [str(sum(vals)), str(sorted(vals)[2]), str(sum(vals) // 4 + 1)],
                   "%d %s 4 = <b>%d</b>." % (sum(vals), DIV, sum(vals) // 4))
    a, b = R.sample(range(4), 2)
    if vals[a] < vals[b]:
        a, b = b, a
    return mcq(pic + "Quanti bambini preferiscono %s più di %s?" % (cats[a], cats[b]), str(vals[a] - vals[b]), [str(vals[a] + vals[b]), str(vals[a]), str(vals[a] - vals[b] + 1)],
               "%d − %d = <b>%d</b>." % (vals[a], vals[b], vals[a] - vals[b]))


def torta(parts):
    """aerogramma: parts = [(nome, percentuale)]"""
    cols = ["#9fd3b0", "#f2c94c", "#8fb8e8", "#f0a6a6", "#c7b4e8"]
    s, a0 = [], -math.pi / 2
    cx, cy, r = 110, 110, 90
    for i, (n, p) in enumerate(parts):
        a1 = a0 + 2 * math.pi * p / 100
        large = 1 if p > 50 else 0
        x0, y0, x1, y1 = cx + r * math.cos(a0), cy + r * math.sin(a0), cx + r * math.cos(a1), cy + r * math.sin(a1)
        s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='1.5'/>" % (cx, cy, x0, y0, r, r, large, x1, y1, cols[i], INK))
        am = (a0 + a1) / 2
        s.append(text(cx + 58 * math.cos(am), cy + 58 * math.sin(am) + 4, "%d%%" % p, 12))
        s.append("<rect x='230' y='%d' width='14' height='14' fill='%s' stroke='%s'/>" % (30 + i * 24, cols[i], INK))
        s.append(text(250, 42 + i * 24, n, 13, anchor="start", weight=500))
        a0 = a1
    return wrap(360, 220, "".join(s), "aerogramma", lg=True)


def s3_torta():
    ps = R.choice([[50, 25, 15, 10], [40, 30, 20, 10], [45, 25, 20, 10], [35, 30, 25, 10], [50, 20, 20, 10], [60, 20, 15, 5]])
    cats = R.sample(["bici", "auto", "a piedi", "scuolabus", "monopattino"], 4)
    n = R.choice([20, 40, 60, 100, 200])
    pic = torta(list(zip(cats, ps)))
    i = R.randrange(4)
    if R.random() < 0.6:
        v = n * ps[i] // 100
        if n * ps[i] % 100:
            return None
        return mcq(pic + "Come vanno a scuola %d alunni. Quanti alunni vanno %s?" % (n, cats[i] if cats[i] == "a piedi" else "in " + cats[i]), str(v), [str(ps[i]), str(n - v), str(v * 2)],
                   "%d%% di %d = %d %s 100 × %d = <b>%d</b>." % (ps[i], n, n, DIV, ps[i], v))
    j = ps.index(max(ps))
    return mcq(pic + "Quale mezzo usa la metà o la parte più grande degli alunni?", cats[j], [c for c in cats if c != cats[j]], "Il settore più grande è %s (%d%%): <b>%s</b>." % (cats[j], ps[j], cats[j]))


def s4_prob():
    k = R.choice(["dado", "dado", "sacchetto", "sacchetto", "ruota", "carte"])
    if k == "dado":
        ev, fav = R.choice([("un numero pari", 3), ("il 6", 1), ("un numero maggiore di 4", 2), ("un numero minore di 3", 2), ("un multiplo di 3", 2), ("un numero dispari", 3), ("un numero minore di 7", 6), ("il 7", 0)])
        a = fr(fav, 6) if 0 < fav < 6 else ("1 (evento certo)" if fav == 6 else "0 (evento impossibile)")
        return mcq("Lanci un dado a 6 facce. Qual è la probabilità che esca %s?" % ev, a, [fr(6, fav) if 0 < fav < 6 else fr(1, 6), fr(fav, 12) if 0 < fav < 6 else fr(5, 6), fr(fav + 1, 6) if fav < 5 else "1", fr(1, fav) if 1 < fav < 6 else fr(1, 2)],
                   "Casi favorevoli: %d; casi possibili: 6. Probabilità = <b>%s</b>." % (fav, a))
    if k == "sacchetto":
        r, b, g = R.randint(1, 7), R.randint(1, 7), R.randint(1, 6)
        t = r + b + g
        c, f = R.choice([("rossa", r), ("blu", b), ("verde", g)])
        return mcq("In un sacchetto ci sono %d palline rosse, %d blu e %d verdi. Peschi senza guardare: qual è la probabilità di una pallina %s?" % (r, b, g, c), fr(f, t),
                   [fr(f, t - f) if t - f != t else fr(f, t + 1), fr(1, 3), fr(f, 10) if t != 10 else fr(f, 12), fr(t - f, t)], "Favorevoli: %d; possibili: %d. <b>%s</b>." % (f, t, fr(f, t)))
    if k == "ruota":
        n = R.choice([4, 5, 8, 10])
        f = R.randint(1, n - 1)
        return mcq("Una ruota è divisa in %d spicchi uguali; %d sono gialli. Qual è la probabilità che si fermi su uno spicchio giallo?" % (n, f), fr(f, n), [fr(n - f, n), fr(f, n - f), fr(1, n) if f != 1 else fr(2, n)],
                   "%d spicchi gialli su %d: <b>%s</b>." % (f, n, fr(f, n)))
    q, a, w = R.choice([("Da un mazzo di 40 carte napoletane (4 semi da 10) peschi una carta. Qual è la probabilità di una carta di coppe?", fr(10, 40), [fr(1, 40), fr(4, 40), fr(10, 30)]),
                        ("Da un mazzo di 40 carte napoletane peschi una carta. Qual è la probabilità di un asso (ce ne sono 4)?", fr(4, 40), [fr(1, 40), fr(4, 10), fr(1, 4)]),
                        ("Lanci una moneta. Qual è la probabilità che esca testa?", fr(1, 2), [fr(1, 4), fr(2, 2), fr(1, 3)])])
    return mcq(q, a, w, "Casi favorevoli su casi possibili: <b>%s</b>." % a)


def s5_confronto():
    p = K.next()
    k = R.choice(["piu", "certo", "equo"])
    if k == "piu":
        a, b = R.sample(range(1, 9), 2)
        ta, tb = a + R.randint(2, 6), b + R.randint(2, 6)
        if abs(a / ta - b / tb) < 0.01:
            return None
        g = "il sacchetto A" if a / ta > b / tb else "il sacchetto B"
        return mcq("Sacchetto A: %d palline vincenti su %d. Sacchetto B: %d vincenti su %d. Da quale conviene pescare?" % (a, ta, b, tb), g,
                   ["il sacchetto B" if g == "il sacchetto A" else "il sacchetto A", "è uguale", "quello con più palline vincenti" if (a > b) != (a / ta > b / tb) else "non si può sapere"],
                   "A: %s; B: %s. Conviene <b>%s</b>, che ha la probabilità più grande." % (fr(a, ta), fr(b, tb), g))
    if k == "certo":
        ev, ans = R.choice([("pescare una pallina rossa da un sacchetto con solo palline rosse", "certo"), ("ottenere 13 lanciando due dadi", "impossibile"),
                            ("ottenere 7 lanciando due dadi", "possibile"), ("pescare una carta di spade da un mazzo con solo carte di coppe", "impossibile"),
                            ("ottenere un numero minore di 13 lanciando due dadi", "certo"), ("che domani piova", "possibile")])
        return mcq("Questo evento è certo, possibile o impossibile: %s?" % ev, ans,
                   [x for x in ("certo", "possibile", "impossibile") if x != ans] + ["non si può dire"], "L’evento è <b>%s</b>." % ans)
    return mcq("%s e un amico giocano: se il dado dà un numero pari vince %s, se dispari vince l’amico. Il gioco è equo?" % (p[0], p[0]), "sì, tutti e due hanno probabilità " + fr(1, 2),
               ["no, vince più spesso %s" % p[0], "no, vince più spesso l’amico", "sì, tutti e due hanno probabilità " + fr(1, 6)], "3 numeri pari e 3 dispari: probabilità %s per tutti e due. <b>Sì, è equo</b>." % fr(3, 6))


def main():
    seen = set()
    sets = [
        ("Moda, media, mediana", mix(R, seen, [(s1_moda_media, 20)])),
        ("Leggere un istogramma", mix(R, seen, [(s2_grafico, 20)])),
        ("Aerogrammi e percentuali", mix(R, seen, [(s3_torta, 20)])),
        ("Calcolare la probabilità", mix(R, seen, [(s4_prob, 20)])),
        ("Confrontare probabilità", mix(R, seen, [(s5_confronto, 8), (s4_prob, 6), (s1_moda_media, 6)])),
    ]
    body = lesson(
        ["La <b>moda</b> è il dato più frequente. La <b>media</b> è la somma dei dati divisa per il numero dei dati. La <b>mediana</b> è il dato centrale dopo averli ordinati.",
         "Il <b>campo di variazione</b> è la differenza tra il dato più grande e il più piccolo.",
         "Nell’<b>aerogramma</b> (grafico a torta) ogni settore è una percentuale del totale.",
         "<b>Probabilità</b> = casi favorevoli / casi possibili. Va da 0 (impossibile) a 1 (certo)."],
        [("Dati: 4, 9, 6, 9, 7", ["moda: 9", "media: 35 %s 5 = 7" % DIV, "ordinati: 4, 6, 7, 9, 9 → mediana 7"], "moda 9, media 7, mediana 7"),
         ("Dado: probabilità di un numero maggiore di 4", ["favorevoli: 5, 6", "possibili: 6"], fr(2, 6) + " = " + fr(1, 3))],
        [["Mediana senza ordinare i dati", "Prima metti i dati in ordine crescente."],
         ["Media = somma dei dati", "Dopo la somma, dividi per quanti sono i dati."],
         ["Probabilità con il denominatore sbagliato", "Sotto vanno tutti i casi possibili, sopra quelli favorevoli."]],
        table(["Indice", "Come si trova"], [["moda", "dato più frequente"], ["media", "somma : numero dei dati"], ["mediana", "dato centrale (dati ordinati)"]]))
    faq = [("Che differenza c’è tra media e mediana?", "La media si calcola con tutti i valori; la mediana è il valore che sta in mezzo. Un dato molto grande cambia la media ma poco la mediana."),
           ("Come si scrive la probabilità?", "Con una frazione (casi favorevoli su casi possibili), ma anche con un numero decimale o una percentuale: 1/2 = 0,5 = 50%.")]
    make_unit(R, "statistica-e-probabilita", "D",
              "Rappresentare relazioni e dati e utilizzare le rappresentazioni per ricavare informazioni; usare le nozioni di frequenza, di moda e di media aritmetica; in situazioni concrete, intuire e argomentare qual è il più probabile, dando una prima quantificazione",
              "Statistica e probabilità: moda, media, mediana e probabilità", "Statistica e probabilità",
              "Schede di matematica per la classe quinta su statistica e probabilità: moda, media, mediana, campo di variazione, istogrammi, aerogrammi e probabilità come frazione. 100 esercizi con soluzioni.",
              "Probabilità = casi favorevoli / casi possibili.", "Media = somma : numero dei dati.",
              body, faq, sets, 21, grade=G)


if __name__ == "__main__":
    main()
