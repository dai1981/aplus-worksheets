# -*- coding: utf-8 -*-
"""
Brasil Matemática 1º ano: Pesquisa e organização de dados (Probabilidade e estatística, EF01MA22)
  python3 tools/gen_br_matematica_1_pesquisa.py
Fazer uma pesquisa com a turma (até 30 pessoas); anotar com tracinhos; contar as respostas de uma lista; total de votos;
escolher a pergunta da pesquisa. Usa geradores do 2º ano (pesquisa) com outro sorteio.
Erros: contar uma pessoa duas vezes, esquecer que o grupo cortado vale 5, achar que o total passa do número de pessoas.
"""
import random
import gen_br_matematica_2_pesquisa_e_organizacao_de_dados as P2
from br_common import mcq, lesson, make_unit, mix, use, lim

R = random.Random(80120)
M2 = "gen_br_matematica_2_pesquisa_e_organizacao_de_dados"
q_tr, q_reg, q_lista, q_total, q_perg, q_graf = use(M2, 80988, "s1_tracinhos", "s1_registrar", "s2_lista", "s2_total", "s4_pergunta", "s3_grafico", preds=(lim(30, 0),))
TEMA = [("Para saber o brinquedo preferido da turma, a melhor pergunta é…", "«Qual é o seu brinquedo preferido?»", ["«Quantos anos você tem?»", "«Você tem irmão?»", "«Qual é o seu nome?»"]),
        ("Para saber como os alunos vêm para a escola, a melhor pergunta é…", "«Como você vem para a escola?»", ["«Você gosta da escola?»", "«Que horas você acorda?»", "«Qual é a sua cor preferida?»"]),
        ("Para saber a fruta preferida da turma, a melhor pergunta é…", "«Qual é a sua fruta preferida?»", ["«Você comeu fruta hoje?»", "«Quantas frutas existem?»", "«Onde fica a feira?»"]),
        ("Para saber o animal preferido da turma, a melhor pergunta é…", "«Qual é o seu animal preferido?»", ["«Você tem cachorro?»", "«Quantas patas tem o gato?»", "«O leão é bravo?»"]),
        ("Antes de perguntar à turma, é bom decidir…", "a pergunta e as respostas possíveis", ["a cor do lápis", "o tamanho do papel", "quem vai ganhar"]),
        ("Numa pesquisa com 20 crianças, cada uma vota…", "uma vez", ["duas vezes", "quantas quiser", "nenhuma vez"])]


def s4_tema():
    q, a, w = R.choice(TEMA)
    return mcq(q, a, w, "Resposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Contar tracinhos", mix(R, seen, [(q_tr, 14), (q_reg, 6)])),
        ("Contar respostas da lista", mix(R, seen, [(q_lista, 20)])),
        ("Total de votos", mix(R, seen, [(q_total, 20)])),
        ("Da tabela para o gráfico", mix(R, seen, [(q_graf, 20)])),
        ("Planejar a pesquisa", mix(R, seen, [(s4_tema, 6), (q_perg, 6), (q_lista, 8)])),
    ]
    body = lesson(
        ["Numa <b>pesquisa</b>, fazemos uma pergunta a várias pessoas e anotamos as respostas.",
         "Para anotar rápido, use <b>tracinhos</b>: a cada 5, risque os 4 com o 5º.",
         "Depois conte os tracinhos de cada resposta e escreva numa tabela.",
         "Se cada criança vota uma vez, o total de votos é o número de crianças."],
        [("2 grupos de 5 e 3 tracinhos", ["5 + 5 + 3"], "13 votos"),
         ("Gato 6, cachorro 9", ["6 + 9"], "15 crianças")],
        [["Contar uma pessoa duas vezes", "Risque o nome de quem já respondeu."],
         ["Esquecer que o grupo cortado vale 5", "Conte de 5 em 5 e depois os soltos."],
         ["Achar que o total passa do número de pessoas", "Cada pessoa vota uma vez."]],
        P2.tally(13))
    faq = [("Como fazer uma pesquisa no 1º ano?", "Escolha uma pergunta com poucas respostas (fruta, cor, animal), pergunte a cada colega, anote com tracinhos ou desenhos e conte. A BNCC pede pesquisas com até 30 pessoas."),
           ("Como praticar em casa?", "Pergunte aos familiares qual é a comida preferida, anote com tracinhos e veja qual ganhou.")]
    make_unit(R, "pesquisa", "E", ["EF01MA22"],
              "Realizar pesquisa, envolvendo até duas variáveis categóricas de seu interesse e universo de até 30 elementos, e organizar dados por meio de representações pessoais",
              "Pesquisa: tracinhos, listas e tabelas", "Pesquisa",
              "Atividades de matemática para o 1º ano sobre pesquisa: anotar com tracinhos, contar respostas de uma lista, total de votos e tabelas. 100 exercícios com gabarito.",
              "Cada pessoa vota uma vez.", "Tracinhos em grupos de 5.",
              body, faq, sets, 20, grade="1-ano")


if __name__ == "__main__":
    main()
