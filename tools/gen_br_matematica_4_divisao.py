# -*- coding: utf-8 -*-
"""
Brasil Matemática 4º ano: Divisão (Números, EF04MA07)
  python3 tools/gen_br_matematica_4_divisao.py
Divisão com divisor de até 2 algarismos: repartição em partes iguais («para cada um») e medida («quantas vezes cabe»);
dividir por 10, 100 e dezenas exatas; método da chave, quociente e resto; prova real; o que fazer com o resto; problemas.
Erros: esquecer o zero no quociente, deixar resto maior que o divisor, ignorar o resto num problema de ônibus.
"""
import random
from br_common import mcq, lesson, make_unit, mix, grupos, KINDS, COISAS, Kids, use, lim

R = random.Random(80406)
K = Kids(R)
L = (lim(99999, 0),)
D5 = "gen_br_matematica_5_divisao"
s_dez, s_exatas, s_um, s_dois, s_prova, s_resto, s_prob5 = use(D5, 80946, "s1_dez", "s1_exatas", "s2_um", "s2_dois", "s3_prova", "s4_resto", "s5_problema", preds=L)


def chave(a, b):
    import gen_br_matematica_5_divisao as D
    return D.chave(a, b)


def s1_grupos():
    g, k = R.randint(2, 6), R.randint(2, 8)
    kind = R.choice(KINDS)
    s, p, gen = COISAS[kind]
    t = g * k
    if g == k or t < 10:
        return None
    if R.random() < 0.5:
        return mcq(grupos(g, k, kind) + "%d %s foram repartid%s igualmente em %d grupos. Quant%s ficam em cada grupo?" % (t, p, "as" if gen == "f" else "os", g, "as" if gen == "f" else "os"),
                   str(k), [str(g), str(t - g), str(k + 1)], "Repartir em partes iguais: %d ÷ %d = <b>%d</b>." % (t, g, k))
    return mcq(grupos(g, k, kind) + "Temos %d %s e fazemos grupos de %d. Quantos grupos formamos?" % (t, p, k), str(g), [str(k), str(t - k), str(g + 1)],
               "Quantas vezes o %d cabe em %d? %d ÷ %d = <b>%d grupos</b>." % (k, t, t, k, g))


def s1_ideia():
    t = R.randint(4, 12) * R.choice([6, 8, 12])
    k = R.choice(["rep", "med"])
    d = R.choice([x for x in (2, 3, 4, 6, 8, 12) if t % x == 0])
    if k == "rep":
        return mcq("%d bombons serão repartidos igualmente entre %d crianças. Que conta resolve o problema e qual é a resposta?" % (t, d), "%d ÷ %d = %d bombons para cada uma" % (t, d, t // d),
                   ["%d × %d = %d bombons para cada uma" % (t, d, t * d), "%d − %d = %d bombons para cada uma" % (t, d, t - d), "%d ÷ %d = %d crianças" % (t, d, t // d)],
                   "Repartir igualmente é dividir: <b>%d ÷ %d = %d</b> bombons para cada uma." % (t, d, t // d))
    return mcq("Um pacote tem %d bombons. Quantas caixas de %d bombons dá para encher?" % (t, d), "%d caixas" % (t // d), ["%d caixas" % x for x in (t * d, t - d, t // d + 1)],
               "Quantas vezes o %d cabe em %d? %d ÷ %d = <b>%d caixas</b>." % (d, t, t, d, t // d))


def s5_problema():
    k = R.choice(["turma", "figur", "km", "garrafas", "doacao", "fita"])
    p, g = K.next()
    if k == "turma":
        n, q = R.randint(20, 36), R.randint(4, 6)
        if n % q:
            return None
        return mcq("A professora dividiu %d alunos em grupos de %d. Quantos grupos formou?" % (n, q), str(n // q), [str(n - q), str(n * q), str(n // q + 1)],
                   "%d ÷ %d = <b>%d grupos</b>." % (n, q, n // q))
    if k == "figur":
        n, q = R.randint(3, 9), R.randint(12, 45)
        return mcq("%s quer repartir %d figurinhas igualmente entre %d amigos. Quantas cada amigo recebe?" % (p, n * q, n), str(q), [str(n * q - n), str(q + 1), str(n)],
                   "%d ÷ %d = <b>%d</b>; conferindo: %d × %d = %d." % (n * q, n, q, q, n, n * q))
    if k == "km":
        d, v = R.randint(11, 25), R.randint(12, 60)
        return mcq("Um ciclista pedalou %s km em %d dias, a mesma distância por dia. Quantos quilômetros pedalou por dia?" % (d * v, d), "%d km" % v,
                   ["%d km" % x for x in (v + 1, d, d * v - d)], "%d ÷ %d = <b>%d km</b>." % (d * v, d, v))
    if k == "garrafas":
        c, n = R.choice([6, 12, 24]), R.randint(8, 40)
        return mcq("Uma loja recebeu %d garrafas de água e vai arrumar em pacotes de %d. Quantos pacotes vai montar?" % (c * n, c), str(n), [str(c * n - c), str(n + 1), str(c)],
                   "%d ÷ %d = <b>%d pacotes</b>." % (c * n, c, n))
    if k == "doacao":
        f, q = R.randint(11, 30), R.randint(20, 80)
        return mcq("Uma campanha juntou %d quilos de alimentos e vai dividi-los igualmente entre %d famílias. Quantos quilos cada família recebe?" % (f * q, f), "%d kg" % q,
                   ["%d kg" % x for x in (q + 1, f, f * q - f)], "%d ÷ %d = <b>%d kg</b>." % (f * q, f, q))
    c = R.choice([15, 20, 25, 30, 40, 50])
    n = R.randint(5, 30)
    r = R.randint(1, c - 1)
    t = c * n + r
    return mcq("Um rolo tem %d cm de fita. Quantos pedaços de %d cm dá para cortar, e quanto sobra?" % (t, c), "%d pedaços e sobram %d cm" % (n, r),
               ["%d pedaços e sobram %d cm" % (n + 1, r), "%d pedaços e sobram %d cm" % (n, c - r), "%d pedaços e não sobra nada" % n],
               "%d ÷ %d = %d e resto %d: <b>%d pedaços e sobram %d cm</b>." % (t, c, n, r, n, r))


def main():
    seen = set()
    sets = [
        ("Repartir e medir", mix(R, seen, [(s1_grupos, 10), (s1_ideia, 10)])),
        ("Dividir por 10, 100 e dezenas exatas", mix(R, seen, [(s_dez, 12), (s_exatas, 8)])),
        ("Método da chave", mix(R, seen, [(s_um, 10), (s_dois, 10)])),
        ("Resto e prova real", mix(R, seen, [(s_prova, 8), (s_resto, 12)])),
        ("Problemas", mix(R, seen, [(s5_problema, 12), (s_prob5, 8)])),
    ]
    body = lesson(
        ["A divisão tem duas ideias: <b>repartir</b> em partes iguais (quanto fica para cada um) e <b>medir</b> (quantas vezes um número cabe no outro).",
         "Dividir por 10 ou 100 é tirar zeros do fim: 3.400 ÷ 100 = 34.",
         "No método da chave, se uma ordem não dá para dividir, escreva <b>0</b> no quociente.",
         "O resto é sempre menor que o divisor. <b>Prova real</b>: quociente × divisor + resto = dividendo."],
        [("Calcule 824 ÷ 4.", ["8 ÷ 4 = 2", "2 ÷ 4 não dá: escreva 0", "24 ÷ 4 = 6"], "206"),
         ("130 alunos, ônibus de 40 lugares. Quantos ônibus?", ["130 ÷ 40 = 3 e resto 10", "os 10 também precisam ir"], "4 ônibus")],
        [["Esquecer o zero no quociente: 824 ÷ 4 = 26", "Quando a ordem não dá para dividir, escreva 0: 206."],
         ["Deixar um resto maior que o divisor", "Se sobra mais que o divisor, ainda cabe mais uma vez."],
         ["Ignorar o resto num problema", "Pense: o que sobra precisa de mais um ônibus?"]],
        chave(824, 4))
    faq = [("Até que divisor o 4º ano divide?", "A BNCC pede divisões cujo divisor tenha no máximo dois algarismos, com as ideias de repartição equitativa e de medida."),
           ("Como ensinar a ideia de medida?", "Pergunte «quantas vezes cabe?»: quantas caixas de 12 ovos dá para encher com 96 ovos? 96 ÷ 12 = 8 caixas.")]
    make_unit(R, "divisao", "N", ["EF04MA07"],
              "Resolver e elaborar problemas de divisão cujo divisor tenha no máximo dois algarismos, envolvendo os significados de repartição equitativa e de medida, utilizando estratégias diversas, como cálculo por estimativa, cálculo mental e algoritmos",
              "Divisão: repartir, medir e método da chave", "Divisão",
              "Atividades de matemática para o 4º ano sobre divisão: repartir e medir, dividir por 10 e 100, método da chave com divisor de 1 e 2 algarismos, resto, prova real e problemas. 100 exercícios com gabarito.",
              "Repartir: quanto para cada um. Medir: quantas vezes cabe.", "Quociente × divisor + resto = dividendo.",
              body, faq, sets, 6, grade="4-ano")


if __name__ == "__main__":
    main()
