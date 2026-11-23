# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: Potências e radicais (Números, EF09MA03)
  python3 tools/gen_br_matematica_9_potencias_e_radicais.py
Propriedades das potências (produto, quociente, potência de potência); expoente zero e negativo; expoente fracionário
(a^(1/n) = ⁿ√a); simplificar radicais (√50 = 5√2); somar, multiplicar e dividir radicais; racionalizar denominadores simples.
Erros: multiplicar as bases (2³ · 2⁴ = 4⁷), achar que 2⁻³ é negativo, somar radicandos (√2 + √3 = √5).
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix
from br_9 import M, d, fq, sq, unit

R = random.Random(89002)
SUP = str.maketrans("0123456789−-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁻")


def pw(b, e):
    return "%s%s" % (b, str(e).translate(SUP))


def s1_prop():
    b = R.choice([2, 3, 5, 7, 10, "a", "x"])
    m, n = R.randint(2, 9), R.randint(2, 6)
    k = R.choice(["prod", "quoc", "pot"])
    if k == "prod":
        return M("Simplifique: %s · %s" % (pw(b, m), pw(b, n)), pw(b, m + n), [pw(b, m * n), pw(b, abs(m - n)) if m != n else pw(b, m + n + 1), pw(b if isinstance(b, str) else b * b, m + n)],
                 "Mesma base: some os expoentes. %d + %d = %d: <b>%s</b>." % (m, n, m + n, pw(b, m + n)))
    if k == "quoc":
        if m <= n:
            m, n = n + 1, m
        return M("Simplifique: %s ÷ %s" % (pw(b, m), pw(b, n)), pw(b, m - n), [pw(b, m + n), pw(b, m * n), pw(1, m - n) if not isinstance(b, str) else pw(b, F(m, n).numerator)],
                 "Mesma base: subtraia os expoentes. %d − %d = %d: <b>%s</b>." % (m, n, m - n, pw(b, m - n)))
    m, n = R.randint(2, 5), R.randint(2, 4)
    return M("Simplifique: (%s)%s" % (pw(b, m), str(n).translate(SUP)), pw(b, m * n), [pw(b, m + n), pw(b, m ** n) if m ** n < 100 else pw(b, m * n + 1), pw(b, m * n - 1)],
             "Potência de potência: multiplique os expoentes. %d · %d = %d: <b>%s</b>." % (m, n, m * n, pw(b, m * n)))


def s2_neg():
    b = R.choice([2, 3, 4, 5, 10])
    e = R.randint(1, 3)
    if b ** e > 1000:
        return None
    k = R.choice(["neg", "zero", "frac"])
    if k == "neg":
        v = F(1, b ** e)
        return M("Quanto vale %s?" % pw(b, "−%d" % e), fq(v), [d(-b ** e), d(-b * e), fq(F(1, b * e)) if b * e != b ** e else fq(F(e, b))],
                 "Expoente negativo é o inverso: %s = 1/%s = <b>%s</b>." % (pw(b, "−%d" % e), pw(b, e), fq(v)))
    if k == "zero":
        return M("Quanto vale %s⁰?" % R.choice(["7", "2026", "(−5)", "15", "(1/2)", "0,3", "1000"]), "1", ["0", "o próprio número", "não existe"],
                 "Todo número diferente de zero elevado a 0 dá <b>1</b>.")
    n = R.choice([2, 3])
    base = R.randint(2, 10) ** n
    return M("Quanto vale %s<sup>1/%d</sup>?" % (num_(base), n), str(round(base ** (1 / n))), [str(base // n), num_(base * n), str(round(base ** (1 / n)) + 1)],
             "Expoente 1/%d é raiz %s: %s%s = <b>%d</b>." % (n, "quadrada" if n == 2 else "cúbica", "√" if n == 2 else "∛", num_(base), round(base ** (1 / n))))


def num_(n):
    return d(n)


def s3_simplificar():
    k = R.choice([2, 3, 5, 6, 7])
    a = R.randint(2, 6)
    n = a * a * k
    return M("Simplifique: √%d" % n, "%d√%d" % (a, k), ["%d√%d" % (k, a) if k != a else "%d√%d" % (a + 1, k), "%d√%d" % (a * a, k), "√%d" % (a * k)],
             "%d = %d · %d, e √%d = %d. Então √%d = <b>%d√%d</b>." % (n, a * a, k, a * a, a, n, a, k))


def s3_operar():
    k = R.choice([2, 3, 5, 7])
    a, b = R.randint(1, 9), R.randint(1, 9)
    t = R.choice(["soma", "sub", "mult", "mult2"])
    if t == "soma":
        return M("Calcule: %s√%d + %s√%d" % (a if a > 1 else "", k, b if b > 1 else "", k), "%d√%d" % (a + b, k), ["%d√%d" % (a + b, 2 * k), "%d√%d" % (a * b, k), "√%d" % ((a + b) * k)],
                 "Radicais iguais: some os números de fora. %d + %d = %d: <b>%d√%d</b>." % (a, b, a + b, a + b, k))
    if t == "sub":
        if a <= b:
            a, b = b + 1, a
        return M("Calcule: %d√%d − %s√%d" % (a, k, b if b > 1 else "", k), "%s√%d" % (a - b if a - b > 1 else "", k), ["%d" % (a - b), "%d√%d" % (a + b, k), "%d√%d" % (a - b, 2 * k)],
                 "%d − %d = %d: <b>%s√%d</b>." % (a, b, a - b, a - b if a - b > 1 else "", k))
    if t == "mult":
        p, q = R.sample([2, 3, 5, 6, 7, 10], 2)
        v = sq(p * q)
        return M("Calcule: √%d · √%d" % (p, q), v, ["√%d" % (p + q), sq(p * q * 4) if sq(p * q * 4) != v else "%d" % (p * q), "%d√%d" % (p, q)],
                 "√a · √b = √(a · b) = √%d = <b>%s</b>." % (p * q, v))
    m = R.randint(2, 9)
    return M("Calcule: (√%d)²" % m, str(m), [str(m * m), "2√%d" % m, "√%d" % (2 * m)], "A raiz quadrada e o quadrado se desfazem: <b>%d</b>." % m)


def s4_racionalizar():
    a = R.randint(1, 12)
    k = R.choice([2, 3, 5, 6, 7])
    if a % k == 0:
        g = a // k
        ok = ("%d√%d" % (g, k)) if g > 1 else "√%d" % k
    else:
        ok = "<span class='fr'><span class='fn'>%s√%d</span><span class='fd'>%d</span></span>" % (a if a > 1 else "", k, k)
    return M("Racionalize o denominador: <span class='fr'><span class='fn'>%d</span><span class='fd'>√%d</span></span>" % (a, k), ok,
             ["<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, k), "%d√%d" % (a, k), "<span class='fr'><span class='fn'>√%d</span><span class='fd'>%d</span></span>" % (k, a) if a > 1 else "%d" % k],
             "Multiplique em cima e embaixo por √%d: %d√%d / %d = <b>%s</b>." % (k, a, k, k, ok.replace("<span class='fr'><span class='fn'>", "").replace("</span><span class='fd'>", "/").replace("</span></span>", "")))


def main():
    seen = set()
    sets = [
        ("Propriedades das potências", mix(R, seen, [(s1_prop, 20)])),
        ("Expoente zero, negativo e fracionário", mix(R, seen, [(s2_neg, 20)])),
        ("Simplificar radicais", mix(R, seen, [(s3_simplificar, 20)])),
        ("Operações com radicais", mix(R, seen, [(s3_operar, 20)])),
        ("Racionalizar e revisar", mix(R, seen, [(s4_racionalizar, 12), (s1_prop, 4), (s3_simplificar, 4)])),
    ]
    body = lesson(
        ["Mesma base: na multiplicação <b>some</b> os expoentes; na divisão <b>subtraia</b>; na potência de potência <b>multiplique</b>.",
         "a⁰ = 1 e a⁻ⁿ = 1/aⁿ (o expoente negativo dá o inverso, não um número negativo).",
         "Expoente fracionário é raiz: a<sup>1/2</sup> = √a e a<sup>1/3</sup> = ∛a.",
         "Para simplificar √n, separe um quadrado perfeito: √72 = √(36 · 2) = 6√2. Só some radicais com o mesmo radicando."],
        [("2⁵ · 2³", ["some os expoentes: 5 + 3"], "2⁸"),
         ("√48", ["48 = 16 · 3", "√16 = 4"], "4√3")],
        [["Multiplicar as bases: 2³ · 2⁴ = 4⁷", "A base fica: 2⁷."],
         ["Achar que 2⁻³ é negativo", "2⁻³ = 1/8, positivo."],
         ["Somar radicandos: √2 + √3 = √5", "Radicais diferentes não se juntam."]],
        "<p><b>Resumo:</b> aᵐ · aⁿ = aᵐ⁺ⁿ; aᵐ ÷ aⁿ = aᵐ⁻ⁿ; (aᵐ)ⁿ = aᵐⁿ; √a · √b = √(ab)</p>")
    faq = [("O que é expoente fracionário?", "É outra forma de escrever raízes: a<sup>1/2</sup> = √a e a<sup>m/n</sup> = ⁿ√(aᵐ). A BNCC pede cálculos com números reais, inclusive potências com expoentes fracionários."),
           ("Como simplificar uma raiz?", "Decomponha o número e procure um fator que seja quadrado perfeito: √75 = √(25 · 3) = 5√3.")]
    unit(R, "potencias-e-radicais", "N", ["EF09MA03"],
         "Efetuar cálculos com números reais, inclusive potências com expoentes fracionários",
         "Potências e radicais: propriedades e expoente fracionário", "Potências e radicais",
         "Atividades de matemática para o 9º ano sobre potências e radicais: propriedades, expoente zero, negativo e fracionário, simplificar e operar radicais, racionalizar. 100 exercícios com gabarito.",
         "Mesma base: some, subtraia ou multiplique os expoentes.", "a⁻ⁿ = 1/aⁿ; a^(1/2) = √a.",
         body, faq, sets, 2)


if __name__ == "__main__":
    main()
