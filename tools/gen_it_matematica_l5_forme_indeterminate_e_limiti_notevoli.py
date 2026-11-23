# -*- coding: utf-8 -*-
"""
Italia Matematica quinta liceo: Forme indeterminate e limiti notevoli (Relazioni e funzioni)
  python3 tools/gen_it_matematica_l5_forme_indeterminate_e_limiti_notevoli.py
Forma 0/0 con la scomposizione e con la razionalizzazione, forma ∞ − ∞ con i radicali, forma ∞/∞ e gerarchia degli infiniti
(ln x, xⁿ, eˣ), limiti notevoli: sen x/x, (1 − cos x)/x², (eˣ − 1)/x, ln(1 + x)/x, (1 + 1/x)ˣ = e e loro varianti.
Errori: 0/0 = 1, lim sen 3x/x = 1, (1 + 1/x)ˣ → 1, √(x² + x) − x → 0.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, P2, FR

R = random.Random(72504)
G = "quinta-liceo"
PINF, MINF = "+∞", "−∞"


def lim(x0, f):
    return "lim<sub>x→%s</sub> %s" % (x0, f)


def s1_scomp():
    r = nz(R, -5, 5)
    s_ = R.randint(-6, 6)
    if s_ == r:
        return None
    k = R.choice(["diff", "trin"])
    if k == "diff":
        num = P2(1, 0, -r * r)
        den = P2(0, 1, -r)
        v = Fr(2 * r)
        e = "(x − %s)(x + %s)/(x − %s) = x + %s → <b>%s</b>." % (fq(r), fq(r), fq(r), fq(r), fq(v)) if r > 0 else "Scompongo il numeratore, semplifico il fattore che si annulla e sostituisco: <b>%s</b>." % fq(v)
    else:
        num = P2(1, -(r + s_), r * s_)
        den = P2(0, 1, -r)
        v = Fr(r - s_)
        e = "Scompongo: (x − %s)(x − %s)/(x − %s) = x − %s → %s − %s = <b>%s</b>." % (fq(r), fq(s_), fq(r), fq(s_), fq(r), fq(s_), fq(v)) if s_ >= 0 and r > 0 else "Scompongo il numeratore, semplifico il fattore (%s) e sostituisco: <b>%s</b>." % (("x − %s" % fq(r)) if r > 0 else ("x + %s" % fq(-r)), fq(v))
    return M("Calcola %s." % lim(fq(r), FR(num, den)), fq(v), [x for x in W("0", "1", PINF, fq(v + 1), fq(-v) if v else "2") if x != fq(v)][:4], e)


def s1_razion():
    a = R.randint(1, 6)
    v = Fr(1, 2 * a)
    return M("Calcola %s." % lim("0", FR("√(x + %d) − %d" % (a * a, a), "x")), fq(v), [fq(x) for x in W(Fr(1, a), 0, Fr(a, 2), 2 * a) if x != v],
             "Forma 0/0: moltiplico per √(x + %d) + %d: x / [x(√(x + %d) + %d)] → 1/(%d + %d) = <b>%s</b>." % (a * a, a, a * a, a, a, a, fq(v)))


def s2_inf():
    b = nz(R, -8, 8)
    k = R.choice(["rad", "poly"])
    if k == "rad":
        v = Fr(b, 2)
        return M("Calcola %s." % lim(PINF, "(√(%s) − x)" % P2(1, b, 0)), fq(v), [x for x in W("0", fq(b), PINF, fq(Fr(b, 4))) if x != fq(v)],
                 "Forma ∞ − ∞: razionalizzo, %sx/(√(x² %s %dx) + x) → %s/2 = <b>%s</b>." % (fq(b) if abs(b) != 1 else ("" if b == 1 else "−"), "+" if b > 0 else "−", abs(b), fq(b), fq(v)))
    a, c = nz(R, -4, 4), R.randint(-5, 5)
    n = R.randint(3, 5)
    sgn = 1 if a > 0 else -1
    v = PINF if sgn > 0 else MINF
    coef = "" if a == 1 else ("−" if a == -1 else fq(a))
    f = "(%sx<sup>%d</sup> − %dx²)" % (coef, n, abs(c) + 1)
    return M("Calcola %s." % lim(PINF, f), v, [x for x in [PINF, MINF, "0", "forma indeterminata"] if x != v][:3],
             "Forma ∞ − ∞: raccolgo x<sup>%d</sup>, la parentesi tende a %s: <b>%s</b>." % (n, fq(a), v))


GER = [("ln x / x", PINF, "0", "il logaritmo è un infinito di ordine inferiore a ogni potenza"),
       ("x<sup>3</sup> / e<sup>x</sup>", PINF, "0", "l’esponenziale è un infinito di ordine superiore a ogni potenza"),
       ("e<sup>x</sup> / x<sup>2</sup>", PINF, PINF, "l’esponenziale cresce più di ogni potenza"),
       ("x / ln x", PINF, PINF, "la potenza cresce più del logaritmo"),
       ("x e<sup>−x</sup>", PINF, "0", "e<sup>−x</sup> tende a 0 più velocemente di quanto x cresca"),
       ("x ln x", "0<sup>+</sup>", "0", "la potenza vince sul logaritmo anche in 0⁺"),
       ("(ln x)<sup>2</sup> / √x", PINF, "0", "ogni potenza del logaritmo è trascurabile rispetto a una potenza di x"),
       ("e<sup>2x</sup> / e<sup>x</sup>", PINF, PINF, "si semplifica: e<sup>x</sup> → +∞"),
       ("(x<sup>2</sup> + 1) / (3x<sup>2</sup> − x)", PINF, FR(1, 3), "stesso grado: rapporto dei coefficienti direttivi")]


def s3_ger():
    f, x0, v, e = R.choice(GER)
    return M("Calcola %s." % lim(x0, f), v, [x for x in [PINF, "0", "1", MINF, FR(1, 3)] if x != v][:3], "Forma indeterminata: %s, quindi <b>%s</b>." % (e, v))


def s4_not():
    k = R.choice(["sen", "senab", "cos", "exp", "ln", "tg"])
    a = R.randint(2, 7)
    b = R.randint(2, 7)
    if k == "sen":
        v = Fr(a)
        return M("Calcola %s." % lim("0", FR("sen %dx" % a, "x")), fq(v), [fq(x) for x in W(1, Fr(1, a), 0, a * a) if x != v],
                 "sen %dx/x = %d · sen %dx/(%dx) → %d · 1 = <b>%d</b>." % (a, a, a, a, a, a))
    if k == "senab":
        if a == b:
            return None
        v = Fr(a, b)
        return M("Calcola %s." % lim("0", FR("sen %dx" % a, "sen %dx" % b)), fq(v), [fq(x) for x in W(1, Fr(b, a), 0, a * b) if x != v],
                 "Moltiplico e divido per %dx e %dx: (sen %dx/%dx) · (%dx/sen %dx) · %d/%d → <b>%s</b>." % (a, b, a, a, b, b, a, b, fq(v)))
    if k == "cos":
        v = Fr(a * a, 2)
        return M("Calcola %s." % lim("0", FR("1 − cos %dx" % a, "x²")), fq(v), [fq(x) for x in W(Fr(1, 2), a * a, Fr(a, 2), 0) if x != v],
                 "(1 − cos t)/t² → 1/2 con t = %dx: %d²/2 = <b>%s</b>." % (a, a, fq(v)))
    if k == "exp":
        v = Fr(a)
        return M("Calcola %s." % lim("0", FR("e<sup>%dx</sup> − 1" % a, "x")), fq(v), [fq(x) for x in W(1, 0, Fr(1, a), a * a) if x != v] + ["e<sup>%d</sup>" % a],
                 "(e<sup>t</sup> − 1)/t → 1 con t = %dx: <b>%d</b>." % (a, a))
    if k == "ln":
        if a == b:
            return None
        v = Fr(a, b)
        return M("Calcola %s." % lim("0", FR("ln(1 + %dx)" % a, "%dx" % b)), fq(v), [fq(x) for x in W(1, Fr(b, a), 0, a) if x != v],
                 "ln(1 + t)/t → 1 con t = %dx: %d/%d = <b>%s</b>." % (a, a, b, fq(v)))
    v = Fr(a)
    return M("Calcola %s." % lim("0", FR("tg %dx" % a, "x")), fq(v), [fq(x) for x in W(1, 0, Fr(1, a), PINF) if x != v],
             "tg t/t → 1 con t = %dx: <b>%d</b>." % (a, a))


def s5_e():
    k = Fr(R.choice([1, 2, 3, -1, -2, 4, -3]))
    m = R.choice([1, 1, 2, 3])
    km = k * m
    ex = lambda t: "e" if t == 1 else "e<sup>%s</sup>" % fq(t).replace("<span class='fr'><span class='fn'>", "").replace("</span><span class='fd'>", "/").replace("</span></span>", "")
    v = ex(km)
    base = "(1 %s %s/x)" % ("+" if k > 0 else "−", fq(abs(k)))
    expo = "x" if m == 1 else "%dx" % m
    return M("Calcola %s." % lim(PINF, "%s<sup>%s</sup>" % (base, expo)), v, [x for x in W("1", PINF, ex(k) if m != 1 else ex(km + 1), ex(-km), "0") if x != v][:3],
             "Forma 1<sup>∞</sup>: (1 + k/x)<sup>x</sup> → e<sup>k</sup>; con l’esponente %s si ottiene e<sup>k · %d</sup> = <b>%s</b>." % (expo, m, v))


def main():
    seen = set()
    sets = [
        ("Forma 0/0", mix(R, seen, [(s1_scomp, 14), (s1_razion, 6)])),
        ("Forme ∞ − ∞ e ∞/∞", mix(R, seen, [(s2_inf, 12), (s3_ger, 8)])),
        ("Limiti notevoli", mix(R, seen, [(s4_not, 20)])),
        ("Il numero e", mix(R, seen, [(s5_e, 10), (s4_not, 10)])),
        ("Riepilogo", mix(R, seen, [(s1_scomp, 7), (s3_ger, 1), (s4_not, 6), (s2_inf, 6)])),
    ]
    body = L(["Le <b>forme indeterminate</b> si risolvono trasformando l’espressione. Con 0/0 tra polinomi si <b>scompone</b> e si semplifica il fattore che si annulla; con le radici si <b>razionalizza</b>.",
              "Con ∞ − ∞ si raccoglie il termine di grado massimo o si razionalizza. Con ∞/∞ vale la <b>gerarchia degli infiniti</b>: ln x ≪ x<sup>n</sup> ≪ e<sup>x</sup>.",
              "<b>Limiti notevoli</b> (x → 0): sen x/x → 1; (1 − cos x)/x² → 1/2; (eˣ − 1)/x → 1; ln(1 + x)/x → 1. Valgono anche con kx al posto di x.",
              "Per x → +∞: (1 + 1/x)ˣ → e e (1 + k/x)ˣ → e<sup>k</sup>."],
             [("lim<sub>x→2</sub> (x² − 4)/(x − 2)", ["(x − 2)(x + 2)/(x − 2) = x + 2"], "4"),
              ("lim<sub>x→0</sub> sen 5x/x", ["5 · sen 5x/(5x)"], "5")],
             [["0/0 = 1", "È indeterminata: il risultato dipende dalle funzioni."],
              ["sen 3x/x → 1", "Serve 3x al denominatore: il limite è 3."],
              ["(1 + 1/x)ˣ → 1", "È la forma 1<sup>∞</sup>: il limite è e."]])
    faq = [("Perché sen x/x tende a 1?", "Per angoli piccoli l’arco x e il seno sono quasi uguali: geometricamente sen x &lt; x &lt; tg x, e con il teorema del confronto il rapporto tende a 1."),
           ("Che cosa vuol dire gerarchia degli infiniti?", "Per x → +∞ alcune funzioni crescono molto più in fretta di altre: ogni esponenziale aˣ (a &gt; 1) supera ogni potenza xⁿ, che supera ogni potenza del logaritmo.")]
    unit(G, R, "forme-indeterminate-e-limiti-notevoli", "F",
         "Calcolo dei limiti: forme indeterminate, limiti notevoli, confronto di infiniti",
         "Forme indeterminate e limiti notevoli", "Forme indeterminate e limiti notevoli",
         "Schede di matematica per la quinta liceo sulle forme indeterminate: 0/0 con scomposizione e razionalizzazione, ∞ − ∞, ∞/∞ e gerarchia degli infiniti, limiti notevoli di seno, coseno, esponenziale e logaritmo, il numero e. 100 esercizi con soluzioni.",
         "sen x / x → 1 per x → 0", "(1 + k/x)^x → e^k; ln x ≪ xⁿ ≪ e^x.",
         body, faq, sets, 4)


if __name__ == "__main__":
    main()
