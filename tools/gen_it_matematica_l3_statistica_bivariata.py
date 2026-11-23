# -*- coding: utf-8 -*-
"""
Italia Matematica terza liceo: Statistica bivariata (Dati e previsioni)
  python3 tools/gen_it_matematica_l3_statistica_bivariata.py
Tabelle a doppia entrata, frequenze congiunte e marginali, distribuzioni condizionate, indipendenza statistica,
covarianza, retta di regressione (metodo dei minimi quadrati), previsioni, coefficiente di correlazione lineare e sua lettura.
Errori: dividere per il totale generale invece che per il totale di riga, coefficiente angolare cov/var(y), correlazione come causa.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, d, dk, nz

R = random.Random(72310)
G = "terza-liceo"


def dd(x):
    try:
        return d(x)
    except ValueError:
        return dk(x, 2)


def tab2():
    righe = R.choice([("Maschi", "Femmine"), ("Prima", "Seconda"), ("Mattina", "Pomeriggio")])
    col = R.choice([("Calcio", "Basket", "Nuoto"), ("Bus", "Bici", "A piedi"), ("Sì", "No", "Non so")])
    n = [[R.randint(2, 15) for _ in col] for _ in righe]
    return righe, col, n


def show_tab(righe, col, n):
    rows = [[r] + [str(v) for v in n[i]] + [str(sum(n[i]))] for i, r in enumerate(righe)]
    rows.append(["Totale"] + [str(sum(n[i][j] for i in range(len(righe)))) for j in range(len(col))] + [str(sum(map(sum, n)))])
    return table([""] + list(col) + ["Totale"], rows)


def s1_marg():
    righe, col, n = tab2()
    tot = sum(map(sum, n))
    i, j = R.randrange(2), R.randrange(3)
    k = R.choice(["cong", "marg", "rel"])
    t = show_tab(righe, col, n)
    if k == "cong":
        return M("%sQual è la frequenza relativa congiunta di «%s» e «%s»?" % (t, righe[i], col[j]), fq(Fr(n[i][j], tot)), [fq(x) for x in W(Fr(n[i][j], sum(n[i])), Fr(n[i][j], n[0][j] + n[1][j]), Fr(sum(n[i]), tot)) if x != Fr(n[i][j], tot)],
                 "%d : %d (totale generale) = <b>%s</b>." % (n[i][j], tot, fq(Fr(n[i][j], tot))))
    if k == "marg":
        v = n[0][j] + n[1][j]
        return M("%sQual è la frequenza marginale di «%s»?" % (t, col[j]), str(v), [str(x) for x in W(n[0][j], n[1][j], sum(n[0]), v + 1) if x != v],
                 "È il totale della colonna: %d + %d = <b>%d</b>." % (n[0][j], n[1][j], v))
    v = Fr(n[i][j], sum(n[i]))
    return M("%sTra i «%s», quale frazione ha scelto «%s» (distribuzione condizionata)?" % (t, righe[i], col[j]), fq(v), [fq(x) for x in W(Fr(n[i][j], tot), Fr(n[i][j], n[0][j] + n[1][j]), Fr(sum(n[i]), tot)) if x != v],
             "Si divide per il totale della riga «%s»: %d : %d = <b>%s</b>." % (righe[i], n[i][j], sum(n[i]), fq(v)))


def s2_indip():
    righe, col, _ = tab2()
    base = [R.randint(2, 6) for _ in col]
    k = R.choice([1, 2, 3])
    ind = R.random() < 0.5
    n = [base, [b * k for b in base]]
    if not ind:
        j = R.randrange(3)
        n[1] = list(n[1])
        n[1][j] += R.choice([1, 2, 3])
    ans = "sì, le distribuzioni condizionate sono uguali" if ind else "no, le distribuzioni condizionate sono diverse"
    return M("%sI due caratteri sono statisticamente indipendenti?" % show_tab(righe, col, n), ans, ["no, le distribuzioni condizionate sono diverse" if ind else "sì, le distribuzioni condizionate sono uguali", "sì, perché i totali sono diversi", "non si può stabilire"],
             "Confronto le frequenze relative di ogni riga: %s. <b>%s</b>." % ("sono proporzionali (la seconda riga è %d volte la prima)" % k if ind else "non sono proporzionali", ans[0].upper() + ans[1:]))


def data_lin():
    n = R.choice([4, 5])
    xs = sorted(R.sample(range(1, 11), n))
    b = R.choice([2, 3, -1, -2, Fr(1, 2), 1])
    a = R.randint(-3, 8)
    noise = [R.choice([-1, 0, 1]) for _ in xs]
    ys = [a + b * x + e for x, e in zip(xs, noise)]
    if any(Fr(y).denominator != 1 for y in ys):
        return None
    return xs, [int(y) for y in ys]


def stats(xs, ys):
    n = len(xs)
    mx, my = Fr(sum(xs), n), Fr(sum(ys), n)
    cov = Fr(sum((x - mx) * (y - my) for x, y in zip(xs, ys)), n)
    vx = Fr(sum((x - mx) ** 2 for x in xs), n)
    vy = Fr(sum((y - my) ** 2 for y in ys), n)
    return mx, my, cov, vx, vy


def s3_cov():
    dl = data_lin()
    if not dl:
        return None
    xs, ys = dl
    mx, my, cov, vx, vy = stats(xs, ys)
    if (cov * 100).denominator != 1:
        return None
    t = table(["x"] + [str(x) for x in xs], [["y"] + [fq(y) for y in ys]])
    return M("%sCalcola la covarianza di x e y." % t, dd(cov), [dd(v) for v in W(cov * len(xs), cov * len(xs) / (len(xs) - 1), -cov, vx) if v != cov],
             "Medie: x̄ = %s, ȳ = %s. cov = Σ(x − x̄)(y − ȳ)/n = <b>%s</b>." % (dd(mx), dd(my), dd(cov)))


def s3_regr():
    dl = data_lin()
    if not dl:
        return None
    xs, ys = dl
    mx, my, cov, vx, vy = stats(xs, ys)
    b = cov / vx
    a = my - b * mx
    try:
        bs, as_ = d(b), d(a)
    except ValueError:
        return None
    t = table(["x"] + [str(x) for x in xs], [["y"] + [fq(y) for y in ys]])
    ans = "y = %sx %s %s" % (bs, "+" if a >= 0 else "−", d(abs(a)))
    bw = cov / vy if vy else b + 1
    w = ["y = %sx %s %s" % (dd(bw), "+" if a >= 0 else "−", d(abs(a))) if bw != b else "y = %sx %s %s" % (d(b + 1), "+" if a >= 0 else "−", d(abs(a))),
         "y = %sx %s %s" % (bs, "+" if -a >= 0 else "−", d(abs(a))) if a else "y = %sx + 1" % bs, "y = %sx %s %s" % (d(-b), "+" if a >= 0 else "−", d(abs(a)))]
    return M("%sQual è la retta di regressione di y su x (minimi quadrati)?" % t, ans, [x for x in w if x != ans],
             "b = cov(x; y)/var(x) = %s/%s = %s; a = ȳ − b · x̄ = %s − %s · %s = %s: <b>%s</b>." % (dd(cov), dd(vx), bs, dd(my), bs, dd(mx), as_, ans))


def s4_prev():
    a = R.randint(-10, 30)
    b = R.choice([Fr(1, 2), Fr(3, 2), 2, 3, Fr(5, 2), Fr(6, 5), 4])
    a = R.randint(1, 30)
    x = R.randint(2, 20)
    v = a + b * x
    ctx = R.choice([("ore di allenamento", "punteggio"), ("temperatura (°C)", "gelati venduti"), ("pubblicità (migliaia di €)", "vendite (migliaia di €)")])
    return M("La retta di regressione tra %s (x) e %s (y) è y = %sx %s %s. Quale valore di y si prevede per x = %d?" % (ctx[0], ctx[1], d(b), "+" if a >= 0 else "−", abs(a), x), d(v), [d(t) for t in W(a * x + b, b * x, a + b + x, v + b) if t != v],
             "Sostituisco: %s · %d %s %d = <b>%s</b>." % (d(b), x, "+" if a >= 0 else "−", abs(a), d(v)))


R_TXT = [(Fr(95, 100), "correlazione lineare positiva forte"), (Fr(-9, 10), "correlazione lineare negativa forte"), (Fr(5, 100), "correlazione lineare quasi assente"),
         (Fr(45, 100), "correlazione lineare positiva debole"), (Fr(-35, 100), "correlazione lineare negativa debole"), (Fr(1), "i punti stanno tutti su una retta crescente"),
         (Fr(-1), "i punti stanno tutti su una retta decrescente"), (Fr(-2, 100), "correlazione lineare quasi assente"), (Fr(88, 100), "correlazione lineare positiva forte"),
         (Fr(-97, 100), "correlazione lineare negativa forte"), (Fr(3, 10), "correlazione lineare positiva debole"), (Fr(-4, 10), "correlazione lineare negativa debole"), (Fr(1, 100), "correlazione lineare quasi assente")]


def s5_corr():
    if R.random() < 0.5:
        r, a = R.choice(R_TXT)
        opts = ["correlazione lineare positiva forte", "correlazione lineare negativa forte", "correlazione lineare quasi assente", "correlazione lineare positiva debole", "correlazione lineare negativa debole"]
        if a not in opts:
            opts = [a] + opts
        return M("Il coefficiente di correlazione lineare di due variabili è r = %s. Che cosa indica?" % d(r), a, [o for o in opts if o != a][:3],
                 "r va da −1 a 1: il segno dice se y cresce o cala con x, il valore assoluto quanto i punti sono vicini a una retta. Qui: <b>%s</b>." % a)
    qs = [("Il coefficiente di correlazione può valere 1,3?", "no, è sempre compreso tra −1 e 1", ["sì, se la correlazione è molto forte", "sì, se i dati sono molti", "solo se è negativo"]),
          ("Se r = 0,9 tra le vendite di gelati e gli annegamenti, possiamo dire che i gelati causano gli annegamenti?", "no, la correlazione non dimostra un rapporto di causa", ["sì, perché r è vicino a 1", "sì, ma solo d’estate", "no, perché r è minore di 1"]),
          ("Se r = 0, che cosa si può dire?", "non c’è legame lineare (ma potrebbe esserci un legame non lineare)", ["le variabili sono uguali", "c’è una correlazione perfetta", "i dati sono sbagliati"]),
          ("Che segno ha il coefficiente angolare della retta di regressione se r &lt; 0?", "negativo", ["positivo", "nullo", "dipende dalle medie"])]
    q, a, w = R.choice(qs)
    return M(q, a, w, "%s <b>%s</b>." % (q.rstrip("?"), a))


def main():
    seen = set()
    sets = [
        ("Tabelle a doppia entrata", mix(R, seen, [(s1_marg, 20)])),
        ("Distribuzioni condizionate e indipendenza", mix(R, seen, [(s1_marg, 12), (s2_indip, 8)])),
        ("Covarianza", mix(R, seen, [(s3_cov, 16), (s5_corr, 4)])),
        ("Retta di regressione", mix(R, seen, [(s3_regr, 14), (s4_prev, 6)])),
        ("Previsioni e correlazione", mix(R, seen, [(s4_prev, 12), (s5_corr, 8)])),
    ]
    body = L(["Una <b>tabella a doppia entrata</b> riporta le frequenze congiunte di due caratteri. I totali di riga e di colonna sono le frequenze <b>marginali</b>. Una distribuzione <b>condizionata</b> si ottiene dividendo per il totale di una riga (o colonna).",
              "Due caratteri sono <b>indipendenti</b> se le distribuzioni condizionate sono tutte uguali.",
              "Per due variabili numeriche: <b>covarianza</b> cov = Σ(x − x̄)(y − ȳ)/n. La <b>retta di regressione</b> y = a + bx ha b = cov/var(x) e passa per il baricentro (x̄; ȳ).",
              "Il <b>coefficiente di correlazione</b> r = cov/(σ<sub>x</sub>σ<sub>y</sub>) è tra −1 e 1: vicino a ±1 i punti sono quasi allineati, vicino a 0 non c’è legame lineare."],
             [("x: 1, 2, 3; y: 2, 4, 6", ["x̄ = 2, ȳ = 4", "cov = 4/3, var(x) = 2/3"], "b = 2, a = 0: y = 2x"),
              ("r = −0,9", ["Segno negativo, valore vicino a 1"], "forte correlazione negativa")],
             [["Distribuzione condizionata sul totale generale", "Si divide per il totale della riga (o colonna) considerata."],
              ["b = cov/var(y)", "Per la regressione di y su x: b = cov/var(x)."],
              ["Correlazione = causa", "Due variabili possono essere correlate per una terza causa comune."]])
    faq = [("Che cosa vuol dire metodo dei minimi quadrati?", "La retta di regressione è quella che rende minima la somma dei quadrati delle distanze verticali tra i punti e la retta."),
           ("Perché la retta di regressione passa per il baricentro?", "Perché a = ȳ − b x̄: sostituendo x = x̄ si ottiene y = ȳ.")]
    unit(G, R, "statistica-bivariata", "Q",
         "Distribuzioni doppie condizionate e marginali; concetti di deviazione standard, dipendenza, correlazione e regressione",
         "Statistica bivariata", "Statistica bivariata",
         "Schede di matematica per la terza liceo sulla statistica bivariata: tabelle a doppia entrata, frequenze marginali e condizionate, indipendenza, covarianza, retta di regressione, previsioni, coefficiente di correlazione. 100 esercizi con soluzioni.",
         "b = cov(x; y) / var(x)", "La retta di regressione passa per (x̄; ȳ); r è tra −1 e 1.",
         body, faq, sets, 10)


if __name__ == "__main__":
    main()
