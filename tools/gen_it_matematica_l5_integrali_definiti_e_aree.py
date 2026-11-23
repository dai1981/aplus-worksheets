# -*- coding: utf-8 -*-
"""
Italia Matematica quinta liceo: Integrali definiti e aree (Relazioni e funzioni)
  python3 tools/gen_it_matematica_l5_integrali_definiti_e_aree.py
Integrale definito e formula di Newton-Leibniz, proprietà (additività, segno), area tra una curva e l’asse x,
area tra due curve, teorema fondamentale del calcolo integrale, valor medio, volume di un solido di rotazione.
Errori: integrale negativo preso come area, sottrarre F(a) − F(b), dimenticare π nel volume.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, W, fq, nz, FR, poly, kurve, relabel

R = random.Random(72511)
G = "quinta-liceo"
BLUE, RED = "#1f6fd1", "#d1452f"


def ev(cs, x):
    v = 0
    for c in cs:
        v = v * x + c
    return v


def prim(cs):
    n = len(cs) - 1
    return [Fr(c, n - i + 1) for i, c in enumerate(cs)] + [0]


def Int(a, b, f):
    return "∫<sub>%s</sub><sup>%s</sup> %s dx" % (a, b, f)


def s1_poly():
    n = R.randint(1, 3)
    cs = [nz(R, -4, 4)] + [R.randint(-5, 5) for _ in range(n)]
    a = R.randint(-2, 1)
    b = a + R.randint(1, 3)
    F = prim(cs)
    v = ev(F, b) - ev(F, a)
    return M("Calcola %s." % Int(fq(a), fq(b), "(%s)" % poly(cs)), fq(v), [fq(x) for x in W(-v, ev(F, b), ev(F, b) + ev(F, a), ev(cs, b) - ev(cs, a), v + 1) if x != v][:3],
             "Una primitiva è F(x) = %s; F(%s) − F(%s) = %s − %s = <b>%s</b>." % (poly(F), fq(b), fq(a), fq(ev(F, b)), "(%s)" % fq(ev(F, a)) if ev(F, a) < 0 else fq(ev(F, a)), fq(v)))


def s2_trasc():
    k = R.randint(2, 6)
    T = [(Int("0", "π", "sen x"), "2", ["0", "−2", "1"], "[−cos x] da 0 a π: −cos π + cos 0 = 1 + 1."),
         (Int("0", "π/2", "cos x"), "1", ["0", "−1", "π/2"], "[sen x] da 0 a π/2: 1 − 0."),
         (Int("1", "e", FR("1", "x")), "1", ["e − 1", "0", FR("1", "e")], "[ln x] da 1 a e: ln e − ln 1 = 1."),
         (Int("0", "ln %d" % k, "e<sup>x</sup>"), str(k - 1), [str(k), "ln %d" % k, str(k + 1)], "[eˣ] da 0 a ln %d: %d − 1." % (k, k)),
         (Int("1", "e<sup>%d</sup>" % k, FR("1", "x")), str(k), ["e<sup>%d</sup> − 1" % k, str(k - 1), "e<sup>%d</sup>" % k], "[ln x] da 1 a e<sup>%d</sup>: %d − 0." % (k, k)),
         (Int("0", "π", "cos x"), "0", ["2", "1", "−2"], "[sen x] da 0 a π: sen π − sen 0 = 0 (le aree sopra e sotto l’asse si compensano)."),
         (Int("0", "1", FR("1", "1 + x²")), FR("π", "4"), [FR("π", "2"), "1", "ln 2"], "[arctg x] da 0 a 1: π/4 − 0."),
         (Int("0", "%d" % k, "%d" % k), str(k * k), [str(k), str(2 * k), str(k * k * k)], "L’integrale di una costante è base × altezza: %d · %d." % (k, k)),
         (Int("0", "π", "x"), FR("π²", "2"), ["π", FR("π", "2"), "π²"], "[x²/2] da 0 a π."),
         (Int("1", "%d" % k, FR("1", "x²")), fq(Fr(k - 1, k)), [x for x in W(fq(Fr(1, k)), fq(Fr(k - 1)), fq(Fr(1, k * k)), fq(Fr(k + 1, k)), "−" + fq(Fr(k - 1, k))) if x != fq(Fr(k - 1, k))][:3], "[−1/x] da 1 a %d: −1/%d + 1." % (k, k))]
    f, a, w, e = R.choice(T)
    return M("Calcola %s." % f, a, w, e + " <b>%s</b>." % a)


def s3_area():
    r1 = R.randint(-4, 1)
    r2 = r1 + R.choice([1, 2, 3, 4, 6])
    k = R.choice([1, -1, 2, -2, 3])
    cs = [k, -k * (r1 + r2), k * r1 * r2]
    A = Fr(abs(k) * (r2 - r1) ** 3, 6)
    fig = relabel(kurve([(lambda x: ev(cs, x), BLUE, "")], (min(r1, 0) - 1, max(r2, 0) + 1, 1), (-max(8, int(abs(k) * (r2 - r1) ** 2 / 4) + 2), max(8, int(abs(k) * (r2 - r1) ** 2 / 4) + 2), 2), W=300, H=260), "grafico della parabola")
    if abs(k) * (r2 - r1) ** 2 / 4 > 12:
        fig = ""
    sgn = -1 if k > 0 else 1
    return M("%sCalcola l’area della regione compresa tra la parabola y = %s e l’asse x." % (fig, poly(cs)), fq(A),
             [fq(x) for x in W(-A, A * 2, Fr(abs(k) * (r2 - r1) ** 3, 3), Fr(abs(k) * (r2 - r1) ** 2, 2), A + 1, A / 2, A * 3) if x != A and x > 0][:3],
             "La parabola taglia l’asse x in %s e %s; tra le radici è %s l’asse, quindi l’area è |∫<sub>%s</sub><sup>%s</sup> f(x) dx| = <b>%s</b>." % (fq(r1), fq(r2), "sotto" if sgn < 0 else "sopra", fq(r1), fq(r2), fq(A)))


def s3_segno():
    a = R.randint(1, 4)
    # ∫ da −a a a di x dx = 0, ma l’area è a²
    T = R.choice(["lin", "cub"])
    if T == "lin":
        return M("Quanto vale l’area della regione tra y = x e l’asse x per −%d ≤ x ≤ %d?" % (a, a), fq(Fr(a * a)), [x for x in W("0", fq(Fr(a * a, 2)), fq(Fr(2 * a)), fq(Fr(2 * a * a))) if x != fq(Fr(a * a))][:3],
                 "∫<sub>−%d</sub><sup>%d</sup> x dx = 0 perché le due parti si compensano, ma l’area è la somma: 2 · %d²/2 = <b>%d</b>." % (a, a, a, a * a))
    return M("Quanto vale ∫<sub>−%d</sub><sup>%d</sup> x³ dx?" % (a, a), "0", W(fq(Fr(a ** 4, 2)), fq(Fr(a ** 4, 4)), fq(Fr(2 * a ** 3)), fq(Fr(a ** 4)))[:3],
             "x³ è dispari e l’intervallo è simmetrico: le aree sopra e sotto l’asse si compensano, <b>0</b>.")


def s4_due():
    kind = R.choice(["xm", "c2", "lin", "pp"])
    if kind == "xm":
        m = R.randint(1, 6)
        A = Fr(m ** 3, 6)
        return M("Calcola l’area della regione compresa tra la parabola y = x² e la retta y = %sx." % (m if m > 1 else ""), fq(A),
                 [fq(x) for x in W(Fr(m ** 3, 2), Fr(m ** 3, 3), Fr(m ** 2, 2), A * 2, A + 1, Fr(m ** 3, 4)) if x != A][:3],
                 "Le curve si incontrano in x = 0 e x = %d; ∫<sub>0</sub><sup>%d</sup> (%sx − x²) dx = %s − %s = <b>%s</b>." % (m, m, m if m > 1 else "", fq(Fr(m ** 3, 2)), fq(Fr(m ** 3, 3)), fq(A)))
    if kind == "c2":
        c = R.randint(1, 4)
        A = Fr(4 * c ** 3, 3)
        return M("Calcola l’area della regione compresa tra la parabola y = x² e la retta y = %d." % (c * c), fq(A),
                 [fq(x) for x in W(Fr(2 * c ** 3, 3), Fr(2 * c ** 3), Fr(c ** 3, 3), Fr(8 * c ** 3, 3)) if x != A][:3],
                 "Si incontrano in x = ±%d; ∫<sub>−%d</sub><sup>%d</sup> (%d − x²) dx = %s − %s = <b>%s</b>." % (c, c, c, c * c, fq(Fr(2 * c ** 3)), fq(Fr(2 * c ** 3, 3)), fq(A)))
    if kind == "pp":
        c = R.randint(1, 3)
        # y = x² e y = 2c² − x²: si incontrano in ±c, area = ∫ (2c² − 2x²) = 8c³/3
        A = Fr(8 * c ** 3, 3)
        return M("Calcola l’area della regione compresa tra le parabole y = x² e y = %d − x²." % (2 * c * c), fq(A),
                 [fq(x) for x in W(Fr(4 * c ** 3, 3), Fr(4 * c ** 3), Fr(8 * c ** 3), Fr(2 * c ** 3, 3)) if x != A][:3],
                 "x² = %d − x² per x = ±%d; ∫<sub>−%d</sub><sup>%d</sup> (%d − 2x²) dx = <b>%s</b>." % (2 * c * c, c, c, c, 2 * c * c, fq(A)))
    # y = x e y = x² + k? area tra retta y = mx + q e asse x da 0 a b
    m, q = R.randint(1, 3), R.randint(1, 4)
    b = R.randint(1, 4)
    A = Fr(m * b * b, 2) + q * b
    return M("Calcola l’area del trapezio delimitato da y = %s, dall’asse x e dalle rette x = 0 e x = %d." % (poly([m, q]), b), fq(A),
             [fq(x) for x in W(Fr(m * b * b, 2), m * b + q, A * 2, q * b) if x != A][:3],
             "∫<sub>0</sub><sup>%d</sup> (%s) dx = %s + %d = <b>%s</b> (come area del trapezio)." % (b, poly([m, q]), fq(Fr(m * b * b, 2)), q * b, fq(A)))


def s5_fond():
    kind = R.choice(["Fp", "media", "vol", "vol2", "Fp2"])
    if kind == "Fp":
        n = R.randint(2, 4)
        a = R.randint(1, 3)
        x0 = R.randint(1, 3)
        v = x0 ** n + a
        return M("F(x) = ∫<sub>0</sub><sup>x</sup> (%s + %d) dt. Quanto vale F′(%d)?" % (poly([1] + [0] * n, "t"), a, x0), str(v), [fq(x) for x in W(Fr(x0 ** (n + 1), n + 1) + a * x0, n * x0 ** (n - 1), v + 1, x0 ** n) if x != v][:3],
                 "Per il teorema fondamentale F′(x) = %s + %d, quindi F′(%d) = <b>%d</b>." % (poly([1] + [0] * n), a, x0, v))
    if kind == "Fp2":
        k = R.randint(2, 5)
        return M("F(x) = ∫<sub>1</sub><sup>x</sup> e<sup>%dt</sup> dt. Qual è F′(x)?" % k, "e<sup>%dx</sup>" % k, ["%d e<sup>%dx</sup>" % (k, k), "e<sup>%dx</sup> − e<sup>%d</sup>" % (k, k), FR("e<sup>%dx</sup>" % k, str(k))],
                 "Teorema fondamentale del calcolo integrale: la derivata della funzione integrale è la funzione integranda calcolata in x: <b>e<sup>%dx</sup></b>." % k)
    if kind == "media":
        a = R.randint(1, 3)
        b = R.randint(1, 4)
        cs = [a, 0, b]
        h = R.randint(1, 3)
        F = prim(cs)
        m = (ev(F, h) - ev(F, 0)) / h
        return M("Qual è il valor medio di f(x) = %s nell’intervallo [0; %d]?" % (poly(cs), h), fq(m), [fq(x) for x in W(ev(F, h), Fr(ev(cs, h) + ev(cs, 0), 2), ev(cs, Fr(h, 2)), m + 1) if x != m][:3],
                 "Valor medio = (1/%d) ∫<sub>0</sub><sup>%d</sup> f(x) dx = %s : %d = <b>%s</b>." % (h, h, fq(ev(F, h)), h, fq(m)))
    if kind == "vol":
        k = R.randint(1, 6)
        v = Fr(k * k, 2)
        return M("Calcola il volume del solido ottenuto ruotando attorno all’asse x il grafico di y = √x per 0 ≤ x ≤ %d." % k, "%sπ" % (fq(v) if v != 1 else ""),
                 ["%s" % fq(v), "%sπ" % fq(Fr(2 * k * k, 3)), "%sπ" % fq(Fr(k * k))],
                 "V = π ∫<sub>0</sub><sup>%d</sup> x dx = π · %d²/2 = <b>%sπ</b>." % (k, k, fq(v)))
    h = R.randint(1, 6)
    r = R.randint(1, 3)
    v = Fr(r * r * h, 3)
    return M("Ruotando attorno all’asse x il segmento y = %sx con 0 ≤ x ≤ %d si ottiene un cono. Quanto vale il volume?" % (fq(Fr(r, h)) if Fr(r, h) != 1 else "", h), "%sπ" % (fq(v) if v != 1 else ""),
             ["%sπ" % fq(Fr(r * r * h)), "%sπ" % fq(Fr(r * r * h, 2)), "%s" % fq(v)],
             "V = π ∫<sub>0</sub><sup>%d</sup> (%sx)² dx = π r² h/3 con r = %d e h = %d: <b>%sπ</b>." % (h, fq(Fr(r, h)) if Fr(r, h) != 1 else "", r, h, fq(v)))


def main():
    seen = set()
    sets = [
        ("Calcolo di integrali definiti", mix(R, seen, [(s1_poly, 20)])),
        ("Integrali definiti di funzioni elementari", mix(R, seen, [(s2_trasc, 10), (s1_poly, 6), (s3_segno, 4)])),
        ("Area tra una curva e l’asse x", mix(R, seen, [(s3_area, 16), (s3_segno, 4)])),
        ("Area tra due curve", mix(R, seen, [(s4_due, 20)])),
        ("Funzione integrale, valor medio e volumi", mix(R, seen, [(s5_fond, 20)])),
    ]
    body = L(["L’<b>integrale definito</b> ∫<sub>a</sub><sup>b</sup> f(x) dx si calcola con una primitiva F: ∫<sub>a</sub><sup>b</sup> f(x) dx = F(b) − F(a) (formula di Newton-Leibniz).",
              "Se f ≥ 0 l’integrale è l’<b>area</b> sotto il grafico; dove f &lt; 0 l’integrale è negativo. Per l’area si integra |f|, spezzando l’intervallo negli zeri di f.",
              "Area tra due curve: ∫<sub>a</sub><sup>b</sup> [g(x) − f(x)] dx, con g sopra f e a, b ascisse dei punti di intersezione.",
              "Teorema fondamentale: se F(x) = ∫<sub>a</sub><sup>x</sup> f(t) dt, allora F′(x) = f(x). Valor medio: (1/(b − a)) ∫<sub>a</sub><sup>b</sup> f(x) dx. Volume di rotazione attorno all’asse x: V = π ∫<sub>a</sub><sup>b</sup> f(x)² dx."],
             [("∫<sub>1</sub><sup>3</sup> 2x dx", ["F(x) = x²", "9 − 1"], "8"),
              ("Area tra y = x² e y = 2x", ["Intersezioni x = 0 e x = 2", "∫<sub>0</sub><sup>2</sup> (2x − x²) dx = 4 − 8/3"], "4/3")],
             [["Calcolare F(a) − F(b)", "L’ordine è F(b) − F(a): estremo superiore meno inferiore."],
              ["Prendere un integrale negativo come area", "L’area è sempre positiva: si prende il valore assoluto."],
              ["Dimenticare π nel volume di rotazione", "V = π ∫ f(x)² dx."]])
    faq = [("Che differenza c’è tra integrale definito e area?", "L’integrale conta con segno negativo le parti sotto l’asse x; l’area le conta tutte con segno positivo."),
           ("Che cosa dice il teorema fondamentale del calcolo integrale?", "Che la funzione integrale F(x) = ∫<sub>a</sub><sup>x</sup> f(t) dt è una primitiva di f: derivazione e integrazione sono operazioni inverse.")]
    unit(G, R, "integrali-definiti-e-aree", "F",
         "Integrale definito, teorema fondamentale del calcolo integrale, calcolo di aree e volumi",
         "Integrali definiti e aree", "Integrali definiti e aree",
         "Schede di matematica per la quinta liceo sugli integrali definiti: formula di Newton-Leibniz, integrali di funzioni elementari, area tra una curva e l’asse x, area tra due curve, funzione integrale, valor medio, volumi di rotazione. 100 esercizi con soluzioni.",
         "∫ₐᵇ f(x) dx = F(b) − F(a)", "L’area si calcola con |f| tra le intersezioni.",
         body, faq, sets, 11)


if __name__ == "__main__":
    main()
