# -*- coding: utf-8 -*-
"""
Italia Matematica quinta liceo: Funzioni reali — dominio, segno, simmetrie (Relazioni e funzioni)
  python3 tools/gen_it_matematica_l5_dominio_e_segno_di_una_funzione.py
Studio preliminare di una funzione: dominio di funzioni razionali, irrazionali, logaritmiche ed esponenziali (anche composte),
intersezioni con gli assi, segno, funzioni pari e dispari, funzioni crescenti, funzione inversa e composta.
Errori: dominio di ln(x²) con x > 0, dimenticare il denominatore dentro la radice, e^x che si annulla.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, P2, FR

R = random.Random(72502)
G = "quinta-liceo"


def lin(a, b):
    return P2(0, a, b)


DOM = [("ln(x² − 4)", "x &lt; −2 ∨ x &gt; 2", ["x &gt; 2", "−2 &lt; x &lt; 2", "x ≠ ±2"], "x² − 4 &gt; 0"),
       ("ln(x²)", "x ≠ 0", ["x &gt; 0", "ℝ", "x ≥ 0"], "x² &gt; 0, cioè x ≠ 0"),
       ("e<sup>1/x</sup>", "x ≠ 0", ["ℝ", "x &gt; 0", "x ≥ 0"], "l’esponente 1/x esiste per x ≠ 0"),
       ("√(ln x)", "x ≥ 1", ["x &gt; 0", "x &gt; 1", "ℝ"], "x &gt; 0 e ln x ≥ 0, cioè x ≥ 1"),
       ("1/(e<sup>x</sup> − 1)", "x ≠ 0", ["ℝ", "x &gt; 0", "x ≠ 1"], "e<sup>x</sup> ≠ 1, cioè x ≠ 0"),
       ("x / ln x", "x &gt; 0 ∧ x ≠ 1", ["x &gt; 0", "x ≠ 1", "x ≥ 1"], "x &gt; 0 e ln x ≠ 0"),
       ("ln((x + 1)/(x − 2))", "x &lt; −1 ∨ x &gt; 2", ["−1 &lt; x &lt; 2", "x &gt; 2", "x ≠ 2"], "(x + 1)/(x − 2) &gt; 0"),
       ("√(e<sup>x</sup> − 1)", "x ≥ 0", ["x &gt; 0", "ℝ", "x ≥ 1"], "e<sup>x</sup> ≥ 1, cioè x ≥ 0"),
       ("√(4 − x²)", "−2 ≤ x ≤ 2", ["x ≤ −2 ∨ x ≥ 2", "x ≤ 2", "−4 ≤ x ≤ 4"], "4 − x² ≥ 0"),
       ("ln(1 − x)", "x &lt; 1", ["x &gt; 1", "x &lt; 0", "x ≤ 1"], "1 − x &gt; 0"),
       ("e<sup>x</sup> / (x² − 9)", "x ≠ ±3", ["ℝ", "x &gt; 3", "x ≠ 3"], "il denominatore non si annulla"),
       ("√((x − 1)/(x + 3))", "x &lt; −3 ∨ x ≥ 1", ["x ≤ −3 ∨ x ≥ 1", "−3 &lt; x ≤ 1", "x ≥ 1"], "(x − 1)/(x + 3) ≥ 0 con x ≠ −3"),
       ("ln(ln x)", "x &gt; 1", ["x &gt; 0", "x ≥ 1", "x &gt; e"], "x &gt; 0 e ln x &gt; 0"),
       ("1/√(x − 5)", "x &gt; 5", ["x ≥ 5", "x ≠ 5", "x &lt; 5"], "x − 5 &gt; 0 (radice al denominatore)"),
       ("∛(x − 2)", "ℝ", ["x ≥ 2", "x &gt; 2", "x ≠ 2"], "la radice cubica esiste per ogni numero reale")]


def s1_dom():
    f, a, w, e = R.choice(DOM)
    return M("Qual è il dominio di f(x) = %s?" % f, a, w, "Condizioni: %s → <b>%s</b>." % (e, a))


def s1_dom_par():
    a = nz(R, -6, 6)
    b = R.randint(1, 5)
    k = R.choice(["ln", "rad"])
    if k == "ln":
        f = "ln(%s)" % lin(-1, a) if R.random() < 0.5 else "ln(%s)" % lin(1, -a)
        neg = f.startswith("ln(−")
        ans = "x &lt; %s" % fq(a) if neg else "x &gt; %s" % fq(a)
        w = ["x &gt; %s" % fq(a) if neg else "x &lt; %s" % fq(a), "x ≠ %s" % fq(a), "x &gt; %s" % fq(-a)]
        return M("Qual è il dominio di f(x) = %s?" % f, ans, w, "L’argomento del logaritmo deve essere positivo: <b>%s</b>." % ans)
    f = "√(%s) + ln(%s)" % (lin(1, -a), lin(-1, a + b))
    ans = "%s ≤ x &lt; %s" % (fq(a), fq(a + b))
    return M("Qual è il dominio di f(x) = %s?" % f, ans, ["x ≥ %s" % fq(a), "x &lt; %s" % fq(a + b), "%s &lt; x ≤ %s" % (fq(a), fq(a + b))],
             "Sistema: x − %s ≥ 0 e %s − x &gt; 0 → <b>%s</b>." % (fq(a), fq(a + b), ans) if a >= 0 else "Sistema delle due condizioni: <b>%s</b>." % ans)


SEGNO = [("(x − 2)e<sup>x</sup>", "x &gt; 2", ["x &gt; 0", "x &lt; 2", "ℝ"], "e<sup>x</sup> &gt; 0 sempre: conta solo x − 2"),
         ("x ln x", "x &gt; 1", ["0 &lt; x &lt; 1", "x &gt; 0", "x &gt; e"], "dominio x &gt; 0; x &gt; 0 e ln x &gt; 0 per x &gt; 1"),
         ("(1 − x²)e<sup>−x</sup>", "−1 &lt; x &lt; 1", ["x &lt; −1 ∨ x &gt; 1", "x &lt; 1", "x &gt; 0"], "e<sup>−x</sup> &gt; 0: conta 1 − x² &gt; 0"),
         ("ln x / x", "x &gt; 1", ["0 &lt; x &lt; 1", "x &gt; 0", "x &lt; 1"], "dominio x &gt; 0, x &gt; 0: conta ln x &gt; 0"),
         ("e<sup>x</sup> − 1", "x &gt; 0", ["x &gt; 1", "ℝ", "x &lt; 0"], "e<sup>x</sup> &gt; 1 per x &gt; 0"),
         ("(x + 3)/(x − 1)", "x &lt; −3 ∨ x &gt; 1", ["−3 &lt; x &lt; 1", "x &gt; 1", "x &gt; −3"], "segni concordi di numeratore e denominatore"),
         ("x² e<sup>x</sup>", "x ≠ 0", ["x &gt; 0", "ℝ", "x &lt; 0"], "x² &gt; 0 per x ≠ 0 ed e<sup>x</sup> &gt; 0"),
         ("ln(x + 2)", "x &gt; −1", ["x &gt; −2", "x &gt; 0", "−2 &lt; x &lt; −1"], "x + 2 &gt; 1"),
         ("x³ − 4x", "−2 &lt; x &lt; 0 ∨ x &gt; 2", ["x &gt; 2", "x &lt; −2 ∨ 0 &lt; x &lt; 2", "x &gt; 0"], "x(x − 2)(x + 2) &gt; 0: segno da destra +, −, +, −")]


def s2_segno():
    f, a, w, e = R.choice(SEGNO)
    return M("Per quali x la funzione f(x) = %s è positiva?" % f, a, w, "%s: <b>%s</b>." % (e[0].upper() + e[1:], a))


def s2_assi():
    k = R.choice(["exp", "ln", "poly"])
    if k == "exp":
        a = R.randint(1, 4)
        f = "e<sup>x</sup> − %d" % (a + 1) if False else "(x − %d)e<sup>x</sup>" % a
        return M("In quali punti il grafico di f(x) = %s incontra gli assi?" % f, "(%d; 0) e (0; −%d)" % (a, a), ["(%d; 0) e (0; %d)" % (a, a), "solo (%d; 0)" % a, "(−%d; 0) e (0; −%d)" % (a, a)],
                 "y = 0 per x = %d (e<sup>x</sup> non si annulla); x = 0 dà y = −%d: <b>(%d; 0) e (0; −%d)</b>." % (a, a, a, a))
    if k == "ln":
        a = R.randint(1, 5)
        return M("In quale punto il grafico di f(x) = ln(x − %d) incontra l’asse x?" % a, "(%d; 0)" % (a + 1), ["(%d; 0)" % a, "(0; %d)" % (a + 1), "(%d; 0)" % (a + 2)],
                 "ln(x − %d) = 0 ⟺ x − %d = 1 → <b>(%d; 0)</b>. Non incontra l’asse y (x = 0 non è nel dominio)." % (a, a, a + 1))
    p, q = sorted(R.sample(range(-5, 6), 2))
    ans = "(%s; 0), (%s; 0) e (0; %s)" % (fq(p), fq(q), fq(p * q))
    return M("In quali punti il grafico di f(x) = %s incontra gli assi?" % P2(1, -(p + q), p * q), ans, ["(%s; 0), (%s; 0) e (0; %s)" % (fq(-q), fq(-p), fq(p * q)), "(%s; 0) e (%s; 0)" % (fq(p), fq(q)), "(%s; 0), (%s; 0) e (0; %s)" % (fq(p), fq(q), fq(-(p + q)))],
             "Zeri: x = %s e x = %s; per x = 0: y = %s. <b>%s</b>." % (fq(p), fq(q), fq(p * q), ans))


PARI = [("x² e<sup>−x²</sup>", "pari"), ("x e<sup>−x²</sup>", "dispari"), ("ln(x² + 1)", "pari"), ("x³ − sen x", "dispari"), ("x + cos x", "né pari né dispari"),
        ("cos x / x²", "pari"), ("e<sup>x</sup>", "né pari né dispari"), ("sen x · cos x", "dispari"), ("|x| − 1", "pari"), ("x² + x", "né pari né dispari"),
        ("tg x", "dispari"), ("e<sup>x</sup> + e<sup>−x</sup>", "pari"), ("e<sup>x</sup> − e<sup>−x</sup>", "dispari"), ("ln x", "né pari né dispari (il dominio non è simmetrico)")]


def s3_pari():
    f, a = R.choice(PARI)
    opts = ["pari", "dispari", "né pari né dispari", "sia pari sia dispari"]
    if a not in opts:
        opts = [a, "pari", "dispari", "sia pari sia dispari"]
    return M("La funzione f(x) = %s è…" % f, a, [o for o in opts if o != a][:3],
             "Calcolo f(−x) e lo confronto con f(x) e −f(x): <b>%s</b>." % a)


def s4_comp():
    k = R.choice(["fg", "gf", "inv"])
    a, b = nz(R, -4, 4), R.randint(-4, 4)
    if k == "inv":
        t = R.choice(["exp", "ln"])
        if t == "exp":
            return M("Qual è l’inversa di f(x) = e<sup>x</sup> %s %d?" % ("+" if b >= 0 else "−", abs(b)) if b else "Qual è l’inversa di f(x) = e<sup>2x</sup>?",
                     ("f⁻¹(x) = ln(x %s %d)" % ("−" if b >= 0 else "+", abs(b))) if b else "f⁻¹(x) = ½ ln x",
                     (["f⁻¹(x) = ln x %s %d" % ("−" if b >= 0 else "+", abs(b)), "f⁻¹(x) = e<sup>−x</sup> %s %d" % ("−" if b >= 0 else "+", abs(b)), "f⁻¹(x) = 1/(e<sup>x</sup> %s %d)" % ("+" if b >= 0 else "−", abs(b))]) if b else ["f⁻¹(x) = 2 ln x", "f⁻¹(x) = ln(2x)", "f⁻¹(x) = e<sup>x/2</sup>"],
                     "Ricavo x da y = f(x) con il logaritmo e scambio x e y.")
        return M("Qual è l’inversa di f(x) = ln(x %s %d)?" % ("+" if b >= 0 else "−", abs(b)) if b else "Qual è l’inversa di f(x) = 3 ln x?",
                 ("f⁻¹(x) = e<sup>x</sup> %s %d" % ("−" if b >= 0 else "+", abs(b))) if b else "f⁻¹(x) = e<sup>x/3</sup>",
                 (["f⁻¹(x) = e<sup>x %s %d</sup>" % ("−" if b >= 0 else "+", abs(b)), "f⁻¹(x) = ln(x %s %d)" % ("−" if b >= 0 else "+", abs(b)), "f⁻¹(x) = e<sup>x</sup> %s %d" % ("+" if b >= 0 else "−", abs(b))]) if b else ["f⁻¹(x) = 3e<sup>x</sup>", "f⁻¹(x) = e<sup>3x</sup>", "f⁻¹(x) = ln(x/3)"],
                 "Ricavo x da y = f(x) con l’esponenziale e scambio x e y.")
    f = "e<sup>x</sup>"
    g = lin(a, b)
    if k == "fg":
        return M("Date f(x) = e<sup>x</sup> e g(x) = %s, qual è f(g(x))?" % g, "e<sup>%s</sup>" % g, ["%s" % lin(a, b).replace("x", "e<sup>x</sup>"), "e<sup>x</sup> · (%s)" % g, "e<sup>x</sup> + %s" % g],
                 "f(g(x)): al posto di x in f si mette g(x): <b>e<sup>%s</sup></b>." % g)
    return M("Date f(x) = e<sup>x</sup> e g(x) = %s, qual è g(f(x))?" % g, lin(a, b).replace("x", "e<sup>x</sup>"), ["e<sup>%s</sup>" % g, "e<sup>x</sup> · (%s)" % g, "%se<sup>x</sup>" % ("" if a == 1 else fq(a)) if b else "e<sup>%dx</sup>" % a],
             "g(f(x)): al posto di x in g si mette e<sup>x</sup>: <b>%s</b>." % lin(a, b).replace("x", "e<sup>x</sup>"))


def main():
    seen = set()
    sets = [
        ("Dominio", mix(R, seen, [(s1_dom, 15), (s1_dom_par, 5)])),
        ("Intersezioni con gli assi", mix(R, seen, [(s2_assi, 14), (s1_dom_par, 6)])),
        ("Segno", mix(R, seen, [(s2_segno, 9), (s2_assi, 11)])),
        ("Simmetrie", mix(R, seen, [(s3_pari, 14), (s1_dom_par, 6)])),
        ("Inversa e composta", mix(R, seen, [(s4_comp, 20)])),
    ]
    body = L(["Lo <b>studio preliminare</b> di una funzione comincia dal <b>dominio</b>: denominatori ≠ 0, radicandi ≥ 0 (indice pari), argomenti dei logaritmi &gt; 0. Le esponenziali sono definite per ogni x e sono sempre positive.",
              "Poi si cercano le <b>intersezioni</b> con gli assi (y = 0 e x = 0) e il <b>segno</b>: si studia dove f(x) &gt; 0, ricordando che e<sup>x</sup> &gt; 0 e che ln x &gt; 0 per x &gt; 1.",
              "Si controllano le <b>simmetrie</b>: f pari se f(−x) = f(x), dispari se f(−x) = −f(x) (il dominio deve essere simmetrico).",
              "Questi elementi preparano il grafico: dividono il piano in zone dove la curva può stare."],
             [("Dominio di ln((x + 1)/(x − 2))", ["(x + 1)/(x − 2) &gt; 0"], "x &lt; −1 ∨ x &gt; 2"),
              ("Segno di (x − 2)e<sup>x</sup>", ["e<sup>x</sup> &gt; 0"], "f(x) &gt; 0 per x &gt; 2")],
             [["Dominio di ln(x²): x &gt; 0", "x² &gt; 0 vale per ogni x ≠ 0."],
              ["Cercare gli zeri di e<sup>x</sup>", "e<sup>x</sup> non si annulla mai."],
              ["ln x pari o dispari", "Il dominio x &gt; 0 non è simmetrico: non è né pari né dispari."]])
    faq = [("Perché lo studio del segno è utile per il grafico?", "Indica dove il grafico sta sopra o sotto l’asse x: si possono cancellare subito le zone del piano dove la funzione non passa."),
           ("Una funzione può essere sia pari sia dispari?", "Solo la funzione nulla f(x) = 0 (su un dominio simmetrico): infatti f(x) = f(−x) = −f(x) implica f(x) = 0.")]
    unit(G, R, "dominio-e-segno-di-una-funzione", "F",
         "Funzioni reali di variabile reale: dominio, segno, simmetrie, funzioni composte e inverse (studio preliminare)",
         "Funzioni reali: dominio, segno e simmetrie", "Dominio e segno",
         "Schede di matematica per la quinta liceo sullo studio preliminare delle funzioni: dominio di funzioni razionali, irrazionali, logaritmiche ed esponenziali, intersezioni con gli assi, segno, simmetrie, inversa e composta. 100 esercizi con soluzioni.",
         "Argomento del logaritmo > 0, radicando ≥ 0, denominatore ≠ 0", "e^x è sempre positiva; ln x > 0 per x > 1.",
         body, faq, sets, 2)


if __name__ == "__main__":
    main()
