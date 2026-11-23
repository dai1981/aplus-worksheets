# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: Probabilidade de eventos independentes e dependentes (Probabilidade e estatística, EF09MA20)
  python3 tools/gen_br_matematica_9_probabilidade.py
Espaço amostral de experimentos em etapas (moedas, dados, urnas), árvore de possibilidades, princípio multiplicativo;
eventos independentes (com reposição) e dependentes (sem reposição); P(A e B) = P(A) · P(B depois de A); porcentagem.
Erros: somar em vez de multiplicar, esquecer que sem reposição o total diminui, contar (2, 3) e (3, 2) como o mesmo resultado.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix
from br_9 import M, d, fq, unit

R = random.Random(89020)
CORES = ["azuis", "vermelhas", "verdes", "amarelas", "pretas", "brancas"]
UMA = {"azuis": "azul", "vermelhas": "vermelha", "verdes": "verde", "amarelas": "amarela", "pretas": "preta", "brancas": "branca"}


def pc(p):
    return fq(p)


def s1_espaco():
    k = R.choice(["moedas", "dados", "roupas", "senha", "moeda_dado"])
    if k == "moedas":
        n = R.choice([2, 3, 4])
        return M("Quantos resultados tem o espaço amostral ao lançar %d moedas?" % n, d(2 ** n), [d(2 * n), d(n), d(2 ** n + 1), d(n * n) if n != 2 else d(3)],
                 "Cada moeda tem 2 resultados: 2%s = <b>%d</b>." % ("".join(" · 2" for _ in range(n - 1)), 2 ** n))
    if k == "dados":
        n = R.choice([2, 3])
        return M("Quantos resultados tem o espaço amostral ao lançar %d dados comuns?" % n, d(6 ** n), [d(6 * n), d(6 + n), d(11) if n == 2 else d(16)],
                 "6%s = <b>%d</b>." % ("".join(" · 6" for _ in range(n - 1)), 6 ** n))
    if k == "roupas":
        a, b, c = R.randint(2, 5), R.randint(2, 4), R.randint(1, 3)
        return M("Ana tem %d blusas, %d saias e %d pares de tênis. De quantas maneiras ela pode se vestir com uma peça de cada?" % (a, b, c), d(a * b * c), [d(a + b + c), d(a * b), d(a * b + c)],
                 "Princípio multiplicativo: %d · %d · %d = <b>%d</b>." % (a, b, c, a * b * c))
    if k == "senha":
        n = R.choice([2, 3, 4])
        return M("Quantas senhas de %d algarismos (0 a 9, podendo repetir) existem?" % n, d(10 ** n), [d(10 * n), d(9 ** n), d(10 ** n - 1)],
                 "10 escolhas para cada algarismo: 10%s = <b>%s</b>." % ("".join(" · 10" for _ in range(n - 1)), d(10 ** n)))
    return M("Lança-se uma moeda e um dado comum. Quantos resultados tem o espaço amostral?", "12", ["8", "6", "36"], "2 · 6 = <b>12</b>.")


def s2_indep():
    k = R.choice(["moedas", "dado_moeda", "dois_dados", "urna_rep"])
    if k == "moedas":
        n = R.choice([2, 3, 4])
        return M("Lançando %d moedas, qual é a probabilidade de sair cara %s?" % (n, "nas duas" if n == 2 else "em todas"), pc(F(1, 2 ** n)), [pc(F(1, 2 * n)) if n != 2 else pc(F(3, 4)), pc(F(1, 2)), pc(F(n, 2 ** n)) if n != 2 else pc(F(1, 3))],
                 "Eventos independentes: (1/2)%s = <b>1/%d</b>." % ("".join(" · (1/2)" for _ in range(n - 1)), 2 ** n))
    if k == "dado_moeda":
        f = R.choice([("um número par", 3), ("o número 6", 1), ("um número maior que 4", 2), ("um múltiplo de 3", 2), ("um número menor que 5", 4)])
        p = F(f[1], 6) * F(1, 2)
        return M("Lança-se um dado comum e uma moeda. Qual é a probabilidade de sair %s no dado e coroa na moeda?" % f[0], pc(p), [pc(F(f[1], 6) + F(1, 2)) if F(f[1], 6) + F(1, 2) < 1 else pc(F(f[1], 6)), pc(F(f[1], 6)), pc(F(1, 12)) if p != F(1, 12) else pc(F(1, 6))],
                 "P = %s · 1/2 = <b>%s</b>." % ("%d/6" % f[1], "%d/%d" % (p.numerator, p.denominator)))
    if k == "dois_dados":
        a, b = R.randint(1, 6), R.randint(1, 6)
        return M("Lançando dois dados comuns, qual é a probabilidade de sair %d no primeiro e %d no segundo?" % (a, b), pc(F(1, 36)), [pc(F(1, 6)), pc(F(1, 12)), pc(F(2, 36))],
                 "1/6 · 1/6 = <b>1/36</b>.")
    c1, c2 = R.sample(CORES, 2)
    x, y = R.randint(2, 7), R.randint(2, 7)
    t = x + y
    p = F(x, t) * F(y, t)
    return M("Uma urna tem %d bolas %s e %d %s. Tira-se uma bola, anota-se a cor e ela é <b>devolvida</b>. Tira-se outra. Qual é a probabilidade de sair uma bola %s e depois uma %s?" % (x, c1, y, c2, UMA[c1], UMA[c2]), pc(p),
             [pc(F(x, t) * F(y, t - 1)), pc(F(x + y, 2 * t)) if F(x + y, 2 * t) != p else pc(F(1, t)), pc(F(x, t) + F(y, t)) if x + y < t else pc(F(x * y, t))],
             "Com reposição, os eventos são independentes: %d/%d · %d/%d = <b>%s</b>." % (x, t, y, t, "%d/%d" % (p.numerator, p.denominator)))


def s3_dep():
    c1, c2 = R.sample(CORES, 2)
    x, y = R.randint(2, 7), R.randint(2, 7)
    t = x + y
    k = R.choice(["ab", "aa"])
    if k == "ab":
        p = F(x, t) * F(y, t - 1)
        return M("Uma urna tem %d bolas %s e %d %s. Tiram-se duas bolas, uma depois da outra, <b>sem reposição</b>. Qual é a probabilidade de a 1ª ser %s e a 2ª ser %s?" % (x, c1, y, c2, UMA[c1], UMA[c2]), pc(p),
                 [pc(F(x, t) * F(y, t)), pc(F(x, t) * F(y - 1, t - 1)) if y > 1 else pc(F(1, t)), pc(F(x + y, t + t - 1)) if F(x + y, 2 * t - 1) != p else pc(F(x, t))],
                 "Depois da 1ª, sobram %d bolas: %d/%d · %d/%d = <b>%s</b>." % (t - 1, x, t, y, t - 1, "%d/%d" % (p.numerator, p.denominator)))
    p = F(x, t) * F(x - 1, t - 1)
    return M("Uma urna tem %d bolas %s e %d %s. Tiram-se duas bolas, sem reposição. Qual é a probabilidade de as duas serem %s?" % (x, c1, y, c2, c1), pc(p),
             [pc(F(x, t) ** 2), pc(F(x, t) * F(x - 1, t)), pc(F(2 * x - 1, 2 * t - 1)), pc(F(x, t))],
             "%d/%d · %d/%d = <b>%s</b>." % (x, t, x - 1, t - 1, "%d/%d" % (p.numerator, p.denominator)))


def s4_situacoes():
    k = R.choice(["sorteio", "cartas", "turma", "porcent"])
    if k == "sorteio":
        n = R.choice([10, 20, 25, 30, 40])
        return M("Numa turma de %d alunos, sorteiam-se dois alunos diferentes para representante e vice. Qual é a probabilidade de Lucas ser o representante e Bia a vice?" % n, pc(F(1, n * (n - 1))), [pc(F(1, n * n)), pc(F(2, n)), pc(F(1, n))],
                 "1/%d · 1/%d = <b>1/%d</b> (sem reposição)." % (n, n - 1, n * (n - 1)))
    if k == "cartas":
        a = R.choice([("ás", 4), ("rei", 4), ("carta de copas", 13)])
        p = F(a[1], 52) * F(a[1] - 1, 51)
        return M("De um baralho de 52 cartas, tiram-se duas cartas sem reposição. Qual é a probabilidade de as duas serem %s?" % ("ases" if a[0] == "ás" else ("reis" if a[0] == "rei" else "de copas")), pc(p), [pc(F(a[1], 52) ** 2), pc(F(2 * a[1], 52)), pc(F(a[1], 52))],
                 "%d/52 · %d/51 = <b>%s</b>." % (a[1], a[1] - 1, "%d/%d" % (p.numerator, p.denominator)))
    if k == "turma":
        m, f = R.randint(8, 16), R.randint(8, 16)
        t = m + f
        p = F(f, t) * F(f - 1, t - 1)
        return M("Numa turma há %d meninos e %d meninas. Sorteiam-se dois estudantes diferentes. Qual é a probabilidade de serem duas meninas?" % (m, f), pc(p), [pc(F(f, t) ** 2), pc(F(f, t)), pc(F(2 * f, t * 2 - 1))],
                 "%d/%d · %d/%d = <b>%s</b>." % (f, t, f - 1, t - 1, "%d/%d" % (p.numerator, p.denominator)))
    p1, p2 = R.choice([(F(1, 2), F(1, 5)), (F(3, 5), F(1, 2)), (F(4, 5), F(1, 4)), (F(1, 4), F(2, 5)), (F(7, 10), F(1, 2))])
    p = p1 * p2
    return M("A chance de chover no sábado é %s%% e, de modo independente, no domingo é %s%%. Qual é a probabilidade de chover nos dois dias?" % (d(p1 * 100), d(p2 * 100)), "%s%%" % d(p * 100),
             ["%s%%" % d((p1 + p2) * 100), "%s%%" % d((p1 + p2) * 50), "%s%%" % d(p * 10, 1)], "%s · %s = %s = <b>%s%%</b>." % (d(p1), d(p2), d(p), d(p * 100)))


def s5_teoria():
    q, a, w = R.choice([
        ("Tirar duas bolas de uma urna <b>com reposição</b>: os eventos são…", "independentes", ["dependentes", "impossíveis", "certos"]),
        ("Tirar duas bolas de uma urna <b>sem reposição</b>: os eventos são…", "dependentes", ["independentes", "impossíveis", "iguais"]),
        ("Uma moeda deu cara 5 vezes seguidas. A probabilidade de dar cara no 6º lançamento é…", "1/2", ["menor que 1/2", "maior que 1/2", "0"]),
        ("Se A e B são independentes, P(A e B) é igual a…", "P(A) · P(B)", ["P(A) + P(B)", "P(A) − P(B)", "P(A) ÷ P(B)"]),
        ("O resultado do 1º dado influencia o resultado do 2º dado?", "não, os lançamentos são independentes", ["sim, sempre", "só se sair 6", "só se forem dados iguais"]),
        ("Num sorteio sem reposição, depois de tirar uma bola, o total de bolas na urna…", "diminui 1", ["fica igual", "aumenta 1", "dobra"]),
        ("Lançando dois dados, (2, 5) e (5, 2) são…", "resultados diferentes do espaço amostral", ["o mesmo resultado", "resultados impossíveis", "o único resultado com soma 7"]),
    ])
    return M(q, a, w, "Resposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Espaço amostral e princípio multiplicativo", mix(R, seen, [(s1_espaco, 16), (s5_teoria, 4)])),
        ("Eventos independentes", mix(R, seen, [(s2_indep, 20)])),
        ("Eventos dependentes (sem reposição)", mix(R, seen, [(s3_dep, 20)])),
        ("Probabilidade em situações", mix(R, seen, [(s4_situacoes, 17), (s5_teoria, 3)])),
        ("Revisão", mix(R, seen, [(s2_indep, 8), (s3_dep, 8), (s1_espaco, 4)])),
    ]
    body = lesson(
        ["Num experimento em etapas, o número de resultados é o produto das possibilidades de cada etapa (princípio multiplicativo).",
         "Eventos <b>independentes</b>: um não muda a chance do outro (moedas, dados, sorteio com reposição). P(A e B) = P(A) · P(B).",
         "Eventos <b>dependentes</b>: o primeiro muda o segundo (sorteio sem reposição). Depois de tirar uma bola, o total diminui.",
         "A árvore de possibilidades ajuda a ver todos os caminhos."],
        [("Urna com 3 azuis e 2 vermelhas, sem reposição: azul e azul", ["3/5 · 2/4"], "6/20 = 3/10"),
         ("Mesma urna, com reposição: azul e azul", ["3/5 · 3/5"], "9/25")],
        [["Somar em vez de multiplicar", "«E» em etapas: multiplique."],
         ["Esquecer que o total diminui sem reposição", "Na 2ª retirada, há uma bola a menos."],
         ["Contar (2, 5) e (5, 2) como um só", "São resultados diferentes."]])
    faq = [("Qual é a diferença entre eventos independentes e dependentes?", "Nos independentes, o resultado de um não altera a probabilidade do outro (como lançar duas moedas). Nos dependentes, altera (como tirar duas bolas sem devolver a primeira)."),
           ("O que a BNCC pede no 9º ano?", "Reconhecer, em experimentos aleatórios, eventos independentes e dependentes e calcular a probabilidade de sua ocorrência, nos dois casos (EF09MA20).")]
    unit(R, "probabilidade", "E", ["EF09MA20"],
         "Reconhecer, em experimentos aleatórios, eventos independentes e dependentes e calcular a probabilidade de sua ocorrência, nos dois casos",
         "Probabilidade de eventos independentes e dependentes", "Probabilidade",
         "Atividades de matemática para o 9º ano sobre probabilidade: espaço amostral, princípio multiplicativo, eventos independentes e dependentes, com e sem reposição. 100 exercícios com gabarito.",
         "Independentes: multiplique as probabilidades.", "Sem reposição, o total diminui a cada retirada.",
         body, faq, sets, 20)


if __name__ == "__main__":
    main()
