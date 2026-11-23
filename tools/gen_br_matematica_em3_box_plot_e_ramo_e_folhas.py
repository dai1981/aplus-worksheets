# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 3ª série: Histograma, box-plot e ramo-e-folhas (EM13MAT407)
  python3 tools/gen_br_matematica_em3_box_plot_e_ramo_e_folhas.py
Quartis (Q1, mediana, Q3) e amplitude interquartil; ler e comparar box-plots; diagrama de ramo-e-folhas (moda, mediana, amplitude);
histogramas. Quartis pelo método das medianas das metades.
Usa geradores do 8º ano (histograma) com outro sorteio.
Erros: calcular quartis sem ordenar, achar que a caixa maior tem mais dados, ler a folha sem o ramo.
"""
import random
from fractions import Fraction as F
from br_em import M, d, bank, mix, lesson, use, unit, tab, _svg, _t, _ln, INK, BLUE

R = random.Random(93005)
c_histo = use("gen_br_matematica_8_graficos_e_classes_de_frequencia", 93903, "s3_histo")


def med(xs):
    n = len(xs)
    return F(xs[n // 2]) if n % 2 else F(xs[n // 2 - 1] + xs[n // 2], 2)


def quartis(xs):
    xs = sorted(xs)
    n = len(xs)
    lo, hi = xs[:n // 2], xs[(n + 1) // 2:]
    return med(lo), med(xs), med(hi)


def boxes(items, lo, hi, step, label):
    """items: [(nome, (min, q1, md, q3, max))]"""
    W = 400
    H = 50 + 60 * len(items)
    x0, x1 = 70, W - 20
    X = lambda v: x0 + (float(v) - lo) / (hi - lo) * (x1 - x0)
    s = []
    yb = H - 26
    s.append(_ln(x0, yb, x1, yb))
    v = lo
    while v <= hi:
        s.append(_ln(X(v), yb, X(v), yb + 5) + _t(X(v), yb + 19, d(v), 12, INK, bold=False))
        v += step
    for i, (nm, (a, q1, m, q3, b)) in enumerate(items):
        y = 30 + 60 * i
        s.append(_t(x0 - 8, y + 5, nm, 13, INK, anchor="end"))
        s.append(_ln(X(a), y, X(q1), y) + _ln(X(q3), y, X(b), y))
        s.append(_ln(X(a), y - 8, X(a), y + 8) + _ln(X(b), y - 8, X(b), y + 8))
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='26' fill='#dfe9f7' stroke='%s' stroke-width='2'/>" % (X(q1), y - 13, X(q3) - X(q1), BLUE))
        s.append(_ln(X(m), y - 13, X(m), y + 13, BLUE, 3))
    return _svg(W, H, "".join(s), label)


def s1_quartis():
    n = R.choice([7, 8, 9, 10, 11])
    xs = [R.randint(1, 40) for _ in range(n)]
    if len(set(xs)) < n - 1:
        return None
    q1, m, q3 = quartis(xs)
    k = R.choice(["q1", "q3", "aiq", "md"])
    lst = "; ".join(map(str, xs))
    if k == "q1":
        return M("Dados: %s. Qual é o primeiro quartil (Q1)?" % lst, d(q1), [d(m), d(q3), d(F(sorted(xs)[n // 4]))], "Em ordem: %s. Q1 é a mediana da metade de baixo: <b>%s</b>." % ("; ".join(map(str, sorted(xs))), d(q1)))
    if k == "q3":
        return M("Dados: %s. Qual é o terceiro quartil (Q3)?" % lst, d(q3), [d(m), d(q1), d(max(xs))], "Em ordem: %s. Q3 é a mediana da metade de cima: <b>%s</b>." % ("; ".join(map(str, sorted(xs))), d(q3)))
    if k == "md":
        return M("Dados: %s. Qual é a mediana (Q2)?" % lst, d(m), [d(F(xs[n // 2])), d(F(sum(xs), n), 1), d(q3)], "Em ordem: %s. O valor do meio é <b>%s</b>." % ("; ".join(map(str, sorted(xs))), d(m)))
    return M("Dados: %s. Qual é a amplitude interquartil (Q3 − Q1)?" % lst, d(q3 - q1), [d(max(xs) - min(xs)), d(q3), d(m - q1)], "Q1 = %s e Q3 = %s: <b>%s</b>." % (d(q1), d(q3), d(q3 - q1)))


def five():
    a = R.randint(0, 20)
    q1 = a + R.randint(2, 15)
    m = q1 + R.randint(1, 12)
    q3 = m + R.randint(1, 12)
    b = q3 + R.randint(2, 20)
    return a, q1, m, q3, b


def s2_boxplot():
    a, q1, m, q3, b = five()
    lo, hi = (a // 10) * 10, ((b + 9) // 10) * 10
    step = 10 if hi - lo <= 80 else 20
    g = boxes([("Notas", (a, q1, m, q3, b))], lo, hi, step, "box-plot das notas de uma turma")
    k = R.choice(["md", "q1", "q3", "amp", "aiq", "pct"])
    pre = g + "O box-plot mostra as notas de uma turma (de 0 a 100). "
    if k == "md":
        return M(pre + "Qual é a mediana?", d(m), [d(q1), d(q3), d(F(a + b, 2))], "A linha dentro da caixa é a mediana: <b>%s</b>." % d(m))
    if k == "q1":
        return M(pre + "Qual é o primeiro quartil?", d(q1), [d(a), d(m), d(q3)], "Q1 é o começo da caixa: <b>%s</b>." % d(q1))
    if k == "q3":
        return M(pre + "Qual é o terceiro quartil?", d(q3), [d(b), d(m), d(q1)], "Q3 é o fim da caixa: <b>%s</b>." % d(q3))
    if k == "amp":
        return M(pre + "Qual é a amplitude total?", d(b - a), [d(q3 - q1), d(b), d(m - a)], "Máximo − mínimo = %s − %s = <b>%s</b>." % (d(b), d(a), d(b - a)))
    if k == "aiq":
        return M(pre + "Qual é a amplitude interquartil?", d(q3 - q1), [d(b - a), d(m - q1), d(q3)], "Q3 − Q1 = %s − %s = <b>%s</b>." % (d(q3), d(q1), d(q3 - q1)))
    return M(pre + "Aproximadamente que porcentagem dos alunos tirou nota entre %s e %s?" % (d(q1), d(q3)), "50%", ["25%", "75%", "100%"], "Entre Q1 e Q3 (a caixa) ficam <b>cerca de 50%</b> dos dados.")


def s3_comparar():
    A = five()
    B = five()
    if A[2] == B[2] or (A[3] - A[1]) == (B[3] - B[1]):
        return None
    lo = min(A[0], B[0]) // 10 * 10
    hi = (max(A[4], B[4]) + 9) // 10 * 10
    g = boxes([("Turma A", A), ("Turma B", B)], lo, hi, 10 if hi - lo <= 80 else 20, "box-plots das notas das turmas A e B")
    k = R.choice(["md", "disp", "maior"])
    if k == "md":
        ans = "Turma A" if A[2] > B[2] else "Turma B"
        return M(g + "Qual turma tem a maior mediana?", ans, ["Turma B" if ans == "Turma A" else "Turma A", "as duas iguais", "não dá para saber"], "Compare as linhas dentro das caixas: <b>%s</b>." % ans)
    if k == "disp":
        ans = "Turma A" if (A[3] - A[1]) < (B[3] - B[1]) else "Turma B"
        return M(g + "Qual turma tem as notas centrais menos dispersas (menor amplitude interquartil)?", ans, ["Turma B" if ans == "Turma A" else "Turma A", "as duas iguais", "a que tem a maior nota"], "Caixa mais estreita: <b>%s</b>." % ans)
    ans = "Turma A" if A[4] > B[4] else ("Turma B" if B[4] > A[4] else None)
    if not ans:
        return None
    return M(g + "Qual turma teve a maior nota?", ans, ["Turma B" if ans == "Turma A" else "Turma A", "as duas iguais", "a de maior mediana"], "O fim da linha da direita mostra o máximo: <b>%s</b>." % ans)


def s4_ramo():
    stems = sorted(R.sample(range(1, 9), 3))
    data = {s_: sorted(R.choice(range(10)) for _ in range(R.randint(2, 5))) for s_ in stems}
    rows = [["Ramo", "Folhas"]] + [[str(s_), " ".join(map(str, data[s_]))] for s_ in stems]
    xs = sorted(10 * s_ + f for s_ in stems for f in data[s_])
    k = R.choice(["n", "max", "min", "md", "moda", "amp"])
    t = tab(rows) + "<p>Legenda: 2 | 5 = 25</p>"
    if k == "n":
        return M(t + "Quantos dados há no diagrama de ramo-e-folhas?", str(len(xs)), [str(len(stems)), str(len(xs) + 1), str(sum(xs) // len(xs))], "Conte as folhas: <b>%d</b>." % len(xs))
    if k == "max":
        return M(t + "Qual é o maior valor?", str(xs[-1]), [str(xs[-1] % 10), str(stems[-1]), str(xs[-2]) if xs[-2] != xs[-1] else str(xs[-1] + 1)], "Último ramo e última folha: <b>%d</b>." % xs[-1])
    if k == "min":
        return M(t + "Qual é o menor valor?", str(xs[0]), [str(xs[0] % 10) if xs[0] % 10 != xs[0] else str(xs[0] + 10), str(stems[0]), str(xs[1]) if xs[1] != xs[0] else str(xs[0] + 1)], "Primeiro ramo e primeira folha: <b>%d</b>." % xs[0])
    if k == "md":
        return M(t + "Qual é a mediana?", d(med(xs)), [d(F(sum(xs), len(xs)), 1), str(xs[len(xs) // 2 - 1]) if len(xs) % 2 else str(xs[len(xs) // 2 + 1]), str(10 * stems[1] + 5)], "Os dados já estão em ordem; o meio dá <b>%s</b>." % d(med(xs)))
    if k == "moda":
        from collections import Counter
        c = Counter(xs).most_common()
        if len(c) > 1 and c[0][1] == c[1][1] or c[0][1] == 1:
            return None
        return M(t + "Qual é a moda?", str(c[0][0]), [str(c[0][0] % 10), str(xs[-1]), str(c[1][0]) if len(c) > 1 else str(c[0][0] + 1)], "O valor que mais se repete: <b>%d</b>." % c[0][0])
    return M(t + "Qual é a amplitude dos dados?", str(xs[-1] - xs[0]), [str(stems[-1] - stems[0]), str(xs[-1]), str(xs[-1] - xs[1]) if xs[1] != xs[0] else str(xs[-1] - xs[0] + 1)], "%d − %d = <b>%d</b>." % (xs[-1], xs[0], xs[-1] - xs[0]))


def main():
    seen = set()
    sets = [
        ("Quartis", mix(R, seen, [(s1_quartis, 20)])),
        ("Ler box-plots", mix(R, seen, [(s2_boxplot, 20)])),
        ("Comparar box-plots", mix(R, seen, [(s3_comparar, 20)])),
        ("Ramo-e-folhas", mix(R, seen, [(s4_ramo, 20)])),
        ("Histogramas e revisão", mix(R, seen, [(c_histo, 10), (s2_boxplot, 5), (s1_quartis, 5)])),
    ]
    body = lesson(
        ["Com os dados em ordem, a <b>mediana</b> (Q2) divide-os ao meio; o <b>1º quartil</b> (Q1) é a mediana da metade de baixo e o <b>3º quartil</b> (Q3), a da metade de cima.",
         "O <b>box-plot</b> mostra mínimo, Q1, mediana, Q3 e máximo. A caixa contém cerca de 50% dos dados; a <b>amplitude interquartil</b> é Q3 − Q1.",
         "No <b>ramo-e-folhas</b>, o ramo são as dezenas e as folhas, as unidades: 3 | 2 5 7 significa 32, 35 e 37.",
         "Para comparar grupos, olhe as medianas (centro) e o tamanho das caixas (dispersão)."],
        [("Dados 3; 5; 7; 8; 10; 12; 15; 18", ["metade de baixo 3, 5, 7, 8: Q1 = 6", "mediana (8 + 10) ÷ 2 = 9", "metade de cima 10, 12, 15, 18: Q3 = 13,5"], "Q1 = 6, Q2 = 9, Q3 = 13,5")],
        [["Calcular quartis sem ordenar", "Ordene os dados primeiro."],
         ["Achar que a caixa maior tem mais dados", "Toda caixa tem cerca de 50% dos dados; maior só indica mais dispersão."],
         ["Ler a folha sozinha", "Junte ramo e folha: 4 | 7 = 47."]],
        boxes([("Exemplo", (3, 6, 9, F(27, 2), 18))], 0, 20, 5, "box-plot do exemplo"))
    faq = [("O que mostra um box-plot?", "Mostra cinco números: mínimo, primeiro quartil, mediana, terceiro quartil e máximo. A caixa vai de Q1 a Q3 e contém cerca de metade dos dados."),
           ("O que a BNCC pede?", "Interpretar e comparar conjuntos de dados estatísticos por meio de diferentes diagramas e gráficos (histograma, box-plot, ramo-e-folhas, entre outros), reconhecendo os mais eficientes para sua análise (EM13MAT407).")]
    unit(R, "histograma-box-plot-e-ramo-e-folhas", "E", ["EM13MAT407"],
         "Interpretar e comparar conjuntos de dados estatísticos por meio de diferentes diagramas e gráficos (histograma, box-plot, ramo-e-folhas, entre outros), reconhecendo os mais eficientes para sua análise",
         "Histograma, box-plot e ramo-e-folhas", "Box-plot e ramo-e-folhas",
         "Atividades de matemática para a 3ª série do Ensino Médio sobre estatística: quartis, amplitude interquartil, leitura e comparação de box-plots, diagrama de ramo-e-folhas e histogramas. 100 exercícios com gabarito.",
         "Box-plot: mínimo, Q1, mediana, Q3, máximo", "A caixa tem cerca de 50% dos dados.",
         body, faq, sets, 5, grade="3-serie")


if __name__ == "__main__":
    main()
