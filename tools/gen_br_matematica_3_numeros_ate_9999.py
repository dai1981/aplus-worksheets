# -*- coding: utf-8 -*-
"""
Brasil Matemática 3º ano: Números até 9.999 (Números, EF03MA01, EF03MA02)
  python3 tools/gen_br_matematica_3_numeros_ate_9999.py
Unidades de milhar, centenas, dezenas e unidades; material dourado e quadro de valor posicional; ler e escrever
números por extenso; composição e decomposição; algarismo e valor posicional; quantas dezenas/centenas ao todo.
Erros: esquecer o zero (3 UM e 5 D → 350), confundir algarismo e número de dezenas, trocar a ordem dos algarismos.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, material_dourado, quadro_valor, extenso, pl, reais

R = random.Random(80301)


def four():
    return R.randint(1001, 9999)


def parts(n):
    return n // 1000, n // 100 % 10, n // 10 % 10, n % 10


def wrong(n):
    m, c, d, u = parts(n)
    out = []
    z = int("".join(str(x) for x in (m, c, d, u) if x))
    if z != n:
        out.append(z)
    out += [m * 1000 + d * 100 + c * 10 + u if c != d else None, m * 1000 + c * 100 + u * 10 + d if d != u else None,
            n + 1000 if n < 9000 else n - 1000, n + 100 if n % 1000 < 900 else n - 100, n + 10, n - 1, c * 1000 + m * 100 + d * 10 + u if c else None]
    return [num(x) for x in out if x and 0 < x < 10000 and x != n]


def s1_material():
    m, c, d, u = R.randint(1, 3), R.randint(0, 4), R.randint(0, 6), R.randint(0, 9)
    n = 1000 * m + 100 * c + 10 * d + u
    return mcq(material_dourado(m, c, d, u) + "Que número o material dourado representa?", num(n), wrong(n),
               "%s, %s, %s e %s: <b>%s</b>." % (pl(m, "milhar", "milhares"), pl(c, "centena", "centenas"), pl(d, "dezena", "dezenas"), pl(u, "unidade", "unidades"), num(n)))


def s1_quadro():
    n = four()
    if R.random() < 0.5:
        k = R.choice([1, 2])
        n = n // 10 * 10 if k == 1 else n // 1000 * 1000 + n % 100
    return mcq(quadro_valor(n) + "Que número está escrito no quadro de valor posicional?", num(n), wrong(n),
               "Leia os algarismos da esquerda para a direita: UM, C, D, U. O número é <b>%s</b>." % num(n))


def s1_partes():
    m, c, d, u = R.randint(1, 9), R.choice([0, R.randint(1, 9)]), R.choice([0, R.randint(1, 9)]), R.choice([0, R.randint(1, 9)])
    n = 1000 * m + 100 * c + 10 * d + u
    words = [pl(v, a, b) for v, a, b in ((m, "unidade de milhar", "unidades de milhar"), (c, "centena", "centenas"), (d, "dezena", "dezenas"), (u, "unidade", "unidades")) if v]
    if len(words) < 2:
        return None
    return mcq("Que número tem " + ", ".join(words[:-1]) + " e " + words[-1] + "?", num(n), wrong(n),
               "Coloque cada quantidade na sua ordem (UM, C, D, U) e escreva 0 nas ordens vazias: <b>%s</b>." % num(n))


def s2_do_extenso():
    n = four()
    if R.random() < 0.4:
        n = n // 100 * 100 if R.random() < 0.5 else n // 1000 * 1000 + n % 100
    return mcq("Escreva com algarismos: <b>%s</b>." % extenso(n), num(n), wrong(n),
               "«%s» se escreve <b>%s</b>." % (extenso(n), num(n)))


def s2_por_extenso():
    n = four()
    m, c, d, u = parts(n)
    w = [n + 100 if c < 9 else n - 100, n + 10 if d < 9 else n - 10, n + 1000 if m < 9 else n - 1000, m * 1000 + d * 100 + c * 10 + u]
    return mcq("Como se escreve %s por extenso?" % num(n), extenso(n), [extenso(x) for x in w if 0 < x < 10000 and x != n],
               "%s se escreve <b>%s</b>." % (num(n), extenso(n)))


def s3_decompor():
    n = four()
    m, c, d, u = parts(n)
    if (c, d, u).count(0) > 1:
        return None
    terms = [v for v in (1000 * m, 100 * c, 10 * d, u) if v]
    sh = " + ".join(num(t) for t in terms)
    if R.random() < 0.5:
        return mcq("Que número é igual a %s?" % sh, num(n), wrong(n), "%s = <b>%s</b>." % (sh, num(n)))
    w1 = " + ".join(num(t) for t in (1000 * m, 100 * c, d, u) if t)
    w2 = " + ".join(num(t) for t in (100 * m, 100 * c, 10 * d, u) if t)
    w3 = " + ".join(num(t) for t in (1000 * m, 10 * c, 100 * d, u) if t)
    return mcq("Qual é a decomposição de %s?" % num(n), sh, [w1, w2, w3],
               "%s = %s: <b>%s</b>." % (num(n), ", ".join([pl(m, "milhar", "milhares"), pl(c, "centena", "centenas"), pl(d, "dezena", "dezenas"), pl(u, "unidade", "unidades")]), sh))


def s3_algarismo():
    n = four()
    m, c, d, u = parts(n)
    if len({m, c, d, u}) < 4:
        return None
    k = R.choice(["m", "c", "d", "u", "v", "v"])
    if k == "v":
        pos = R.choice([(c, 100, "centenas"), (d, 10, "dezenas"), (m, 1000, "unidades de milhar")])
        a, v, nome = pos
        return mcq("Em %s, quanto vale o algarismo %d?" % (num(n), a), num(a * v), [str(a), num(a * 10) if v != 10 else num(a * 100), num(a * 1000) if v != 1000 else num(a * 100)],
                   "O %d está na ordem das %s, então vale <b>%s</b>." % (a, nome, num(a * v)))
    nomes = {"m": ("unidades de milhar", m), "c": ("centenas", c), "d": ("dezenas", d), "u": ("unidades", u)}
    nome, a = nomes[k]
    return mcq("Qual é o algarismo das %s em %s?" % (nome, num(n)), str(a), [str(x) for x in (m, c, d, u) if x != a],
               "Na ordem das %s de %s está o algarismo <b>%d</b>." % (nome, num(n), a))


def s4_ao_todo():
    n = four()
    k = R.choice(["d", "c"])
    if k == "d":
        return mcq("Quantas dezenas há ao todo em %s?" % num(n), num(n // 10), [str(n // 10 % 10), num(n // 100), num(n // 10 + 1)],
                   "%s = %s dezenas e %d unidades. Há <b>%s</b> dezenas ao todo (o algarismo das dezenas é só %d)." % (num(n), num(n // 10), n % 10, num(n // 10), n // 10 % 10))
    return mcq("Quantas centenas há ao todo em %s?" % num(n), str(n // 100), [str(n // 100 % 10), str(n // 1000), num(n // 10)],
               "%s = %d centenas e %d. Há <b>%d</b> centenas ao todo." % (num(n), n // 100, n % 100, n // 100))


def s4_troca():
    k = R.choice(["d", "c", "m"])
    if k == "d":
        a = R.randint(11, 99)
        return mcq("%d dezenas formam que número?" % a, num(a * 10), [num(a), num(a * 100), num(a + 10)],
                   "Cada dezena vale 10: %d × 10 = <b>%s</b>." % (a, num(a * 10)))
    if k == "c":
        a = R.randint(11, 99)
        return mcq("%d centenas formam que número?" % a, num(a * 100), [num(a * 10), num(a * 1000) if a < 10 else num(a + 100), num(a)],
                   "Cada centena vale 100: %d × 100 = <b>%s</b>." % (a, num(a * 100)))
    a = R.randint(2, 9)
    b = R.randint(1, 9)
    return mcq("%s e %s formam que número?" % (pl(a, "milhar", "milhares"), pl(b, "centena", "centenas")), num(a * 1000 + b * 100),
               [num(a * 1000 + b * 10), num(a * 100 + b * 10), num(a * 1000 + b)],
               "%s + %s = <b>%s</b>." % (num(a * 1000), num(b * 100), num(a * 1000 + b * 100)))


def s5_problema():
    k = R.choice(["notas", "caixas", "pacotes", "livros", "adivinha"])
    if k == "notas":
        m, c, d = R.randint(1, 9), R.randint(1, 9), R.randint(1, 9)
        tot = 100 * m + 10 * c + d
        return mcq("No cofrinho há %s de R$ 100, %s de R$ 10 e %s de R$ 1. Quantos reais há ao todo?" % (
                       pl(m, "cédula", "cédulas"), pl(c, "cédula", "cédulas"), pl(d, "moeda", "moedas")),
                   reais(tot * 100), [reais((m + c + d) * 100), reais((100 * m + c + 10 * d) * 100), reais((10 * m + 10 * c + d) * 100)],
                   "%s + %s + %s = <b>%s</b>." % (reais(100 * m * 100), reais(10 * c * 100), reais(d * 100), reais(tot * 100)))
    n = R.randint(1100, 9900)
    if k == "caixas":
        return mcq("Uma fábrica fez %s biscoitos e os coloca em caixas de 10. Quantas caixas cheias ela consegue?" % num(n), num(n // 10),
                   [str(n // 10 % 10), num(n // 100), num(n // 10 + 1)],
                   "Em %s há %s dezenas: <b>%s</b> caixas cheias." % (num(n), num(n // 10), num(n // 10)))
    if k == "pacotes":
        return mcq("Uma papelaria tem %s folhas e faz pacotes de 100. Quantos pacotes completos ela faz?" % num(n), str(n // 100),
                   [num(n // 10), str(n % 100), str(n // 100 + 1)],
                   "Em %s há %d centenas: <b>%d</b> pacotes completos." % (num(n), n // 100, n // 100))
    if k == "livros":
        a = R.randint(1, 8)
        b = R.randint(1, 9)
        tot = 1000 * a + 100 * b
        return mcq("Uma biblioteca tinha %s livros e recebeu mais %s. Quantos livros ela tem agora?" % (num(tot), num(1000)), num(tot + 1000),
                   [num(tot + 100), num(tot + 10), num(tot - 1000)],
                   "Somar 1.000 muda só o algarismo das unidades de milhar: <b>%s</b>." % num(tot + 1000))
    m, c, d, u = R.randint(1, 9), R.randint(0, 9), R.randint(0, 9), R.randint(0, 9)
    if len({m, c, d, u}) < 4:
        return None
    n = 1000 * m + 100 * c + 10 * d + u
    pistas = ["meu algarismo das unidades de milhar é %d" % m, "meu algarismo das centenas é %d" % c, "meu algarismo das dezenas é %d" % d, "meu algarismo das unidades é %d" % u]
    R.shuffle(pistas)
    return mcq("Adivinha: %s. Quem sou eu?" % "; ".join(pistas), num(n), wrong(n),
               "Coloque cada algarismo na sua ordem: UM = %d, C = %d, D = %d, U = %d. O número é <b>%s</b>." % (m, c, d, u, num(n)))


def main():
    seen = set()
    sets = [
        ("Milhares, centenas, dezenas e unidades", mix(R, seen, [(s1_material, 8), (s1_quadro, 6), (s1_partes, 6)])),
        ("Ler e escrever números", mix(R, seen, [(s2_do_extenso, 10), (s2_por_extenso, 10)])),
        ("Decompor e valor posicional", mix(R, seen, [(s3_decompor, 10), (s3_algarismo, 10)])),
        ("Trocas e agrupamentos", mix(R, seen, [(s4_ao_todo, 10), (s4_troca, 10)])),
        ("Adivinhas e problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Um número até 9.999 tem no máximo <b>4 algarismos</b>: unidades de milhar (UM), centenas (C), dezenas (D) e unidades (U).",
         "10 unidades = 1 dezena; 10 dezenas = 1 centena; 10 centenas = 1 milhar (1.000).",
         "Se uma ordem fica vazia, escreva <b>0</b>: 3 milhares e 5 dezenas formam 3.050.",
         "O <b>algarismo</b> das dezenas de 4.372 é 7, mas o <b>número</b> de dezenas ao todo é 437."],
        [("Escreva o número: 6 milhares, 2 centenas e 9 unidades.", ["UM = 6, C = 2, D = 0, U = 9"], "6.209"),
         ("Decomponha 5.708.", ["5 milhares, 7 centenas, 0 dezena, 8 unidades"], "5.000 + 700 + 8")],
        [["Esquecer o zero: 3 UM e 5 D → 35", "Escreva 0 em cada ordem vazia: 3.050."],
         ["Confundir algarismo e número de dezenas", "O algarismo é um só; o número de dezenas conta também as dezenas que estão nas centenas e nos milhares."],
         ["Trocar a ordem: 4.372 → 4.732", "Leia as ordens em sequência: UM, C, D, U."]],
        quadro_valor(4372))
    faq = [("Até que número se trabalha no 3º ano?", "A BNCC indica números até a ordem da unidade de milhar, ou seja, até 9.999: ler, escrever, comparar, compor e decompor."),
           ("Por que usar o material dourado?", "O cubinho, a barra, a placa e o cubo grande mostram que cada ordem vale 10 vezes a anterior. Isso ajuda a entender as trocas na adição e na subtração.")]
    make_unit(R, "numeros-ate-9999", "N", ["EF03MA01", "EF03MA02"],
              "Ler, escrever e comparar números naturais até a ordem de unidade de milhar, estabelecendo relações entre os registros numéricos e em língua materna; identificar características do sistema de numeração decimal, utilizando a composição e a decomposição de número natural de até quatro ordens",
              "Números até 9.999: milhar, centena, dezena e unidade", "Números até 9.999",
              "Atividades de matemática para o 3º ano sobre números até 9.999: material dourado, quadro de valor posicional, números por extenso, decomposição e valor do algarismo. 100 exercícios com gabarito.",
              "Cada algarismo vale conforme a sua ordem: UM, C, D, U.", "Nas ordens vazias escreva 0.",
              body, faq, sets, 1)


if __name__ == "__main__":
    main()
