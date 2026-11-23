# -*- coding: utf-8 -*-
"""
Italia Matematica quarta liceo: Numeri complessi (Aritmetica e algebra)
  python3 tools/gen_it_matematica_l4_numeri_complessi.py
Unità immaginaria e potenze di i, forma algebrica a + bi, somma, prodotto, coniugato, quoziente, modulo,
equazioni di secondo grado con Δ < 0, forma trigonometrica (modulo e argomento), prodotto in forma trigonometrica e formula di De Moivre.
Errori: i² = 1, (a + bi)(c + di) senza i² = −1, modulo √(a + b), quoziente senza il coniugato.
"""
import math
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, pif, simp_root

R = random.Random(72408)
G = "quarta-liceo"


def cz(a, b):
    a, b = Fr(a), Fr(b)
    if b == 0:
        return fq(a)
    bi = ("" if abs(b) == 1 else fq(abs(b))) + "i"
    if a == 0:
        return ("−" if b < 0 else "") + bi
    return "%s %s %s" % (fq(a), "+" if b > 0 else "−", bi)


def rt(n):
    k, m = simp_root(int(n))
    return str(k) if m == 1 else ("" if k == 1 else str(k)) + "√" + str(m)


def s1_pot():
    n = R.randint(5, 60)
    r = n % 4
    v = ["1", "i", "−1", "−i"][r]
    return M("Calcola i<sup>%d</sup>." % n, v, [x for x in ["1", "i", "−1", "−i"] if x != v],
             "Le potenze di i si ripetono ogni 4: %d = 4 · %d + %d, quindi i<sup>%d</sup> = i<sup>%d</sup> = <b>%s</b>." % (n, n // 4, r, n, r, v))


def s1_ops():
    a, b, c, d_ = [nz(R, -6, 6) for _ in range(4)]
    k = R.choice(["+", "−", "·", "·"])
    if k == "+":
        v = (a + c, b + d_)
        w = [(a + c, b - d_), (a - c, b + d_), (a * c, b * d_)]
    elif k == "−":
        v = (a - c, b - d_)
        w = [(a + c, b + d_), (a - c, b + d_), (a - c, d_ - b), (c - a, d_ - b), (a - c, 1 if b == d_ else 0)]
    else:
        v = (a * c - b * d_, a * d_ + b * c)
        w = [(a * c + b * d_, a * d_ + b * c), (a * c, b * d_), (a * c - b * d_, a * d_ - b * c)]
    ans = cz(*v)
    return M("Calcola: (%s) %s (%s)" % (cz(a, b), k, cz(c, d_)), ans, [cz(*x) for x in w if cz(*x) != ans],
             "%s: <b>%s</b>." % ({"+": "Si sommano parti reali e parti immaginarie", "−": "Si sottraggono parti reali e parti immaginarie", "·": "Proprietà distributiva e i² = −1"}[k], ans))


def s2_coni():
    a, b = nz(R, -8, 8), nz(R, -8, 8)
    k = R.choice(["con", "mod", "prod"])
    if k == "con":
        return M("Qual è il coniugato di %s?" % cz(a, b), cz(a, -b), W(cz(-a, b), cz(-a, -b), cz(b, a) if a != b else cz(a, b + 1), cz(a, -b + 1)),
                 "Il coniugato cambia il segno della parte immaginaria: <b>%s</b>." % cz(a, -b))
    if k == "mod":
        v = rt(a * a + b * b)
        return M("Calcola il modulo di %s." % cz(a, b), v, [x for x in W(str(abs(a) + abs(b)), str(a * a + b * b), rt(abs(a * a - b * b)) if a * a != b * b else "0", rt(a * a + b * b + 1)) if x != v],
                 "|a + bi| = √(a² + b²) = √(%d + %d) = <b>%s</b>." % (a * a, b * b, v))
    return M("Calcola (%s)(%s)." % (cz(a, b), cz(a, -b)), str(a * a + b * b), [str(a * a - b * b), cz(a * a + b * b, 2 * a * b) if False else cz(a * a - b * b, 2 * a * b), str(-(a * a + b * b))],
             "z · z̄ = a² + b² (un numero reale): %d + %d = <b>%d</b>." % (a * a, b * b, a * a + b * b))


def s3_quoz():
    c, d_ = nz(R, -4, 4), nz(R, -4, 4)
    q1, q2 = R.randint(-4, 4), R.randint(-4, 4)
    # (a + bi) = (q1 + q2 i)(c + d i)
    a, b = q1 * c - q2 * d_, q1 * d_ + q2 * c
    if (a, b) == (0, 0) or (q1, q2) == (0, 0):
        return None
    ans = cz(q1, q2)
    n2 = c * c + d_ * d_
    w = [cz(Fr(a, c) if c else 1, Fr(b, d_) if d_ else 1), cz(q1, -q2), cz(Fr(a * c - b * d_, n2), Fr(b * c + a * d_, n2))]
    return M("Calcola: (%s) : (%s)" % (cz(a, b), cz(c, d_)), ans, [x for x in W(*w) if x != ans] + [cz(-q1, q2)],
             "Moltiplico numeratore e denominatore per il coniugato %s; il denominatore diventa %d: <b>%s</b>." % (cz(c, -d_), n2, ans))


def s3_eq():
    k = R.choice(["pura", "compl"])
    if k == "pura":
        n = R.randint(1, 9)
        return M("Risolvi in ℂ: x² + %d = 0" % (n * n), "x = ±%si" % ("" if n == 1 else n), ["x = ±%d" % n, "impossibile", "x = ±%di" % (n * n) if n > 1 else "x = i"],
                 "x² = −%d → x = ±√(−%d) = <b>±%si</b>." % (n * n, n * n, "" if n == 1 else n))
    p, q = nz(R, -5, 5), R.randint(1, 6)
    # x² − 2p x + p² + q² = 0 → p ± qi
    b, c = -2 * p, p * p + q * q
    ans = "x = %s ± %si" % (fq(p), "" if q == 1 else q)
    from it_liceo import P2
    return M("Risolvi in ℂ: %s = 0" % P2(1, b, c), ans, ["x = %s ± %si" % (fq(-p), "" if q == 1 else q), "impossibile", "x = %s ± %s" % (fq(p), q) if q > 1 else "x = %s" % fq(p)],
             "Δ/4 = %d − %d = −%d &lt; 0: x = %s ± √(−%d) = <b>%s</b>." % (p * p, c, q * q, fq(p), q * q, ans))


SPEC = [((1, 1), "√2", Fr(1, 4)), ((1, -1), "√2", Fr(-1, 4)), ((-1, 1), "√2", Fr(3, 4)), ((0, 1), "1", Fr(1, 2)), ((0, -2), "2", Fr(-1, 2)),
        ((-3, 0), "3", Fr(1)), ((2, 0), "2", Fr(0)), ((1, "√3"), "2", Fr(1, 3)), (("√3", 1), "2", Fr(1, 6)), ((-1, "√3"), "2", Fr(2, 3)), ((-1, -1), "√2", Fr(-3, 4)), ((0, 4), "4", Fr(1, 2))]


def s4_trig():
    (a, b), rho, th = R.choice(SPEC)
    th = th % 2
    z = "%s %s %si" % (a, "+" if not str(b).startswith("-") else "−", str(b).lstrip("-") if str(b).lstrip("-") != "1" else "") if a != 0 else ("%si" % (b if b not in (1, -1) else ("" if b == 1 else "−")))
    if b == 0:
        z = str(a).replace("-", "−")
    z = z.replace("-", "−")
    ans = "%s(cos %s + i sen %s)" % (rho, pif(th), pif(th))
    w = ["%s(cos %s + i sen %s)" % (rho, pif(t % 2), pif(t % 2)) for t in W(th + Fr(1, 2), 2 - th if th else Fr(1), Fr(1, 2) - th if (Fr(1, 2) - th) % 2 != th else th + 1, th + 1)]
    return M("Scrivi in forma trigonometrica z = %s." % z, ans, [x for x in w if x != ans],
             "Modulo ρ = √(a² + b²) = %s; argomento θ con cos θ = a/ρ e sen θ = b/ρ: θ = %s. <b>%s</b>." % (rho, pif(th), ans))


def s5_moivre():
    (a, b), rho, th = R.choice([((1, 1), 2, Fr(1, 4)), ((1, -1), 2, Fr(-1, 4)), ((0, 1), 1, Fr(1, 2)), ((-1, 1), 2, Fr(3, 4))])
    n = R.choice([2, 4, 6, 8, 3])
    # (√ρ2)^n where rho given as rho² value
    mod = Fr(rho) ** Fr(n, 2) if rho != 1 else Fr(1)
    ang = (th * n) % 2
    cv, sv = round(math.cos(float(ang) * math.pi)), round(math.sin(float(ang) * math.pi))
    if abs(math.cos(float(ang) * math.pi) - cv) > 1e-9 or abs(math.sin(float(ang) * math.pi) - sv) > 1e-9:
        return None
    if mod.denominator != 1:
        return None
    v = cz(mod * cv, mod * sv)
    z = cz(a, b)
    w = [cz(-mod * cv, -mod * sv) if (cv, sv) != (0, 0) else "0", cz(mod * sv, mod * cv) if cv != sv else cz(mod, 0), cz(Fr(n) * cv if cv else n, Fr(n) * sv)]
    return M("Calcola (%s)<sup>%d</sup> con la formula di De Moivre." % (z, n), v, [x for x in W(*w) if x != v],
             "z = %s(cos %s + i sen %s); zⁿ = ρⁿ(cos nθ + i sen nθ) = %s(cos %s + i sen %s) = <b>%s</b>." % ("√2" if rho == 2 else "1", pif(th), pif(th), fq(mod), pif(th * n), pif(th * n), v))


def main():
    seen = set()
    sets = [
        ("Potenze di i e operazioni", mix(R, seen, [(s1_pot, 8), (s1_ops, 12)])),
        ("Coniugato e modulo", mix(R, seen, [(s2_coni, 14), (s1_ops, 6)])),
        ("Quoziente ed equazioni", mix(R, seen, [(s3_quoz, 12), (s3_eq, 8)])),
        ("Forma trigonometrica", mix(R, seen, [(s4_trig, 10), (s3_eq, 10)])),
        ("Formula di De Moivre", mix(R, seen, [(s5_moivre, 12), (s1_pot, 8)])),
    ]
    body = L(["L’<b>unità immaginaria</b> i ha i² = −1. Un numero complesso si scrive z = a + bi (a parte reale, b parte immaginaria). Le potenze di i si ripetono ogni 4: 1, i, −1, −i.",
              "Si calcola come con i polinomi, sostituendo i² = −1. Il <b>coniugato</b> di a + bi è a − bi; il <b>modulo</b> è |z| = √(a² + b²) e z · z̄ = a² + b².",
              "Per dividere si moltiplicano numeratore e denominatore per il coniugato del denominatore. Le equazioni di secondo grado con Δ &lt; 0 hanno due soluzioni complesse coniugate.",
              "<b>Forma trigonometrica</b>: z = ρ(cos θ + i sen θ). Nel prodotto i moduli si moltiplicano e gli argomenti si sommano; <b>De Moivre</b>: zⁿ = ρⁿ(cos nθ + i sen nθ)."],
             [("(2 + 3i)(1 − i)", ["2 − 2i + 3i − 3i²", "2 + i + 3"], "5 + i"),
              ("x² − 2x + 5 = 0", ["Δ/4 = 1 − 5 = −4"], "x = 1 ± 2i")],
             [["i² = 1", "i² = −1: è la definizione di i."],
              ["|3 + 4i| = 7", "|3 + 4i| = √(9 + 16) = 5."],
              ["Dividere parte per parte", "Si moltiplica per il coniugato del denominatore."]])
    faq = [("A che cosa servono i numeri complessi?", "Permettono di risolvere tutte le equazioni polinomiali (teorema fondamentale dell’algebra) e sono usati in fisica e ingegneria, per esempio per le correnti alternate e le onde."),
           ("Che cosa rappresenta il modulo?", "Nel piano di Gauss (asse x reale, asse y immaginario) il numero a + bi è il punto (a; b): il modulo è la sua distanza dall’origine e l’argomento è l’angolo con il semiasse reale positivo.")]
    unit(G, R, "numeri-complessi", "A",
         "Numeri complessi: forma algebrica e trigonometrica, operazioni, rappresentazione nel piano di Gauss",
         "Numeri complessi", "Numeri complessi",
         "Schede di matematica per la quarta liceo sui numeri complessi: potenze di i, operazioni in forma algebrica, coniugato, modulo, quoziente, equazioni con Δ < 0, forma trigonometrica e formula di De Moivre. 100 esercizi con soluzioni.",
         "i² = −1", "|a + bi| = √(a² + b²); zⁿ = ρⁿ(cos nθ + i sen nθ).",
         body, faq, sets, 8)


if __name__ == "__main__":
    main()
