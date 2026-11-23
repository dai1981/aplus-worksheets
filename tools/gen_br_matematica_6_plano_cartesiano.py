# -*- coding: utf-8 -*-
"""
Brasil Matemática 6º ano: Plano cartesiano (Geometria, EF06MA16)
  python3 tools/gen_br_matematica_6_plano_cartesiano.py
Pares ordenados (x, y) no 1º quadrante; ler as coordenadas de um ponto; localizar pontos; vértices de polígonos; deslocamentos
(direita/esquerda, cima/baixo); lados horizontais e verticais e perímetro de retângulos com vértices no plano.
Erros: trocar a ordem (y, x), contar os quadradinhos a partir de 1, confundir abscissa e ordenada.
"""
import random
from br_common import lesson, mix
from br_9 import M, bank, kosy, unit

R = random.Random(86012)


def P(x, y):
    return "(%d, %d)" % (x, y)


def pts(n):
    out = set()
    while len(out) < n:
        out.add((R.randint(1, 8), R.randint(1, 8)))
    return sorted(out)


def s1_ler():
    ps = pts(3)
    nm = "ABC"
    i = R.randrange(3)
    x, y = ps[i]
    pic = kosy(pts=[(a, b, n) for (a, b), n in zip(ps, nm)], lo=0, hi=9)
    return M(pic + "Quais são as coordenadas do ponto %s?" % nm[i], P(x, y), [P(y, x) if x != y else P(x + 1, y), P(x + 1, y), P(x, y - 1) if y > 1 else P(x, y + 1)],
             "Primeiro o x (ande %d para a direita), depois o y (suba %d): <b>%s</b>." % (x, y, P(x, y)))


def s2_qual():
    ps = pts(4)
    nm = "ABCD"
    i = R.randrange(4)
    x, y = ps[i]
    pic = kosy(pts=[(a, b, n) for (a, b), n in zip(ps, nm)], lo=0, hi=9)
    return M(pic + "Qual ponto tem coordenadas %s?" % P(x, y), nm[i], [nm[j] for j in range(4) if j != i], "x = %d e y = %d: é o ponto <b>%s</b>." % (x, y, nm[i]))


def s3_mover():
    x, y = R.randint(1, 8), R.randint(1, 8)
    dx, dy = R.choice([-3, -2, -1, 1, 2, 3]), R.choice([-3, -2, -1, 1, 2, 3])
    if not (0 <= x + dx <= 9 and 0 <= y + dy <= 9):
        return None
    t = "%d para a %s e %d para %s" % (abs(dx), "direita" if dx > 0 else "esquerda", abs(dy), "cima" if dy > 0 else "baixo")
    return M("O ponto P%s se desloca %s. Onde ele chega?" % (P(x, y), t), P(x + dx, y + dy), [P(x + dy, y + dx) if dx != dy else P(x - dx, y + dy), P(x - dx, y - dy) if (x - dx >= 0 and y - dy >= 0) else P(x + dx + 1, y + dy), P(x + dx, y - dy) if y - dy >= 0 else P(x + dx, y + dy + 1)],
             "Direita/esquerda muda o x; cima/baixo muda o y: <b>%s</b>." % P(x + dx, y + dy))


def s4_poligono():
    x, y = R.randint(1, 4), R.randint(1, 4)
    w, h = R.randint(2, 5), R.randint(2, 4)
    k = R.choice(["vertice", "perim", "area"])
    V = [(x, y, "A"), (x + w, y, "B"), (x + w, y + h, "C"), (x, y + h, "D")]
    if k == "vertice":
        return M("ABCD é um retângulo com A%s, B%s e C%s. Quais são as coordenadas de D?" % (P(x, y), P(x + w, y), P(x + w, y + h)), P(x, y + h), [P(x + h, y), P(x + w, y + h + 1), P(y + h, x)],
                 "D fica acima de A e na mesma altura de C: <b>%s</b>." % P(x, y + h))
    pic = kosy(pts=V, lo=0, hi=9)
    if k == "perim":
        return M(pic + "ABCD é um retângulo. Qual é o seu perímetro (cada quadradinho tem lado 1)?", str(2 * (w + h)), [str(w * h), str(w + h), str(2 * (w + h) + 2)], "Lados %d e %d: 2 × (%d + %d) = <b>%d</b>." % (w, h, w, h, 2 * (w + h)))
    return M(pic + "ABCD é um retângulo. Quantos quadradinhos de lado 1 cabem dentro dele?", str(w * h), [str(2 * (w + h)), str(w + h), str((w + 1) * (h + 1))], "%d × %d = <b>%d</b>." % (w, h, w * h))


s5_conceitos = bank(R, [
    ("No par ordenado (5, 2), o primeiro número indica…", "a posição no eixo horizontal (x)", ["a posição no eixo vertical (y)", "a distância até a origem", "o quadrante"]),
    ("O ponto de encontro dos eixos chama-se…", "origem, com coordenadas (0, 0)", ["abscissa", "ordenada", "vértice"]),
    ("Os pontos (3, 4) e (4, 3) são…", "pontos diferentes", ["o mesmo ponto", "pontos na origem", "pontos fora do plano"]),
    ("Um ponto sobre o eixo x tem…", "y = 0", ["x = 0", "x = y", "y = 1"]),
    ("Um ponto sobre o eixo y tem…", "x = 0", ["y = 0", "x = y", "x = 1"]),
    ("Os pontos (2, 5) e (7, 5) estão…", "na mesma linha horizontal", ["na mesma linha vertical", "sobre o eixo x", "na origem"]),
    ("Os pontos (4, 1) e (4, 6) estão…", "na mesma linha vertical", ["na mesma linha horizontal", "sobre o eixo y", "na origem"]),
    ("A distância entre (2, 5) e (7, 5) é…", "5", ["9", "10", "2"]),
    ("O primeiro número do par ordenado também se chama…", "abscissa", ["ordenada", "origem", "quadrante"]),
    ("O segundo número do par ordenado também se chama…", "ordenada", ["abscissa", "origem", "vértice"]),
], "s5_conceitos")


def main():
    seen = set()
    sets = [
        ("Ler coordenadas", mix(R, seen, [(s1_ler, 20)])),
        ("Encontrar o ponto", mix(R, seen, [(s2_qual, 20)])),
        ("Deslocamentos", mix(R, seen, [(s3_mover, 14), (s5_conceitos, 6)])),
        ("Polígonos no plano", mix(R, seen, [(s4_poligono, 20)])),
        ("Revisão", mix(R, seen, [(s5_conceitos, 4), (s1_ler, 8), (s3_mover, 8)])),
    ]
    body = lesson(
        ["O <b>plano cartesiano</b> tem um eixo horizontal (x) e um vertical (y), que se cruzam na origem (0, 0).",
         "Cada ponto é dado por um <b>par ordenado</b> (x, y): primeiro ande x para a direita, depois suba y.",
         "Mover para a direita ou para a esquerda muda o x; para cima ou para baixo muda o y."],
        [("Ponto 3 à direita e 5 acima da origem", ["x = 3", "y = 5"], "(3, 5)"),
         ("(2, 4) movido 3 para a direita", ["x: 2 + 3"], "(5, 4)")],
        [["Trocar a ordem", "(3, 5) e (5, 3) são pontos diferentes."],
         ["Começar a contar do 1", "A origem é o 0."],
         ["Confundir abscissa e ordenada", "Abscissa é x; ordenada é y."]],
        kosy(pts=[(3, 5, "P")], lo=0, hi=9))
    faq = [("Como ler um ponto no plano cartesiano?", "Desça do ponto até o eixo x para ler a primeira coordenada e vá até o eixo y para ler a segunda. Escreva (x, y), nessa ordem."),
           ("O que a BNCC pede no 6º ano?", "Associar pares ordenados de números a pontos do plano cartesiano do 1º quadrante, em situações como a localização dos vértices de um polígono (EF06MA16).")]
    unit(R, "plano-cartesiano", "G", ["EF06MA16"],
         "Associar pares ordenados de números a pontos do plano cartesiano do 1º quadrante, em situações como a localização dos vértices de um polígono",
         "Plano cartesiano: pares ordenados no 1º quadrante", "Plano cartesiano",
         "Atividades de matemática para o 6º ano sobre o plano cartesiano: ler coordenadas, localizar pontos, pares ordenados, deslocamentos e polígonos no 1º quadrante. 100 exercícios com gabarito.",
         "(x, y): primeiro anda, depois sobe.", "A origem é (0, 0).",
         body, faq, sets, 12, grade="6-ano")


if __name__ == "__main__":
    main()
