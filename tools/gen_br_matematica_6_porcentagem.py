# -*- coding: utf-8 -*-
"""
Brasil Matemática 6º ano: Porcentagem (Números, EF06MA13)
  python3 tools/gen_br_matematica_6_porcentagem.py
Porcentagem como fração de denominador 100 e como decimal; 50%, 25%, 10%, 1% e combinações (30% = 3 × 10%, 75%, 5%, 15%);
porcentagem de uma quantidade; que porcentagem uma parte representa; descontos e acréscimos simples; sem calculadora.
Erros: achar que 5% de 80 é 80 ÷ 5, tirar o desconto do valor errado, confundir 0,5 com 5%.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, reais
from br_9 import M, d, fq, bank, unit

R = random.Random(86010)
PCT = [1, 5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 80, 90]


def s1_formas():
    p = R.choice([1, 2, 5, 8, 10, 12, 20, 25, 35, 40, 50, 75, 80])
    k = R.choice(["dec", "fr", "de_dec", "de_fr"])
    if k == "dec":
        return M("Escreva %d%% como número decimal." % p, d(F(p, 100)), [d(F(p, 10)), d(p), d(F(p, 1000), 3)], "%d%% = %d/100 = <b>%s</b>." % (p, p, d(F(p, 100))))
    if k == "fr":
        return M("Escreva %d%% como fração irredutível." % p, fq(F(p, 100)), [fq(F(p, 10)) if p % 10 else fq(F(p, 1000)), fq(F(1, p)), fq(F(p + 1, 100))], "%d%% = %d/100 = <b>%s</b>." % (p, p, fq(F(p, 100))))
    if k == "de_dec":
        return M("Escreva %s em porcentagem." % d(F(p, 100)), "%d%%" % p, ["%s%%" % d(F(p, 10)), "%d%%" % (p * 10), "%s%%" % d(F(p, 100))], "%s × 100 = <b>%d%%</b>." % (d(F(p, 100)), p))
    f = F(p, 100)
    return M("Escreva %s em porcentagem." % fq(f), "%d%%" % p, ["%d%%" % (f.numerator * 10) if f.numerator * 10 != p else "%d%%" % (p + 5), "%d%%" % f.denominator, "%d%%" % (f.numerator + f.denominator)],
             "%s = %d/100 = <b>%d%%</b>." % (fq(f), p, p))


def s2_de():
    p = R.choice(PCT)
    q = R.choice([20, 40, 60, 80, 120, 150, 200, 240, 300, 360, 400, 500, 600, 800, 1200])
    v = F(p * q, 100)
    if v.denominator != 1:
        return None
    hint = {50: "metade", 25: "metade da metade", 10: "÷ 10", 1: "÷ 100", 5: "metade de 10%", 75: "50% + 25%", 20: "2 × 10%"}.get(p, "%d × 10%%" % (p // 10) if p % 10 == 0 else "10%% + 5%%" if p == 15 else "")
    return M("Quanto é %d%% de %s?" % (p, d(q)), d(v), [d(F(q, p)) if (F(q, p)).denominator == 1 else d(v + 10), d(v * 10), d(q - v)],
             "%d%% de %s%s = <b>%s</b>." % (p, d(q), " (%s)" % hint if hint else "", d(v)))


def s3_qual_pct():
    tot = R.choice([20, 25, 40, 50, 200, 400, 500])
    p = R.choice([5, 10, 20, 25, 30, 40, 50, 60, 75, 80])
    part = F(p * tot, 100)
    if part.denominator != 1:
        return None
    ctx = R.choice(["Numa turma de %d alunos, %d usam óculos." % (tot, part), "Num pomar com %d árvores, %d são laranjeiras." % (tot, part), "Numa prova de %d questões, Ana acertou %d." % (tot, part)])
    return M("%s Que porcentagem isso representa?" % ctx, "%d%%" % p, ["%s%%" % d(part), "%d%%" % (100 - p), "%s%%" % d(F(tot, part)) if (F(tot, part)).denominator == 1 and F(tot, part) != p else "%d%%" % (p + 10)],
             "%d/%d = %d/100 = <b>%d%%</b>." % (part, tot, p, p))


def s4_desconto():
    p = R.choice([10, 15, 20, 25, 30, 40, 50])
    v = R.choice([40, 60, 80, 120, 150, 200, 250, 300, 400, 600, 800])
    dsc = F(p * v, 100)
    if dsc.denominator != 1:
        return None
    k = R.choice(["desc", "acr", "valor_desc"])
    if k == "desc":
        return M("Um tênis custa %s e está com %d%% de desconto. Quanto vai custar?" % (reais(v * 100), p), reais(int(v - dsc) * 100), [reais(int(dsc) * 100), reais(int(v + dsc) * 100), reais((v - p) * 100)],
                 "Desconto: %d%% de %d = %s; %d − %s = <b>%s</b>." % (p, v, d(dsc), v, d(dsc), reais(int(v - dsc) * 100)))
    if k == "acr":
        return M("Uma conta de %s foi paga com atraso e teve acréscimo de %d%%. Qual foi o valor pago?" % (reais(v * 100), p), reais(int(v + dsc) * 100), [reais(int(v - dsc) * 100), reais(int(dsc) * 100), reais((v + p) * 100)],
                 "Acréscimo: %s; %d + %s = <b>%s</b>." % (d(dsc), v, d(dsc), reais(int(v + dsc) * 100)))
    return M("Uma bicicleta de %s está com %d%% de desconto. De quantos reais é o desconto?" % (reais(v * 100), p), reais(int(dsc) * 100), [reais(int(v - dsc) * 100), reais(p * 100), reais(int(dsc) * 1000)],
             "%d%% de %d = <b>%s</b>." % (p, v, reais(int(dsc) * 100)))


s5_conceitos = bank(R, [
    ("100% de uma quantidade é…", "a quantidade inteira", ["a metade", "zero", "o dobro"]),
    ("50% é o mesmo que…", "a metade", ["um quarto", "o dobro", "um décimo"]),
    ("25% é o mesmo que…", "um quarto", ["a metade", "um quinto", "um décimo"]),
    ("10% de um valor se acha…", "dividindo por 10", ["dividindo por 100", "multiplicando por 10", "tirando 10"]),
    ("Qual é maior: 30% de 200 ou 50% de 100?", "30% de 200", ["50% de 100", "são iguais", "não dá para comparar"]),
    ("0,5 é igual a…", "50%", ["5%", "0,5%", "500%"]),
    ("Se 20% de um número é 30, o número é…", "150", ["60", "600", "50"]),
    ("Uma loja dá 10% de desconto e depois mais 10%. O desconto total é…", "menor que 20%", ["exatamente 20%", "maior que 20%", "10%"]),
    ("O símbolo % significa…", "«por cento», dividido por 100", ["«por mil»", "«vezes 100»", "«por dez»"]),
    ("75% de uma pizza são…", "3 de 4 pedaços iguais", ["7 de 5 pedaços", "1 de 4 pedaços", "75 pedaços"]),
], "s5_conceitos")


def main():
    seen = set()
    sets = [
        ("Porcentagem, fração e decimal", mix(R, seen, [(s1_formas, 20)])),
        ("Porcentagem de uma quantidade", mix(R, seen, [(s2_de, 20)])),
        ("Que porcentagem é?", mix(R, seen, [(s3_qual_pct, 14), (s5_conceitos, 6)])),
        ("Descontos e acréscimos", mix(R, seen, [(s4_desconto, 20)])),
        ("Revisão", mix(R, seen, [(s5_conceitos, 4), (s2_de, 8), (s4_desconto, 8)])),
    ]
    body = lesson(
        ["<b>Porcentagem</b> é uma fração de denominador 100: 35% = 35/100 = 0,35.",
         "Atalhos: 50% é a metade, 25% é a metade da metade, 10% é dividir por 10, 1% é dividir por 100. Combine: 30% = 3 × 10%; 15% = 10% + 5%.",
         "Desconto: tire a porcentagem do preço. Acréscimo: some a porcentagem ao preço."],
        [("15% de 80", ["10% = 8", "5% = 4", "8 + 4"], "12"),
         ("R$ 120,00 com 25% de desconto", ["25% de 120 = 30", "120 − 30"], "R$ 90,00")],
        [["Achar 5% dividindo por 5", "5% é a metade de 10%."],
         ["Responder só o desconto", "O preço final é preço − desconto."],
         ["Confundir 0,5 com 5%", "0,5 = 50%; 5% = 0,05."]])
    faq = [("Como calcular porcentagem de cabeça?", "Comece pelos 10% (divida por 10) e pelos 50% (metade). Depois combine: 20% é o dobro de 10%; 5% é a metade de 10%; 75% é 50% + 25%."),
           ("O que a BNCC pede no 6º ano?", "Resolver e elaborar problemas que envolvam porcentagens, com base na ideia de proporcionalidade, sem fazer uso da «regra de três», utilizando estratégias pessoais, cálculo mental e calculadora (EF06MA13).")]
    unit(R, "porcentagem", "N", ["EF06MA13"],
         "Resolver e elaborar problemas que envolvam porcentagens, com base na ideia de proporcionalidade, sem fazer uso da «regra de três», utilizando estratégias pessoais, cálculo mental e calculadora, em contextos de educação financeira, entre outros",
         "Porcentagem: cálculo mental, descontos e acréscimos", "Porcentagem",
         "Atividades de matemática para o 6º ano sobre porcentagem: porcentagem como fração e decimal, porcentagem de uma quantidade, que porcentagem uma parte representa, descontos e acréscimos. 100 exercícios com gabarito.",
         "10% = ÷ 10; 50% = metade; 25% = metade da metade.", "Preço com desconto = preço − desconto.",
         body, faq, sets, 10, grade="6-ano")


if __name__ == "__main__":
    main()
