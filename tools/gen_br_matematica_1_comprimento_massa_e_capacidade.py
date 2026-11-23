# -*- coding: utf-8 -*-
"""
Brasil Matemática 1º ano: Comprimento, massa e capacidade (Grandezas e medidas, EF01MA15)
  python3 tools/gen_br_matematica_1_comprimento_massa_e_capacidade.py
Mais comprido e mais curto, mais alto e mais baixo; medir com cubinhos e clipes; mais pesado e mais leve na balança;
cabe mais e cabe menos; ordenar objetos do dia a dia. Usa geradores do 2º ano (massa e capacidade) com outro sorteio.
Erros: comparar sem alinhar as pontas, achar que o maior é sempre o mais pesado, olhar só a altura da água.
"""
import random
import k_pics
from br_common import mcq, lesson, make_unit, mix, use
from br_1 import pic, lapis, torres

R = random.Random(80114)
M2 = "gen_br_matematica_2_massa_e_capacidade"
m_bal, m_eq, m_rec, m_copos = use(M2, 80982, "s1_balanca", "s1_equilibrio", "s2_recipientes", "s2_copos")


def s1_lapis():
    ls = R.sample(range(2, 9), 3)
    big = R.random() < 0.5
    i = ls.index(max(ls) if big else min(ls))
    return mcq(lapis(ls) + "Qual lápis é o mais %s?" % ("comprido" if big else "curto"), "ABC"[i], [x for x in "ABC" if x != "ABC"[i]] + ["são todos iguais"],
               "Os lápis começam no mesmo lugar. O que termina mais %s é o <b>%s</b>." % ("longe" if big else "perto", "ABC"[i]))


def s1_medir():
    hs = R.sample(range(2, 9), 3)
    i = R.randrange(3)
    k = R.choice(["quantos", "dif"])
    if k == "quantos":
        return mcq(torres(hs) + "Quantos cubinhos de altura tem a torre %s?" % "ABC"[i], str(hs[i]), [str(hs[i] + 1), str(hs[i] - 1), str(sum(hs))],
                   "Conte os cubinhos da torre %s: <b>%d</b>." % ("ABC"[i], hs[i]))
    a, b = R.sample(range(3), 2)
    if hs[a] < hs[b]:
        a, b = b, a
    return mcq(torres(hs) + "Quantos cubinhos a torre %s tem a mais que a torre %s?" % ("ABC"[a], "ABC"[b]), str(hs[a] - hs[b]), [str(hs[a] + hs[b]), str(hs[a]), str(hs[a] - hs[b] + 1)],
               "%d − %d = <b>%d</b>." % (hs[a], hs[b], hs[a] - hs[b]))


PALAVRAS = [("O que é mais alto: uma girafa ou um cachorro?", "a girafa", ["o cachorro", "são iguais", "não dá para saber"]),
            ("O que é mais pesado: um elefante ou um gato?", "o elefante", ["o gato", "são iguais", "não dá para saber"]),
            ("O que é mais leve: uma pena ou um tijolo?", "a pena", ["o tijolo", "são iguais", "não dá para saber"]),
            ("Onde cabe mais água: num balde ou numa xícara?", "no balde", ["na xícara", "nos dois igual", "não dá para saber"]),
            ("O que é mais comprido: um ônibus ou um carro?", "o ônibus", ["o carro", "são iguais", "não dá para saber"]),
            ("O que é mais curto: um lápis novo ou um lápis usado até o fim?", "o lápis usado", ["o lápis novo", "são iguais", "não dá para saber"]),
            ("O que é mais grosso: o tronco de uma árvore ou um galho fino?", "o tronco", ["o galho", "são iguais", "não dá para saber"]),
            ("O que é mais largo: uma porta ou uma janela pequena?", "a porta", ["a janela pequena", "são iguais", "não dá para saber"]),
            ("Onde cabe menos suco: numa garrafa ou num copinho?", "no copinho", ["na garrafa", "nos dois igual", "não dá para saber"]),
            ("O que é mais baixo: um prédio ou uma casinha de cachorro?", "a casinha de cachorro", ["o prédio", "são iguais", "não dá para saber"]),
            ("O que é mais fino: um fio de cabelo ou uma corda?", "o fio de cabelo", ["a corda", "são iguais", "não dá para saber"]),
            ("O que pesa mais: uma melancia ou um morango?", "a melancia", ["o morango", "pesam o mesmo", "não dá para saber"])]


def s2_palavras():
    q, a, w = R.choice(PALAVRAS)
    return mcq(q, a, w, "Pense nos objetos de verdade. Resposta: <b>%s</b>." % a)


ORDEM = [(["formiga", "gato", "cavalo"], "do mais leve para o mais pesado"), (["xícara", "garrafa", "balde"], "do que cabe menos para o que cabe mais"),
         (["borracha", "lápis", "régua"], "do mais curto para o mais comprido"), (["criança", "adulto", "prédio"], "do mais baixo para o mais alto"),
         (["botão", "prato", "mesa"], "do menor para o maior"), (["uva", "laranja", "melancia"], "da mais leve para a mais pesada")]


def s3_ordem():
    xs, como = R.choice(ORDEM)
    ok = ", ".join(xs)
    sh = xs[:]
    while sh == xs:
        R.shuffle(sh)
    return mcq("Coloque em ordem, %s: %s." % (como, ", ".join(sh)), ok, [", ".join(xs[::-1]), ", ".join([xs[1], xs[0], xs[2]]), ", ".join([xs[0], xs[2], xs[1]])],
               "Ordem %s: <b>%s</b>." % (como, ok))


def main():
    seen = set()
    sets = [
        ("Mais comprido, mais curto", mix(R, seen, [(s1_lapis, 12), (s2_palavras, 8)])),
        ("Medir com cubinhos", mix(R, seen, [(s1_medir, 20)])),
        ("Mais pesado, mais leve", mix(R, seen, [(m_bal, 14), (m_eq, 6)])),
        ("Cabe mais, cabe menos", mix(R, seen, [(m_rec, 12), (m_copos, 8)])),
        ("Comparar e ordenar", mix(R, seen, [(s3_ordem, 6), (s2_palavras, 4), (s1_lapis, 4), (m_copos, 6)])),
    ]
    body = lesson(
        ["Para comparar comprimentos, coloque os objetos <b>lado a lado</b>, começando no mesmo lugar.",
         "Podemos medir com cubinhos, clipes ou palmos: quem precisa de mais cubinhos é mais comprido.",
         "Na balança, o lado mais <b>pesado</b> desce e o mais <b>leve</b> sobe.",
         "Para saber onde <b>cabe mais</b>, encha um com água e despeje no outro, ou conte quantos copos cabem."],
        [("Lápis A termina mais longe que o lápis B", ["começam no mesmo lugar"], "A é mais comprido"),
         ("Balança: o lado da melancia desce", ["o lado que desce é o mais pesado"], "a melancia é mais pesada")],
        [["Comparar sem alinhar as pontas", "Comece os dois no mesmo lugar."],
         ["Achar que o maior é sempre o mais pesado", "Use a balança: uma bola grande de isopor é leve."],
         ["Olhar só a altura da água", "Veja também se o pote é largo ou fino."]],
        lapis([6, 4, 7]))
    faq = [("O que o 1º ano aprende sobre medidas?", "A BNCC pede comparar comprimentos, capacidades e massas usando termos como mais alto, mais baixo, mais comprido, mais curto, mais pesado, mais leve, cabe mais e cabe menos, para ordenar objetos do dia a dia."),
           ("Como praticar em casa?", "Compare quem é mais alto na família, qual sapato é mais comprido e qual garrafa enche mais copos. Use uma balança de cozinha para ver o que pesa mais.")]
    make_unit(R, "comprimento-massa-e-capacidade", "M", ["EF01MA15"],
              "Comparar comprimentos, capacidades ou massas, utilizando termos como mais alto, mais baixo, mais comprido, mais curto, mais grosso, mais fino, mais largo, mais pesado, mais leve, cabe mais, cabe menos, entre outros, para ordenar objetos de uso cotidiano",
              "Comprimento, massa e capacidade: comparar e ordenar", "Comprimento, massa e capacidade",
              "Atividades de matemática para o 1º ano sobre medidas: mais comprido e mais curto, mais alto e mais baixo, mais pesado e mais leve, cabe mais e cabe menos. 100 exercícios com gabarito.",
              "Compare começando no mesmo lugar.", "O lado mais pesado da balança desce.",
              body, faq, sets, 14, grade="1-ano")


if __name__ == "__main__":
    main()
