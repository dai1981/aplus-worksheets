# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 1ª série: Logaritmos (EM13MAT305)
  python3 tools/gen_br_matematica_em1_logaritmos.py
Definição log_b a = x ⇔ bˣ = a; logaritmos decimais; propriedades (produto, quociente, potência), mudança de base;
aplicações: pH, escala Richter, decibéis, tempo para dobrar um capital (com log 2 ≈ 0,301, log 3 ≈ 0,477).
Erros: log(a + b) = log a + log b, confundir base e logaritmando, achar que 1 grau a mais na escala Richter é só um pouco mais forte.
"""
import random
from fractions import Fraction as F
from br_em import M, d, fq, par, bank, mix, lesson, unit, num

R = random.Random(91011)
SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def lg(b, a):
    return "log%s %s" % (str(b).translate(SUB), a) if b != 10 else "log %s" % a


def s1_def():
    b = R.choice([2, 3, 4, 5, 10])
    k = R.choice(["pos", "pos", "neg", "frac", "um", "x"])
    if k == "pos":
        x = R.randint(2, 6 if b <= 3 else 4)
        a = b ** x
        if a > 10 ** 6:
            return None
        return M("Quanto vale %s?" % lg(b, num(a)), str(x), [num(a // b), str(x + 1), str(x - 1) if x > 2 else str(b)], "%d%s = %s, então <b>%s = %d</b>." % (b, str(x).translate(SUP), num(a), lg(b, num(a)), x))
    if k == "neg":
        x = R.randint(1, 3)
        return M("Quanto vale %s?" % lg(b, fq(F(1, b ** x))), "−%d" % x, [str(x), fq(F(1, x)), "−%d" % (x + 1)], "%d%s = %s: <b>−%d</b>." % (b, ("-" + str(x)).translate(SUP), fq(F(1, b ** x)), x))
    if k == "frac":
        if b not in (4, 10):
            return None
        a = {4: "2", 10: "√10"}[b]
        return M("Quanto vale %s?" % lg(b, a), fq(F(1, 2)), ["2", "−2", fq(F(1, 4)) if b == 4 else "5"], "%s = %d^(1/2): <b>1/2</b>." % (a, b))
    if k == "um":
        return M("Quanto vale %s + %s?" % (lg(b, "1"), lg(b, str(b))), "1", ["0", str(b), "2"], "%s = 0 e %s = 1: <b>1</b>." % (lg(b, "1"), lg(b, str(b))))
    x = R.randint(2, 4)
    return M("Qual é o valor de x em %s = %d?" % (lg(b, "x"), x), num(b ** x), [str(x * b), num(x ** b) if x ** b < 10 ** 6 and x ** b != b ** x else str(x + b), num(b ** (x + 1))],
             "x = %d%s = <b>%s</b>." % (b, str(x).translate(SUP), num(b ** x)))


L2, L3 = F(301, 1000), F(477, 1000)


def s2_prop():
    k = R.choice(["num", "num", "expand", "regra", "mudanca"])
    if k == "num":
        m2, m3, m10 = R.randint(0, 3), R.randint(0, 2), R.randint(-1, 2)
        if m2 + m3 == 0:
            return None
        n = F(2) ** m2 * F(3) ** m3 * F(10) ** m10
        v = m2 * L2 + m3 * L3 + m10
        txt = num(n) if n.denominator == 1 else d(n)
        return M("Usando log 2 = 0,301 e log 3 = 0,477, calcule log %s." % txt, d(v), [d(m2 * L2 * m3 * L3 + m10) if m3 and m2 else d(v + 1), d(v - m10) if m10 else d(v * 2), d(m2 * L3 + m3 * L2 + m10) if m2 != m3 else d(v + F(1, 10))],
                 "%s = %s: log = %s = <b>%s</b>." % (txt, " · ".join(["2"] * m2 + ["3"] * m3 + (["10"] * m10 if m10 > 0 else [])) + (" ÷ 10" * (-m10)), " + ".join([d(L2)] * m2 + [d(L3)] * m3) + ((" + %d" % m10) if m10 > 0 else (" − %d" % -m10 if m10 < 0 else "")), d(v)))
    if k == "expand":
        p = R.randint(2, 4)
        return M("Pelas propriedades dos logaritmos, log (a%s · b) é igual a…" % str(p).translate(SUP), "%d log a + log b" % p, ["log a + %d log b" % p, "%d(log a + log b)" % p, "%d log a · log b" % p],
                 "log(a%s · b) = log a%s + log b = <b>%d log a + log b</b>." % (str(p).translate(SUP), str(p).translate(SUP), p))
    if k == "regra":
        q, a, w = R.choice([("log (a · b) = …", "log a + log b", ["log a · log b", "log (a + b)", "log a − log b"]),
                            ("log (a ÷ b) = …", "log a − log b", ["log a ÷ log b", "log (a − b)", "log b − log a"]),
                            ("log aⁿ = …", "n · log a", ["(log a)ⁿ", "log a + n", "log (n · a)"]),
                            ("log₂ 8 + log₂ 4 = …", "5", ["12", "32", "log₂ 12"]),
                            ("log 50 + log 2 = …", "2", ["log 52", "100", "1"]),
                            ("log₃ 54 − log₃ 2 = …", "3", ["27", "log₃ 52", "1"])])
        return M(q, a, w, "Resposta: <b>%s</b>." % a)
    b, a2, v = R.choice([(4, 8, F(3, 2)), (8, 4, F(2, 3)), (9, 27, F(3, 2)), (4, 2, F(1, 2)), (25, 125, F(3, 2)), (27, 9, F(2, 3)), (16, 8, F(3, 4)), (8, 16, F(4, 3))])
    base = 2 if b in (4, 8, 16) else (3 if b in (9, 27) else 5)
    return M("Usando a mudança de base, calcule %s." % lg(b, a2), fq(v), [fq(1 / v), fq(F(a2, b)), fq(v + 1)], "%s = %s ÷ %s: <b>%s</b>." % (lg(b, a2), lg(base, a2), lg(base, b), fq(v)))


def s3_aplic():
    k = R.choice(["ph", "ph2", "richter", "db", "dobrar"])
    if k == "ph":
        n = R.randint(2, 12)
        return M("O pH é dado por pH = −log [H⁺]. Qual é o pH de uma solução com [H⁺] = 10%s mol/L?" % ("-" + str(n)).translate(SUP), str(n), ["−%d" % n, str(14 - n) if 14 - n != n else str(n + 1), str(n * 10)],
                 "−log 10%s = −(−%d) = <b>%d</b>." % (("-" + str(n)).translate(SUP), n, n))
    if k == "ph2":
        a, b = sorted(R.sample(range(2, 9), 2))
        return M("Uma solução A tem pH %d e uma solução B tem pH %d. Quantas vezes a concentração de H⁺ de A é maior que a de B?" % (a, b), num(10 ** (b - a)), [str(b - a), num(10 * (b - a)), num(10 ** (b - a - 1)) if b - a > 1 else "100"],
                 "Cada unidade de pH é um fator 10: 10%s = <b>%s</b>." % (str(b - a).translate(SUP), num(10 ** (b - a))))
    if k == "richter":
        a = R.randint(3, 6)
        k2 = R.randint(1, 3)
        return M("Na escala Richter, cada ponto a mais corresponde a uma amplitude 10 vezes maior. Um terremoto de magnitude %d tem amplitude quantas vezes maior que um de magnitude %d?" % (a + k2, a), num(10 ** k2), [str(k2), num(10 * k2), num(2 ** k2)],
                 "10%s = <b>%s</b>." % (str(k2).translate(SUP), num(10 ** k2)))
    if k == "db":
        n = R.randint(2, 4)
        return M("O nível sonoro é N = 10 · log (I ÷ I₀), em decibéis. Se I = 10%s · I₀, qual é o nível sonoro?" % str(n * 2).translate(SUP), "%d dB" % (20 * n), ["%d dB" % (2 * n), "%d dB" % (10 * n), "%s dB" % num(10 ** (2 * n))],
                 "10 · log 10%s = 10 · %d = <b>%d dB</b>." % (str(2 * n).translate(SUP), 2 * n, 20 * n))
    i = R.choice([10, 20, 5])
    # tempo para dobrar: 2 = (1 + i)^t ⇒ t = log 2 / log(1 + i)
    if i == 10:
        return M("Um capital rende 10% ao ano (juros compostos). Usando log 2 = 0,301 e log 1,1 = 0,041, em quanto tempo ele dobra, aproximadamente?", "cerca de 7,3 anos", ["cerca de 10 anos", "cerca de 20 anos", "cerca de 2 anos"], "1,1ᵗ = 2 ⇒ t = 0,301 ÷ 0,041 ≈ <b>7,3 anos</b>.")
    if i == 20:
        return M("Um capital rende 20% ao ano (juros compostos). Usando log 2 = 0,301 e log 1,2 = 0,079, em quanto tempo ele dobra, aproximadamente?", "cerca de 3,8 anos", ["cerca de 5 anos", "cerca de 10 anos", "cerca de 2 anos"], "1,2ᵗ = 2 ⇒ t = 0,301 ÷ 0,079 ≈ <b>3,8 anos</b>.")
    return M("Uma população cresce 5% ao ano. Usando log 2 = 0,301 e log 1,05 = 0,021, em quanto tempo ela dobra, aproximadamente?", "cerca de 14 anos", ["cerca de 20 anos", "cerca de 10 anos", "cerca de 40 anos"], "1,05ᵗ = 2 ⇒ t = 0,301 ÷ 0,021 ≈ <b>14 anos</b>.")


s4_conceitos = bank(R, [
    ("log₂ 32 = 5 porque…", "2⁵ = 32", ["5² = 32", "32 ÷ 2 = 5", "2 · 5 = 32"]),
    ("O logaritmo de 1 em qualquer base é…", "0", ["1", "a própria base", "não existe"]),
    ("O logaritmo de um número negativo, nos reais,…", "não existe", ["é negativo", "é zero", "é igual ao do número positivo"]),
    ("log (a + b) é igual a log a + log b?", "não; log a + log b = log (a · b)", ["sim, sempre", "sim, se a = b", "não; é log a · log b"]),
    ("Quando não se escreve a base, o logaritmo é…", "decimal (base 10)", ["de base 2", "de base e", "de base 1"]),
    ("Se log x = 3, então x é…", "1.000", ["30", "3", "300"]),
    ("Na escala de pH, a solução com pH 3 é ___ que a de pH 5.", "100 vezes mais ácida", ["2 vezes mais ácida", "menos ácida", "igualmente ácida"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Definição de logaritmo", mix(R, seen, [(s1_def, 20)])),
        ("Definição e conceitos", mix(R, seen, [(s1_def, 13), (s4_conceitos, 7)])),
        ("Propriedades", mix(R, seen, [(s2_prop, 20)])),
        ("pH, terremotos e som", mix(R, seen, [(s3_aplic, 20)])),
        ("Revisão", mix(R, seen, [(s2_prop, 10), (s3_aplic, 6), (s1_def, 4)])),
    ]
    body = lesson(
        ["<b>Logaritmo</b>: log_b a = x significa bˣ = a (b &gt; 0, b ≠ 1, a &gt; 0). Ex.: log₂ 8 = 3 porque 2³ = 8.",
         "Sem base escrita, é base 10: log 1.000 = 3.",
         "<b>Propriedades</b>: log (a · b) = log a + log b; log (a ÷ b) = log a − log b; log aⁿ = n · log a. Mudança de base: log_b a = log a ÷ log b.",
         "Escalas logarítmicas (pH, Richter, decibéis): somar 1 na escala é multiplicar a grandeza por 10."],
        [("log 12 com log 2 = 0,301 e log 3 = 0,477", ["12 = 2² · 3", "2 · 0,301 + 0,477"], "1,079"),
         ("pH com [H⁺] = 10⁻⁴", ["−log 10⁻⁴"], "4")],
        [["log (a + b) = log a + log b", "A soma vem do produto: log (a · b)."],
         ["Trocar base e logaritmando", "log₂ 8: a base é 2."],
         ["Ler a escala como linear", "1 ponto a mais = 10 vezes mais."]])
    faq = [("O que é um logaritmo?", "É o expoente: log_b a é o número ao qual se eleva a base b para obter a. Por exemplo, log₃ 81 = 4 porque 3⁴ = 81."),
           ("O que a BNCC pede?", "Resolver e elaborar problemas com funções logarítmicas nos quais seja necessário compreender e interpretar a variação das grandezas envolvidas, em contextos como os de abalos sísmicos, pH, radioatividade, Matemática Financeira, entre outros (EM13MAT305).")]
    unit(R, "logaritmos", "A", ["EM13MAT305"],
         "Resolver e elaborar problemas com funções logarítmicas nos quais seja necessário compreender e interpretar a variação das grandezas envolvidas, em contextos como os de abalos sísmicos, pH, radioatividade, Matemática Financeira, entre outros",
         "Logaritmos: definição, propriedades e aplicações", "Logaritmos",
         "Atividades de matemática para a 1ª série do Ensino Médio sobre logaritmos: definição, logaritmo decimal, propriedades, mudança de base, pH, escala Richter, decibéis e tempo para dobrar um capital. 100 exercícios com gabarito.",
         "log_b a = x ⇔ bˣ = a", "log (a · b) = log a + log b.",
         body, faq, sets, 11, grade="1-serie")


if __name__ == "__main__":
    main()
