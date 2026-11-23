# -*- coding: utf-8 -*-
"""
Brasil Matemática 5º ano: Perímetro e área (Grandezas e medidas, EF05MA20)
  python3 tools/gen_br_matematica_5_perimetro_e_area.py
Perímetro (contorno) e área (superfície) na malha quadriculada e com medidas; área do retângulo e do quadrado (cm², m²);
figuras com a mesma área e perímetros diferentes, e com o mesmo perímetro e áreas diferentes; figuras compostas; problemas.
Erros: confundir área e perímetro, somar só dois lados do retângulo, contar os quadradinhos do contorno em vez dos de dentro.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, wrap, line, text, INK, GREEN, Kids, reais

R = random.Random(80519)
K = Kids(R)
C = 18
COLS = ["#cfe6d6", "#f6d6a8", "#c9dcf2", "#f2c6d0"]


def cells_perim(cells):
    s = set(cells)
    return sum(1 for (x, y) in s for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (x + dx, y + dy) not in s)


def malha(figs, W, H, labels=()):
    """figs: [(cells, ox, oy)]"""
    s = []
    for i in range(W + 1):
        s.append(line(6 + i * C, 6, 6 + i * C, 6 + H * C, "#c9d6e3", 1))
    for j in range(H + 1):
        s.append(line(6, 6 + j * C, 6 + W * C, 6 + j * C, "#c9d6e3", 1))
    for k, (cells, ox, oy) in enumerate(figs):
        cs = set(cells)
        for x, y in cs:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (6 + (ox + x) * C, 6 + (oy + y) * C, C, C, COLS[k % 4]))
        for x, y in cs:
            X, Y = 6 + (ox + x) * C, 6 + (oy + y) * C
            if (x, y - 1) not in cs:
                s.append(line(X, Y, X + C, Y, INK, 2.2))
            if (x, y + 1) not in cs:
                s.append(line(X, Y + C, X + C, Y + C, INK, 2.2))
            if (x - 1, y) not in cs:
                s.append(line(X, Y, X, Y + C, INK, 2.2))
            if (x + 1, y) not in cs:
                s.append(line(X + C, Y, X + C, Y + C, INK, 2.2))
    for x, y, t in labels:
        s.append(text(6 + x * C, 6 + y * C, t, 15))
    return wrap(12 + W * C, 12 + H * C, "".join(s), "figuras numa malha quadriculada", lg=True)


def rect(w, h):
    return [(x, y) for x in range(w) for y in range(h)]


def blob():
    w, h = R.randint(3, 6), R.randint(2, 4)
    cells = set(rect(w, h))
    for _ in range(R.randint(1, 3)):
        c = R.choice(sorted(cells))
        if len(cells) > 4:
            cells.discard(c)
    # manter conexo
    start = min(cells)
    seen, st = {start}, [start]
    while st:
        x, y = st.pop()
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + d[0], y + d[1])
            if n in cells and n not in seen:
                seen.add(n)
                st.append(n)
    if seen != cells:
        return None
    # sem buracos: cada célula vazia dentro do retângulo deve tocar a borda por um caminho
    return sorted(cells), w, h


def s1_malha():
    b = blob()
    if not b:
        return None
    cells, w, h = b
    holes = [(x, y) for x in range(w) for y in range(h) if (x, y) not in cells and 0 < x < w - 1 and 0 < y < h - 1]
    if holes:
        return None
    A, P = len(cells), cells_perim(cells)
    pic = malha([(cells, 1, 1)], w + 2, h + 2)
    if R.random() < 0.5:
        return mcq(pic + "Cada quadradinho tem 1 cm de lado. Qual é o perímetro da figura?", "%d cm" % P, ["%d cm" % x for x in (A, P + 2, P - 2, A + P)],
                   "Conte os lados dos quadradinhos no contorno: <b>%d cm</b>." % P)
    return mcq(pic + "Cada quadradinho tem 1 cm². Qual é a área da figura?", "%d cm²" % A, ["%d cm²" % x for x in (P, A + 1, A - 1, w * h)],
               "Conte os quadradinhos de dentro: <b>%d cm²</b>." % A)


def s1_ret():
    a, b = R.randint(3, 25), R.randint(2, 18)
    if a == b:
        return None
    k = R.choice(["per", "per", "area"])
    u = R.choice(["cm", "m"])
    if k == "per":
        return mcq("Um retângulo tem %d %s de comprimento e %d %s de largura. Qual é o perímetro?" % (a, u, b, u), "%d %s" % (2 * (a + b), u),
                   ["%d %s" % x for x in ((a + b, u), (a * b, u), (2 * a + b, u), (4 * a, u))], "%d + %d + %d + %d = <b>%d %s</b>." % (a, b, a, b, 2 * (a + b), u))
    return mcq("Um retângulo tem %d %s de comprimento e %d %s de largura. Qual é a área?" % (a, u, b, u), "%s %s²" % (num(a * b), u),
               ["%s %s²" % (num(x), u) for x in (2 * (a + b), a + b, a * b + a)] + ["%s %s" % (num(a * b), u)], "Área = comprimento × largura = %d × %d = <b>%s %s²</b>." % (a, b, num(a * b), u))


def s2_quadrado():
    L = R.randint(2, 15)
    k = R.choice(["area", "per", "lado_p", "lado_a"])
    if k == "area":
        return mcq("Qual é a área de um quadrado de %d cm de lado?" % L, "%d cm²" % (L * L), ["%d cm²" % x for x in (4 * L, 2 * L, L * L + L)],
                   "%d × %d = <b>%d cm²</b>." % (L, L, L * L))
    if k == "per":
        return mcq("Qual é o perímetro de um quadrado de %d cm de lado?" % L, "%d cm" % (4 * L), ["%d cm" % x for x in (L * L, 2 * L, 3 * L) if x != 4 * L] + ["%d cm" % (4 * L + 4)],
                   "4 lados iguais: 4 × %d = <b>%d cm</b>." % (L, 4 * L))
    if k == "lado_p":
        return mcq("Um quadrado tem perímetro de %d cm. Quanto mede o lado?" % (4 * L), "%d cm" % L, ["%d cm" % x for x in (4 * L // 2, 4 * L - 4, L + 4)] if L != 4 else ["8 cm", "12 cm", "2 cm"],
                   "%d ÷ 4 = <b>%d cm</b>." % (4 * L, L))
    return mcq("Um quadrado tem área de %d cm². Quanto mede o lado?" % (L * L), "%d cm" % L, ["%d cm" % x for x in (L * L // 4 if L * L % 4 == 0 and L != 4 else L + 2, L * L // 2, L + 1)],
               "Que número vezes ele mesmo dá %d? %d × %d = %d: <b>%d cm</b>." % (L * L, L, L, L * L, L))


def s3_mesma_area():
    A = R.choice([12, 16, 18, 20, 24, 36])
    pares = [(w, A // w) for w in range(1, A + 1) if A % w == 0 and w <= A // w]
    if len(pares) < 3:
        return None
    (w1, h1), (w2, h2) = R.sample(pares, 2)
    p1, p2 = 2 * (w1 + h1), 2 * (w2 + h2)
    if R.random() < 0.5 and max(h1, h2) <= 12 and w1 + w2 + 5 <= 30:
        figs = [(rect(h1, w1), 1, 1), (rect(h2, w2), h1 + 3, 1)]
        pic = malha(figs, h1 + h2 + 4, max(w1, w2) + 2)
        q = pic + "Os dois retângulos têm a mesma área (%d quadradinhos). Os perímetros também são iguais?" % A
    else:
        q = "Um retângulo mede %d cm por %d cm e outro mede %d cm por %d cm. Os dois têm %d cm² de área. Os perímetros também são iguais?" % (w1, h1, w2, h2, A)
    big = "o primeiro" if p1 > p2 else "o segundo"
    return mcq(q, "Não: %d cm e %d cm" % (p1, p2), ["Sim: os dois têm %d cm" % p1, "Sim: área igual dá perímetro igual", "Não: %d cm e %d cm" % (A, A + 2)],
               "Perímetros: 2 × (%d + %d) = %d e 2 × (%d + %d) = %d. Mesma área nem sempre quer dizer mesmo perímetro. <b>Não</b>; %s tem o perímetro maior." % (w1, h1, p1, w2, h2, p2, big))


def s3_mesmo_per():
    P = R.choice([16, 20, 24, 28])
    half = P // 2
    pares = [(w, half - w) for w in range(1, half) if w <= half - w]
    (w1, h1), (w2, h2) = R.sample(pares, 2)
    a1, a2 = w1 * h1, w2 * h2
    k = R.choice(["maior", "iguais"])
    if k == "iguais":
        return mcq("Dois retângulos têm o mesmo perímetro, %d cm: um mede %d cm por %d cm e o outro mede %d cm por %d cm. As áreas são iguais?" % (P, w1, h1, w2, h2),
                   "Não: %d cm² e %d cm²" % (a1, a2), ["Sim: %d cm²" % a1, "Sim: perímetro igual dá área igual", "Não: %d cm² e %d cm²" % (P, P * 2)],
                   "Áreas: %d × %d = %d e %d × %d = %d. Mesmo perímetro nem sempre quer dizer mesma área. <b>Não</b>." % (w1, h1, a1, w2, h2, a2))
    sq = half // 2 if half % 2 == 0 else None
    if not sq:
        return None
    return mcq("Com %d m de cerca, que cercado retangular tem a <b>maior</b> área?" % P, "%d m por %d m" % (sq, sq),
               ["%d m por %d m" % (w, h) for w, h in pares if (w, h) != (sq, sq)][:3],
               "Perímetro %d m: o lado e a largura somam %d m. A maior área é a do quadrado: %d × %d = <b>%d m²</b>." % (P, half, sq, sq, sq * sq))


def s4_composta():
    a, b = R.randint(5, 12), R.randint(4, 10)
    c, d = R.randint(2, a - 2), R.randint(2, b - 2)
    A = a * b - c * d
    P = 2 * (a + b)
    k = R.choice(["area", "per"])
    s = 14.0 * min(1, 16.0 / max(a, b))
    W, Hh = a * s, b * s
    x0, y0 = 30, 20
    pts = [(x0, y0), (x0 + W - c * s, y0), (x0 + W - c * s, y0 + d * s), (x0 + W, y0 + d * s), (x0 + W, y0 + Hh), (x0, y0 + Hh)]
    body = "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.4'/>" % (" ".join("%.1f,%.1f" % p for p in pts), R.choice(COLS), INK)
    body += text(x0 + W / 2, y0 + Hh + 18, "%d cm" % a, 14) + text(x0 - 6, y0 + Hh / 2, "%d cm" % b, 14, anchor="end")
    body += text(x0 + W - c * s / 2, y0 + d * s - 6, "%d cm" % c, 13) + text(x0 + W - c * s + 4, y0 + d * s / 2 + 4, "%d cm" % d, 13, anchor="start")
    pic = wrap(int(x0 + W + 60), int(y0 + Hh + 30), body, "figura em forma de L com medidas", lg=True)
    if k == "area":
        return mcq(pic + "A figura é um retângulo de %d cm por %d cm sem um canto de %d cm por %d cm. Qual é a área?" % (a, b, c, d), "%d cm²" % A,
                   ["%d cm²" % x for x in (a * b, a * b + c * d, P, A + c)], "%d × %d − %d × %d = %d − %d = <b>%d cm²</b>." % (a, b, c, d, a * b, c * d, A))
    return mcq(pic + "A figura é um retângulo de %d cm por %d cm sem um canto de %d cm por %d cm. Qual é o perímetro?" % (a, b, c, d), "%d cm" % P,
               ["%d cm" % x for x in (P - c - d, P + c + d, A, P - 2 * c)], "Os degraus do canto somam o mesmo que os lados que faltam: o perímetro é igual ao do retângulo, 2 × (%d + %d) = <b>%d cm</b>." % (a, b, P))


def s4_unidade():
    q, a, w = R.choice([("Que unidade é melhor para medir a área de uma sala de aula?", "m²", ["cm²", "km²", "m"]),
                        ("Que unidade é melhor para medir a área de uma folha de caderno?", "cm²", ["m²", "km²", "cm"]),
                        ("Que unidade é melhor para medir a área de uma cidade?", "km²", ["m²", "cm²", "km"]),
                        ("O que mede o perímetro de uma figura?", "o comprimento do contorno", ["a superfície de dentro", "o número de vértices", "a altura"]),
                        ("O que mede a área de uma figura?", "o tamanho da superfície", ["o comprimento do contorno", "o número de lados", "a altura"]),
                        ("Para saber quanto de rodapé colocar numa sala, calculamos…", "o perímetro", ["a área", "o volume", "a massa"]),
                        ("Para saber quanto piso colocar numa sala, calculamos…", "a área", ["o perímetro", "o volume", "a altura"]),
                        ("Para cercar uma horta com tela, precisamos saber…", "o perímetro", ["a área", "o volume", "a temperatura"]),
                        ("Para pintar uma parede, precisamos saber…", "a área", ["o perímetro", "o volume", "o peso"]),
                        ("1 m² é a área de um quadrado de…", "1 m de lado", ["1 cm de lado", "10 m de lado", "4 m de lado"])])
    return mcq(q, a, w, "Perímetro é o contorno (cm, m); área é a superfície (cm², m², km²). Resposta: <b>%s</b>." % a)


def s5_problema():
    k = R.choice(["piso", "cerca", "pintar", "terreno", "jardim", "tapete"])
    p, g = K.next()
    if k == "piso":
        a, b = R.randint(3, 8), R.randint(3, 6)
        pr = R.randint(3, 9) * 1000
        return mcq("Uma sala mede %d m por %d m. O piso custa %s o metro quadrado. Quanto custa o piso da sala?" % (a, b, reais(pr)), reais(a * b * pr),
                   [reais(x) for x in (2 * (a + b) * pr, (a + b) * pr, a * b * pr + pr)], "Área: %d × %d = %d m². %d × %s = <b>%s</b>." % (a, b, a * b, a * b, reais(pr), reais(a * b * pr)))
    if k == "cerca":
        a, b = R.randint(8, 30), R.randint(5, 20)
        return mcq("Um terreno retangular mede %d m por %d m. Quantos metros de cerca são necessários para contorná-lo?" % (a, b), "%d m" % (2 * (a + b)),
                   ["%s m" % num(x) for x in (a * b, a + b, 2 * a + b)], "Perímetro: 2 × (%d + %d) = <b>%d m</b>." % (a, b, 2 * (a + b)))
    if k == "pintar":
        a, b = R.randint(3, 6), R.randint(2, 3)
        lata = R.choice([6, 8, 10, 12])
        A = a * b
        n = -(-A // lata)
        return mcq("Uma parede mede %d m por %d m. Uma lata de tinta pinta %d m². Quantas latas são necessárias?" % (a, b, lata, ), str(n),
                   [str(x) for x in (A // lata if A // lata != n else n + 1, A, n + 1 if n + 1 != A // lata else n + 2, 2 * (a + b) // lata or 1)],
                   "Área: %d × %d = %d m². %d ÷ %d = %d e resto %d → <b>%d latas</b>." % (a, b, A, A, lata, A // lata, A % lata, n) if A % lata else
                   "Área: %d × %d = %d m². %d ÷ %d = <b>%d latas</b>." % (a, b, A, A, lata, n))
    if k == "terreno":
        a = R.randint(10, 30)
        A = a * R.randint(10, 40)
        b = A // a
        return mcq("Um terreno retangular tem %s m² de área e %d m de frente. Quanto mede o fundo (o outro lado)?" % (num(A), a), "%d m" % b,
                   ["%d m" % x for x in (A - a, A // 2 - a, b + a)], "%s ÷ %d = <b>%d m</b>." % (num(A), a, b))
    if k == "jardim":
        L = R.randint(4, 12)
        return mcq("%s fez um jardim quadrado com %d m de lado. Qual é a área do jardim?" % (p, L), "%d m²" % (L * L), ["%d m²" % x for x in (4 * L, 2 * L, L * L + L)],
                   "%d × %d = <b>%d m²</b>." % (L, L, L * L))
    a, b = R.randint(2, 5), R.randint(2, 5)
    q, h = R.randint(2, 4), R.randint(2, 4)
    if a * b == q * h:
        return None
    big = "o primeiro" if a * b > q * h else "o segundo"
    return mcq("Um tapete mede %d m por %d m e outro mede %d m por %d m. Qual tapete cobre mais chão?" % (a, b, q, h), big,
               ["o segundo" if big == "o primeiro" else "o primeiro", "cobrem o mesmo", "o que tiver maior perímetro"],
               "Áreas: %d × %d = %d m² e %d × %d = %d m². Cobre mais <b>%s</b>." % (a, b, a * b, q, h, q * h, big))


def main():
    seen = set()
    sets = [
        ("Perímetro e área", mix(R, seen, [(s1_malha, 10), (s1_ret, 10)])),
        ("O quadrado", mix(R, seen, [(s2_quadrado, 20)])),
        ("Mesma área, mesmo perímetro?", mix(R, seen, [(s3_mesma_area, 12), (s3_mesmo_per, 8)])),
        ("Figuras compostas e unidades", mix(R, seen, [(s4_composta, 12), (s4_unidade, 8)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["O <b>perímetro</b> é a medida do contorno: some todos os lados (cm, m).",
         "A <b>área</b> é a medida da superfície: quantos quadradinhos de 1 cm² (ou 1 m²) cabem dentro.",
         "No retângulo: área = comprimento × largura; perímetro = 2 × (comprimento + largura).",
         "Figuras com a mesma área podem ter perímetros diferentes, e figuras com o mesmo perímetro podem ter áreas diferentes."],
        [("Retângulo de 6 cm por 4 cm.", ["perímetro: 6 + 4 + 6 + 4 = 20 cm", "área: 6 × 4 = 24 cm²"], "20 cm e 24 cm²"),
         ("Retângulos de 1 × 12 e de 3 × 4.", ["os dois têm área 12", "perímetros: 26 e 14"], "mesma área, perímetros diferentes")],
        [["Confundir área e perímetro", "Contorno → perímetro (cm). Superfície → área (cm²)."],
         ["Somar só dois lados: 6 + 4 = 10 cm", "O retângulo tem 4 lados: 6 + 4 + 6 + 4."],
         ["Esquecer o «²» na área", "Área se mede em unidades quadradas: cm², m²."]],
        malha([(rect(6, 2), 1, 1), (rect(4, 3), 8, 1)], 13, 5))
    faq = [("O que o 5º ano aprende sobre área e perímetro?", "A BNCC pede concluir, por meio de investigações, que figuras de perímetros iguais podem ter áreas diferentes e que figuras de mesma área podem ter perímetros diferentes."),
           ("Por que a área usa cm²?", "Porque medimos quantos quadrados de 1 cm de lado cabem na figura. O «²» lembra que é uma medida de superfície.")]
    make_unit(R, "perimetro-e-area", "M", ["EF05MA20"],
              "Concluir, por meio de investigações, que figuras de perímetros iguais podem ter áreas diferentes e que, também, figuras que têm a mesma área podem ter perímetros diferentes",
              "Perímetro e área: retângulos, quadrados e figuras compostas", "Perímetro e área",
              "Atividades de matemática para o 5º ano sobre perímetro e área: malha quadriculada, retângulo e quadrado, cm² e m², mesma área com perímetros diferentes, figuras compostas e problemas. 100 exercícios com gabarito.",
              "Perímetro: contorno. Área: superfície (cm²).", "Mesma área não quer dizer mesmo perímetro.",
              body, faq, sets, 19, grade="5-ano")


if __name__ == "__main__":
    main()
