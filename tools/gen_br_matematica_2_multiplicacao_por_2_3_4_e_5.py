# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: Multiplicação por 2, 3, 4 e 5 (Números, EF02MA07)
  python3 tools/gen_br_matematica_2_multiplicacao_por_2_3_4_e_5.py
Grupos iguais e adição de parcelas iguais (4 + 4 + 4 = 3 × 4); disposição retangular; tabuadas do 2, 3, 4 e 5;
contar de 2 em 2, de 3 em 3…; fator que falta; problemas com grupos iguais.
Erros: somar os números em vez de multiplicar (3 × 4 = 7), contar os grupos em vez dos objetos, trocar 3 × 5 por 3 + 5.
"""
import random
from br_common import mcq, lesson, make_unit, mix, arranjo, grupos, coisas, COISAS, KINDS, Kids

R = random.Random(80208)
K = Kids(R)
F = [2, 3, 4, 5]


def qt(kind):
    return "Quantas" if COISAS[kind][2] == "f" else "Quantos"


def s1_grupos():
    kind = R.choice(KINDS)
    g, k = R.randint(2, 5), R.choice(F)
    pic = grupos(g, k, kind)
    return mcq(pic + "São %d grupos com %d em cada. %s %s há ao todo?" % (g, k, qt(kind), COISAS[kind][1]), str(g * k), [str(g + k), str(g * k + k), str(g * k - 1)],
               "%s = %d × %d = <b>%d</b>." % (" + ".join([str(k)] * g), g, k, g * k))


def s1_parcelas():
    g, k = R.randint(2, 5), R.choice(F)
    sh = " + ".join([str(k)] * g)
    if R.random() < 0.5:
        return mcq("Qual multiplicação é igual a %s?" % sh, "%d × %d" % (g, k), ["%d × %d" % (g + 1, k), "%d + %d" % (g, k), "%d × %d" % (k, k) if g != k else "%d × %d" % (g, k + 1)],
                   "São %d parcelas iguais a %d: <b>%d × %d</b>." % (g, k, g, k))
    return mcq("Qual adição é igual a %d × %d?" % (g, k), sh, [" + ".join([str(k)] * (g + 1)), "%d + %d" % (g, k), " + ".join([str(g)] * (k + 1)) if g != k else " + ".join([str(k + 1)] * g)],
               "%d vezes o %d: <b>%s</b> = %d." % (g, k, sh, g * k))


def s2_arranjo():
    kind = R.choice(KINDS)
    r, c = R.randint(2, 5), R.choice(F)
    if r * c < 6:
        return None
    pic = arranjo(r, c, kind)
    if R.random() < 0.5:
        return mcq(pic + "%d linhas com %d em cada. %s %s há?" % (r, c, qt(kind), COISAS[kind][1]), str(r * c), [str(r + c), str(r * c + c), str(r * c - r)],
                   "%d × %d = <b>%d</b>." % (r, c, r * c))
    return mcq(pic + "Que multiplicação mostra a figura?", "%d × %d = %d" % (r, c, r * c), ["%d + %d = %d" % (r, c, r + c), "%d × %d = %d" % (r, c, r * c + 1), "%d × %d = %d" % (r + 1, c, (r + 1) * c)],
               "São %d linhas de %d: <b>%d × %d = %d</b>." % (r, c, r, c, r * c))


def s2_saltos():
    k = R.choice(F)
    n = R.randint(4, 8)
    seq = [k * i for i in range(1, n)]
    return mcq("Conte de %d em %d: %s, ___" % (k, k, ", ".join(map(str, seq))), str(k * n), [str(k * n + 1), str(k * (n + 1)), str(k * n - 1)],
               "Some %d: %d + %d = <b>%d</b>." % (k, k * (n - 1), k, k * n))


def s3_tabuada():
    a = R.randint(2, 10)
    k = R.choice(F)
    if R.random() < 0.5:
        a, k = k, a
    p = a * k
    w = [a + k, p + min(a, k), p - 1 if p > 2 else p + 2, p + 1]
    return mcq("Quanto é %d × %d?" % (a, k), str(p), [str(x) for x in w if x != p],
               "%d × %d = <b>%d</b>." % (a, k, p))


def s3_falta():
    k = R.choice(F)
    a = R.randint(3, 10)
    p = a * k
    if R.random() < 0.5:
        return mcq("Complete: %d × ___ = %d" % (k, p), str(a), [str(p - k), str(a + 1), str(a - 1)], "%d × %d = %d. Resposta: <b>%d</b>." % (k, a, p, a))
    return mcq("Complete: ___ × %d = %d" % (k, p), str(a), [str(p + k), str(a + 1), str(a - 1)], "%d × %d = %d. Resposta: <b>%d</b>." % (a, k, p, a))


def s4_comut():
    a, b = R.sample(range(2, 6), 2)
    if R.random() < 0.5:
        return mcq("Sabendo que %d × %d = %d, quanto é %d × %d?" % (a, b, a * b, b, a), str(a * b), [str(a + b), str(a * b + a), str(a * b - b)],
                   "A ordem dos fatores não muda o resultado: <b>%d</b>." % (a * b))
    k = R.choice(F)
    a = R.randint(2, 9)
    return mcq("Qual é maior: %d × %d ou %d × %d?" % (k, a, k, a + 1), "%d × %d" % (k, a + 1), ["%d × %d" % (k, a), "são iguais", "não dá para saber"],
               "%d × %d = %d e %d × %d = %d. Maior: <b>%d × %d</b>." % (k, a, k * a, k, a + 1, k * (a + 1), k, a + 1))


CENAS = [("Uma bicicleta tem 2 rodas. Quantas rodas têm {g} bicicletas?", 2, "rodas"),
         ("Um triciclo tem 3 rodas. Quantas rodas têm {g} triciclos?", 3, "rodas"),
         ("Um carro tem 4 rodas. Quantas rodas têm {g} carros?", 4, "rodas"),
         ("Uma mão tem 5 dedos. Quantos dedos há em {g} mãos?", 5, "dedos"),
         ("Um cachorro tem 4 patas. Quantas patas têm {g} cachorros?", 4, "patas"),
         ("Cada caixa tem 3 lápis. Quantos lápis há em {g} caixas?", 3, "lápis"),
         ("Cada prato tem 5 pães de queijo. Quantos pães de queijo há em {g} pratos?", 5, "pães de queijo"),
         ("Cada mesa tem 4 cadeiras. Quantas cadeiras há em {g} mesas?", 4, "cadeiras"),
         ("Cada pacote tem 2 meias. Quantas meias há em {g} pacotes?", 2, "meias"),
         ("Cada vaso tem 3 flores. Quantas flores há em {g} vasos?", 3, "flores"),
         ("Cada estrela-do-mar tem 5 braços. Quantos braços têm {g} estrelas-do-mar?", 5, "braços"),
         ("Um banco do parque tem lugar para 3 pessoas. Quantas pessoas cabem em {g} bancos?", 3, "pessoas")]


def s5_problema():
    t, k, u = R.choice(CENAS)
    g = R.randint(2, 9)
    if R.random() < 0.25:
        p, _ = K.next()
        n = R.randint(2, 5)
        price = R.choice(F)
        return mcq("%s comprou %d pirulitos de %d reais cada. Quanto gastou?" % (p, n, price), "%d reais" % (n * price), ["%d reais" % (n + price), "%d reais" % (n * price + price), "%d reais" % price],
                   "%d × %d = <b>%d reais</b>." % (n, price, n * price))
    return mcq(t.format(g=g), "%d %s" % (g * k, u), ["%d %s" % (g + k, u), "%d %s" % (g * k + k, u), "%d %s" % (g * k - 1, u)],
               "%d × %d = <b>%d %s</b>." % (g, k, g * k, u))


def main():
    seen = set()
    sets = [
        ("Grupos iguais", mix(R, seen, [(s1_grupos, 12), (s1_parcelas, 8)])),
        ("Linhas e colunas e contar de tanto em tanto", mix(R, seen, [(s2_arranjo, 12), (s2_saltos, 8)])),
        ("Tabuadas do 2, 3, 4 e 5", mix(R, seen, [(s3_tabuada, 14), (s3_falta, 6)])),
        ("Fator que falta e ordem dos fatores", mix(R, seen, [(s3_falta, 10), (s4_comut, 10)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Multiplicar é somar <b>parcelas iguais</b>: 4 + 4 + 4 = 3 × 4 = 12.",
         "Leia 3 × 4 como «3 vezes o 4»: 3 grupos com 4 em cada.",
         "Numa disposição em linhas e colunas, multiplique as linhas pelas colunas.",
         "A ordem não muda o resultado: 3 × 4 = 4 × 3."],
        [("5 grupos de 2", ["2 + 2 + 2 + 2 + 2"], "5 × 2 = 10"),
         ("4 carros, 4 rodas cada", ["4 + 4 + 4 + 4"], "16 rodas")],
        [["Somar os números: 3 × 4 = 7", "São 3 grupos de 4: 4 + 4 + 4 = 12."],
         ["Contar só os grupos", "Conte os objetos de todos os grupos."],
         ["Pular um número ao contar de 3 em 3", "Some 3 de cada vez: 3, 6, 9, 12."]],
        grupos(3, 4, "star"))
    faq = [("Quais tabuadas o 2º ano estuda?", "A BNCC pede problemas de multiplicação por 2, 3, 4 e 5 com a ideia de adição de parcelas iguais, usando desenhos e materiais."),
           ("Como começar a multiplicação com a criança?", "Use objetos em grupos: 3 pratos com 4 biscoitos cada. Conte de 4 em 4 e depois mostre que 3 × 4 = 12.")]
    make_unit(R, "multiplicacao-por-2-3-4-e-5", "N", ["EF02MA07"],
              "Resolver e elaborar problemas de multiplicação (por 2, 3, 4 e 5) com a ideia de adição de parcelas iguais por meio de estratégias e formas de registro pessoais, utilizando ou não suporte de imagens e/ou material manipulável",
              "Multiplicação por 2, 3, 4 e 5", "Multiplicação",
              "Atividades de matemática para o 2º ano sobre multiplicação por 2, 3, 4 e 5: grupos iguais, adição de parcelas iguais, linhas e colunas, tabuadas e problemas. 100 exercícios com gabarito.",
              "3 × 4 = 4 + 4 + 4.", "3 grupos com 4 em cada.",
              body, faq, sets, 8, grade="2-ano")


if __name__ == "__main__":
    main()
