# -*- coding: utf-8 -*-
"""
Italia Matematica terza media: Statistica e indici di posizione (Dati e previsioni)
  python3 tools/gen_it_matematica_m3_statistica_e_indici_di_posizione.py
Popolazione e campione, caratteri qualitativi e quantitativi, distribuzioni di frequenza (relative, percentuali, cumulate),
media aritmetica semplice e ponderata, mediana (numero pari e dispari di dati), moda, campo di variazione,
scegliere l’indice adatto, dati raggruppati in classi, aerogramma (gradi).
Errori: mediana senza ordinare i dati, media ponderata come media dei valori, dimenticare di dividere per il totale delle frequenze.
"""
import random
from fractions import Fraction as Fr
from it_media import M as M0, L, unit, mix, table, W, d, dk, num, Kids

R = random.Random(71313)
G = "terza-media"
K = Kids(R)


def M(q, a, w, e):
    return M0(q, a, w, e.replace("= <b>≈ ", "≈ <b>").replace("= ≈ ", "≈ "))


def dd(x):
    x = Fr(x)
    try:
        return d(x)
    except ValueError:
        return "≈ " + dk(x, 2)


def lista(xs):
    return "; ".join(dd(x) for x in xs)


def s1_concetti():
    q, a, w = R.choice([
        ("Si intervistano 200 studenti di una scuola di 900 per conoscere lo sport preferito. I 200 studenti sono…", "il campione", ["la popolazione", "la frequenza", "la moda"]),
        ("Si intervistano 200 studenti di una scuola di 900. I 900 studenti sono…", "la popolazione", ["il campione", "la frequenza", "la mediana"]),
        ("Il colore degli occhi è un carattere…", "qualitativo", ["quantitativo", "numerico continuo", "ordinato"]),
        ("L’altezza in cm è un carattere…", "quantitativo", ["qualitativo", "solo nominale", "non misurabile"]),
        ("Quale indice si può calcolare anche per un carattere qualitativo (es. il colore preferito)?", "la moda", ["la media", "la mediana", "il campo di variazione"]),
        ("Quale indice è più adatto se tra i dati c’è un valore molto più grande degli altri?", "la mediana", ["la media", "il campo di variazione", "la somma"]),
        ("Il campo di variazione indica…", "quanto sono distanti il dato più grande e il più piccolo", ["il dato più frequente", "il dato centrale", "la media dei dati"]),
        ("La somma delle frequenze relative di tutti i valori è…", "1", ["100", "il numero dei dati", "0"]),
        ("La frequenza cumulata di un valore è…", "la somma delle frequenze di quel valore e dei precedenti", ["la frequenza più alta", "la frequenza diviso il totale", "il numero dei valori"]),
        ("In un aerogramma, a una frequenza percentuale del 25% corrisponde un settore di…", "90°", ["25°", "45°", "180°"]),
    ])
    return M(q, a, w, "Risposta: <b>%s</b>." % a)


def data(n, lo=1, hi=30):
    return [R.randint(lo, hi) for _ in range(n)]


def s2_indici():
    n = R.choice([5, 6, 7, 8, 9, 10])
    xs = data(n, 2, 40)
    k = R.choice(["media", "mediana", "moda", "campo"])
    s = sorted(xs)
    if k == "media":
        m = Fr(sum(xs), n)
        if (m * 100).denominator != 1:
            return None
        return M("Calcola la media aritmetica dei dati: %s" % lista(xs), dd(m), W(dd(Fr(sum(xs), n - 1)) if (Fr(sum(xs), n - 1) * 100).denominator == 1 else None, dd(Fr(s[n // 2] + s[(n - 1) // 2], 2)) if Fr(s[n // 2] + s[(n - 1) // 2], 2) != m else None, num(sum(xs)), dd(m + 1)),
                 "Somma: %d; numero dei dati: %d; media = %d : %d = <b>%s</b>." % (sum(xs), n, sum(xs), n, dd(m)))
    if k == "mediana":
        med = Fr(s[n // 2] + s[(n - 1) // 2], 2)
        mid_unsorted = Fr(xs[n // 2] + xs[(n - 1) // 2], 2)
        return M("Calcola la mediana dei dati: %s" % lista(xs), dd(med), W(dd(mid_unsorted) if mid_unsorted != med else None, dd(Fr(sum(xs), n)) if (Fr(sum(xs), n) * 100).denominator == 1 and Fr(sum(xs), n) != med else None, dd(s[n // 2]) if n % 2 == 0 and s[n // 2] != med else dd(s[n // 2 + 1]), dd(med + 1), dd(med - 1), dd(med + 2)),
                 "Ordino: %s. %s <b>%s</b>." % (lista(s), ("Il dato centrale è" if n % 2 else "I due centrali sono %d e %d: la loro media è" % (s[n // 2 - 1], s[n // 2])), dd(med)))
    if k == "moda":
        v = R.choice(xs)
        xs = xs[:-2] + [v, v]
        R.shuffle(xs)
        cnt = {x: xs.count(x) for x in xs}
        mx = max(cnt.values())
        modes = [x for x in cnt if cnt[x] == mx]
        if len(modes) != 1:
            return None
        mo = modes[0]
        return M("Qual è la moda dei dati: %s?" % lista(xs), str(mo), W(str(mx), str(max(xs)) if max(xs) != mo else str(min(xs)), str(sorted(xs)[len(xs) // 2]) if sorted(xs)[len(xs) // 2] != mo else None, str(mo + 1), str(mo - 1), str(sorted(set(xs))[0]) if sorted(set(xs))[0] != mo else str(mo + 2)),
                 "Il dato che compare più volte (%d volte) è <b>%d</b>." % (mx, mo))
    return M("Calcola il campo di variazione dei dati: %s" % lista(xs), str(max(xs) - min(xs)), W(str(max(xs)), str(max(xs) + min(xs)), str(xs[-1] - xs[0]) if xs[-1] - xs[0] > 0 and xs[-1] - xs[0] != max(xs) - min(xs) else None, str(max(xs) - min(xs) + 1)),
             "Massimo %d, minimo %d: %d − %d = <b>%d</b>." % (max(xs), min(xs), max(xs), min(xs), max(xs) - min(xs)))


def s3_ponderata():
    vals = sorted(R.sample(range(4, 11), 3))
    fs = [R.randint(1, 9) for _ in vals]
    N = sum(fs)
    S = sum(v * f for v, f in zip(vals, fs))
    m = Fr(S, N)
    k = R.choice(["media", "media", "mediana", "freq"])
    tab = table(["Voto"] + [str(v) for v in vals], [["Numero di alunni"] + [str(f) for f in fs]])
    if k == "media":
        return M("In una verifica i voti sono stati:<br>%sQual è il voto medio (arrotonda ai centesimi se serve)?" % tab, dd(m), W(dd(Fr(sum(vals), 3)), dd(Fr(S, 3)) if S < 300 else None, dd(m + Fr(1, 2)), dd(Fr(S, N + 1))),
                 "Media ponderata: (%s) : %d = %d : %d = <b>%s</b>." % (" + ".join("%d × %d" % (v, f) for v, f in zip(vals, fs)), N, S, N, dd(m)))
    if k == "mediana":
        s = []
        for v, f in zip(vals, fs):
            s += [v] * f
        med = Fr(s[N // 2] + s[(N - 1) // 2], 2)
        return M("In una verifica i voti sono stati:<br>%sQual è il voto mediano?" % tab, dd(med), W(*[dd(v) for v in vals if v != med] + [dd(m) if m != med else None]),
                 "I voti sono %d; ordinati, %s <b>%s</b>." % (N, "il centrale (posto %d) è" % (N // 2 + 1) if N % 2 else "i centrali sono ai posti %d e %d:" % (N // 2, N // 2 + 1), dd(med)))
    i = R.randrange(3)
    fr_ = Fr(fs[i] * 100, N)
    return M("In una verifica i voti sono stati:<br>%sQual è la frequenza percentuale del voto %d (arrotonda all’unità)?" % (tab, vals[i]), "%s%%" % dk(fr_, 0), W("%d%%" % fs[i] if Fr(fs[i]) != fr_.__round__() else None, "%s%%" % dk(Fr(fs[i] * 100, sum(vals)), 0), "%s%%" % dk(100 - fr_, 0), "%s%%" % dk(fr_ + 5, 0)),
             "%d : %d × 100 ≈ <b>%s%%</b>." % (fs[i], N, dk(fr_, 0)))


def s4_inversa():
    n = R.randint(4, 7)
    m = R.randint(5, 9)
    xs = data(n - 1, 3, 10)
    target = m * n
    x = target - sum(xs)
    if not 1 <= x <= 10:
        return None
    p = K.next()
    return M("%s ha preso questi voti: %s. Quale voto deve prendere nella prossima verifica per avere la media %d?" % (p[0], lista(xs), m), str(x), W(str(m), str(m * (n - 1) - sum(xs)) if 0 < m * (n - 1) - sum(xs) <= 10 else None, str(x + 1) if x < 10 else str(x - 2), str(x - 1) if x > 1 else str(x + 2), str(x + 2) if x < 9 else str(x - 3), str(x - 2) if x > 2 else str(x + 3)),
             "Con %d voti la somma deve essere %d × %d = %d; ora è %d: %d − %d = <b>%d</b>." % (n, m, n, target, sum(xs), target, sum(xs), x))


def s5_classi():
    k = R.choice(["aero", "classi", "media_classi"])
    if k == "aero":
        N = R.choice([20, 30, 36, 40, 60, 72, 90, 120])
        f = R.randint(2, N - 1)
        g = Fr(360 * f, N)
        if g.denominator != 1:
            return None
        return M("In un’indagine su %d ragazzi, %d preferiscono il nuoto. Quanti gradi ha il settore del nuoto in un aerogramma?" % (N, f), "%d°" % g, W("%d°" % f, "%s°" % dd(Fr(100 * f, N)) if Fr(100 * f, N).denominator == 1 else None, "%d°" % (360 - g), "%d°" % (g // 2) if g % 2 == 0 else "%d°" % (g + 10)),
                 "%d : %d × 360° = <b>%d°</b>." % (f, N, g))
    if k == "classi":
        edges = [140, 150, 160, 170, 180]
        hs = [R.randint(140, 179) for _ in range(R.randint(10, 14))]
        i = R.randrange(4)
        f = sum(1 for h in hs if edges[i] <= h < edges[i + 1])
        return M("Le altezze (cm) di un gruppo di ragazzi sono: %s. Quanti ragazzi sono nella classe %d ⊢ %d (da %d compreso a %d escluso)?" % (lista(hs), edges[i], edges[i + 1], edges[i], edges[i + 1]), str(f), W(str(f + 1), str(f - 1) if f else "2", str(sum(1 for h in hs if edges[i] <= h <= edges[i + 1])) if sum(1 for h in hs if edges[i] <= h <= edges[i + 1]) != f else None, str(len(hs) - f), str(f + 2), str(f - 2) if f > 2 else str(f + 3)),
                 "Si contano i dati da %d a %d (escluso): <b>%d</b>." % (edges[i], edges[i + 1] - 1, f))
    cl = [(0, 10), (10, 20), (20, 30), (30, 40)]
    fs = [R.randint(1, 8) for _ in cl]
    N = sum(fs)
    S = sum((a + b) / 2 * f for (a, b), f in zip(cl, fs))
    m = Fr(int(S), N)
    tab = table(["Minuti di studio"] + ["%d ⊢ %d" % c for c in cl], [["Studenti"] + [str(f) for f in fs]])
    return M("Usando i valori centrali delle classi, calcola la media (arrotonda ai decimi):<br>%s" % tab, "≈ " + dk(m, 1) if (m * 10).denominator != 1 else dk(m, 1), W(("≈ " if (Fr(int(S), 4) * 10).denominator != 1 else "") + dk(Fr(int(S), 4), 1), ("≈ " if (Fr(sum(a * f for (a, b), f in zip(cl, fs)), N) * 10).denominator != 1 else "") + dk(Fr(sum(a * f for (a, b), f in zip(cl, fs)), N), 1), dk(Fr(N, 4), 1)),
             "Valori centrali 5, 15, 25, 35: (%s) : %d = %d : %d ≈ <b>%s</b>." % (" + ".join("%d × %d" % ((a + b) // 2, f) for (a, b), f in zip(cl, fs)), N, int(S), N, dk(m, 1)))


def main():
    seen = set()
    sets = [
        ("Indagini e caratteri", mix(R, seen, [(s1_concetti, 10), (s2_indici, 10)])),
        ("Media, mediana, moda, campo di variazione", mix(R, seen, [(s2_indici, 20)])),
        ("Tabelle di frequenza e media ponderata", mix(R, seen, [(s3_ponderata, 20)])),
        ("Problemi con la media", mix(R, seen, [(s4_inversa, 12), (s5_classi, 8)])),
        ("Classi e aerogrammi", mix(R, seen, [(s5_classi, 20)])),
    ]
    body = L(["Un’indagine statistica studia un <b>carattere</b> (qualitativo o quantitativo) su una <b>popolazione</b> o su un suo <b>campione</b>.",
              "<b>Frequenza assoluta</b>: quante volte compare un valore; <b>relativa</b>: frequenza assoluta : totale; <b>percentuale</b>: relativa × 100.",
              "<b>Media</b>: somma dei dati : numero dei dati. Con una tabella si usa la <b>media ponderata</b>: Σ(valore × frequenza) : Σ frequenze.",
              "<b>Mediana</b>: il dato centrale dopo averli ordinati (con un numero pari di dati, la media dei due centrali). <b>Moda</b>: il dato più frequente. <b>Campo di variazione</b>: massimo − minimo."],
             [("Dati: 4; 9; 6; 9; 7", ["ordinati: 4; 6; 7; 9; 9", "somma 35"], "media 7, mediana 7, moda 9, campo 5")],
             [["Calcolare la mediana senza ordinare", "Prima si ordinano i dati, poi si prende il centrale."],
              ["Media ponderata come media dei valori", "Ogni valore va moltiplicato per la sua frequenza."],
              ["Dividere per il numero di valori diversi", "Si divide per il numero totale dei dati (la somma delle frequenze)."]],
             table(["Indice", "Che cosa indica"], [["media", "il valore «medio» (risente dei valori estremi)"], ["mediana", "il dato centrale"], ["moda", "il dato più frequente"], ["campo di variazione", "quanto sono sparsi i dati"]]))
    faq = [("Quando è meglio usare la mediana invece della media?", "Quando ci sono valori molto diversi dagli altri: per esempio negli stipendi, pochi valori altissimi alzano molto la media ma non la mediana."),
           ("Che cos’è il valore centrale di una classe?", "La media degli estremi della classe: per la classe 10 ⊢ 20 è 15. Si usa per calcolare la media con dati raggruppati.")]
    unit(G, R, "statistica-e-indici-di-posizione", "D",
         "Rappresentare insiemi di dati; in situazioni significative, confrontare dati al fine di prendere decisioni, utilizzando le distribuzioni delle frequenze e delle frequenze relative; scegliere ed utilizzare valori medi (moda, mediana, media aritmetica) adeguati alla tipologia ed alle caratteristiche dei dati a disposizione; saper valutare la variabilità di un insieme di dati determinandone, ad esempio, il campo di variazione",
         "Statistica e indici di posizione", "Statistica",
         "Schede di matematica per la terza media sulla statistica: popolazione e campione, frequenze, media aritmetica e ponderata, mediana, moda, campo di variazione, classi e aerogrammi. 100 esercizi con soluzioni.",
         "Mediana: prima ordina i dati.", "Media ponderata: Σ(valore × frequenza) : Σ frequenze.",
         body, faq, sets, 13)


if __name__ == "__main__":
    main()
