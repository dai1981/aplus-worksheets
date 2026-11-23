# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 1ª série: Medidas de tendência central e de dispersão (EM13MAT316)
  python3 tools/gen_br_matematica_em1_medidas_de_tendencia_central_e_dispersao.py
Média, média ponderada, mediana e moda; amplitude, desvio médio, variância e desvio padrão (populacional);
comparar a regularidade de dois grupos; efeito de somar ou multiplicar todos os valores.
Usa geradores do 8º ano (mediana, moda) e do 9º ano (média, mediana e moda) com outro sorteio.
Erros: esquecer de elevar os desvios ao quadrado, esquecer a raiz no desvio padrão, usar média simples quando há pesos.
"""
import random
import math
from fractions import Fraction as F
from br_em import M, d, par, bank, mix, lesson, use, unit, tab, sq

R = random.Random(91015)
m_mediana, m_moda = use("gen_br_matematica_8_medidas_de_tendencia_central", 91910, "s1_mediana", "s2_moda")
m_med9 = use("gen_br_matematica_9_graficos_e_estatistica", 91911, "s4_medidas")


def lista(xs):
    return "; ".join(d(x) for x in xs)


def dados(n):
    """n valores inteiros com média inteira e variância com raiz exata"""
    for _ in range(400):
        m = R.randint(5, 20)
        devs = [R.randint(-6, 6) for _ in range(n - 1)]
        last = -sum(devs)
        if abs(last) > 8:
            continue
        devs.append(last)
        var = F(sum(x * x for x in devs), n)
        if var.denominator == 1 and math.isqrt(int(var)) ** 2 == var and var > 0:
            xs = [m + x for x in devs]
            if min(xs) > 0:
                R.shuffle(xs)
                return xs, m, var
    return None


def s1_dp():
    n = R.choice([4, 5, 6, 8])
    r = dados(n)
    if not r:
        return None
    xs, m, var = r
    dp = math.isqrt(int(var))
    k = R.choice(["var", "dp", "dp"])
    if k == "var":
        return M("Dados: %s (média %d). Qual é a variância?" % (lista(xs), m), d(var), [d(dp), d(sum(abs(x - m) for x in xs)), d(F(sum((x - m) ** 2 for x in xs), n - 1), 2) if n > 1 else d(var + 1)],
                 "Desvios ao quadrado: %s; soma %d; ÷ %d = <b>%s</b>." % (" + ".join(str((x - m) ** 2) for x in xs), sum((x - m) ** 2 for x in xs), n, d(var)))
    return M("Dados: %s. Qual é o desvio padrão?" % lista(xs), d(dp), [d(var), d(F(sum(abs(x - m) for x in xs), n), 2), d(dp + 1)],
             "Média %d; variância = %s ÷ %d = %s; desvio padrão = √%s = <b>%d</b>." % (m, sum((x - m) ** 2 for x in xs), n, d(var), d(var), dp))


def s2_ponderada():
    k = R.choice(["notas", "tab", "dm"])
    if k == "notas":
        ns = [R.randint(4, 10) for _ in range(3)]
        ps = R.choice([(1, 2, 2), (2, 3, 5), (1, 1, 2), (3, 3, 4), (1, 2, 3)])
        mp = F(sum(a * b for a, b in zip(ns, ps)), sum(ps))
        if (mp * 10).denominator != 1:
            return None
        return M("Um aluno tirou %s nas provas de pesos %s. Qual é a média ponderada?" % (lista(ns), "; ".join(map(str, ps))), d(mp), [d(F(sum(ns), 3), 1), d(sum(a * b for a, b in zip(ns, ps))), d(mp + F(1, 2))],
                 "(%s) ÷ %d = <b>%s</b>." % (" + ".join("%d · %d" % (a, b) for a, b in zip(ns, ps)), sum(ps), d(mp)))
    if k == "tab":
        vs = sorted(R.sample(range(1, 8), 3))
        fs = [R.randint(2, 9) for _ in vs]
        mp = F(sum(a * b for a, b in zip(vs, fs)), sum(fs))
        if (mp * 100).denominator != 1:
            return None
        t = tab([["Gols por jogo", "Nº de jogos"]] + [[str(v), str(f)] for v, f in zip(vs, fs)])
        return M(t + "Qual é a média de gols por jogo?", d(mp), [d(F(sum(vs), 3), 2), d(F(sum(fs), 3), 2), d(sum(a * b for a, b in zip(vs, fs)))],
                 "(%s) ÷ %d = <b>%s</b>." % (" + ".join("%d · %d" % (a, b) for a, b in zip(vs, fs)), sum(fs), d(mp)))
    n = R.choice([4, 5])
    r = dados(n)
    if not r:
        return None
    xs, m, _ = r
    dm = F(sum(abs(x - m) for x in xs), n)
    if (dm * 100).denominator != 1:
        return None
    return M("Dados: %s (média %d). Qual é o desvio médio?" % (lista(xs), m), d(dm), [d(sum(abs(x - m) for x in xs)), d(F(sum((x - m) ** 2 for x in xs), n), 2), "0"],
             "Média dos desvios absolutos: (%s) ÷ %d = <b>%s</b>." % (" + ".join(str(abs(x - m)) for x in xs), n, d(dm)))


def s3_comparar():
    k = R.choice(["regular", "soma", "mult", "dpzero"])
    if k == "regular":
        a, b = R.sample(range(1, 6), 2)
        ga, gb = R.sample(["Turma A", "Turma B"], 2)
        return M("A %s e a %s têm média 7 nas provas. O desvio padrão da %s é %d e o da %s é %d. Qual turma tem notas mais regulares (homogêneas)?" % (ga, gb, ga, a, gb, b), ga if a < b else gb, [gb if a < b else ga, "as duas igualmente", "não dá para saber"],
                 "Menor desvio padrão = dados mais próximos da média: <b>%s</b>." % (ga if a < b else gb))
    if k == "soma":
        c = R.randint(2, 10)
        dp = R.randint(2, 6)
        return M("Um conjunto tem média 20 e desvio padrão %d. Se somarmos %d a todos os valores, o desvio padrão será…" % (dp, c), str(dp), [str(dp + c), str(dp * c), "0"], "Somar a todos desloca, mas não espalha: desvio padrão <b>%d</b>." % dp)
    if k == "mult":
        c = R.choice([2, 3, 10])
        dp = R.randint(2, 6)
        return M("Um conjunto tem desvio padrão %d. Se todos os valores forem multiplicados por %d, o novo desvio padrão será…" % (dp, c), str(dp * c), [str(dp), str(dp * c * c), str(dp + c)], "Multiplicar por %d multiplica o desvio padrão por %d: <b>%d</b>." % (c, c, dp * c))
    v = R.randint(3, 20)
    return M("Num conjunto, todos os %d valores são iguais a %d. Qual é o desvio padrão?" % (R.randint(5, 12), v), "0", [str(v), "1", sq(v) if sq(v) != str(v) else str(v * v)], "Não há afastamento da média: <b>0</b>.")


s4_conceitos = bank(R, [
    ("O desvio padrão mede…", "o quanto os dados se espalham em torno da média", ["o valor central", "o valor mais frequente", "a soma dos dados"]),
    ("O desvio padrão é a raiz quadrada…", "da variância", ["da média", "da amplitude", "da mediana"]),
    ("Se o desvio padrão é 0, então…", "todos os valores são iguais", ["a média é 0", "os dados são negativos", "não há dados"]),
    ("A variância de um conjunto é 16. O desvio padrão é…", "4", ["8", "256", "16"]),
    ("Qual medida é mais afetada por um valor extremo?", "a média", ["a mediana", "a moda", "nenhuma"]),
    ("A amplitude usa…", "só o maior e o menor valor", ["todos os valores", "só a média", "só a moda"]),
    ("Para calcular a variância, elevamos os desvios ao quadrado porque…", "senão os desvios positivos e negativos se anulam", ["fica mais fácil", "a média é sempre positiva", "é a regra da mediana"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Média, mediana e moda", mix(R, seen, [(m_med9, 8), (m_mediana, 6), (m_moda, 6)])),
        ("Média ponderada e desvio médio", mix(R, seen, [(s2_ponderada, 20)])),
        ("Variância e desvio padrão", mix(R, seen, [(s1_dp, 20)])),
        ("Comparar dispersões", mix(R, seen, [(s3_comparar, 13), (s4_conceitos, 7)])),
        ("Revisão", mix(R, seen, [(s1_dp, 8), (s2_ponderada, 8), (s3_comparar, 4)])),
    ]
    body = lesson(
        ["<b>Tendência central</b>: média (soma ÷ quantidade), mediana (valor do meio, com os dados em ordem) e moda (mais frequente). <b>Média ponderada</b>: some valor × peso e divida pela soma dos pesos.",
         "<b>Dispersão</b>: mostra o quanto os dados se espalham. Amplitude = maior − menor. Desvio médio = média dos |x − média|.",
         "<b>Variância</b> = média dos (x − média)². <b>Desvio padrão</b> = √variância, na mesma unidade dos dados.",
         "Somar um número a todos os dados não muda o desvio padrão; multiplicar por k multiplica o desvio padrão por k."],
        [("Dados 2; 4; 4; 4; 5; 5; 7; 9 (média 5)", ["desvios²: 9, 1, 1, 1, 0, 0, 4, 16", "soma 32 ÷ 8 = 4"], "variância 4; desvio padrão 2")],
        [["Somar os desvios sem elevar ao quadrado", "A soma dos desvios dá sempre 0."],
         ["Esquecer a raiz", "Desvio padrão = √variância."],
         ["Usar média simples com pesos", "Multiplique cada valor pelo seu peso."]])
    faq = [("Para que serve o desvio padrão?", "Mostra se os dados estão próximos da média (desvio padrão pequeno, grupo homogêneo) ou espalhados (desvio padrão grande)."),
           ("O que a BNCC pede?", "Resolver e elaborar problemas, em diferentes contextos, que envolvem cálculo e interpretação das medidas de tendência central (média, moda, mediana) e das medidas de dispersão (amplitude, variância e desvio padrão) (EM13MAT316).")]
    unit(R, "medidas-de-tendencia-central-e-dispersao", "E", ["EM13MAT316"],
         "Resolver e elaborar problemas, em diferentes contextos, que envolvem cálculo e interpretação das medidas de tendência central (média, moda, mediana) e das medidas de dispersão (amplitude, variância e desvio padrão)",
         "Média, mediana, moda, variância e desvio padrão", "Medidas de tendência central e dispersão",
         "Atividades de matemática para a 1ª série do Ensino Médio sobre medidas estatísticas: média, média ponderada, mediana, moda, amplitude, desvio médio, variância e desvio padrão. 100 exercícios com gabarito.",
         "Desvio padrão = √variância", "Mede o quanto os dados se afastam da média.",
         body, faq, sets, 15, grade="1-serie")


if __name__ == "__main__":
    main()
