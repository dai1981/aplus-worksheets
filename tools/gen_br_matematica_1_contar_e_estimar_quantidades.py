# -*- coding: utf-8 -*-
"""
Brasil Matemática 1º ano: Contar e estimar quantidades (Números, EF01MA02, EF01MA03)
  python3 tools/gen_br_matematica_1_contar_e_estimar_quantidades.py
Contar de 1 em 1, de 2 em 2 e de 5 em 5; estimar sem contar (poucos ou muitos, cerca de 10, 20…);
comparar duas coleções por correspondência um a um (tem mais, tem menos, a mesma quantidade) e dizer quantos a mais.
Usa geradores do 2º ano (estimar e comparar) com outro sorteio.
Erros: achar que a fileira mais comprida tem mais, contar um objeto duas vezes, responder o total quando pedem quantos a mais.
"""
import random
import k_pics
from br_common import mcq, lesson, make_unit, mix, use, lim, KINDS
from br_1 import pic, dados, dois_grupos, nome, quantos, coisas

R = random.Random(80103)
M2 = "gen_br_matematica_2_estimar_e_comparar_quantidades"
e_grupos, e_comparar, e_mais, e_um, e_pares = use(M2, 80970, "s1_grupos", "s3_comparar", "s3_quantos_mais", "s4_um_a_um", "s4_pares", preds=(lim(30, 0),))
e_estimar = use(M2, 80970, "s2_estimar_figura", preds=(lim(999, 0),))


def s1_dados():
    a, b = R.sample(range(1, 7), 2)
    if R.random() < 0.5:
        return mcq(dados([a, b]) + "Quantos pontinhos há nos dois dados juntos?", str(a + b), [str(a + b + 1), str(abs(a - b)), str(a + b - 1)],
                   "%d + %d = <b>%d</b>." % (a, b, a + b))
    big = max(a, b)
    return mcq(dados([a, b]) + "Qual dado mostra mais pontinhos?", "o dado com %d" % big, ["o dado com %d" % min(a, b), "os dois mostram o mesmo", "não dá para saber"],
               "%d é mais que %d: <b>o dado com %d</b>." % (big, min(a, b), big))


def s1_dois():
    kind = R.choice(KINDS)
    k = R.choice([2, 5])
    g = R.randint(3, 6 if k == 5 else 9)
    p = pic(k_pics.groups_svg([(k, kind)] * g), "%d grupos com %s cada" % (g, coisas(kind, k)))
    return mcq(p + "Conte de %d em %d. %s %s há?" % (k, k, quantos(kind), nome(kind)), str(g * k), [str(g * k + k), str(g + k), str(g * k - 1)],
               "%s: <b>%d</b>." % (", ".join(str(k * i) for i in range(1, g + 1)), g * k))


POUCOS = [("Quantos dedos você tem nas duas mãos?", "10", ["2", "100", "5"]),
          ("Quantas rodas tem uma bicicleta?", "2", ["4", "10", "1"]),
          ("Quantas crianças cabem num banco de praça?", "cerca de 3", ["cerca de 30", "cerca de 100", "nenhuma"]),
          ("Quantos grãos de areia há numa praia?", "muitos, não dá para contar", ["cerca de 10", "cerca de 20", "5"]),
          ("Quantas folhas tem uma árvore grande?", "muitas, não dá para contar", ["cerca de 5", "cerca de 10", "2"]),
          ("Quantos ovos há numa caixa de uma dúzia?", "12", ["2", "20", "100"]),
          ("Quantas patas tem um cachorro?", "4", ["2", "6", "10"]),
          ("Quantos dias tem uma semana?", "7", ["5", "10", "30"]),
          ("Quantas estrelas há no céu numa noite sem nuvens?", "muitas, não dá para contar", ["cerca de 10", "cerca de 5", "1"]),
          ("Quantos alunos cabem numa sala de aula?", "cerca de 30", ["cerca de 3", "cerca de 300", "1"])]


def s2_quantos():
    q, a, w = R.choice(POUCOS)
    return mcq(q, a, w, "Pense no que você conhece. Resposta: <b>%s</b>." % a)


def s3_comparar_grupos():
    ka, kb = R.sample(KINDS, 2)
    a, b = R.randint(2, 9), R.randint(2, 9)
    if a == b:
        return None
    p = dois_grupos(a, ka, b, kb, "e")
    big = ka if a > b else kb
    return mcq(p + "Há mais %s ou mais %s?" % (nome(ka), nome(kb)), "mais %s" % nome(big), ["mais %s" % nome(kb if big == ka else ka), "a mesma quantidade", "não dá para saber"],
               "%s e %s: há <b>mais %s</b>." % (coisas(ka, a), coisas(kb, b), nome(big)))


def s5_problema():
    k = R.choice(["meninos", "pratos", "pirulitos", "bolas"])
    a, b = R.randint(3, 15), R.randint(3, 15)
    if a == b:
        return None
    if k == "meninos":
        return mcq("Na sala há %d meninas e %d meninos. Há mais meninas ou mais meninos?" % (a, b), "mais meninas" if a > b else "mais meninos",
                   ["mais meninos" if a > b else "mais meninas", "a mesma quantidade", "não dá para saber"], "%d %s %d: <b>%s</b>." % (a, "&gt;" if a > b else "&lt;", b, "mais meninas" if a > b else "mais meninos"))
    if k == "pratos":
        return mcq("Há %d pratos e %d colheres. Cada prato recebe uma colher. Sobra alguma coisa?" % (a, b),
                   ("sobram %d pratos sem colher" % (a - b)) if a > b else ("sobram %d colheres" % (b - a)),
                   [("sobram %d colheres" % (a - b)) if a > b else ("sobram %d pratos sem colher" % (b - a)), "não sobra nada", "sobram %d" % (a + b)],
                   "Ligue um a um: %d − %d = <b>%d</b>." % (max(a, b), min(a, b), abs(a - b)))
    if k == "pirulitos":
        return mcq("Lia tem %d pirulitos e Téo tem %d. Quantos pirulitos um tem a mais que o outro?" % (a, b), str(abs(a - b)), [str(a + b), str(max(a, b)), str(abs(a - b) + 1)],
                   "%d − %d = <b>%d</b>." % (max(a, b), min(a, b), abs(a - b)))
    return mcq("No cesto há %d bolas azuis e %d vermelhas. Quantas bolas há ao todo?" % (a, b), str(a + b), [str(abs(a - b)), str(a + b + 1), str(a + b - 1)], "%d + %d = <b>%d</b>." % (a, b, a + b))


def main():
    seen = set()
    sets = [
        ("Contar", mix(R, seen, [(s1_dados, 8), (s1_dois, 6), (e_grupos, 6)])),
        ("Estimar", mix(R, seen, [(e_estimar, 10), (s2_quantos, 10)])),
        ("Mais, menos ou igual", mix(R, seen, [(e_comparar, 10), (s3_comparar_grupos, 10)])),
        ("Quantos a mais?", mix(R, seen, [(e_mais, 10), (e_um, 6), (e_pares, 4)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Para contar mais rápido, conte de <b>2 em 2</b> ou de <b>5 em 5</b>.",
         "<b>Estimar</b> é dizer «cerca de quantos» sem contar um por um.",
         "Para comparar, ligue um objeto de um grupo com um do outro. O grupo que sobra tem mais.",
         "Uma fileira mais comprida <b>não</b> tem sempre mais objetos."],
        [("8 maçãs e 5 peras", ["ligue uma a uma", "sobram 3 maçãs"], "há 3 maçãs a mais"),
         ("5, 10, 15, 20", ["de 5 em 5"], "20 objetos")],
        [["Achar que a fileira mais comprida tem mais", "Ligue um a um ou conte."],
         ["Contar um objeto duas vezes", "Toque em cada um uma vez só."],
         ["Responder o total quando pedem quantos a mais", "Veja quantos sobram sem par."]],
        dois_grupos(8, "apple", 5, "star", "e"))
    faq = [("O que é comparar por correspondência?", "É ligar um objeto de um grupo com um objeto do outro, um a um. O grupo que fica com objetos sobrando tem mais. A BNCC pede isso no 1º ano."),
           ("Como treinar estimativa?", "Mostre um punhado de tampinhas e pergunte «cerca de quantas há?». Depois contem juntos para conferir.")]
    make_unit(R, "contar-e-estimar-quantidades", "N", ["EF01MA02", "EF01MA03"],
              "Contar de maneira exata ou aproximada, utilizando diferentes estratégias como o pareamento e outros agrupamentos; estimar e comparar quantidades de objetos de dois conjuntos (em torno de 20 elementos), por estimativa e/ou por correspondência (um a um, dois a dois) para indicar «tem mais», «tem menos» ou «tem a mesma quantidade»",
              "Contar e estimar quantidades", "Contar e estimar",
              "Atividades de matemática para o 1º ano sobre contar e estimar: contar de 2 em 2 e de 5 em 5, cerca de quantos, tem mais, tem menos, a mesma quantidade. 100 exercícios com gabarito.",
              "Ligue um a um para comparar.", "Estimar é dizer cerca de quantos.",
              body, faq, sets, 3, grade="1-ano")


if __name__ == "__main__":
    main()
