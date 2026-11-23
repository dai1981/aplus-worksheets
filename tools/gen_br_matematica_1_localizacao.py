# -*- coding: utf-8 -*-
"""
Brasil Matemática 1º ano: Localização: em cima, embaixo, na frente, atrás (Geometria, EF01MA11, EF01MA12)
  python3 tools/gen_br_matematica_1_localizacao.py
Em cima, embaixo, ao lado, na frente, atrás, entre; à direita e à esquerda; posição numa fila e numa estante;
pontos de referência. Usa geradores do 2º e do 3º ano (localização) com outro sorteio.
Erros: trocar direita e esquerda, confundir na frente e atrás, esquecer o ponto de referência.
"""
import random
import k_pics
from br_common import mcq, lesson, make_unit, mix, use, KINDS
from br_1 import pic, art

R = random.Random(80111)
M2 = "gen_br_matematica_2_localizacao_e_trajetos"
l_fila, l_estante, l_pal = use(M2, 80977, "s1_fila", "s1_estante", "s2_palavras")
l_lado = use("gen_br_matematica_3_localizacao_e_trajetos", 80978, "s4_lado")
MESA = {"above": "em cima da mesa", "below": "embaixo da mesa", "beside": "ao lado da mesa"}
CAIXA = {"front": "na frente da caixa", "behind": "atrás da caixa", "beside": "ao lado da caixa", "above": "em cima da caixa"}


def s1_mesa():
    kind = R.choice(KINDS)
    rel = R.choice(sorted(MESA))
    p = pic(k_pics.table_scene_svg(kind, rel), "uma mesa e %s %s" % (art(kind), MESA[rel]))
    return mcq(p + "Onde está %s?" % art(kind), MESA[rel], [v for k, v in sorted(MESA.items()) if k != rel] + ["dentro da mesa"],
               "Olhe a mesa como referência: %s está <b>%s</b>." % (art(kind), MESA[rel]))


def s1_caixa():
    kind = R.choice(KINDS)
    rel = R.choice(sorted(CAIXA))
    p = pic(k_pics.box_scene_svg(kind, rel), "uma caixa e %s %s" % (art(kind), CAIXA[rel]))
    return mcq(p + "Onde está %s?" % art(kind), CAIXA[rel], [v for k, v in sorted(CAIXA.items()) if k != rel],
               "%s está <b>%s</b>%s." % (art(kind).capitalize(), CAIXA[rel], " (aparece só uma parte, porque a caixa tapa)" if rel == "behind" else ""))


PAL = [("Quando você está sentado na carteira, o tampo da mesa fica…", "em cima das suas pernas", ["embaixo dos seus pés", "atrás da sua cabeça", "dentro da mochila"]),
       ("Numa fila, quem está atrás de você fica…", "nas suas costas", ["na sua frente", "em cima de você", "embaixo de você"]),
       ("O sapato fica no pé e a meia fica…", "dentro do sapato", ["em cima do sapato", "atrás do sapato", "longe do sapato"]),
       ("No prédio, o 1º andar fica… do 2º andar", "embaixo", ["em cima", "ao lado", "atrás"]),
       ("O telhado da casa fica…", "em cima da casa", ["embaixo da casa", "dentro da casa", "atrás da casa"]),
       ("As raízes da árvore ficam…", "embaixo da terra", ["em cima da árvore", "na frente da árvore", "no céu"]),
       ("Para atravessar a rua com segurança, olhamos para a direita e para a…", "esquerda", ["frente só", "cima", "baixo"]),
       ("O motorista do ônibus fica… dos passageiros", "na frente", ["atrás", "embaixo", "em cima"])]


def s2_palavras():
    q, a, w = R.choice(PAL)
    return mcq(q, a, w, "Resposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Em cima, embaixo, ao lado", mix(R, seen, [(s1_mesa, 12), (s2_palavras, 8)])),
        ("Na frente, atrás, ao lado", mix(R, seen, [(s1_caixa, 20)])),
        ("Direita, esquerda e entre", mix(R, seen, [(l_fila, 20)])),
        ("Na estante", mix(R, seen, [(l_estante, 20)])),
        ("Pontos de referência", mix(R, seen, [(l_pal, 8), (l_lado, 8), (s1_mesa, 4)])),
    ]
    body = lesson(
        ["Para dizer onde algo está, escolha um <b>ponto de referência</b>: a mesa, a caixa, você mesmo.",
         "<b>Em cima</b> e <b>embaixo</b>: mais alto ou mais baixo que a referência.",
         "<b>Na frente</b> e <b>atrás</b>: perto do seu rosto ou das suas costas. Quem está atrás pode ficar escondido.",
         "<b>Direita</b> e <b>esquerda</b>: a maioria das pessoas escreve com a mão direita."],
        [("A bola está abaixo do tampo da mesa", ["referência: a mesa"], "embaixo da mesa"),
         ("Bola, caixa, flor (da esquerda para a direita)", ["o que está à direita da caixa?"], "a flor")],
        [["Trocar direita e esquerda", "Levante a mão com que você escreve e confira."],
         ["Confundir na frente e atrás", "Atrás é do lado das costas."],
         ["Esquecer o ponto de referência", "Diga sempre: em cima de quê? ao lado de quê?"]],
        pic(k_pics.table_scene_svg("ball", "below"), "uma bola embaixo da mesa"))
    faq = [("O que o 1º ano aprende sobre localização?", "A BNCC pede descrever a localização de pessoas e objetos usando termos como à direita, à esquerda, em frente, atrás, em cima e embaixo, e indicar pontos de referência."),
           ("Como praticar em casa?", "Brinque de esconder um objeto e dar pistas: «está embaixo da cadeira, ao lado da porta». Depois troquem de papel.")]
    make_unit(R, "localizacao", "G", ["EF01MA11", "EF01MA12"],
              "Descrever a localização de pessoas e de objetos no espaço em relação à sua própria posição, utilizando termos como à direita, à esquerda, em frente, atrás; descrever a localização de pessoas e de objetos no espaço segundo um dado ponto de referência, compreendendo que, para a utilização de termos que se referem à posição, como direita, esquerda, em cima, em baixo, é necessário explicitar-se o referencial",
              "Localização: em cima, embaixo, na frente, atrás", "Localização",
              "Atividades de matemática para o 1º ano sobre localização: em cima, embaixo, ao lado, na frente, atrás, entre, à direita e à esquerda. 100 exercícios com gabarito.",
              "Diga sempre o ponto de referência.", "Atrás é do lado das costas.",
              body, faq, sets, 11, grade="1-ano")


if __name__ == "__main__":
    main()
