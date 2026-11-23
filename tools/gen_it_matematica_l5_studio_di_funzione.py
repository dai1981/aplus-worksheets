# -*- coding: utf-8 -*-
"""
Italia Matematica quinta liceo: Studio di funzione (Relazioni e funzioni)
  python3 tools/gen_it_matematica_l5_studio_di_funzione.py
Schema dello studio di funzione: simmetrie (pari, dispari), intersezioni con gli assi, asintoti, punti stazionari
di funzioni razionali, esponenziali e logaritmiche, lettura del grafico, grafico di f′ e di f.
Errori: confondere pari e dispari, non controllare il dominio, cercare punti stazionari fuori dal dominio.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, W, fq, nz, FR, poly, kurve, relabel

R = random.Random(72509)
G = "quinta-liceo"
BLUE = "#1f6fd1"


def pt(x, y):
    return "(%s; %s)" % (fq(x), fq(y))


SIM = [("x<sup>4</sup> − {a}x²", "pari"), ("x³ − {a}x", "dispari"), ("x³ + {a}", "né pari né dispari"), (FR("x", "x² + {a}"), "dispari"),
       (FR("x²", "x² − {a}"), "pari"), ("e<sup>−x²</sup>", "pari"), ("x e<sup>x</sup>", "né pari né dispari"), ("sen x + x", "dispari"),
       ("x² cos x", "pari"), ("|x| − {a}", "pari"), ("x² + {a}x", "né pari né dispari"), (FR("x² + {a}", "x"), "dispari"),
       ("ln(x² + {a})", "pari"), (FR("{a}", "x − 1"), "né pari né dispari"), ("x<sup>5</sup> − {a}x³", "dispari"), ("x sen x", "pari")]


def s1_sim():
    f, a = R.choice(SIM)
    if "{a}" in f:
        f = f.format(a=R.randint(2, 9))
    elif R.random() < 0.7:
        return None
    why = {"pari": "f(−x) = f(x): il grafico è simmetrico rispetto all’asse y.", "dispari": "f(−x) = −f(x): il grafico è simmetrico rispetto all’origine.",
           "né pari né dispari": "f(−x) non è uguale né a f(x) né a −f(x)."}[a]
    return M("La funzione f(x) = %s è…" % f, a, [x for x in ["pari", "dispari", "né pari né dispari", "sia pari sia dispari"] if x != a], why + " <b>%s</b>." % a.capitalize())


def s2_int():
    a, b = R.sample([-4, -3, -2, -1, 1, 2, 3, 5], 2)
    k = R.choice([1, 2, -1, 3])
    xm = lambda r: "x − %d" % r if r > 0 else "x + %d" % -r
    f = FR(xm(a) if k == 1 else "%s(%s)" % (fq(k) if k != -1 else "−", xm(a)), xm(b))
    y0 = Fr(-k * a, -b)
    ask = R.choice(["x", "y"])
    if ask == "x":
        return M("In quale punto il grafico di f(x) = %s interseca l’asse x?" % f, pt(a, 0), [pt(*p) for p in W((b, 0), (0, y0), (-a, 0), (k, 0), (0, a), (-b, 0)) if p != (a, 0)][:3],
                 "f(x) = 0 quando il numeratore è nullo e x ≠ %s: x = %s, <b>%s</b>." % (fq(b), fq(a), pt(a, 0)))
    return M("In quale punto il grafico di f(x) = %s interseca l’asse y?" % f, pt(0, y0), [pt(*p) for p in W((0, Fr(b, a)), (y0, 0), (0, -y0), (0, k)) if p != (0, y0)][:3],
             "Pongo x = 0: f(0) = %s(%s)/(%s) = <b>%s</b>." % (fq(k), fq(-a), fq(-b), pt(0, y0)))


def s3_esp():
    k = R.choice([1, 2, 3, -1, -2, -3, 4, -4])
    kind = R.choice(["xe", "x2e", "xln", "eminus", "x2ln", "lnx"])
    if kind == "xe":
        x0 = Fr(-1) / k
        f = "x e<sup>%s</sup>" % poly([k, 0]) if k != 1 else "x e<sup>x</sup>"
        e = "f′(x) = e<sup>%s</sup>(%s) = 0 per x = %s." % (poly([k, 0]), poly([k, 1]), fq(x0))
        t = "minimo" if k > 0 else "massimo"
        w = W(-x0, Fr(k), Fr(1, 1) / k if k != -1 else 2, 0, x0 + 2, x0 - 2)
    elif kind == "x2e":
        x0 = Fr(-2) / k
        f = "x² e<sup>%s</sup>" % poly([k, 0]) if k != 1 else "x² e<sup>x</sup>"
        e = "f′(x) = x e<sup>%s</sup>(%s): si annulla in 0 (minimo) e in x = %s." % (poly([k, 0]), poly([k, 2]), fq(x0))
        t = "massimo"
        w = W(-x0, Fr(0), Fr(-1) / k, Fr(2) * k)
    elif kind == "xln":
        if k < 0:
            return None
        # f = x − k ln x  →  f′ = 1 − k/x  → x = k (minimo)
        x0 = Fr(k)
        f = "x − %sln x" % ("%s " % fq(k) if k != 1 else "")
        e = "Dominio x &gt; 0; f′(x) = 1 − %s/x = 0 per x = %s; f′ passa da − a +." % (fq(k), fq(x0))
        t = "minimo"
        w = W(Fr(1, 1) / k if k != 1 else 2, -x0, Fr(0) + (k + 1), Fr(1) if k != 1 else 3)
    elif kind == "eminus":
        if k <= 0:
            return None
        # f = eˣ − kx → x = ln k
        f = "e<sup>x</sup> − %sx" % (fq(k) if k != 1 else "")
        ans = "x = ln %s" % fq(k) if k != 1 else "x = 0"
        e = "f′(x) = eˣ − %s = 0 per %s; f′ passa da − a +." % (fq(k), ans)
        wr = ["x = %s" % fq(k), "x = e<sup>%s</sup>" % fq(k), "x = −ln %s" % fq(k)] if k != 1 else ["x = 1", "x = e", "x = −1"]
        return M("Dove ha un minimo la funzione f(x) = %s?" % f, ans, wr, e + " <b>%s</b>." % ans)
    elif kind == "x2ln":
        m = R.randint(1, 4)
        kk = 2 * m * m
        f = "x² − %d ln x" % kk
        x0 = Fr(m)
        e = "Dominio x &gt; 0; f′(x) = 2x − %d/x = 0 per x² = %d, x = %s (la radice negativa è fuori dal dominio)." % (kk, m * m, fq(m))
        t = "minimo"
        w = W(-x0, Fr(kk), Fr(m * m), Fr(kk, 2) + 1, Fr(m + 1), Fr(2 * m + 1))
    else:
        if k not in (1, 2, 3):
            return None
        # f = ln x / x^k → f′ = (1 − k ln x)/x^(k+1) → x = e^(1/k)
        f = FR("ln x", "x" if k == 1 else "x<sup>%d</sup>" % k)
        ans = "x = e" if k == 1 else "x = e<sup>1/%d</sup>" % k
        e = "f′(x) = (1 − %sln x)/%s = 0 per ln x = %s." % ("%d " % k if k > 1 else "", "x²" if k == 1 else "x<sup>%d</sup>" % (k + 1), "1" if k == 1 else "1/%d" % k)
        return M("Dove ha un massimo la funzione f(x) = %s?" % f, ans, ["x = 1", "x = e<sup>%d</sup>" % k if k > 1 else "x = e²", "x = 0"], e + " <b>%s</b>." % ans)
    ans = "x = %s" % fq(x0)
    return M("Dove ha un %s relativo la funzione f(x) = %s?" % (t, f), ans, ["x = %s" % fq(v) for v in w if v != x0][:3], e + " <b>%s</b>." % ans)


def s4_raz():
    k = R.randint(1, 6)
    ask = R.choice(["staz", "val", "asin", "dom"])
    f = "x + %s" % FR(str(k * k), "x")
    if ask == "staz":
        return M("f(x) = %s. Quali sono i punti stazionari?" % f, "x = ±%d" % k, ["x = %d" % k, "x = ±%d" % (2 * k), "x = 0"],
                 "f′(x) = 1 − %d/x² = 0 per x² = %d: <b>x = ±%d</b>." % (k * k, k * k, k))
    if ask == "val":
        return M("f(x) = %s. Qual è il minimo relativo?" % f, pt(k, 2 * k), [pt(*p) for p in W((-k, -2 * k), (k, k * k + 1), (2 * k, k), (k, k + 1)) if p != (k, 2 * k)][:3],
                 "f′ = 0 per x = ±%d; in x = %d f′ passa da − a +: f(%d) = %d + %d/%d = %d: <b>%s</b>. (In x = −%d c’è il massimo %s.)" % (k, k, k, k, k * k, k, 2 * k, pt(k, 2 * k), k, pt(-k, -2 * k)))
    if ask == "asin":
        return M("Quali asintoti ha f(x) = %s?" % f, "x = 0 e y = x", ["x = 0 e y = 0", "solo x = 0", "y = x + %d" % (k * k)],
                 "Per x → 0 f → ∞: x = 0 verticale; f(x) − x = %d/x → 0: obliquo <b>y = x</b>. Risposta: <b>x = 0 e y = x</b>." % (k * k))
    a, b = R.sample([-3, -2, -1, 1, 2, 3, 4], 2)
    a, b = sorted([a, b])
    xm = lambda r: "x − %d" % r if r > 0 else "x + %d" % -r
    g = FR("1", "(%s)(%s)" % (xm(a), xm(b)))
    return M("Qual è il dominio di f(x) = %s?" % g, "x ≠ %s ∧ x ≠ %s" % (fq(a), fq(b)), ["x ≠ %s ∧ x ≠ %s" % (fq(-b), fq(-a)) if (-b, -a) != (a, b) else "x ≠ %s" % fq(b), "x &gt; %s" % fq(b), "ℝ"],
             "Il denominatore si annulla in %s e %s: <b>x ≠ %s ∧ x ≠ %s</b>." % (fq(a), fq(b), fq(a), fq(b)))


def cubic_fig():
    r1 = R.randint(-3, 1)
    r2 = r1 + 2
    d = Fr(R.randint(-2, 2))
    k = R.choice([1, -1])
    # f′ = k(x − r1)(x − r2), f = k[x³/3 − (r1 + r2)/2 x² + r1 r2 x] + d
    f = lambda x: k * (x ** 3 / 3 - (r1 + r2) / 2 * x ** 2 + r1 * r2 * x) + float(d)
    return r1, r2, k, f


def s5_graf():
    r1, r2, k, f = cubic_fig()
    fig = relabel(kurve([(f, BLUE, "")], (-4, 4, 1), (-6, 6, 1), W=300, H=280), "grafico della funzione f")
    ask = R.choice(["dec", "cre", "max", "min"])
    inside = "(%s; %s)" % (fq(r1), fq(r2))
    outside = "x &lt; %s ∨ x &gt; %s" % (fq(r1), fq(r2))
    if ask in ("dec", "cre"):
        ans = inside if (ask == "dec") == (k > 0) else outside
        oth = outside if ans == inside else inside
        return M("%sDal grafico, in quale insieme f è %s?" % (fig, "decrescente" if ask == "dec" else "crescente"), ans,
                 [oth, "(%s; %s)" % (fq(r1 - 1), fq(r2 + 1)), "x &gt; %s" % fq(r1)],
                 "Il grafico %s tra x = %s e x = %s: f è %s in <b>%s</b>." % ("scende" if k > 0 else "sale", fq(r1), fq(r2), "decrescente" if ask == "dec" else "crescente", ans))
    xmax, xmin = (r1, r2) if k > 0 else (r2, r1)
    xa = xmax if ask == "max" else xmin
    return M("%sDal grafico, in quale ascissa f ha un %s relativo?" % (fig, "massimo" if ask == "max" else "minimo"), "x = %s" % fq(xa),
             ["x = %s" % fq(v) for v in W(xmin if ask == "max" else xmax, Fr(r1 + r2, 2), -xa if xa else 3, xa + 3) if v != xa][:3],
             "Il grafico ha la tangente orizzontale in x = %s e x = %s; il %s è in <b>x = %s</b>." % (fq(r1), fq(r2), "massimo" if ask == "max" else "minimo", fq(xa)))


def s5_deriv():
    r = R.randint(-3, 3)
    k = R.choice([1, -1])
    g = lambda x: k * (x - r)
    fig = relabel(kurve([(g, BLUE, "")], (-4, 4, 1), (-5, 5, 1), W=300, H=260), "grafico di f′")
    t = "minimo" if k > 0 else "massimo"
    return M("%sNella figura c’è il grafico della <b>derivata</b> f′. Che cosa ha f in x = %s?" % (fig, fq(r)), "un %s relativo" % t,
             ["un %s relativo" % ("massimo" if t == "minimo" else "minimo"), "un punto di flesso", "uno zero"],
             "f′ si annulla in x = %s e passa da %s a %s: f ha <b>un %s relativo</b>." % (fq(r), "−" if k > 0 else "+", "+" if k > 0 else "−", t))


def main():
    seen = set()
    sets = [
        ("Simmetrie e intersezioni con gli assi", mix(R, seen, [(s1_sim, 10), (s2_int, 10)])),
        ("Funzioni razionali", mix(R, seen, [(s4_raz, 14), (s2_int, 6)])),
        ("Funzioni esponenziali e logaritmiche", mix(R, seen, [(s3_esp, 20)])),
        ("Leggere il grafico", mix(R, seen, [(s5_graf, 14), (s5_deriv, 6)])),
        ("Riepilogo", mix(R, seen, [(s1_sim, 4), (s3_esp, 6), (s4_raz, 4), (s5_graf, 6)])),
    ]
    body = L(["Lo <b>studio di funzione</b> segue uno schema: 1) dominio; 2) simmetrie (pari se f(−x) = f(x), dispari se f(−x) = −f(x)); 3) intersezioni con gli assi e segno; 4) limiti agli estremi del dominio e asintoti.",
              "5) Derivata prima: crescenza, decrescenza, massimi e minimi. 6) Derivata seconda: concavità e flessi. 7) Grafico.",
              "I punti stazionari vanno cercati <b>solo nel dominio</b>: per f(x) = x² − 8 ln x la radice x = −2 non si considera.",
              "Dal grafico di f′ si legge la crescenza di f: dove f′ &gt; 0 f cresce, dove f′ si annulla cambiando segno f ha un massimo o un minimo."],
             [("f(x) = x e<sup>−x</sup>", ["f′(x) = e<sup>−x</sup>(1 − x)", "f′ &gt; 0 per x &lt; 1"], "massimo in (1; 1/e)"),
              ("f(x) = x + 4/x", ["Dispari; asintoti x = 0 e y = x", "f′ = 1 − 4/x² = 0 per x = ±2"], "massimo (−2; −4), minimo (2; 4)")],
             [["Pensare che x³ + 1 sia dispari", "f(−x) = −x³ + 1, diverso da −f(x) = −x³ − 1."],
              ["Dimenticare il dominio dei logaritmi", "ln x esiste solo per x &gt; 0."],
              ["Leggere f′ come se fosse f", "Gli zeri di f′ sono i punti stazionari di f, non i suoi zeri."]])
    faq = [("Da dove si comincia uno studio di funzione?", "Dal dominio: tutte le altre informazioni (simmetrie, limiti, derivate) hanno senso solo dove la funzione è definita."),
           ("A che cosa serve la simmetria?", "Se f è pari o dispari basta studiarla per x ≥ 0 e completare il grafico per simmetria rispetto all’asse y o all’origine.")]
    unit(G, R, "studio-di-funzione", "F",
         "Studio di funzioni razionali, esponenziali e logaritmiche e rappresentazione del grafico",
         "Studio di funzione", "Studio di funzione",
         "Schede di matematica per la quinta liceo sullo studio di funzione: simmetrie, intersezioni con gli assi, dominio e asintoti di funzioni razionali, massimi e minimi di funzioni esponenziali e logaritmiche, lettura del grafico di f e di f′. 100 esercizi con soluzioni.",
         "Dominio, simmetrie, segno, limiti, f′, f″, grafico.", "I punti stazionari si cercano solo nel dominio.",
         body, faq, sets, 9)


if __name__ == "__main__":
    main()
