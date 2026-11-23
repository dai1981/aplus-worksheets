# -*- coding: utf-8 -*-
"""
Brasil Matemática 8º ano: Medidas de tendência central e amplitude (Probabilidade e estatística, EF08MA25)
  python3 tools/gen_br_matematica_8_medidas_de_tendencia_central.py
Média, moda e mediana (com quantidade par e ímpar de dados), amplitude; média em tabelas de frequência;
qual medida representa melhor os dados (valores muito diferentes).
Usa geradores do 7º ano (média, amplitude, tabela) e do 9º ano (medidas, qual medida usar) com outro sorteio.
Erros: calcular a mediana sem ordenar, com quantidade par escolher só um dos valores do meio, dizer que não há moda quando há duas.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, use
from br_9 import M, d, bank, unit

R = random.Random(88019)
m_media, m_amp, m_tab = use("gen_br_matematica_7_media_e_amplitude", 88919, "s1_media", "s2_amplitude", "s3_tabela")
m_med, m_qual = use("gen_br_matematica_9_graficos_e_estatistica", 88929, "s4_medidas", "s5_qual_medida")
CTX = [("as notas de um aluno", ""), ("os gols de um time em cada jogo", ""), ("as idades de um grupo de amigos", " anos"),
       ("as temperaturas máximas da semana", " °C"), ("os minutos que Rafa leu por dia", " min"), ("as alturas de plantas", " cm")]


def lista(xs):
    return "; ".join(map(str, xs))


def s1_mediana():
    n = R.choice([4, 6, 8, 5, 7])
    xs = [R.randint(1, 30) for _ in range(n)]
    o = sorted(xs)
    if len(set(xs)) < n or xs == o:
        return None
    ctx, un = R.choice(CTX)
    if n % 2:
        md = F(o[n // 2])
        w = [d(F(xs[n // 2])) if xs[n // 2] != md else d(md + 1), d(F(sum(xs), n), 1) if F(sum(xs), n) != md else d(md - 1), d(F(o[0] + o[-1], 2), 1) if F(o[0] + o[-1], 2) != md else d(md + 2)]
        e = "Em ordem: %s. O valor do meio é <b>%s</b>." % (lista(o), d(md))
    else:
        md = F(o[n // 2 - 1] + o[n // 2], 2)
        w = [d(F(o[n // 2 - 1])), d(F(o[n // 2])), d(F(xs[n // 2 - 1] + xs[n // 2], 2)) if F(xs[n // 2 - 1] + xs[n // 2], 2) != md else d(md + 1)]
        e = "Em ordem: %s. Os dois do meio são %d e %d: (%d + %d) ÷ 2 = <b>%s</b>." % (lista(o), o[n // 2 - 1], o[n // 2], o[n // 2 - 1], o[n // 2], d(md))
    return M("Os dados mostram %s: %s. Qual é a mediana?" % (ctx, lista(xs)), d(md) + un, [x + un for x in w], e)


def s2_moda():
    k = R.choice(["uma", "duas", "nenhuma"])
    base = R.sample(range(1, 20), 6)
    if k == "uma":
        xs = base[:5] + [base[0], base[0]]
        a = str(base[0])
    elif k == "duas":
        xs = base[:5] + [base[0], base[1]]
        a = "%d e %d" % tuple(sorted(base[:2]))
    else:
        xs = base[:]
        a = "não há moda"
    R.shuffle(xs)
    w = ["não há moda" if k != "nenhuma" else str(max(xs)), str(max(xs)) if k != "nenhuma" else "todos os valores", str(sorted(xs)[len(xs) // 2]), str(base[0]) if k == "duas" else str(len(xs))]
    e = {"uma": "O %s aparece 3 vezes: moda = <b>%s</b>." % (a, a), "duas": "O %s aparecem 2 vezes cada: as modas são <b>%s</b> (bimodal)." % (a.replace(" e ", " e o "), a),
         "nenhuma": "Cada valor aparece uma vez só: <b>não há moda</b>."}[k]
    return M("Qual é a moda dos dados %s?" % lista(xs), a, w, e)


def s3_mudanca():
    n = R.choice([4, 5])
    xs = [R.randint(2, 20) for _ in range(n)]
    s = sum(xs)
    if s % n:
        return None
    m = s // n
    k = R.choice(["soma", "novo", "tira"])
    if k == "soma":
        c = R.randint(2, 10)
        return M("A média dos dados %s é %d. Se somarmos %d a cada valor, qual será a nova média?" % (lista(xs), m, c), str(m + c), [str(m), str(m + c * n), str(m * c)],
                 "Todos sobem %d, a média também: %d + %d = <b>%d</b>." % (c, m, c, m + c))
    if k == "novo":
        nv = m * (n + 1) - s + R.choice([0, n + 1, 2 * (n + 1)])
        nm = F(s + nv, n + 1)
        if nv < 0 or nm.denominator != 1:
            return None
        return M("A média de %d números é %d. Juntando o número %d, qual é a nova média?" % (n, m, nv), d(nm), [d(F(m + nv, 2)), d(F(s + nv, n)), str(m)] if nm != m else [d(F(m + nv, 2)) if F(m + nv, 2) != m else str(m + 1), d(F(s + nv, n)), str(m + 1)],
                 "Soma antiga: %d × %d = %d; nova soma: %d + %d = %d; ÷ %d = <b>%s</b>." % (n, m, s, s, nv, s + nv, n + 1, d(nm)))
    t = R.choice(xs)
    nm = F(s - t, n - 1)
    if nm.denominator != 1 or nm == m:
        return None
    return M("Os dados são %s (média %d). Tirando o valor %d, qual é a nova média?" % (lista(xs), m, t), d(nm), [str(m), d(F(s - t, n)) if F(s - t, n) != nm else str(m - 1), str(m - t) if m - t > 0 else str(m + t)],
             "(%d − %d) ÷ %d = <b>%s</b>." % (s, t, n - 1, d(nm)))


s4_conceitos = bank(R, [
    ("Para achar a mediana, primeiro é preciso…", "colocar os dados em ordem", ["somar os dados", "achar a moda", "tirar o maior valor"]),
    ("Com 6 dados em ordem, a mediana é…", "a média dos dois valores do meio (3º e 4º)", ["o 3º valor", "o 6º valor", "o valor mais frequente"]),
    ("Os salários de uma empresa são quase todos parecidos, mas o do dono é muito alto. Qual medida representa melhor o salário típico?", "a mediana", ["a média", "a amplitude", "o maior valor"]),
    ("Numa pesquisa sobre o tamanho de sapato mais vendido, a medida mais útil para a loja é…", "a moda", ["a média", "a amplitude", "a soma"]),
    ("Um conjunto pode ter duas modas?", "sim, quando dois valores aparecem o mesmo número máximo de vezes", ["não, nunca", "só se tiver números pares", "só se a média for zero"]),
    ("A amplitude dos dados 3, 8, 15, 6 é…", "12", ["15", "3", "8"]),
    ("Se todos os valores de um conjunto forem iguais a 7, a média, a moda e a mediana são…", "todas iguais a 7", ["0", "diferentes", "7, 0 e 7"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Média e amplitude", mix(R, seen, [(m_media, 12), (m_amp, 8)])),
        ("Mediana", mix(R, seen, [(s1_mediana, 20)])),
        ("Moda", mix(R, seen, [(s2_moda, 14), (s4_conceitos, 6)])),
        ("Média, mediana e moda", mix(R, seen, [(m_med, 12), (m_tab, 8)])),
        ("Qual medida usar? Problemas", mix(R, seen, [(m_qual, 6), (s3_mudanca, 14)])),
    ]
    body = lesson(
        ["<b>Média</b>: soma dos valores ÷ quantidade de valores.",
         "<b>Mediana</b>: com os dados em ordem, o valor do meio. Com quantidade par, a média dos dois valores do meio.",
         "<b>Moda</b>: o valor que mais aparece. Pode haver duas modas ou nenhuma.",
         "<b>Amplitude</b>: maior − menor. Mostra o quanto os dados estão espalhados.",
         "Se há um valor muito diferente dos outros, a mediana costuma representar melhor os dados do que a média."],
        [("Dados 8; 3; 10; 5", ["em ordem: 3; 5; 8; 10", "(5 + 8) ÷ 2"], "mediana 6,5"),
         ("Dados 2; 4; 4; 6; 9", ["soma 25 ÷ 5", "mais frequente"], "média 5, moda 4")],
        [["Achar a mediana sem ordenar", "Coloque os dados em ordem antes."],
         ["Com quantidade par, pegar só um valor do meio", "Faça a média dos dois valores do meio."],
         ["Dizer que não há moda quando há duas", "Dois valores com a mesma frequência máxima: são duas modas."]])
    faq = [("Como calcular a mediana com uma quantidade par de dados?", "Coloque os dados em ordem e faça a média dos dois valores do meio. Para 3, 5, 8, 10, a mediana é (5 + 8) ÷ 2 = 6,5."),
           ("O que a BNCC pede no 8º ano?", "Obter os valores de medidas de tendência central de uma pesquisa estatística (média, moda e mediana) com a compreensão de seus significados e relacioná-los com a dispersão de dados, indicada pela amplitude (EF08MA25).")]
    unit(R, "medidas-de-tendencia-central", "E", ["EF08MA25"],
         "Obter os valores de medidas de tendência central de uma pesquisa estatística (média, moda e mediana) com a compreensão de seus significados e relacioná-los com a dispersão de dados, indicada pela amplitude",
         "Média, moda, mediana e amplitude", "Medidas de tendência central",
         "Atividades de matemática para o 8º ano sobre medidas de tendência central: média, mediana com quantidade par e ímpar, moda, amplitude e qual medida usar. 100 exercícios com gabarito.",
         "Média, moda e mediana", "Mediana: ordene os dados primeiro.",
         body, faq, sets, 19, grade="8-ano")


if __name__ == "__main__":
    main()
