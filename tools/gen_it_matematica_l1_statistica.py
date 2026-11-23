# -*- coding: utf-8 -*-
"""
Italia Matematica prima liceo: Statistica (Dati e previsioni)
  python3 tools/gen_it_matematica_l1_statistica.py
Frequenze assolute, relative e percentuali, media aritmetica e ponderata, mediana, moda, campo di variazione,
varianza e scarto quadratico medio (deviazione standard), valore mancante per una media data.
Errori: mediana senza ordinare i dati, media ponderata come media delle modalità, varianza senza elevare al quadrato.
"""
import math
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, d, dk

R = random.Random(72110)
G = "prima-liceo"
CTX = [("i voti di una verifica", ""), ("le ore di sonno di alcuni studenti", " h"), ("i gol segnati in alcune partite", ""),
       ("le temperature massime di una settimana", " °C"), ("i minuti di viaggio per arrivare a scuola", " min"), ("i libri letti in un anno", "")]


def lst(xs):
    return "; ".join(str(x) for x in xs)


def nice(v):
    v = Fr(v)
    try:
        return d(v)
    except ValueError:
        return dk(v, 2) if True else fq(v)


def s1_media():
    n = R.randint(5, 8)
    xs = [R.randint(3, 10) for _ in range(n)]
    s = sum(xs)
    if (Fr(s, n) * 100).denominator != 1:
        return None
    c, u = R.choice(CTX)
    m = Fr(s, n)
    srt = sorted(xs)
    med = Fr(srt[n // 2]) if n % 2 else Fr(srt[n // 2 - 1] + srt[n // 2], 2)
    w = [med, Fr(s, n - 1), Fr(max(xs) + min(xs), 2)]
    return M("Ecco %s: %s. Calcola la media aritmetica." % (c, lst(xs)), nice(m), [nice(x) for x in w if x != m] + [nice(m + 1)],
             "Somma dei dati : numero dei dati = %d : %d = <b>%s</b>." % (s, n, nice(m)))


def s1_mediana():
    n = R.randint(5, 9)
    xs = R.sample(range(1, 30), n)
    srt = sorted(xs)
    med = Fr(srt[n // 2]) if n % 2 else Fr(srt[n // 2 - 1] + srt[n // 2], 2)
    unsorted = Fr(xs[n // 2]) if n % 2 else Fr(xs[n // 2 - 1] + xs[n // 2], 2)
    w = [unsorted, Fr(sum(xs), n), Fr(srt[n // 2]) if n % 2 == 0 else Fr(srt[n // 2 - 1])]
    return M("Trova la mediana dei dati: %s." % lst(xs), nice(med), [nice(x) for x in w if x != med] + [nice(med + 1)],
             "Ordino i dati: %s. %s: <b>%s</b>." % (lst(srt), "Il valore centrale" if n % 2 else "La media dei due valori centrali", nice(med)))


def s1_moda():
    vals = R.sample(range(2, 12), 4)
    mo = vals[0]
    xs = [mo] * 3 + [vals[1]] * 2 + [vals[2]] + [vals[3]]
    R.shuffle(xs)
    w = [vals[1], max(xs), sorted(xs)[len(xs) // 2] if sorted(xs)[len(xs) // 2] != mo else min(xs), 3, min(xs)]
    return M("Qual è la moda dei dati %s?" % lst(xs), str(mo), [str(x) for x in w if x != mo] + [str(len(set(xs)))],
             "La moda è il dato con la frequenza più alta: %d compare 3 volte, quindi <b>%d</b>." % (mo, mo))


def s2_freq():
    cats = R.choice([["calcio", "nuoto", "basket", "pallavolo"], ["rosso", "blu", "verde", "giallo"], ["treno", "autobus", "bici", "a piedi"]])
    tot = R.choice([20, 25, 40, 50])
    fs = []
    left = tot
    for i in range(3):
        f = R.randint(2, left - (3 - i) * 2)
        fs.append(f)
        left -= f
    fs.append(left)
    i = R.randrange(4)
    k = R.choice(["rel", "perc"])
    if k == "rel":
        v = Fr(fs[i], tot)
        ans = d(v)
        w = [d(Fr(fs[i], 100)), str(fs[i]), d(Fr(tot - fs[i], tot))]
        e = "Frequenza relativa = %d : %d = <b>%s</b>." % (fs[i], tot, ans)
        q = "Qual è la frequenza relativa di «%s»?" % cats[i]
    else:
        v = Fr(fs[i] * 100, tot)
        ans = "%s%%" % d(v)
        w = ["%d%%" % fs[i], "%s%%" % d(Fr(fs[i], tot)), "%s%%" % d(100 - v)]
        e = "%d : %d = %s, cioè <b>%s</b>." % (fs[i], tot, d(Fr(fs[i], tot)), ans)
        q = "Qual è la frequenza percentuale di «%s»?" % cats[i]
    tab = table(["Modalità"] + cats, [["Frequenza"] + [str(f) for f in fs]])
    return M("%s%s" % (tab, q), ans, [x for x in w if x != ans], e)


def s2_pond():
    xs = sorted(R.sample(range(4, 11), 4))
    fs = [R.randint(1, 6) for _ in xs]
    n = sum(fs)
    s = sum(x * f for x, f in zip(xs, fs))
    m = Fr(s, n)
    if (m * 100).denominator != 1:
        return None
    tab = table(["Voto"] + [str(x) for x in xs], [["Numero di studenti"] + [str(f) for f in fs]])
    w = [Fr(sum(xs), len(xs)), Fr(s, len(xs)), Fr(sum(fs), len(fs))]
    return M("%sCalcola la media dei voti della classe." % tab, nice(m), [nice(x) for x in w if x != m] + [nice(m + Fr(1, 2))],
             "Media ponderata: (%s) : %d = %d : %d = <b>%s</b>." % (" + ".join("%d · %d" % (x, f) for x, f in zip(xs, fs)), n, s, n, nice(m)))


def s3_campo():
    n = R.randint(6, 9)
    xs = [R.randint(-5, 30) for _ in range(n)]
    c = max(xs) - min(xs)
    w = [max(xs), max(xs) + min(xs), max(xs) - sorted(xs)[1]]
    return M("Le temperature minime registrate sono: %s (°C). Qual è il campo di variazione?" % lst([fq(x) for x in xs]), "%d °C" % c, ["%s °C" % fq(x) for x in w if x != c] + ["%d °C" % (c + 1)],
             "Campo di variazione = massimo − minimo = %s − (%s) = <b>%d °C</b>." % (fq(max(xs)), fq(min(xs)), c))


def s3_var():
    m = R.randint(4, 8)
    devs = R.choice([[-2, 0, 2], [-1, 1, -1, 1], [-3, -1, 1, 3], [-2, -2, 2, 2], [-4, 0, 0, 4], [-1, 0, 1], [-2, 1, 1], [-3, 0, 3], [-2, -1, 0, 1, 2], [-4, -2, 2, 4]])
    xs = [m + t for t in devs]
    R.shuffle(xs)
    n = len(xs)
    var = Fr(sum(t * t for t in devs), n)
    if (var * 100).denominator != 1:
        return None
    sd = math.sqrt(var)
    k = R.choice(["var", "sd"]) if abs(sd - round(sd)) < 1e-9 else "var"
    if k == "var":
        w = [Fr(sum(abs(t) for t in devs), n), Fr(sum(t * t for t in devs), n - 1), Fr(sum(t * t for t in devs))]
        return M("Calcola la varianza dei dati %s." % lst(xs), nice(var), [nice(x) for x in w if x != var] + [nice(var + 1)],
                 "Media = %d. Varianza = media dei quadrati degli scarti = (%s) : %d = <b>%s</b>." % (m, " + ".join(str(t * t) for t in devs), n, nice(var)))
    w = [var, Fr(sum(abs(t) for t in devs), n), Fr(int(round(sd))) + 1, Fr(sum(t * t for t in devs)), Fr(int(round(sd)) * 2)]
    return M("Calcola lo scarto quadratico medio (deviazione standard) dei dati %s." % lst(xs), str(int(round(sd))), [nice(x) for x in w if x != int(round(sd))] + [str(int(round(sd)) + 2)],
             "Media = %d, varianza = %s; lo scarto quadratico medio è la radice della varianza: <b>%d</b>." % (m, nice(var), int(round(sd))))


def s4_manca():
    n = R.randint(3, 5)
    xs = [R.randint(4, 9) for _ in range(n)]
    t = R.randint(6, 8)
    need = t * (n + 1) - sum(xs)
    if not 1 <= need <= 10:
        return None
    w = [t, need - 1, t * n - sum(xs) if t * n - sum(xs) > 0 else need + 2]
    return M("Giulia ha preso %s. Che voto deve prendere nella prossima verifica per avere la media %d?" % (", ".join(map(str, xs[:-1])) + " e " + str(xs[-1]), t), str(need), [str(x) for x in w if x != need] + [str(need + 1)],
             "Servono %d · %d = %d punti in tutto; ne ha %d: %d − %d = <b>%d</b>." % (t, n + 1, t * (n + 1), sum(xs), t * (n + 1), sum(xs), need))


def s4_cambia():
    n = R.randint(4, 7)
    xs = [R.randint(10, 30) for _ in range(n)]
    k = R.choice([2, 3, 5, 10])
    op = R.choice(["somma", "per"])
    m = Fr(sum(xs), n)
    if (m * 100).denominator != 1:
        return None
    if op == "somma":
        v = m + k
        q = "La media dei dati %s è %s. Se si aggiunge %d a ogni dato, quanto diventa la media?" % (lst(xs), nice(m), k)
        w = [m, m + Fr(k, n), m * k]
        e = "Aggiungendo %d a tutti i dati anche la media aumenta di %d: <b>%s</b>." % (k, k, nice(v))
    else:
        v = m * k
        q = "La media dei dati %s è %s. Se si moltiplica ogni dato per %d, quanto diventa la media?" % (lst(xs), nice(m), k)
        w = [m, m + k, m * k * k]
        e = "Moltiplicando tutti i dati per %d anche la media si moltiplica per %d: <b>%s</b>." % (k, k, nice(v))
    return M(q, nice(v), [nice(x) for x in w if x != v], e)


def s5_conf():
    a = [R.randint(5, 8) for _ in range(5)]
    mu = R.randint(6, 7)
    A = [mu - 1, mu, mu, mu, mu + 1]
    B = [mu - 3, mu - 2, mu, mu + 2, mu + 3]
    R.shuffle(A)
    R.shuffle(B)
    nA, nB = R.sample(["Sezione A", "Sezione B"], 2)
    q = "Due classi hanno questi voti. %s: %s. %s: %s. Hanno la stessa media %d. Quale classe ha i voti più dispersi (scarto quadratico medio maggiore)?" % (nA, lst(A), nB, lst(B), mu)
    return M(q, nB, [nA, "hanno la stessa dispersione", "non si può dire senza la moda"],
             "Gli scarti dalla media di %s sono più grandi (fino a 3), quindi lo scarto quadratico medio è maggiore: <b>%s</b>." % (nB, nB))


def main():
    seen = set()
    sets = [
        ("Media, mediana e moda", mix(R, seen, [(s1_media, 8), (s1_mediana, 8), (s1_moda, 4)])),
        ("Frequenze e media ponderata", mix(R, seen, [(s2_freq, 10), (s2_pond, 10)])),
        ("Campo di variazione e varianza", mix(R, seen, [(s3_campo, 6), (s3_var, 14)])),
        ("Proprietà della media", mix(R, seen, [(s4_manca, 10), (s4_cambia, 10)])),
        ("Confrontare dati", mix(R, seen, [(s5_conf, 4), (s2_pond, 6), (s1_mediana, 5), (s4_manca, 5)])),
    ]
    body = L(["La <b>frequenza assoluta</b> conta quante volte compare un dato; la <b>relativa</b> è frequenza : totale (in percentuale × 100).",
              "<b>Media aritmetica</b>: somma dei dati : numero dei dati. Con una tabella di frequenze si usa la <b>media ponderata</b>: Σ x · f : Σ f.",
              "<b>Mediana</b>: il valore centrale dei dati <b>ordinati</b> (con un numero pari di dati, la media dei due centrali). <b>Moda</b>: il dato più frequente.",
              "La dispersione si misura con il <b>campo di variazione</b> (massimo − minimo) e con la <b>varianza</b> (media dei quadrati degli scarti dalla media). Lo <b>scarto quadratico medio</b> è la radice quadrata della varianza."],
             [("Dati 4; 6; 8; 10. Varianza?", ["Media 7; scarti −3, −1, 1, 3.", "(9 + 1 + 1 + 9) : 4 = 5."], "5"),
              ("Mediana di 7; 2; 9; 4", ["Ordino: 2; 4; 7; 9.", "(4 + 7) : 2."], "5,5")],
             [["Trovare la mediana senza ordinare", "Prima si ordinano i dati dal più piccolo al più grande."],
              ["Media ponderata come media dei voti", "Ogni voto conta tante volte quanti studenti l’hanno preso."],
              ["Varianza come media degli scarti", "Gli scarti hanno somma 0: vanno elevati al quadrato."]])
    faq = [("Quando usare la mediana invece della media?", "Quando ci sono valori molto diversi dagli altri (valori anomali): la media ne è influenzata molto, la mediana poco. Per esempio con gli stipendi."),
           ("Che differenza c’è tra varianza e scarto quadratico medio?", "La varianza è la media dei quadrati degli scarti; lo scarto quadratico medio è la sua radice quadrata e si misura nella stessa unità dei dati.")]
    unit(G, R, "statistica", "Q",
         "Rappresentare e analizzare dati: frequenze, indici di posizione (media, mediana, moda) e di variabilità (campo di variazione, varianza, scarto quadratico medio)",
         "Statistica", "Statistica",
         "Schede di matematica per la prima liceo sulla statistica: frequenze relative e percentuali, media aritmetica e ponderata, mediana, moda, campo di variazione, varianza e scarto quadratico medio. 100 esercizi con soluzioni.",
         "Varianza = media dei quadrati degli scarti", "Scarto quadratico medio = √varianza; la mediana si trova sui dati ordinati.",
         body, faq, sets, 10)


if __name__ == "__main__":
    main()
