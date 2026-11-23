# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 3ª série: Correlação e reta de ajuste (EM13MAT510)
  python3 tools/gen_br_matematica_em3_correlacao_e_reta_de_ajuste.py
Gráfico de dispersão; correlação positiva, negativa ou fraca; reta de ajuste (tendência) e previsões;
interpretar a inclinação; valores atípicos; correlação não é causa.
Erros: achar que correlação prova causa, prever muito fora dos dados, ler a inclinação com o sinal trocado.
"""
import random
from fractions import Fraction as F
from br_em import M, d, fq, expr, bank, mix, lesson, unit, curva, num

R = random.Random(93007)
CTX = [("horas de estudo", "nota", 1), ("temperatura (°C)", "sorvetes vendidos", 1), ("idade do carro (anos)", "preço (mil R$)", -1),
       ("altura (cm)", "número do calçado", 1), ("horas de celular por dia", "horas de sono", -1), ("km rodados", "litros de gasolina", 1)]


def nuvem(m, b, kind, n=10):
    pts = []
    for _ in range(n):
        x = R.uniform(1, 9)
        if kind == "fraca":
            y = R.uniform(1, 9)
        else:
            y = m * x + b + R.uniform(-0.9, 0.9)
        if 0.3 <= y <= 9.7:
            pts.append((round(x, 1), round(y, 1), ""))
    return pts


def s1_tipo():
    kind = R.choice(["positiva", "negativa", "fraca"])
    m = {"positiva": R.choice([0.6, 0.8, 1.0]), "negativa": R.choice([-0.6, -0.8, -1.0]), "fraca": 0}[kind]
    b = {"positiva": R.uniform(0.5, 2), "negativa": R.uniform(8, 9.5), "fraca": 0}[kind]
    pts = nuvem(m, b, kind)
    if len(pts) < 7:
        return None
    g = curva([(lambda x: None, "")], (0, 10, 1), (0, 10, 1), pts=pts, label="gráfico de dispersão")
    ans = {"positiva": "correlação positiva", "negativa": "correlação negativa", "fraca": "correlação fraca ou nula"}[kind]
    return M(g + "Que tipo de correlação o gráfico de dispersão mostra?", ans, [x for x in ("correlação positiva", "correlação negativa", "correlação fraca ou nula", "correlação perfeita") if x != ans],
             {"positiva": "Quando x aumenta, y tende a aumentar: <b>positiva</b>.", "negativa": "Quando x aumenta, y tende a diminuir: <b>negativa</b>.", "fraca": "Os pontos não seguem uma tendência: <b>fraca ou nula</b>."}[kind])


def s2_prever():
    cx, cy, sg = R.choice(CTX)
    a = F(R.choice([2, 3, 4, 5, 6, 8, 10]), R.choice([1, 2])) * sg
    b = R.randint(5, 60) if sg > 0 else R.randint(60, 120)
    x = R.randint(2, 12)
    y = a * x + b
    if y <= 0:
        return None
    k = R.choice(["prev", "incl"])
    reta = "y = " + expr([(a, "x"), (b, "")])
    if k == "prev":
        return M("A reta de ajuste entre %s (x) e %s (y) é %s. Qual é a previsão de y para x = %d?" % (cx, cy, reta, x), d(y), [d(a * x), d(b - a * x) if b - a * x > 0 else d(y + abs(a)), d(a + b + x)],
                 "%s · %d %s %d = <b>%s</b>." % (fq(a), x, "+", b, d(y)))
    return M("A reta de ajuste entre %s (x) e %s (y) é %s. O que significa o coeficiente %s?" % (cx, cy, reta, fq(a)),
             "a cada 1 unidade a mais de x, y %s em média %s" % ("aumenta" if a > 0 else "diminui", fq(abs(a))),
             ["y vale %s quando x = 0" % fq(a), "a cada 1 unidade a mais de x, y %s em média %s" % ("diminui" if a > 0 else "aumenta", fq(abs(a))), "x vale %s quando y = 0" % fq(a)],
             "O coeficiente angular é a variação média de y por unidade de x: <b>%s %s</b>." % ("aumenta" if a > 0 else "diminui", fq(abs(a))))


def s3_grafico_reta():
    m = R.choice([F(1, 2), F(1), F(-1, 2), F(-1)])
    b = 2 if m > 0 else 8
    pts = []
    for x in range(1, 10):
        y = float(m * x + b) + R.choice([-0.6, -0.3, 0.3, 0.6])
        if 0.3 <= y <= 9.7:
            pts.append((x, y, ""))
    out = None
    if R.random() < 0.5:
        ox = R.choice([3, 5, 7])
        oy = 9 if float(m * ox + b) < 5 else 1
        pts.append((ox, oy, ""))
        out = (ox, oy)
    g = curva([(lambda x: float(m * x + b), "reta")], (0, 10, 1), (0, 10, 1), pts=pts, label="gráfico de dispersão com reta de ajuste")
    if out:
        return M(g + "Qual ponto parece ser um valor atípico (fora da tendência)?", "(%d, %d)" % out, ["(1, %s)" % d(m + b), "(%d, %s)" % (out[0] + 1, d(m * (out[0] + 1) + b)), "(9, %s)" % d(m * 9 + b)],
                 "Ele fica muito longe da reta: <b>(%d, %d)</b>." % out)
    x = R.choice([12, 14, 16]) if m > 0 else 12
    yv = m * x + b
    if yv < 0:
        return M(g + "A reta de ajuste é y = %s. Faz sentido usá-la para prever y quando x = 30?" % expr([(m, "x"), (b, "")]), "não, é muito fora do intervalo dos dados (e daria valor negativo)", ["sim, sempre", "sim, e o resultado é exato", "não, porque a reta é crescente"],
                 "Extrapolar muito além dos dados é arriscado: <b>não</b>.")
    return M(g + "Pela reta de ajuste y = %s, qual é a previsão para x = %d?" % (expr([(m, "x"), (b, "")]), x), d(yv), [d(m * x), d(yv + 2), d(b)], "%s · %d + %d = <b>%s</b>." % (fq(m), x, b, d(yv)))


s4_conceitos = bank(R, [
    ("Em várias cidades, mais sorvetes vendidos acompanham mais afogamentos. Isso prova que sorvete causa afogamento?", "não; os dois aumentam no calor (correlação não é causa)", ["sim", "sim, se a correlação for forte", "não, porque os dados estão errados"]),
    ("Uma correlação negativa significa que…", "quando uma variável aumenta, a outra tende a diminuir", ["as variáveis são negativas", "não há relação", "uma causa a outra"]),
    ("A reta de ajuste serve para…", "descrever a tendência e fazer previsões aproximadas", ["passar por todos os pontos", "provar uma causa", "mostrar só o maior valor"]),
    ("Um coeficiente de correlação perto de 0 indica…", "relação linear fraca ou nula", ["relação forte", "relação perfeita", "variáveis iguais"]),
    ("Um coeficiente de correlação perto de −1 indica…", "relação linear forte e negativa", ["nenhuma relação", "relação positiva", "erro nos dados"]),
    ("Prever valores muito fora do intervalo dos dados (extrapolar) é…", "arriscado, pois a tendência pode mudar", ["sempre exato", "proibido", "mais preciso"]),
    ("Num gráfico de dispersão, cada ponto representa…", "um par de valores (x, y) de um mesmo indivíduo", ["uma média", "um intervalo", "uma frequência"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Tipos de correlação", mix(R, seen, [(s1_tipo, 14), (s4_conceitos, 6)])),
        ("Reta de ajuste: previsões", mix(R, seen, [(s2_prever, 20)])),
        ("Interpretar a reta", mix(R, seen, [(s3_grafico_reta, 20)])),
        ("Correlação e causa", mix(R, seen, [(s2_prever, 10), (s1_tipo, 6), (s4_conceitos, 1), (s3_grafico_reta, 3)])),
        ("Revisão", mix(R, seen, [(s2_prever, 10), (s1_tipo, 6), (s3_grafico_reta, 4)])),
    ]
    body = lesson(
        ["Um <b>gráfico de dispersão</b> mostra pares (x, y). Se os pontos sobem, a correlação é <b>positiva</b>; se descem, <b>negativa</b>; se não há tendência, é <b>fraca ou nula</b>.",
         "A <b>reta de ajuste</b> (ou de regressão) passa no meio da nuvem de pontos. A inclinação diz quanto y muda, em média, para cada unidade de x.",
         "Use a reta para prever valores <b>dentro</b> do intervalo dos dados; muito fora dele, a previsão pode falhar.",
         "<b>Correlação não é causa</b>: duas variáveis podem variar juntas por causa de uma terceira."],
        [("Reta: nota = 1,5 · horas + 4", ["para 4 horas: 1,5 · 4 + 4"], "nota prevista 10")],
        [["Concluir causa a partir de correlação", "Procure uma terceira variável que explique."],
         ["Extrapolar demais", "Fique perto do intervalo dos dados."],
         ["Trocar o sinal da inclinação", "Inclinação negativa: y diminui quando x aumenta."]])
    faq = [("O que é uma reta de ajuste?", "É a reta que melhor representa a tendência dos pontos num gráfico de dispersão. Ela permite fazer previsões aproximadas dentro do intervalo dos dados."),
           ("O que a BNCC pede?", "Investigar conjuntos de dados relativos ao comportamento de duas variáveis numéricas, usando ou não tecnologias da informação, e, quando apropriado, levar em conta a variação e utilizar uma reta para descrever a relação observada (EM13MAT510).")]
    unit(R, "correlacao-e-reta-de-ajuste", "E", ["EM13MAT510"],
         "Investigar conjuntos de dados relativos ao comportamento de duas variáveis numéricas, usando ou não tecnologias da informação, e, quando apropriado, levar em conta a variação e utilizar uma reta para descrever a relação observada",
         "Correlação e reta de ajuste", "Correlação e reta de ajuste",
         "Atividades de matemática para a 3ª série do Ensino Médio sobre gráficos de dispersão: correlação positiva, negativa e fraca, reta de ajuste, previsões, valores atípicos e correlação versus causa. 100 exercícios com gabarito.",
         "Correlação não é causa", "A reta de ajuste mostra a tendência.",
         body, faq, sets, 7, grade="3-serie")


if __name__ == "__main__":
    main()
