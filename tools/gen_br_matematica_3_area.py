# -*- coding: utf-8 -*-
"""
Brasil Matemática 3º ano: Comparar áreas (Grandezas e medidas, EF03MA21)
  python3 tools/gen_br_matematica_3_area.py
Área como o espaço ocupado por uma superfície; contar quadradinhos na malha; comparar áreas de figuras diferentes;
figuras diferentes com a mesma área; meio quadradinho; área e contorno não são a mesma coisa; superposição.
Erros: contar os lados em vez dos quadradinhos, achar que a figura mais comprida tem mais área, esquecer as metades.
"""
import random
from br_common import mcq, lesson, make_unit, mix, wrap, line, text, INK, GREEN, FILL, Kids

R = random.Random(80318)
K = Kids(R)
C = 20


def grid(polys, W, H, labels=None, halves=()):
    s = []
    for x in range(W + 1):
        s.append(line(6 + x * C, 6, 6 + x * C, 6 + H * C, "#d0dbe6", 1))
    for y in range(H + 1):
        s.append(line(6, 6 + y * C, 6 + W * C, 6 + y * C, "#d0dbe6", 1))
    cols = [FILL, "#f6d6a8", "#c9dcf2", "#f2c6d0"]
    for i, cells in enumerate(polys):
        for x, y in cells:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1'/>" % (6 + x * C, 6 + y * C, C, C, cols[i % 4], GREEN))
        if labels:
            cx = sum(x for x, _ in cells) / float(len(cells))
            cy = min(y for _, y in cells)
            s.append(text(6 + (cx + 0.5) * C, 6 + cy * C - 4, labels[i], 13, col=INK))
    for x, y, d in halves:
        pts = {"tl": "%d,%d %d,%d %d,%d" % (x, y, x + 1, y, x, y + 1), "br": "%d,%d %d,%d %d,%d" % (x + 1, y, x + 1, y + 1, x, y + 1)}[d]
        pts = " ".join("%d,%d" % (6 + int(a) * C, 6 + int(b) * C) for a, b in (p.split(",") for p in pts.split()))
        s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='1'/>" % (pts, FILL, GREEN))
    return wrap(W * C + 12, H * C + 12, "".join(s), "figuras na malha quadriculada", lg=True)


def blob(n, w, h):
    """n quadradinhos ligados dentro de w × h"""
    cells = {(R.randrange(w), R.randrange(h))}
    while len(cells) < n:
        x, y = R.choice(sorted(cells))
        dx, dy = R.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h:
            cells.add((nx, ny))
    return sorted(cells)


def perim(cells):
    S = set(cells)
    return sum(1 for x, y in cells for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (x + dx, y + dy) not in S)


def s1_contar():
    n = R.randint(5, 14)
    cells = [(x + 1, y + 1) for x, y in blob(n, 6, 4)]
    p = perim(cells)
    return mcq(grid([cells], 8, 6) + "Quantos quadradinhos ocupa a figura pintada?", "%d quadradinhos" % n,
               ["%d quadradinhos" % p if p != n else "%d quadradinhos" % (n + 2), "%d quadradinhos" % (n + 1), "%d quadradinhos" % (n - 1)],
               "Conte os quadradinhos pintados, um por um: <b>%d quadradinhos</b>. Essa é a área da figura." % n)


def s1_retangulo():
    w, h = R.randint(2, 6), R.randint(2, 4)
    cells = [(x + 1, y + 1) for x in range(w) for y in range(h)]
    return mcq(grid([cells], w + 2, h + 2) + "Quantos quadradinhos tem este retângulo?", str(w * h), [str(2 * (w + h)), str(w + h), str(w * h + w)],
               "São %d fileiras com %d quadradinhos: %d × %d = <b>%d</b>." % (h, w, h, w, w * h))


def s2_comparar():
    a, b = R.sample(range(5, 13), 2)
    ca = [(x + 1, y + 1) for x, y in blob(a, 4, 4)]
    cb = [(x + 7, y + 1) for x, y in blob(b, 4, 4)]
    big = "A" if a > b else "B"
    ask = R.choice(["maior", "menor"])
    ans = big if ask == "maior" else ("B" if big == "A" else "A")
    return mcq(grid([ca, cb], 12, 6, ["A", "B"]) + "Qual figura tem a %s área?" % ask, "a figura %s" % ans, ["a figura %s" % ("B" if ans == "A" else "A"), "as duas têm a mesma área", "não dá para saber"],
               "A tem %d quadradinhos e B tem %d: <b>a figura %s</b> tem a %s área." % (a, b, ans, ask))


def s2_mesma():
    n = R.randint(6, 10)
    ca = [(x + 1, y + 1) for x, y in blob(n, 4, 4)]
    cb = [(x + 7, y + 1) for x, y in blob(n, 4, 4)]
    if sorted((x - 6, y) for x, y in cb) == sorted(ca):
        return None
    pa, pb = perim(ca), perim(cb)
    return mcq(grid([ca, cb], 12, 6, ["A", "B"]) + "As figuras A e B têm formas diferentes. O que se pode dizer das áreas?", "têm a mesma área",
               ["A tem área maior", "B tem área maior", "não dá para comparar figuras diferentes"],
               "As duas têm %d quadradinhos: <b>têm a mesma área</b>, mesmo com formas diferentes." % n)


def s3_metade():
    w, h = R.randint(2, 4), R.randint(2, 3)
    cells = [(x + 1, y + 1) for x in range(w) for y in range(h)]
    k = R.randint(1, 2)
    halves = [(w + 1, y + 1, "tl") for y in range(2 * k)]
    tot = w * h + len(halves) // 2
    return mcq(grid([cells], w + 3, max(h, len(halves)) + 2, halves=halves) + "Cada triângulo pintado é meio quadradinho. Qual é a área da figura em quadradinhos?",
               "%d quadradinhos" % tot, ["%d quadradinhos" % (w * h + len(halves)), "%d quadradinhos" % (w * h), "%d quadradinhos" % (tot + 1)],
               "%d quadradinhos inteiros e %d metades; %d metades formam %d %s: <b>%d quadradinhos</b>." % (w * h, len(halves), len(halves), len(halves) // 2,
                                                                                                         "quadradinho" if len(halves) == 2 else "quadradinhos", tot))


QUIZ = [("Para saber qual de dois tapetes ocupa mais espaço no chão, comparamos…", "as áreas", ["os contornos", "as cores", "as alturas"]),
        ("Uma folha de caderno é colocada por cima de um livro e cobre todo o livro, sobrando papel. O que podemos dizer?", "a folha tem área maior", ["o livro tem área maior", "as áreas são iguais", "não dá para saber"]),
        ("Duas figuras têm 8 quadradinhos cada uma, mas formatos diferentes. As áreas são…", "iguais", ["diferentes", "a mais comprida é maior", "a mais alta é maior"]),
        ("Área é…", "o espaço que uma superfície ocupa", ["o tamanho do contorno", "a altura de uma figura", "o número de lados"]),
        ("Para cobrir o chão com lajotas quadradas, o que precisamos contar?", "quantas lajotas cabem (a área)", ["quantos lados tem o chão", "o contorno do chão", "a altura da parede"]),
        ("Uma figura comprida e fina e uma figura curta e larga podem ter a mesma área?", "sim, se ocuparem o mesmo número de quadradinhos", ["não, a comprida é sempre maior", "não, a larga é sempre maior", "só se forem quadrados"]),
        ("Um quadrado de 3 × 3 quadradinhos e um retângulo de 2 × 4 quadradinhos: qual tem área maior?", "o quadrado (9 quadradinhos)", ["o retângulo (8 quadradinhos)", "têm a mesma área", "o retângulo, porque é mais comprido"]),
        ("Um retângulo de 2 × 6 e outro de 3 × 4 quadradinhos: o que se pode dizer das áreas?", "são iguais (12 quadradinhos)", ["a do 2 × 6 é maior", "a do 3 × 4 é maior", "não dá para comparar"])]


def s4_quiz():
    q, a, w = R.choice(QUIZ)
    return mcq(q, a, w, "Resposta: <b>%s</b>." % a)


def s4_ret():
    a, b = R.sample([(2, 6), (3, 4), (2, 5), (3, 3), (4, 4), (2, 8), (4, 3), (5, 2), (3, 5), (2, 7)], 2)
    A, B = a[0] * a[1], b[0] * b[1]
    if A == B:
        ans = "têm a mesma área"
    else:
        ans = "o de %d × %d" % (a if A > B else b)
    return mcq("Qual retângulo tem área maior: um de %d × %d quadradinhos ou um de %d × %d quadradinhos?" % (a + b), ans,
               [x for x in ["o de %d × %d" % a, "o de %d × %d" % b, "têm a mesma área", "não dá para saber"] if x != ans],
               "%d × %d = %d e %d × %d = %d: <b>%s</b>." % (a + (A,) + b + (B, ans)))


def s5_problema():
    p, g = K.next()
    k = R.choice(["piso", "jardim", "mural", "toalha", "azulejo"])
    if k == "piso":
        w, h = R.randint(3, 8), R.randint(3, 6)
        return mcq("O piso de um quarto é coberto por %d fileiras de %d lajotas quadradas. Quantas lajotas há?" % (h, w), str(w * h), [str(w + h), str(2 * (w + h)), str(w * h + h)],
                   "%d × %d = <b>%d</b> lajotas." % (h, w, w * h))
    if k == "jardim":
        a, b = R.randint(8, 15), R.randint(8, 15)
        if a == b:
            return None
        (p2, _) = K.next()
        win = p if a > b else p2
        return mcq("%s plantou flores num canteiro de %d quadradinhos e %s num canteiro de %d quadradinhos. Quem tem o canteiro de maior área?" % (p, a, p2, b), win,
                   [p2 if win == p else p, "os dois canteiros têm a mesma área", "quem tem mais flores"],
                   "%d %s %d: <b>%s</b>." % (a, "&gt;" if a > b else "&lt;", b, win))
    if k == "mural":
        n = R.randint(4, 8)
        m = R.randint(3, 6)
        return mcq("Um mural é coberto com %d fileiras de %d folhas iguais. Faltam 5 folhas para completar. Quantas folhas já estão no mural?" % (m, n), str(m * n - 5),
                   [str(m * n), str(m * n + 5), str(m + n - 5)], "%d × %d = %d; %d − 5 = <b>%d</b>." % (m, n, m * n, m * n, m * n - 5))
    if k == "toalha":
        w, h = R.randint(3, 6), R.randint(3, 6)
        if w * h % 2:
            return None
        return mcq("Uma toalha xadrez tem %d quadrados numa fileira e %d fileiras. Metade dos quadrados é branca. Quantos quadrados são brancos?" % (w, h),
                   str(w * h // 2), [str(w * h), str(w + h), str(w * h // 2 + 1)], "%d × %d = %d; metade: <b>%d</b>." % (w, h, w * h, w * h // 2))
    w, h = R.randint(4, 9), R.randint(3, 6)
    return mcq("Uma parede tem %d fileiras de %d azulejos. %s pintou uma fileira inteira. Quantos azulejos %s pintou?" % (h, w, p, g), str(w),
               [str(h), str(w * h), str(w + h)], "Uma fileira tem <b>%d</b> azulejos." % w)


def main():
    seen = set()
    sets = [
        ("Contar quadradinhos", mix(R, seen, [(s1_contar, 12), (s1_retangulo, 8)])),
        ("Comparar áreas na malha", mix(R, seen, [(s2_comparar, 14), (s2_mesma, 6)])),
        ("Meio quadradinho e mesma área", mix(R, seen, [(s3_metade, 6), (s2_mesma, 6), (s1_contar, 8)])),
        ("O que é área?", mix(R, seen, [(s4_quiz, 8), (s4_ret, 12)])),
        ("Problemas de área", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["A <b>área</b> é o espaço que uma superfície ocupa. Na malha quadriculada, medimos a área contando os <b>quadradinhos</b>.",
         "Para comparar áreas, conte os quadradinhos de cada figura, ou coloque uma figura por cima da outra (superposição).",
         "Figuras de formas diferentes podem ter a <b>mesma área</b>: um retângulo 2 × 6 e um 3 × 4 têm 12 quadradinhos.",
         "Dois meios quadradinhos formam um quadradinho inteiro."],
        [("Retângulo com 3 fileiras de 5 quadradinhos", ["3 × 5"], "15 quadradinhos"),
         ("Qual é maior: 3 × 3 ou 2 × 4?", ["9 e 8"], "3 × 3")],
        [["Contar os lados do contorno", "Área é o que está dentro: conte os quadradinhos pintados."],
         ["Achar que a figura mais comprida tem mais área", "Conte: comprido não quer dizer maior área."],
         ["Contar cada meio quadradinho como 1", "Dois meios formam 1 quadradinho."]])
    faq = [("O que a BNCC pede sobre área no 3º ano?", "Comparar, visualmente ou por superposição, áreas de faces de objetos, de figuras planas ou de desenhos. O cálculo com unidades como cm² vem depois."),
           ("Como explicar área para crianças?", "Use papel quadriculado: pinte figuras e conte os quadradinhos. Peça para desenhar figuras diferentes com o mesmo número de quadradinhos.")]
    make_unit(R, "area", "M", ["EF03MA21"],
              "Comparar, visualmente ou por superposição, áreas de faces de objetos, de figuras planas ou de desenhos",
              "Comparar áreas na malha quadriculada", "Área",
              "Atividades de matemática para o 3º ano sobre área: contar quadradinhos na malha, comparar áreas, figuras com a mesma área, meio quadradinho e problemas. 100 exercícios com gabarito.",
              "Área: conte os quadradinhos de dentro.", "Formas diferentes podem ter a mesma área.",
              body, faq, sets, 18)


if __name__ == "__main__":
    main()
