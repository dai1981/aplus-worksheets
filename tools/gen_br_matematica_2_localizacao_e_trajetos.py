# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: Localização e trajetos (Geometria, EF02MA12, EF02MA13)
  python3 tools/gen_br_matematica_2_localizacao_e_trajetos.py
Posição de objetos com mais de um ponto de referência (entre, à direita de, à esquerda de, em cima, embaixo);
malha quadriculada; deslocamentos com setas e códigos; virar à direita ou à esquerda; roteiros e plantas simples.
Usa geradores do 3º ano (localização) com outro sorteio.
Erros: trocar direita e esquerda, contar a casa de partida, esquecer o ponto de referência.
"""
import random
import k_pics
from br_common import mcq, lesson, make_unit, mix, use, relabel, fig, COISAS, KINDS

R = random.Random(80212)
M3 = "gen_br_matematica_3_localizacao_e_trajetos"
l_onde, l_oque, l_passos, l_codigo, l_escrever, l_virar, l_lado, l_croqui = use(M3, 80907, "s1_onde", "s1_oque", "s2_passos", "s3_codigo", "s3_escrever", "s4_virar", "s4_lado", "s5_croqui")


def art(kind):
    return ("a " if COISAS[kind][2] == "f" else "o ") + COISAS[kind][0]


def s1_fila():
    ks = R.sample(KINDS, 5)
    pic = fig(relabel(k_pics.kinds_row_svg(ks), "fila da esquerda para a direita: " + ", ".join(COISAS[k][0] for k in ks)))
    i = R.randint(1, 3)
    k = R.choice(["entre", "dir", "esq", "dir2"])
    if k == "entre":
        ans = COISAS[ks[i]][0]
        return mcq(pic + "Que objeto está entre %s e %s?" % (art(ks[i - 1]), art(ks[i + 1])), ans, [COISAS[x][0] for x in ks if x != ks[i]],
                   "Entre %s e %s está <b>%s</b>." % (art(ks[i - 1]), art(ks[i + 1]), art(ks[i])))
    if k == "dir":
        ans = COISAS[ks[i + 1]][0]
        return mcq(pic + "Que objeto está logo à direita d%s?" % art(ks[i]), ans, [COISAS[x][0] for x in ks if x != ks[i + 1]],
                   "Logo à direita d%s está <b>%s</b>." % (art(ks[i]), art(ks[i + 1])))
    if k == "esq":
        ans = COISAS[ks[i - 1]][0]
        return mcq(pic + "Que objeto está logo à esquerda d%s?" % art(ks[i]), ans, [COISAS[x][0] for x in ks if x != ks[i - 1]],
                   "Logo à esquerda d%s está <b>%s</b>." % (art(ks[i]), art(ks[i - 1])))
    j = R.choice([0, 4])
    pos = "1º" if j == 0 else "5º"
    ans = COISAS[ks[j]][0]
    return mcq(pic + "Contando da esquerda, qual objeto está em %s lugar?" % pos, ans, [COISAS[x][0] for x in ks if x != ks[j]],
               "Da esquerda para a direita, o %s é <b>%s</b>." % (pos, art(ks[j])))


def s1_estante():
    ks = R.sample(KINDS, 4)
    pic = fig(relabel(k_pics.shelf_svg(ks), "estante de cima para baixo: " + ", ".join(COISAS[k][0] for k in ks)))
    i = R.randint(1, 2)
    k = R.choice(["cima", "baixo", "entre", "topo"])
    if k == "cima":
        ans = COISAS[ks[i - 1]][0]
        return mcq(pic + "Que objeto está na prateleira logo acima d%s?" % art(ks[i]), ans, [COISAS[x][0] for x in ks if x != ks[i - 1]], "Logo acima d%s: <b>%s</b>." % (art(ks[i]), art(ks[i - 1])))
    if k == "baixo":
        ans = COISAS[ks[i + 1]][0]
        return mcq(pic + "Que objeto está na prateleira logo abaixo d%s?" % art(ks[i]), ans, [COISAS[x][0] for x in ks if x != ks[i + 1]], "Logo abaixo d%s: <b>%s</b>." % (art(ks[i]), art(ks[i + 1])))
    if k == "entre":
        return mcq(pic + "Que objeto está entre %s e %s?" % (art(ks[i - 1]), art(ks[i + 1])), COISAS[ks[i]][0], [COISAS[x][0] for x in ks if x != ks[i]],
                   "Entre as duas prateleiras está <b>%s</b>." % art(ks[i]))
    j = R.choice([0, 3])
    return mcq(pic + "Que objeto está na prateleira %s?" % ("mais alta" if j == 0 else "mais baixa"), COISAS[ks[j]][0], [COISAS[x][0] for x in ks if x != ks[j]],
               "Na prateleira %s está <b>%s</b>." % ("de cima" if j == 0 else "de baixo", art(ks[j])))


PALAVRAS = [("Na fila, Ana está na frente de Bia e atrás de Caio. Quem está no meio?", "Ana", ["Bia", "Caio", "ninguém"]),
            ("Caio está na frente de Ana, e Ana está na frente de Bia. Quem é o primeiro da fila?", "Caio", ["Ana", "Bia", "não dá para saber"]),
            ("O gato está embaixo da mesa e o vaso está em cima da mesa. O que está mais alto?", "o vaso", ["o gato", "a mesa", "os dois na mesma altura"]),
            ("Você está de frente para a lousa e vira para trás. Para onde você olha agora?", "para o fundo da sala", ["para a lousa", "para o teto", "para o chão"]),
            ("Se você levanta a mão direita e vira de costas, a mão continua sendo a…", "direita", ["esquerda", "de cima", "da frente"]),
            ("O livro está entre o caderno e o estojo. Quantos objetos há ao lado do livro?", "2", ["1", "3", "0"]),
            ("A padaria fica entre a farmácia e a escola. O que fica ao lado da padaria?", "a farmácia e a escola", ["só a escola", "só a farmácia", "nada"]),
            ("Lia está de frente para Téo. Lia levanta a mão direita. Para Téo, essa mão fica do lado…", "esquerdo dele", ["direito dele", "de cima", "de trás"])]


def s2_palavras():
    q, a, w = R.choice(PALAVRAS)
    return mcq(q, a, w, "Pense em cada ponto de referência. Resposta: <b>%s</b>." % a)


PLANTA = [("Numa planta da casa, a porta de entrada é marcada para mostrar…", "por onde se entra e sai", ["o lugar da cama", "a cor da parede", "o telhado"]),
          ("Uma planta mostra o ambiente visto…", "de cima", ["de lado", "de frente", "de baixo"]),
          ("Num roteiro da escola até a praça, o que ajuda a não se perder?", "pontos de referência, como a padaria e a igreja", ["a cor das nuvens", "o nome do cachorro", "a hora do lanche"]),
          ("No desenho da sala de aula visto de cima, a mesa da professora aparece como…", "um retângulo", ["um círculo pequeno", "uma linha", "um triângulo"]),
          ("Para ir do portão até a quadra, Rui anda 10 passos, vira à direita e anda 5 passos. Quantas vezes ele virou?", "1 vez", ["2 vezes", "nenhuma vez", "15 vezes"]),
          ("Numa planta, o símbolo de uma saída de emergência indica…", "por onde sair com segurança", ["onde fica o lanche", "onde guardar a mochila", "a sala do diretor"])]


def s5_planta():
    q, a, w = R.choice(PLANTA)
    return mcq(q, a, w, "Resposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Entre, à direita, à esquerda", mix(R, seen, [(s1_fila, 12), (s1_estante, 8)])),
        ("Pontos de referência", mix(R, seen, [(s2_palavras, 6), (s1_estante, 6), (l_lado, 8)])),
        ("Na malha quadriculada", mix(R, seen, [(l_onde, 10), (l_oque, 10)])),
        ("Deslocamentos e códigos", mix(R, seen, [(l_passos, 8), (l_codigo, 6), (l_virar, 6)])),
        ("Roteiros e plantas", mix(R, seen, [(l_croqui, 8), (l_escrever, 6), (s5_planta, 6)])),
    ]
    body = lesson(
        ["Para dizer onde algo está, use um <b>ponto de referência</b>: «a bola está à direita da caixa».",
         "Com dois pontos de referência fica mais fácil: «o livro está entre o caderno e o estojo».",
         "Na malha quadriculada, conte as casas a partir do lado de fora da casa de partida.",
         "Num <b>roteiro</b>, diga quantos passos andar e quando virar à direita ou à esquerda."],
        [("Bola, caixa, flor (da esquerda para a direita). O que está à direita da caixa?", ["olhe o lado direito da caixa"], "a flor"),
         ("Robô em A1 com o código → → ↑", ["→ → : C1", "↑ : C2"], "C2")],
        [["Trocar direita e esquerda", "Levante a mão com que você escreve e confira (a maioria escreve com a direita)."],
         ["Contar a casa de partida", "Comece a contar na casa seguinte."],
         ["Esquecer o ponto de referência", "Diga sempre: à direita de quê?"]],
        fig(relabel(k_pics.kinds_row_svg(["ball", "cup", "flower"]), "fila: bola, xícara, flor")))
    faq = [("O que o 2º ano aprende sobre localização?", "A BNCC pede identificar e registrar a localização e os deslocamentos de pessoas e objetos usando mais de um ponto de referência, e esboçar roteiros e plantas de ambientes conhecidos."),
           ("Como praticar em casa?", "Esconda um objeto e dê pistas: «está embaixo da mesa, à direita da cadeira». Depois peça para a criança desenhar o caminho do quarto até a cozinha.")]
    make_unit(R, "localizacao-e-trajetos", "G", ["EF02MA12", "EF02MA13"],
              "Identificar e registrar, em linguagem verbal ou não verbal, a localização e os deslocamentos de pessoas e de objetos no espaço, considerando mais de um ponto de referência, e indicar as mudanças de direção e de sentido; esboçar roteiros a ser seguidos ou plantas de ambientes familiares, assinalando entradas, saídas e alguns pontos de referência",
              "Localização e trajetos: direita, esquerda e malha", "Localização e trajetos",
              "Atividades de matemática para o 2º ano sobre localização e trajetos: entre, à direita, à esquerda, em cima, embaixo, malha quadriculada, deslocamentos com setas, roteiros e plantas. 100 exercícios com gabarito.",
              "Use um ponto de referência: à direita de quê?", "Na malha, não conte a casa de partida.",
              body, faq, sets, 12, grade="2-ano")


if __name__ == "__main__":
    main()
