# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: Gráficos e medidas de tendência central (Probabilidade e estatística, EF09MA21, EF09MA22)
  python3 tools/gen_br_matematica_9_graficos_e_estatistica.py
Gráficos enganosos (eixo que não começa no zero, escalas diferentes, figuras fora de proporção); escolher o gráfico
adequado (colunas, linhas, setores, histograma); ler gráficos; média, mediana, moda e amplitude; quando usar cada medida.
Erros: comparar só a altura das barras sem ver a escala, calcular a mediana sem ordenar, achar que a média é sempre o melhor resumo.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, grafico
from br_9 import M, d, unit, _svg, _t, _ln, INK, BLUE

R = random.Random(89021)
PROD = ["Arroz", "Feijão", "Café", "Leite", "Pão"]
MESES = ["jan", "fev", "mar", "abr", "mai", "jun"]


def barras(data, lo, hi, step, label="gráfico de colunas"):
    W, H, x0, y0, h = 360, 230, 56, 20, 170
    bw, gap = 48, 30
    s = [_ln(x0, y0, x0, y0 + h), _ln(x0, y0 + h, W - 10, y0 + h)]
    v = lo
    while v <= hi:
        y = y0 + h - (v - lo) * h / float(hi - lo)
        s.append(_ln(x0 - 4, y, x0, y, INK, 1.4))
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='#ddd' stroke-width='1'/>" % (x0, y, W - 10, y))
        s.append(_t(x0 - 8, y + 5, d(v), 13, INK, bold=False, anchor="end"))
        v += step
    for i, (nm, val) in enumerate(data):
        x = x0 + 24 + i * (bw + gap)
        y = y0 + h - (val - lo) * h / float(hi - lo)
        s.append("<rect x='%d' y='%.1f' width='%d' height='%.1f' fill='#7fa9da' stroke='%s'/>" % (x, y, bw, y0 + h - y, INK))
        s.append(_t(x + bw / 2, y0 + h + 18, nm, 13, INK, bold=False))
    return _svg(W, H, "".join(s), label)


def s1_enganoso():
    a = R.choice([90, 92, 94, 95, 96])
    b = a + R.choice([2, 3, 4])
    lo = a - 2
    k = R.choice(["vezes", "motivo", "real"])
    g = barras([("Loja A", a), ("Loja B", b)], lo, b + 1, 1, "gráfico de colunas com o eixo vertical começando em %d" % lo)
    if k == "vezes":
        ratio = F(b - lo, a - lo)
        return M(g + "Olhando só a altura das colunas, a da Loja B parece quantas vezes maior que a da Loja A?", "%s vezes" % d(ratio, 1) if (ratio * 10).denominator != 1 else "%s vezes" % d(ratio), ["1 vez (iguais)", "%s vezes" % d(ratio + 1), "%s vezes" % d(F(b, a), 2)],
                 "As colunas medem %d e %d unidades acima de %d: parece <b>%s vezes</b>, mas %d não é tão maior que %d." % (a - lo, b - lo, lo, d(ratio, 1), b, a))
    if k == "motivo":
        return M(g + "Por que este gráfico pode enganar o leitor?", "o eixo vertical não começa no zero", ["as colunas têm a mesma largura", "há poucas lojas", "os nomes estão embaixo"],
                 "Como o eixo começa em %d, a diferença parece muito maior: <b>o eixo vertical não começa no zero</b>." % lo)
    pc = F(b - a, a) * 100
    return M(g + "Qual é a diferença real entre as vendas, em porcentagem do valor da Loja A? (aproximada)", "cerca de %s%%" % d(pc, 0), ["cerca de %s%%" % d(F(b - lo, a - lo) * 100 - 100, 0), "cerca de 50%", "cerca de 200%", "cerca de 25%"],
             "(%d − %d) ÷ %d ≈ <b>%s%%</b>: a diferença real é pequena." % (b, a, a, d(pc, 0)))


def s2_escolher():
    q, a, w = R.choice([
        ("Qual gráfico é mais adequado para mostrar a temperatura de uma cidade ao longo dos 12 meses do ano?", "gráfico de linhas", ["gráfico de setores", "pictograma de pizza", "tabela de dupla entrada sem números"]),
        ("Qual gráfico é mais adequado para mostrar que parte do orçamento de uma família vai para cada tipo de gasto?", "gráfico de setores", ["gráfico de linhas", "histograma", "gráfico de dispersão"]),
        ("Qual gráfico é mais adequado para comparar o número de alunos de cada turma da escola?", "gráfico de colunas", ["gráfico de linhas", "gráfico de setores com 1 setor", "nenhum gráfico"]),
        ("Qual gráfico é mais adequado para mostrar as alturas dos alunos agrupadas em intervalos (150–155 cm, 155–160 cm…)?", "histograma", ["gráfico de setores", "gráfico de linhas", "pictograma"]),
        ("Qual gráfico é mais adequado para mostrar a evolução da população do Brasil de 1950 a 2020?", "gráfico de linhas", ["gráfico de setores", "histograma", "gráfico de colunas empilhadas sem datas"]),
        ("Num gráfico de setores, a soma de todas as partes deve ser…", "100% (o todo)", ["50%", "o maior valor", "qualquer valor"]),
        ("Qual gráfico é mais adequado para comparar, mês a mês, as vendas de duas lojas?", "gráfico de linhas com duas linhas (ou colunas duplas)", ["gráfico de setores", "histograma", "um único número"]),
        ("Uma pesquisa pergunta o esporte preferido de cada aluno (cada aluno escolhe um). Para mostrar a porcentagem de cada esporte, o melhor é…", "gráfico de setores", ["gráfico de linhas", "histograma", "gráfico de dispersão"]),
    ])
    return M(q, a, w, "Resposta: <b>%s</b>." % a)


def s3_ler():
    data = list(zip(R.sample(PROD, 4), [R.choice(range(10, 60, 5)) for _ in range(4)]))
    if len(set(v for _, v in data)) < 4:
        return None
    g = grafico(data, "kg vendidos")
    k = R.choice(["max", "dif", "total", "media"])
    if k == "max":
        nm, v = max(data, key=lambda x: x[1])
        return M(g + "O gráfico mostra os quilos vendidos de cada produto num dia. Qual produto vendeu mais?", nm, [n for n, _ in data if n != nm], "A coluna mais alta é a de <b>%s</b> (%d kg)." % (nm, v))
    if k == "dif":
        (n1, v1), (n2, v2) = R.sample(data, 2)
        return M(g + "Quantos quilos de %s foram vendidos a mais que de %s?" % (n1.lower(), n2.lower()) if v1 > v2 else g + "Quantos quilos de %s foram vendidos a mais que de %s?" % (n2.lower(), n1.lower()), "%d kg" % abs(v1 - v2), ["%d kg" % (v1 + v2), "%d kg" % max(v1, v2), "%d kg" % (abs(v1 - v2) + 5)],
                 "%d − %d = <b>%d kg</b>." % (max(v1, v2), min(v1, v2), abs(v1 - v2)))
    if k == "total":
        t = sum(v for _, v in data)
        return M(g + "Quantos quilos foram vendidos no total?", "%d kg" % t, ["%d kg" % (t - 5), "%d kg" % max(v for _, v in data), "%d kg" % (t + 10)], "%s = <b>%d kg</b>." % (" + ".join(str(v) for _, v in data), t))
    t = sum(v for _, v in data)
    return M(g + "Qual é a média de quilos vendidos por produto?", "%s kg" % d(F(t, 4)), ["%d kg" % t, "%s kg" % d(F(max(v for _, v in data) + min(v for _, v in data), 2)) if F(max(v for _, v in data) + min(v for _, v in data), 2) != F(t, 4) else "%s kg" % d(F(t, 4) + 5), "%s kg" % d(F(t, 3), 1)],
             "%d ÷ 4 = <b>%s kg</b>." % (t, d(F(t, 4))))


def s4_medidas():
    n = R.choice([5, 6, 7, 8, 9])
    xs = [R.randint(2, 20) for _ in range(n)]
    srt = sorted(xs)
    k = R.choice(["media", "mediana", "moda", "amp"])
    lst = ", ".join(map(str, xs))
    if k == "media":
        m = F(sum(xs), n)
        if (m * 10).denominator != 1:
            return None
        return M("Notas de um grupo: %s. Qual é a média?" % lst, d(m), [d(srt[n // 2]) if d(srt[n // 2]) != d(m) else d(m + 1), d(sum(xs)), d(F(srt[0] + srt[-1], 2)) if F(srt[0] + srt[-1], 2) != m else d(m - 1)],
                 "Soma %d ÷ %d = <b>%s</b>." % (sum(xs), n, d(m)))
    if k == "mediana":
        med = F(srt[n // 2]) if n % 2 else F(srt[n // 2 - 1] + srt[n // 2], 2)
        return M("Dados: %s. Qual é a mediana?" % lst, d(med), [d(xs[n // 2]) if d(xs[n // 2]) != d(med) else d(med + 1), d(F(sum(xs), n), 1), d(srt[n // 2 + 1]) if F(srt[n // 2 + 1]) != med else d(med + 2)],
                 "Em ordem: %s. %s <b>%s</b>." % (", ".join(map(str, srt)), "O valor do meio é" if n % 2 else "A média dos dois do meio é", d(med)))
    if k == "moda":
        v = R.choice(xs)
        xs2 = xs + [v, v]
        R.shuffle(xs2)
        cnt = {x: xs2.count(x) for x in xs2}
        mx = max(cnt.values())
        modes = [x for x in cnt if cnt[x] == mx]
        if len(modes) > 1:
            return None
        return M("Dados: %s. Qual é a moda?" % ", ".join(map(str, xs2)), d(modes[0]), [d(max(xs2)), d(sorted(xs2)[len(xs2) // 2]) if sorted(xs2)[len(xs2) // 2] != modes[0] else d(min(xs2)), d(mx)],
                 "O valor que mais aparece (%d vezes) é <b>%d</b>." % (mx, modes[0]))
    return M("Dados: %s. Qual é a amplitude?" % lst, d(srt[-1] - srt[0]), [d(srt[-1]), d(srt[-1] + srt[0]), d(srt[-1] - srt[1]) if srt[1] != srt[0] else d(srt[-1] - srt[0] + 1)],
             "Maior − menor = %d − %d = <b>%d</b>." % (srt[-1], srt[0], srt[-1] - srt[0]))


def s5_qual_medida():
    q, a, w = R.choice([
        ("Os salários de uma empresa são R$ 2.000,00, R$ 2.100,00, R$ 2.200,00, R$ 2.300,00 e R$ 40.000,00. Qual medida representa melhor o salário típico?", "a mediana", ["a média", "a amplitude", "o maior valor"]),
        ("Uma loja quer saber qual número de sapato é mais vendido para fazer o estoque. Qual medida usar?", "a moda", ["a média", "a amplitude", "a soma"]),
        ("Um valor muito diferente dos outros (muito alto) afeta mais…", "a média", ["a mediana", "a moda", "nenhuma medida"]),
        ("Para dados que não são números (cor preferida), qual medida de tendência central faz sentido?", "a moda", ["a média", "a mediana", "a amplitude"]),
        ("A amplitude mede…", "o quanto os dados estão espalhados (maior − menor)", ["o valor mais comum", "o valor do meio", "a soma dividida pela quantidade"]),
        ("Para calcular a mediana, primeiro é preciso…", "colocar os dados em ordem", ["somar todos os dados", "achar o valor mais frequente", "tirar o maior valor"]),
    ])
    return M(q, a, w, "Resposta: <b>%s</b>." % a)


def s6_linhas():
    vals = [R.choice(range(10, 40, 2)) for _ in MESES]
    if len(set(vals)) < 5:
        return None
    W, H, x0, y0, h = 380, 232, 50, 28, 160
    hi = 40
    s = [_ln(x0, y0, x0, y0 + h), _ln(x0, y0 + h, W - 10, y0 + h)]
    for v in range(0, hi + 1, 10):
        y = y0 + h - v * h / float(hi)
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='#ddd'/>" % (x0, y, W - 10, y))
        s.append(_t(x0 - 8, y + 5, str(v), 13, INK, bold=False, anchor="end"))
    pts = [(x0 + 30 + i * 55, y0 + h - v * h / float(hi)) for i, v in enumerate(vals)]
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='2.4'/>" % (" ".join("%.1f,%.1f" % p for p in pts), BLUE))
    for (x, y), m, v in zip(pts, MESES, vals):
        s.append("<circle cx='%.1f' cy='%.1f' r='4' fill='%s'/>" % (x, y, BLUE))
        s.append(_t(x, y - 10, str(v), 12, BLUE))
        s.append(_t(x, y0 + h + 18, m, 13, INK, bold=False))
    g = _svg(W, H, "".join(s), "gráfico de linhas com valores de janeiro a junho")
    k = R.choice(["subida", "max"])
    if k == "subida":
        dif = [(vals[i + 1] - vals[i], i) for i in range(5)]
        best = max(dif)
        if [x[0] for x in dif].count(best[0]) > 1 or best[0] <= 0:
            return None
        i = best[1]
        return M(g + "O gráfico mostra as vendas de sorvete (em centenas) de janeiro a junho. Entre quais meses houve o maior aumento?", "de %s para %s" % (MESES[i], MESES[i + 1]),
                 ["de %s para %s" % (MESES[j], MESES[j + 1]) for j in range(5) if j != i][:3], "Aumento de %d, o maior: <b>de %s para %s</b>." % (best[0], MESES[i], MESES[i + 1]))
    m = max(vals)
    if vals.count(m) > 1:
        return None
    return M(g + "O gráfico mostra as vendas de sorvete (em centenas) de janeiro a junho. Em que mês as vendas foram maiores?", MESES[vals.index(m)], [x for x in MESES if x != MESES[vals.index(m)]][:3],
             "O ponto mais alto é <b>%s</b> (%d)." % (MESES[vals.index(m)], m))


def main():
    seen = set()
    sets = [
        ("Gráficos que enganam", mix(R, seen, [(s1_enganoso, 14), (s2_escolher, 6)])),
        ("Escolher e ler gráficos", mix(R, seen, [(s3_ler, 14), (s6_linhas, 6)])),
        ("Média, mediana, moda e amplitude", mix(R, seen, [(s4_medidas, 20)])),
        ("Qual medida usar?", mix(R, seen, [(s5_qual_medida, 6), (s4_medidas, 8), (s6_linhas, 6)])),
        ("Revisão", mix(R, seen, [(s3_ler, 8), (s1_enganoso, 6), (s4_medidas, 6)])),
    ]
    body = lesson(
        ["Antes de tirar conclusões de um gráfico, veja o <b>título</b>, as <b>unidades</b> e a <b>escala</b>. Um eixo que não começa no zero pode exagerar diferenças pequenas.",
         "Escolha o gráfico pela pergunta: colunas para comparar categorias, linhas para mostrar evolução no tempo, setores para partes de um todo, histograma para dados em intervalos.",
         "Média = soma ÷ quantidade. Mediana = valor do meio dos dados em ordem. Moda = valor mais frequente. Amplitude = maior − menor."],
        [("Dados 4, 7, 7, 9, 13", ["soma 40 ÷ 5", "meio: 7", "mais frequente: 7"], "média 8, mediana 7, moda 7"),
         ("Eixo começando em 90: colunas de 92 e 96", ["altura 2 e 6"], "parece 3 vezes, mas a diferença real é ≈ 4%")],
        [["Comparar só a altura das colunas", "Olhe onde começa o eixo."],
         ["Calcular a mediana sem ordenar", "Coloque os dados em ordem primeiro."],
         ["Usar sempre a média", "Com um valor muito diferente, a mediana representa melhor."]],
        barras([("A", 92), ("B", 96)], 90, 97, 1))
    faq = [("Como um gráfico pode enganar?", "Com o eixo vertical começando acima do zero, escalas diferentes, intervalos desiguais ou figuras que crescem em área e não só em altura. Por isso é importante ler a escala antes de comparar."),
           ("O que a BNCC pede no 9º ano?", "Analisar e identificar, em gráficos divulgados pela mídia, os elementos que podem induzir a erros de leitura (EF09MA21) e escolher e construir o gráfico mais adequado, com a análise das medidas de tendência central e da amplitude (EF09MA22).")]
    unit(R, "graficos-e-estatistica", "E", ["EF09MA21", "EF09MA22"],
         "Analisar e identificar, em gráficos divulgados pela mídia, os elementos que podem induzir, às vezes propositadamente, erros de leitura; escolher e construir o gráfico mais adequado (colunas, setores, linhas), com ou sem uso de planilhas, para apresentar um determinado conjunto de dados, destacando aspectos como as medidas de tendência central",
         "Gráficos, leitura crítica e medidas de tendência central", "Gráficos e estatística",
         "Atividades de matemática para o 9º ano sobre gráficos e estatística: gráficos enganosos, escolher o gráfico adequado, ler gráficos de colunas e linhas, média, mediana, moda e amplitude. 100 exercícios com gabarito.",
         "Leia a escala antes de comparar.", "Média, mediana, moda e amplitude resumem os dados.",
         body, faq, sets, 21)


if __name__ == "__main__":
    main()
