# -*- coding: utf-8 -*-
"""
Brasil Matemática 4º ano: Probabilidade: mais chance e menos chance (Probabilidade e estatística, EF04MA26)
  python3 tools/gen_br_matematica_4_probabilidade.py
Eventos certos, possíveis e impossíveis; resultados possíveis de um experimento; qual resultado tem mais chance (sacos de bolinhas,
roletas, dados, sorteios) sem usar frações; jogos justos e não justos; comparar a chance em dois sacos.
Usa geradores do 3º ano (probabilidade) e do 5º ano (sem frações) com outro sorteio.
Erros: achar que a cor com mais partes na roleta não importa, achar que um resultado «está devendo», confundir possível com certo.
"""
import random
from br_common import mcq, lesson, make_unit, mix, Kids, use
import gen_br_matematica_3_probabilidade as P3

R = random.Random(80421)
K = Kids(R)
M3 = "gen_br_matematica_3_probabilidade"
M5 = "gen_br_matematica_5_probabilidade"


def sem_fracao(it):
    t = it["q"] + it["e"] + "".join(it["c"])
    return "class='fr'" not in t and "ⁿ" not in t


p_evento, p_result, p_chance, p_roleta, p_justo = use(M3, 80966, "s1_evento", "s2_resultados", "s3_chance", "s3_roleta", "s4_justo")
q_espaco, q_justo, q_classif = use(M5, 80967, "s1_espaco", "s1_justo", "s4_classificar", preds=(sem_fracao,))


def s4_dois_sacos():
    a, b = R.sample(sorted(P3.CORES), 2)
    x1, y1 = R.randint(1, 8), R.randint(1, 8)
    x2, y2 = R.randint(1, 8), R.randint(1, 8)
    # comparação simples, sem frações: mesmo total ou mesma quantidade da outra cor
    if R.random() < 0.5:
        y2 = x1 + y1 - x2
        if y2 < 1:
            return None
    else:
        y2 = y1
    if x1 == x2:
        return None
    ans = "o saco 1" if x1 > x2 else "o saco 2"
    why = ("Os dois sacos têm %d bolinhas; o que tem mais bolinhas %s tem mais chance" % (x1 + y1, P3.PL[a])) if x1 + y1 == x2 + y2 else \
          ("Os dois sacos têm %d bolinhas %s; o que tem mais bolinhas %s tem mais chance" % (y1, P3.PL[b], P3.PL[a]))
    q = "Saco 1: %s e %s. Saco 2: %s e %s. Em qual saco é mais provável tirar uma bolinha %s?" % (P3.cor(a, x1), P3.cor(b, y1), P3.cor(a, x2), P3.cor(b, y2), a)
    return mcq(q, ans, [x for x in ["o saco 1", "o saco 2", "os dois dão a mesma chance", "não dá para saber"] if x != ans], "%s: <b>%s</b>." % (why, ans))


def s5_cotidiano():
    q, a, w = R.choice([("Em Manaus, em janeiro, é mais provável fazer…", "calor", ["neve", "temperatura abaixo de zero", "geada todos os dias"]),
                        ("Lançando um dado comum, o que é mais provável?", "sair um número menor que 6", ["sair o número 6", "sair o número 7", "sair o número 0"]),
                        ("Numa turma com 20 meninas e 5 meninos, sorteando um nome, é mais provável sair…", "uma menina", ["um menino", "um professor", "tanto faz"]),
                        ("Sorteando um dia do mês de abril, é mais provável sair…", "um dia que não é domingo", ["um domingo", "o dia 31", "o dia 40"]),
                        ("Lançando uma moeda, sair cara e sair coroa têm…", "a mesma chance", ["mais chance de cara", "mais chance de coroa", "nenhuma chance"]),
                        ("Uma moeda deu cara 4 vezes seguidas. Na próxima jogada…", "cara e coroa continuam com a mesma chance", ["vai sair coroa com certeza", "vai sair cara com certeza", "a moeda não cai"]),
                        ("Num saco só com bolinhas azuis, tirar uma bolinha azul é…", "certo", ["impossível", "pouco provável", "tão provável quanto vermelho"]),
                        ("Tirar uma bolinha verde de um saco só com bolinhas amarelas é…", "impossível", ["certo", "muito provável", "provável"]),
                        ("Numa rifa de 100 números, quem compra 10 números tem…", "mais chance que quem compra 1", ["menos chance que quem compra 1", "a mesma chance de quem compra 1", "certeza de ganhar"]),
                        ("O sol nascer amanhã é um evento…", "certo", ["impossível", "pouco provável", "que depende da sorte"])])
    return mcq(q, a, w, "Compare quantas vezes cada resultado pode acontecer. Resposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Certo, possível ou impossível", mix(R, seen, [(p_evento, 12), (q_classif, 4), (s5_cotidiano, 4)])),
        ("Resultados possíveis", mix(R, seen, [(p_result, 8), (q_espaco, 6), (p_roleta, 6)])),
        ("Mais chance, menos chance", mix(R, seen, [(p_chance, 14), (q_justo, 6)])),
        ("Comparar chances", mix(R, seen, [(s4_dois_sacos, 14), (p_justo, 6)])),
        ("Chances no dia a dia", mix(R, seen, [(s5_cotidiano, 6), (p_chance, 8), (q_justo, 6)])),
    ]
    body = lesson(
        ["Um evento pode ser <b>certo</b> (vai acontecer), <b>impossível</b> (não pode acontecer) ou <b>possível</b> (pode ou não acontecer).",
         "Num saco com 7 bolinhas azuis e 2 vermelhas, é <b>mais provável</b> tirar azul, porque há mais azuis.",
         "Numa roleta, a cor que ocupa mais partes tem mais chance de sair.",
         "Um jogo é <b>justo</b> quando todos os jogadores têm a mesma chance de ganhar."],
        [("Saco com 5 verdes e 3 amarelas. Que cor tem mais chance?", ["há mais verdes"], "verde"),
         ("Dado comum: sair 7 é…", ["o dado só vai até 6"], "impossível")],
        [["Achar que a cor com mais bolinhas não importa", "Quanto mais bolinhas de uma cor, mais chance ela tem."],
         ["Achar que um resultado «está devendo»", "A moeda não tem memória: cada jogada é uma nova chance."],
         ["Confundir possível com certo", "Certo é o que sempre acontece; possível pode não acontecer."]],
        P3.saco([("azul", 7), ("vermelha", 2)]))
    faq = [("O 4º ano usa frações em probabilidade?", "Não. A BNCC pede identificar os eventos com maior chance de acontecer, reconhecendo os resultados mais prováveis, sem usar frações. As frações entram no 5º ano."),
           ("Como trabalhar probabilidade em casa?", "Use um saco com tampinhas de cores diferentes: pergunte qual cor tem mais chance, faça várias retiradas e anote os resultados.")]
    make_unit(R, "probabilidade", "E", ["EF04MA26"],
              "Identificar, entre eventos aleatórios cotidianos, aqueles que têm maior chance de ocorrência, reconhecendo características de resultados mais prováveis, sem utilizar frações",
              "Probabilidade: mais chance e menos chance", "Probabilidade",
              "Atividades de matemática para o 4º ano sobre probabilidade: eventos certos, possíveis e impossíveis, resultados possíveis, mais chance e menos chance, jogos justos, sem frações. 100 exercícios com gabarito.",
              "Mais bolinhas de uma cor, mais chance de sair essa cor.", "Certo, possível ou impossível.",
              body, faq, sets, 21, grade="4-ano")


if __name__ == "__main__":
    main()
