# -*- coding: utf-8 -*-
"""
Brasil Matemática 1º ano: Números até 100 (Números, EF01MA01, EF01MA04)
  python3 tools/gen_br_matematica_1_numeros_ate_100.py
Contar objetos (até 20 com figuras e até 100 em grupos de 10); ler e escrever números até 100 com algarismos e por extenso;
número que vem antes e depois; números que faltam na contagem.
Erros: contar o mesmo objeto duas vezes, escrever 61 para dezesseis, esquecer um número ao contar.
"""
import random
from br_common import mcq, lesson, make_unit, mix, extenso, KINDS
from br_1 import fila, quadro_dez, espalhados, nome, quantos, pic
import k_pics

R = random.Random(80101)


def s1_contar():
    kind = R.choice(KINDS)
    n = R.randint(3, 16)
    p = espalhados(n, kind, R.randint(1, 9999)) if R.random() < 0.5 else fila(n, kind)
    return mcq(p + "%s %s há?" % (quantos(kind), nome(kind)), str(n), [str(n + 1), str(n - 1), str(n + 2)],
               "Conte um por um, sem pular nenhum: <b>%d</b>." % n)


def s1_quadro():
    n = R.randint(4, 20)
    return mcq(quadro_dez(n, 2 if n > 10 else 1) + "Quantas bolinhas há no quadro?", str(n), [str(n + 1), str(n - 1), str(n + 10) if n <= 10 else str(n - 10)],
               ("Um quadro cheio tem 10. 10 + %d = <b>%d</b>." % (n - 10, n)) if n > 10 else "Conte as bolinhas: <b>%d</b>." % n)


def s2_grupos():
    kind = R.choice(KINDS)
    d, u = R.randint(2, 5), R.randint(0, 9)
    n = 10 * d + u
    return mcq(fila(n, kind) + "Cada fileira cheia tem 10. %s %s há?" % (quantos(kind), nome(kind)), str(n), [str(n + 10), str(d + u), str(n - 1)],
               "%d fileiras de 10 e mais %d: %d + %d = <b>%d</b>." % (d, u, 10 * d, u, n))


def s3_extenso():
    n = R.randint(11, 99) if R.random() < 0.7 else R.randint(1, 10)
    if R.random() < 0.5:
        w = {int(str(n)[::-1]) if n > 10 and n % 10 else n + 10, n + 1, n - 1 if n > 1 else n + 2}
        return mcq("Escreva com algarismos: <b>%s</b>." % extenso(n), str(n), [str(x) for x in sorted(w) if x != n and x > 0],
                   "«%s» = <b>%d</b>." % (extenso(n), n))
    w = [n + 1, n - 1 if n > 1 else n + 2, int(str(n)[::-1]) if n > 10 and n % 10 and int(str(n)[::-1]) != n else n + 10]
    return mcq("Como se escreve %d por extenso?" % n, extenso(n), [extenso(x) for x in w if 0 < x <= 100], "%d se escreve <b>%s</b>." % (n, extenso(n)))


def s4_vizinhos():
    n = R.randint(2, 98)
    k = R.choice(["depois", "antes", "entre"])
    if k == "depois":
        return mcq("Que número vem logo depois de %d?" % n, str(n + 1), [str(n - 1), str(n + 10) if n < 90 else str(n + 2), str(n)], "Depois de %d vem <b>%d</b>." % (n, n + 1))
    if k == "antes":
        return mcq("Que número vem logo antes de %d?" % n, str(n - 1), [str(n + 1), str(n - 10) if n > 10 else str(n - 2) if n > 2 else str(n + 2), str(n)], "Antes de %d vem <b>%d</b>." % (n, n - 1))
    return mcq("Que número fica entre %d e %d?" % (n - 1, n + 1), str(n), [str(n + 2), str(n - 2) if n > 2 else str(n + 3), str(n + 10) if n < 90 else str(n - 10)], "%d, <b>%d</b>, %d." % (n - 1, n, n + 1))


def s4_falta():
    a = R.randint(1, 94)
    i = R.randint(1, 4)
    xs = list(range(a, a + 6))
    shown = ", ".join("___" if j == i else str(x) for j, x in enumerate(xs))
    return mcq("Que número falta na contagem? %s" % shown, str(xs[i]), [str(xs[i] + 1), str(xs[i] - 1), str(xs[i] + 10) if xs[i] < 90 else str(xs[i] - 10)],
               "Conte de 1 em 1: <b>%d</b>." % xs[i])


def s5_problema():
    k = R.choice(["ovos", "lapis", "figurinhas", "degraus", "palitos"])
    if k == "ovos":
        d = R.randint(2, 9)
        return mcq("Cada caixa tem 10 ovos. Quantos ovos há em %d caixas?" % d, str(10 * d), [str(d), str(10 * d + 1), str(d + 10)], "Conte de 10 em 10: <b>%d</b>." % (10 * d))
    if k == "lapis":
        d, u = R.randint(1, 6), R.randint(1, 9)
        return mcq("Lia tem %d caixa%s de 10 lápis e mais %d lápis soltos. Quantos lápis ela tem?" % (d, "s" if d > 1 else "", u), str(10 * d + u), [str(d + u), str(10 * u + d), str(10 * d + u + 1)],
                   "%d + %d = <b>%d</b>." % (10 * d, u, 10 * d + u))
    if k == "figurinhas":
        n = R.randint(20, 98)
        return mcq("Davi tem %d figurinhas. Ganhou mais 1. Com quantas ficou?" % n, str(n + 1), [str(n - 1), str(n + 10), str(n)], "Depois de %d vem <b>%d</b>." % (n, n + 1))
    if k == "degraus":
        n = R.randint(12, 40)
        return mcq("Rui subiu %d degraus. Desceu 1. Em que degrau ele está?" % n, str(n - 1), [str(n + 1), str(n - 10), str(n)], "Antes de %d vem <b>%d</b>." % (n, n - 1))
    d = R.randint(3, 9)
    return mcq("Ana fez %d montinhos de 10 palitos. Quantos palitos ela usou?" % d, str(10 * d), [str(d), str(d + 10), str(10 * d + 10)], "%d dezenas = <b>%d</b>." % (d, 10 * d))


def main():
    seen = set()
    sets = [
        ("Contar objetos", mix(R, seen, [(s1_contar, 12), (s1_quadro, 8)])),
        ("Contar de 10 em 10", mix(R, seen, [(s2_grupos, 14), (s1_quadro, 6)])),
        ("Ler e escrever números", mix(R, seen, [(s3_extenso, 20)])),
        ("Antes, depois e entre", mix(R, seen, [(s4_vizinhos, 12), (s4_falta, 8)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Para contar, aponte cada objeto <b>uma vez só</b>. O último número que você fala é o total.",
         "Quando há muitos objetos, faça grupos de <b>10</b>: 3 grupos de 10 e mais 4 = 34.",
         "Depois do 19 vem o 20; depois do 29 vem o 30; depois do 99 vem o 100.",
         "Cuidado com a escrita: <b>dezesseis</b> é 16, e não 61."],
        [("4 fileiras de 10 e mais 2", ["40 + 2"], "42"),
         ("Vinte e sete", ["2 dezenas e 7 unidades"], "27")],
        [["Contar o mesmo objeto duas vezes", "Risque ou toque em cada objeto ao contar."],
         ["Escrever 61 para dezesseis", "Dezesseis é dez e seis: 16."],
         ["Pular um número ao contar", "Fale os números em ordem, sem pressa."]],
        pic(k_pics.tenframe_svg(14, 2), "quadro de dez com 14 bolinhas"))
    faq = [("O que o 1º ano aprende sobre números?", "A BNCC pede contar coleções de até 100 objetos e registrar a quantidade, ler e escrever números e usar os números para indicar quantidade e ordem."),
           ("Como praticar contagem em casa?", "Conte objetos do dia a dia (tampinhas, brinquedos, degraus) e, quando forem muitos, faça montinhos de 10.")]
    make_unit(R, "numeros-ate-100", "N", ["EF01MA01", "EF01MA04"],
              "Utilizar números naturais como indicador de quantidade ou de ordem em diferentes situações cotidianas; contar a quantidade de objetos de coleções até 100 unidades e apresentar o resultado por registros verbais e simbólicos",
              "Números até 100: contar, ler e escrever", "Números até 100",
              "Atividades de matemática para o 1º ano sobre números até 100: contar objetos, contar de 10 em 10, ler e escrever números, antes e depois. 100 exercícios com gabarito.",
              "Conte cada objeto uma vez só.", "Muitos objetos? Faça grupos de 10.",
              body, faq, sets, 1, grade="1-ano")


if __name__ == "__main__":
    main()
