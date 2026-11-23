# -*- coding: utf-8 -*-
"""
Brasil Matemática 7º ano: Triângulos (Geometria, EF07MA24, EF07MA25, EF07MA26)
  python3 tools/gen_br_matematica_7_triangulos.py
Condição de existência (desigualdade triangular); soma dos ângulos internos (180°); ângulo externo = soma dos dois internos
não adjacentes; triângulos isósceles e equiláteros (ângulos da base); rigidez do triângulo (estruturas); construção com régua e
compasso a partir dos três lados.
Erros: aceitar lados 2, 3 e 6, somar 360°, achar que o ângulo externo é o suplemento do ângulo oposto.
"""
import random
from br_common import lesson, mix
from br_9 import M, bank, formas, tri_pts, unit

R = random.Random(87013)


def s1_existe():
    k = R.choice(["sim", "nao", "intervalo"])
    if k == "intervalo":
        a, b = sorted(R.sample(range(3, 16), 2))
        return M("Dois lados de um triângulo medem %d cm e %d cm. O terceiro lado (número inteiro de cm) pode medir…" % (a, b), "de %d cm a %d cm" % (b - a + 1, a + b - 1), ["de %d cm a %d cm" % (b - a, a + b), "de 1 cm a %d cm" % (a + b), "de %d cm a %d cm" % (b, a + b)],
                 "O terceiro lado fica entre a diferença e a soma: %d &lt; x &lt; %d, então <b>de %d cm a %d cm</b>." % (b - a, a + b, b - a + 1, a + b - 1))
    while True:
        a, b, c = sorted(R.sample(range(2, 20), 3))
        if (a + b > c) == (k == "sim"):
            break
    ans = "sim" if k == "sim" else "não"
    return M("É possível construir um triângulo com lados de %d cm, %d cm e %d cm?" % (a, b, c), ans, ["não" if k == "sim" else "sim", "só se for retângulo", "só com régua e compasso grandes"],
             "Os dois menores somam %d, que é %s %d: <b>%s</b>." % (a + b, "maior que" if a + b > c else "menor ou igual a", c, ans))


def s2_angulos():
    a, b = R.randint(25, 95), R.randint(25, 95)
    c = 180 - a - b
    if c < 10:
        return None
    k = R.choice(["int", "ext", "iso", "eq"])
    if k == "int":
        P = tri_pts(4.0, 3.5, 3.0, 40, 170, 40)
        pic = formas([{"pts": P, "poly": "ABC", "angles": [("B", "A", "C", "%d°" % a), ("C", "A", "B", "%d°" % b), ("A", "B", "C", "x")]}], W=260, H=200, label="triângulo ABC com dois ângulos conhecidos")
        return M(pic + "Os ângulos em B e C medem %d° e %d° (o desenho não está em escala). Quanto mede x?" % (a, b), "%d°" % c, ["%d°" % (360 - a - b), "%d°" % (a + b), "%d°" % (180 - a)],
                 "180 − %d − %d = <b>%d°</b>." % (a, b, c))
    if k == "ext":
        return M("Num triângulo, dois ângulos internos medem %d° e %d°. Quanto mede o ângulo externo junto ao terceiro vértice?" % (a, b), "%d°" % (a + b), ["%d°" % c, "%d°" % (360 - a - b), "%d°" % (180 - a)],
                 "O ângulo externo é a soma dos dois internos não adjacentes: %d + %d = <b>%d°</b>." % (a, b, a + b))
    if k == "iso":
        v = R.choice(range(20, 141, 4))
        return M("Num triângulo isósceles, o ângulo do vértice (entre os lados iguais) mede %d°. Quanto mede cada ângulo da base?" % v, "%d°" % ((180 - v) // 2), ["%d°" % (180 - v), "%d°" % v, "%d°" % ((360 - v) // 2)],
                 "Os ângulos da base são iguais: (180 − %d) ÷ 2 = <b>%d°</b>." % (v, (180 - v) // 2))
    x = R.choice(range(10, 41))
    return M("Os ângulos de um triângulo medem x, 2x e 3x. Quanto vale x?", "30°", ["60°", "45°", "18°"], "x + 2x + 3x = 180 → 6x = 180 → <b>x = 30°</b>.") if x == 10 else \
        M("Os ângulos de um triângulo medem x, x + %d° e x + %d°. Quanto vale x?" % (x, 2 * x), "%d°" % ((180 - 3 * x) // 3), ["%d°" % ((180 - 3 * x) // 3 + x), "%d°" % (60), "%d°" % (180 - 3 * x)],
          "3x + %d = 180 → 3x = %d → <b>x = %d°</b>." % (3 * x, 180 - 3 * x, (180 - 3 * x) // 3)) if (180 - 3 * x) % 3 == 0 and (180 - 3 * x) // 3 > 0 and (180 - 3 * x) // 3 != 60 else None


s3_rigidez = bank(R, [
    ("Por que muitas estruturas (pontes, telhados, portões) usam triângulos?", "porque o triângulo é uma figura rígida", ["porque é mais bonito", "porque tem 4 lados", "porque gasta menos ferro sempre"]),
    ("Um quadrado feito de varetas articuladas pode se deformar. O que o torna rígido?", "colocar uma diagonal, formando triângulos", ["colocar mais um quadrado", "pintá-lo", "aumentar os lados"]),
    ("Com três lados dados (que formam triângulo), quantos triângulos diferentes podemos construir?", "apenas um (a menos da posição)", ["infinitos", "dois", "nenhum"]),
    ("Para construir um triângulo com régua e compasso conhecendo os três lados, depois de traçar um lado, usamos o compasso para…", "traçar arcos com as medidas dos outros dois lados", ["medir os ângulos", "traçar a altura", "dividir o lado ao meio"]),
    ("Num triângulo, ao maior lado se opõe…", "o maior ângulo", ["o menor ângulo", "um ângulo de 90° sempre", "o ângulo do vértice"]),
    ("Um triângulo pode ter dois ângulos obtusos?", "não, a soma passaria de 180°", ["sim", "só se for isósceles", "só se for grande"]),
    ("Cada ângulo de um triângulo equilátero mede…", "60°", ["90°", "45°", "120°"]),
    ("Num triângulo retângulo, os dois ângulos agudos somam…", "90°", ["180°", "60°", "45°"]),
    ("A soma dos três ângulos externos de um triângulo (um em cada vértice) é…", "360°", ["180°", "270°", "540°"]),
], "s3_rigidez")


def main():
    seen = set()
    sets = [
        ("Condição de existência", mix(R, seen, [(s1_existe, 20)])),
        ("Ângulos internos", mix(R, seen, [(s2_angulos, 20)])),
        ("Ângulo externo e isósceles", mix(R, seen, [(s2_angulos, 20)])),
        ("Rigidez e construção", mix(R, seen, [(s3_rigidez, 9), (s1_existe, 11)])),
        ("Revisão", mix(R, seen, [(s2_angulos, 14), (s1_existe, 6)])),
    ]
    body = lesson(
        ["<b>Condição de existência</b>: cada lado precisa ser menor que a soma dos outros dois. Basta conferir o maior lado.",
         "A soma dos ângulos internos de qualquer triângulo é <b>180°</b>.",
         "O <b>ângulo externo</b> é igual à soma dos dois ângulos internos não adjacentes a ele.",
         "O triângulo é uma figura <b>rígida</b>: com os três lados fixos, ele não se deforma. Por isso aparece em pontes e telhados."],
        [("Lados 4, 5 e 10", ["4 + 5 = 9 &lt; 10"], "não forma triângulo"),
         ("Isósceles com vértice de 40°", ["(180 − 40) ÷ 2"], "70° cada ângulo da base")],
        [["Aceitar 2, 3 e 6", "2 + 3 = 5 &lt; 6: não fecha."],
         ["Somar 360°", "No triângulo, 180°."],
         ["Errar o ângulo externo", "Externo = soma dos dois internos do outro lado."]])
    faq = [("Qual é a condição de existência de um triângulo?", "A medida de cada lado deve ser menor que a soma das medidas dos outros dois. Se o maior lado for menor que a soma dos outros dois, o triângulo existe."),
           ("O que a BNCC pede no 7º ano?", "Construir triângulos e reconhecer a condição de existência (EF07MA24), reconhecer a rigidez geométrica dos triângulos e suas aplicações (EF07MA25) e descrever um algoritmo para a construção de um triângulo qualquer, conhecidas as medidas dos três lados (EF07MA26).")]
    unit(R, "triangulos", "G", ["EF07MA24", "EF07MA25", "EF07MA26"],
         "Construir triângulos, usando régua e compasso, reconhecer a condição de existência do triângulo quanto à medida dos lados e verificar que a soma das medidas dos ângulos internos de um triângulo é 180°; reconhecer a rigidez geométrica dos triângulos e suas aplicações; descrever, por escrito e por meio de um fluxograma, um algoritmo para a construção de um triângulo qualquer, conhecidas as medidas dos três lados",
         "Triângulos: existência, ângulos e rigidez", "Triângulos",
         "Atividades de matemática para o 7º ano sobre triângulos: condição de existência, soma dos ângulos internos, ângulo externo, triângulo isósceles, rigidez e construção com régua e compasso. 100 exercícios com gabarito.",
         "Soma dos ângulos internos: 180°.", "Maior lado < soma dos outros dois.",
         body, faq, sets, 13, grade="7-ano")


if __name__ == "__main__":
    main()
