# -*- coding: utf-8 -*-
"""
Brasil Matemática 1º ano: Números ordinais (Números, EF01MA01)
  python3 tools/gen_br_matematica_1_numeros_ordinais.py
Ordinais do 1º ao 10º: posição numa fila (contando da esquerda ou da direita), chegada de uma corrida, andares,
escrita por extenso (primeiro, segundo…), antes e depois na ordem.
Erros: contar a partir do lado errado, confundir «3º» (posição) com «3» (quantidade), pular uma posição.
"""
import random
import k_pics
from br_common import mcq, lesson, make_unit, mix, KINDS, COISAS, Kids
from br_1 import pic, art, ORD_M

R = random.Random(80102)
K = Kids(R)
O = ["", "1º", "2º", "3º", "4º", "5º", "6º", "7º", "8º", "9º", "10º"]


def fila_pic(ks):
    return pic(k_pics.kinds_row_svg(ks), "fila da esquerda para a direita: " + ", ".join(COISAS[k][0] for k in ks))


def s1_qual():
    ks = R.sample(KINDS, R.randint(5, 7))
    i = R.randrange(len(ks))
    return mcq(fila_pic(ks) + "Contando da esquerda, qual objeto está em %s lugar?" % O[i + 1], COISAS[ks[i]][0],
               [COISAS[x][0] for x in ks if x != ks[i]], "Conte da esquerda: 1º, 2º… O %s é <b>%s</b>." % (O[i + 1], art(ks[i])))


def s1_lugar():
    ks = R.sample(KINDS, R.randint(5, 7))
    i = R.randrange(len(ks))
    return mcq(fila_pic(ks) + "Contando da esquerda, em que lugar está %s?" % art(ks[i]), O[i + 1], [O[j] for j in range(1, len(ks) + 1) if j != i + 1],
               "%s está em <b>%s lugar</b>." % (art(ks[i]).capitalize(), O[i + 1]))


def s2_direita():
    ks = R.sample(KINDS, R.randint(5, 6))
    n = len(ks)
    i = R.randint(1, 3)
    obj = ks[n - i]
    return mcq(fila_pic(ks) + "Agora conte <b>da direita</b>. Qual objeto está em %s lugar?" % O[i], COISAS[obj][0],
               [COISAS[x][0] for x in ks if x != obj], "Da direita para a esquerda, o %s é <b>%s</b> (da esquerda seria %s)." % (O[i], art(obj), art(ks[i - 1])))


def s2_extenso():
    i = R.randint(1, 10)
    if R.random() < 0.5:
        return mcq("Como se escreve %s por extenso?" % O[i], ORD_M[i], [ORD_M[j] for j in (i - 1, i + 1, i + 2) if 1 <= j <= 10] + ["dez"],
                   "%s = <b>%s</b>." % (O[i], ORD_M[i]))
    return mcq("Como se escreve <b>%s</b> com número?" % ORD_M[i], O[i], [O[j] for j in (i - 1, i + 1, i + 2) if 1 <= j <= 10] + [str(i)],
               "%s = <b>%s</b>." % (ORD_M[i], O[i]))


def s3_corrida():
    n = R.randint(4, 6)
    ps = []
    while len(ps) < n:
        p, _ = K.next()
        if p not in ps:
            ps.append(p)
    i = R.randrange(n)
    txt = ", ".join(ps[:-1]) + " e " + ps[-1]
    if R.random() < 0.5:
        return mcq("Na corrida, chegaram nesta ordem: %s. Quem chegou em %s lugar?" % (txt, O[i + 1]), ps[i], [x for x in ps if x != ps[i]],
                   "Conte na ordem de chegada: o %s é <b>%s</b>." % (O[i + 1], ps[i]))
    return mcq("Na corrida, chegaram nesta ordem: %s. Em que lugar chegou %s?" % (txt, ps[i]), O[i + 1], [O[j] for j in range(1, n + 1) if j != i + 1],
               "%s chegou em <b>%s lugar</b>." % (ps[i], O[i + 1]))


def s4_ordem():
    i = R.randint(2, 9)
    k = R.choice(["depois", "antes", "andar"])
    if k == "depois":
        return mcq("Que posição vem logo depois do %s?" % O[i], O[i + 1], [O[i - 1], O[min(i + 2, 10)] if i + 2 <= 10 else "1º", str(i + 1)], "Depois do %s vem o <b>%s</b>." % (O[i], O[i + 1]))
    if k == "antes":
        return mcq("Que posição vem logo antes do %s?" % O[i], O[i - 1], [O[i + 1], O[i - 2] if i > 2 else O[i + 2], str(i - 1)], "Antes do %s vem o <b>%s</b>." % (O[i], O[i - 1]))
    a = R.randint(1, 6)
    b = R.randint(1, 3)
    return mcq("Lia mora no %s andar. A avó mora %d %s acima. Em que andar mora a avó?" % (O[a], b, "andar" if b == 1 else "andares"), O[a + b] + " andar",
               [O[a + b - 1] + " andar" if a + b - 1 != a else O[a + b + 1] + " andar", O[a + b + 1] + " andar", O[a] + " andar"], "%s + %d: <b>%s andar</b>." % (O[a], b, O[a + b]))


def s5_fila():
    n = R.randint(6, 10)
    p, g = K.next()
    k = R.choice(["frente", "atras", "total"])
    i = R.randint(2, n - 1)
    pos = ("a %dª" if g == "ela" else "o %dº") % i
    ele = "dela" if g == "ela" else "dele"
    if k == "frente":
        return mcq("Numa fila de %d crianças, %s é %s. Quantas crianças estão na frente %s?" % (n, p, pos, ele),
                   str(i - 1), [str(i), str(n - i), str(i + 1)], "Antes do %s há %d posições: <b>%d crianças</b>." % (O[i], i - 1, i - 1))
    if k == "atras":
        return mcq("Numa fila de %d crianças, %s é %s. Quantas crianças estão atrás %s?" % (n, p, pos, ele),
                   str(n - i), [str(i), str(n - i + 1), str(i - 1) if i - 1 != n - i else str(n)], "Depois do %s vêm as posições até o %s: <b>%d crianças</b>." % (O[i], O[n], n - i))
    return mcq("%s é %s da fila e também %s. Quantas crianças há na fila?" % (p, "a última" if g == "ela" else "o último", ("a %dª" if g == "ela" else "o %dº") % n), str(n),
               [str(n - 1), str(n + 1), str(n + 2)], "Se o último é o %s, há <b>%d crianças</b>." % (O[n], n))


def main():
    seen = set()
    sets = [
        ("Qual está em que lugar?", mix(R, seen, [(s1_qual, 10), (s1_lugar, 10)])),
        ("Contar da direita e escrever", mix(R, seen, [(s2_direita, 10), (s2_extenso, 10)])),
        ("Corridas", mix(R, seen, [(s3_corrida, 20)])),
        ("Antes e depois", mix(R, seen, [(s4_ordem, 14), (s2_extenso, 6)])),
        ("Problemas de fila", mix(R, seen, [(s5_fila, 14), (s3_corrida, 6)])),
    ]
    body = lesson(
        ["Os <b>números ordinais</b> dizem a posição: 1º (primeiro), 2º (segundo), 3º (terceiro)…",
         "Numa fila, combine de onde começar a contar: da esquerda, da direita ou da frente.",
         "Depois do 9º (nono) vem o 10º (décimo).",
         "«3 crianças» é uma quantidade; «3º lugar» é uma posição."],
        [("Corrida: Ana, Davi, Lia. Quem foi o 2º?", ["1º Ana", "2º Davi"], "Davi"),
         ("O 4º de uma fila: quantos estão na frente?", ["1º, 2º, 3º"], "3")],
        [["Contar do lado errado", "Veja se a pergunta diz «da esquerda» ou «da direita»."],
         ["Confundir 3º com 3", "3º é a terceira posição."],
         ["Pular uma posição", "Aponte cada um e fale: primeiro, segundo, terceiro…"]],
        fila_pic(["duck", "apple", "star", "ball", "fish"]))
    faq = [("Quais ordinais o 1º ano aprende?", "Do primeiro ao décimo, usados para dizer posições numa fila, numa corrida ou em andares. A BNCC pede usar números como indicador de quantidade ou de ordem."),
           ("Como praticar ordinais em casa?", "Faça filas de brinquedos e pergunte quem é o primeiro, o terceiro ou o último. Mude o lado de começar a contar.")]
    make_unit(R, "numeros-ordinais", "N", ["EF01MA01"],
              "Utilizar números naturais como indicador de quantidade ou de ordem em diferentes situações cotidianas e reconhecer situações em que os números não indicam contagem nem ordem, mas sim código de identificação",
              "Números ordinais: primeiro, segundo, terceiro", "Números ordinais",
              "Atividades de matemática para o 1º ano sobre números ordinais: posição numa fila, corridas, do 1º ao 10º, primeiro, segundo, terceiro. 100 exercícios com gabarito.",
              "Ordinal diz a posição: 1º, 2º, 3º.", "Combine de que lado começar a contar.",
              body, faq, sets, 2, grade="1-ano")


if __name__ == "__main__":
    main()
