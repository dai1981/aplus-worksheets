# -*- coding: utf-8 -*-
"""
Brasil Matemática 5º ano: Ampliação e redução de figuras (Geometria, EF05MA18)
  python3 tools/gen_br_matematica_5_ampliacao_e_reducao.py
Ampliar e reduzir figuras poligonais em malha quadriculada; lados proporcionais (todos × 2, × 3 ou ÷ 2) e ângulos iguais;
reconhecer a ampliação correta; o perímetro também muda na mesma proporção; fotos, plantas e mapas.
Erros: somar o mesmo número a todos os lados (deforma a figura), ampliar só a largura, achar que os ângulos também dobram.
"""
import random
from br_common import mcq, lesson, make_unit, mix, wrap, line, text, INK, GREEN, Kids

R = random.Random(80517)
K = Kids(R)
C = 16
COLS = ["#cfe6d6", "#f6d6a8", "#c9dcf2", "#f2c6d0"]


def shape():
    k = R.choice(["ret", "L", "T", "tri", "esc"])
    w, h = R.randint(2, 4), R.randint(1, 3)
    if k == "ret":
        return [(0, 0), (w, 0), (w, h), (0, h)]
    if k == "L":
        a, b = R.randint(1, w - 1) if w > 1 else 1, R.randint(1, 2)
        return [(0, 0), (w, 0), (w, a), (b, a), (b, a + 2), (0, a + 2)] if b < w else None
    if k == "T":
        return [(0, 0), (3, 0), (3, 1), (2, 1), (2, 3), (1, 3), (1, 1), (0, 1)]
    if k == "tri":
        return [(0, 0), (w, 0), (0, h + 1)]
    return [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2), (3, 3), (0, 3)]


def scale(p, m):
    return [(x * m, y * m) for x, y in p]


def bbox(p):
    return max(x for x, _ in p), max(y for _, y in p)


def malha(figs, W, H, labels=()):
    s = []
    for i in range(W + 1):
        s.append(line(6 + i * C, 6, 6 + i * C, 6 + H * C, "#c9d6e3", 1))
    for j in range(H + 1):
        s.append(line(6, 6 + j * C, 6 + W * C, 6 + j * C, "#c9d6e3", 1))
    for k, (pts, ox, oy) in enumerate(figs):
        P = " ".join("%d,%d" % (6 + (ox + x) * C, 6 + (H - oy - y) * C) for x, y in pts)
        s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.2'/>" % (P, COLS[k % 4], INK))
    for (x, y, t) in labels:
        s.append(text(6 + x * C, 6 + (H - y) * C, t, 15))
    return wrap(12 + W * C, 12 + H * C, "".join(s), "figuras numa malha quadriculada", lg=True)


def side_len(p):
    """comprimento do lado horizontal de baixo (em quadradinhos)"""
    return p[1][0] - p[0][0]


def s1_lado():
    p = shape()
    if not p:
        return None
    m = R.choice([2, 3])
    w, h = bbox(p)
    q = scale(p, m)
    W = w + 2 + w * m + 1
    H = max(h, h * m) + 2
    pic = malha([(p, 1, 1)], w + 2, h + 2)
    L = side_len(p)
    if L < 2:
        return None
    ans = L * m
    return mcq(pic + "Vamos ampliar esta figura %d vezes (× %d). O lado de baixo tem %d quadradinhos. Quantos quadradinhos ele terá na figura ampliada?" % (m, m, L), str(ans),
               [str(L + m), str(L + 2), str(ans + m), str(L)], "Na ampliação × %d, todos os lados ficam %d vezes maiores: %d × %d = <b>%d</b>." % (m, m, L, m, ans))


def s1_reduzir():
    p = shape()
    if not p:
        return None
    m = 2
    q = scale(p, m)
    w, h = bbox(q)
    pic = malha([(q, 1, 1)], w + 2, h + 2)
    L = side_len(q)
    k = R.choice(["lado", "altura"])
    if k == "altura":
        hh = h
        return mcq(pic + "Esta figura será reduzida à metade (÷ 2). Ela tem %d quadradinhos de altura. Quantos terá depois?" % hh, str(hh // 2),
                   [str(hh - 2), str(hh * 2), str(hh - 1)], "Na redução à metade, todas as medidas ficam divididas por 2: %d ÷ 2 = <b>%d</b>." % (hh, hh // 2))
    return mcq(pic + "Esta figura será reduzida à metade (÷ 2). O lado de baixo tem %d quadradinhos. Quantos terá depois?" % L, str(L // 2),
               [str(L - 2), str(L * 2), str(L - 1)], "%d ÷ 2 = <b>%d</b>." % (L, L // 2))


def s2_qual():
    w, h = R.randint(2, 4), R.randint(1, 3)
    if w == h:
        return None
    m = 2
    good = [(0, 0), (w * m, 0), (w * m, h * m), (0, h * m)]
    bad1 = [(0, 0), (w + 2, 0), (w + 2, h + 2), (0, h + 2)]
    bad2 = [(0, 0), (w * m, 0), (w * m, h), (0, h)]
    bad3 = [(0, 0), (w, 0), (w, h * m), (0, h * m)]
    opts = [("certa", good), ("soma", bad1), ("larg", bad2), ("alt", bad3)]
    if bad1 == good:
        return None
    R.shuffle(opts)
    letters = "ABCD"
    figs, labels, x = [([(0, 0), (w, 0), (w, h), (0, h)], 1, 1)], [(1 + w / 2.0, h + 1.6, "")], w + 3
    H = max(h * m, h + 2) + 4
    for i, (k, pts) in enumerate(opts):
        figs.append((pts, x, 1))
        labels.append((x + bbox(pts)[0] / 2.0, bbox(pts)[1] + 2.2, letters[i]))
        x += bbox(pts)[0] + 2
    pic = malha(figs, x, H, labels)
    ans = letters[[k for k, _ in opts].index("certa")]
    return mcq(pic + "A primeira figura (à esquerda) é um retângulo de %d por %d quadradinhos. Qual das figuras A, B, C ou D é a sua ampliação × 2?" % (w, h), ans,
               [l for l in letters if l != ans], "A ampliação × 2 tem %d por %d quadradinhos (os dois lados dobram): <b>%s</b>." % (w * 2, h * 2, ans))


IDEIAS = [("Quando ampliamos uma figura sem deformar, o que acontece com os ângulos?", "Ficam iguais", ["Dobram", "Ficam menores", "Viram ângulos retos"]),
          ("Quando ampliamos uma figura × 3, o que acontece com cada lado?", "Fica 3 vezes maior", ["Ganha 3 quadradinhos", "Não muda", "Fica 3 vezes menor"]),
          ("Um quadrado ampliado × 2 continua sendo…", "um quadrado", ["um retângulo comprido", "um losango", "um triângulo"]),
          ("Uma figura foi esticada só na largura. Ela é uma ampliação correta?", "Não, ficou deformada", ["Sim, ficou maior", "Sim, porque a altura não mudou", "Só se for colorida"]),
          ("Se um triângulo tem um ângulo reto e é ampliado × 2, o ângulo na figura nova…", "continua reto", ["vira obtuso", "vira agudo", "desaparece"]),
          ("Numa redução à metade, os lados da figura nova…", "medem a metade", ["medem 2 quadradinhos a menos", "medem o dobro", "ficam iguais"]),
          ("Ampliar uma foto sem deformar quer dizer…", "multiplicar a largura e a altura pelo mesmo número", ["somar 2 cm à largura e à altura", "aumentar só a largura", "aumentar só a altura"]),
          ("Ampliamos um retângulo de 3 cm por 2 cm. Qual destas medidas é uma ampliação correta?", "6 cm por 4 cm", ["5 cm por 4 cm", "6 cm por 2 cm", "4 cm por 3 cm"]),
          ("Reduzimos um retângulo de 8 cm por 6 cm à metade. Que medidas ele terá?", "4 cm por 3 cm", ["6 cm por 4 cm", "4 cm por 6 cm", "7 cm por 5 cm"]),
          ("Na ampliação × 2 de uma figura, o contorno (perímetro)…", "também fica 2 vezes maior", ["fica igual", "fica 4 vezes maior", "aumenta 2 cm"])]


def s3_ideia():
    q, a, w = R.choice(IDEIAS)
    return mcq(q, a, w, "Ampliar ou reduzir sem deformar é multiplicar (ou dividir) <b>todos os lados pelo mesmo número</b>; os ângulos não mudam. Resposta: <b>%s</b>." % a)


def s3_medidas():
    a, b = R.randint(2, 9), R.randint(2, 9)
    if a == b:
        return None
    m = R.choice([2, 3, 4])
    good = "%d cm por %d cm" % (a * m, b * m)
    w = ["%d cm por %d cm" % (a + m, b + m), "%d cm por %d cm" % (a * m, b), "%d cm por %d cm" % (a * m, b * m + 1)]
    return mcq("Um retângulo mede %d cm por %d cm. Que medidas tem a ampliação × %d?" % (a, b, m), good, w,
               "Os dois lados são multiplicados por %d: %d × %d = %d e %d × %d = %d. <b>%s</b>." % (m, a, m, a * m, b, m, b * m, good))


def s4_perimetro():
    a, b = R.randint(2, 9), R.randint(2, 9)
    m = R.choice([2, 3])
    P = 2 * (a + b)
    k = R.choice(["per", "fator"])
    if k == "per":
        return mcq("Um retângulo de %d cm por %d cm tem perímetro %d cm. Qual é o perímetro da ampliação × %d?" % (a, b, P, m), "%d cm" % (P * m),
                   ["%d cm" % x for x in (P + m, P * m * m, P + 4 * m, P)], "Todos os lados × %d, então o perímetro também × %d: %d × %d = <b>%d cm</b>." % (m, m, P, m, P * m))
    a2 = a * m
    return mcq("Um lado de %d cm passou a medir %d cm numa ampliação. A ampliação foi de quantas vezes?" % (a, a2), "%d vezes" % m,
               ["%d vezes" % (a2 - a), "%d vezes" % (m + 1), "%d vezes" % a2], "%d ÷ %d = <b>%d</b>: a figura foi ampliada %d vezes." % (a2, a, m, m))


def s5_problema():
    k = R.choice(["foto", "planta", "mapa", "desenho", "maquete"])
    p, g = K.next()
    if k == "foto":
        a, b = R.choice([(10, 15), (9, 13), (13, 18), (15, 21), (5, 7)])
        m = R.choice([2, 3])
        return mcq("%s quer ampliar uma foto de %d cm por %d cm, %d vezes, sem deformar. Que medidas terá a foto ampliada?" % (p, a, b, m), "%d cm por %d cm" % (a * m, b * m),
                   ["%d cm por %d cm" % (a + m, b + m), "%d cm por %d cm" % (a * m, b), "%d cm por %d cm" % (a + 10, b + 10)], "%d × %d e %d × %d: <b>%d cm por %d cm</b>." % (a, m, b, m, a * m, b * m))
    if k == "planta":
        s = R.choice([100, 200, 50])
        c = R.randint(2, 8)
        return mcq("Numa planta de casa, cada 1 cm do desenho representa %d cm de verdade. A sala mede %d cm no desenho. Qual é o comprimento real?" % (s, c), "%d cm" % (c * s),
                   ["%d cm" % x for x in (c + s, s, c * s * 10)], "%d × %d = <b>%d cm</b> (= %s m)." % (c, s, c * s, str(c * s // 100) if c * s % 100 == 0 else str(c * s / 100.0).replace(".", ",")))
    if k == "mapa":
        s = R.choice([2, 5, 10])
        c = R.randint(3, 9)
        return mcq("Num mapa, cada 1 cm representa %d km. Duas cidades estão a %d cm uma da outra no mapa. Qual é a distância real?" % (s, c), "%d km" % (c * s),
                   ["%d km" % x for x in (c + s, c, c * s * 10)], "%d × %d = <b>%d km</b>." % (c, s, c * s))
    if k == "desenho":
        L = R.randint(3, 8)
        m = R.choice([2, 3])
        return mcq("%s desenhou um triângulo com lados de %d, %d e %d quadradinhos. Ampliando × %d, quais serão os lados?" % (p, L, L + 1, L + 2, m),
                   "%d, %d e %d" % (L * m, (L + 1) * m, (L + 2) * m), ["%d, %d e %d" % (L + m, L + 1 + m, L + 2 + m), "%d, %d e %d" % (L * m, L + 1, L + 2), "%d, %d e %d" % (L * m, (L + 1) * m, L + 2)],
                   "Cada lado × %d: <b>%d, %d e %d</b>." % (m, L * m, (L + 1) * m, (L + 2) * m))
    a = R.randint(2, 6) * 10
    return mcq("Uma maquete é uma redução: 1 cm da maquete representa 1 m (100 cm) do prédio. A maquete tem %d cm de altura. Qual é a altura do prédio?" % a, "%d m" % a,
               ["%d cm" % a, "%d m" % (a * 100), "%d m" % (a // 10)], "Cada 1 cm vale 1 m: %d cm na maquete = <b>%d m</b>." % (a, a))


def main():
    seen = set()
    sets = [
        ("Ampliar e reduzir na malha", mix(R, seen, [(s1_lado, 12), (s1_reduzir, 8)])),
        ("Qual é a ampliação certa?", mix(R, seen, [(s2_qual, 20)])),
        ("Lados proporcionais, ângulos iguais", mix(R, seen, [(s3_ideia, 10), (s3_medidas, 10)])),
        ("Perímetro e fator", mix(R, seen, [(s4_perimetro, 20)])),
        ("Fotos, plantas e mapas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["<b>Ampliar</b> uma figura sem deformar é multiplicar <b>todos os lados</b> pelo mesmo número; <b>reduzir</b> é dividir todos os lados pelo mesmo número.",
         "Os <b>ângulos não mudam</b>: um ângulo reto continua reto na figura ampliada.",
         "Na malha quadriculada, conte os quadradinhos de cada lado e multiplique.",
         "Se os lados ficam 2 vezes maiores, o perímetro também fica 2 vezes maior."],
        [("Um retângulo de 3 por 2 quadradinhos é ampliado × 2.", ["3 × 2 = 6", "2 × 2 = 4"], "6 por 4 quadradinhos"),
         ("Uma foto de 10 cm por 15 cm é reduzida à metade.", ["10 ÷ 2 = 5", "15 ÷ 2 = 7,5"], "5 cm por 7,5 cm")],
        [["Somar o mesmo número a todos os lados (3 × 2 → 5 × 4)", "Multiplique: 3 × 2 vira 6 × 4."],
         ["Ampliar só a largura", "A figura fica deformada. Multiplique largura e altura."],
         ["Achar que os ângulos também dobram", "Os ângulos ficam iguais; só os lados mudam."]],
        malha([([(0, 0), (3, 0), (3, 2), (0, 2)], 1, 1), ([(0, 0), (6, 0), (6, 4), (0, 4)], 6, 1)], 13, 6))
    faq = [("O que é ampliação e redução de figuras?", "É desenhar uma figura maior ou menor, multiplicando ou dividindo todos os lados pelo mesmo número, sem mudar os ângulos. A figura nova é semelhante à original."),
           ("Por que usar a malha quadriculada?", "Na malha, as crianças contam os quadradinhos de cada lado e veem que todos os lados mudaram na mesma proporção, enquanto os ângulos continuam iguais.")]
    make_unit(R, "ampliacao-e-reducao", "G", ["EF05MA18"],
              "Reconhecer a congruência dos ângulos e a proporcionalidade entre os lados correspondentes de figuras poligonais em situações de ampliação e de redução em malhas quadriculadas e usando tecnologias digitais",
              "Ampliação e redução de figuras na malha quadriculada", "Ampliação e redução",
              "Atividades de matemática para o 5º ano sobre ampliação e redução de figuras: malha quadriculada, lados proporcionais, ângulos iguais, perímetro, fotos, plantas e mapas. 100 exercícios com gabarito.",
              "Ampliar: todos os lados × o mesmo número.", "Os ângulos não mudam.",
              body, faq, sets, 17, grade="5-ano")


if __name__ == "__main__":
    main()
