# -*- coding: utf-8 -*-
"""
Italia Matematica terza liceo: Funzioni e loro proprietà (Relazioni e funzioni)
  python3 tools/gen_it_matematica_l3_funzioni_e_loro_proprieta.py
Dominio (frazioni, radici, frazioni sotto radice), zeri e segno, funzioni pari e dispari, funzioni iniettive e invertibili,
funzione inversa, funzione composta, trasformazioni del grafico (traslazioni, simmetrie, valore assoluto).
Errori: dominio di √(x² − 9) con x ≥ 3 soltanto, f(x − 2) traslata a sinistra, (f ∘ g)(x) = f(x) · g(x).
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, P2, FR, poly, kurve, relabel

R = random.Random(72302)
G = "terza-liceo"
BLUE, RED = "#1f6fd1", "#dc2626"


def lin(a, b):
    return P2(0, a, b)


def s1_dom():
    k = R.choice(["fq", "rq", "rfr", "rdiff"])
    a = R.randint(1, 7)
    if k == "fq":
        p, q = R.sample(range(-6, 7), 2)
        den = P2(1, -(p + q), p * q)
        ans = "x ≠ %s ∧ x ≠ %s" % (fq(min(p, q)), fq(max(p, q)))
        w = ["x ≠ %s ∧ x ≠ %s" % (fq(-max(p, q)), fq(-min(p, q))), "ℝ", "x ≠ %s" % fq(p * q)]
        return M("Qual è il dominio di f(x) = %s?" % FR("x + 1", den), ans, [x for x in w if x != ans] + ["x ≠ %s" % fq(p)], "Il denominatore %s si annulla per x = %s e x = %s: <b>%s</b>." % (den, fq(p), fq(q), ans))
    if k == "rq":
        ans = "x ≤ −%d ∨ x ≥ %d" % (a, a)
        return M("Qual è il dominio di f(x) = √(%s)?" % P2(1, 0, -a * a), ans, ["x ≥ %d" % a, "−%d ≤ x ≤ %d" % (a, a), "x ≥ %d" % (a * a)],
                 "Serve x² − %d ≥ 0: valori esterni alle radici ±%d, <b>%s</b>." % (a * a, a, ans))
    if k == "rdiff":
        ans = "−%d ≤ x ≤ %d" % (a, a)
        return M("Qual è il dominio di f(x) = √(%s)?" % P2(-1, 0, a * a), ans, ["x ≤ −%d ∨ x ≥ %d" % (a, a), "x ≤ %d" % a, "ℝ"],
                 "Serve %d − x² ≥ 0, cioè x² ≤ %d: <b>%s</b>." % (a * a, a * a, ans))
    b = R.randint(-6, 6)
    if b == a or b == -a:
        return None
    # √((x − a)/(x − b))
    lo, hi = sorted([a, b])
    o1 = "≤" if lo == a else "&lt;"
    o2 = "≥" if hi == a else "&gt;"
    ans = "x %s %s ∨ x %s %s" % (o1, fq(lo), o2, fq(hi))
    return M("Qual è il dominio di f(x) = √(%s)?" % FR(lin(1, -a), lin(1, -b)), ans, ["%s %s x %s %s" % (fq(lo), "&lt;" if o1 == "≤" else "≤", "&lt;" if o2 == "&gt;" else "≤", fq(hi)), "x ≥ %s" % fq(a), "x ≤ %s ∨ x ≥ %s" % (fq(lo), fq(hi))],
             "Serve (x − %s)/(x − %s) ≥ 0 con x ≠ %s: <b>%s</b>." % (fq(a), fq(b), fq(b), ans))


PARI = [("x⁴ − 3x²", "pari"), ("x³ − 2x", "dispari"), ("x² + x", "né pari né dispari"), ("|x| + 1", "pari"), ("5x", "dispari"),
        ("x² − 4", "pari"), ("x³ + 1", "né pari né dispari"), ("2x⁵ + x³", "dispari"), ("(x − 1)²", "né pari né dispari"), ("x⁶ + x² + 7", "pari"),
        ("1/x", "dispari"), ("x/(x² + 1)", "dispari"), ("|x − 2|", "né pari né dispari"), ("x² · |x|", "pari")]


def s2_pari():
    f, a = R.choice(PARI)
    return M("La funzione f(x) = %s è…" % f, a, [x for x in ["pari", "dispari", "né pari né dispari", "sia pari sia dispari"] if x != a],
             "Calcolo f(−x): se f(−x) = f(x) è pari (simmetrica rispetto all’asse y), se f(−x) = −f(x) è dispari (simmetrica rispetto all’origine). Qui è <b>%s</b>." % a)


INIET = [("f(x) = 2x + 1 in ℝ", "sì"), ("f(x) = x² in ℝ", "no"), ("f(x) = x³ in ℝ", "sì"), ("f(x) = |x| in ℝ", "no"), ("f(x) = x² con x ≥ 0", "sì"),
         ("f(x) = x² − 4x in ℝ", "no"), ("f(x) = 1/x con x ≠ 0", "sì"), ("f(x) = −3x + 5 in ℝ", "sì"), ("f(x) = x⁴ in ℝ", "no"), ("f(x) = 7 (costante) in ℝ", "no")]


def s2_iniet():
    f, a = R.choice(INIET)
    return M("La funzione %s è iniettiva (e quindi invertibile sul suo insieme immagine)?" % f, a, ["no" if a == "sì" else "sì", "solo per x &gt; 0", "solo se è pari"],
             "È iniettiva se valori diversi di x hanno immagini diverse (ogni retta orizzontale taglia il grafico al massimo una volta): <b>%s</b>." % a)


def s3_inv():
    a, b = nz(R, -5, 5), R.randint(-9, 9)
    if abs(a) == 1 and b == 0:
        return None
    k = R.choice(["lin", "cubo"]) if R.random() < 0.3 else "lin"
    if k == "cubo":
        return M("Qual è la funzione inversa di f(x) = x³ %s %d?" % ("+" if b >= 0 else "−", abs(b)), "f⁻¹(x) = ∛(x %s %d)" % ("−" if b >= 0 else "+", abs(b)),
                 ["f⁻¹(x) = ∛x %s %d" % ("−" if b >= 0 else "+", abs(b)), "f⁻¹(x) = ∛(x %s %d)" % ("+" if b >= 0 else "−", abs(b)), "f⁻¹(x) = 1/(x³ %s %d)" % ("+" if b >= 0 else "−", abs(b))],
                 "Scrivo y = x³ %s %d e ricavo x: x = ∛(y %s %d); poi scambio x e y: <b>f⁻¹(x) = ∛(x %s %d)</b>." % ("+" if b >= 0 else "−", abs(b), "−" if b >= 0 else "+", abs(b), "−" if b >= 0 else "+", abs(b)))
    if abs(a) == 1:
        ans = "f⁻¹(x) = %s" % (lin(1, -b) if a == 1 else lin(-1, b))
        w = ["f⁻¹(x) = %s" % lin(1, b), "f⁻¹(x) = %s" % FR("1", lin(a, b)), "f⁻¹(x) = %s" % lin(-1, -b)]
    else:
        ans = "f⁻¹(x) = %s" % (FR(lin(1, -b), str(a)) if a > 0 else FR(lin(-1, b), str(-a)))
        w = ["f⁻¹(x) = %s" % (FR(lin(1, b), str(abs(a)))), "f⁻¹(x) = %s" % FR("1", lin(a, b)), "f⁻¹(x) = %s" % lin(Fr(1, a) if False else a, -b), "f⁻¹(x) = %s" % FR(lin(1, -b), str(abs(a))) if a < 0 else "f⁻¹(x) = %s" % FR(lin(-1, b), str(a))]
    return M("Qual è la funzione inversa di f(x) = %s?" % lin(a, b), ans, [x for x in w if x != ans],
             "Ricavo x da y = %s, poi scambio x e y: <b>%s</b>." % (lin(a, b), ans))


def s3_comp():
    a, b = nz(R, -4, 4), R.randint(-5, 5)
    c = R.randint(-4, 4)
    f = lin(a, b)
    g = P2(1, 0, c)
    k = R.choice(["fg", "gf"])
    if k == "fg":
        ans = "(f ∘ g)(x) = %s" % P2(a, 0, a * c + b)
        w = ["(f ∘ g)(x) = %s" % P2(a * a, 2 * a * b, b * b + c), "(f ∘ g)(x) = %s" % poly([a, b, a * c, b * c]), "(f ∘ g)(x) = %s" % P2(1, a, b + c)]
        e = "(f ∘ g)(x) = f(g(x)): al posto di x in f metto %s: %s(%s) %s %d = <b>%s</b>." % (g, fq(a), g, "+" if b >= 0 else "−", abs(b), ans.split("= ")[1])
    else:
        ans = "(g ∘ f)(x) = %s" % P2(a * a, 2 * a * b, b * b + c)
        w = ["(g ∘ f)(x) = %s" % P2(a, 0, a * c + b), "(g ∘ f)(x) = %s" % P2(a, b, c), "(g ∘ f)(x) = %s" % P2(a * a, 0, b * b + c)]
        e = "(g ∘ f)(x) = g(f(x)) = (%s)² %s %d = <b>%s</b>." % (f, "+" if c >= 0 else "−", abs(c), ans.split("= ")[1])
    return M("Date f(x) = %s e g(x) = %s, calcola %s." % (f, g, "(f ∘ g)(x)" if k == "fg" else "(g ∘ f)(x)"), ans, [x for x in w if x != ans], e)


TR = [("y = f(x − %d)", "traslazione di %d verso destra"), ("y = f(x + %d)", "traslazione di %d verso sinistra"), ("y = f(x) + %d", "traslazione di %d verso l’alto"),
      ("y = f(x) − %d", "traslazione di %d verso il basso")]
TR2 = [("y = −f(x)", "simmetria rispetto all’asse x"), ("y = f(−x)", "simmetria rispetto all’asse y"), ("y = −f(−x)", "simmetria rispetto all’origine"),
       ("y = |f(x)|", "le parti sotto l’asse x si ribaltano sopra"), ("y = f(|x|)", "la parte con x ≥ 0 si ripete simmetrica a sinistra")]


def s4_trasf():
    if R.random() < 0.6:
        k = R.randint(1, 6)
        f, a = R.choice(TR)
        f, a = f % k, a % k
        opts = [t[1] % k for t in TR]
    else:
        f, a = R.choice(TR2)
        opts = [t[1] for t in TR2]
    return M("Come si ottiene il grafico di %s da quello di y = f(x)?" % f, a, [o for o in opts if o != a][:3], "%s: <b>%s</b>." % (f, a))


def s4_graf():
    a, b = R.randint(-3, 3), R.randint(-3, 3)
    if (a, b) == (0, 0):
        return None
    fig = relabel(kurve([(lambda x: x * x, BLUE, "f"), (lambda x, a=a, b=b: (x - a) ** 2 + b, RED, "g")], (-5, 5, 1), (-4, 8, 2), W=300, H=260), "grafici di f e g")
    ans = "g(x) = f(x %s %d) %s %d" % ("−" if a >= 0 else "+", abs(a), "+" if b >= 0 else "−", abs(b))
    w = ["g(x) = f(x %s %d) %s %d" % ("+" if a >= 0 else "−", abs(a), "+" if b >= 0 else "−", abs(b)), "g(x) = f(x %s %d) %s %d" % ("−" if b >= 0 else "+", abs(b), "+" if a >= 0 else "−", abs(a)), "g(x) = f(x %s %d) %s %d" % ("+" if a >= 0 else "−", abs(a), "−" if b >= 0 else "+", abs(b))]
    return M("%sIl grafico blu è f(x) = x². Il grafico rosso g si ottiene traslando f. Quale espressione ha g?" % fig, ans.replace("x − 0", "x").replace(" + 0", "").replace(" − 0", ""), W(*[x.replace("x − 0", "x").replace("x + 0", "x").replace(" + 0", "").replace(" − 0", "") for x in w + ["g(x) = f(x %s %d) %s %d" % ("−" if a >= 0 else "+", abs(a) + 1, "+" if b >= 0 else "−", abs(b)), "g(x) = f(x) %s %d" % ("+" if a + b >= 0 else "−", abs(a + b) + 1)]]),
             "Il vertice passa da (0; 0) a (%s; %s): traslazione di vettore (%s; %s), <b>%s</b>." % (fq(a), fq(b), fq(a), fq(b), ans.replace("x − 0", "x").replace(" + 0", "").replace(" − 0", "")))


def s5_segno():
    p, q = sorted(R.sample(range(-6, 7), 2))
    a = R.choice([1, -1])
    f = P2(a, -a * (p + q), a * p * q)
    if a > 0:
        ans = "x &lt; %s ∨ x &gt; %s" % (fq(p), fq(q))
        w = ["%s &lt; x &lt; %s" % (fq(p), fq(q)), "x &gt; %s" % fq(q), "x &lt; %s ∨ x &gt; %s" % (fq(-q), fq(-p))]
    else:
        ans = "%s &lt; x &lt; %s" % (fq(p), fq(q))
        w = ["x &lt; %s ∨ x &gt; %s" % (fq(p), fq(q)), "x &lt; %s" % fq(q), "%s &lt; x &lt; %s" % (fq(-q), fq(-p))]
    return M("Per quali x la funzione f(x) = %s è positiva?" % f, ans, [x for x in w if x != ans],
             "Zeri %s e %s; parabola rivolta verso %s: f(x) &gt; 0 per <b>%s</b>." % (fq(p), fq(q), "l’alto" if a > 0 else "il basso", ans))


def main():
    seen = set()
    sets = [
        ("Dominio", mix(R, seen, [(s1_dom, 20)])),
        ("Funzioni pari, dispari e iniettive", mix(R, seen, [(s2_pari, 12), (s2_iniet, 8)])),
        ("Funzione inversa e composta", mix(R, seen, [(s3_inv, 10), (s3_comp, 10)])),
        ("Trasformazioni del grafico", mix(R, seen, [(s4_trasf, 10), (s4_graf, 10)])),
        ("Zeri e segno", mix(R, seen, [(s5_segno, 14), (s1_dom, 6)])),
    ]
    body = L(["Una funzione reale f: D → ℝ associa a ogni x del <b>dominio</b> D un solo numero f(x). Il dominio si trova escludendo denominatori nulli e radicandi negativi (per le radici di indice pari).",
              "f è <b>pari</b> se f(−x) = f(x) (grafico simmetrico rispetto all’asse y), <b>dispari</b> se f(−x) = −f(x) (simmetrico rispetto all’origine).",
              "f è <b>iniettiva</b> se a x diversi corrispondono immagini diverse: allora è invertibile e la <b>funzione inversa</b> si trova ricavando x da y = f(x) e scambiando le lettere.",
              "La <b>composta</b> (g ∘ f)(x) = g(f(x)). Trasformazioni: f(x − a) + b trasla di (a; b); −f(x) simmetria rispetto all’asse x; f(−x) rispetto all’asse y."],
             [("Inversa di f(x) = 3x − 6", ["y = 3x − 6 → x = (y + 6)/3"], "f⁻¹(x) = (x + 6)/3"),
              ("f(x) = x², g(x) = x + 1: (f ∘ g)(x)", ["f(g(x)) = (x + 1)²"], "x² + 2x + 1")],
             [["f(x − 2): traslazione a sinistra", "f(x − 2) trasla di 2 verso destra."],
              ["(f ∘ g)(x) = f(x) · g(x)", "La composta si ottiene sostituendo g(x) al posto di x in f."],
              ["Dominio di √(x² − 9): x ≥ 3", "Anche x ≤ −3 va bene: x² − 9 ≥ 0 per valori esterni."]])
    faq = [("Una funzione può essere né pari né dispari?", "Sì, la maggior parte: per esempio f(x) = x² + x, perché f(−x) = x² − x non è né f(x) né −f(x)."),
           ("Che relazione c’è tra il grafico di f e quello di f⁻¹?", "Sono simmetrici rispetto alla bisettrice y = x del primo e terzo quadrante.")]
    unit(G, R, "funzioni-e-loro-proprieta", "F",
         "Funzioni reali: dominio, zeri e segno, simmetrie, funzioni iniettive, inversa e composta; trasformazioni dei grafici",
         "Funzioni e loro proprietà", "Funzioni e proprietà",
         "Schede di matematica per la terza liceo sulle funzioni: dominio, zeri e segno, funzioni pari e dispari, iniettive e invertibili, funzione inversa e composta, traslazioni e simmetrie dei grafici. 100 esercizi con soluzioni.",
         "f(−x) = f(x): pari; f(−x) = −f(x): dispari.", "f(x − a) + b trasla il grafico di a a destra e di b in alto.",
         body, faq, sets, 2)


if __name__ == "__main__":
    main()
