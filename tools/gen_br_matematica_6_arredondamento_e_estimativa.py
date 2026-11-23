# -*- coding: utf-8 -*-
"""
Brasil Matemática 6º ano: Arredondamento e estimativa (Números, EF06MA12)
  python3 tools/gen_br_matematica_6_arredondamento_e_estimativa.py
Arredondar naturais para a dezena, centena, milhar e milhão mais próximos; arredondar decimais para o inteiro, décimo e centésimo;
estimar somas, diferenças, produtos e quocientes; verificar se uma resposta é razoável.
Erros: olhar o algarismo errado, arredondar «para baixo» quando o algarismo seguinte é 5, mudar as outras ordens sem zerar.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, reais
from br_9 import M, d, bank, unit

R = random.Random(86009)
ORD = [(10, "dezena"), (100, "centena"), (1000, "unidade de milhar"), (10 ** 6, "unidade de milhão")]


def rnd(x, u):
    return int(F(x, u) + F(1, 2)) * u


def s1_naturais():
    u, nm = R.choice(ORD)
    x = R.randint(u * 2, u * 999 if u < 10 ** 6 else u * 99)
    if x % u == 0:
        return None
    r = rnd(x, u)
    dn = x // u * u
    return M("Arredonde %s para a %s mais próxima." % (d(x), nm), d(r), [d(dn if r != dn else dn + u), d(rnd(x, u * 10)) if rnd(x, u * 10) != r else d(r + u), d(rnd(x, u // 10)) if u >= 100 else d(x - x % 10)],
             "Olhe o algarismo à direita da %s: %s 5, então arredonde para %s: <b>%s</b>." % (nm, "é maior ou igual a" if r > dn else "é menor que", "cima" if r > dn else "baixo", d(r)))


def s2_decimais():
    p = R.choice([0, 1, 2])
    x = F(R.randint(10, 99999), 1000)
    u = F(1, 10 ** p)
    r = int(x / u + F(1, 2)) * u
    if r == x or (x * 10 ** p).denominator == 1:
        return None
    nm = {0: "o inteiro mais próximo", 1: "os décimos", 2: "os centésimos"}[p]
    dn = int(x / u) * u
    return M("Arredonde %s para %s." % (d(x), nm), d(r) if p == 0 else d(r, p, keep=True), [d(dn if dn != r else dn + u, p, keep=True) if p else d(dn if dn != r else dn + 1), d(int(x / u * 10 + F(1, 2)) * u / 10, p + 1, keep=True), d(r + u, p, keep=True) if p else d(r + 1)],
             "Olhe a casa seguinte e arredonde: <b>%s</b>." % (d(r) if p == 0 else d(r, p, keep=True)))


def s3_estimar():
    k = R.choice(["+", "−", "×", "÷"])
    if k == "+":
        a, b = R.randint(1000, 9999), R.randint(1000, 9999)
        e = rnd(a, 1000) + rnd(b, 1000)
        return M("Qual é a melhor estimativa para %s + %s (arredonde para o milhar)?" % (d(a), d(b)), d(e), [d(e + 1000), d(e - 1000), d(e * 10)], "%s + %s ≈ <b>%s</b>." % (d(rnd(a, 1000)), d(rnd(b, 1000)), d(e)))
    if k == "−":
        a, b = R.randint(5000, 9999), R.randint(1000, 4999)
        e = rnd(a, 1000) - rnd(b, 1000)
        return M("Qual é a melhor estimativa para %s − %s (arredonde para o milhar)?" % (d(a), d(b)), d(e), [d(e + 1000), d(e - 1000), d(rnd(a, 1000) + rnd(b, 1000))], "%s − %s ≈ <b>%s</b>." % (d(rnd(a, 1000)), d(rnd(b, 1000)), d(e)))
    if k == "×":
        a, b = R.randint(21, 98), R.randint(21, 98)
        e = rnd(a, 10) * rnd(b, 10)
        return M("Qual é a melhor estimativa para %d × %d?" % (a, b), d(e), [d(e * 10), d(e // 10), d(rnd(a, 10) + rnd(b, 10))], "%d × %d ≈ <b>%s</b>." % (rnd(a, 10), rnd(b, 10), d(e)))
    b = R.choice([2, 3, 4, 5, 6, 7, 8, 9])
    q = R.randint(20, 300)
    a = b * q + R.randint(-b + 1, b - 1)
    e = rnd(a, 10 if a < 1000 else 100)
    return M("Qual é a melhor estimativa para %s ÷ %d?" % (d(a), b), "cerca de %s" % d(q), ["cerca de %s" % d(q * 10), "cerca de %s" % d(q // 10) if q >= 30 else "cerca de %s" % d(q + 50), "cerca de %s" % d(a - b)],
             "%d × %s ≈ %s, então %s ÷ %d ≈ <b>%s</b>." % (b, d(q), d(b * q), d(a), b, d(q)))


def s4_razoavel():
    k = R.choice(["mercado", "viagem", "calc"])
    if k == "mercado":
        ps = [R.randint(190, 1990) for _ in range(4)]
        t = sum(ps)
        e = sum(rnd(p, 100) for p in ps)
        return M("No mercado, os preços são %s. Arredondando cada um para o real mais próximo, quanto você estima gastar?" % "; ".join(reais(p) for p in ps), "cerca de %s" % reais(e), ["cerca de %s" % reais(e * 10), "cerca de %s" % reais(e // 10 // 100 * 100), "cerca de %s" % reais(e + 1000)],
                 "%s ≈ <b>%s</b> (o total exato é %s)." % (" + ".join(reais(rnd(p, 100)) for p in ps), reais(e), reais(t)))
    if k == "viagem":
        v, h = R.choice([78, 82, 88, 92, 98, 61]), R.choice([3, 4, 5, 6])
        return M("Um carro anda a cerca de %d km por hora durante %d horas. Qual é a estimativa mais razoável da distância?" % (v, h), "cerca de %d km" % (rnd(v, 10) * h), ["cerca de %d km" % (rnd(v, 10) * h * 10), "cerca de %d km" % (rnd(v, 10) + h), "cerca de %d km" % (rnd(v, 10) * h // 10)],
                 "%d × %d ≈ <b>%d km</b>." % (rnd(v, 10), h, rnd(v, 10) * h))
    a, b = R.randint(21, 99), R.randint(21, 99)
    r = a * b
    ws = [r * 10, r // 10, r + 1000]
    show = R.choice([r] + ws)
    ans = "sim, é razoável" if show == r else "não, está longe da estimativa"
    return M("Ana usou a calculadora e obteve %d × %d = %s. O resultado é razoável?" % (a, b, d(show)), ans, ["sim, é razoável" if ans != "sim, é razoável" else "não, está longe da estimativa", "só dá para saber fazendo a conta inteira", "não, porque o resultado é par"],
             "Estimativa: %d × %d = %s. %s." % (rnd(a, 10), rnd(b, 10), d(rnd(a, 10) * rnd(b, 10)), "Como %s está perto, <b>é razoável</b>" % d(show) if show == r else "%s está muito longe: <b>não é razoável</b>" % d(show)))


s5_conceitos = bank(R, [
    ("Ao arredondar 4.750 para a centena mais próxima, obtemos…", "4.800", ["4.700", "5.000", "4.750"]),
    ("Ao arredondar 2,45 para o décimo mais próximo, obtemos…", "2,5", ["2,4", "2,0", "3,0"]),
    ("Arredondar serve para…", "fazer estimativas rápidas", ["achar o resultado exato", "aumentar o número", "tirar as casas decimais sempre para baixo"]),
    ("Qual número arredondado para a dezena dá 350?", "346", ["344", "356", "340"]),
    ("Qual número arredondado para o inteiro dá 8?", "7,6", ["7,4", "8,5", "6,9"]),
    ("A população de uma cidade é 1.487.312. Arredondada para o milhão, fica…", "1.000.000", ["2.000.000", "1.500.000", "1.490.000"]),
    ("A população de uma cidade é 1.487.312. Arredondada para a centena de milhar, fica…", "1.500.000", ["1.400.000", "1.000.000", "1.490.000"]),
    ("Se o algarismo à direita da ordem escolhida é 5, arredondamos…", "para cima", ["para baixo", "não arredondamos", "tiramos o 5 só"]),
], "s5_conceitos")


def main():
    seen = set()
    sets = [
        ("Arredondar números naturais", mix(R, seen, [(s1_naturais, 20)])),
        ("Arredondar números decimais", mix(R, seen, [(s2_decimais, 20)])),
        ("Estimar operações", mix(R, seen, [(s3_estimar, 20)])),
        ("O resultado é razoável?", mix(R, seen, [(s4_razoavel, 20)])),
        ("Revisão", mix(R, seen, [(s5_conceitos, 8), (s1_naturais, 6), (s2_decimais, 6)])),
    ]
    body = lesson(
        ["Para <b>arredondar</b>, olhe o algarismo logo à direita da ordem escolhida: se for 0, 1, 2, 3 ou 4, mantenha; se for 5, 6, 7, 8 ou 9, aumente 1. Depois zere as ordens à direita.",
         "Com decimais é igual: 3,46 arredondado para o décimo é 3,5.",
         "Para <b>estimar</b>, arredonde os números antes de calcular: 48 × 21 ≈ 50 × 20 = 1.000.",
         "A estimativa ajuda a conferir se a resposta da calculadora é razoável."],
        [("Arredondar 68.452 para o milhar", ["o algarismo à direita é 4"], "68.000"),
         ("Estimar 612 ÷ 3", ["600 ÷ 3"], "cerca de 200")],
        [["Olhar o algarismo errado", "Olhe o algarismo logo à direita da ordem."],
         ["Arredondar 5 para baixo", "Com 5, arredonde para cima."],
         ["Esquecer de zerar as outras ordens", "3.682 → 3.700, não 3.782."]])
    faq = [("Como arredondar um número?", "Escolha a ordem (dezena, centena…), olhe o algarismo logo à direita: de 0 a 4, mantenha; de 5 a 9, aumente 1. Depois troque as ordens à direita por zeros."),
           ("O que a BNCC pede no 6º ano?", "Fazer estimativas de quantidades e aproximar números para múltiplos da potência de 10 mais próxima (EF06MA12).")]
    unit(R, "arredondamento-e-estimativa", "N", ["EF06MA12"],
         "Fazer estimativas de quantidades e aproximar números para múltiplos da potência de 10 mais próxima",
         "Arredondamento e estimativa", "Arredondamento e estimativa",
         "Atividades de matemática para o 6º ano sobre arredondamento e estimativa: arredondar números naturais e decimais, estimar somas, diferenças, produtos e quocientes e conferir se o resultado é razoável. 100 exercícios com gabarito.",
         "De 0 a 4 mantém; de 5 a 9 sobe.", "Arredonde antes de calcular para estimar.",
         body, faq, sets, 9, grade="6-ano")


if __name__ == "__main__":
    main()
