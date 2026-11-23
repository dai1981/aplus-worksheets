# -*- coding: utf-8 -*-
"""
Brasil Matemática 5º ano: Tabelas e gráficos (Probabilidade e estatística, EF05MA24, EF05MA25)
  python3 tools/gen_br_matematica_5_tabelas_e_graficos.py
Tabelas de dupla entrada; gráficos de colunas simples e duplas; gráficos de linhas (aumentou, diminuiu, maior variação);
variáveis categóricas e numéricas; escolher o gráfico adequado; tirar conclusões (texto de síntese) em contextos de saúde, trânsito e escola.
Erros: ler a coluna errada, não ver a escala do eixo, confundir o maior valor com o maior aumento.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, table, grafico, wrap, line, text, INK, GREEN, BLUE, RED, Kids

R = random.Random(80522)
K = Kids(R)
MESES = ["jan.", "fev.", "mar.", "abr.", "maio", "jun.", "jul.", "ago.", "set.", "out.", "nov.", "dez."]

GRID = [("Vacinas aplicadas no posto de saúde", ["segunda", "terça", "quarta", "quinta"], ["crianças", "adultos"], (20, 90)),
        ("Veículos que passaram no cruzamento", ["7h às 8h", "12h às 13h", "18h às 19h"], ["carros", "motos"], (40, 250)),
        ("Alunos que usam o transporte escolar", ["4º ano", "5º ano", "6º ano"], ["manhã", "tarde"], (12, 60)),
        ("Livros emprestados pela biblioteca", ["março", "abril", "maio", "junho"], ["infantis", "juvenis"], (30, 150)),
        ("Garrafas recicladas pela escola", ["1º bimestre", "2º bimestre", "3º bimestre"], ["vidro", "plástico"], (50, 400)),
        ("Pessoas atendidas na farmácia", ["sábado", "domingo"], ["manhã", "tarde"], (30, 120))]


def dupla():
    t, rows, cols, (lo, hi) = R.choice(GRID)
    v = [[R.randint(lo, hi) for _ in cols] for _ in rows]
    tb = "<p><b>%s</b></p>" % t + table([""] + cols, [[r] + [num(x) for x in vv] for r, vv in zip(rows, v)])
    return t, rows, cols, v, tb


def s1_dupla():
    t, rows, cols, v, tb = dupla()
    k = R.choice(["cel", "linha", "coluna", "dif", "max", "total"])
    i, j = R.randrange(len(rows)), R.randrange(len(cols))
    if k == "cel":
        a = v[i][j]
        return mcq(tb + "Quantos «%s» na linha «%s»?" % (cols[j], rows[i]), num(a), [num(x) for x in (v[i][1 - j], v[(i + 1) % len(rows)][j], a + v[i][1 - j])],
                   "Cruze a linha «%s» com a coluna «%s»: <b>%s</b>." % (rows[i], cols[j], num(a)))
    if k == "linha":
        s = sum(v[i])
        return mcq(tb + "Qual é o total de «%s» (somando as colunas)?" % rows[i], num(s), [num(x) for x in (v[i][0], sum(r[0] for r in v), s + 10)],
                   "%s = <b>%s</b>." % (" + ".join(num(x) for x in v[i]), num(s)))
    if k == "coluna":
        s = sum(r[j] for r in v)
        return mcq(tb + "Qual é o total de «%s» em todas as linhas?" % cols[j], num(s), [num(x) for x in (sum(v[0]), s - v[0][j], s + 10)],
                   "%s = <b>%s</b>." % (" + ".join(num(r[j]) for r in v), num(s)))
    if k == "dif":
        a, b = v[i][0], v[i][1]
        if a == b:
            return None
        return mcq(tb + "Na linha «%s», qual é a diferença entre «%s» e «%s»?" % (rows[i], cols[0], cols[1]), num(abs(a - b)), [num(x) for x in (a + b, max(a, b), abs(a - b) + 10)],
                   "%s − %s = <b>%s</b>." % (num(max(a, b)), num(min(a, b)), num(abs(a - b))))
    if k == "max":
        col = [r[j] for r in v]
        if len(set(col)) < len(col):
            return None
        m = rows[col.index(max(col))]
        return mcq(tb + "Em que linha houve mais «%s»?" % cols[j], m, [r for r in rows if r != m] + ["em todas foi igual"],
                   "Compare a coluna «%s»: o maior número é %s, em <b>%s</b>." % (cols[j], num(max(col)), m))
    s = sum(sum(r) for r in v)
    return mcq(tb + "Qual é o total geral da tabela?", num(s), [num(x) for x in (sum(v[0]), sum(r[0] for r in v), s + 100)],
               "Some todos os números da tabela: <b>%s</b>." % num(s))


def colunas_duplas(cats, a, b, la, lb, step):
    mx = max(a + b)
    top = -(-mx // step) * step
    W, H = 60 + len(cats) * 70, 210
    y0, hgt = 180, 150
    s = []
    for k in range(0, top + 1, step):
        y = y0 - hgt * k / top
        s.append(line(46, y, W - 6, y, "#d6dde4", 1))
        s.append(text(40, y + 4, num(k), 11, anchor="end"))
    for i, c in enumerate(cats):
        x = 56 + i * 70
        for j, (vals, col) in enumerate(((a, "#64b5f6"), (b, "#ffb74d"))):
            h = hgt * vals[i] / top
            s.append("<rect x='%d' y='%.1f' width='24' height='%.1f' fill='%s' stroke='%s'/>" % (x + j * 26, y0 - h, h, col, INK))
        s.append(text(x + 25, y0 + 16, c, 12))
    s.append(line(46, y0, W - 6, y0, INK, 2))
    s.append("<rect x='%d' y='4' width='12' height='12' fill='#64b5f6'/>" % (W - 170) + text(W - 154, 14, la, 12, anchor="start"))
    s.append("<rect x='%d' y='4' width='12' height='12' fill='#ffb74d'/>" % (W - 80) + text(W - 64, 14, lb, 12, anchor="start"))
    return wrap(W, H, "".join(s), "gráfico de colunas duplas", lg=True)


def s2_colunas():
    k = R.choice(["simples", "duplas", "duplas"])
    if k == "simples":
        step = R.choice([5, 10, 20, 50])
        cats = R.sample(["futebol", "vôlei", "natação", "basquete", "judô", "handebol"], 4)
        vals = [R.randint(1, 9) * step for _ in cats]
        if len(set(vals)) < 4:
            return None
        i, j = R.sample(range(4), 2)
        q = R.choice(["um", "dif", "tot"])
        pic = "<p><b>Esporte preferido dos alunos da escola</b></p>" + grafico(list(zip(cats, vals)), "alunos", step)
        if q == "um":
            return mcq(pic + "Quantos alunos preferem %s?" % cats[i], num(vals[i]), [num(x) for x in (vals[i] // step, vals[i] + step, vals[j])],
                       "Cada linha do gráfico vale %d. A coluna de %s chega a <b>%s</b>." % (step, cats[i], num(vals[i])))
        if q == "dif":
            a, b = max(vals[i], vals[j]), min(vals[i], vals[j])
            ca = cats[i] if vals[i] > vals[j] else cats[j]
            cb = cats[j] if ca == cats[i] else cats[i]
            return mcq(pic + "Quantos alunos a mais preferem %s do que %s?" % (ca, cb), num(a - b), [num(x) for x in (a + b, a, (a - b) // step)],
                       "%s − %s = <b>%s</b>." % (num(a), num(b), num(a - b)))
        return mcq(pic + "Quantos alunos responderam à pesquisa?", num(sum(vals)), [num(x) for x in (sum(vals) // step, max(vals), sum(vals) + step)],
                   "%s = <b>%s</b>." % (" + ".join(num(v) for v in vals), num(sum(vals))))
    cats = R.choice([["1º", "2º", "3º", "4º"], ["seg.", "ter.", "qua.", "qui."], ["jan.", "fev.", "mar.", "abr."]])
    step = R.choice([5, 10])
    a = [R.randint(1, 9) * step for _ in cats]
    b = [R.randint(1, 9) * step for _ in cats]
    la, lb = R.choice([("meninas", "meninos"), ("turma A", "turma B"), ("manhã", "tarde")])
    pic = colunas_duplas(cats, a, b, la, lb, step)
    i = R.randrange(len(cats))
    q = R.choice(["um", "mais", "soma"])
    if q == "um":
        return mcq(pic + "No gráfico, quanto vale a coluna de «%s» em %s?" % (la, cats[i]), num(a[i]), [num(x) for x in (b[i], a[i] + step, a[(i + 1) % 4])],
                   "A coluna azul (%s) em %s chega a <b>%s</b>." % (la, cats[i], num(a[i])))
    if q == "mais":
        if a[i] == b[i]:
            return None
        ans = la if a[i] > b[i] else lb
        return mcq(pic + "Em %s, quem teve o maior valor: %s ou %s?" % (cats[i], la, lb), ans, [lb if ans == la else la, "empataram", "não dá para saber"],
                   "Em %s: %s = %s e %s = %s. <b>%s</b>." % (cats[i], la, num(a[i]), lb, num(b[i]), ans))
    return mcq(pic + "Somando as duas colunas de %s, qual é o total?" % cats[i], num(a[i] + b[i]), [num(x) for x in (a[i], abs(a[i] - b[i]), a[i] + b[i] + step)],
               "%s + %s = <b>%s</b>." % (num(a[i]), num(b[i]), num(a[i] + b[i])))


def linhas(labels, vals, unit, step):
    mx = max(vals)
    mn = 0
    top = -(-mx // step) * step
    W, H = 70 + len(labels) * 48, 210
    y0, hgt = 180, 150
    s = []
    for k in range(mn, top + 1, step):
        y = y0 - hgt * k / top
        s.append(line(52, y, W - 10, y, "#d6dde4", 1))
        s.append(text(46, y + 4, num(k), 11, anchor="end"))
    pts = []
    for i, (l, v) in enumerate(zip(labels, vals)):
        x = 74 + i * 48
        y = y0 - hgt * v / top
        pts.append((x, y))
        s.append(text(x, y0 + 16, l, 11))
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='2.6'/>" % (" ".join("%.1f,%.1f" % p for p in pts), BLUE))
    for x, y in pts:
        s.append("<circle cx='%.1f' cy='%.1f' r='4' fill='%s'/>" % (x, y, BLUE))
    s.append(line(52, y0, W - 10, y0, INK, 2))
    s.append(text(10, 14, unit, 12, anchor="start"))
    return wrap(W, H, "".join(s), "gráfico de linhas", lg=True)


LTEMAS = [("Temperatura máxima média em Curitiba", "°C", 2, (14, 28)), ("Altura de uma planta (cm)", "cm", 5, (5, 60)),
          ("Casos de gripe atendidos no posto", "casos", 10, (20, 120)), ("Visitantes do museu (centenas)", "centenas", 2, (4, 30)),
          ("Chuva no mês (mm)", "mm", 20, (20, 260))]


def s3_linhas():
    t, u, step, (lo, hi) = R.choice(LTEMAS)
    n = R.randint(5, 6)
    start = R.randint(0, 12 - n)
    labs = MESES[start:start + n]
    if t.startswith("Altura"):
        vals = sorted(R.sample(range(lo, hi + 1, 1), n))
        labs = ["%dª sem." % (i + 1) for i in range(n)]
    else:
        vals = [R.randint(lo, hi) for _ in range(n)]
    vals = [v // step * step for v in vals]
    if len(set(vals)) < n:
        return None
    pic = "<p><b>%s</b></p>" % t + linhas(labs, vals, u, step)
    k = R.choice(["max", "min", "um", "subiu", "maior_var"])
    if k == "max":
        i = vals.index(max(vals))
        return mcq(pic + "Em que período o valor foi o maior?", labs[i], [labs[j] for j in range(n) if j != i][:3], "O ponto mais alto da linha está em <b>%s</b> (%s)." % (labs[i], num(vals[i])))
    if k == "min":
        i = vals.index(min(vals))
        return mcq(pic + "Em que período o valor foi o menor?", labs[i], [labs[j] for j in range(n) if j != i][:3], "O ponto mais baixo da linha está em <b>%s</b> (%s)." % (labs[i], num(vals[i])))
    if k == "um":
        i = R.randrange(n)
        return mcq(pic + "Qual foi o valor em %s?" % labs[i], num(vals[i]), [num(x) for x in (vals[i] + step, vals[i] - step, vals[(i + 1) % n])],
                   "Siga a linha até %s e olhe a escala: <b>%s</b>." % (labs[i], num(vals[i])))
    if k == "subiu":
        i = R.randrange(n - 1)
        up = vals[i + 1] > vals[i]
        ans = "aumentou %s" % num(abs(vals[i + 1] - vals[i])) if up else "diminuiu %s" % num(abs(vals[i + 1] - vals[i]))
        d = abs(vals[i + 1] - vals[i])
        return mcq(pic + "De %s para %s, o valor aumentou ou diminuiu? Quanto?" % (labs[i], labs[i + 1]), ans,
                   ["diminuiu %s" % num(d) if up else "aumentou %s" % num(d), ("aumentou %s" if up else "diminuiu %s") % num(d + step), "ficou igual"],
                   "%s → %s: <b>%s</b>." % (num(vals[i]), num(vals[i + 1]), ans))
    difs = [abs(vals[i + 1] - vals[i]) for i in range(n - 1)]
    if difs.count(max(difs)) > 1:
        return None
    i = difs.index(max(difs))
    ans = "de %s para %s" % (labs[i], labs[i + 1])
    w = ["de %s para %s" % (labs[j], labs[j + 1]) for j in range(n - 1) if j != i]
    R.shuffle(w)
    return mcq(pic + "Entre quais períodos seguidos houve a <b>maior variação</b> (subida ou descida)?", ans, w,
               "A linha fica mais inclinada %s: variação de %s. <b>%s</b>." % (ans, num(max(difs)), ans))


VAR = [("cor dos olhos", "categórica"), ("idade em anos", "numérica"), ("esporte preferido", "categórica"), ("altura em centímetros", "numérica"),
       ("número de irmãos", "numérica"), ("sabor de suco preferido", "categórica"), ("meio de transporte para a escola", "categórica"),
       ("massa em quilogramas", "numérica"), ("bairro onde mora", "categórica"), ("tempo gasto até a escola, em minutos", "numérica"),
       ("cor preferida", "categórica"), ("quantidade de livros lidos no ano", "numérica")]
GRAF = [("Para mostrar como a temperatura mudou ao longo dos meses, o melhor é…", "um gráfico de linhas", ["um gráfico de colunas", "uma lista de nomes", "um pictograma"]),
        ("Para comparar o esporte preferido de meninas e meninos, o melhor é…", "um gráfico de colunas duplas", ["um gráfico de linhas", "um relógio", "uma reta numérica"]),
        ("Para mostrar o crescimento de uma planta semana a semana, o melhor é…", "um gráfico de linhas", ["um gráfico de colunas duplas", "uma tabela de preços", "um mapa"]),
        ("Para mostrar quantos alunos preferem cada fruta, um bom gráfico é…", "um gráfico de colunas", ["um gráfico de linhas", "um termômetro", "uma régua"]),
        ("Num pictograma, cada figura vale 10 alunos. Quatro figuras e meia valem…", "45 alunos", ["4 alunos", "40 alunos", "410 alunos"]),
        ("Num pictograma, cada figura vale 5 votos. Seis figuras valem…", "30 votos", ["6 votos", "11 votos", "56 votos"])]


def s4_variavel():
    if R.random() < 0.55:
        v, t = R.choice(VAR)
        return mcq("Numa pesquisa, perguntamos a «%s». Essa variável é…" % v, t, ["numérica" if t == "categórica" else "categórica", "as duas ao mesmo tempo", "não é uma variável"],
                   "Variável numérica tem respostas em números (que podem ser medidas ou contadas); categórica tem respostas em palavras ou categorias. <b>%s</b>." % t)
    q, a, w = R.choice(GRAF)
    return mcq(q, a, w, "Gráfico de linhas mostra mudanças no tempo; gráfico de colunas compara quantidades. Resposta: <b>%s</b>." % a)


def s4_conclusao():
    t, rows, cols, v, tb = dupla()
    tots = [sum(r[j] for r in v) for j in range(len(cols))]
    if tots[0] == tots[1]:
        return None
    big = cols[0] if tots[0] > tots[1] else cols[1]
    small = cols[1] if big == cols[0] else cols[0]
    good = "No total, houve mais «%s» (%s) do que «%s» (%s)." % (big, num(max(tots)), small, num(min(tots)))
    w = ["No total, houve mais «%s» (%s) do que «%s» (%s)." % (small, num(max(tots)), big, num(min(tots))),
         "Em todas as linhas houve o mesmo número de «%s»." % cols[0], "A tabela não permite comparar «%s» e «%s»." % (cols[0], cols[1])]
    return mcq(tb + "Qual frase resume corretamente a tabela?", good, w,
               "Some cada coluna: «%s» = %s e «%s» = %s. <b>%s</b>" % (cols[0], num(tots[0]), cols[1], num(tots[1]), good))


def s5_problema():
    k = R.choice(["transito", "saude", "lixo", "pesquisa", "escala"])
    if k == "transito":
        a, b, c = R.randint(20, 90), R.randint(20, 90), R.randint(20, 90)
        tb = table(["Infração", "Multas no mês"], [["excesso de velocidade", str(a)], ["avanço do sinal vermelho", str(b)], ["estacionamento proibido", str(c)]])
        tot = a + b + c
        return mcq("<p><b>Multas de trânsito numa avenida</b></p>" + tb + "Quantas multas foram aplicadas ao todo?", str(tot), [str(x) for x in (tot - c, max(a, b, c), tot + 10)],
                   "%d + %d + %d = <b>%d</b>." % (a, b, c, tot))
    if k == "saude":
        m = R.sample(MESES[:6], 3)
        v = [R.randint(30, 150) for _ in m]
        if len(set(v)) < 3:
            return None
        tb = table(["Mês", "Crianças vacinadas"], [[x, str(y)] for x, y in zip(m, v)])
        i = v.index(max(v))
        return mcq("<p><b>Campanha de vacinação</b></p>" + tb + "Em que mês foram vacinadas mais crianças?", m[i], [x for x in m if x != m[i]] + ["em todos foi igual"],
                   "O maior número é %d: <b>%s</b>." % (max(v), m[i]))
    if k == "lixo":
        a, b = R.randint(100, 400), R.randint(100, 400)
        if a == b:
            return None
        tb = table(["Material", "kg recolhidos"], [["papel", num(a)], ["plástico", num(b)]])
        return mcq("<p><b>Coleta seletiva da escola</b></p>" + tb + "Quantos quilos de papel a mais (ou a menos) que de plástico foram recolhidos?",
                   ("%s kg a mais" if a > b else "%s kg a menos") % num(abs(a - b)), [("%s kg a menos" if a > b else "%s kg a mais") % num(abs(a - b)), "%s kg a mais" % num(a + b), "a mesma quantidade"],
                   "%s − %s = %s: <b>%s kg a %s</b>." % (num(max(a, b)), num(min(a, b)), num(abs(a - b)), num(abs(a - b)), "mais" if a > b else "menos"))
    if k == "pesquisa":
        n = R.choice([20, 25, 30, 40])
        a = R.randint(n // 4, n // 2)
        b = R.randint(2, n - a - 2)
        c = n - a - b
        return mcq("Numa pesquisa com %d alunos, %d preferem praia, %d preferem campo e o resto prefere cidade. Quantos preferem cidade?" % (n, a, b), str(c), [str(x) for x in (a + b, n - a, n - b)],
                   "%d − %d − %d = <b>%d</b>." % (n, a, b, c))
    step = R.choice([10, 20, 50, 100])
    k2 = R.randint(3, 9)
    return mcq("Num gráfico de colunas, cada linha da escala vale %d. Uma coluna chega à %dª linha. Que valor ela representa?" % (step, k2), num(step * k2), [num(x) for x in (k2, step + k2, step * (k2 + 1))],
               "%d × %d = <b>%s</b>." % (k2, step, num(step * k2)))


def main():
    seen = set()
    sets = [
        ("Tabelas de dupla entrada", mix(R, seen, [(s1_dupla, 20)])),
        ("Gráficos de colunas", mix(R, seen, [(s2_colunas, 20)])),
        ("Gráficos de linhas", mix(R, seen, [(s3_linhas, 20)])),
        ("Pesquisa e conclusões", mix(R, seen, [(s4_variavel, 12), (s4_conclusao, 8)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Numa <b>tabela de dupla entrada</b>, cruze a linha com a coluna para achar o dado.",
         "No <b>gráfico de colunas</b>, olhe a escala: cada linha pode valer 1, 5, 10 ou mais.",
         "O <b>gráfico de linhas</b> mostra como um valor muda com o tempo: a linha sobe quando aumenta e desce quando diminui.",
         "Numa pesquisa, a variável é <b>categórica</b> (cor, esporte) ou <b>numérica</b> (idade, altura).",
         "Para concluir, compare os dados e escreva uma frase curta que resuma o resultado."],
        [("Num gráfico de linhas, a temperatura foi de 18 °C em março para 24 °C em abril.", ["a linha sobe", "24 − 18 = 6"], "aumentou 6 °C"),
         ("Numa tabela, meninas: 12 e 15; meninos: 10 e 9. Quem é a maioria?", ["meninas: 12 + 15 = 27", "meninos: 10 + 9 = 19"], "as meninas")],
        [["Ler a coluna errada", "Ponha o dedo na linha e na coluna antes de ler."],
         ["Não ver a escala", "Se cada linha vale 10, uma coluna na 4ª linha vale 40."],
         ["Confundir o maior valor com o maior aumento", "O maior aumento é onde a linha fica mais inclinada."]],
        linhas(["mar.", "abr.", "maio", "jun.", "jul."], [24, 22, 18, 16, 16], "°C", 2))
    faq = [("Que gráficos o 5º ano estuda?", "A BNCC pede interpretar e construir tabelas, gráficos de colunas (simples e agrupadas), pictóricos e de linhas, e escrever um texto que resuma as conclusões."),
           ("Qual é a diferença entre variável categórica e numérica?", "Categórica tem respostas em categorias (cor preferida, esporte); numérica tem respostas em números que contam ou medem (idade, altura, número de irmãos).")]
    make_unit(R, "tabelas-e-graficos", "E", ["EF05MA24", "EF05MA25"],
              "Interpretar dados estatísticos apresentados em textos, tabelas e gráficos (colunas ou linhas), referentes a outras áreas do conhecimento ou a outros contextos, como saúde e trânsito, e produzir textos com o objetivo de sintetizar conclusões; realizar pesquisa envolvendo variáveis categóricas e numéricas, organizar dados coletados por meio de tabelas, gráficos de colunas, pictóricos e de linhas, e apresentar texto escrito sobre a finalidade da pesquisa e a síntese dos resultados",
              "Tabelas e gráficos de colunas e de linhas", "Tabelas e gráficos",
              "Atividades de matemática para o 5º ano sobre tabelas e gráficos: tabelas de dupla entrada, gráficos de colunas simples e duplas, gráficos de linhas, variáveis de pesquisa e conclusões. 100 exercícios com gabarito.",
              "Olhe a escala antes de ler o gráfico.", "Gráfico de linhas: mudanças ao longo do tempo.",
              body, faq, sets, 22, grade="5-ano")


if __name__ == "__main__":
    main()
