# -*- coding: utf-8 -*-
"""
Brasil Matemática 8º ano: Mediatriz, bissetriz e construções geométricas (Geometria, EF08MA15, EF08MA16, EF08MA17)
  python3 tools/gen_br_matematica_8_mediatriz_bissetriz_e_construcoes.py
Mediatriz como lugar dos pontos equidistantes das extremidades de um segmento; bissetriz como lugar dos pontos equidistantes dos
lados de um ângulo; construir ângulos de 90°, 60°, 45° e 30° com régua e compasso; construir o hexágono regular (lado = raio);
aplicações (ponto equidistante de três cidades: circuncentro).
Erros: achar que a mediatriz passa por uma das pontas, dividir o ângulo errado, abrir o compasso com medida errada no hexágono.
"""
import random
from br_common import lesson, mix
from br_9 import M, d, bank, unit

R = random.Random(88013)


def s1_mediatriz():
    k = R.choice(["dist", "meio", "eq"])
    if k == "dist":
        a = R.randint(3, 20)
        return M("P está na mediatriz do segmento AB e PA = %d cm. Quanto mede PB?" % a, "%d cm" % a, ["%d cm" % (2 * a), "%s cm" % d(a / 2) if a % 2 == 0 else "%d cm" % (a + 1), "não dá para saber"],
                 "Todo ponto da mediatriz está à mesma distância de A e de B: <b>PB = %d cm</b>." % a)
    if k == "meio":
        ab = R.randint(4, 30) * 2
        return M("A mediatriz de um segmento AB de %d cm o corta no ponto M. Quanto mede AM?" % ab, "%d cm" % (ab // 2), ["%d cm" % ab, "%d cm" % (ab // 4), "%d cm" % (ab // 2 + 1)], "A mediatriz passa pelo ponto médio: %d ÷ 2 = <b>%d cm</b>." % (ab, ab // 2))
    x = R.randint(2, 15)
    a, b = R.choice([(2, 1), (3, 1), (3, 2), (4, 3), (5, 2)])
    c = (a - b) * x
    e = R.randint(1, 12)
    return M("P está na mediatriz de AB, com PA = %dx + %d e PB = %dx + %d (em cm). Quanto vale x?" % (a, e, b, c + e), d(x), [d(c + e), d(x + 1), d((c + 2 * e) // (a + b)) if (c + 2 * e) % (a + b) == 0 else d(x * 2)],
             "PA = PB: %dx + %d = %dx + %d → %dx = %d → <b>x = %d</b>." % (a, e, b, c + e, a - b, c, x))


def s2_bissetriz():
    k = R.choice(["metade", "inteiro", "dist"])
    if k == "metade":
        a = R.choice(range(30, 171, 2))
        return M("A bissetriz de um ângulo de %d° o divide em dois ângulos de…" % a, "%d°" % (a // 2), ["%d°" % a, "%d°" % (180 - a), "%d°" % (a // 4) if a % 4 == 0 else "%d°" % (a // 2 + 5)], "A bissetriz divide o ângulo ao meio: <b>%d°</b>." % (a // 2))
    if k == "inteiro":
        a = R.randint(10, 85)
        return M("A bissetriz forma, com um dos lados de um ângulo, %d°. Quanto mede o ângulo inteiro?" % a, "%d°" % (2 * a), ["%d°" % a, "%d°" % (180 - a), "%d°" % (90 - a)], "O ângulo é o dobro: <b>%d°</b>." % (2 * a))
    a = R.randint(2, 15)
    return M("Um ponto P da bissetriz de um ângulo está a %d cm de um dos lados. A que distância ele está do outro lado?" % a, "%d cm" % a, ["%d cm" % (2 * a), "%s cm" % d(a / 2) if a % 2 == 0 else "%d cm" % (a + 1), "depende do ângulo"],
             "Todo ponto da bissetriz está à mesma distância dos dois lados: <b>%d cm</b>." % a)


s3_construcoes = bank(R, [
    ("Para construir um ângulo de 90° com régua e compasso, podemos traçar…", "a mediatriz de um segmento", ["um triângulo equilátero", "a bissetriz de um ângulo de 60°", "um arco qualquer"]),
    ("Para construir um ângulo de 60° com régua e compasso, podemos construir…", "um triângulo equilátero", ["a mediatriz de um segmento", "um quadrado", "a bissetriz de 90°"]),
    ("Para construir um ângulo de 45°, traçamos…", "a bissetriz de um ângulo de 90°", ["a bissetriz de 60°", "a mediatriz de 45 cm", "um triângulo equilátero"]),
    ("Para construir um ângulo de 30°, traçamos…", "a bissetriz de um ângulo de 60°", ["a bissetriz de 90°", "a mediatriz", "um hexágono"]),
    ("Para construir um ângulo de 120°, podemos usar…", "dois ângulos de 60° lado a lado", ["a bissetriz de 60°", "a mediatriz", "dois ângulos de 45°"]),
    ("Para construir um ângulo de 135°, podemos usar…", "90° + 45°", ["60° + 60°", "90° + 30°", "60° + 45°"]),
    ("Na construção da mediatriz de AB, abrimos o compasso com uma medida…", "maior que a metade de AB, igual nos dois arcos", ["menor que a metade de AB", "diferente em cada ponta", "igual a zero"]),
    ("Para construir um hexágono regular inscrito numa circunferência, a abertura do compasso deve ser…", "igual ao raio", ["igual ao diâmetro", "metade do raio", "qualquer uma"]),
    ("Depois de marcar os 6 pontos na circunferência, para obter o hexágono regular devemos…", "ligar os pontos vizinhos", ["ligar cada ponto ao centro", "traçar um diâmetro", "apagar a circunferência"]),
    ("Ligando pontos alternados do hexágono regular inscrito obtemos…", "um triângulo equilátero", ["um quadrado", "um pentágono", "um losango"]),
    ("O ponto que está à mesma distância de três cidades A, B e C fica no encontro das…", "mediatrizes de AB, BC e AC", ["bissetrizes do triângulo", "alturas do triângulo", "medianas"]),
    ("O ponto que está à mesma distância dos três lados de um triângulo fica no encontro das…", "bissetrizes", ["mediatrizes", "alturas", "diagonais"]),
    ("O lugar geométrico dos pontos a 3 cm de um ponto O é…", "uma circunferência de centro O e raio 3 cm", ["uma reta", "um quadrado", "um segmento de 3 cm"]),
    ("A mediatriz de um segmento é…", "a reta perpendicular a ele que passa pelo ponto médio", ["qualquer reta que o corta", "a reta paralela a ele", "o próprio segmento"]),
], "s3_construcoes")


def s4_hexagono():
    r = R.randint(2, 15)
    k = R.choice(["lado", "per", "ang"])
    if k == "lado":
        return M("Um hexágono regular foi construído numa circunferência de raio %d cm. Quanto mede cada lado?" % r, "%d cm" % r, ["%d cm" % (2 * r), "%s cm" % d(r / 2) if r % 2 == 0 else "%d cm" % (r + 1), "%d cm" % (6 * r)],
                     "No hexágono regular inscrito, o lado é igual ao raio: <b>%d cm</b>." % r)
    if k == "per":
        return M("Qual é o perímetro de um hexágono regular inscrito numa circunferência de raio %d cm?" % r, "%d cm" % (6 * r), ["%d cm" % (2 * r), "%d cm" % (12 * r), "%d cm" % (3 * r)], "6 lados iguais ao raio: 6 × %d = <b>%d cm</b>." % (r, 6 * r))
    return M("Cada ângulo central do hexágono regular mede…", "60°", ["120°", "90°", "30°"], "360° ÷ 6 = <b>60°</b>.") if r == 5 else \
        M("Cada ângulo interno do hexágono regular mede…", "120°", ["60°", "90°", "135°"], "180° − 60° = <b>120°</b>.") if r == 6 else None


def main():
    seen = set()
    sets = [
        ("Mediatriz", mix(R, seen, [(s1_mediatriz, 20)])),
        ("Bissetriz", mix(R, seen, [(s2_bissetriz, 20)])),
        ("Construir ângulos", mix(R, seen, [(s3_construcoes, 8), (s2_bissetriz, 6), (s1_mediatriz, 6)])),
        ("Hexágono regular", mix(R, seen, [(s4_hexagono, 14), (s3_construcoes, 6)])),
        ("Lugares geométricos", mix(R, seen, [(s1_mediatriz, 10), (s2_bissetriz, 10)])),
    ]
    body = lesson(
        ["A <b>mediatriz</b> de AB é a reta perpendicular a AB pelo ponto médio. Cada ponto dela está à mesma distância de A e de B.",
         "A <b>bissetriz</b> de um ângulo divide-o ao meio. Cada ponto dela está à mesma distância dos dois lados do ângulo.",
         "Com régua e compasso: 90° (mediatriz), 60° (triângulo equilátero), 45° e 30° (bissetrizes de 90° e de 60°).",
         "Hexágono regular: trace uma circunferência e, com o compasso aberto no raio, marque 6 pontos; ligue os vizinhos."],
        [("PA = 2x + 3 e PB = x + 8, P na mediatriz", ["2x + 3 = x + 8"], "x = 5"),
         ("Bissetriz de 130°", ["130 ÷ 2"], "65° de cada lado")],
        [["Achar que a mediatriz passa por A", "Ela passa pelo ponto médio."],
         ["Errar a metade do ângulo", "A bissetriz divide exatamente ao meio."],
         ["Abrir o compasso com o diâmetro", "No hexágono, o lado é o raio."]])
    faq = [("O que é a mediatriz de um segmento?", "É a reta perpendicular ao segmento que passa pelo seu ponto médio. Todos os seus pontos estão à mesma distância das extremidades do segmento."),
           ("O que a BNCC pede no 8º ano?", "Construir mediatriz, bissetriz, ângulos de 90°, 60°, 45° e 30° e polígonos regulares (EF08MA15), descrever um algoritmo para a construção de um hexágono regular (EF08MA16) e aplicar os conhecimentos sobre a mediatriz e a bissetriz como lugares geométricos (EF08MA17).")]
    unit(R, "mediatriz-bissetriz-e-construcoes", "G", ["EF08MA15", "EF08MA16", "EF08MA17"],
         "Construir, utilizando instrumentos de desenho ou softwares de geometria dinâmica, mediatriz, bissetriz, ângulos de 90°, 60°, 45° e 30° e polígonos regulares; descrever, por escrito e por meio de um fluxograma, um algoritmo para a construção de um hexágono regular de qualquer área, a partir da medida do ângulo central e da utilização de esquadros e compasso; aplicar os conhecimentos geométricos de lugar geométrico na resolução de problemas",
         "Mediatriz, bissetriz e construções", "Mediatriz e bissetriz",
         "Atividades de matemática para o 8º ano sobre mediatriz, bissetriz e construções com régua e compasso: lugares geométricos, ângulos de 90°, 60°, 45° e 30° e o hexágono regular. 100 exercícios com gabarito.",
         "Mediatriz: mesma distância de A e B.", "Bissetriz: mesma distância dos lados.",
         body, faq, sets, 13, grade="8-ano")


if __name__ == "__main__":
    main()
