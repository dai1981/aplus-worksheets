# -*- coding: utf-8 -*-
"""
Brasil Matemática 7º ano: Gráficos de setores e pesquisa amostral (Probabilidade e estatística, EF07MA36, EF07MA37)
  python3 tools/gen_br_matematica_7_graficos_de_setores_e_pesquisa.py
Gráfico de setores: porcentagem ↔ graus (100% = 360°), ler e construir; quando usar setores; população e amostra; planejar
uma pesquisa amostral e organizar os dados.
Usa geradores do 9º ano (pesquisa amostral) com outro sorteio.
Erros: usar 100° em vez de 360°, achar que setores servem para mostrar evolução no tempo, confundir população e amostra.
"""
import math
import random
from fractions import Fraction as F
from br_common import lesson, mix, use
from br_9 import M, d, bank, unit, _svg, _t, INK

R = random.Random(87020)
p_pop, p_vies, p_tipos = use("gen_br_matematica_9_pesquisa_amostral", 87920, "s1_pop_amostra", "s2_vies", "s3_tipos")
COLS = ["#7fa9da", "#f2b66d", "#9fd3a6", "#e59aa8", "#c3b1e1"]
ESP = ["futebol", "vôlei", "basquete", "natação", "handebol", "ciclismo"]


def pizza(parts):
    """parts: [(nome, porcentagem)]"""
    cx, cy, r = 110, 110, 90
    s = []
    a0 = 90.0
    for i, (nm, p) in enumerate(parts):
        a1 = a0 - 360.0 * p / 100
        x0, y0 = cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0))
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
        big = 1 if p > 50 else 0
        s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z' fill='%s' stroke='white' stroke-width='2'/>" % (cx, cy, x0, y0, r, r, big, x1, y1, COLS[i]))
        mid = math.radians((a0 + a1) / 2)
        s.append(_t(cx + r * 0.62 * math.cos(mid), cy - r * 0.62 * math.sin(mid) + 5, "%d%%" % p, 13, INK))
        a0 = a1
    for i, (nm, p) in enumerate(parts):
        s.append("<rect x='225' y='%d' width='14' height='14' fill='%s'/>" % (30 + i * 24, COLS[i]))
        s.append(_t(245, 42 + i * 24, nm, 14, INK, bold=False, anchor="start"))
    return _svg(360, 220, "".join(s), "gráfico de setores")


def parts4():
    while True:
        ps = [R.choice([5, 10, 15, 20, 25, 30, 35, 40, 45]) for _ in range(3)]
        last = 100 - sum(ps)
        if last >= 5 and len(set(ps + [last])) == 4:
            return list(zip(R.sample(ESP, 4), ps + [last]))


def s1_graus():
    p = R.choice([5, 10, 15, 20, 25, 30, 40, 45, 50, 60, 75, 80])
    k = R.choice(["pg", "gp"])
    if k == "pg":
        return M("Num gráfico de setores, quantos graus tem o setor de %d%%?" % p, "%s°" % d(F(p * 360, 100)), ["%d°" % p, "%s°" % d(F(p * 180, 100)), "%s°" % d(F(p * 360, 100) + 10)],
                 "100%% = 360°; %d%% de 360 = <b>%s°</b>." % (p, d(F(p * 360, 100))))
    g = F(p * 360, 100)
    return M("Num gráfico de setores, um setor tem %s°. Que porcentagem ele representa?" % d(g), "%d%%" % p, ["%s%%" % d(g), "%s%%" % d(F(p, 2)) if p % 2 == 0 else "%d%%" % (p + 5), "%s%%" % d(g * 100 / 180, 1) if (g * 100 / 180 * 10).denominator == 1 else "%d%%" % (2 * p)],
             "%s ÷ 360 = %s = <b>%d%%</b>." % (d(g), d(F(p, 100)), p))


def s2_ler():
    parts = parts4()
    tot = R.choice([40, 60, 80, 120, 200, 400])
    i = R.randrange(4)
    nm, p = parts[i]
    v = F(p * tot, 100)
    if v.denominator != 1:
        return None
    k = R.choice(["qtd", "maior", "graus"])
    pic = pizza(parts)
    if k == "qtd":
        return M(pic + "O gráfico mostra o esporte preferido de %d alunos. Quantos preferem %s?" % (tot, nm), d(v), [d(p), d(F((100 - p) * tot, 100)), d(F(p * tot, 10)) if (F(p * tot, 10)).denominator == 1 else d(v + 2)],
                 "%d%% de %d = <b>%s</b>." % (p, tot, d(v)))
    if k == "maior":
        big = max(parts, key=lambda t: t[1])
        return M(pic + "Qual é o esporte preferido pela maioria?", big[0], [x for x, _ in parts if x != big[0]], "O maior setor é <b>%s</b> (%d%%)." % big)
    return M(pic + "Quantos graus tem o setor de %s?" % nm, "%s°" % d(F(p * 360, 100)), ["%d°" % p, "%s°" % d(F(p * 360, 100) + 18), "%s°" % d(F(p * 180, 100))], "%d%% de 360° = <b>%s°</b>." % (p, d(F(p * 360, 100))))


s3_conceitos = bank(R, [
    ("O gráfico de setores é mais adequado para mostrar…", "as partes de um todo", ["a evolução no tempo", "dados de dois grupos ao longo dos meses", "uma única medida"]),
    ("A soma das porcentagens de um gráfico de setores deve ser…", "100%", ["360%", "50%", "qualquer valor"]),
    ("A soma dos ângulos dos setores é…", "360°", ["100°", "180°", "90°"]),
    ("Um setor de 90° representa…", "25% do total", ["90% do total", "50% do total", "10% do total"]),
    ("Um setor de 180° representa…", "metade do total", ["um quarto", "o total", "180% do total"]),
    ("Para construir o setor de 20%, abrimos o transferidor em…", "72°", ["20°", "36°", "200°"]),
], "s3_conceitos")


def main():
    seen = set()
    sets = [
        ("Porcentagem e graus", mix(R, seen, [(s1_graus, 20)])),
        ("Ler gráficos de setores", mix(R, seen, [(s2_ler, 20)])),
        ("Setores: quando usar", mix(R, seen, [(s3_conceitos, 6), (s2_ler, 14)])),
        ("População e amostra", mix(R, seen, [(p_pop, 12), (p_vies, 8)])),
        ("Planejar a pesquisa", mix(R, seen, [(p_tipos, 20)])),
    ]
    body = lesson(
        ["No <b>gráfico de setores</b>, o círculo inteiro (360°) representa o total (100%). Cada 1% vale 3,6°.",
         "Para achar os graus de um setor: porcentagem × 3,6 (ou fração × 360°). Para achar a quantidade: porcentagem × total.",
         "Numa <b>pesquisa amostral</b>, escolhemos uma parte da população (a amostra) que represente bem o todo, de preferência por sorteio."],
        [("Setor de 35%", ["35 × 3,6"], "126°"),
         ("25% de 120 alunos", ["120 ÷ 4"], "30 alunos")],
        [["Usar 100° no lugar de 360°", "O círculo todo tem 360°."],
         ["Usar setores para evolução no tempo", "Para o tempo, use gráfico de linhas."],
         ["Confundir população e amostra", "A amostra é a parte pesquisada."]],
        pizza([("futebol", 40), ("vôlei", 25), ("natação", 20), ("basquete", 15)]))
    faq = [("Como fazer um gráfico de setores?", "Calcule a porcentagem de cada categoria, multiplique por 3,6 para achar o ângulo em graus e desenhe os setores com o transferidor."),
           ("O que a BNCC pede no 7º ano?", "Planejar e realizar pesquisa envolvendo tema da realidade social, identificando a necessidade de ser censitária ou de usar amostra (EF07MA36) e interpretar e analisar dados apresentados em gráfico de setores divulgados pela mídia e compreender quando é possível ou conveniente sua utilização (EF07MA37).")]
    unit(R, "graficos-de-setores-e-pesquisa", "E", ["EF07MA36", "EF07MA37"],
         "Planejar e realizar pesquisa envolvendo tema da realidade social, identificando a necessidade de ser censitária ou de usar amostra, e interpretar os dados para comunicá-los por meio de relatório escrito, tabelas e gráficos; interpretar e analisar dados apresentados em gráfico de setores divulgados pela mídia e compreender quando é possível ou conveniente sua utilização",
         "Gráficos de setores e pesquisa amostral", "Gráficos de setores e pesquisa",
         "Atividades de matemática para o 7º ano sobre gráficos de setores e pesquisas: porcentagem e graus, ler gráficos de setores, quando usá-los, população, amostra e tipos de amostragem. 100 exercícios com gabarito.",
         "100% = 360°; 1% = 3,6°.", "A amostra deve representar a população.",
         body, faq, sets, 20, grade="7-ano")


if __name__ == "__main__":
    main()
