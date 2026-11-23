# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: Números até 1.000 (Números, EF02MA01)
  python3 tools/gen_br_matematica_2_numeros_ate_1000.py
Centenas, dezenas e unidades com material dourado e quadro de valor posicional; ler e escrever números por extenso;
valor do algarismo; trocas (10 unidades = 1 dezena, 10 dezenas = 1 centena); problemas com cédulas e caixas.
Erros: esquecer o zero (3 centenas e 5 unidades → 35), trocar a ordem dos algarismos, confundir 10 dezenas com 10.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, quadro_valor, extenso, pl, reais
from br_2 import parts, wrong, md, cdu

R = random.Random(80201)


def three():
    return R.randint(101, 999)


def s1_material():
    c, d, u = R.randint(1, 5), R.randint(0, 7), R.randint(0, 9)
    n = 100 * c + 10 * d + u
    return mcq(md(c, d, u) + "Que número o material dourado mostra?", num(n), wrong(n),
               "Placa = 100, barra = 10, cubinho = 1. %s: <b>%s</b>." % (cdu(c, d, u), num(n)))


def s1_quadro():
    n = three()
    if R.random() < 0.4:
        n = n // 10 * 10 if R.random() < 0.5 else n // 100 * 100 + n % 10
    return mcq(quadro_valor(n, 3) + "Que número está no quadro?", num(n), wrong(n),
               "Leia C, D e U da esquerda para a direita: <b>%s</b>." % num(n))


def s1_partes():
    c, d, u = R.randint(1, 9), R.choice([0, R.randint(1, 9)]), R.choice([0, R.randint(1, 9)])
    if not d and not u:
        return None
    n = 100 * c + 10 * d + u
    return mcq("Que número tem %s?" % cdu(c, d, u), num(n), wrong(n),
               "Escreva cada algarismo na sua ordem e 0 na ordem vazia: <b>%s</b>." % num(n))


def s2_do_extenso():
    n = three()
    if R.random() < 0.35:
        n = n // 100 * 100 + n % 10 if R.random() < 0.5 else n // 10 * 10
    return mcq("Escreva com algarismos: <b>%s</b>." % extenso(n), num(n), wrong(n), "«%s» = <b>%s</b>." % (extenso(n), num(n)))


def s2_por_extenso():
    n = three()
    c, d, u = parts(n)
    w = [n + 100 if c < 9 else n - 100, n + 10 if d < 9 else n - 10, c * 100 + u * 10 + d, n + 1 if u < 9 else n - 1]
    return mcq("Como se escreve %s por extenso?" % num(n), extenso(n), [extenso(x) for x in w if 100 < x < 1000 and x != n],
               "%s se escreve <b>%s</b>." % (num(n), extenso(n)))


def s3_algarismo():
    n = three()
    c, d, u = parts(n)
    if len({c, d, u}) < 3:
        return None
    k = R.choice(["c", "d", "u", "v", "v"])
    if k == "v":
        a, v, nome = R.choice([(c, 100, "centenas"), (d, 10, "dezenas")])
        return mcq("No número %s, quanto vale o algarismo %d?" % (num(n), a), num(a * v), [str(a), num(a * 10) if v == 100 else num(a * 100), num(a * 1000) if a * 1000 <= 999 else str(a + v)],
                   "O %d está na ordem das %s. Ele vale <b>%s</b>." % (a, nome, num(a * v)))
    nome, a = {"c": ("centenas", c), "d": ("dezenas", d), "u": ("unidades", u)}[k]
    return mcq("Qual é o algarismo das %s em %s?" % (nome, num(n)), str(a), [str(x) for x in (c, d, u) if x != a] + [str((a + 1) % 10)],
               "Em %s, o algarismo das %s é <b>%d</b>." % (num(n), nome, a))


def s3_ao_todo():
    n = three()
    if R.random() < 0.6:
        return mcq("Quantas dezenas há ao todo em %s?" % num(n), str(n // 10), [str(n // 10 % 10), str(n // 100), str(n // 10 + 1)],
                   "%s = %d dezenas e %d unidades. Ao todo: <b>%d dezenas</b>." % (num(n), n // 10, n % 10, n // 10))
    return mcq("Quantas centenas inteiras há em %s?" % num(n), str(n // 100), [str(n // 10), str(n % 10) if n % 10 != n // 100 else str(n // 100 + 2), str(n // 100 + 1)],
               "%s = %d centenas e %d. Há <b>%d centenas</b>." % (num(n), n // 100, n % 100, n // 100))


def s4_troca():
    k = R.choice(["u", "d", "dd", "c", "uu"])
    if k == "u":
        return mcq("10 unidades formam…", "1 dezena", ["1 centena", "10 dezenas", "100 unidades"], "10 unidades = <b>1 dezena</b>.")
    if k == "d":
        a = R.randint(11, 99)
        return mcq("%d dezenas formam que número?" % a, num(a * 10), [str(a), num(a * 100) if a < 10 else str(a + 10), num(a * 10 + 1)],
                   "Cada dezena vale 10: %d × 10 = <b>%s</b>." % (a, num(a * 10)))
    if k == "dd":
        a = R.randint(2, 9)
        return mcq("%d centenas formam quantas dezenas?" % a, str(a * 10), [str(a), str(a * 100), str(a + 10)],
                   "1 centena = 10 dezenas. %d centenas = <b>%d dezenas</b>." % (a, a * 10))
    if k == "c":
        a = R.randint(2, 9)
        return mcq("%s formam que número?" % pl(a, "centena", "centenas"), num(a * 100), [str(a * 10), str(a), num(a * 100 + 10)],
                   "Cada centena vale 100: <b>%s</b>." % num(a * 100))
    a = R.randint(2, 9)
    b = R.randint(11, 19)
    return mcq("%s e %d unidades formam que número?" % (pl(a, "dezena", "dezenas"), b), str(a * 10 + b), [str(a * 10 + b - 10), "%d%d" % (a, b), str(a + b)],
               "%d dezenas = %d. %d + %d = <b>%d</b>." % (a, a * 10, a * 10, b, a * 10 + b))


def s4_saltos():
    k = R.choice([10, 100])
    if k == 10:
        a = R.randint(10, 89) * 10 + R.choice([0, R.randint(1, 9)])
        seq = [a + 10 * i for i in range(4)]
    else:
        a = R.randint(1, 5) * 100 + R.randint(0, 99)
        seq = [a + 100 * i for i in range(4)]
    if seq[-1] + k > 1000:
        return None
    nxt = seq[-1] + k
    return mcq("Conte de %d em %d: %s, ___. Qual é o próximo?" % (k, k, ", ".join(num(x) for x in seq)), num(nxt),
               [num(seq[-1] + 1), num(seq[-1] + (100 if k == 10 else 10)), num(nxt + k)],
               "Somar %d muda só o algarismo das %s: <b>%s</b>." % (k, "dezenas" if k == 10 else "centenas", num(nxt)))


def s5_problema():
    k = R.choice(["notas", "caixas", "pacotes", "adivinha", "figurinhas"])
    if k == "notas":
        c, d, u = R.randint(1, 5), R.randint(1, 9), R.randint(1, 9)
        tot = 100 * c + 10 * d + u
        return mcq("No cofrinho há %s de R$ 100, %s de R$ 10 e %s de R$ 1. Quantos reais há?" % (pl(c, "cédula", "cédulas"), pl(d, "cédula", "cédulas"), pl(u, "moeda", "moedas")),
                   reais(tot * 100), [reais((c + d + u) * 100), reais((100 * c + d + 10 * u) * 100), reais((10 * c + 10 * d + u) * 100)],
                   "%s + %s + %s = <b>%s</b>." % (reais(c * 10000), reais(d * 1000), reais(u * 100), reais(tot * 100)))
    n = R.randint(120, 990)
    if k == "caixas":
        return mcq("Há %s ovos. Em cada caixa cabem 10. Quantas caixas ficam cheias?" % num(n), str(n // 10), [str(n // 10 % 10), str(n // 100), str(n // 10 + 1)],
                   "%s tem %d dezenas. Ficam cheias <b>%d caixas</b>." % (num(n), n // 10, n // 10))
    if k == "pacotes":
        return mcq("Uma escola tem %s folhas. Ela faz pacotes de 100. Quantos pacotes completos faz?" % num(n), str(n // 100), [str(n // 10), str(n % 100), str(n // 100 + 1)],
                   "%s tem %d centenas. São <b>%d pacotes</b>." % (num(n), n // 100, n // 100))
    if k == "figurinhas":
        c, d = R.randint(1, 8), R.randint(1, 9)
        return mcq("Léo tem %s de 100 figurinhas e %s de 10. Quantas figurinhas ele tem?" % (pl(c, "pacote", "pacotes"), pl(d, "pacote", "pacotes")), num(100 * c + 10 * d),
                   [str(c + d), num(10 * c + d), num(100 * c + d)], "%d + %d = <b>%s</b>." % (100 * c, 10 * d, num(100 * c + 10 * d)))
    c, d, u = R.randint(1, 9), R.randint(0, 9), R.randint(0, 9)
    if len({c, d, u}) < 3:
        return None
    n = 100 * c + 10 * d + u
    p = ["minhas centenas são %d" % c, "minhas dezenas são %d" % d, "minhas unidades são %d" % u]
    R.shuffle(p)
    return mcq("Adivinha: %s. Que número sou eu?" % "; ".join(p), num(n), wrong(n), "C = %d, D = %d, U = %d: <b>%s</b>." % (c, d, u, num(n)))


def main():
    seen = set()
    sets = [
        ("Centenas, dezenas e unidades", mix(R, seen, [(s1_material, 8), (s1_quadro, 6), (s1_partes, 6)])),
        ("Ler e escrever números", mix(R, seen, [(s2_do_extenso, 10), (s2_por_extenso, 10)])),
        ("O valor de cada algarismo", mix(R, seen, [(s3_algarismo, 12), (s3_ao_todo, 8)])),
        ("Trocas e contagens", mix(R, seen, [(s4_troca, 10), (s4_saltos, 10)])),
        ("Problemas com números até 1.000", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["10 unidades formam 1 <b>dezena</b>. 10 dezenas formam 1 <b>centena</b>. 10 centenas formam 1.000 (mil).",
         "No material dourado: cubinho = 1, barra = 10, placa = 100.",
         "Num número de 3 algarismos, leia da esquerda: centenas, dezenas, unidades.",
         "Se uma ordem fica vazia, escreva <b>0</b>: 4 centenas e 7 unidades = 407."],
        [("2 placas, 3 barras e 5 cubinhos", ["200 + 30 + 5"], "235"),
         ("Seiscentos e oito", ["6 centenas, 0 dezena, 8 unidades"], "608")],
        [["Escrever 47 para 4 centenas e 7 unidades", "Ponha 0 nas dezenas: 407."],
         ["Ler 352 como 253", "As centenas vêm primeiro, à esquerda."],
         ["Achar que 10 dezenas é 10", "10 dezenas = 100."]],
        md(2, 3, 5))
    faq = [("O que o 2º ano aprende sobre números?", "A BNCC pede comparar e ordenar números até a ordem das centenas, entendendo o valor posicional, e ler e escrever esses números."),
           ("Como ajudar a criança com centenas, dezenas e unidades?", "Use palitos ou tampinhas: faça montinhos de 10 (dezenas) e juntos de 10 montinhos (centenas). Depois escreva o número que formou.")]
    make_unit(R, "numeros-ate-1000", "N", ["EF02MA01"],
              "Comparar e ordenar números naturais (até a ordem de centenas) pela compreensão de características do sistema de numeração decimal (valor posicional e função do zero)",
              "Números até 1.000: centenas, dezenas e unidades", "Números até 1.000",
              "Atividades de matemática para o 2º ano sobre números até 1.000: centenas, dezenas e unidades, material dourado, quadro de valor, números por extenso e valor do algarismo. 100 exercícios com gabarito.",
              "10 dezenas = 1 centena.", "Placa = 100, barra = 10, cubinho = 1.",
              body, faq, sets, 1, grade="2-ano")


if __name__ == "__main__":
    main()
