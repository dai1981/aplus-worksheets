# -*- coding: utf-8 -*-
"""
Brasil Matemática 4º ano: Tabelas e gráficos (Probabilidade e estatística, EF04MA27, EF04MA28)
  python3 tools/gen_br_matematica_4_tabelas_e_graficos.py
Tabelas simples e de dupla entrada; gráficos de colunas simples e agrupadas; pictogramas com legenda (cada figura vale 2, 5 ou 10);
pesquisas com variáveis categóricas e numéricas; frases que resumem os dados. Usa geradores do 3º e do 5º ano com outro sorteio.
Erros: ler a coluna errada, esquecer a escala ou a legenda (cada figura vale 5), contar meia figura como inteira.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, wrap, text, INK, use, lim

R = random.Random(80422)
T3 = "gen_br_matematica_3_tabelas_e_graficos"
T5 = "gen_br_matematica_5_tabelas_e_graficos"
L = (lim(99999, 0),)


def sem_linhas(it):
    t = it["q"] + "".join(it["c"])
    return "gráfico de linhas" not in t and "gráficos de linhas" not in t and "aria-label='gráfico de linhas'" not in t


a_tab, a_graf, a_pesq, a_prob = use(T3, 80968, "s1_tabela", "s2_grafico", "s4_pesquisa", "s5_problema")
b_dupla, b_col, b_var, b_conc, b_prob = use(T5, 80969, "s1_dupla", "s2_colunas", "s4_variavel", "s4_conclusao", "s5_problema", preds=L + (sem_linhas,))
_ID = [0]
COR = ["#64b5f6", "#ffb74d", "#81c784", "#e57373", "#ba68c8"]


def icon(x, y, col, half=False):
    pts = []
    import math
    for i in range(10):
        r = 10 if i % 2 == 0 else 4.2
        a = -math.pi / 2 + math.pi * i / 5
        pts.append((x + r * math.cos(a), y + r * math.sin(a)))
    star = "<polygon points='%s' fill='%s' stroke='%s' stroke-width='0.8'/>" % (" ".join("%.1f,%.1f" % p for p in pts), col, INK)
    if half:
        _ID[0] += 1
        k = "bm4h%d" % _ID[0]
        return "<g><clipPath id='%s'><rect x='%d' y='%d' width='10' height='22'/></clipPath><g clip-path='url(#%s)'>%s</g></g>" % (k, x - 10, y - 11, k, star)
    return star


def pictograma(cats, vals, per, titulo):
    rowh = 30
    s = [text(10, 18, titulo, 13, anchor="start")]
    for i, (c, v) in enumerate(zip(cats, vals)):
        y = 44 + i * rowh
        s.append(text(10, y + 5, c, 13, anchor="start"))
        n, half = divmod(v, per)
        for j in range(n):
            s.append(icon(110 + j * 24, y, COR[i % 5]))
        if half:
            s.append(icon(110 + n * 24, y, COR[i % 5], True))
    yk = 44 + len(cats) * rowh
    s.append(icon(20, yk, "#9e9e9e") + text(36, yk + 5, "= %d votos" % per, 13, anchor="start"))
    W = 110 + (max(vals) // per + 1) * 24 + 20
    return wrap(max(W, 260), yk + 20, "".join(s), "pictograma: cada estrela vale %d votos" % per, lg=True)


def s3_picto():
    per = R.choice([2, 4, 10])
    cats = R.sample(["banana", "maçã", "uva", "manga", "laranja", "abacaxi", "caju", "goiaba"], 4)
    vals = [per * R.randint(1, 7) + (per // 2 if R.random() < 0.4 else 0) for _ in cats]
    if len(set(vals)) < 4:
        return None
    pic = pictograma(cats, vals, per, "Fruta preferida da turma")
    k = R.choice(["um", "mais", "dif", "tot"])
    i, j = R.sample(range(4), 2)
    if k == "um":
        return mcq(pic + "Quantos votos teve a fruta %s?" % cats[i], str(vals[i]), [str(x) for x in (vals[i] // per, vals[i] + per, vals[i] - per // 2 if vals[i] % per else vals[i] + per // 2)],
                   "Cada estrela vale %d (meia estrela vale %d). %s tem <b>%d votos</b>." % (per, per // 2, cats[i].capitalize(), vals[i]))
    if k == "mais":
        m = vals.index(max(vals))
        return mcq(pic + "Qual fruta teve mais votos?", cats[m], [c for x, c in enumerate(cats) if x != m], "A linha com mais estrelas é a da fruta <b>%s</b> (%d votos)." % (cats[m], vals[m]))
    if k == "dif":
        a, b = max(vals[i], vals[j]), min(vals[i], vals[j])
        return mcq(pic + "Quantos votos a mais teve %s do que %s?" % (cats[i] if vals[i] > vals[j] else cats[j], cats[j] if vals[i] > vals[j] else cats[i]), str(a - b),
                   [str(x) for x in ((a - b) // per if (a - b) // per != a - b else a - b + per, a + b, a - b + per)], "%d − %d = <b>%d</b>." % (a, b, a - b))
    t = sum(vals)
    return mcq(pic + "Quantos alunos votaram ao todo?", str(t), [str(x) for x in (t // per, t + per, t - per)], "%s = <b>%d</b>." % (" + ".join(map(str, vals)), t))


def main():
    seen = set()
    sets = [
        ("Tabelas simples e de dupla entrada", mix(R, seen, [(a_tab, 6), (b_dupla, 14)])),
        ("Gráficos de colunas", mix(R, seen, [(a_graf, 8), (b_col, 12)])),
        ("Pictogramas", mix(R, seen, [(s3_picto, 20)])),
        ("Pesquisas e conclusões", mix(R, seen, [(a_pesq, 8), (b_var, 6), (b_conc, 6)])),
        ("Problemas", mix(R, seen, [(a_prob, 10), (b_prob, 10)])),
    ]
    body = lesson(
        ["Numa <b>tabela de dupla entrada</b>, cruze a linha com a coluna para achar o dado.",
         "No <b>gráfico de colunas</b>, olhe a escala: cada linha pode valer 1, 5, 10…",
         "No <b>pictograma</b>, leia a legenda: se cada figura vale 4, meia figura vale 2.",
         "Numa pesquisa, a variável é <b>categórica</b> (fruta, cor, esporte) ou <b>numérica</b> (idade, altura, número de irmãos).",
         "Depois de ler os dados, escreva uma frase curta que resuma o que você descobriu."],
        [("Pictograma: cada estrela = 4 votos. Manga tem 3 estrelas e meia.", ["3 × 4 = 12", "meia estrela = 2"], "14 votos"),
         ("Tabela: meninas 12 e 15; meninos 10 e 9. Quem é a maioria?", ["meninas: 27", "meninos: 19"], "as meninas")],
        [["Ler a coluna errada", "Ponha o dedo na linha e na coluna antes de ler."],
         ["Esquecer a legenda do pictograma", "Multiplique o número de figuras pelo valor de cada uma."],
         ["Contar meia figura como inteira", "Meia figura vale a metade da legenda."]],
        pictograma(["banana", "uva", "manga"], [12, 8, 14], 4, "Fruta preferida da turma"))
    faq = [("Que gráficos o 4º ano estuda?", "A BNCC pede analisar tabelas simples e de dupla entrada, gráficos de colunas (simples ou agrupadas) e pictóricos, fazer pesquisas e escrever uma síntese dos resultados."),
           ("O que é um pictograma?", "É um gráfico com figuras. A legenda diz quanto vale cada figura: se uma estrela vale 5 votos, três estrelas valem 15.")]
    make_unit(R, "tabelas-e-graficos", "E", ["EF04MA27", "EF04MA28"],
              "Analisar dados apresentados em tabelas simples ou de dupla entrada e em gráficos de colunas ou pictóricos, com base em informações das diferentes áreas do conhecimento, e produzir texto com a síntese de sua análise; realizar pesquisa envolvendo variáveis categóricas e numéricas e organizar dados coletados por meio de tabelas e gráficos de colunas simples ou agrupadas, com e sem uso de tecnologias digitais",
              "Tabelas, gráficos de colunas e pictogramas", "Tabelas e gráficos",
              "Atividades de matemática para o 4º ano sobre tabelas e gráficos: tabelas de dupla entrada, gráficos de colunas simples e agrupadas, pictogramas com legenda e pesquisas. 100 exercícios com gabarito.",
              "Leia a escala ou a legenda antes de ler o gráfico.", "Cruze a linha com a coluna na tabela de dupla entrada.",
              body, faq, sets, 22, grade="4-ano")


if __name__ == "__main__":
    main()
