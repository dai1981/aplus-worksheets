# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: Polígonos regulares (Geometria, EF09MA15)
  python3 tools/gen_br_matematica_9_poligonos_regulares.py
Ângulo central, interno e externo; soma dos ângulos internos; construção com régua e compasso (circunferência dividida em
arcos iguais); algoritmo «ande e gire» (fluxograma); lados do triângulo, quadrado e hexágono inscritos (r√3, r√2, r); apótema.
Erros: girar o ângulo interno em vez do externo, usar 180° em vez de 360°, achar que todo polígono de lados iguais é regular.
"""
import random
from br_common import lesson, mix
from br_9 import M, d, sq, unit
import br_9

R = random.Random(89015)
NOME = {3: "triângulo equilátero", 4: "quadrado", 5: "pentágono regular", 6: "hexágono regular", 8: "octógono regular", 9: "eneágono regular", 10: "decágono regular", 12: "dodecágono regular", 15: "pentadecágono regular", 18: "polígono regular de 18 lados", 20: "icoságono regular"}
NS = sorted(NOME)


def poly_pic(n):
    import math
    pts = {}
    names = "ABCDEFGHIJKL"
    for i in range(n):
        t = 90 + 360.0 * i / n
        pts[names[i]] = t
    segs = [(names[i], names[(i + 1) % n]) for i in range(n)]
    return br_9.circulo(pts, segs + [("O", "A"), ("O", "B")], arcs=[("O", "A", "B", "x")], label="%s inscrito numa circunferência de centro O" % NOME[n])


def s1_angulos():
    n = R.choice(NS)
    k = R.choice(["central", "interno", "externo", "soma"])
    c = 360 // n if 360 % n == 0 else None
    if c is None:
        return None
    i = 180 - c
    if k == "central":
        return M("Quanto mede o ângulo central de um %s?" % NOME[n], "%d°" % c, ["%d°" % i, "%s°" % d(180 / n if 180 % n == 0 else c * 2), "%d°" % (c * 2) if c * 2 < 180 else "%d°" % (c // 2)],
                 "Ângulo central = 360° ÷ %d = <b>%d°</b>." % (n, c))
    if k == "interno":
        return M("Quanto mede cada ângulo interno de um %s?" % NOME[n], "%d°" % i, ["%d°" % c, "%d°" % ((n - 2) * 180), "%d°" % (360 - c) if n > 3 else "90°", "%d°" % (i - 10)],
                 "Soma = (%d − 2) · 180° = %s°; ÷ %d = <b>%d°</b> (ou 180° − %d°)." % (n, d((n - 2) * 180), n, i, c))
    if k == "externo":
        return M("Quanto mede cada ângulo externo de um %s?" % NOME[n], "%d°" % c, ["%d°" % i, "%d°" % (180 + c), "%d°" % (c // 2) if c % 2 == 0 else "%d°" % (c + 5)],
                 "A soma dos externos é 360°: 360 ÷ %d = <b>%d°</b>." % (n, c))
    return M("Qual é a soma dos ângulos internos de um %s?" % NOME[n], "%s°" % d((n - 2) * 180), ["%s°" % d(n * 180), "%d°" % 360, "%s°" % d((n - 1) * 180), "%s°" % d((n - 2) * 90)],
             "S = (n − 2) · 180° = (%d − 2) · 180° = <b>%s°</b>." % (n, d((n - 2) * 180)))


def s2_inverso():
    n = R.choice([n for n in NS if 360 % n == 0])
    c = 360 // n
    k = R.choice(["int", "ext"])
    if k == "int":
        return M("Cada ângulo interno de um polígono regular mede %d°. Quantos lados ele tem?" % (180 - c), d(n), [d(360 // (180 - c)) if 360 % (180 - c) == 0 and 360 // (180 - c) != n else d(n + 2), d(n - 1), d((180 - c) // 10)],
                 "O externo mede 180° − %d° = %d°; 360 ÷ %d = <b>%d lados</b>." % (180 - c, c, c, n))
    return M("Cada ângulo externo de um polígono regular mede %d°. Quantos lados ele tem?" % c, d(n), [d(180 // c) if 180 % c == 0 and 180 // c != n else d(n + 1), d(c), d(n * 2)],
             "360 ÷ %d = <b>%d lados</b>." % (c, n))


def s3_construcao():
    n = R.choice([3, 4, 5, 6, 8, 9, 10, 12])
    k = R.choice(["fig", "passo", "giro"])
    c = 360 // n
    if k == "fig":
        return M(poly_pic(n) + "Para construir este %s, dividimos a circunferência em arcos iguais. Quanto mede o ângulo central x?" % NOME[n], "%d°" % c, ["%d°" % (180 - c), "%d°" % (c // 2) if c % 2 == 0 else "%d°" % (c + 10), "%d°" % (360 - c)],
                 "360° ÷ %d = <b>%d°</b>." % (n, c))
    if k == "giro":
        return M("Um robô desenha um %s com o algoritmo: «repita %d vezes: ande 10 cm e gire à esquerda». Quantos graus ele deve girar a cada vez?" % (NOME[n], n), "%d°" % c, ["%d°" % (180 - c), "%d°" % 360, "%d°" % (180 // n) if 180 % n == 0 else "%d°" % (c + 5)],
                 "Ele gira o ângulo externo; ao final, deu uma volta completa: 360° ÷ %d = <b>%d°</b>." % (n, c))
    q, a, w = R.choice([
        ("Para construir um hexágono regular inscrito com o compasso, a abertura do compasso deve ser igual…", "ao raio da circunferência", ["ao diâmetro", "à metade do raio", "a qualquer medida"]),
        ("Num algoritmo para construir um polígono regular de n lados inscrito numa circunferência, o primeiro passo depois de traçar a circunferência é…", "dividir 360° por n para achar o ângulo central", ["medir o ângulo interno com 180°", "traçar as diagonais", "dividir o raio por n"]),
        ("Depois de marcar os n pontos na circunferência, o último passo da construção é…", "ligar os pontos vizinhos com a régua", ["apagar a circunferência antes de ligar", "traçar o diâmetro", "medir a área"]),
        ("Um polígono é regular quando…", "tem todos os lados iguais e todos os ângulos iguais", ["tem todos os lados iguais", "tem todos os ângulos iguais", "está dentro de uma circunferência"]),
        ("Um losango que não é quadrado é um polígono regular?", "não, porque os ângulos não são todos iguais", ["sim, porque os lados são iguais", "sim, porque tem 4 lados", "não, porque os lados não são iguais"]),
        ("Num fluxograma para desenhar um polígono regular, o passo «repita n vezes» serve para…", "desenhar os n lados", ["calcular a área", "medir o raio", "contar as diagonais"]),
    ])
    return M(q, a, w, "Resposta: <b>%s</b>." % a)


def s4_inscritos():
    r = R.randint(2, 12)
    k = R.choice(["hex", "quad", "tri", "ap_quad", "ap_hex"])
    if k == "hex":
        return M("Um hexágono regular está inscrito numa circunferência de raio %d cm. Quanto mede o lado?" % r, "%d cm" % r, ["%d cm" % (2 * r), "%d√3 cm" % r, "%d√2 cm" % r],
                 "No hexágono regular, os 6 triângulos centrais são equiláteros: lado = raio = <b>%d cm</b>." % r)
    if k == "quad":
        return M("Um quadrado está inscrito numa circunferência de raio %d cm. Quanto mede o lado?" % r, "%d√2 cm" % r, ["%d cm" % (2 * r), "%d√3 cm" % r, "%d cm" % r],
                 "A diagonal do quadrado é o diâmetro %d: l√2 = %d → l = <b>%d√2 cm</b>." % (2 * r, 2 * r, r))
    if k == "tri":
        return M("Um triângulo equilátero está inscrito numa circunferência de raio %d cm. Quanto mede o lado?" % r, "%d√3 cm" % r, ["%d√2 cm" % r, "%d cm" % (2 * r), "%d cm" % (3 * r)],
                 "No triângulo equilátero inscrito, l = r√3 = <b>%d√3 cm</b>." % r)
    if k == "ap_quad":
        l = 2 * r
        return M("Qual é o apótema (distância do centro ao lado) de um quadrado de lado %d cm?" % l, "%d cm" % r, ["%d cm" % l, "%d√2 cm" % r, "%d cm" % (l * l)],
                 "O apótema do quadrado é metade do lado: <b>%d cm</b>." % r)
    l = 2 * r
    return M("Qual é o apótema de um hexágono regular de lado %d cm?" % l, "%d√3 cm" % r, ["%d cm" % r, "%d√2 cm" % r, "%d√3 cm" % l],
             "O apótema é a altura de um triângulo equilátero de lado %d: %d√3 ÷ 2 = <b>%d√3 cm</b>." % (l, l, r))


def s5_perimetro():
    n = R.choice([5, 6, 8, 10, 12])
    k = R.choice(["per", "lado", "ang"])
    if k == "per":
        l = R.randint(3, 15)
        return M("Qual é o perímetro de um %s de lado %d cm?" % (NOME[n], l), "%d cm" % (n * l), ["%d cm" % (n + l), "%d cm" % (l * l), "%d cm" % ((n - 1) * l)], "%d · %d = <b>%d cm</b>." % (n, l, n * l))
    if k == "lado":
        l = R.randint(3, 15)
        return M("Um %s tem perímetro de %d cm. Quanto mede cada lado?" % (NOME[n], n * l), "%d cm" % l, ["%d cm" % (n * l - n), "%d cm" % (l + 1), "%d cm" % n], "%d ÷ %d = <b>%d cm</b>." % (n * l, n, l))
    m = R.choice([2, 3, 4])
    return M("Ladrilhos em forma de polígono regular se encaixam em volta de um ponto sem sobrar espaço quando os ângulos internos somam 360°. Quantos hexágonos regulares se encaixam em volta de um ponto?" if m == 3 else
             ("Quantos quadrados se encaixam em volta de um ponto, sem sobrar espaço?" if m == 4 else "Quantos triângulos equiláteros se encaixam em volta de um ponto, sem sobrar espaço?"),
             d({3: 3, 4: 4, 2: 6}[m]), [d({3: 3, 4: 4, 2: 6}[m] + 1), d({3: 3, 4: 4, 2: 6}[m] - 1), d(5) if m != 2 else d(8)],
             "Ângulo interno: %d°; 360 ÷ %d = <b>%d</b>." % ({3: 120, 4: 90, 2: 60}[m], {3: 120, 4: 90, 2: 60}[m], {3: 3, 4: 4, 2: 6}[m]))


def main():
    seen = set()
    sets = [
        ("Ângulos de polígonos regulares", mix(R, seen, [(s1_angulos, 20)])),
        ("Quantos lados?", mix(R, seen, [(s2_inverso, 14), (s5_perimetro, 6)])),
        ("Construção e algoritmos", mix(R, seen, [(s3_construcao, 20)])),
        ("Polígonos inscritos", mix(R, seen, [(s4_inscritos, 20)])),
        ("Revisão", mix(R, seen, [(s1_angulos, 8), (s5_perimetro, 6), (s2_inverso, 6)])),
    ]
    body = lesson(
        ["Um <b>polígono regular</b> tem todos os lados e todos os ângulos iguais.",
         "Ângulo central = ângulo externo = 360° ÷ n. Ângulo interno = 180° − ângulo externo. Soma dos internos = (n − 2) · 180°.",
         "Para construir um polígono regular inscrito: trace a circunferência, divida 360° por n, marque os n pontos com o transferidor (ou o compasso) e ligue os pontos vizinhos.",
         "Um robô que «anda e gira» gira o ângulo externo a cada lado."],
        [("Pentágono regular", ["360 ÷ 5 = 72", "180 − 72 = 108"], "central e externo 72°, interno 108°"),
         ("Hexágono inscrito em raio 5 cm", ["lado = raio"], "lado 5 cm")],
        [["Girar o ângulo interno", "O robô gira o ângulo externo: 360° ÷ n."],
         ["Usar 180° em vez de 360°", "A volta completa tem 360°."],
         ["Achar que lados iguais bastam", "O losango tem lados iguais, mas não é regular."]],
        poly_pic(6))
    faq = [("Como calcular o ângulo interno de um polígono regular?", "Divida 360° pelo número de lados para achar o ângulo externo e faça 180° menos esse valor. Ou calcule (n − 2) · 180° e divida por n."),
           ("O que a BNCC pede no 9º ano sobre polígonos regulares?", "Descrever, por escrito e por meio de um fluxograma, um algoritmo para a construção de um polígono regular cuja medida do lado é conhecida, utilizando régua e compasso, como também softwares (EF09MA15).")]
    unit(R, "poligonos-regulares", "G", ["EF09MA15"],
         "Descrever, por escrito e por meio de um fluxograma, um algoritmo para a construção de um polígono regular cuja medida do lado é conhecida, utilizando régua e compasso, como também softwares",
         "Polígonos regulares: ângulos e construção", "Polígonos regulares",
         "Atividades de matemática para o 9º ano sobre polígonos regulares: ângulo central, interno e externo, soma dos ângulos, construção com régua e compasso, algoritmos e polígonos inscritos. 100 exercícios com gabarito.",
         "Ângulo central = 360° ÷ n", "Ângulo interno = 180° − 360° ÷ n",
         body, faq, sets, 15)


if __name__ == "__main__":
    main()
