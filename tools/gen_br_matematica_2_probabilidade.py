# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: Probabilidade: muito provável, pouco provável, impossível (Probabilidade e estatística, EF02MA21)
  python3 tools/gen_br_matematica_2_probabilidade.py
Classificar eventos do dia a dia como muito prováveis, pouco prováveis, improváveis ou impossíveis (e certos);
sacos de bolinhas e roletas: que cor é mais provável sair, qual é impossível; dados e moedas.
Usa geradores do 3º ano (probabilidade) com outro sorteio.
Erros: achar que o que é pouco provável nunca acontece, confundir impossível com pouco provável, ignorar a quantidade de bolinhas.
"""
import random
import gen_br_matematica_3_probabilidade as P3
from br_common import mcq, lesson, make_unit, mix, use, fig

R = random.Random(80220)
p_roleta, p_result = use("gen_br_matematica_3_probabilidade", 80913, "s3_roleta", "s2_resultados")
CL = ["muito provável", "pouco provável", "impossível", "certo"]

EVENTOS = [("Chover num dia de céu bem nublado e escuro", "muito provável"), ("Fazer frio em Manaus num dia de verão", "pouco provável"),
           ("Um cachorro falar como gente", "impossível"), ("Amanhã o sol nascer", "certo"), ("Ver um elefante andando na rua da escola", "pouco provável"),
           ("Uma criança do 2º ano ter 3 metros de altura", "impossível"), ("A professora entrar na sala hoje, num dia de aula", "muito provável"),
           ("Nevar em Salvador", "impossível"), ("Tirar um número maior que 1 num dado comum", "muito provável"), ("Tirar o número 6 num dado comum", "pouco provável"),
           ("Tirar o número 7 num dado comum", "impossível"), ("Depois da segunda-feira vir a terça-feira", "certo"), ("Um gato ter filhotes que são passarinhos", "impossível"),
           ("Ganhar sozinho uma rifa com 500 números comprando 1 número", "pouco provável"), ("Um ônibus da cidade passar no ponto hoje", "muito provável"),
           ("A água do mar ser salgada", "certo"), ("Encontrar um tesouro no quintal de casa", "pouco provável"), ("Um peixe viver fora da água por um ano", "impossível"),
           ("Comer arroz e feijão no almoço numa casa brasileira", "muito provável"), ("Um bebê nascer já sabendo ler", "impossível"),
           ("Fazer calor no Rio de Janeiro em janeiro", "muito provável"), ("Encontrar um dinossauro vivo no parque", "impossível"),
           ("Achar uma moeda na calçada a caminho da escola", "pouco provável"), ("A semana ter 8 dias", "impossível"),
           ("Um ano ter 12 meses", "certo"), ("Chover num dia de céu azul sem nenhuma nuvem", "pouco provável"),
           ("Uma criança do 2º ano ir à escola num dia de aula", "muito provável"), ("Tirar cara ou coroa ao jogar uma moeda", "certo"),
           ("Um passarinho pousar numa árvore da praça", "muito provável"), ("Ganhar um jogo de dados tirando o número 6 três vezes seguidas", "pouco provável"),
           ("Uma pedra flutuar no ar sozinha", "impossível"), ("Depois de dezembro vir janeiro", "certo")]


def s1_classificar():
    ev, ans = R.choice(EVENTOS)
    return mcq("Como você classifica este acontecimento? <b>%s</b>." % ev, ans, [x for x in CL if x != ans], "%s é <b>%s</b>." % (ev, ans))


def saco(cnt):
    return P3.saco(cnt)


def s2_saco():
    a, b = R.sample(sorted(P3.CORES), 2)
    x = R.randint(6, 10)
    y = R.randint(1, 2)
    pic = saco([(a, x), (b, y)])
    c = R.choice([x for x in sorted(P3.CORES) if x not in (a, b)])
    k = R.choice(["a", "b", "c"])
    if k == "a":
        ans, q = "muito provável", "tirar, sem olhar, uma bolinha %s" % a
        why = "há %s e só %s" % (P3.cor(a, x), P3.cor(b, y))
    elif k == "b":
        ans, q = "pouco provável", "tirar, sem olhar, uma bolinha %s" % b
        why = "há só %s e %s" % (P3.cor(b, y), P3.cor(a, x))
    else:
        ans, q = "impossível", "tirar uma bolinha %s" % c
        why = "não há nenhuma bolinha %s no saco" % c
    return mcq(pic + "No saco há %s e %s. Como é %s?" % (P3.cor(a, x), P3.cor(b, y), q), ans, [w for w in CL if w != ans], "%s: <b>%s</b>." % (why[0].upper() + why[1:], ans))


def s2_mais():
    cs = R.sample(sorted(P3.CORES), 3)
    ns = R.sample(range(1, 9), 3)
    pic = saco(list(zip(cs, ns)))
    big = R.random() < 0.6
    i = ns.index(max(ns) if big else min(ns))
    return mcq(pic + "No saco há %s, %s e %s. Tirando uma sem olhar, que cor é %s provável sair?" % (P3.cor(cs[0], ns[0]), P3.cor(cs[1], ns[1]), P3.cor(cs[2], ns[2]), "mais" if big else "menos"),
               cs[i], [c for c in cs if c != cs[i]] + ["todas têm a mesma chance"],
               "A cor com %s bolinhas tem %s chance: <b>%s</b>." % ("mais" if big else "menos", "mais" if big else "menos", cs[i]))


def s3_moeda_dado():
    q, a, w = R.choice([("Lançando uma moeda, sair cara é…", "possível, com a mesma chance de coroa", ["impossível", "certo", "muito mais provável que coroa"]),
                        ("Num dado comum, sair um número de 1 a 6 é…", "certo", ["impossível", "pouco provável", "muito provável, mas não certo"]),
                        ("Num dado comum, sair o número 0 é…", "impossível", ["pouco provável", "muito provável", "certo"]),
                        ("Num dado comum, sair o número 3 é…", "pouco provável", ["impossível", "certo", "muito provável"]),
                        ("Num dado comum, sair um número diferente de 2 é…", "muito provável", ["impossível", "pouco provável", "certo"]),
                        ("Lançando uma moeda, sair cara e coroa ao mesmo tempo é…", "impossível", ["muito provável", "pouco provável", "certo"]),
                        ("Uma moeda deu coroa 3 vezes seguidas. Na próxima, sair cara é…", "possível, com a mesma chance de coroa", ["impossível", "certo", "muito provável"]),
                        ("Lançando dois dados comuns, a soma ser 13 é…", "impossível", ["pouco provável", "muito provável", "certo"])])
    return mcq(q, a, w, "Pense em todos os resultados que podem sair. Resposta: <b>%s</b>." % a)


def s4_improvavel():
    q, a, w = R.choice([("Um acontecimento <b>improvável</b> é aquele que…", "pode acontecer, mas é muito difícil", ["nunca pode acontecer", "sempre acontece", "acontece quase sempre"]),
                        ("Um acontecimento <b>impossível</b> é aquele que…", "nunca pode acontecer", ["pode acontecer às vezes", "sempre acontece", "é muito provável"]),
                        ("Um acontecimento <b>muito provável</b> é aquele que…", "acontece quase sempre", ["nunca acontece", "acontece muito pouco", "é impossível"]),
                        ("Um acontecimento <b>certo</b> é aquele que…", "sempre vai acontecer", ["nunca acontece", "acontece às vezes", "é pouco provável"]),
                        ("Ganhar na loteria é um exemplo de acontecimento…", "improvável", ["impossível", "certo", "muito provável"]),
                        ("Um acontecimento pouco provável…", "pode acontecer, mas não é comum", ["nunca acontece", "sempre acontece", "acontece todo dia"])])
    return mcq(q, a, w, "Resposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Muito provável, pouco provável ou impossível?", mix(R, seen, [(s1_classificar, 16), (s4_improvavel, 4)])),
        ("Bolinhas no saco", mix(R, seen, [(s2_saco, 20)])),
        ("Que cor é mais provável?", mix(R, seen, [(s2_mais, 14), (p_roleta, 6)])),
        ("Dados e moedas", mix(R, seen, [(s3_moeda_dado, 8), (p_result, 6), (s4_improvavel, 2), (s1_classificar, 4)])),
        ("Classificar acontecimentos", mix(R, seen, [(s1_classificar, 6), (s2_saco, 8), (s2_mais, 6)])),
    ]
    body = lesson(
        ["Alguns acontecimentos são <b>certos</b>: o sol vai nascer amanhã.",
         "Outros são <b>impossíveis</b>: um cachorro falar como gente.",
         "<b>Muito provável</b> é o que quase sempre acontece. <b>Pouco provável</b> ou <b>improvável</b> pode acontecer, mas é difícil.",
         "Num saco com muitas bolinhas de uma cor, é muito provável tirar essa cor. Se não há uma cor no saco, tirar essa cor é impossível."],
        [("Saco com 9 azuis e 1 vermelha: tirar azul", ["há muitas azuis"], "muito provável"),
         ("Mesmo saco: tirar verde", ["não há verde"], "impossível")],
        [["Achar que pouco provável nunca acontece", "Pode acontecer, só é difícil."],
         ["Confundir impossível com pouco provável", "Impossível nunca acontece."],
         ["Ignorar quantas bolinhas há de cada cor", "Conte as bolinhas de cada cor."]],
        saco([("azul", 9), ("vermelha", 1)]))
    faq = [("O que o 2º ano aprende sobre probabilidade?", "A BNCC pede classificar resultados de eventos do dia a dia como pouco prováveis, muito prováveis, improváveis e impossíveis."),
           ("Como brincar de probabilidade em casa?", "Coloque tampinhas de cores diferentes num saco, em quantidades diferentes, e pergunte qual cor é mais provável sair antes de tirar uma sem olhar.")]
    make_unit(R, "probabilidade", "E", ["EF02MA21"],
              "Classificar resultados de eventos cotidianos aleatórios como «pouco prováveis», «muito prováveis», «improváveis» e «impossíveis»",
              "Probabilidade: muito provável, pouco provável e impossível", "Probabilidade",
              "Atividades de matemática para o 2º ano sobre probabilidade: classificar acontecimentos como muito prováveis, pouco prováveis, improváveis ou impossíveis, bolinhas no saco, dados e moedas. 100 exercícios com gabarito.",
              "Impossível nunca acontece; certo sempre acontece.", "Mais bolinhas de uma cor, mais chance.",
              body, faq, sets, 20, grade="2-ano")


if __name__ == "__main__":
    main()
