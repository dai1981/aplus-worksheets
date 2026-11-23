# -*- coding: utf-8 -*-
"""
Brasil Matemática 5º ano: Multiplicação (Números, EF05MA08)
  python3 tools/gen_br_matematica_5_multiplicacao.py
Multiplicar por 10, 100 e 1.000 e por dezenas e centenas exatas; multiplicação por 1 algarismo e por 2 algarismos
(conta armada, decomposição); propriedades (comutativa, associativa, distributiva); estimativa; problemas.
Erros: esquecer o zero da segunda linha (× dezenas), não somar o «vai um», contar errado os zeros em 40 × 500.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, reais, armada, Kids

R = random.Random(80508)
K = Kids(R)


def no_shift(a, b):
    """a × b com 2 algarismos esquecendo o zero da segunda linha"""
    return a * (b % 10) + a * (b // 10)


def no_carry(a, d):
    """a × d (1 algarismo) sem somar o «vai um»"""
    return int("".join(str(int(x) * d % 10) for x in str(a)))


def s1_dez():
    a = R.randint(2, 999)
    m = R.choice([10, 100, 1000])
    if a * m >= 1000000 or a % 10 == 0 and R.random() < 0.5:
        return None
    return mcq("Calcule %s × %s." % (num(a), num(m)), num(a * m), [num(x) for x in (a * m // 10, a * m * 10, a + m, a * 10 if m != 10 else a * 1000) if x < 10 ** 7 and x != a * m],
               "Multiplicar por %s é acrescentar %d zero%s: <b>%s</b>." % (num(m), len(str(m)) - 1, "" if m == 10 else "s", num(a * m)))


def s1_exatas():
    a = R.randint(2, 9) * R.choice([10, 100])
    b = R.randint(2, 9) * R.choice([10, 100, 1])
    if a * b >= 1000000 or b < 10 and a < 100:
        return None
    p = a * b
    da, db = a, b
    za = len(str(a)) - len(str(a).rstrip("0"))
    zb = len(str(b)) - len(str(b).rstrip("0"))
    core = int(str(a).rstrip("0")) * int(str(b).rstrip("0"))
    return mcq("Calcule %s × %s." % (num(a), num(b)), num(p), [num(x) for x in (p // 10, p * 10, core * 10 ** max(za, zb), p * 100, a + b) if x != p],
               "%d × %d = %d; acrescente os %d zeros: <b>%s</b>." % (int(str(a).rstrip("0")), int(str(b).rstrip("0")), core, za + zb, num(p)))


def s2_um():
    a = R.randint(1000, 99999)
    d = R.randint(3, 9)
    p = a * d
    w = no_carry(a, d)
    pic = armada([num(a), str(d)], "×") if R.random() < 0.5 else ""
    return mcq(pic + "Calcule %s × %d." % (num(a), d), num(p), [num(x) for x in (w, p + d, p - 10, p + 1000, a * (d - 1)) if x != p and x > 0],
               "Multiplique cada ordem por %d, da direita para a esquerda, somando o «vai um»: <b>%s</b>." % (d, num(p)))


def s2_dois():
    a = R.randint(100, 9999)
    b = R.randint(12, 99)
    if b % 10 == 0 or a * b >= 1000000:
        return None
    p = a * b
    pic = armada([num(a), str(b)], "×") if R.random() < 0.5 else ""
    return mcq(pic + "Calcule %s × %d." % (num(a), b), num(p), [num(x) for x in (no_shift(a, b), p + a, p - a, p + 100) if x != p],
               "%s × %d = %s e %s × %d = %s. Some: %s + %s = <b>%s</b>." % (num(a), b % 10, num(a * (b % 10)), num(a), b // 10 * 10, num(a * (b // 10 * 10)),
                                                                     num(a * (b % 10)), num(a * (b // 10 * 10)), num(p)))


def s3_distributiva():
    a = R.randint(12, 99)
    b = R.randint(12, 99)
    t, u = b // 10 * 10, b % 10
    if u == 0:
        return None
    k = R.choice(["dec", "comp"])
    if k == "dec":
        good = "%d × %d + %d × %d" % (a, t, a, u)
        return mcq("Qual conta tem o mesmo resultado que %d × %d?" % (a, b), good, ["%d × %d + %d" % (a, t, u), "%d × %d × %d" % (a, t, u), "%d + %d × %d" % (a, t, u), "%d × %d + %d × %d" % (a, b // 10, a, u)],
                   "Decomponha %d = %d + %d e multiplique cada parte: <b>%s</b>." % (b, t, u, good))
    good = num(a * t + a * u)
    return mcq("Calcule de cabeça: %d × %d = %d × %d + %d × %d = ?" % (a, b, a, t, a, u), good, [num(x) for x in (a * t + u, a * t * u, no_shift(a, b), a * b + a) if x != a * b],
               "%d × %d = %s e %d × %d = %d. %s + %d = <b>%s</b>." % (a, t, num(a * t), a, u, a * u, num(a * t), a * u, good))


PROPS = [("comutativa", "a ordem dos fatores não altera o produto"), ("associativa", "podemos agrupar os fatores de modos diferentes"),
         ("distributiva", "multiplicar uma soma é o mesmo que somar os produtos"), ("elemento neutro", "multiplicar por 1 não muda o número")]


def s3_props():
    a, b, c = R.randint(2, 30), R.randint(2, 30), R.randint(2, 9)
    k = R.choice(range(4))
    if k == 0:
        q = "%d × %d = %d × %d" % (a, b, b, a)
    elif k == 1:
        q = "(%d × %d) × %d = %d × (%d × %d)" % (a, b, c, a, b, c)
    elif k == 2:
        q = "%d × (%d + %d) = %d × %d + %d × %d" % (c, a, b, c, a, c, b)
    else:
        q = "%d × 1 = %d" % (a * b, a * b)
    nome, why = PROPS[k]
    return mcq("Que propriedade da multiplicação aparece em %s?" % q, nome, [n for n, _ in PROPS if n != nome],
               "Na propriedade %s, %s. Resposta: <b>%s</b>." % (nome, why, nome))


def s4_estimar():
    a = R.randint(110, 990)
    b = R.randint(11, 98)
    if a % 100 == 50 or b % 10 == 5:
        return None
    ra, rb = (a + 50) // 100 * 100, (b + 5) // 10 * 10
    e = ra * rb
    opts = [e // 10, e * 10, e + ra * 10 if e + ra * 10 != e else e * 2, e * 2]
    return mcq("Arredonde os fatores e estime %d × %d." % (a, b), "cerca de " + num(e), ["cerca de " + num(x) for x in opts if x != e],
               "%d ≈ %d e %d ≈ %d. %d × %d = <b>%s</b> (a conta exata dá %s)." % (a, ra, b, rb, ra, rb, num(e), num(a * b)))


def s4_falta():
    a = R.randint(12, 99)
    m = R.choice([10, 100, 1000, 20, 50, 200])
    p = a * m
    return mcq("Que número multiplicado por %s dá %s?" % (num(m), num(p)), num(a), [num(x) for x in (a * 10, a // 10 if a >= 20 else a + 10, p - m, m) if x != a and x > 0],
               "Pense na divisão: %s ÷ %s = <b>%s</b>." % (num(p), num(m), num(a)))


def s5_problema():
    k = R.choice(["onibus", "caixas", "preco", "dias", "cadeiras", "salario", "pacotes", "km"])
    p, g = K.next()
    if k == "onibus":
        a, b = R.randint(12, 25), R.randint(38, 52)
        return mcq("Uma escola alugou %d ônibus para uma excursão. Cada ônibus leva %d pessoas. Quantas pessoas podem ir?" % (a, b), num(a * b),
                   [num(x) for x in (a + b, no_shift(b, a), a * b + b, a * b - a) if x != a * b], "%d × %d = <b>%s</b> pessoas." % (a, b, num(a * b)))
    if k == "caixas":
        a, b = R.randint(120, 480), R.randint(12, 36)
        return mcq("Uma fábrica embala %d caixas por dia. Cada caixa tem %d sucos. Quantos sucos ela embala por dia?" % (a, b), num(a * b),
                   [num(x) for x in (no_shift(a, b), a * b + a, a + b, a * b - 100) if x != a * b], "%d × %d = <b>%s</b> sucos." % (a, b, num(a * b)))
    if k == "preco":
        pr = R.randint(15, 99) * 100 + R.choice([0, 50, 90])
        n = R.randint(3, 12)
        return mcq("Um ingresso de cinema custa %s. Quanto custam %d ingressos?" % (reais(pr), n), reais(pr * n),
                   [reais(x) for x in (pr * (n - 1), pr * n + pr, pr + n * 100, pr * n + 1000) if x != pr * n], "%d × %s = <b>%s</b>." % (n, reais(pr), reais(pr * n)))
    if k == "dias":
        a = R.randint(25, 60)
        return mcq("%s lê %d páginas por dia. Quantas páginas %s lê em 4 semanas?" % (p, a, g), num(a * 28), [num(x) for x in (a * 4, a * 7, a * 30, a * 28 + a) if x != a * 28],
                   "4 semanas = 4 × 7 = 28 dias. %d × 28 = <b>%s</b> páginas." % (a, num(a * 28)))
    if k == "cadeiras":
        a, b = R.randint(15, 40), R.randint(18, 35)
        return mcq("Um auditório tem %d fileiras com %d cadeiras cada. Quantas cadeiras há ao todo?" % (a, b), num(a * b),
                   [num(x) for x in (no_shift(a, b), a + b, a * b + 10, a * b - b) if x != a * b], "%d × %d = <b>%s</b> cadeiras." % (a, b, num(a * b)))
    if k == "salario":
        m = R.randint(15, 45) * 10000
        return mcq("Uma loja vende %s por mês. Mantendo esse valor, quanto vende em 12 meses?" % reais(m), reais(m * 12), [reais(x) for x in (m * 10, m * 2, m * 12 + m, m * 11) if x != m * 12],
                   "12 × %s = <b>%s</b>." % (reais(m), reais(m * 12)))
    if k == "pacotes":
        a = R.randint(14, 48)
        return mcq("Um pacote tem %d figurinhas. %s comprou 25 pacotes. Quantas figurinhas %s tem?" % (a, p, g), num(a * 25), [num(x) for x in (a * 20, a + 25, a * 25 + a, no_shift(a, 25)) if x != a * 25],
                   "%d × 25 = %d × 100 ÷ 4 = <b>%s</b> figurinhas." % (a, a, num(a * 25)))
    a = R.randint(110, 480)
    return mcq("Um caminhão roda %d km por dia. Quantos quilômetros roda em 15 dias?" % a, num(a * 15) + " km", [num(x) + " km" for x in (a * 10, a * 5, a + 15, no_shift(a, 15)) if x != a * 15],
               "%d × 15 = %d × 10 + %d × 5 = %s + %s = <b>%s km</b>." % (a, a, a, num(a * 10), num(a * 5), num(a * 15)))


def main():
    seen = set()
    sets = [
        ("Multiplicar por 10, 100 e 1.000", mix(R, seen, [(s1_dez, 12), (s1_exatas, 8)])),
        ("Conta armada", mix(R, seen, [(s2_um, 8), (s2_dois, 12)])),
        ("Propriedades e cálculo mental", mix(R, seen, [(s3_distributiva, 12), (s3_props, 8)])),
        ("Estimativa e número que falta", mix(R, seen, [(s4_estimar, 10), (s4_falta, 10)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Multiplicar por 10, 100 ou 1.000 é acrescentar 1, 2 ou 3 zeros: 47 × 100 = 4.700.",
         "Com números exatos, multiplique sem os zeros e depois junte todos os zeros: 40 × 500 → 4 × 5 = 20 → 20.000.",
         "Para multiplicar por 2 algarismos, decomponha: 243 × 36 = 243 × 6 + 243 × 30.",
         "Antes de calcular, faça uma <b>estimativa</b>: 243 × 36 ≈ 200 × 40 = 8.000."],
        [("Calcule 243 × 36.", ["243 × 6 = 1.458", "243 × 30 = 7.290", "1.458 + 7.290"], "8.748"),
         ("Calcule 40 × 500.", ["4 × 5 = 20", "3 zeros: 20.000"], "20.000")],
        [["Esquecer o zero da segunda linha", "A segunda linha é × dezenas: 243 × 30 = 7.290, não 729."],
         ["Não somar o «vai um»", "Escreva o algarismo que vai em cima da coluna seguinte."],
         ["Contar errado os zeros: 40 × 500 = 2.000", "Conte os zeros dos dois fatores: 1 + 2 = 3 zeros."]],
        armada(["243", "36"], "×"))
    faq = [("O que o 5º ano aprende de multiplicação?", "A BNCC pede resolver e elaborar problemas de multiplicação com números naturais e decimais, usando estimativa, cálculo mental e algoritmos (conta armada)."),
           ("Por que fazer uma estimativa antes?", "A estimativa mostra se o resultado é razoável. Se 243 × 36 deu 1.458, a estimativa de 8.000 mostra que faltou a segunda linha.")]
    make_unit(R, "multiplicacao", "N", ["EF05MA08"],
              "Resolver e elaborar problemas de multiplicação e divisão com números naturais e com números racionais cuja representação decimal é finita (com multiplicador natural e divisor natural e diferente de zero), utilizando estratégias diversas, como cálculo por estimativa, cálculo mental e algoritmos",
              "Multiplicação: por 10, 100 e 1.000, conta armada e propriedades", "Multiplicação",
              "Atividades de matemática para o 5º ano sobre multiplicação: por 10, 100 e 1.000, dezenas e centenas exatas, conta armada com 2 algarismos, propriedades, estimativa e problemas. 100 exercícios com gabarito.",
              "243 × 36 = 243 × 6 + 243 × 30", "Faça uma estimativa antes de calcular.",
              body, faq, sets, 8, grade="5-ano")


if __name__ == "__main__":
    main()
