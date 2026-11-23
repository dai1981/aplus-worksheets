# -*- coding: utf-8 -*-
"""
Brasil Matemática 8º ano: Potências e notação científica (Números, EF08MA01)
  python3 tools/gen_br_matematica_8_potencias_e_notacao_cientifica.py
Potências de expoente natural e inteiro (zero e negativo); base negativa; propriedades (produto e quociente de mesma base,
potência de potência); potências de 10; notação científica de números grandes e pequenos; comparar e operar.
Usa geradores do 9º ano (potências e notação científica) com outro sorteio.
Erros: 2³ = 6, 2⁻³ negativo, (−2)⁴ negativo, 3,4 × 10⁵ escrito com zeros a mais.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, use
from br_9 import M, d, fq, unit

R = random.Random(88001)
p_prop, p_neg = use("gen_br_matematica_9_potencias_e_radicais", 88901, "s1_prop", "s2_neg")
n_grande, n_peq, n_volta, n_ctx = use("gen_br_matematica_9_notacao_cientifica", 88902, "s1_grande", "s1_pequeno", "s2_voltar", "s5_ctx")
SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def pw(b, e):
    bs = "(%s)" % d(b) if (isinstance(b, int) and b < 0) or (isinstance(b, F) and b < 0) else (fq(b) if isinstance(b, F) and b.denominator > 1 else d(b))
    if isinstance(b, F) and b.denominator > 1:
        bs = "(%s)" % bs
    return bs + str(e).translate(SUP)


def s1_calcular():
    k = R.choice(["nat", "neg_base", "zero", "fr"])
    if k == "nat":
        b, e = R.choice([(2, R.randint(3, 10)), (3, R.randint(2, 5)), (4, R.randint(2, 4)), (5, R.randint(2, 4)), (10, R.randint(2, 6)), (R.randint(6, 12), 2)])
        return M("Quanto é %s?" % pw(b, e), d(b ** e), [d(b * e), d(b ** (e - 1)), d(e ** b) if e ** b != b ** e and e ** b < 10 ** 7 else d(b ** e + b)], "%s = %s (%d fatores iguais a %d) = <b>%s</b>." % (pw(b, e), " × ".join([str(b)] * e) if e <= 6 else "…", e, b, d(b ** e)))
    if k == "neg_base":
        b, e = R.randint(-5, -2), R.randint(2, 5)
        return M("Quanto é %s?" % pw(b, e), d(b ** e), [d(-(b ** e)), d(b * e), d(abs(b) * e)], "Base negativa: expoente %s dá resultado %s. <b>%s</b>." % ("par" if e % 2 == 0 else "ímpar", "positivo" if e % 2 == 0 else "negativo", d(b ** e)))
    if k == "zero":
        b = R.choice([7, 15, 100, 2026, -9])
        return M("Quanto é %s?" % pw(b, 0), "1", ["0", d(b), d(-b) if b else "−1"], "Todo número diferente de zero elevado a 0 dá <b>1</b>.")
    b = F(R.randint(1, 4), R.randint(2, 5))
    if b.denominator == 1:
        return None
    e = R.randint(2, 3)
    return M("Quanto é %s?" % pw(b, e), fq(b ** e), [fq(F(b.numerator * e, b.denominator * e)), fq(F(b.numerator ** e, b.denominator)), fq(F(b.numerator, b.denominator ** e))], "Eleve o numerador e o denominador: <b>%s</b>." % fq(b ** e))


def s2_dez():
    e = R.randint(-6, 9)
    k = R.choice(["valor", "exp"])
    v = F(10) ** e
    if k == "valor":
        return M("Quanto é 10%s?" % str(e).translate(SUP), d(v, 6) if e < 0 else d(v), [d(F(10) ** -e, 6) if -e < 0 else d(F(10) ** -e), d(v * 10, 7) if e < 0 else d(v * 10), d(-abs(10 * e)) if e < 0 else d(10 * e)],
                 "%s = <b>%s</b>%s." % ("10" + str(e).translate(SUP), d(v, 6) if e < 0 else d(v), " (1 dividido por 10%s)" % str(-e).translate(SUP) if e < 0 else ""))
    return M("Escreva %s como potência de 10." % (d(v, 6) if e < 0 else d(v)), "10" + str(e).translate(SUP), ["10" + str(-e).translate(SUP) if e else "10¹", "10" + str(e + 1).translate(SUP), "10" + str(e - 1).translate(SUP)],
             "Conte as casas: <b>10%s</b>." % str(e).translate(SUP))


def main():
    seen = set()
    sets = [
        ("Calcular potências", mix(R, seen, [(s1_calcular, 20)])),
        ("Potências de 10 e expoente negativo", mix(R, seen, [(s2_dez, 12), (p_neg, 8)])),
        ("Propriedades das potências", mix(R, seen, [(p_prop, 20)])),
        ("Notação científica", mix(R, seen, [(n_grande, 8), (n_peq, 8), (n_volta, 4)])),
        ("Notação científica no dia a dia", mix(R, seen, [(n_ctx, 8), (n_volta, 6), (s2_dez, 6)])),
    ]
    body = lesson(
        ["Uma <b>potência</b> é uma multiplicação de fatores iguais: 2⁵ = 2 × 2 × 2 × 2 × 2 = 32.",
         "a⁰ = 1 (a ≠ 0). Expoente negativo é o inverso: 2⁻³ = 1/2³ = 1/8.",
         "Propriedades: aᵐ · aⁿ = aᵐ⁺ⁿ; aᵐ ÷ aⁿ = aᵐ⁻ⁿ; (aᵐ)ⁿ = aᵐ·ⁿ.",
         "<b>Notação científica</b>: a × 10ⁿ, com 1 ≤ a &lt; 10. Ex.: 3.400.000 = 3,4 × 10⁶; 0,00052 = 5,2 × 10⁻⁴."],
        [("(−2)⁵", ["5 fatores negativos"], "−32"),
         ("0,000 7 em notação científica", ["a vírgula anda 4 casas"], "7 × 10⁻⁴")],
        [["2³ = 6", "2³ = 2 × 2 × 2 = 8."],
         ["Achar que 2⁻³ é negativo", "2⁻³ = 1/8, que é positivo."],
         ["Errar a base negativa", "(−2)⁴ = 16, mas −2⁴ = −16."]])
    faq = [("O que é notação científica?", "É a forma a × 10ⁿ, com a entre 1 e 10 (incluindo o 1). Ela serve para escrever números muito grandes ou muito pequenos de forma curta."),
           ("O que a BNCC pede no 8º ano?", "Efetuar cálculos com potências de expoentes inteiros e aplicar esse conhecimento na representação de números em notação científica (EF08MA01).")]
    unit(R, "potencias-e-notacao-cientifica", "N", ["EF08MA01"],
         "Efetuar cálculos com potências de expoentes inteiros e aplicar esse conhecimento na representação de números em notação científica",
         "Potências de expoente inteiro e notação científica", "Potências e notação científica",
         "Atividades de matemática para o 8º ano sobre potências: expoente natural, zero e negativo, base negativa, propriedades, potências de 10 e notação científica. 100 exercícios com gabarito.",
         "2⁻³ = 1/8", "Notação científica: a × 10ⁿ, com 1 ≤ a < 10.",
         body, faq, sets, 1, grade="8-ano")


if __name__ == "__main__":
    main()
