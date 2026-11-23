# -*- coding: utf-8 -*-
"""
Brasil Matemática 5º ano: Volume (Grandezas e medidas, EF05MA21)
  python3 tools/gen_br_matematica_5_volume.py
Volume como o espaço ocupado; medir volumes empilhando cubinhos; blocos retangulares (camadas: comprimento × largura × altura);
construções de cubinhos vistas de cima; centímetro cúbico (cm³); comparar volumes; problemas com caixas.
Erros: contar só os cubinhos que aparecem, somar as três medidas em vez de multiplicar, confundir volume com área.
"""
import random
import gen_br_matematica_3_figuras_geometricas_espaciais as BR3
from br_common import mcq, num, lesson, make_unit, mix, wrap, INK, Kids

R = random.Random(80520)
K = Kids(R)
BR3.DE.R = random.Random(80920)
TOPS = ["#f6d6a8", "#c9dcf2", "#cfe6d6", "#f2c6d0"]


def bloco(a, b, c, col=None):
    """bloco de a (comprimento) × b (profundidade) × c (altura) cubinhos, em perspectiva"""
    u = 26
    dx, dy = u * 0.5, -u * 0.42
    x0, y0 = 10, 14 + b * -dy + c * u
    col = col or R.choice(TOPS)
    s = []

    def P(x, y, z):
        return (x0 + x * u + y * dx, y0 - z * u + y * dy)

    def quad(p):
        return "<polygon points='%s' fill='%%s' stroke='%s' stroke-width='1.2'/>" % (" ".join("%.1f,%.1f" % q for q in p), INK)
    for z in range(c):
        for x in range(a):
            s.append(quad([P(x, 0, z), P(x + 1, 0, z), P(x + 1, 0, z + 1), P(x, 0, z + 1)]) % col)
    for y in range(b):
        for x in range(a):
            s.append(quad([P(x, y, c), P(x + 1, y, c), P(x + 1, y + 1, c), P(x, y + 1, c)]) % "#ffffff")
    for y in range(b):
        for z in range(c):
            s.append(quad([P(a, y, z), P(a, y + 1, z), P(a, y + 1, z + 1), P(a, y, z + 1)]) % "#dddddd")
    W = x0 * 2 + a * u + b * dx
    H = y0 + 10
    return wrap(int(W), int(H), "".join(s), "bloco formado por cubinhos iguais")


def dims(maxv=60):
    while True:
        a, b, c = R.randint(2, 5), R.randint(2, 4), R.randint(2, 4)
        if a * b * c <= maxv:
            return a, b, c


def s1_contar():
    a, b, c = dims()
    V = a * b * c
    vis = a * b + a * c + b * c - a - b - c + 1
    return mcq(bloco(a, b, c) + "O bloco é maciço (cheio de cubinhos iguais). Quantos cubinhos ele tem?", str(V),
               [str(x) for x in (vis, a + b + c, a * b + a * c + b * c, V + a * b)],
               "Cada camada tem %d × %d = %d cubinhos, e são %d camadas: %d × %d = <b>%d</b>." % (a, b, a * b, c, a * b, c, V))


def s1_camada():
    a, b, c = dims()
    k = R.choice(["camada", "camadas"])
    if k == "camada":
        return mcq(bloco(a, b, c) + "Quantos cubinhos há em cada camada deste bloco?", str(a * b), [str(x) for x in (a + b, a * b * c, a * c if a * c != a * b else b * c, 2 * (a + b))],
                   "Uma camada tem %d cubinhos de comprimento e %d de largura: %d × %d = <b>%d</b>." % (a, b, a, b, a * b))
    return mcq(bloco(a, b, c) + "Este bloco tem quantas camadas de cubinhos, de baixo para cima?", str(c), [str(x) for x in (a, b, a * b, c + 1) if x != c],
               "Conte a altura: <b>%d camadas</b>." % c)


def s2_medidas():
    a, b, c = R.randint(2, 12), R.randint(2, 10), R.randint(2, 8)
    V = a * b * c
    return mcq("Um bloco retangular tem %d cm de comprimento, %d cm de largura e %d cm de altura. Quantos cubinhos de 1 cm³ cabem nele?" % (a, b, c), num(V),
               [num(x) for x in (a + b + c, a * b + c, 2 * (a * b + a * c + b * c), a * b)], "Volume = comprimento × largura × altura = %d × %d × %d = <b>%s cm³</b>." % (a, b, c, num(V)))


def s2_falta():
    a, b, c = R.randint(2, 8), R.randint(2, 6), R.randint(2, 6)
    V = a * b * c
    return mcq("Uma caixa tem volume de %s cm³. O fundo mede %d cm por %d cm. Qual é a altura da caixa?" % (num(V), a, b), "%d cm" % c,
               ["%d cm" % x for x in (V - a * b, V // a, a * b, c + 1) if x != c], "Cada camada tem %d × %d = %d cm³. %s ÷ %d = <b>%d cm</b>." % (a, b, a * b, num(V), a * b, c))


def tr(it, pairs):
    if not it:
        return None
    for a, b in pairs:
        it["q"], it["e"] = it["q"].replace(a, b), it["e"].replace(a, b)
        it["c"] = [c.replace(a, b) for c in it["c"]]
    return mcq(it["q"], it["c"][0], it["c"][1:], it["e"])


def s3_planta():
    if R.random() < 0.6:
        return tr(BR3.DE.bauplan(), [("Ein Bauplan zeigt ein Würfelgebäude von oben. Die Zahl sagt, wie viele Würfel übereinander stehen. Wie viele Würfel sind es?",
                                      "A figura mostra uma construção de cubinhos vista de cima. Cada número diz quantos cubinhos estão empilhados naquele lugar. Qual é o volume da construção, em cubinhos?"),
                                     ("Addiere alle Zahlen im Bauplan:", "Some todos os números:"), ("aria-label='Bauplan'", "aria-label='vista de cima'")])
    return tr(BR3.DE.bauplan_hoch(), [("Bauplan eines Würfelgebäudes: Wie hoch ist der höchste Turm?", "Vista de cima de uma construção de cubinhos: quantos cubinhos tem a pilha mais alta?"),
                                      ("Die größte Zahl im Bauplan ist", "O maior número da vista de cima é"), ("Der höchste Turm ist", "A pilha mais alta tem"),
                                      (" Würfel</b> hoch.", " cubinhos</b>."), (" Würfel", " cubinhos"), ("aria-label='Bauplan'", "aria-label='vista de cima'")])


def s3_comparar():
    while True:
        p1, p2 = dims(48), dims(48)
        if p1 != p2:
            break
    v1, v2 = p1[0] * p1[1] * p1[2], p2[0] * p2[1] * p2[2]
    pic = bloco(*p1, col=TOPS[0]) + bloco(*p2, col=TOPS[1])
    if v1 == v2:
        ans = "Têm o mesmo volume"
    else:
        ans = "O primeiro" if v1 > v2 else "O segundo"
    return mcq(pic + "Os dois blocos são maciços. Qual tem o <b>maior volume</b>?", ans, [x for x in ["O primeiro", "O segundo", "Têm o mesmo volume", "O que for mais alto"] if x != ans],
               "Primeiro: %d × %d × %d = %d cubinhos. Segundo: %d × %d × %d = %d cubinhos. <b>%s</b>." % (p1[0], p1[1], p1[2], v1, p2[0], p2[1], p2[2], v2, ans))


IDEIAS = [("O que é o volume de um objeto?", "o espaço que ele ocupa", ["o contorno dele", "a área de uma face", "a massa dele"]),
          ("Que unidade mede volume?", "cm³ (centímetro cúbico)", ["cm² (centímetro quadrado)", "cm (centímetro)", "kg (quilograma)"]),
          ("1 cm³ é o volume de…", "um cubinho de 1 cm de aresta", ["um quadrado de 1 cm de lado", "uma régua de 1 cm", "um litro de água"]),
          ("Um bloco de 4 cubinhos de comprimento, 2 de largura e 3 de altura tem volume de…", "24 cubinhos", ["9 cubinhos", "14 cubinhos", "26 cubinhos"]),
          ("Se dobrarmos a altura de um bloco, o volume…", "dobra", ["fica igual", "fica 4 vezes maior", "diminui"]),
          ("Dois blocos diferentes podem ter o mesmo volume?", "Sim, como 2 × 3 × 4 e 1 × 4 × 6", ["Não, nunca", "Só se forem cubos", "Só se tiverem a mesma altura"]),
          ("Para saber quantas caixas cabem num caminhão, pensamos no…", "volume", ["perímetro", "ângulo", "número de vértices"]),
          ("Qual destes tem maior volume?", "uma caixa de geladeira", ["uma caixa de fósforos", "um dado", "uma borracha"]),
          ("Um cubo com 3 cubinhos em cada aresta tem quantos cubinhos?", "27", ["9", "12", "18"]),
          ("Um cubo com 2 cubinhos em cada aresta tem quantos cubinhos?", "8", ["4", "6", "12"])]


def s4_ideia():
    q, a, w = R.choice(IDEIAS)
    return mcq(q, a, w, "Volume é o espaço ocupado; no bloco, conte camadas: comprimento × largura × altura. Resposta: <b>%s</b>." % a)


def s4_cubo():
    n = R.randint(2, 6)
    return mcq(bloco(n, n, n) + "Este cubo é formado por cubinhos iguais. Qual é o volume dele, em cubinhos?", str(n ** 3), [str(x) for x in (n * n, 3 * n, n * n * 6, n ** 3 + n * n) if x != n ** 3],
               "%d × %d × %d = <b>%d</b> cubinhos." % (n, n, n, n ** 3))


def s5_problema():
    k = R.choice(["caixas", "aquario", "tijolos", "dados", "falta", "camadas"])
    p, g = K.next()
    if k == "caixas":
        a, b, c = R.randint(3, 6), R.randint(2, 5), R.randint(2, 4)
        return mcq("Um depósito empilha caixas iguais: %d de comprimento, %d de largura e %d de altura. Quantas caixas há?" % (a, b, c), str(a * b * c),
                   [str(x) for x in (a + b + c, a * b, a * b * c + c)], "%d × %d × %d = <b>%d caixas</b>." % (a, b, c, a * b * c))
    if k == "aquario":
        a, b, c = R.choice([(40, 20, 30), (50, 30, 30), (30, 20, 20), (60, 30, 40), (40, 25, 30)])
        V = a * b * c
        return mcq("Um aquário mede %d cm por %d cm por %d cm. Qual é o volume dele? (1 L = 1.000 cm³)" % (a, b, c), "%s cm³ = %d L" % (num(V), V // 1000),
                   ["%s cm³ = %s L" % (num(V), num(V)), "%d cm³ = %d L" % (a + b + c, a + b + c), "%s cm³ = %s L" % (num(V), num(V // 100))],
                   "%d × %d × %d = %s cm³. %s ÷ 1.000 = <b>%d L</b>." % (a, b, c, num(V), num(V), V // 1000))
    if k == "tijolos":
        a, b, c = R.randint(5, 12), R.randint(2, 4), R.randint(3, 8)
        return mcq("Um muro foi feito com tijolos iguais: %d tijolos de comprimento, %d de espessura e %d de altura. Quantos tijolos foram usados?" % (a, b, c), str(a * b * c),
                   [str(x) for x in (a + b + c, a * c, a * b * c - a)], "%d × %d × %d = <b>%d tijolos</b>." % (a, b, c, a * b * c))
    if k == "dados":
        n = R.choice([2, 3, 4])
        return mcq("%s quer montar um cubo grande com dados iguais, com %d dados em cada aresta. Quantos dados vai usar?" % (p, n), str(n ** 3),
                   [str(x) for x in (n * n, 3 * n, 6 * n * n) if x != n ** 3] + [str(n ** 3 + 1)], "%d × %d × %d = <b>%d dados</b>." % (n, n, n, n ** 3))
    if k == "falta":
        a, b, c = R.randint(2, 4), R.randint(2, 4), R.randint(2, 4)
        tem = a * b * (c - 1)
        return mcq("Uma caixa comporta %d × %d × %d cubinhos. %s já colocou %d cubinhos. Quantos faltam para encher a caixa?" % (a, b, c, p, tem), str(a * b),
                   [str(x) for x in (a * b * c, tem, a + b + c, a * b + 1)], "A caixa comporta %d. %d − %d = <b>%d</b>." % (a * b * c, a * b * c, tem, a * b))
    a, b = R.randint(3, 6), R.randint(2, 5)
    V = a * b * R.randint(3, 6)
    return mcq("Uma caixa tem fundo de %d × %d cubinhos e foi enchida com %d cubinhos. Quantas camadas de cubinhos há?" % (a, b, V), str(V // (a * b)),
               [str(x) for x in (V - a * b, V // a, a * b)], "%d ÷ (%d × %d) = %d ÷ %d = <b>%d camadas</b>." % (V, a, b, V, a * b, V // (a * b)))


def main():
    seen = set()
    sets = [
        ("Contar cubinhos", mix(R, seen, [(s1_contar, 12), (s1_camada, 8)])),
        ("Comprimento × largura × altura", mix(R, seen, [(s2_medidas, 12), (s2_falta, 8)])),
        ("Construções e comparação", mix(R, seen, [(s3_planta, 10), (s3_comparar, 10)])),
        ("O que é volume", mix(R, seen, [(s4_ideia, 10), (s4_cubo, 10)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["O <b>volume</b> é o espaço que um objeto ocupa. Podemos medi-lo contando quantos cubinhos iguais cabem nele.",
         "Num bloco, conte por <b>camadas</b>: cubinhos de uma camada (comprimento × largura) vezes o número de camadas (altura).",
         "Volume do bloco retangular = comprimento × largura × altura.",
         "Um cubinho de 1 cm de aresta tem volume de <b>1 cm³</b> (centímetro cúbico). 1.000 cm³ = 1 L."],
        [("Bloco de 4 por 3 cubinhos e 2 de altura.", ["cada camada: 4 × 3 = 12", "2 camadas: 12 × 2"], "24 cubinhos"),
         ("Caixa de 10 cm × 5 cm × 4 cm.", ["10 × 5 = 50", "50 × 4 = 200"], "200 cm³")],
        [["Contar só os cubinhos que aparecem", "Há cubinhos escondidos atrás e por baixo: conte por camadas."],
         ["Somar as medidas: 4 + 3 + 2 = 9", "Multiplique: 4 × 3 × 2 = 24."],
         ["Confundir volume com área", "Área é superfície (cm²); volume é espaço (cm³)."]],
        bloco(4, 3, 2, TOPS[0]))
    faq = [("O que o 5º ano aprende sobre volume?", "A BNCC pede reconhecer o volume como grandeza associada a sólidos geométricos e medi-lo por meio de empilhamento de cubos, de preferência com objetos concretos."),
           ("Qual é a relação entre volume e capacidade?", "Um cubo de 10 cm de aresta tem 1.000 cm³ e comporta exatamente 1 litro de água. Por isso 1 L = 1.000 cm³.")]
    make_unit(R, "volume", "M", ["EF05MA21"],
              "Reconhecer volume como grandeza associada a sólidos geométricos e medir volumes por meio de empilhamento de cubos, utilizando, preferencialmente, objetos concretos",
              "Volume: empilhamento de cubinhos e blocos retangulares", "Volume",
              "Atividades de matemática para o 5º ano sobre volume: contar cubinhos, camadas, comprimento × largura × altura, cm³, construções vistas de cima e problemas com caixas. 100 exercícios com gabarito.",
              "Volume = comprimento × largura × altura.", "Conte por camadas, incluindo os cubinhos escondidos.",
              body, faq, sets, 20, grade="5-ano")


if __name__ == "__main__":
    main()
