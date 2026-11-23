# -*- coding: utf-8 -*-
"""
Brasil Matemática 8º ano: Gráficos e classes de frequência (Probabilidade e estatística, EF08MA23, EF08MA24)
  python3 tools/gen_br_matematica_8_graficos_e_classes_de_frequencia.py
Escolher o gráfico adequado (colunas, linhas, setores, histograma); ler gráficos de colunas;
organizar dados em classes (intervalos ⊢), frequência absoluta e relativa, amplitude da classe, ponto médio; ler histogramas.
Usa geradores do 9º ano (escolher, ler e gráficos que enganam) com outro sorteio.
Erros: contar o valor do limite superior na classe errada, confundir frequência absoluta e relativa, esquecer o eixo começando no zero.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, use
from br_9 import M, d, fq, bank, tab, unit, _svg, _t, _ln, INK

R = random.Random(88018)
g_engan, g_escolher, g_ler = use("gen_br_matematica_9_graficos_e_estatistica", 88918, "s1_enganoso", "s2_escolher", "s3_ler")
NB = " "
TEMAS = [("altura", "cm", (140, 145, 150, 155, 160, 165, 170)), ("massa", "kg", (30, 35, 40, 45, 50, 55, 60)),
         ("tempo", "s", (50, 55, 60, 65, 70, 75, 80)), ("idade", "anos", (0, 10, 20, 30, 40, 50, 60)),
         ("nota", "pontos", (0, 2, 4, 6, 8, 10))]
DESC = {"altura": "a altura dos alunos de uma turma", "massa": "a massa dos alunos de uma turma", "tempo": "o tempo de corrida dos atletas de um clube",
        "idade": "a idade dos visitantes de um museu", "nota": "a nota de uma turma numa prova"}
QUEM = {"altura": "alunos", "massa": "alunos", "tempo": "atletas", "idade": "visitantes", "nota": "alunos"}


def cl(a, b):
    return "%d%s⊢%s%d" % (a, NB, NB, b)


def histo(lims, fr, un):
    W, H, x0, y0, h = 380, 240, 46, 16, 180
    n = len(fr)
    bw = (W - x0 - 20) / float(n)
    top = max(fr)
    step = 2 if top <= 12 else 5
    hi = ((top + step - 1) // step) * step
    s = [_ln(x0, y0, x0, y0 + h), _ln(x0, y0 + h, W - 10, y0 + h)]
    for v in range(0, hi + 1, step):
        y = y0 + h - v * h / float(hi)
        s.append(_ln(x0 - 4, y, x0, y, INK, 1.4))
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='#ddd' stroke-width='1'/>" % (x0, y, W - 10, y))
        s.append(_t(x0 - 8, y + 5, str(v), 13, INK, bold=False, anchor="end"))
    for i, f in enumerate(fr):
        x = x0 + i * bw
        y = y0 + h - f * h / float(hi)
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#7fa9da' stroke='%s'/>" % (x, y, bw, y0 + h - y, INK))
    for i, L in enumerate(lims[:n + 1]):
        s.append(_t(x0 + i * bw, y0 + h + 18, str(L), 13, INK, bold=False))
    s.append(_t((x0 + W) / 2, y0 + h + 36, "(%s)" % un, 12, INK, bold=False))
    return _svg(W, H + 12, "".join(s), "histograma")


def tabela(nome, un, lims, fr):
    return tab([["%s (%s)" % (nome.capitalize(), un), "Frequência"]] + [[cl(lims[i], lims[i + 1]), str(f)] for i, f in enumerate(fr)])


def dados():
    nome, un, L = R.choice(TEMAS)
    n = R.choice([4, 5]) if len(L) > 5 else 4
    lims = list(L[:n + 1])
    fr = [R.randint(1, 12) for _ in range(n)]
    return nome, un, lims, fr


def s1_classes():
    nome, un, lims, fr = dados()
    k = R.choice(["amp", "pm", "freq", "total", "rel", "maior"])
    t = tabela(nome, un, lims, fr)
    a = lims[1] - lims[0]
    if k == "amp":
        return M(t + "Qual é a amplitude de cada classe da tabela?", "%d %s" % (a, un), ["%d %s" % (lims[-1] - lims[0], un), "%d %s" % (len(fr), un) if len(fr) != a else "%d %s" % (a * 2, un), "%d %s" % (a + 1, un)],
                 "%d − %d = <b>%d %s</b>." % (lims[1], lims[0], a, un))
    i = R.randrange(len(fr))
    if k == "pm":
        pm = F(lims[i] + lims[i + 1], 2)
        return M(t + "Qual é o ponto médio da classe %s?" % cl(lims[i], lims[i + 1]), "%s %s" % (d(pm), un), ["%d %s" % (lims[i + 1], un), "%d %s" % (lims[i], un), "%d %s" % (fr[i], un) if fr[i] != pm else "%d %s" % (a, un)],
                 "(%d + %d) ÷ 2 = <b>%s %s</b>." % (lims[i], lims[i + 1], d(pm), un))
    if k == "total":
        return M(t + "Quantos dados há ao todo na tabela?", str(sum(fr)), [str(len(fr)), str(max(fr)), str(sum(fr) - fr[0])], "%s = <b>%d</b>." % (" + ".join(map(str, fr)), sum(fr)))
    if k == "rel":
        T = sum(fr)
        p = F(fr[i], T) * 100
        if (p * 10).denominator != 1:
            return None
        return M(t + "Qual é a frequência relativa da classe %s, em porcentagem?" % cl(lims[i], lims[i + 1]), "%s%%" % d(p), ["%d%%" % fr[i], "%s%%" % d(F(100, len(fr))) if F(100, len(fr)) != p else "%d%%" % (fr[i] * 2), "%s%%" % d(100 - p) if 100 - p != p else "%d%%" % T],
                 "%d ÷ %d = %s = <b>%s%%</b>." % (fr[i], T, d(F(fr[i], T)), d(p)))
    if k == "maior":
        if fr.count(max(fr)) > 1:
            return None
        j = fr.index(max(fr))
        return M(t + "Qual classe tem a maior frequência?", cl(lims[j], lims[j + 1]), [cl(lims[m], lims[m + 1]) for m in range(len(fr)) if m != j], "A maior frequência é %d, na classe <b>%s</b>." % (fr[j], cl(lims[j], lims[j + 1])))
    if i == 0:
        return None
    return M(t + "A tabela mostra %s. Quantos %s ficam abaixo de %d %s?" % (DESC[nome], QUEM[nome], lims[i], un), str(sum(fr[:i])), [str(fr[i - 1]), str(sum(fr[:i + 1])), str(sum(fr) - sum(fr[:i]))],
             "Somamos as classes abaixo de %d: %s = <b>%d</b>." % (lims[i], " + ".join(map(str, fr[:i])), sum(fr[:i])))


def s2_agrupar():
    a = R.choice([5, 10])
    lo = R.choice([20, 30, 40, 50]) if a == 10 else R.choice([10, 20, 30])
    vals = sorted(R.randint(lo, lo + 3 * a - 1) for _ in range(R.randint(10, 14)))
    k = R.randrange(3)
    A, B = lo + k * a, lo + (k + 1) * a
    c = sum(1 for v in vals if A <= v < B)
    edge = sum(1 for v in vals if A <= v <= B)
    w = [str(edge) if edge != c else str(c + 1), str(sum(1 for v in vals if A < v <= B)) if sum(1 for v in vals if A < v <= B) != c else str(c + 2), str(len(vals) - c)]
    return M("Dados: %s.<br>Quantos dados ficam na classe %s? (O símbolo ⊢ inclui o primeiro número e não inclui o segundo.)" % ("; ".join(map(str, vals)), cl(A, B)), str(c), w,
             "Contamos de %d até antes de %d: <b>%d</b> dados." % (A, B, c))


def s3_histo():
    nome, un, lims, fr = dados()
    if len(set(fr)) < len(fr):
        return None
    g = histo(lims, fr, un)
    k = R.choice(["classe", "total", "acima", "maior"])
    i = R.randrange(len(fr))
    if k == "classe":
        return M(g + "O histograma mostra %s. Quantos %s estão na classe %s?" % (DESC[nome], QUEM[nome], cl(lims[i], lims[i + 1])), str(fr[i]), [str(fr[i] + 1), str(lims[i + 1] - lims[i]), str(sum(fr[:i + 1])) if i else str(fr[i] + 2)],
                 "A coluna sobre %s vai até <b>%d</b>." % (cl(lims[i], lims[i + 1]), fr[i]))
    if k == "total":
        return M(g + "O histograma mostra %s. Quantos %s há ao todo?" % (DESC[nome], QUEM[nome]), str(sum(fr)), [str(len(fr)), str(max(fr)), str(sum(fr) + 2)], "%s = <b>%d</b>." % (" + ".join(map(str, fr)), sum(fr)))
    if k == "acima":
        if i == 0:
            return None
        return M(g + "O histograma mostra %s. Quantos %s têm %d %s ou mais?" % (DESC[nome], QUEM[nome], lims[i], un), str(sum(fr[i:])), [str(fr[i]), str(sum(fr[:i])), str(sum(fr[i + 1:])) if i + 1 < len(fr) else str(fr[i] + 1)],
                 "%s = <b>%d</b>." % (" + ".join(map(str, fr[i:])), sum(fr[i:])))
    j = fr.index(max(fr))
    return M(g + "O histograma mostra %s. Qual classe tem mais %s?" % (DESC[nome], QUEM[nome]), cl(lims[j], lims[j + 1]), [cl(lims[m], lims[m + 1]) for m in range(len(fr)) if m != j], "A coluna mais alta é <b>%s</b>." % cl(lims[j], lims[j + 1]))


s4_conceitos = bank(R, [
    ("Num histograma, as colunas…", "ficam encostadas, porque as classes são intervalos seguidos", ["ficam sempre separadas", "mostram partes de um todo", "não têm altura"]),
    ("A classe 10 ⊢ 20 inclui o número…", "10, mas não o 20", ["20, mas não o 10", "10 e 20", "nem 10 nem 20"]),
    ("O ponto médio da classe 40 ⊢ 50 é…", "45", ["40", "50", "10"]),
    ("A frequência relativa de uma classe é…", "a frequência da classe ÷ total de dados", ["o número de classes", "a amplitude da classe", "a soma das classes"]),
    ("Para mostrar a evolução da inflação mês a mês, o gráfico mais adequado é o de…", "linhas", ["setores", "histograma", "pictograma"]),
    ("Para mostrar como as alturas de 40 alunos se distribuem em intervalos, o gráfico mais adequado é o…", "histograma", ["de setores", "de linhas", "pictograma"]),
    ("A soma das frequências relativas de todas as classes é…", "100%", ["50%", "o número de classes", "a maior frequência"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Escolher o gráfico adequado", mix(R, seen, [(g_escolher, 8), (s4_conceitos, 7), (g_engan, 5)])),
        ("Ler gráficos de colunas", mix(R, seen, [(g_ler, 14), (g_engan, 6)])),
        ("Agrupar dados em classes", mix(R, seen, [(s2_agrupar, 20)])),
        ("Tabelas de frequência com classes", mix(R, seen, [(s1_classes, 20)])),
        ("Histogramas", mix(R, seen, [(s3_histo, 20)])),
    ]
    body = lesson(
        ["Escolha o gráfico pela pergunta: <b>colunas</b> para comparar categorias, <b>linhas</b> para evolução no tempo, <b>setores</b> para partes de um todo, <b>histograma</b> para dados em intervalos.",
         "Com muitos dados numéricos, agrupe-os em <b>classes</b> de mesma amplitude. 10 ⊢ 20 inclui o 10 e não inclui o 20.",
         "Na tabela: frequência (quantos), frequência relativa (frequência ÷ total), ponto médio ((início + fim) ÷ 2).",
         "No <b>histograma</b>, cada classe é uma coluna encostada na outra; a altura é a frequência."],
        [("Classe 150 ⊢ 155 com 6 alunos de 24", ["6 ÷ 24 = 0,25"], "25%"),
         ("Ponto médio de 30 ⊢ 40", ["(30 + 40) ÷ 2"], "35")],
        [["Contar o limite de cima na classe", "Em 10 ⊢ 20, o 20 vai para a classe seguinte."],
         ["Confundir frequência com frequência relativa", "A relativa é uma parte do total (fração ou %)."],
         ["Ler o gráfico sem ver a escala", "Veja onde começa o eixo e de quanto em quanto ele sobe."]],
        histo([150, 155, 160, 165, 170], [4, 9, 7, 3], "cm"))
    faq = [("O que é uma classe de frequência?", "É um intervalo de valores, como 150 ⊢ 155 cm. Agrupamos os dados em classes de mesma amplitude e contamos quantos caem em cada uma."),
           ("O que a BNCC pede no 8º ano?", "Avaliar a adequação de diferentes tipos de gráficos para representar um conjunto de dados de uma pesquisa (EF08MA23) e classificar as frequências de uma variável contínua de uma pesquisa em classes, de modo que resumam os dados de maneira adequada para a tomada de decisões (EF08MA24).")]
    unit(R, "graficos-e-classes-de-frequencia", "E", ["EF08MA23", "EF08MA24"],
         "Avaliar a adequação de diferentes tipos de gráficos para representar um conjunto de dados de uma pesquisa; classificar as frequências de uma variável contínua de uma pesquisa em classes, de modo que resumam os dados de maneira adequada para a tomada de decisões",
         "Gráficos e classes de frequência", "Gráficos e classes de frequência",
         "Atividades de matemática para o 8º ano sobre gráficos e classes de frequência: escolher o gráfico adequado, agrupar dados em classes, tabelas de frequência, ponto médio e histogramas. 100 exercícios com gabarito.",
         "Classes: 10 ⊢ 20 inclui o 10, não o 20", "Histograma: colunas encostadas.",
         body, faq, sets, 18, grade="8-ano")


if __name__ == "__main__":
    main()
