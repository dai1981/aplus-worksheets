# -*- coding: utf-8 -*-
"""
Italia Matematica seconda media: Proporzionalità diretta e inversa (Relazioni e funzioni)
  python3 tools/gen_it_matematica_m2_proporzionalita_diretta_e_inversa.py
Grandezze direttamente proporzionali (y/x = k, y = kx, retta per l’origine) e inversamente proporzionali (x · y = k, y = k/x, iperbole);
riconoscere dalla tabella, dalla formula e dal grafico; completare tabelle; problemi del tre semplice diretto e inverso.
Errori: confondere «cresce» con «direttamente proporzionale», usare il rapporto al posto del prodotto, la retta che non passa per l’origine.
"""
import random
from fractions import Fraction as Fr
from it_media import M, L, unit, mix, table, W, num, fq, d, dk, kurve, Kids
from de_common import BLUE

R = random.Random(71204)
G = "seconda-media"
K = Kids(R)


def ore(x):
    x = Fr(x)
    return "1 ora" if x == 1 else "%s ore" % d(x)


def eu(x):
    return "%s €" % dk(x, 2)


def tab(xs, ys, nx="x", ny="y"):
    return table([nx] + [str(x) for x in xs], [[ny] + [str(y) for y in ys]])


def s1_riconosci():
    k = R.choice(["dir", "inv", "no"])
    xs = sorted(R.sample(range(1, 13), 4))
    if k == "dir":
        c = R.randint(2, 9)
        ys = [c * x for x in xs]
    elif k == "inv":
        c = R.choice([12, 24, 36, 48, 60, 72, 120])
        xs = sorted(R.sample([x for x in range(1, 13) if c % x == 0], 4))
        ys = [c // x for x in xs]
    else:
        c, q = R.randint(2, 6), R.randint(1, 5)
        ys = [c * x + q for x in xs]
    ans = {"dir": "direttamente proporzionali", "inv": "inversamente proporzionali", "no": "né direttamente né inversamente proporzionali"}[k]
    e = {"dir": "y : x = %d sempre: <b>direttamente proporzionali</b>." % c, "inv": "x × y = %d sempre: <b>inversamente proporzionali</b>." % c,
         "no": "y : x non è costante (%s, %s…) e neanche x × y: <b>né direttamente né inversamente</b>." % (fq(Fr(ys[0], xs[0])), fq(Fr(ys[1], xs[1])))}[k]
    others = [v for v in ["direttamente proporzionali", "inversamente proporzionali", "né direttamente né inversamente proporzionali"] if v != ans]
    return M("Osserva la tabella. Le grandezze x e y sono…<br>%s" % tab(xs, ys), ans, others + ["uguali"], e)


def s1_quiz():
    q, a, w = R.choice([
        ("Il costo di un certo numero di quaderni uguali e il numero dei quaderni sono…", "direttamente proporzionali", ["inversamente proporzionali", "non proporzionali", "uguali"]),
        ("Il numero di operai e il tempo per finire lo stesso lavoro sono…", "inversamente proporzionali", ["direttamente proporzionali", "non proporzionali", "uguali"]),
        ("La velocità e il tempo per fare lo stesso percorso sono…", "inversamente proporzionali", ["direttamente proporzionali", "non proporzionali", "uguali"]),
        ("Il lato di un quadrato e il suo perimetro sono…", "direttamente proporzionali", ["inversamente proporzionali", "non proporzionali", "uguali"]),
        ("L’età di una persona e la sua altezza sono…", "non proporzionali", ["direttamente proporzionali", "inversamente proporzionali", "uguali"]),
        ("Il lato di un quadrato e la sua area sono…", "non proporzionali", ["direttamente proporzionali", "inversamente proporzionali", "uguali"]),
        ("Il numero di amici che dividono una pizza in parti uguali e la parte di ognuno sono…", "inversamente proporzionali", ["direttamente proporzionali", "non proporzionali", "uguali"]),
        ("I litri di benzina e il prezzo pagato sono…", "direttamente proporzionali", ["inversamente proporzionali", "non proporzionali", "uguali"]),
        ("Il grafico di due grandezze direttamente proporzionali è…", "una retta che passa per l’origine", ["un ramo di iperbole", "una retta che non passa per l’origine", "una parabola"]),
        ("Il grafico di due grandezze inversamente proporzionali è…", "un ramo di iperbole", ["una retta che passa per l’origine", "una retta orizzontale", "una parabola"]),
        ("Se x e y sono direttamente proporzionali e x raddoppia, y…", "raddoppia", ["si dimezza", "resta uguale", "aumenta di 2"]),
        ("Se x e y sono inversamente proporzionali e x triplica, y…", "diventa la terza parte", ["triplica", "resta uguale", "diminuisce di 3"]),
        ("Quale formula indica una proporzionalità diretta?", "y = 4x", ["y = 4/x", "y = 4x + 1", "y = x²"]),
        ("Quale formula indica una proporzionalità inversa?", "y = 12/x", ["y = 12x", "y = x + 12", "y = 12 − x"]),
    ])
    return M(q, a, w, "Risposta: <b>%s</b>." % a)


def s2_completa():
    k = R.choice(["dir", "inv"])
    if k == "dir":
        c = R.randint(2, 12)
        xs = sorted(R.sample(range(1, 15), 4))
        ys = [c * x for x in xs]
        i = R.randint(1, 3)
        x = ys[i]
        shown = [str(v) if j != i else "?" for j, v in enumerate(ys)]
        return M("x e y sono direttamente proporzionali. Quale numero va al posto di ?<br>%s" % table(["x"] + [str(v) for v in xs], [["y"] + shown]),
                 str(x), W(x + c, xs[i] + c, Fr(c * xs[0] * xs[i], 1) // max(1, ys[0]) + 1, x - c),
                 "k = y : x = %d : %d = %d; y = %d × %d = <b>%d</b>." % (ys[0], xs[0], c, c, xs[i], x))
    c = R.choice([24, 36, 48, 60, 72, 90, 120, 180])
    xs = sorted(R.sample([v for v in range(1, 31) if c % v == 0], 4))
    ys = [c // v for v in xs]
    i = R.randint(1, 3)
    x = ys[i]
    shown = [str(v) if j != i else "?" for j, v in enumerate(ys)]
    return M("x e y sono inversamente proporzionali. Quale numero va al posto di ?<br>%s" % table(["x"] + [str(v) for v in xs], [["y"] + shown]),
             str(x), W(ys[0] * xs[i] // xs[0] if ys[0] * xs[i] % xs[0] == 0 else None, x + 1, x * 2, ys[0] - (xs[i] - xs[0]), x - 1, c // xs[i - 1] if i > 1 else None),
             "k = x × y = %d × %d = %d; y = %d : %d = <b>%d</b>." % (xs[0], ys[0], c, c, xs[i], x))


def s2_costante():
    k = R.choice(["dir", "inv"])
    if k == "dir":
        c = R.randint(2, 15)
        x = R.randint(2, 12)
        return M("y è direttamente proporzionale a x. Per x = %d si ha y = %d. Qual è la formula?" % (x, c * x), "y = %dx" % c, ["y = %d/x" % (c * x * x), "y = x + %d" % (c * x - x), "y = %dx" % (c * x)],
                 "k = %d : %d = %d, quindi <b>y = %dx</b>." % (c * x, x, c, c))
    x, y = R.randint(2, 12), R.randint(2, 12)
    return M("y è inversamente proporzionale a x. Per x = %d si ha y = %d. Qual è la formula?" % (x, y), "y = %d/x" % (x * y), ["y = %sx" % fq(Fr(y, x)) if y % x == 0 else "y = %dx" % (x * y), "y = %d/x" % (x + y), "y = x + %d" % abs(y - x) if y != x else "y = %d − x" % (2 * y)],
             "k = %d × %d = %d, quindi <b>y = %d/x</b>." % (x, y, x * y, x * y))


def s3_grafico():
    k = R.choice(["dir", "inv", "lin"])
    if k == "dir":
        c = R.choice([Fr(1, 2), Fr(1), Fr(2), Fr(3), Fr(3, 2)])
        f = lambda x: float(c) * x
        x0 = 2 if c.denominator == 2 else R.choice([1, 2])
        pts = [(x0, c * x0, "")]
    elif k == "inv":
        c = R.choice([4, 6, 8, 12])
        f = lambda x: c / x if x > 0.05 else None
        x0 = R.choice([v for v in (1, 2, 3, 4, 6) if c % v == 0 and c // v <= 12])
        pts = [(x0, c // x0, "")]
    else:
        c, q = R.choice([1, 2]), R.choice([1, 2, 3])
        f = lambda x: c * x + q
        pts = [(1, c + q, "")]
    pic = kurve([(f, BLUE, "")], (0, 8, 1), (0, 12, 2), pts=pts, W=300, H=290, label="grafico di due grandezze")
    ans = {"dir": "proporzionalità diretta", "inv": "proporzionalità inversa", "lin": "nessuna delle due"}[k]
    e = {"dir": "È una retta che passa per l’origine: <b>proporzionalità diretta</b>.", "inv": "È un ramo di iperbole (x × y costante): <b>proporzionalità inversa</b>.",
         "lin": "È una retta ma non passa per l’origine: <b>nessuna delle due</b>."}[k]
    return M("%sChe tipo di relazione mostra il grafico? (punto evidenziato: x = %s, y = %s)" % (pic, d(pts[0][0]), d(pts[0][1])), ans,
             [v for v in ["proporzionalità diretta", "proporzionalità inversa", "nessuna delle due"] if v != ans] + ["non si può dire"], e)


def s3_valore():
    k = R.choice(["dir", "inv"])
    if k == "dir":
        c = R.randint(2, 9)
        x = R.randint(2, 15)
        return M("Considera la funzione y = %dx. Quanto vale y quando x = %d?" % (c, x), str(c * x), W(c + x, c * x + c, x, c * (x - 1)), "y = %d × %d = <b>%d</b>." % (c, x, c * x))
    c = R.choice([12, 24, 36, 48, 60, 72, 84, 96])
    x = R.choice([v for v in range(2, 13) if c % v == 0])
    return M("Considera la funzione y = %d/x. Quanto vale y quando x = %d?" % (c, x), str(c // x), W(c * x, c - x, c // x + 1, c // x * 2), "y = %d : %d = <b>%d</b>." % (c, x, c // x))


def s4_tre_diretto():
    p = K.next()
    k = R.choice(["kg", "km", "ore", "pagine"])
    if k == "kg":
        a, pr = R.randint(2, 6), R.choice([150, 180, 240, 320, 450, 360])
        b = R.randint(2, 10)
        if a == b:
            return None
        return M("%d kg di mele costano %s. Quanto costano %d kg?" % (a, eu(Fr(pr * a, 100)), b), eu(Fr(pr * b, 100)), W(eu(Fr(pr * a, 100) + b - a), eu(Fr(pr * a * b, 100)), eu(Fr(pr, 100) * a / b) if (Fr(pr * a, 100) / b * 100).denominator == 1 else None, eu(Fr(pr * (b + 1), 100))),
                 "1 kg costa %s : %d = %s €; %d kg costano <b>%s</b>." % (dk(Fr(pr * a, 100), 2), a, dk(Fr(pr, 100), 2), b, eu(Fr(pr * b, 100))))
    if k == "km":
        l, km = R.randint(3, 8), R.choice([12, 15, 16, 18, 20])
        b = R.randint(2, 12) * 5
        tot = b * l
        return M("Un’auto con %d litri di benzina percorre %d km. Quanti km percorre con %d litri?" % (l, l * km, b), "%s km" % num(b * km), W("%s km" % num(l * km + b), "%s km" % num(b * l), "%s km" % num((b + l) * km), "%s km" % num(b * km // 2)),
                 "Con 1 litro percorre %d km; con %d litri <b>%s km</b>." % (km, b, num(b * km)))
    if k == "ore":
        h, eur = R.randint(2, 6), R.choice([8, 9, 10, 12, 15])
        b = R.randint(2, 10)
        if b == h:
            return None
        return M("%s guadagna %d € in %d ore di lavoro. Quanto guadagna in %d ore?" % (p[0], h * eur, h, b), "%d €" % (b * eur), W("%d €" % (h * eur + b), "%d €" % (h * eur * b), "%d €" % ((b + 1) * eur), "%d €" % (b * eur + h)),
                 "In 1 ora guadagna %d €; in %d ore <b>%d €</b>." % (eur, b, b * eur))
    pg, mn = R.randint(4, 10), R.choice([2, 3, 4, 5])
    b = R.randint(11, 40)
    return M("%s legge %d pagine in %d minuti. Quanti minuti impiega per %d pagine allo stesso ritmo?" % (p[0], pg, pg * mn, b), "%d minuti" % (b * mn), W("%d minuti" % (pg * mn + b), "%d minuti" % (b * mn + mn), "%d minuti" % b, "%d minuti" % (b * pg)),
             "1 pagina in %d minuti; %d pagine in <b>%d minuti</b>." % (mn, b, b * mn))


def s4_tre_inverso():
    k = R.choice(["operai", "vel", "rubinetti", "pizza"])
    if k == "operai":
        a, g = R.randint(2, 8), R.randint(3, 12)
        t = a * g
        b = R.choice([v for v in range(2, 25) if t % v == 0 and v != a])
        return M("%d operai fanno un lavoro in %d giorni. Quanti giorni impiegano %d operai (allo stesso ritmo)?" % (a, g, b), "%d giorni" % (t // b) if t // b != 1 else "1 giorno",
                 W("%d giorni" % (g * b // a) if g * b % a == 0 and g * b // a != 1 else None, "%d giorni" % (g + a - b) if g + a - b > 1 else None, "%d giorni" % (t), "%d giorni" % (t // b + 1), "%d giorni" % (t // b * 2), "%d giorni" % (g * b)),
                 "Lavoro totale: %d × %d = %d giornate; %d : %d = <b>%d</b>." % (a, g, t, t, b, t // b))
    if k == "vel":
        v, h = R.choice([40, 50, 60, 80, 90, 100, 120]), R.randint(2, 6)
        s = v * h
        v2 = R.choice([x for x in (40, 50, 60, 75, 80, 90, 100, 120, 150) if s % x == 0 and x != v])
        return M("Andando a %d km/h un viaggio dura %d ore. Quante ore dura andando a %d km/h?" % (v, h, v2), ore(Fr(s, v2)),
                 W(ore(Fr(h * v2, v)) if Fr(h * v2, v).denominator in (1, 2, 4, 5) else None, ore(h + 1), ore(h * 2), ore(Fr(s, v2) + 1), ore(Fr(s, v2) * 2), ore(h + 2), ore(Fr(s, v2) - 1) if Fr(s, v2) > 1 else None),
                 "Percorso: %d × %d = %d km; %d : %d = <b>%s</b>." % (v, h, s, s, v2, ore(Fr(s, v2))))
    if k == "rubinetti":
        a, m = R.randint(2, 5), R.choice([12, 15, 20, 24, 30, 36])
        t = a * m
        b = R.choice([v for v in range(2, 13) if t % v == 0 and v != a])
        return M("Con %d rubinetti uguali una vasca si riempie in %d minuti. In quanti minuti si riempie con %d rubinetti?" % (a, m, b), "%d minuti" % (t // b),
                 W("%d minuti" % (m * b // a) if m * b % a == 0 else None, "%d minuti" % (m + a - b) if m + a - b > 0 else None, "%d minuti" % t, "%d minuti" % (t // b + a)),
                 "%d × %d = %d; %d : %d = <b>%d minuti</b>." % (a, m, t, t, b, t // b))
    a, f = R.randint(2, 6), R.choice([4, 6, 8, 12])
    t = a * f
    b = R.choice([v for v in range(2, 13) if t % v == 0 and v != a])
    return M("Una torta divisa tra %d amici dà %d pezzetti a testa. Quanti pezzetti a testa se la stessa torta, con lo stesso numero di pezzetti, si divide tra %d amici?" % (a, f, b), str(t // b),
             W(f * b // a if f * b % a == 0 else None, f + a - b if f + a - b > 0 else None, t, t // b + 1, t // b * 2, f * b), "Pezzetti: %d × %d = %d; %d : %d = <b>%d</b>." % (a, f, t, t, b, t // b))


def main():
    seen = set()
    sets = [
        ("Riconoscere la proporzionalità", mix(R, seen, [(s1_riconosci, 10), (s1_quiz, 10)])),
        ("Tabelle e costante", mix(R, seen, [(s2_completa, 12), (s2_costante, 8)])),
        ("Grafici e formule", mix(R, seen, [(s3_grafico, 10), (s3_valore, 10)])),
        ("Problemi diretti", mix(R, seen, [(s4_tre_diretto, 20)])),
        ("Problemi inversi", mix(R, seen, [(s4_tre_inverso, 20)])),
    ]
    body = L(["Due grandezze sono <b>direttamente proporzionali</b> se il loro <b>rapporto</b> è costante: y : x = k, cioè y = kx. Se una raddoppia, anche l’altra raddoppia. Il grafico è una <b>retta che passa per l’origine</b>.",
              "Sono <b>inversamente proporzionali</b> se il loro <b>prodotto</b> è costante: x × y = k, cioè y = k/x. Se una raddoppia, l’altra si dimezza. Il grafico è un <b>ramo di iperbole</b>.",
              "Per i problemi (il «tre semplice») trova prima la costante: il valore per 1 (diretta) oppure il totale (inversa)."],
             [("3 quaderni costano 6 €. Quanto costano 7 quaderni?", ["1 quaderno costa 6 : 3 = 2 €", "7 × 2 = 14"], "14 €"),
              ("4 operai finiscono in 6 giorni. In quanti giorni finiscono 8 operai?", ["totale: 4 × 6 = 24 giornate", "24 : 8 = 3"], "3 giorni")],
             [["«Cresce insieme, quindi è proporzionale»", "Età e altezza crescono insieme ma il rapporto non è costante."],
              ["Usare il rapporto per l’inversa", "Nell’inversa è costante il prodotto x × y."],
              ["Retta che non passa per l’origine", "y = 2x + 1 non è una proporzionalità diretta."]],
             table(["", "Diretta", "Inversa"], [["costante", "y : x = k", "x × y = k"], ["formula", "y = kx", "y = k/x"], ["grafico", "retta per l’origine", "iperbole"]]))
    faq = [("Come capisco se due grandezze sono inversamente proporzionali?", "Moltiplica i valori corrispondenti: se il prodotto è sempre lo stesso, sono inversamente proporzionali."),
           ("Perché y = 2x + 1 non è una proporzionalità diretta?", "Perché il rapporto y : x cambia (per x = 1 è 3, per x = 2 è 2,5) e il grafico non passa per l’origine.")]
    unit(G, R, "proporzionalita-diretta-e-inversa", "F",
         "Riconoscere grandezze direttamente e inversamente proporzionali; usare le formule y = kx e y = k/x e i loro grafici; risolvere problemi",
         "Proporzionalità diretta e inversa", "Proporzionalità",
         "Schede di matematica per la seconda media sulla proporzionalità diretta e inversa: tabelle, costante, formule y = kx e y = k/x, grafici e problemi del tre semplice. 100 esercizi con soluzioni.",
         "Diretta: y : x costante. Inversa: x × y costante.", "Diretta: retta per l’origine. Inversa: iperbole.",
         body, faq, sets, 4)


if __name__ == "__main__":
    main()
