# -*- coding: utf-8 -*-
"""
Brasil Matemática 1º ano: Probabilidade: certo, talvez ou impossível (Probabilidade e estatística, EF01MA20)
  python3 tools/gen_br_matematica_1_probabilidade.py
Classificar acontecimentos do dia a dia como «vai acontecer com certeza», «talvez aconteça» e «é impossível acontecer»;
sacos de bolinhas e dados: o que é certo, o que pode sair e o que nunca sai.
Erros: achar que «talvez» é o mesmo que «com certeza», chamar de impossível o que só é difícil, não olhar o que há no saco.
"""
import random
import gen_br_matematica_3_probabilidade as P3
from br_common import mcq, lesson, make_unit, mix, swap

R = random.Random(80118)
swap(P3, 80985)
CERTO = ["o sol nascer amanhã", "depois da segunda-feira vir a terça-feira", "um dado comum mostrar um número de 1 a 6", "a água do mar ser salgada",
         "depois de dezembro vir janeiro", "uma semana ter 7 dias", "a moeda cair mostrando cara ou coroa", "o gelo derreter fora da geladeira num dia quente", "um ano ter 12 meses", "a noite chegar depois do dia", "uma pedra solta cair no chão", "o domingo vir depois do sábado", "todo bebê crescer com o tempo", "o número 5 vir depois do 4"]
TALVEZ = ["chover amanhã", "ganhar um jogo de dados", "tirar o número 6 num dado", "ver um arco-íris hoje", "ganhar um presente amanhã",
          "sair cara ao jogar uma moeda", "a professora contar uma história hoje", "encontrar um amigo no parque", "comer macarrão no jantar", "ver um passarinho na janela", "o ônibus chegar atrasado", "fazer sol no fim de semana", "achar uma moeda na rua", "um colega faltar à aula"]
IMPOSS = ["um cachorro voar sozinho", "um gato falar português", "tirar o número 7 num dado comum", "uma semana ter 10 dias",
          "um peixe subir numa árvore e cantar", "o sol nascer à meia-noite no Brasil", "uma criança de 6 anos ter 3 metros de altura", "nevar dentro da sala de aula", "um carro andar sem rodas no chão", "uma galinha botar um ovo de ouro", "um mês ter 40 dias", "a lua cair no quintal", "um elefante caber numa caixa de sapatos", "uma pedra virar sorvete"]
CL = {"certo": "vai acontecer com certeza", "talvez": "talvez aconteça", "impossivel": "é impossível acontecer"}
LISTAS = {"certo": CERTO, "talvez": TALVEZ, "impossivel": IMPOSS}


def s1_classificar():
    k = R.choice(sorted(LISTAS))
    ev = R.choice(LISTAS[k])
    return mcq("Como é este acontecimento: <b>%s</b>?" % ev, CL[k], [v for kk, v in sorted(CL.items()) if kk != k] + ["acontece só no domingo"],
               "%s: <b>%s</b>." % (ev[0].upper() + ev[1:], CL[k]))


def s2_qual():
    k = R.choice(sorted(LISTAS))
    ok = R.choice(LISTAS[k])
    outros = [R.choice(LISTAS[x]) for x in sorted(LISTAS) if x != k] + [R.choice(LISTAS[[x for x in sorted(LISTAS) if x != k][R.randrange(2)]])]
    if len(set(outros)) < 3:
        return None
    perg = {"certo": "vai acontecer com certeza", "talvez": "talvez aconteça (pode ou não acontecer)", "impossivel": "é impossível acontecer"}[k]
    return mcq("Qual destes acontecimentos %s?" % perg, ok, outros, "<b>%s</b> %s." % (ok[0].upper() + ok[1:], CL[k]))


def s3_saco():
    cores = sorted(P3.CORES)
    k = R.choice(["uma", "duas"])
    if k == "uma":
        c = R.choice(cores)
        n = R.randint(4, 9)
        outra = R.choice([x for x in cores if x != c])
        pic = P3.saco([(c, n)])
        ok = "é certo que sai uma bolinha %s" % c
        w = ["é impossível sair uma bolinha %s" % c, "talvez saia uma bolinha %s" % outra, "é certo que sai uma bolinha %s" % outra]
        why = "Só há bolinhas %s: com certeza sai %s, e nunca sai outra cor" % (P3.PL[c], c)
    else:
        a, b = R.sample(cores, 2)
        c = R.choice([x for x in cores if x not in (a, b)])
        pic = P3.saco([(a, R.randint(2, 6)), (b, R.randint(2, 6))])
        q = R.choice(["talvez", "impossivel"])
        if q == "talvez":
            x = R.choice([a, b])
            ok = "talvez saia uma bolinha %s" % x
            w = ["é certo que sai uma bolinha %s" % x, "é impossível sair uma bolinha %s" % x, "talvez saia uma bolinha %s" % c]
            why = "Há bolinhas %s e %s: pode sair %s ou não" % (P3.PL[a], P3.PL[b], x)
        else:
            ok = "é impossível sair uma bolinha %s" % c
            w = ["talvez saia uma bolinha %s" % c, "é certo que sai uma bolinha %s" % a, "é impossível sair uma bolinha %s" % a]
            why = "Não há nenhuma bolinha %s no saco" % c
    return mcq(pic + "Tirando uma bolinha sem olhar, qual frase está certa?", ok, w, "%s: <b>%s</b>." % (why, ok))


def s4_dado():
    k = R.choice(["certo", "talvez", "impossivel"])
    if k == "certo":
        ev = R.choice(["sair um número menor que 7", "sair um número de 1 a 6", "sair um número maior que 0"])
    elif k == "talvez":
        ev = "sair o número %d" % R.randint(1, 6) if R.random() < 0.6 else R.choice(["sair um número par", "sair um número maior que 3", "sair um número menor que 3"])
    else:
        ev = R.choice(["sair o número %d" % R.choice([0, 7, 8, 9, 10]), "sair um número maior que 6", "sair dois números ao mesmo tempo"])
    return mcq("Jogando um dado comum (números de 1 a 6): <b>%s</b>. Isso…" % ev, CL[k], [v for kk, v in sorted(CL.items()) if kk != k] + ["só acontece se jogar com força"],
               "O dado tem 1, 2, 3, 4, 5 e 6. %s: <b>%s</b>." % (ev[0].upper() + ev[1:], CL[k]))


def main():
    seen = set()
    sets = [
        ("Certo, talvez ou impossível?", mix(R, seen, [(s1_classificar, 20)])),
        ("Acontecimentos e dados", mix(R, seen, [(s2_qual, 3), (s1_classificar, 9), (s4_dado, 8)])),
        ("Bolinhas no saco", mix(R, seen, [(s3_saco, 20)])),
        ("Dados e bolinhas", mix(R, seen, [(s4_dado, 6), (s3_saco, 14)])),
        ("Revisão", mix(R, seen, [(s1_classificar, 4), (s3_saco, 16)])),
    ]
    body = lesson(
        ["Alguns acontecimentos <b>vão acontecer com certeza</b>: o sol vai nascer amanhã.",
         "Outros <b>talvez aconteçam</b>: pode chover ou não.",
         "E alguns são <b>impossíveis</b>: um cachorro não voa sozinho.",
         "Num saco só com bolinhas azuis, é certo sair azul e impossível sair vermelha."],
        [("Tirar o número 7 num dado", ["o dado vai de 1 a 6"], "é impossível"),
         ("Chover amanhã", ["pode ou não acontecer"], "talvez aconteça")],
        [["Achar que «talvez» é o mesmo que «com certeza»", "Talvez quer dizer que pode não acontecer."],
         ["Chamar de impossível o que é só difícil", "Ganhar um jogo é difícil, mas pode acontecer."],
         ["Não olhar o que há no saco", "Veja as cores antes de responder."]],
        P3.saco([("azul", 6)]))
    faq = [("O que o 1º ano aprende sobre probabilidade?", "A BNCC pede classificar acontecimentos do dia a dia como «acontecerá com certeza», «talvez aconteça» e «é impossível acontecer»."),
           ("Como brincar de probabilidade em casa?", "Ponha tampinhas de uma cor num saco e pergunte: que cor vai sair? Depois misture duas cores e pergunte de novo.")]
    make_unit(R, "probabilidade", "E", ["EF01MA20"],
              "Classificar eventos envolvendo o acaso, tais como «acontecerá com certeza», «talvez aconteça» e «é impossível acontecer», em situações do cotidiano",
              "Probabilidade: certo, talvez ou impossível", "Probabilidade",
              "Atividades de matemática para o 1º ano sobre probabilidade: acontece com certeza, talvez aconteça ou é impossível, bolinhas no saco e dados. 100 exercícios com gabarito.",
              "Certo, talvez ou impossível.", "Veja o que há no saco antes de responder.",
              body, faq, sets, 18, grade="1-ano")


if __name__ == "__main__":
    main()
