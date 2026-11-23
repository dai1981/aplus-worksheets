# -*- coding: utf-8 -*-
"""
Brasil Matemática 4º ano: Propriedades das operações e cálculo mental (Números, EF04MA05)
  python3 tools/gen_br_matematica_4_propriedades_e_calculo_mental.py
Propriedades comutativa e associativa da adição e da multiplicação, distributiva, elemento neutro e o zero na multiplicação;
estratégias de cálculo mental: agrupar parcelas que dão dezenas exatas, 25 × 4 = 100, × 5 = × 10 ÷ 2, × 4 = dobro do dobro, decompor um fator.
Erros: aplicar a comutativa na subtração e na divisão, esquecer uma parte na distributiva (6 × 23 = 6 × 20 + 3), achar que n × 0 = n.
"""
import random
from br_common import mcq, num, reais, lesson, make_unit, mix, use, lim

R = random.Random(80404)
s5_dist, s5_props = use("gen_br_matematica_5_multiplicacao", 80944, "s3_distributiva", "s3_props", preds=(lim(99999, 0),))


def s1_agrupar():
    a = R.randint(11, 89)
    b = R.randint(11, 89)
    c = (100 - a % 100) % 100 if R.random() < 0.5 else 100 - a
    if c <= 0 or c == b:
        return None
    nums = [a, b, c]
    R.shuffle(nums)
    s = a + b + c
    return mcq("Calcule de cabeça, agrupando as parcelas que dão 100: %s." % " + ".join(map(str, nums)), str(s), [str(s - 10), str(s + 10), str(s + 100)],
               "Junte primeiro %d + %d = 100 (associativa e comutativa); depois some %d: <b>%d</b>." % (a, c, b, s))


def s1_comut():
    a, b = R.randint(12, 99), R.randint(3, 9)
    k = R.choice(["add", "mul", "sub", "div"])
    if k == "add":
        return mcq("Se %d + %d = %d, quanto é %d + %d?" % (a, b * 7, a + b * 7, b * 7, a), str(a + b * 7), [str(a - b * 7) if a > b * 7 else str(b * 7 - a), str(a + b * 7 + 1), "não dá para saber sem calcular"],
                   "A ordem das parcelas não altera a soma (comutativa): <b>%d</b>." % (a + b * 7))
    if k == "mul":
        return mcq("Se %d × %d = %d, quanto é %d × %d?" % (a, b, a * b, b, a), str(a * b), [str(a + b), str(a * b + a), "não dá para saber sem calcular"],
                   "A ordem dos fatores não altera o produto (comutativa): <b>%d</b>." % (a * b))
    if k == "sub":
        x, y = a + 20, b
        return mcq("Na subtração vale a propriedade comutativa? Compare %d − %d e %d − %d." % (x, y, y, x), "Não: %d − %d = %d, mas %d − %d não dá %d" % (x, y, x - y, y, x, x - y),
                   ["Sim: as duas dão %d" % (x - y), "Sim: a ordem nunca importa", "Só quando os números são pares"],
                   "A comutativa vale para a adição e a multiplicação, <b>não para a subtração</b>.")
    x = b * R.randint(2, 9)
    return mcq("Na divisão vale a propriedade comutativa? Compare %d ÷ %d e %d ÷ %d." % (x, b, b, x), "Não: %d ÷ %d = %d, mas %d ÷ %d não dá %d" % (x, b, x // b, b, x, x // b),
               ["Sim: as duas dão %d" % (x // b), "Sim: a ordem nunca importa", "Só quando os números são pares"],
               "A comutativa vale para a adição e a multiplicação, <b>não para a divisão</b>.")


def s2_associa():
    k = R.choice(["25x4", "5x2", "50x2", "125x8"])
    a = R.randint(3, 99)
    pair = {"25x4": (25, 4), "5x2": (5, 2), "50x2": (50, 2), "125x8": (125, 8)}[k]
    x, y = pair
    nums = [x, a, y]
    R.shuffle(nums)
    p = x * y * a
    return mcq("Calcule de cabeça: %s." % " × ".join(map(str, nums)), num(p), [num(p // 10), num(p * 10), num(x * a + y), num(p + a)],
               "Agrupe %d × %d = %d primeiro (associativa e comutativa); depois × %d: <b>%s</b>." % (x, y, x * y, a, num(p)))


def s2_truques():
    k = R.choice(["x5", "x4", "x9", "x11", "x20"])
    a = R.randint(12, 98) if k != "x5" else R.randint(12, 98) * 2
    if k == "x5":
        return mcq("Calcule de cabeça %d × 5 (dica: × 10 e depois ÷ 2)." % a, num(a * 5), [num(a * 10), num(a * 5 + 5), num(a // 2), num(a + 5)],
                   "%d × 10 = %s; %s ÷ 2 = <b>%s</b>." % (a, num(a * 10), num(a * 10), num(a * 5)))
    if k == "x4":
        return mcq("Calcule de cabeça %d × 4 (dica: o dobro do dobro)." % a, num(a * 4), [num(a * 2), num(a * 4 + 4), num(a + 4), num(a * 8)],
                   "Dobro de %d = %d; dobro de %d = <b>%s</b>." % (a, a * 2, a * 2, num(a * 4)))
    if k == "x9":
        return mcq("Calcule de cabeça %d × 9 (dica: × 10 e tire uma vez o número)." % a, num(a * 9), [num(a * 10), num(a * 10 - 9), num(a * 9 + a), num(a * 10 - 10)],
                   "%d × 10 = %s; %s − %d = <b>%s</b>." % (a, num(a * 10), num(a * 10), a, num(a * 9)))
    if k == "x11":
        return mcq("Calcule de cabeça %d × 11 (dica: × 10 e some uma vez o número)." % a, num(a * 11), [num(a * 10), num(a * 10 + 11), num(a * 11 - a * 2), num(a + 11)],
                   "%d × 10 = %s; %s + %d = <b>%s</b>." % (a, num(a * 10), num(a * 10), a, num(a * 11)))
    return mcq("Calcule de cabeça %d × 20 (dica: dobre e acrescente um zero)." % a, num(a * 20), [num(a * 2), num(a * 200), num(a * 20 + 20), num(a + 20)],
               "Dobro de %d = %d; × 10 = <b>%s</b>." % (a, a * 2, num(a * 20)))


def s3_neutro():
    a = R.randint(12, 9999)
    k = R.choice(["x1", "x0", "+0", "÷1", "0÷"])
    if k == "x1":
        return mcq("Quanto é %s × 1?" % num(a), num(a), ["1", "0", num(a + 1)], "Multiplicar por 1 não muda o número (elemento neutro): <b>%s</b>." % num(a))
    if k == "x0":
        return mcq("Quanto é %s × 0?" % num(a), "0", [num(a), "1", num(a * 10)], "Qualquer número multiplicado por 0 dá <b>0</b>.")
    if k == "+0":
        return mcq("Quanto é %s + 0?" % num(a), num(a), ["0", num(a * 10), num(a + 1)], "Somar 0 não muda o número (elemento neutro da adição): <b>%s</b>." % num(a))
    if k == "÷1":
        return mcq("Quanto é %s ÷ 1?" % num(a), num(a), ["1", "0", num(a - 1)], "Dividir por 1 não muda o número: <b>%s</b>." % num(a))
    return mcq("Quanto é 0 ÷ %s?" % num(a), "0", [num(a), "1", "não existe"], "Zero dividido por qualquer número (diferente de zero) dá <b>0</b>.")


def s4_dist_soma():
    a = R.randint(3, 9)
    b, c = R.randint(10, 60), R.randint(2, 9)
    t = b // 10 * 10
    u = b % 10
    if not u:
        return None
    k = R.choice(["mostra", "calc"])
    if k == "mostra":
        good = "%d × %d + %d × %d" % (a, t, a, u)
        return mcq("Qual conta tem o mesmo resultado que %d × %d?" % (a, b), good, ["%d × %d + %d" % (a, t, u), "%d + %d × %d" % (a, t, u), "%d × %d × %d" % (a, t, u)],
                   "Decomponha %d = %d + %d e multiplique as duas partes por %d (distributiva): <b>%s</b>." % (b, t, u, a, good))
    return mcq("Calcule %d × (%d + %d) de dois jeitos. Qual é o resultado?" % (a, t, c), str(a * (t + c)), [str(a * t + c), str(a + t + c), str(a * t * c)],
               "%d × %d + %d × %d = %d + %d = <b>%d</b>." % (a, t, a, c, a * t, a * c, a * (t + c)))


def s5_problema():
    k = R.choice(["caixas", "ovos", "mesada", "canetas", "parcelas", "trilha"])
    if k == "caixas":
        e, c = R.randint(3, 18), R.choice([2, 4, 8])
        t = e * c * 25
        return mcq("Um mercado recebeu %d engradados. Cada engradado tem %d caixas com 25 garrafas. Quantas garrafas são?" % (e, c), num(t),
                   [num(e * c + 25), num(e * 25), num(t // 10), num(t + 25)],
                   "Agrupe de um jeito fácil: %d × (%d × 25) = %d × %d = <b>%s</b>." % (e, c, e, c * 25, num(t)))
    if k == "ovos":
        n = R.randint(11, 39)
        return mcq("Uma granja embala %d caixas com 12 ovos. Quantos ovos são? (dica: 12 = 10 + 2)" % n, num(n * 12), [num(n * 10 + 2), num(n * 12 + 12), num(n + 12)],
                   "%d × 10 + %d × 2 = %d + %d = <b>%s</b>." % (n, n, n * 10, n * 2, num(n * 12)))
    if k == "mesada":
        v = R.randint(15, 45)
        return mcq("Uma criança ganha %s por semana. Quanto ganha em 9 semanas? (dica: × 10 e tire uma semana)" % reais(v * 100), reais(v * 900),
                   [reais(x * 100) for x in (v * 10, v * 9 + 9, v * 10 - 9)], "%d × 10 = %d; %d − %d = <b>%s</b>." % (v, v * 10, v * 10, v, reais(v * 900)))
    if k == "canetas":
        n = R.randint(12, 48)
        return mcq("Cada pacote tem 5 canetas. Quantas canetas há em %d pacotes? (dica: × 10 e ÷ 2)" % (n * 2), str(n * 10), [str(n * 20), str(n * 2 + 5), str(n * 5)],
                   "%d × 10 = %d; %d ÷ 2 = <b>%d</b>." % (n * 2, n * 20, n * 20, n * 10))
    if k == "parcelas":
        a, b = R.randint(3, 6), R.randint(25, 95)
        return mcq("Uma loja vendeu %d bonés de %s e %d camisetas de %s. Quanto recebeu ao todo? (dica: %d × (%d + %d))" % (a, reais(b * 100), a, reais((100 - b) * 100), a, b, 100 - b),
                   reais(a * 10000), [reais(x * 100) for x in (a * b, a + 100, a * 100 + b)],
                   "%d × %d + %d × %d = %d × (%d + %d) = %d × 100 = <b>%s</b>." % (a, b, a, 100 - b, a, b, 100 - b, a, reais(a * 10000)))
    a, b, c = R.randint(15, 85), R.randint(15, 85), R.randint(15, 85)
    d = 100 - a
    return mcq("Numa trilha, uma família andou %d m, %d m, %d m e %d m. Quantos metros andou?" % (a, b, d, c), "%d m" % (a + b + c + d),
               ["%d m" % x for x in (a + b + c + d + 10, a + b + c + d - 10, a + b + c)], "Junte %d + %d = 100 e depois some %d + %d: <b>%d m</b>." % (a, d, b, c, a + b + c + d))


def main():
    seen = set()
    sets = [
        ("Comutativa e associativa", mix(R, seen, [(s1_agrupar, 10), (s1_comut, 10)])),
        ("Agrupar para facilitar", mix(R, seen, [(s2_associa, 10), (s2_truques, 10)])),
        ("Elemento neutro e propriedades", mix(R, seen, [(s3_neutro, 10), (s5_props, 10)])),
        ("Propriedade distributiva", mix(R, seen, [(s4_dist_soma, 10), (s5_dist, 10)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["<b>Comutativa</b>: a ordem não muda o resultado da adição e da multiplicação (7 × 8 = 8 × 7). Não vale para a subtração e a divisão.",
         "<b>Associativa</b>: podemos agrupar parcelas ou fatores do jeito mais fácil: 25 × 7 × 4 = (25 × 4) × 7 = 700.",
         "<b>Distributiva</b>: 6 × 23 = 6 × 20 + 6 × 3 = 120 + 18 = 138.",
         "Somar 0 ou multiplicar por 1 não muda o número; multiplicar por 0 dá 0."],
        [("Calcule 37 + 48 + 63.", ["37 + 63 = 100", "100 + 48"], "148"),
         ("Calcule 46 × 9.", ["46 × 10 = 460", "460 − 46"], "414")],
        [["Usar a comutativa na subtração: 5 − 8 = 8 − 5", "Na subtração e na divisão, a ordem importa."],
         ["Esquecer uma parte na distributiva: 6 × 23 = 120 + 3", "Multiplique as duas partes: 6 × 20 + 6 × 3."],
         ["Achar que 7 × 0 = 7", "7 grupos de nada é nada: 7 × 0 = 0."]])
    faq = [("Para que servem as propriedades das operações?", "Para calcular de cabeça e de jeitos mais fáceis: trocar a ordem, agrupar números que formam dezenas exatas ou decompor um fator."),
           ("A propriedade comutativa vale para todas as operações?", "Não. Vale para a adição e a multiplicação. Na subtração e na divisão, trocar a ordem muda o resultado.")]
    make_unit(R, "propriedades-e-calculo-mental", "N", ["EF04MA05"],
              "Utilizar as propriedades das operações para desenvolver estratégias de cálculo",
              "Propriedades das operações e cálculo mental", "Propriedades das operações",
              "Atividades de matemática para o 4º ano sobre propriedades das operações: comutativa, associativa, distributiva, elemento neutro e estratégias de cálculo mental. 100 exercícios com gabarito.",
              "Troque a ordem, agrupe ou decomponha para calcular mais fácil.", "6 × 23 = 6 × 20 + 6 × 3",
              body, faq, sets, 4, grade="4-ano")


if __name__ == "__main__":
    main()
