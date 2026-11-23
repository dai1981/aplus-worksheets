# -*- coding: utf-8 -*-
"""
Brasil Matemática 1º ano: Dezenas e unidades: compor e decompor (Números, EF01MA07)
  python3 tools/gen_br_matematica_1_dezenas_e_unidades.py
Dezenas e unidades com material dourado e quadro de dez; decompor (47 = 40 + 7); diferentes adições para o mesmo número
(8 = 5 + 3 = 6 + 2); o todo e as partes; trocar 10 unidades por 1 dezena.
Erros: escrever 47 como 4 + 7, trocar dezenas e unidades (74), esquecer o zero (40 é 4 dezenas e 0 unidades).
"""
import random
from br_common import mcq, lesson, make_unit, mix, relabel, material_dourado, pl, fig
from br_1 import ligacao, quadro_dez

R = random.Random(80105)


def md(d, u):
    return relabel(material_dourado(0, 0, d, u), "material dourado: %s e %s" % (pl(d, "barra", "barras"), pl(u, "cubinho", "cubinhos")))


def du(d, u):
    return " e ".join(x for x in (pl(d, "dezena", "dezenas") if d else "", pl(u, "unidade", "unidades") if u else "") if x)


def wrong(n):
    d, u = divmod(n, 10)
    out = [10 * u + d if u and u != d else n + 10, d + u if d + u != n else n + 1, n + 10 if n < 90 else n - 10, n + 1]
    return [str(x) for x in out if 0 < x < 100 and x != n]


def s1_material():
    d, u = R.randint(1, 6), R.randint(0, 9)
    n = 10 * d + u
    return mcq(md(d, u) + "Que número o material dourado mostra?", str(n), wrong(n), "Barra = 10, cubinho = 1. %s: <b>%d</b>." % (du(d, u), n))


def s1_quantas():
    n = R.randint(11, 99)
    d, u = divmod(n, 10)
    if R.random() < 0.5:
        return mcq("Quantas dezenas tem o número %d?" % n, str(d), [str(u) if u != d else str(d + 1), str(n), str(d + 1) if u != d + 1 else str(d + 2)],
                   "%d = %s. Tem <b>%d dezena%s</b>." % (n, du(d, u), d, "s" if d > 1 else ""))
    return mcq("Quantas unidades soltas tem o número %d?" % n, str(u), [str(d) if d != u else str(u + 1), str(n), str(u + 10)],
               "%d = %s. Unidades: <b>%d</b>." % (n, du(d, u), u))


def s2_decompor():
    n = R.randint(11, 99)
    d, u = divmod(n, 10)
    if not u:
        return None
    ok = "%d + %d" % (10 * d, u)
    return mcq("Qual é a decomposição de %d?" % n, ok, ["%d + %d" % (d, u), "%d + %d" % (10 * u, d), "%d + %d" % (10 * d, u + 1) if u < 9 else "%d + %d" % (10 * d + 10, u)],
               "%d = %s = <b>%s</b>." % (n, du(d, u), ok))


def s2_compor():
    d, u = R.randint(1, 9), R.randint(1, 9)
    n = 10 * d + u
    if R.random() < 0.5:
        return mcq("Quanto é %d + %d?" % (10 * d, u), str(n), wrong(n), "%d dezenas e %d unidades: <b>%d</b>." % (d, u, n))
    return mcq("Que número tem %s?" % du(d, u), str(n), wrong(n), "<b>%d</b>." % n)


def s3_partes():
    t = R.randint(5, 10)
    a = R.randint(1, t - 1)
    k = R.choice(["parte", "todo", "jeitos"])
    if k == "parte":
        return mcq(ligacao(t, a, "?") + "O todo é %d e uma parte é %d. Qual é a outra parte?" % (t, a), str(t - a), [str(t), str(t - a + 1), str(t + a) if t + a <= 20 else str(t - a - 1)],
                   "%d + ___ = %d. A outra parte é <b>%d</b>." % (a, t, t - a))
    if k == "todo":
        b = R.randint(1, 9)
        return mcq(ligacao("?", a, b) + "As partes são %d e %d. Qual é o todo?" % (a, b), str(a + b), [str(a + b + 1), str(abs(a - b)) if a != b else str(a + b - 1), str(a * 10 + b)],
                   "%d + %d = <b>%d</b>." % (a, b, a + b))
    b = t - a
    c = R.randint(1, t - 1)
    if c in (a, b):
        return None
    ok = "%d + %d" % (c, t - c)
    return mcq("%d + %d = %d. Qual outra adição também dá %d?" % (a, b, t, t), ok, ["%d + %d" % (c, t - c + 1), "%d + %d" % (c, t - c - 1) if t - c > 1 else "%d + %d" % (c + 2, t - c), "%d + %d" % (t, c)],
               "%d + %d = %d também: <b>%s</b>." % (c, t - c, t, ok))


def s4_trocar():
    k = R.choice(["dez", "dez", "dezenas", "quadro"])
    if k == "dez":
        u = R.randint(11, 19)
        return mcq("Lia tem 1 dezena e %d unidades soltas. Trocando 10 unidades por 1 dezena, com o que ela fica?" % (u), "2 dezenas e %s" % pl(u - 10, "unidade", "unidades"),
                   ["1 dezena e %s" % pl(u - 10, "unidade", "unidades"), "%d dezenas" % (u - 10 + 1), "11 dezenas"], "10 unidades = 1 dezena. 1 + 1 = 2 dezenas e sobram %d: <b>%d</b> ao todo." % (u - 10, 10 + u))
    if k == "dezenas":
        d = R.randint(2, 9)
        return mcq("%d dezenas formam que número?" % d, str(10 * d), [str(d), str(d + 10), str(10 * d + 1)], "Cada dezena vale 10: <b>%d</b>." % (10 * d))
    n = R.randint(11, 19)
    return mcq(quadro_dez(n, 2) + "Quantas dezenas completas e quantas unidades há?", du(1, n - 10), [du(0, n), du(n - 10, 1), du(2, n - 10)],
               "Um quadro cheio = 1 dezena; o outro tem %d: <b>%s</b> (%d)." % (n - 10, du(1, n - 10), n))


def s5_problema():
    k = R.choice(["pacotes", "palitos", "caixas", "moedas"])
    d, u = R.randint(1, 8), R.randint(1, 9)
    n = 10 * d + u
    if k == "pacotes":
        return mcq("Um pacote tem 10 balas. Rui tem %d pacote%s e %d balas soltas. Quantas balas ele tem?" % (d, "s" if d > 1 else "", u), str(n), wrong(n), "%d + %d = <b>%d</b>." % (10 * d, u, n))
    if k == "palitos":
        return mcq("Ana tem %d palitos. Quantos montinhos de 10 ela consegue fazer?" % n, str(d), [str(u), str(n), str(d + 1)], "%d = %s: <b>%d montinhos</b> e sobram %d." % (n, du(d, u), d, u))
    if k == "caixas":
        return mcq("Há %d ovos. Cada caixa leva 10. Quantos ovos ficam fora das caixas cheias?" % n, str(u), [str(d), str(10 - u), str(n)], "%d = %d caixas cheias e <b>%d</b> ovos fora." % (n, d, u))
    return mcq("Téo tem %d moedas de 10 centavos. Quantos centavos ele tem?" % d, "%d centavos" % (10 * d), ["%d centavos" % d, "%d centavos" % (d + 10), "%d centavos" % (10 * d + 10)],
               "Conte de 10 em 10: <b>%d centavos</b>." % (10 * d))


def main():
    seen = set()
    sets = [
        ("Material dourado", mix(R, seen, [(s1_material, 12), (s1_quantas, 8)])),
        ("Decompor e compor", mix(R, seen, [(s2_decompor, 10), (s2_compor, 10)])),
        ("O todo e as partes", mix(R, seen, [(s3_partes, 20)])),
        ("Trocar 10 unidades por 1 dezena", mix(R, seen, [(s4_trocar, 12), (s1_quantas, 8)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["10 unidades formam 1 <b>dezena</b>. No material dourado, a barra vale 10 e o cubinho vale 1.",
         "No número 47, o 4 diz as dezenas (40) e o 7 diz as unidades (7): <b>47 = 40 + 7</b>.",
         "Um número pode ser formado de muitos jeitos: 8 = 5 + 3 = 6 + 2 = 7 + 1.",
         "Num número como 40, o 0 mostra que não há unidades soltas."],
        [("3 barras e 5 cubinhos", ["30 + 5"], "35"),
         ("Decompor 62", ["6 dezenas e 2 unidades"], "60 + 2")],
        [["Escrever 47 como 4 + 7", "O 4 vale 40: 47 = 40 + 7."],
         ["Trocar a ordem (74 em vez de 47)", "Dezenas primeiro, à esquerda."],
         ["Esquecer o zero", "4 dezenas e 0 unidades = 40."]],
        fig(md(3, 5)))
    faq = [("O que é decompor um número?", "É separar o número em partes, como 47 = 40 + 7. A BNCC pede que o 1º ano componha e decomponha números de até duas ordens com material manipulável."),
           ("Como ajudar em casa?", "Faça amarrados de 10 palitos com elástico. Monte números (3 amarrados e 5 soltos = 35) e peça para a criança dizer e escrever o número.")]
    make_unit(R, "dezenas-e-unidades", "N", ["EF01MA07"],
              "Compor e decompor número de até duas ordens, por meio de diferentes adições, com o suporte de material manipulável, contribuindo para a compreensão de características do sistema de numeração decimal e o desenvolvimento de estratégias de cálculo",
              "Dezenas e unidades: compor e decompor números", "Dezenas e unidades",
              "Atividades de matemática para o 1º ano sobre dezenas e unidades: material dourado, decompor (47 = 40 + 7), o todo e as partes, trocar 10 unidades por 1 dezena. 100 exercícios com gabarito.",
              "10 unidades = 1 dezena.", "47 = 40 + 7.",
              body, faq, sets, 5, grade="1-ano")


if __name__ == "__main__":
    main()
