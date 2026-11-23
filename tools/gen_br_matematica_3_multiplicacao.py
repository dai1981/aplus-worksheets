# -*- coding: utf-8 -*-
"""
Brasil Matemática 3º ano: Multiplicação (Números, EF03MA07)
  python3 tools/gen_br_matematica_3_multiplicacao.py
Disposição retangular, multiplicar por 10 e por 100, dezenas e centenas exatas (3 × 40), multiplicar um número de
2 algarismos por 2, 3, 4 ou 5 decompondo (4 × 23 = 4 × 20 + 4 × 3), conta armada simples, problemas.
Erros: multiplicar só as dezenas (4 × 23 = 80), esquecer de multiplicar as unidades, × 10 «acrescenta» 10.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, arranjo, KINDS, COISAS, coisas, armada, Kids, reais

R = random.Random(80308)
K = Kids(R)


def s1_arranjo():
    a, b = R.randint(2, 5), R.randint(3, 8)
    kind = R.choice(KINDS)
    nome = coisas(kind, 2).split(" ", 1)[1]
    q = "%s %s há? Use uma multiplicação." % ("Quantas" if COISAS[kind][2] == "f" else "Quantos", nome)
    return mcq(arranjo(a, b, kind) + q, str(a * b), [str(a + b), str(a * b + b), str(a * b - a), str(2 * (a + b))],
               "%d linhas com %d em cada: %d × %d = <b>%d</b>." % (a, b, a, b, a * b))


def s1_linhas():
    a, b = R.randint(2, 6), R.randint(3, 9)
    c = R.choice(["cadeiras", "carteiras", "mudas de alface", "azulejos", "quadradinhos"])
    return mcq("Num auditório, as %s estão em %d fileiras com %d em cada uma. Quantas são ao todo?" % (c, a, b) if c in ("cadeiras", "carteiras")
               else "Uma horta tem %d fileiras com %d %s em cada. Quantas %s há?" % (a, b, c, c) if c == "mudas de alface"
               else "Uma parede tem %d fileiras com %d %s em cada. Quantos %s há?" % (a, b, c, c),
               str(a * b), [str(a + b), str(a * b + a), str(a * (b - 1))],
               "Disposição retangular: %d × %d = <b>%d</b>." % (a, b, a * b))


def s2_dez():
    k = R.choice(["10", "100", "dez", "cem"])
    if k == "10":
        n = R.randint(4, 99)
        return mcq("Quanto é %d × 10?" % n, num(n * 10), [num(n + 10), num(n * 100), num(n)],
                   "Multiplicar por 10: cada unidade vira dezena, acrescente um zero à direita: <b>%s</b>." % num(n * 10))
    if k == "100":
        n = R.randint(2, 99)
        return mcq("Quanto é %d × 100?" % n, num(n * 100), [num(n + 100), num(n * 10), num(n * 1000) if n < 10 else num(n * 100 + 100)],
                   "Multiplicar por 100: acrescente dois zeros à direita: <b>%s</b>." % num(n * 100))
    if k == "dez":
        a, b = R.randint(2, 5), R.randint(2, 9) * 10
        return mcq("Quanto é %d × %d?" % (a, b), num(a * b), [num(a * b // 10), num(a + b), num(a * b + 10)],
                   "%d × %d dezenas = %d dezenas = <b>%s</b>." % (a, b // 10, a * b // 10, num(a * b)))
    a, b = R.randint(2, 5), R.randint(1, 9) * 100
    return mcq("Quanto é %d × %s?" % (a, num(b)), num(a * b), [num(a * b // 10), num(a + b), num(a * b // 100)],
               "%d × %d centenas = %d centenas = <b>%s</b>." % (a, b // 100, a * b // 100, num(a * b)))


def s3_decompor():
    a = R.choice([2, 3, 4, 5])
    n = R.randint(12, 49)
    if n % 10 == 0:
        return None
    d, u = n // 10 * 10, n % 10
    p = a * n
    return mcq("Calcule %d × %d decompondo: %d × %d + %d × %d." % (a, n, a, d, a, u), num(p), [num(a * d), num(a * d + u), num(a * (d // 10) * 10 + a * u * 10) if a * u * 10 != p else num(p + 10)],
               "%d × %d = %d; %d × %d = %d; %d + %d = <b>%s</b>." % (a, d, a * d, a, u, a * u, a * d, a * u, num(p)))


def s3_armada():
    a = R.choice([2, 3, 4, 5])
    n = R.randint(13, 99) if a <= 3 else R.randint(13, 49)
    if n % 10 == 0:
        return None
    p = a * n
    sem_vai = (a * (n // 10)) * 10 + (a * (n % 10)) % 10
    return mcq(armada([str(n), str(a)], "×") + "Quanto é %d × %d?" % (n, a), num(p), [num(sem_vai) if sem_vai != p else None, num(p + 10), num(n + a), num(p - a)],
               "%d × %d = %d (escreve %d, vai %d); %d × %d + %d = %d. Resposta: <b>%s</b>." % (a, n % 10, a * (n % 10), a * (n % 10) % 10, a * (n % 10) // 10, a, n // 10, a * (n % 10) // 10, p // 10, num(p)))


def s4_falta():
    a = R.choice([2, 3, 4, 5, 10])
    b = R.randint(3, 12)
    p = a * b
    k = R.choice(["f", "maior"])
    if k == "f":
        return mcq("Que número falta? %d × ___ = %d" % (a, p), str(b), [str(p - a), str(b + 1), str(b - 1)],
                   "%d × %d = %d. Resposta: <b>%d</b>." % (a, b, p, b))
    x, y = R.randint(2, 5), R.randint(11, 25)
    v = x * y
    alt = [(x, y + 1), (x + 1, y - 1), (x, y - 2)]
    opts = ["%d × %d" % (x, y)] + ["%d × %d" % t for t in alt]
    best = max([(x, y)] + alt, key=lambda t: t[0] * t[1])
    ok = "%d × %d" % best
    return mcq("Qual multiplicação tem o maior resultado: %s?" % ", ".join(opts), ok, [o for o in opts if o != ok],
               "%s. O maior é <b>%s</b>." % ("; ".join("%s = %d" % ("%d × %d" % t, t[0] * t[1]) for t in [(x, y)] + alt), ok))


def s5_problema():
    p, _ = K.next()
    k = R.choice(["album", "caixa", "onibus", "preco", "pacotes", "carros", "semanas", "bombons"])
    if k == "album":
        a, b = R.randint(2, 5), R.randint(12, 30)
        return mcq("Um álbum tem %d páginas com %d figurinhas em cada. Quantas figurinhas cabem no álbum?" % (b, a), str(a * b), [str(a + b), str(a * b + a), str(a * b - b)],
                   "%d × %d = <b>%d</b>." % (b, a, a * b))
    if k == "caixa":
        a, b = R.randint(2, 5), R.choice([12, 15, 18, 20, 24, 25, 30])
        return mcq("Uma caixa tem %d lápis. Quantos lápis há em %d caixas?" % (b, a), str(a * b), [str(a + b), str(a * b + b), str(a * (b - 1))],
                   "%d × %d = <b>%d</b> lápis." % (a, b, a * b))
    if k == "onibus":
        a, b = R.randint(2, 5), R.choice([32, 36, 40, 42, 44, 45, 48])
        return mcq("Uma escola alugou %d ônibus. Cada ônibus leva %d alunos. Quantos alunos podem ir ao passeio?" % (a, b), num(a * b), [num(a + b), num(a * b + a), num(a * (b // 10) * 10)],
                   "%d × %d = <b>%s</b> alunos." % (a, b, num(a * b)))
    if k == "preco":
        a, b = R.randint(2, 5), R.randint(12, 35)
        return mcq("Um caderno custa %s. Quanto custam %d cadernos?" % (reais(b * 100), a), reais(a * b * 100), [reais((a + b) * 100), reais(a * (b // 10) * 1000), reais((a * b + b) * 100)],
                   "%d × %d = %d: <b>%s</b>." % (a, b, a * b, reais(a * b * 100)))
    if k == "pacotes":
        a = R.randint(2, 9)
        return mcq("Um pacote de pão de queijo tem 10 unidades. Quantos pães de queijo há em %d pacotes?" % a, str(10 * a), [str(10 + a), str(100 * a), str(10 * a + 10)],
                   "%d × 10 = <b>%d</b>." % (a, 10 * a))
    if k == "carros":
        a = R.randint(12, 25)
        return mcq("Num estacionamento há %d carros. Quantas rodas há ao todo nesses carros?" % a, str(4 * a), [str(a + 4), str(4 * a + 4), str(2 * a)],
                   "Cada carro tem 4 rodas: 4 × %d = <b>%d</b>." % (a, 4 * a))
    if k == "semanas":
        a = R.randint(2, 5)
        b = R.randint(15, 40)
        return mcq("%s lê %d páginas por semana. Quantas páginas lê em %d semanas?" % (p, b, a), str(a * b), [str(a + b), str(a * b + b), str(7 * a)],
                   "%d × %d = <b>%d</b> páginas." % (a, b, a * b))
    a = R.choice([3, 4, 5])
    b = R.randint(2, 4) * 5
    return mcq("Uma caixa de bombons tem %d fileiras com %d bombons em cada. Quantos bombons há em 2 caixas?" % (a, b), str(2 * a * b), [str(a * b), str(2 * (a + b)), str(a * b + 2)],
               "Em uma caixa: %d × %d = %d. Em 2 caixas: 2 × %d = <b>%d</b>." % (a, b, a * b, a * b, 2 * a * b))


def main():
    seen = set()
    sets = [
        ("Disposição retangular", mix(R, seen, [(s1_arranjo, 12), (s1_linhas, 8)])),
        ("Multiplicar por 10, 100 e números exatos", mix(R, seen, [(s2_dez, 20)])),
        ("Multiplicar decompondo", mix(R, seen, [(s3_decompor, 12), (s3_armada, 8)])),
        ("Fator que falta e comparar produtos", mix(R, seen, [(s4_falta, 12), (s3_armada, 8)])),
        ("Problemas de multiplicação", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Objetos arrumados em <b>linhas e colunas</b> (disposição retangular) se contam com multiplicação: 4 linhas com 6 em cada = 4 × 6 = 24.",
         "Para multiplicar por <b>10</b>, acrescente um zero à direita (23 × 10 = 230); por <b>100</b>, dois zeros (23 × 100 = 2.300).",
         "Para multiplicar um número de 2 algarismos, <b>decomponha</b>: 4 × 23 = 4 × 20 + 4 × 3 = 80 + 12 = 92.",
         "Na conta armada, multiplique primeiro as unidades. Se passar de 9, escreva as unidades e «vai» para as dezenas."],
        [("3 × 40", ["3 × 4 dezenas = 12 dezenas"], "120"),
         ("5 × 17", ["5 × 10 = 50", "5 × 7 = 35", "50 + 35"], "85")],
        [["4 × 23 = 80", "Faltou multiplicar as unidades: 4 × 3 = 12; 80 + 12 = 92."],
         ["23 × 10 = 33", "Multiplicar por 10 não é somar 10: 23 × 10 = 230."],
         ["Esquecer o «vai» na conta armada", "Escreva o número que vai em cima das dezenas."]],
        armada(["23", "4"], "×", result="92"))
    faq = [("Qual é a diferença entre tabuada e multiplicação?", "A tabuada são os fatos básicos (até 10 × 10). Na multiplicação usamos esses fatos para calcular contas maiores, como 4 × 23, e para resolver problemas."),
           ("Por que usar a disposição retangular?", "Ela mostra por que 3 × 5 = 5 × 3 (é só girar o retângulo) e prepara para o cálculo de área nos anos seguintes.")]
    make_unit(R, "multiplicacao", "N", ["EF03MA07"],
              "Resolver e elaborar problemas de multiplicação (por 2, 3, 4, 5 e 10) com os significados de adição de parcelas iguais e elementos apresentados em disposição retangular, utilizando diferentes estratégias de cálculo e registros",
              "Multiplicação: disposição retangular e decomposição", "Multiplicação",
              "Atividades de matemática para o 3º ano sobre multiplicação: disposição retangular, multiplicar por 10 e por 100, dezenas exatas, decomposição, conta armada e problemas. 100 exercícios com gabarito.",
              "4 × 23 = 4 × 20 + 4 × 3", "× 10: um zero à direita; × 100: dois zeros.",
              body, faq, sets, 8)


if __name__ == "__main__":
    main()
