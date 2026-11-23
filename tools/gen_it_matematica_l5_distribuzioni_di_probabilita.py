# -*- coding: utf-8 -*-
"""
Italia Matematica quinta liceo: Distribuzioni di probabilità (Dati e previsioni)
  python3 tools/gen_it_matematica_l5_distribuzioni_di_probabilita.py
Variabili aleatorie discrete, valore atteso, varianza e deviazione standard, giochi equi, distribuzione binomiale
(probabilità, media, varianza), distribuzione di Poisson, distribuzione normale (standardizzazione, regola 68–95–99,7).
Errori: dimenticare il coefficiente binomiale, Var = E(X²) senza sottrarre E(X)², confondere σ e σ².
"""
import random
from math import comb
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, W, fq, FR, table

R = random.Random(72513)
G = "quinta-liceo"


def dist():
    n = R.randint(3, 4)
    xs = sorted(R.sample(range(-2, 7), n))
    den = R.choice([10, 8, 12, 6])
    while True:
        ps = [R.randint(1, den - n + 1) for _ in range(n)]
        if sum(ps) == den:
            break
    return xs, [Fr(p, den) for p in ps]


def tab(xs, ps, hide=None):
    return table(["x<sub>i</sub>"] + [fq(x) for x in xs], [["p<sub>i</sub>"] + ["p" if i == hide else fq(p) for i, p in enumerate(ps)]])


def s1_E():
    xs, ps = dist()
    E = sum(x * p for x, p in zip(xs, ps))
    return M("%sLa variabile aleatoria X ha la distribuzione della tabella. Calcola il valore atteso E(X)." % tab(xs, ps), fq(E),
             [fq(v) for v in W(Fr(sum(xs), len(xs)), sum(xs), E + Fr(1, 2), -E, sum(x * x * p for x, p in zip(xs, ps))) if v != E][:3],
             "E(X) = Σ x<sub>i</sub> p<sub>i</sub> = %s = <b>%s</b>." % (" + ".join("%s · %s" % ("(%s)" % fq(x) if x < 0 else fq(x), fq(p)) for x, p in zip(xs, ps)), fq(E)))


def s1_p():
    xs, ps = dist()
    i = R.randrange(len(xs))
    p = ps[i]
    return M("%sNella distribuzione di probabilità della tabella manca un valore. Quanto vale p?" % tab(xs, ps, i), fq(p),
             [fq(v) for v in W(1 - p, p + Fr(1, 10), Fr(1, len(xs)), p / 2) if v != p and 0 < v < 1][:3],
             "La somma delle probabilità è 1: p = 1 − %s = <b>%s</b>." % (fq(1 - p), fq(p)))


def s2_var():
    xs, ps = dist()
    E = sum(x * p for x, p in zip(xs, ps))
    E2 = sum(x * x * p for x, p in zip(xs, ps))
    V = E2 - E * E
    return M("%sCalcola la varianza Var(X) della variabile aleatoria della tabella." % tab(xs, ps), fq(V),
             [fq(v) for v in W(E2, E * E, V + E, E2 + E * E, V + 1, 2 * V) if v != V][:3],
             "E(X) = %s, E(X²) = %s; Var(X) = E(X²) − E(X)² = %s − %s = <b>%s</b>." % (fq(E), fq(E2), fq(E2), fq(E * E), fq(V)))


def s2_gioco():
    T = R.choice(["dado", "moneta", "urna"])
    if T == "dado":
        v = R.choice([6, 12, 18, 30])
        c = R.choice([1, 2, 3, 4, 5])
        g = Fr(v, 6) - c
        q = "Si paga %d € per lanciare un dado: se esce 6 si vincono %d €, altrimenti niente. Qual è il guadagno atteso?" % (c, v)
        e = "E = %d · 1/6 − %d = %s €" % (v, c, fq(g))
    elif T == "moneta":
        v = R.choice([2, 4, 6, 10])
        c = R.choice([1, 2, 3, 4, 5])
        g = Fr(v, 4) - c
        q = "Si pagano %d € per lanciare due monete: se escono due teste si vincono %d €. Qual è il guadagno atteso?" % (c, v)
        e = "P(TT) = 1/4; E = %d · 1/4 − %d = %s €" % (v, c, fq(g))
    else:
        r, b = R.randint(1, 4), R.randint(2, 6)
        v = R.choice([5, 10, 20])
        c = R.choice([1, 2, 3, 4])
        g = Fr(v * r, r + b) - c
        q = "Un’urna contiene %d palline rosse e %d bianche. Si pagano %d € per estrarne una: se è rossa si vincono %d €. Qual è il guadagno atteso?" % (r, b, c, v)
        e = "P(rossa) = %d/%d; E = %d · %d/%d − %d = %s €" % (r, r + b, v, r, r + b, c, fq(g))
    ans = "%s €" % fq(g)
    eq = " (il gioco è equo)" if g == 0 else (" (sfavorevole al giocatore)" if g < 0 else " (favorevole al giocatore)")
    return M(q, ans, ["%s €" % fq(x) for x in W(-g, g + c, g - 1, g + 1, g + Fr(1, 2), g - Fr(1, 2)) if x != g][:3], e + eq + ": <b>%s</b>." % ans)


PS = [Fr(1, 2), Fr(1, 3), Fr(1, 6), Fr(1, 4), Fr(1, 5), Fr(2, 3)]


def s3_bin():
    n = R.randint(3, 6)
    p = R.choice(PS)
    k = R.randint(0, n)
    v = comb(n, k) * p ** k * (1 - p) ** (n - k)
    ctx = {Fr(1, 2): "lanci di una moneta (X = numero di teste)", Fr(1, 6): "lanci di un dado (X = numero di volte che esce 6)", Fr(1, 3): "prove con probabilità di successo 1/3",
           Fr(1, 4): "risposte a caso a domande con 4 opzioni (X = risposte esatte)", Fr(1, 5): "prove con probabilità di successo 1/5", Fr(2, 3): "prove con probabilità di successo 2/3"}[p]
    return M("X è binomiale: %d %s. Calcola P(X = %d)." % (n, ctx, k), fq(v),
             [fq(x) for x in W(p ** k * (1 - p) ** (n - k), comb(n, k) * p ** k, Fr(k, n) if k else None, comb(n, k) * p ** (n - k) * (1 - p) ** k, p ** k if k else (1 - p), 1 - v, p ** (k + 1) * (1 - p) ** (n - k)) if x != v and 0 < x < 1][:3],
             "P(X = k) = C(n, k) p<sup>k</sup> (1 − p)<sup>n − k</sup> = %d · (%s)<sup>%d</sup> · (%s)<sup>%d</sup> = <b>%s</b>." % (comb(n, k), fq(p), k, fq(1 - p), n - k, fq(v)))


def s3_binm():
    n = R.choice([10, 12, 20, 30, 36, 50, 60, 100])
    p = R.choice(PS)
    if (n * p).denominator != 1:
        return None
    ask = R.choice(["E", "V"])
    if ask == "E":
        v = n * p
        return M("X è binomiale con n = %d e p = %s. Quanto vale il valore atteso E(X)?" % (n, fq(p)), fq(v), [fq(x) for x in W(n * (1 - p), n * p * (1 - p), v + 1, Fr(n, 2), 2 * v, v - 1, n) if x != v][:3],
                 "E(X) = np = %d · %s = <b>%s</b>." % (n, fq(p), fq(v)))
    v = n * p * (1 - p)
    return M("X è binomiale con n = %d e p = %s. Quanto vale la varianza Var(X)?" % (n, fq(p)), fq(v), [fq(x) for x in W(n * p, n * (1 - p), n * p * p, v * 2, v + 1, v - 1) if x != v][:3],
             "Var(X) = np(1 − p) = %d · %s · %s = <b>%s</b>." % (n, fq(p), fq(1 - p), fq(v)))


def pform(a, ex, f):
    num = ("%d " % a if a != 1 else "") + "e<sup>%s</sup>" % fq(ex)
    return FR(num, str(f)) if f > 1 else num


def s4_pois():
    from math import factorial
    lam = R.randint(1, 6)
    k = R.randint(0, 4)
    ask = R.choice(["p", "p", "E"])
    if ask == "E":
        return M("Il numero di clienti che arrivano in un minuto segue una distribuzione di Poisson con λ = %d. Quanti clienti si aspettano in media al minuto?" % lam, str(lam),
                 [str(x) for x in W(lam * lam, lam + 1, lam + 2, 2 * lam, lam + 3) if x != lam][:3], "Per Poisson E(X) = Var(X) = λ: <b>%d</b>." % lam)
    f = factorial(k)
    ans = pform(lam ** k, -lam, f)
    w = [x for x in W(pform(lam ** k, -k, f) if k != lam else None, pform(lam ** k, -lam, 1) if f > 1 else None, pform(lam * k, -lam, f) if lam * k != lam ** k else None,
                      pform(lam ** k, lam, f), pform(k ** lam, -lam, f) if k ** lam != lam ** k else None) if x != ans][:3]
    return M("X segue una distribuzione di Poisson con λ = %d. Calcola P(X = %d)." % (lam, k), ans, w,
             "P(X = k) = λ<sup>k</sup> e<sup>−λ</sup>/k! = %d<sup>%d</sup> e<sup>−%d</sup>/%d!: <b>%s</b>." % (lam, k, lam, k, ans))


def s5_norm():
    mu = R.choice([50, 100, 170, 60, 500, 20, 75])
    s = R.choice([2, 4, 5, 10, 8, 3])
    k = R.choice([1, 2, 3])
    ask = R.choice(["dentro", "sopra", "z"])
    pin = {1: "68%", 2: "95%", 3: "99,7%"}
    pout = {1: "16%", 2: "2,5%", 3: "0,15%"}
    if ask == "dentro":
        return M("X è normale con media μ = %d e deviazione standard σ = %d. Circa quale percentuale dei valori sta tra %d e %d?" % (mu, s, mu - k * s, mu + k * s), pin[k],
                 [v for v in ["68%", "95%", "99,7%", "50%"] if v != pin[k]][:3], "L’intervallo è μ ± %dσ: per la regola empirica circa <b>%s</b>." % (k, pin[k]))
    if ask == "sopra":
        return M("X è normale con μ = %d e σ = %d. Circa quale percentuale dei valori supera %d?" % (mu, s, mu + k * s), pout[k],
                 [v for v in W(pin[k], {1: "32%", 2: "5%", 3: "0,3%"}[k], "50%", pout[(k % 3) + 1]) if v != pout[k]][:3],
                 "Fuori da μ ± %dσ c’è circa %s dei valori, metà per parte: <b>%s</b>." % (k, {1: "il 32%", 2: "il 5%", 3: "lo 0,3%"}[k], pout[k]))
    x = mu + R.choice([-2, -1, 1, 2, 3]) * s + R.choice([0, 0, s // 2])
    z = Fr(x - mu, s)
    return M("X è normale con μ = %d e σ = %d. Qual è il valore standardizzato z di x = %d?" % (mu, s, x), fq(z),
             [fq(v) for v in W(-z, Fr(x - mu), Fr(x - mu, s * s), Fr(x, s)) if v != z][:3],
             "z = (x − μ)/σ = (%d − %d)/%d = <b>%s</b>." % (x, mu, s, fq(z)))


def main():
    seen = set()
    sets = [
        ("Variabili aleatorie e valore atteso", mix(R, seen, [(s1_E, 12), (s1_p, 8)])),
        ("Varianza e giochi equi", mix(R, seen, [(s2_var, 10), (s2_gioco, 10)])),
        ("Distribuzione binomiale", mix(R, seen, [(s3_bin, 12), (s3_binm, 8)])),
        ("Distribuzione di Poisson", mix(R, seen, [(s4_pois, 12), (s3_binm, 8)])),
        ("Distribuzione normale", mix(R, seen, [(s5_norm, 20)])),
    ]
    body = L(["Una <b>variabile aleatoria discreta</b> X assume valori x<sub>i</sub> con probabilità p<sub>i</sub> (Σ p<sub>i</sub> = 1). Valore atteso: E(X) = Σ x<sub>i</sub> p<sub>i</sub>; varianza: Var(X) = E(X²) − E(X)²; deviazione standard σ = √Var(X).",
              "Un gioco è <b>equo</b> se il guadagno atteso è 0.",
              "<b>Binomiale</b> (n prove indipendenti, probabilità di successo p): P(X = k) = C(n, k) p<sup>k</sup>(1 − p)<sup>n − k</sup>, E(X) = np, Var(X) = np(1 − p). <b>Poisson</b> (eventi rari): P(X = k) = λ<sup>k</sup>e<sup>−λ</sup>/k!, E(X) = Var(X) = λ.",
              "<b>Normale</b> di media μ e deviazione standard σ: z = (x − μ)/σ. Regola empirica: circa il 68% dei valori in μ ± σ, il 95% in μ ± 2σ, il 99,7% in μ ± 3σ."],
             [("Binomiale n = 4, p = 1/2, P(X = 2)", ["C(4, 2) = 6", "6 · (1/2)<sup>4</sup>"], "3/8"),
              ("Normale μ = 100, σ = 10: P(X &gt; 120)", ["120 = μ + 2σ", "(100% − 95%)/2"], "circa 2,5%")],
             [["Dimenticare C(n, k)", "P(X = k) conta tutti i modi di ottenere k successi."],
              ["Var(X) = E(X²)", "Bisogna sottrarre E(X)²."],
              ["Confondere σ e σ²", "σ è la deviazione standard, σ² la varianza."]])
    faq = [("Quando si usa la distribuzione binomiale?", "Quando si ripete n volte una prova con due esiti (successo o insuccesso), le prove sono indipendenti e la probabilità di successo p è sempre la stessa."),
           ("Che cosa rappresenta la distribuzione normale?", "Descrive grandezze che si distribuiscono a campana intorno alla media, come le altezze o gli errori di misura; è simmetrica rispetto a μ.")]
    unit(G, R, "distribuzioni-di-probabilita", "Q",
         "Distribuzioni di probabilità discrete e continue: binomiale, di Poisson, normale; valore atteso e varianza",
         "Distribuzioni di probabilità", "Distribuzioni di probabilità",
         "Schede di matematica per la quinta liceo sulle distribuzioni di probabilità: variabili aleatorie discrete, valore atteso, varianza, giochi equi, distribuzione binomiale, distribuzione di Poisson, distribuzione normale e regola empirica. 100 esercizi con soluzioni.",
         "Binomiale: E(X) = np, Var(X) = np(1 − p).", "Normale: 68% in μ ± σ, 95% in μ ± 2σ.",
         body, faq, sets, 13)


if __name__ == "__main__":
    main()
