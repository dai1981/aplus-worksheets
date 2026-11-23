# -*- coding: utf-8 -*-
"""
Brasil Matemática 5º ano: Plano cartesiano (Geometria, EF05MA14, EF05MA15)
  python3 tools/gen_br_matematica_5_plano_cartesiano.py
Malha quadriculada e 1º quadrante do plano cartesiano; ler e marcar coordenadas (x, y); eixo horizontal e vertical;
deslocamentos (direita, esquerda, para cima, para baixo); trajetos e mudanças de direção num mapa; figuras no plano.
Erros: trocar a ordem (x, y), contar os quadradinhos em vez das linhas, começar a contar no 1 em vez do 0.
"""
import random
from br_common import mcq, lesson, make_unit, mix, wrap, text, line, INK, GREEN, RED, BLUE, Kids

R = random.Random(80514)
K = Kids(R)
C = 32
N = 8
LET = "ABCDEFGHJKLMNPRSTUVW"
X0, Y0 = 30, 18


def px(x, y):
    return X0 + x * C, Y0 + (N - y) * C


def plano(points=(), polys=(), path=None, n=N):
    """points: [(x, y, rótulo, cor)]; polys: [[(x, y), …]]"""
    s = []
    for i in range(n + 1):
        s.append(line(X0 + i * C, Y0, X0 + i * C, Y0 + n * C, "#c9d6e3", 1))
        s.append(line(X0, Y0 + i * C, X0 + n * C, Y0 + i * C, "#c9d6e3", 1))
        s.append(text(X0 + i * C, Y0 + n * C + 18, str(i), 13))
        if i:
            s.append(text(X0 - 12, Y0 + (n - i) * C + 5, str(i), 13))
    s.append(line(X0, Y0 + n * C, X0 + n * C + 10, Y0 + n * C, INK, 2))
    s.append(line(X0, Y0 + n * C, X0, Y0 - 8, INK, 2))
    s.append(text(X0 + n * C + 16, Y0 + n * C + 5, "x", 14))
    s.append(text(X0, Y0 - 10, "y", 14))
    for poly in polys:
        pts = " ".join("%d,%d" % px(x, y) for x, y in poly)
        s.append("<polygon points='%s' fill='#cfe6d6' stroke='%s' stroke-width='2'/>" % (pts, GREEN))
    if path:
        pts = " ".join("%d,%d" % px(x, y) for x, y in path)
        s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3'/>" % (pts, BLUE))
    for x, y, lab, col in points:
        cx, cy = px(x, y)
        s.append("<circle cx='%d' cy='%d' r='5' fill='%s'/>" % (cx, cy, col))
        s.append(text(cx + 10, cy - 7, lab, 14, col=col, anchor="start"))
    return wrap(X0 + n * C + 28, Y0 + n * C + 26, "".join(s), "plano cartesiano com eixos x e y de 0 a %d" % n, lg=True)


def pts(k):
    out = set()
    while len(out) < k:
        out.add((R.randint(0, N), R.randint(0, N)))
    return sorted(out, key=lambda _: R.random())


def co(p):
    return "(%d, %d)" % p


def s1_ler():
    P = pts(4)
    labs = R.sample(LET, 4)
    i = R.randrange(4)
    x, y = P[i]
    if x == y:
        return None
    pic = plano([(a, b, l, RED if j == i else INK) for j, ((a, b), l) in enumerate(zip(P, labs))])
    return mcq(pic + "Quais são as coordenadas do ponto %s?" % labs[i], co((x, y)), [co((y, x)), co((x + 1, y)) if x < N else co((x - 1, y)), co((x, y + 1)) if y < N else co((x, y - 1))],
               "Primeiro ande no eixo x (horizontal): %d. Depois suba no eixo y (vertical): %d. <b>%s</b>." % (x, y, co((x, y))))


def s1_qual():
    P = pts(4)
    labs = R.sample(LET, 4)
    i = R.randrange(4)
    x, y = P[i]
    if x == y:
        return None
    pic = plano([(a, b, l, INK) for (a, b), l in zip(P, labs)])
    return mcq(pic + "Que ponto está em %s?" % co((x, y)), labs[i], [labs[j] for j in range(4) if j != i],
               "Ande %d no eixo x e suba %d no eixo y: é o ponto <b>%s</b>." % (x, y, labs[i]))


def s2_eixos():
    k = R.choice(["x", "y", "origem", "sobre_x", "sobre_y"])
    if k == "x":
        x, y = R.randint(1, 9), R.randint(1, 9)
        if x == y:
            return None
        return mcq("No ponto %s, qual é a coordenada x (a primeira)?" % co((x, y)), str(x), [str(y), str(x + y), "0"], "A primeira coordenada é a do eixo horizontal (x): <b>%d</b>." % x)
    if k == "y":
        x, y = R.randint(1, 9), R.randint(1, 9)
        if x == y:
            return None
        return mcq("No ponto %s, qual é a coordenada y (a segunda)?" % co((x, y)), str(y), [str(x), str(x + y), "0"], "A segunda coordenada é a do eixo vertical (y): <b>%d</b>." % y)
    if k == "origem":
        return mcq("Qual é o ponto onde os dois eixos se cruzam (a origem)?", "(0, 0)", ["(1, 1)", "(0, 1)", "(1, 0)"], "Na origem, x = 0 e y = 0: <b>(0, 0)</b>.")
    if k == "sobre_x":
        a = R.randint(2, 8)
        return mcq("Qual destes pontos está <b>sobre o eixo x</b>? (%d, 0), (0, %d), (%d, %d) ou (%d, 1)?" % (a, a, a, a, a), "(%d, 0)" % a, ["(0, %d)" % a, "(%d, %d)" % (a, a), "(%d, 1)" % a],
                   "Sobre o eixo x, a altura é 0: y = 0. <b>(%d, 0)</b>." % a)
    a = R.randint(2, 8)
    return mcq("Qual destes pontos está <b>sobre o eixo y</b>? (%d, 0), (0, %d), (%d, %d) ou (1, %d)?" % (a, a, a, a, a), "(0, %d)" % a, ["(%d, 0)" % a, "(%d, %d)" % (a, a), "(1, %d)" % a],
               "Sobre o eixo y, não andamos para a direita: x = 0. <b>(0, %d)</b>." % a)


DIR = {"direita": (1, 0), "esquerda": (-1, 0), "cima": (0, 1), "baixo": (0, -1)}


def mover(p, moves):
    x, y = p
    for d, n in moves:
        dx, dy = DIR[d]
        x, y = x + dx * n, y + dy * n
    return x, y


def frase(moves):
    return ", ".join("%d para %s" % (n, "a " + d if d in ("direita", "esquerda") else d) for d, n in moves)


def s3_mover():
    p = (R.randint(0, N), R.randint(0, N))
    k = R.randint(1, 2)
    ds = R.sample(list(DIR), k)
    moves = [(d, R.randint(1, 4)) for d in ds]
    q = mover(p, moves)
    if not (0 <= q[0] <= N and 0 <= q[1] <= N) or q == p:
        return None
    wrong = [co((q[1], q[0])) if q[0] != q[1] else None]
    rev = mover(p, [({"direita": "esquerda", "esquerda": "direita", "cima": "baixo", "baixo": "cima"}[d], n) for d, n in moves])
    wrong += [co(rev) if rev[0] >= 0 and rev[1] >= 0 else None, co((q[0] + 1, q[1])), co((q[0], q[1] + 1)), co(p)]
    return mcq("Um robô está em %s e anda %s. Em que ponto ele para?" % (co(p), frase(moves)), co(q), wrong,
               "Para a direita/esquerda muda o x; para cima/baixo muda o y. %s → <b>%s</b>." % (co(p), co(q)))


def s3_como():
    p = (R.randint(0, 5), R.randint(0, 5))
    dx, dy = R.randint(1, 3), R.randint(1, 3)
    sx, sy = R.choice([1, -1]), R.choice([1, -1])
    q = (p[0] + sx * dx, p[1] + sy * dy)
    if not (0 <= q[0] <= N and 0 <= q[1] <= N):
        return None
    h = "%d para a %s" % (dx, "direita" if sx > 0 else "esquerda")
    v = "%d para %s" % (dy, "cima" if sy > 0 else "baixo")
    h2 = "%d para a %s" % (dx, "esquerda" if sx > 0 else "direita")
    v2 = "%d para %s" % (dy, "baixo" if sy > 0 else "cima")
    h3 = "%d para a %s" % (dy, "direita" if sx > 0 else "esquerda")
    v3 = "%d para %s" % (dx, "cima" if sy > 0 else "baixo")
    return mcq("Como ir do ponto %s ao ponto %s?" % (co(p), co(q)), "%s e %s" % (h, v), ["%s e %s" % (h2, v), "%s e %s" % (h, v2), "%s e %s" % (h3, v3) if dx != dy else "%s e %s" % (h2, v2)],
               "x vai de %d para %d (%s); y vai de %d para %d (%s). <b>%s e %s</b>." % (p[0], q[0], h, p[1], q[1], v, h, v))


def s4_figura():
    k = R.choice(["ret", "tri", "quad"])
    x0, y0 = R.randint(0, 3), R.randint(0, 3)
    w, h = R.randint(2, 4), R.randint(2, 4)
    if k == "quad":
        h = w
    if k == "tri":
        poly = [(x0, y0), (x0 + w, y0), (x0, y0 + h)]
    else:
        poly = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
    labs = "ABCD"[:len(poly)]
    pic = plano([(x, y, l, INK) for (x, y), l in zip(poly, labs)], polys=[poly])
    i = R.randrange(1, len(poly))
    x, y = poly[i]
    if k == "tri" or R.random() < 0.5:
        return mcq(pic + "Quais são as coordenadas do vértice %s?" % labs[i], co((x, y)), [co((y, x)) if x != y else co((x + 1, y)), co((x - 1, y)) if x else co((x + 2, y)), co((x, y - 1)) if y else co((x, y + 2))],
                   "Do 0, ande %d para a direita e %d para cima: <b>%s</b>." % (x, y, co((x, y))))
    nome = "quadrado" if w == h else "retângulo"
    return mcq(pic + "A figura ABCD é um %s. Quantas unidades mede o lado AB?" % nome, str(w), [str(h) if h != w else str(w + 1), str(w + 1), str(x0 + w), str(w * 4), str(w * w), str(w - 1)],
               "A vai de x = %d até B em x = %d: %d − %d = <b>%d</b>." % (x0, x0 + w, x0 + w, x0, w))


def s4_falta():
    x0, y0 = R.randint(0, 3), R.randint(0, 3)
    w, h = R.randint(2, 4), R.randint(2, 5)
    poly = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
    i = R.randrange(4)
    shown = [p for j, p in enumerate(poly) if j != i]
    x, y = poly[i]
    return mcq("Três vértices de um retângulo estão em %s, %s e %s. Onde está o quarto vértice?" % tuple(co(p) for p in shown), co((x, y)),
               [co((y, x)) if x != y else co((x + 1, y + 1)), co((x + 1, y)), co((x, y + 1)), co((x0 + w + 1, y0 + h + 1))],
               "Num retângulo, os vértices se alinham: o x de um vizinho e o y do outro. <b>%s</b>." % co((x, y)))


LUGARES = ["a escola", "a padaria", "o parque", "a farmácia", "o mercado", "a biblioteca", "o hospital", "a praça", "o cinema", "o museu"]


def s5_mapa():
    P = pts(5)
    L = R.sample(LUGARES, 5)
    labs = [l.split(" ")[1][0].upper() for l in L]
    if len(set(labs)) < 5:
        return None
    pic = plano([(x, y, lb, INK) for (x, y), lb in zip(P, labs)])
    leg = "; ".join("%s = %s" % (lb, l) for lb, l in zip(labs, L))
    k = R.choice(["onde", "qual", "caminho"])
    i = R.randrange(5)
    if k == "onde":
        x, y = P[i]
        if x == y:
            return None
        return mcq(pic + "Legenda: %s. Em que coordenadas fica %s?" % (leg, L[i]), co(P[i]), [co((y, x)), co(P[(i + 1) % 5]), co(P[(i + 2) % 5])],
                   "%s está no ponto %s: <b>%s</b>." % (L[i][0].upper() + L[i][1:], labs[i], co(P[i])))
    if k == "qual":
        return mcq(pic + "Legenda: %s. O que fica no ponto %s?" % (leg, co(P[i])), L[i], [L[j] for j in range(5) if j != i],
                   "No ponto %s está a letra %s: <b>%s</b>." % (co(P[i]), labs[i], L[i]))
    j = (i + 1) % 5
    a, b = P[i], P[j]
    dx, dy = b[0] - a[0], b[1] - a[1]
    if dx == 0 or dy == 0:
        return None
    good = "%d para a %s e %d para %s" % (abs(dx), "direita" if dx > 0 else "esquerda", abs(dy), "cima" if dy > 0 else "baixo")
    w1 = "%d para a %s e %d para %s" % (abs(dx), "esquerda" if dx > 0 else "direita", abs(dy), "cima" if dy > 0 else "baixo")
    w2 = "%d para a %s e %d para %s" % (abs(dx), "direita" if dx > 0 else "esquerda", abs(dy), "baixo" if dy > 0 else "cima")
    w3 = "%d para a %s e %d para %s" % (abs(dy), "direita" if dx > 0 else "esquerda", abs(dx), "cima" if dy > 0 else "baixo") if abs(dx) != abs(dy) else "%d para a %s e %d para %s" % (abs(dx) + 1, "direita" if dx > 0 else "esquerda", abs(dy), "cima" if dy > 0 else "baixo")
    return mcq(pic + "Legenda: %s. Como ir de %s até %s, andando pelas linhas?" % (leg, L[i], L[j]), good, [w1, w2, w3],
               "De %s a %s: x muda %+d e y muda %+d. <b>%s</b>." % (co(a), co(b), dx, dy, good))


def main():
    seen = set()
    sets = [
        ("Ler coordenadas", mix(R, seen, [(s1_ler, 12), (s1_qual, 8)])),
        ("Os eixos x e y", mix(R, seen, [(s2_eixos, 20)])),
        ("Deslocamentos", mix(R, seen, [(s3_mover, 12), (s3_como, 8)])),
        ("Figuras no plano", mix(R, seen, [(s4_figura, 12), (s4_falta, 8)])),
        ("Mapas e trajetos", mix(R, seen, [(s5_mapa, 20)])),
    ]
    body = lesson(
        ["O plano cartesiano tem dois eixos: o <b>eixo x</b> (horizontal) e o <b>eixo y</b> (vertical). Eles se cruzam na <b>origem</b> (0, 0).",
         "Um ponto é dado por um <b>par ordenado (x, y)</b>: primeiro ande no eixo x, depois suba no eixo y.",
         "Andar para a direita ou para a esquerda muda o x; andar para cima ou para baixo muda o y.",
         "As linhas da malha é que têm números: conte as linhas a partir do 0, não os quadradinhos."],
        [("Onde fica o ponto (3, 5)?", ["3 para a direita, a partir do 0", "5 para cima"], "x = 3, y = 5"),
         ("Um robô em (2, 4) anda 3 para a direita e 1 para baixo.", ["x: 2 + 3 = 5", "y: 4 − 1 = 3"], "(5, 3)")],
        [["Trocar a ordem: (3, 5) no lugar de (5, 3)", "Sempre x primeiro (horizontal), depois y (vertical)."],
         ["Começar a contar no 1", "A origem é o 0; o primeiro risco depois dela é o 1."],
         ["Contar os quadradinhos em vez das linhas", "Os pontos ficam nos cruzamentos das linhas."]],
        plano([(3, 5, "A", RED), (5, 3, "B", BLUE)]))
    faq = [("O 5º ano usa números negativos no plano cartesiano?", "Não. No 5º ano a BNCC trabalha o 1º quadrante, com coordenadas positivas. Os quatro quadrantes vêm no 7º ano."),
           ("Para que serve o plano cartesiano?", "Para localizar pontos com precisão: mapas, jogos de batalha naval, telas de computador e gráficos usam a mesma ideia.")]
    make_unit(R, "plano-cartesiano", "G", ["EF05MA14", "EF05MA15"],
              "Utilizar e compreender diferentes representações para a localização de objetos no plano, como mapas, células em planilhas eletrônicas e coordenadas geográficas, a fim de desenvolver as primeiras noções de coordenadas cartesianas; interpretar, descrever e representar a localização ou movimentação de objetos no plano cartesiano (1º quadrante), utilizando coordenadas cartesianas, indicando mudanças de direção e de sentido e giros",
              "Plano cartesiano: coordenadas, deslocamentos e mapas", "Plano cartesiano",
              "Atividades de matemática para o 5º ano sobre o plano cartesiano (1º quadrante): ler e marcar coordenadas, eixos x e y, deslocamentos, figuras e mapas. 100 exercícios com gabarito.",
              "(x, y): primeiro o eixo horizontal, depois o vertical.", "A origem é o ponto (0, 0).",
              body, faq, sets, 14, grade="5-ano")


if __name__ == "__main__":
    main()
