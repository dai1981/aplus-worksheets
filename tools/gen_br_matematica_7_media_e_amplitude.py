# -*- coding: utf-8 -*-
"""
Brasil Matemática 7º ano: Média aritmética e amplitude (Probabilidade e estatística, EF07MA35)
  python3 tools/gen_br_matematica_7_media_e_amplitude.py
Média aritmética como «nivelamento»; amplitude como medida de dispersão; média a partir de tabelas de frequência; valor que falta
para obter uma média; efeito de um valor muito diferente; comparar grupos pela média e pela amplitude.
Usa geradores do 9º ano (medidas de tendência central) com outro sorteio.
Erros: esquecer de dividir pela quantidade de valores, usar o maior valor como amplitude, multiplicar errado na tabela de frequência.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, use
from br_9 import M, d, bank, tab, unit

R = random.Random(87019)
g_med = use("gen_br_matematica_9_graficos_e_estatistica", 87919, "s4_medidas")


def s1_media():
    n = R.choice([4, 5, 6])
    while True:
        xs = [R.randint(10, 40) for _ in range(n)]
        if sum(xs) % n == 0:
            break
    ctx = R.choice(["Os gols de um time nas rodadas foram", "As temperaturas máximas (°C) da semana foram", "Os pontos de Bia em %d jogos foram" % n, "As idades dos primos de Lia são"])
    m = sum(xs) // n
    return M("%s %s. Qual é a média?" % (ctx, ", ".join(map(str, xs))), d(m), [d(sum(xs)), d(sorted(xs)[n // 2]) if sorted(xs)[n // 2] != m else d(m + 1), d(F(max(xs) + min(xs), 2), 1) if F(max(xs) + min(xs), 2) != m else d(m - 2)],
             "Soma %d ÷ %d = <b>%s</b>." % (sum(xs), n, d(m)))


def s2_amplitude():
    xs = R.sample(range(5, 90), R.choice([5, 6, 7]))
    a = max(xs) - min(xs)
    return M("Dados: %s. Qual é a amplitude?" % ", ".join(map(str, xs)), d(a), [d(max(xs)), d(max(xs) + min(xs)), d(sorted(xs)[-2] - min(xs)) if sorted(xs)[-2] - min(xs) != a else d(a + 1)],
             "Amplitude = maior − menor = %d − %d = <b>%d</b>." % (max(xs), min(xs), a))


def s3_tabela():
    vals = sorted(R.sample(range(0, 6), 4))
    fs = [R.randint(1, 8) for _ in vals]
    n = sum(fs)
    s = sum(v * f for v, f in zip(vals, fs))
    if (F(s, n) * 10).denominator != 1:
        return None
    t = tab([["Nº de irmãos", "Nº de alunos"]] + [[str(v), str(f)] for v, f in zip(vals, fs)])
    return M(t + "Qual é a média do número de irmãos da turma?", d(F(s, n)), [d(F(sum(vals), len(vals)), 2) if (F(sum(vals), len(vals)) * 100).denominator == 1 else d(F(s, n) + 1), d(F(s, len(vals)), 1) if (F(s, len(vals)) * 10).denominator == 1 else d(s), d(F(n, len(vals)), 2) if (F(n, len(vals)) * 100).denominator == 1 else d(F(s, n) + F(1, 2))],
             "Multiplique e some: %s = %d; ÷ %d alunos = <b>%s</b>." % (" + ".join("%d × %d" % (v, f) for v, f in zip(vals, fs)), s, n, d(F(s, n))))


def s4_falta():
    n = R.choice([3, 4, 5])
    m = R.randint(6, 9)
    xs = [R.randint(4, 10) for _ in range(n - 1)]
    x = m * n - sum(xs)
    if not 0 <= x <= 10:
        return None
    return M("Para passar, Rui precisa de média %d em %d provas. Ele tirou %s. Quanto precisa tirar na última prova?" % (m, n, ", ".join(map(str, xs))), d(x), [d(m), d(x + 1), d(F(sum(xs), n - 1), 1) if (F(sum(xs), n - 1) * 10).denominator == 1 else d(x - 1)],
             "A soma precisa ser %d × %d = %d; %d − %d = <b>%d</b>." % (m, n, m * n, m * n, sum(xs), x))


s5_conceitos = bank(R, [
    ("A média aritmética de 4, 6 e 8 é…", "6", ["18", "4", "8"]),
    ("Se todos os valores aumentam 2, a média…", "aumenta 2", ["não muda", "dobra", "aumenta 4"]),
    ("Se todos os valores aumentam 2, a amplitude…", "não muda", ["aumenta 2", "dobra", "aumenta 4"]),
    ("Um valor muito maior que os outros faz a média…", "subir bastante", ["ficar igual", "descer", "virar zero"]),
    ("Dois grupos têm a mesma média, mas o grupo A tem amplitude maior. Isso quer dizer que…", "os valores de A são mais espalhados", ["A tem mais valores", "A tem valores maiores", "os grupos são iguais"]),
    ("A amplitude mede…", "a diferença entre o maior e o menor valor", ["o valor do meio", "o valor mais frequente", "a soma dos valores"]),
    ("A média de 5 números é 10. A soma desses números é…", "50", ["10", "15", "2"]),
    ("A média sempre é um dos valores do conjunto?", "não necessariamente", ["sim, sempre", "sim, é o do meio", "sim, é o maior"]),
], "s5_conceitos")


def main():
    seen = set()
    sets = [
        ("Média aritmética", mix(R, seen, [(s1_media, 20)])),
        ("Amplitude", mix(R, seen, [(s2_amplitude, 14), (s5_conceitos, 6)])),
        ("Média em tabelas", mix(R, seen, [(s3_tabela, 20)])),
        ("Quanto falta para a média?", mix(R, seen, [(s4_falta, 20)])),
        ("Revisão", mix(R, seen, [(g_med, 16), (s5_conceitos, 2), (s2_amplitude, 2)])),
    ]
    body = lesson(
        ["A <b>média aritmética</b> é a soma dos valores dividida pela quantidade de valores. É como «nivelar» todos os valores.",
         "A <b>amplitude</b> (maior − menor) mostra o quanto os dados estão espalhados.",
         "Numa tabela de frequência, multiplique cada valor pela frequência, some e divida pelo total de pessoas."],
        [("Notas 6, 7, 9 e 10", ["32 ÷ 4"], "média 8; amplitude 10 − 6 = 4"),
         ("Média 7 em 3 provas, já tirou 6 e 8", ["21 − 14"], "precisa de 7")],
        [["Esquecer de dividir", "Some e divida pela quantidade."],
         ["Usar o maior valor como amplitude", "Amplitude = maior − menor."],
         ["Dividir pelo número de linhas da tabela", "Divida pelo total de pessoas (soma das frequências)."]])
    faq = [("Como calcular a média aritmética?", "Some todos os valores e divida pela quantidade de valores. Numa tabela, multiplique cada valor pela sua frequência antes de somar."),
           ("O que a BNCC pede no 7º ano?", "Compreender, em contextos significativos, o significado de média estatística como indicador da tendência de uma pesquisa, calcular seu valor e relacioná-lo, intuitivamente, com a amplitude do conjunto de dados (EF07MA35).")]
    unit(R, "media-e-amplitude", "E", ["EF07MA35"],
         "Compreender, em contextos significativos, o significado de média estatística como indicador da tendência de uma pesquisa, calcular seu valor e relacioná-lo, intuitivamente, com a amplitude do conjunto de dados",
         "Média aritmética e amplitude", "Média e amplitude",
         "Atividades de matemática para o 7º ano sobre média aritmética e amplitude: calcular a média, média em tabelas de frequência, valor que falta para a média e amplitude. 100 exercícios com gabarito.",
         "Média = soma ÷ quantidade.", "Amplitude = maior − menor.",
         body, faq, sets, 19, grade="7-ano")


if __name__ == "__main__":
    main()
