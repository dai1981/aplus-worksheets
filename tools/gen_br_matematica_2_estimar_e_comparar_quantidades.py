# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: Estimar e comparar quantidades (Números, EF02MA02, EF02MA03)
  python3 tools/gen_br_matematica_2_estimar_e_comparar_quantidades.py
Contar coleções agrupando de 10 em 10; estimar «cerca de» quantos objetos; comparar duas coleções por correspondência
um a um (tem mais, tem menos, a mesma quantidade) e dizer quantos a mais ou a menos; estimativas no dia a dia.
Erros: contar o mesmo objeto duas vezes, achar que a fileira mais comprida tem mais, confundir «quantos a mais» com o total.
"""
import random
import k_pics
from br_common import mcq, num, lesson, make_unit, mix, coisas, COISAS, KINDS, relabel, fig, Kids

R = random.Random(80204)
K = Kids(R)


def nome(kind, n):
    return COISAS[kind][0] if n == 1 else COISAS[kind][1]


def quantas(kind):
    return "Quantas" if COISAS[kind][2] == "f" else "Quantos"


def fila(n, kind, per_row=10):
    return fig(relabel(k_pics.row_svg(n, kind, per_row), coisas(kind, n)))


def s1_contar():
    kind = R.choice(KINDS)
    n = R.randint(13, 48)
    return mcq(fila(n, kind) + "%s %s há? Conte de 10 em 10." % (quantas(kind), nome(kind, 2)), str(n), [str(n + 10), str(n - 1), str(n // 10 + n % 10)],
               "Há %d fileiras de 10 e mais %d: %d + %d = <b>%d</b>." % (n // 10, n % 10, n // 10 * 10, n % 10, n))


def s1_grupos():
    kind = R.choice(KINDS)
    k = R.choice([2, 5, 10])
    g = R.randint(3, 7 if k == 10 else 8)
    pic = fig(relabel(k_pics.groups_svg([(k, kind)] * g), "%d grupos com %s cada" % (g, coisas(kind, k))))
    n = g * k
    return mcq(pic + "Os grupos têm %d cada. %s %s há ao todo?" % (k, quantas(kind), nome(kind, 2)), str(n), [str(g + k), str(n + k), str(n - k)],
               "Conte de %d em %d: %s = <b>%d</b>." % (k, k, ", ".join(str(k * i) for i in range(1, g + 1)), n))


def s2_estimar_figura():
    kind = R.choice(KINDS)
    n = R.randint(18, 52)
    if n % 10 in (0, 4, 5, 6):
        return None
    ans = (n + 5) // 10 * 10
    pic = fig(relabel(k_pics.scatter_svg(n, kind, R.randint(1, 9999), cols=10, rows=6), "%s espalhadas" % nome(kind, 2) if COISAS[kind][2] == "f" else "%s espalhados" % nome(kind, 2)))
    return mcq(pic + "Sem contar um por um: há <b>cerca de</b> quantos objetos?", "cerca de %d" % ans,
               ["cerca de %d" % x for x in (ans + 20, ans - 20 if ans > 20 else ans + 40, ans * 10, 10 if ans != 10 else 5)],
               "Contando, há %d, que está perto de %d: <b>cerca de %d</b>." % (n, ans, ans))


ESTIM = [("Quantas crianças cabem numa sala de aula?", "cerca de 30", ["cerca de 3", "cerca de 300", "cerca de 1.000"]),
         ("Quantas páginas tem um livro de histórias infantil?", "cerca de 30", ["cerca de 3", "cerca de 3.000", "cerca de 900"]),
         ("Quantos grãos de arroz há num prato de arroz?", "muitos, mais de 500", ["cerca de 5", "cerca de 20", "cerca de 50"]),
         ("Quantos dedos têm 10 crianças juntas?", "100", ["10", "50", "1.000"]),
         ("Quantas pessoas cabem num ônibus da cidade?", "cerca de 60", ["cerca de 6", "cerca de 600", "cerca de 1.000"]),
         ("Quantas folhas tem um caderno escolar pequeno?", "cerca de 50", ["cerca de 5", "cerca de 500", "cerca de 1.000"]),
         ("Quantos alunos há numa escola com 10 turmas de 25 alunos?", "cerca de 250", ["cerca de 25", "cerca de 35", "cerca de 2.500"]),
         ("Quantos ovos cabem numa bandeja de padaria grande?", "30", ["3", "300", "3.000"]),
         ("Quantos passos você dá para atravessar a sala de aula?", "cerca de 15", ["cerca de 1", "cerca de 150", "cerca de 1.000"]),
         ("Quantos lápis cabem num estojo?", "cerca de 12", ["cerca de 1", "cerca de 120", "cerca de 1.000"]),
         ("Quantas pessoas cabem num estádio de futebol grande?", "muitas, mais de 1.000", ["cerca de 10", "cerca de 50", "cerca de 100"]),
         ("Quantas balas cabem num saquinho de festa?", "cerca de 10", ["cerca de 1", "cerca de 100", "cerca de 1.000"])]


def s2_estimar_dia():
    q, a, w = R.choice(ESTIM)
    return mcq(q, a, w, "Pense numa situação de verdade e compare com o que você conhece. A melhor estimativa é <b>%s</b>." % a)


def comparar_svg(a, ka, b, kb, spa=None, spb=None):
    svg = k_pics.match_svg([(a, ka, "A", spa), (b, kb, "B", spb)])
    return fig(relabel(svg, "fileira A: %s; fileira B: %s" % (coisas(ka, a), coisas(kb, b))))


def s3_comparar():
    ka, kb = R.sample(KINDS, 2)
    a, b = R.randint(4, 12), R.randint(4, 12)
    long_ = R.random() < 0.4
    spa = spb = None
    if long_ and a != b:
        # a fileira com menos objetos é a mais comprida
        if a < b:
            spa = 46
        else:
            spb = 46
    pic = comparar_svg(a, ka, b, kb, spa, spb)
    k = R.choice(["mais", "menos", "mais"])
    if a == b:
        ans = "as duas têm a mesma quantidade"
    elif k == "mais":
        ans = "a fileira A" if a > b else "a fileira B"
    else:
        ans = "a fileira A" if a < b else "a fileira B"
    opts = ["a fileira A", "a fileira B", "as duas têm a mesma quantidade", "a fileira mais comprida"]
    return mcq(pic + "Qual fileira tem %s objetos?" % k, ans, [x for x in opts if x != ans],
               "Ligue um a um: A tem %d e B tem %d. Resposta: <b>%s</b>." % (a, b, ans) + (" O comprimento da fileira não importa." if spa or spb else ""))


def s3_quantos_mais():
    ka, kb = R.sample(KINDS, 2)
    a, b = R.randint(3, 13), R.randint(3, 13)
    if a == b:
        return None
    pic = comparar_svg(a, ka, b, kb)
    big = "A" if a > b else "B"
    d = abs(a - b)
    if R.random() < 0.5:
        return mcq(pic + "Quantos objetos a fileira %s tem a mais?" % big, str(d), [str(a + b), str(max(a, b)), str(d + 1)],
                   "%d − %d = <b>%d</b> a mais." % (max(a, b), min(a, b), d))
    small = "B" if big == "A" else "A"
    return mcq(pic + "Quantos objetos a fileira %s tem a menos?" % small, str(d), [str(a + b), str(min(a, b)), str(d + 2)],
               "Os que sobram sem par na outra fileira: %d − %d = <b>%d</b>." % (max(a, b), min(a, b), d))


CENAS = [("Há {x} crianças e {y} cadeiras. Cada criança senta numa cadeira. Quantas crianças ficam sem cadeira?",
          "Há {x} crianças e {y} cadeiras. Cada criança senta numa cadeira. Quantas cadeiras ficam vazias?"),
         ("Há {x} pratos e {y} colheres. Cada prato recebe uma colher. Quantos pratos ficam sem colher?",
          "Há {x} pratos e {y} colheres. Cada prato recebe uma colher. Quantas colheres sobram?"),
         ("Há {x} cachorros e {y} ossos. Cada cachorro ganha um osso. Quantos cachorros ficam sem osso?",
          "Há {x} cachorros e {y} ossos. Cada cachorro ganha um osso. Quantos ossos sobram?"),
         ("Há {x} garrafas e {y} tampas. Cada garrafa recebe uma tampa. Quantas garrafas ficam sem tampa?",
          "Há {x} garrafas e {y} tampas. Cada garrafa recebe uma tampa. Quantas tampas sobram?"),
         ("Há {x} vasos e {y} flores. Cada vaso recebe uma flor. Quantos vasos ficam sem flor?",
          "Há {x} vasos e {y} flores. Cada vaso recebe uma flor. Quantas flores sobram?")]


def s4_um_a_um():
    t1, t2 = R.choice(CENAS)
    x, y = R.randint(5, 30), R.randint(5, 30)
    if x == y:
        return None
    q = (t1 if x > y else t2).format(x=x, y=y)
    d = abs(x - y)
    return mcq(q, str(d), [str(x + y), str(min(x, y)), str(d + 1)], "Ligue um a um: %d − %d = <b>%d</b>." % (max(x, y), min(x, y), d))


def s4_pares():
    n = R.randint(5, 18)
    k = R.choice(["meias", "sapatos", "luvas", "brincos"])
    return mcq("Há %d %s. Quantos pares (de 2 em 2) se formam?" % (2 * n, k), str(n), [str(2 * n), str(n + 2), str(4 * n) if 4 * n < 100 else str(n - 1)],
               "Cada par tem 2. Conte de 2 em 2 até %d: <b>%d pares</b>." % (2 * n, n))


def s5_problema():
    (p, g), (q2, g2) = K.two()
    k = R.choice(["figurinhas", "bolinhas", "pontos", "festa", "pipoca"])
    if k == "festa":
        n = R.randint(181, 419)
        if n % 100 < 10 or n % 100 > 90 or 40 < n % 100 < 60:
            return None
        c = (n + 50) // 100 * 100
        return mcq("Na festa da escola havia %s pessoas. Cerca de quantas pessoas foram à festa?" % num(n), "cerca de %s" % num(c),
                   ["cerca de %s" % num(x) for x in (c + 100, c - 100, c * 10 if c < 100 else 50)], "%s está mais perto de %s: <b>cerca de %s</b>." % (num(n), num(c), num(c)))
    x, y = R.randint(15, 95), R.randint(15, 95)
    if x == y:
        return None
    what = {"figurinhas": "figurinhas", "bolinhas": "bolinhas de gude", "pontos": "pontos", "pipoca": "pipocas no saquinho"}[k]
    if R.random() < 0.5:
        win = p if x > y else q2
        return mcq("%s tem %d %s e %s tem %d. Quem tem mais? Quantos a mais?" % (p, x, what, q2, y), "%s, %d a mais" % (win, abs(x - y)),
                   ["%s, %d a mais" % (q2 if win == p else p, abs(x - y)), "%s, %d a mais" % (win, x + y), "%s, %d a mais" % (win, abs(x - y) + 10)],
                   "%d − %d = %d. <b>%s, %d a mais</b>." % (max(x, y), min(x, y), abs(x - y), win, abs(x - y)))
    fem = what.split()[0] != "pontos"
    return mcq("%s tem %d %s. %s tem %d. %s %s faltam para %s ficar com o mesmo que %s?" % (p, max(x, y), what, q2, min(x, y), "Quantas" if fem else "Quantos", what.split()[0], q2, p),
               str(abs(x - y)), [str(x + y), str(min(x, y)), str(abs(x - y) + 1)], "%d − %d = <b>%d</b>." % (max(x, y), min(x, y), abs(x - y)))


def main():
    seen = set()
    sets = [
        ("Contar coleções", mix(R, seen, [(s1_contar, 12), (s1_grupos, 8)])),
        ("Estimar: cerca de quantos?", mix(R, seen, [(s2_estimar_figura, 10), (s2_estimar_dia, 10)])),
        ("Tem mais, tem menos, a mesma quantidade", mix(R, seen, [(s3_comparar, 12), (s3_quantos_mais, 8)])),
        ("Um a um e dois a dois", mix(R, seen, [(s4_um_a_um, 12), (s4_pares, 8)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Para contar muitos objetos, faça <b>grupos de 10</b>: 3 grupos de 10 e mais 4 = 34.",
         "<b>Estimar</b> é dizer «cerca de quantos» sem contar um por um. Depois, conte para conferir.",
         "Para comparar duas coleções, ligue <b>um a um</b>. A que fica com objetos sobrando tem mais.",
         "Uma fileira mais comprida <b>não</b> tem sempre mais objetos: conte ou ligue um a um."],
        [("12 crianças e 9 cadeiras", ["ligue uma criança a cada cadeira", "12 − 9"], "3 crianças sem cadeira"),
         ("38 balas", ["3 grupos de 10 e mais 8", "38 está perto de 40"], "cerca de 40")],
        [["Contar o mesmo objeto duas vezes", "Risque ou separe os que já contou."],
         ["Achar que a fileira mais comprida tem mais", "Ligue um a um para comparar."],
         ["Responder o total quando pedem «quantos a mais»", "Tire o menor do maior."]],
        comparar_svg(7, "star", 5, "heart", None, 46))
    faq = [("O que é estimar?", "É dar um valor aproximado sem contar um por um, por exemplo «cerca de 40 balas». A BNCC pede que o 2º ano estime quantidades de coleções até 1.000 e depois confira contando."),
           ("Como trabalhar a correspondência um a um?", "Ponha na mesa pratos e colheres e peça para a criança dar uma colher a cada prato. Quem fica sobrando mostra que há mais.")]
    make_unit(R, "estimar-e-comparar-quantidades", "N", ["EF02MA02", "EF02MA03"],
              "Fazer estimativas por meio de estratégias diversas a respeito da quantidade de objetos de coleções e registrar o resultado da contagem desses objetos (até 1000 unidades); comparar quantidades de objetos de dois conjuntos, por estimativa e/ou por correspondência (um a um, dois a dois, entre outros), para indicar «tem mais», «tem menos» ou «tem a mesma quantidade», indicando, quando for o caso, quantos a mais e quantos a menos",
              "Estimar e comparar quantidades", "Estimar e comparar",
              "Atividades de matemática para o 2º ano sobre estimar e comparar quantidades: contar em grupos de 10, cerca de quantos, tem mais, tem menos, a mesma quantidade, quantos a mais. 100 exercícios com gabarito.",
              "Ligue um a um para comparar.", "Estimar é dizer cerca de quantos.",
              body, faq, sets, 4, grade="2-ano")


if __name__ == "__main__":
    main()
