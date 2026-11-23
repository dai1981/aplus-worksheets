# -*- coding: utf-8 -*-
"""
Italia Matematica quinta liceo: Continuità e asintoti (Relazioni e funzioni)
  python3 tools/gen_it_matematica_l5_continuita_e_asintoti.py
Funzioni continue, parametro che rende continua una funzione definita a tratti, punti di discontinuità
(prima, seconda, terza specie), teorema degli zeri (Bolzano), asintoti verticali, orizzontali e obliqui.
Errori: prendere come asintoto verticale uno zero che si semplifica, confondere salto e discontinuità eliminabile,
asintoto obliquo con q sbagliato.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, W, fq, nz, P2, FR, poly

R = random.Random(72505)
G = "quinta-liceo"


def xm(r):
    return "x − %s" % fq(r) if r > 0 else ("x + %s" % fq(-r) if r < 0 else "x")


def s1_param():
    x0 = R.choice([-2, -1, 1, 2, 3])
    a, b = nz(R, -4, 4), R.randint(-5, 5)
    k = a * x0 + b - x0 * x0
    left = poly([a, b])
    f = "f(x) = { %s se x &lt; %s; x² + k se x ≥ %s }" % (left, fq(x0), fq(x0))
    return M("Per quale valore di k la funzione %s è continua in x = %s?" % (f, fq(x0)), fq(k),
             [fq(v) for v in W(a * x0 + b, a * x0 + b + x0 * x0, -k, k + 1) if v != k],
             "Il limite sinistro vale %s; il valore in %s è %s + k. Impongo %s + k = %s: <b>k = %s</b>." % (fq(a * x0 + b), fq(x0), fq(x0 * x0), fq(x0 * x0), fq(a * x0 + b), fq(k)))


def s1_param2():
    x0 = R.randint(1, 3)
    m = R.randint(-3, 4)
    c = R.randint(-6, 6)
    # f = kx + m per x < x0 ; x² + c per x ≥ x0  → k x0 + m = x0² + c
    num = x0 * x0 + c - m
    k = Fr(num, x0)
    f = "f(x) = { kx %s se x &lt; %d; %s se x ≥ %d }" % (("+ %d" % m) if m >= 0 else ("− %d" % -m), x0, poly([1, 0, c]), x0)
    return M("Per quale valore di k la funzione %s è continua in x = %d?" % (f, x0), fq(k),
             [fq(v) for v in W(Fr(x0 * x0 + c + m, x0), num, Fr(x0 * x0 + c, x0), k + 1) if v != k],
             "Impongo che i due tratti coincidano in x = %d: %dk %s = %s, quindi <b>k = %s</b>." % (x0, x0, ("+ %d" % m) if m >= 0 else ("− %d" % -m), fq(x0 * x0 + c), fq(k)))


DISC = [
    ("(x² − {a2})/({xa})", "eliminabile (terza specie)", "Numeratore e denominatore si annullano insieme: semplificando il limite esiste ed è finito, ma f non è definita nel punto."),
    ("|{xa}|/({xa})", "prima specie (salto)", "Il limite destro vale 1 e il sinistro −1: sono finiti ma diversi, c’è un salto."),
    ("1/({xa})", "seconda specie", "Il limite è infinito: x = {a} è un asintoto verticale."),
    ("e<sup>1/({xa})</sup>", "seconda specie", "Da destra il limite è +∞: basta un limite infinito per la seconda specie."),
    ("sen({xa})/({xa})", "eliminabile (terza specie)", "Per il limite notevole il limite vale 1 ed è finito: si può eliminare la discontinuità ponendo f({a}) = 1."),
    ("1/({xa})²", "seconda specie", "Il limite è +∞ da entrambi i lati: seconda specie."),
    ("arctg(1/({xa}))", "prima specie (salto)", "Da destra il limite è π/2, da sinistra −π/2: limiti finiti e diversi, salto di ampiezza π."),
]
SPEC = ["prima specie (salto)", "seconda specie", "eliminabile (terza specie)", "la funzione è continua"]


def s2_disc():
    f, ans, why = R.choice(DISC)
    a = R.choice([-3, -2, -1, 1, 2, 3, 4])
    if "a2" in f:
        a = abs(a)
    xa = xm(a)
    ff = f.format(xa=xa, a2=a * a, a=fq(a))
    return M("Che tipo di discontinuità ha f(x) = %s in x = %s?" % (ff, fq(a)), ans, [s for s in SPEC if s != ans],
             why.format(a=fq(a)) + " <b>%s</b>." % ans.capitalize())


def s2_salto():
    x0 = R.randint(-2, 3)
    a, b = nz(R, -3, 3), R.randint(-4, 4)
    c = R.randint(-4, 4)
    l1 = a * x0 + b
    l2 = x0 * x0 + c
    if l1 == l2:
        return None
    s = abs(l1 - l2)
    return M("f(x) = { %s se x &lt; %s; %s se x ≥ %s }. Quanto è ampio il salto in x = %s?" % (poly([a, b]), fq(x0), poly([1, 0, c]), fq(x0), fq(x0)),
             fq(s), [fq(v) for v in W(abs(l1 + l2), abs(l1), abs(l2), s + 1, s + 2, s * 2) if v != s][:3],
             "Limite sinistro %s, limite destro %s: il salto è |%s − %s| = <b>%s</b>." % (fq(l1), fq(l2), fq(l2), fq(l1) if l1 >= 0 else "(%s)" % fq(l1), fq(s)))


def s3_zeri():
    while True:
        p, q = R.randint(-6, 6), R.randint(-9, 9)
        f = lambda x: x ** 3 + p * x + q
        iv = [(-3, -2), (-2, -1), (-1, 0), (0, 1), (1, 2), (2, 3)]
        good = [i for i in iv if f(i[0]) * f(i[1]) < 0]
        if len(good) == 1 and all(f(x) != 0 for x in range(-3, 4)):
            break
    g = good[0]
    opts = [i for i in iv if i != g]
    R.shuffle(opts)
    st = lambda i: "[%s; %s]" % (fq(i[0]), fq(i[1]))
    return M("Per il teorema degli zeri, in quale intervallo f(x) = %s ha sicuramente uno zero?" % poly([1, 0, p, q]), st(g), [st(i) for i in opts[:3]],
             "f(%s) = %s e f(%s) = %s hanno segni opposti e f è continua: c’è uno zero in <b>%s</b>." % (fq(g[0]), fq(f(g[0])), fq(g[1]), fq(f(g[1])), st(g)))


def s3_teo():
    T = [("f è continua in [a; b] e f(a) · f(b) &lt; 0. Che cosa si può concludere?", "f ha almeno uno zero in (a; b)", ["f ha esattamente uno zero in (a; b)", "f non ha zeri in (a; b)", "f è crescente in [a; b]"],
          "È il teorema degli zeri (Bolzano): garantisce <b>almeno</b> uno zero, non uno solo."),
         ("Per il teorema di Weierstrass, una funzione continua in un intervallo chiuso e limitato [a; b]…", "ha massimo e minimo assoluti", ["è derivabile", "è monotona", "ha almeno uno zero"],
          "Weierstrass: f continua in [a; b] <b>ha massimo e minimo assoluti</b>."),
         ("f è continua in [a; b], f(a) = 2 e f(b) = 8. Per il teorema dei valori intermedi, f assume sicuramente il valore…", "5", ["10", "0", "−2"],
          "f assume tutti i valori compresi tra 2 e 8: quindi <b>5</b>."),
         ("f(x) = 1/x in (0; 1]. Perché non ha massimo?", "l’intervallo non è chiuso", ["f non è continua in (0; 1]", "f è crescente", "f ha uno zero"],
          "f è continua in (0; 1] ma l’intervallo non è chiuso: Weierstrass non si applica, f cresce senza limite vicino a 0. <b>L’intervallo non è chiuso</b>."),
         ("f è continua in [0; 4], f(0) = −3 e f(4) = 5. Quale valore assume sicuramente f in (0; 4)?", "0", ["6", "−4", "10"],
          "Per i valori intermedi f assume ogni valore tra −3 e 5, quindi anche <b>0</b>."),
         ("La funzione f(x) = x² − 4 è continua in x = 2?", "sì, è un polinomio", ["no, perché f(2) = 0", "no, perché ha uno zero", "solo da destra"],
          "I polinomi sono continui in tutto ℝ: <b>sì, è un polinomio</b>.")]
    q, a, w, e = R.choice(T)
    return M(q, a, w, e)


def s4_vert():
    a, b = R.sample([-4, -3, -2, -1, 1, 2, 3, 5], 2)
    a, b = sorted([a, b])
    if R.random() < 0.5:
        c = R.choice([v for v in range(-5, 6) if v not in (a, b)])
        f = FR(xm(c), "(%s)(%s)" % (xm(a), xm(b)))
        ans = "x = %s e x = %s" % (fq(a), fq(b))
        wr = ["x = %s e x = %s" % (fq(-b), fq(-a)) if (-b, -a) != (a, b) else "nessun asintoto verticale", "x = %s" % fq(c), "solo x = %s" % fq(a)]
        e = "Il denominatore si annulla in %s e %s e il numeratore no: <b>%s</b>." % (fq(a), fq(b), ans)
    else:
        f = FR(xm(a), "(%s)(%s)" % (xm(a), xm(b)))
        ans = "solo x = %s" % fq(b)
        wr = ["x = %s e x = %s" % (fq(a), fq(b)), "solo x = %s" % fq(a), "x = %s" % fq(-b)]
        e = "x − %s si semplifica: in x = %s c’è una discontinuità eliminabile, non un asintoto. Resta <b>%s</b>." % (fq(a), fq(a), ans) if a > 0 else \
            "x + %s si semplifica: in x = %s c’è una discontinuità eliminabile, non un asintoto. Resta <b>%s</b>." % (fq(-a), fq(a), ans)
    return M("Quali sono gli asintoti verticali di f(x) = %s?" % f, ans, wr, e)


def s4_oriz():
    n1, n2 = R.choice([(1, 1), (2, 2), (1, 2), (2, 1), (3, 3), (0, 1), (3, 2)])
    a, c = nz(R, -6, 6), nz(R, -5, 5)
    nc = [a] + [R.randint(-5, 5) for _ in range(n1)]
    dc = [c] + [R.randint(-5, 5) for _ in range(n2 - 1)] + [nz(R, -5, 5)] if n2 else [c]
    if n1 == n2 and all(Fr(x, a) == Fr(y, c) for x, y in zip(nc, dc)):
        return None
    num, den = poly(nc), poly(dc)
    f = FR(num, den)
    if n1 < n2:
        ans = "y = 0"
        e = "Il grado del numeratore è minore di quello del denominatore: <b>y = 0</b>."
    elif n1 == n2:
        ans = "y = %s" % fq(Fr(a, c))
        e = "Stesso grado: rapporto dei coefficienti direttivi %s/%s, <b>%s</b>." % (fq(a), fq(c), ans)
    else:
        ans = "non c’è asintoto orizzontale"
        e = "Il grado del numeratore è maggiore: f → ∞, quindi <b>non c’è asintoto orizzontale</b>%s." % (" (c’è un asintoto obliquo)" if n1 == n2 + 1 else "")
    wr = W("y = %s" % fq(Fr(a, c)), "y = 0", "y = %s" % fq(Fr(c, a)), "y = %s" % fq(a), "non c’è asintoto orizzontale")
    return M("Qual è l’asintoto orizzontale di f(x) = %s?" % f, ans, [w for w in wr if w != ans], e)


def s5_obl():
    a = nz(R, -3, 3)
    b, c = R.randint(-6, 6), R.randint(-6, 6)
    d = nz(R, -4, 4)
    m, q = a, b - a * d
    if c - d * q == 0:  # numeratore divisibile: retta con buco, non asintoto
        return None
    num = P2(a, b, c)
    f = FR(num, xm(-d) if d else "x")
    yq = lambda mm, qq: "y = %s" % poly([mm, qq])
    ans = yq(m, q)
    return M("Qual è l’asintoto obliquo di f(x) = %s?" % f, ans, [yq(*v) for v in W((m, b), (m, b + a * d), (m, -q), (m, c), (-m, q), (m, q + d)) if v != (m, q) and v[0] != 0][:3],
             "m = lim f(x)/x = %s; q = lim (f(x) − (%s)) = %s − (%s)(%s) = %s. <b>%s</b>." % (fq(m), poly([m, 0]).strip(), fq(b), fq(a), fq(d), fq(q), ans))


def s5_tipo():
    T = [("f(x) = (2x² + 1)/(x − 3)", "un asintoto verticale e uno obliquo", "Grado 2 su grado 1: x = 3 verticale e un obliquo y = 2x + 6."),
         ("f(x) = (3x + 1)/(x − 2)", "un asintoto verticale e uno orizzontale", "Stesso grado: y = 3 orizzontale; x = 2 verticale."),
         ("f(x) = 1/(x² + 1)", "solo un asintoto orizzontale", "Il denominatore non si annulla mai: solo y = 0."),
         ("f(x) = x³/(x² − 1)", "due asintoti verticali e uno obliquo", "x = ±1 verticali; grado 3 su 2: obliquo y = x."),
         ("f(x) = (x² − 4)/(x − 2)", "nessun asintoto", "Si semplifica: f(x) = x + 2 per x ≠ 2, una retta con un punto escluso."),
         ("f(x) = eˣ", "solo un asintoto orizzontale", "eˣ → 0 per x → −∞: y = 0; nessun asintoto verticale."),
         ("f(x) = ln x", "solo un asintoto verticale", "ln x → −∞ per x → 0⁺: x = 0; per x → +∞ cresce senza limite, senza asintoti."),
         ("f(x) = (x² + 1)/(x² − 9)", "due asintoti verticali e uno orizzontale", "x = ±3 verticali; stesso grado: y = 1.")]
    f, a, e = R.choice(T)
    opts = ["un asintoto verticale e uno obliquo", "un asintoto verticale e uno orizzontale", "solo un asintoto orizzontale", "due asintoti verticali e uno obliquo",
            "nessun asintoto", "solo un asintoto verticale", "due asintoti verticali e uno orizzontale"]
    w = [o for o in opts if o != a]
    R.shuffle(w)
    return M("Quali asintoti ha %s?" % f, a, w[:3], e + " <b>%s</b>." % a.capitalize())


def main():
    seen = set()
    sets = [
        ("Funzioni continue e parametri", mix(R, seen, [(s1_param, 12), (s1_param2, 8)])),
        ("Punti di discontinuità", mix(R, seen, [(s2_disc, 12), (s2_salto, 8)])),
        ("Teoremi sulle funzioni continue", mix(R, seen, [(s3_zeri, 14), (s3_teo, 6)])),
        ("Asintoti verticali e orizzontali", mix(R, seen, [(s4_vert, 10), (s4_oriz, 10)])),
        ("Asintoti obliqui e riepilogo", mix(R, seen, [(s5_obl, 12), (s5_tipo, 8)])),
    ]
    body = L(["f è <b>continua</b> in x<sub>0</sub> se lim<sub>x→x<sub>0</sub></sub> f(x) = f(x<sub>0</sub>). Per una funzione a tratti si impone che i due tratti abbiano lo stesso valore nel punto di raccordo.",
              "Discontinuità: di <b>prima specie</b> (limiti destro e sinistro finiti ma diversi: salto), di <b>seconda specie</b> (almeno un limite infinito o inesistente), <b>eliminabile</b> o di terza specie (il limite esiste finito ma è diverso da f(x<sub>0</sub>) o f non è definita).",
              "Teoremi: <b>degli zeri</b> (f continua in [a; b] con f(a) · f(b) &lt; 0 ha almeno uno zero), <b>di Weierstrass</b> (massimo e minimo in [a; b]), <b>dei valori intermedi</b>.",
              "Asintoti: <b>verticale</b> x = a se f → ∞ per x → a; <b>orizzontale</b> y = ℓ se f → ℓ per x → ±∞; <b>obliquo</b> y = mx + q con m = lim f(x)/x e q = lim (f(x) − mx)."],
             [("Asintoti di (x² + 1)/(x − 1)", ["x = 1 verticale", "m = 1, q = lim (x + 1)/(x − 1) = 1"], "y = x + 1"),
              ("f(x) = (x² − 1)/(x − 1) in x = 1", ["Si semplifica: x + 1 → 2"], "discontinuità eliminabile")],
             [["Prendere ogni zero del denominatore come asintoto", "Prima semplifica: se il fattore si cancella è una discontinuità eliminabile."],
              ["Pensare che il teorema degli zeri dia un solo zero", "Garantisce almeno uno zero, non uno solo."],
              ["Calcolare q come il termine noto del numeratore", "q = lim (f(x) − mx): si fa la divisione tra polinomi."]])
    faq = [("Una funzione può attraversare il suo asintoto orizzontale?", "Sì: l’asintoto orizzontale descrive il comportamento per x → ±∞, non vieta al grafico di intersecare la retta per valori finiti di x."),
           ("Quando c’è un asintoto obliquo in una funzione razionale?", "Quando il grado del numeratore supera di uno il grado del denominatore. Allora la retta si trova con la divisione tra polinomi (quoziente).")]
    unit(G, R, "continuita-e-asintoti", "F",
         "Continuità di una funzione, teoremi sulle funzioni continue, classificazione delle discontinuità e ricerca degli asintoti",
         "Continuità e asintoti", "Continuità e asintoti",
         "Schede di matematica per la quinta liceo su continuità e asintoti: funzioni continue a tratti, punti di discontinuità di prima, seconda e terza specie, teorema degli zeri e di Weierstrass, asintoti verticali, orizzontali e obliqui. 100 esercizi con soluzioni.",
         "Asintoto obliquo: m = lim f(x)/x, q = lim (f(x) − mx).", "Prima di cercare gli asintoti verticali semplifica la funzione.",
         body, faq, sets, 5)


if __name__ == "__main__":
    main()
