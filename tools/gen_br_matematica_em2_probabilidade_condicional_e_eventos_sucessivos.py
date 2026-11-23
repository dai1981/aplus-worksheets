# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 2ª série: Probabilidade condicional e eventos sucessivos (EM13MAT312, EM13MAT106)
  python3 tools/gen_br_matematica_em2_probabilidade_condicional_e_eventos_sucessivos.py
Eventos independentes (P(A e B) = P(A) · P(B)) e dependentes (sem reposição); árvore de probabilidades;
probabilidade condicional P(A | B) em tabelas de dupla entrada; k sucessos em n tentativas (binomial simples);
riscos e decisões (exames com falso positivo, eficácia de vacinas, seguros).
Usa geradores do 9º ano (independentes, dependentes, situações) com outro sorteio.
Erros: somar quando é «e», esquecer de diminuir o total sem reposição, dividir pelo total geral na condicional.
"""
import random
import math
from fractions import Fraction as F
from br_em import M, d, fq, bank, mix, lesson, use, unit, tab, num

R = random.Random(92014)
q_ind, q_dep, q_sit = use("gen_br_matematica_9_probabilidade", 92912, "s2_indep", "s3_dep", "s4_situacoes")


def s1_cond():
    a, b, c, e = [R.randint(5, 30) for _ in range(4)]
    tot = a + b + c + e
    t = tab([["", "Pratica esporte", "Não pratica", "Total"], ["Meninas", str(a), str(b), str(a + b)], ["Meninos", str(c), str(e), str(c + e)], ["Total", str(a + c), str(b + e), str(tot)]])
    k = R.choice(["m_dado_e", "e_dado_m", "simples", "e"])
    if k == "m_dado_e":
        p = F(a, a + c)
        return M(t + "Sorteando um aluno que pratica esporte, qual é a probabilidade de ser menina?", fq(p), [fq(F(a, tot)), fq(F(a, a + b)), fq(F(a + c, tot))], "Só entre os que praticam (%d): %d ÷ %d = <b>%s</b>." % (a + c, a, a + c, fq(p)))
    if k == "e_dado_m":
        p = F(c, c + e)
        return M(t + "Sorteando um menino, qual é a probabilidade de ele praticar esporte?", fq(p), [fq(F(c, tot)), fq(F(c, a + c)), fq(F(e, c + e))], "Só entre os meninos (%d): %d ÷ %d = <b>%s</b>." % (c + e, c, c + e, fq(p)))
    if k == "simples":
        p = F(b + e, tot)
        return M(t + "Sorteando um aluno qualquer, qual é a probabilidade de ele não praticar esporte?", fq(p), [fq(F(b, b + e)), fq(F(a + c, tot)), fq(F(b, tot))], "%d ÷ %d = <b>%s</b>." % (b + e, tot, fq(p)))
    p = F(a, tot)
    return M(t + "Sorteando um aluno qualquer, qual é a probabilidade de ser menina e praticar esporte?", fq(p), [fq(F(a, a + c)), fq(F(a, a + b)), fq(F(a + b, tot) * F(a + c, tot))], "%d ÷ %d = <b>%s</b>." % (a, tot, fq(p)))


def s2_binomial():
    k = R.choice(["moedas", "dado", "teste", "alvo", "pelo_menos"])
    if k == "alvo":
        pa = R.choice([F(1, 3), F(2, 5), F(3, 4), F(1, 4), F(2, 3)])
        n = R.choice([2, 3])
        j = R.randint(0, n)
        p = math.comb(n, j) * pa ** j * (1 - pa) ** (n - j)
        return M("Um atleta acerta o alvo com probabilidade %s em cada tiro. Em %d tiros, qual é a probabilidade de acertar exatamente %d?" % (fq(pa), n, j), fq(p), [fq(pa ** j) if j else fq(1 - pa), fq(F(j, n)), fq(pa ** j * (1 - pa) ** (n - j)) if math.comb(n, j) > 1 else fq(1 - p), fq(p / 2)],
                 "C(%d, %d) · (%s)%s · (%s)%s = <b>%s</b>." % (n, j, fq(pa), "⁰¹²³"[j], fq(1 - pa), "⁰¹²³"[n - j], fq(p)))
    if k == "pelo_menos":
        n = R.randint(2, 6)
        return M("Lançando %d moedas, qual é a probabilidade de sair pelo menos uma cara?" % n, fq(1 - F(1, 2 ** n)), [fq(F(1, 2 ** n)), fq(F(1, 2)), fq(F(n, 2 ** n))], "1 − P(nenhuma cara) = 1 − (1/2)%s = <b>%s</b>." % ("²³⁴⁵⁶"[n - 2], fq(1 - F(1, 2 ** n))))
    if k == "moedas":
        n = R.choice([3, 4, 5])
        j = R.randint(1, n - 1)
        p = F(math.comb(n, j), 2 ** n)
        return M("Lançando %d moedas, qual é a probabilidade de sair exatamente %d %s?" % (n, j, "cara" if j == 1 else "caras"), fq(p), [fq(F(1, 2 ** n)), fq(F(j, n)), fq(F(1, 2) ** j)], "C(%d, %d) · (1/2)%s = %d ÷ %d = <b>%s</b>." % (n, j, "³⁴⁵"[n - 3], math.comb(n, j), 2 ** n, fq(p)))
    if k == "dado":
        n = R.choice([2, 3])
        j = R.randint(1, n)
        p = math.comb(n, j) * F(1, 6) ** j * F(5, 6) ** (n - j)
        return M("Lançando um dado %d vezes, qual é a probabilidade de sair o número 6 exatamente %d %s?" % (n, j, "vez" if j == 1 else "vezes"), fq(p), [fq(F(1, 6) ** j), fq(F(j, 6)), fq(F(1, 6) ** j * F(5, 6) ** (n - j)) if math.comb(n, j) > 1 else fq(F(5, 6) ** n)],
                 "C(%d, %d) · (1/6)%s · (5/6)%s = <b>%s</b>." % (n, j, "¹²³"[j - 1], "⁰¹²"[n - j], fq(p)))
    n = R.choice([4, 5])
    return M("Numa prova com %d questões de 2 alternativas, um aluno chuta todas. Qual é a probabilidade de acertar todas?" % n, fq(F(1, 2 ** n)), [fq(F(1, 2 * n)), fq(F(1, n)), fq(F(n, 2 ** n))], "(1/2)%s = <b>%s</b>." % ("⁴⁵"[n - 4], fq(F(1, 2 ** n))))


def s3_risco():
    k = R.choice(["exame", "exame", "vacina", "seguro"])
    if k == "exame":
        n = R.choice([1000, 2000, 10000])
        prev = R.choice([F(1, 100), F(2, 100), F(5, 100)])
        sens = F(R.choice([90, 95, 99]), 100)
        fp = F(R.choice([5, 10]), 100)
        doentes = int(n * prev)
        vp = int(doentes * sens)
        fpos = int((n - doentes) * fp)
        p = F(vp, vp + fpos)
        return M("Numa população de %s pessoas, %s%% têm uma doença. Um exame dá positivo em %s%% dos doentes e, por engano, em %s%% dos sadios. Uma pessoa testou positivo. Qual é a probabilidade de ela ter a doença, aproximadamente?" % (num(n), d(prev * 100), d(sens * 100), d(fp * 100)),
                 "cerca de %s%%" % d(p * 100, 0), ["cerca de %s%%" % d(sens * 100, 0), "cerca de %s%%" % d(100 - fp * 100, 0), "cerca de %s%%" % d(prev * 100, 0)],
                 "Doentes positivos: %d; sadios positivos: %d; %d ÷ %d ≈ <b>%s%%</b>." % (vp, fpos, vp, vp + fpos, d(p * 100, 0)))
    if k == "vacina":
        a, b = R.choice([(10, 100), (5, 50), (20, 100), (4, 40)])
        return M("Num estudo, %d de cada 1.000 vacinados e %d de cada 1.000 não vacinados ficaram doentes. Quantas vezes o risco é menor entre os vacinados?" % (a, b), "%d vezes" % (b // a), ["%d vezes" % (b - a), "%d vezes" % (a), "o risco é igual"], "%d ÷ %d = <b>%d vezes</b>." % (b, a, b // a))
    p = R.choice([F(1, 100), F(2, 100), F(1, 50), F(5, 1000)])
    val = R.choice([20000, 50000, 80000])
    E = p * val
    return M("A chance de um carro ser roubado num ano é %s%%. O carro vale R$ %s. Qual é a perda esperada por ano (probabilidade × valor)?" % (d(p * 100), num(val)), "R$ %s" % num(E), ["R$ %s" % num(val * p * 10), "R$ %s" % num(val), "R$ %s" % num(E / 2)], "%s × %s = <b>R$ %s</b>." % (d(p), num(val), num(E)))


s4_conceitos = bank(R, [
    ("Dois eventos são independentes quando…", "um não muda a probabilidade do outro", ["não podem acontecer juntos", "têm a mesma probabilidade", "a soma é 1"]),
    ("Tirar duas bolas de uma urna sem reposição gera eventos…", "dependentes", ["independentes", "impossíveis", "complementares"]),
    ("Na probabilidade condicional P(A | B), dividimos pelo número de casos…", "em que B acontece", ["do total geral", "em que A acontece", "em que nenhum acontece"]),
    ("Uma moeda deu cara 5 vezes seguidas. A probabilidade de cara no próximo lançamento é…", "1/2", ["menor que 1/2", "maior que 1/2", "0"]),
    ("Um exame com 99% de acerto pode ter muitos falsos positivos quando…", "a doença é muito rara", ["a doença é muito comum", "o exame é caro", "o resultado é negativo"]),
    ("Se P(A) = 0,3 e P(B) = 0,5 e A e B são independentes, P(A e B) = …", "0,15", ["0,8", "0,2", "0,35"]),
    ("Numa árvore de probabilidades, ao longo de um caminho as probabilidades são…", "multiplicadas", ["somadas", "subtraídas", "divididas"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Eventos independentes", mix(R, seen, [(q_ind, 16), (s4_conceitos, 4)])),
        ("Eventos dependentes", mix(R, seen, [(q_dep, 20)])),
        ("Probabilidade condicional", mix(R, seen, [(s1_cond, 20)])),
        ("Repetir um experimento", mix(R, seen, [(s2_binomial, 17), (s4_conceitos, 3)])),
        ("Riscos e decisões", mix(R, seen, [(s3_risco, 12), (q_sit, 8)])),
    ]
    body = lesson(
        ["Em experimentos <b>sucessivos</b>, multiplique as probabilidades ao longo de cada caminho da árvore.",
         "<b>Independentes</b> (com reposição, moedas, dados): P(A e B) = P(A) · P(B). <b>Dependentes</b> (sem reposição): depois do 1º, o total muda.",
         "<b>Condicional</b>: P(A | B) = casos de A e B ÷ casos de B. Numa tabela, olhe só a linha ou a coluna de B.",
         "Exatamente k sucessos em n tentativas: C(n, k) · pᵏ · (1 − p)ⁿ⁻ᵏ.",
         "Para decidir com riscos, compare probabilidades: um exame positivo numa doença rara pode ser, muitas vezes, falso positivo."],
        [("Urna com 3 azuis e 2 vermelhas, sem reposição: duas azuis", ["3/5 · 2/4"], "3/10"),
         ("3 moedas: exatamente 2 caras", ["C(3, 2) · (1/2)³ = 3/8"], "3/8")],
        [["Somar quando é «e»", "Em sequência, multiplique."],
         ["Esquecer que o total diminui", "Sem reposição, o 2º sorteio tem uma bola a menos."],
         ["Dividir pelo total geral", "Na condicional, divida pelo número de casos da condição."]])
    faq = [("O que é probabilidade condicional?", "É a probabilidade de A sabendo que B aconteceu. Calcula-se só dentro dos casos de B: P(A | B) = casos de A e B ÷ casos de B."),
           ("O que a BNCC pede?", "Resolver e elaborar problemas que envolvem o cálculo de probabilidade de eventos em experimentos aleatórios sucessivos (EM13MAT312) e identificar situações da vida cotidiana nas quais seja necessário fazer escolhas levando-se em conta os riscos probabilísticos (EM13MAT106).")]
    unit(R, "probabilidade-condicional-e-eventos-sucessivos", "E", ["EM13MAT312", "EM13MAT106"],
         "Resolver e elaborar problemas que envolvem o cálculo de probabilidade de eventos em experimentos aleatórios sucessivos; identificar situações da vida cotidiana nas quais seja necessário fazer escolhas levando-se em conta os riscos probabilísticos (usar este ou aquele método contraceptivo, optar por um tratamento médico em detrimento de outro etc.)",
         "Probabilidade condicional e eventos sucessivos", "Probabilidade condicional",
         "Atividades de matemática para a 2ª série do Ensino Médio sobre probabilidade de eventos sucessivos: independentes e dependentes, árvore, probabilidade condicional em tabelas, repetições e riscos como falsos positivos. 100 exercícios com gabarito.",
         "Em sequência, multiplique", "Condicional: divida pelos casos da condição.",
         body, faq, sets, 14, grade="2-serie")


if __name__ == "__main__":
    main()
