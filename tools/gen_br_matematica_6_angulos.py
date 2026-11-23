# -*- coding: utf-8 -*-
"""
Brasil Matemática 6º ano: Ângulos (Geometria, EF06MA25, EF06MA26, EF06MA27)
  python3 tools/gen_br_matematica_6_angulos.py
Ângulo como mudança de direção (giro); frações de volta em graus; ângulos agudo, reto, obtuso e raso; ângulos entre os ponteiros
do relógio; medir com o transferidor (as duas escalas); estimar a medida de um ângulo desenhado.
Erros: ler a escala errada do transferidor, achar que o tamanho dos lados muda o ângulo, dizer que 1/4 de volta tem 25°.
"""
import random
import math
from br_common import lesson, mix
from br_9 import M, bank, unit, _svg, _ln, _t, _arc, INK, BLUE, RED

R = random.Random(86018)


def ang_svg(a, lado=None):
    W, H = 260, 170
    vx, vy = 60 if a <= 90 else 135, 150
    L1 = lado or R.randint(100, 120 if a > 90 else 175)
    L2 = R.randint(85, 125) if lado is None else lado
    rot = R.uniform(-10, 10) if a < 170 else 0
    t1, t2 = rot, rot + a
    p1 = (vx + L1 * math.cos(math.radians(t1)), vy - L1 * math.sin(math.radians(t1)))
    p2 = (vx + L2 * math.cos(math.radians(t2)), vy - L2 * math.sin(math.radians(t2)))
    s = [_ln(vx, vy, p1[0], p1[1], INK, 2.4), _ln(vx, vy, p2[0], p2[1], INK, 2.4), _arc(vx, vy, 22, t1, t2, RED)]
    if a == 90:
        u = (math.cos(math.radians(t1)) * 14, -math.sin(math.radians(t1)) * 14)
        w = (math.cos(math.radians(t2)) * 14, -math.sin(math.radians(t2)) * 14)
        s = s[:2] + ["<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='1.8'/>" % (vx + u[0], vy + u[1], vx + u[0] + w[0], vy + u[1] + w[1], vx + w[0], vy + w[1], RED)]
    return _svg(W, H, "".join(s), "um ângulo")


def s1_classe():
    k = R.choice(["agudo", "reto", "obtuso", "raso"])
    a = {"agudo": R.randint(20, 75), "reto": 90, "obtuso": R.randint(105, 160), "raso": 180}[k]
    return M(ang_svg(a) + "Como se classifica este ângulo?", k, [x for x in ["agudo", "reto", "obtuso", "raso"] if x != k],
             {"agudo": "Menor que 90°: <b>agudo</b>.", "reto": "O quadradinho marca 90°: <b>reto</b>.", "obtuso": "Maior que 90° e menor que 180°: <b>obtuso</b>.", "raso": "Os lados formam uma linha reta, 180°: <b>raso</b>."}[k])


def s2_estimar():
    a = R.choice([30, 45, 60, 90, 120, 135, 150])
    ws = [x for x in [30, 45, 60, 90, 120, 135, 150, 180] if abs(x - a) >= 30]
    R.shuffle(ws)
    return M(ang_svg(a) + "Qual é a medida mais provável deste ângulo?", "%d°" % a, ["%d°" % x for x in ws[:3]], "Compare com o ângulo reto (90°) e com o raso (180°): cerca de <b>%d°</b>." % a)


FR = [("1/4 de volta", 90), ("meia volta", 180), ("3/4 de volta", 270), ("uma volta inteira", 360), ("1/8 de volta", 45), ("1/3 de volta", 120), ("1/6 de volta", 60), ("1/12 de volta", 30), ("2/3 de volta", 240), ("1/36 de volta", 10)]


def s3_giro():
    k = R.choice(["fr", "inv", "dir"])
    if k == "fr":
        t, a = R.choice(FR)
        return M("Quantos graus tem %s?" % t, "%d°" % a, ["%d°" % x for x in {25, 50, 100, a * 2 % 360 or 720, a // 2} - {a}][:4], "Uma volta inteira tem 360°: %s = <b>%d°</b>." % (t, a))
    if k == "inv":
        t, a = R.choice(FR)
        return M("Um giro de %d° corresponde a que fração de volta?" % a, t, [x for x, _ in R.sample(FR, 4) if x != t][:3], "%d ÷ 360 → <b>%s</b>." % (a, t))
    d0 = R.choice(["norte", "leste", "sul", "oeste"])
    DIR = ["norte", "leste", "sul", "oeste"]
    g = R.choice([90, 180, 270])
    lado = R.choice(["direita", "esquerda"])
    i = DIR.index(d0)
    f = DIR[(i + (g // 90) * (1 if lado == "direita" else -1)) % 4]
    return M("Uma pessoa está virada para o %s e gira %d° para a %s. Para onde ela fica virada?" % (d0, g, lado), f, [x for x in DIR if x != f], "Cada 90° para a %s é um quarto de volta: fica virada para o <b>%s</b>." % (lado, f))


def s4_relogio():
    k = R.choice(["hora", "min"])
    if k == "hora":
        h = R.randint(1, 11)
        a = min(30 * h, 360 - 30 * h)
        return M("Qual é o menor ângulo entre os ponteiros de um relógio às %dh em ponto?" % h, "%d°" % a, ["%d°" % (a + 30), "%d°" % (360 - a), "%d°" % (h * 10) if h * 10 != a else "%d°" % (a - 30)],
                 "Entre dois números do relógio há 30° (360 ÷ 12). Às %dh há %d espaço%s: <b>%d°</b>." % (h, a // 30, "" if a == 30 else "s", a))
    m = R.choice([5, 10, 15, 20, 25, 30, 40, 45, 50])
    return M("Quantos graus o ponteiro dos minutos gira em %d minutos?" % m, "%d°" % (6 * m), ["%d°" % m, "%d°" % (30 * m) if 30 * m <= 360 else "%d°" % (3 * m), "%d°" % (6 * m + 30)], "Em 60 min ele dá 360°: 6° por minuto; %d × 6 = <b>%d°</b>." % (m, 6 * m))


s5_transferidor = bank(R, [
    ("No transferidor, um lado do ângulo passa pelo 0 da escala de fora e o outro pelo 50 dessa escala. O ângulo mede…", "50°", ["130°", "40°", "150°"]),
    ("No transferidor, um lado passa pelo 0 da escala de dentro e o outro pelo 115 dessa mesma escala. O ângulo mede…", "115°", ["65°", "15°", "125°"]),
    ("Para medir um ângulo com o transferidor, o centro do transferidor fica…", "sobre o vértice do ângulo", ["no fim de um dos lados", "no meio do ângulo", "fora do ângulo"]),
    ("Um ângulo de 70° foi lido como 110°. Qual foi o erro?", "usar a outra escala do transferidor", ["desenhar mal o vértice", "apagar um lado", "nenhum erro"]),
    ("Se aumentarmos o comprimento dos lados de um ângulo, a medida do ângulo…", "não muda", ["aumenta", "diminui", "dobra"]),
    ("Um ângulo agudo mede…", "menos de 90°", ["exatamente 90°", "entre 90° e 180°", "180°"]),
    ("Um ângulo obtuso mede…", "mais de 90° e menos de 180°", ["menos de 90°", "exatamente 90°", "360°"]),
    ("Dois ângulos retos juntos formam um ângulo…", "raso (180°)", ["agudo", "reto", "de 360°"]),
    ("A unidade usual para medir ângulos é…", "o grau (°)", ["o centímetro", "o metro quadrado", "o litro"]),
    ("Uma volta completa mede…", "360°", ["180°", "100°", "90°"]),
    ("O ângulo formado pelo encontro de duas paredes de uma sala costuma ser…", "reto", ["agudo", "raso", "obtuso"]),
    ("A abertura de um leque quase todo aberto, formando quase uma linha reta, lembra um ângulo…", "obtuso perto de 180°", ["agudo", "reto", "nulo"]),
], "s5_transferidor")


def main():
    seen = set()
    sets = [
        ("Classificar ângulos", mix(R, seen, [(s1_classe, 20)])),
        ("Giros e frações de volta", mix(R, seen, [(s3_giro, 20)])),
        ("Estimar e medir", mix(R, seen, [(s2_estimar, 12), (s5_transferidor, 8)])),
        ("Ângulos no relógio", mix(R, seen, [(s4_relogio, 20)])),
        ("Revisão", mix(R, seen, [(s5_transferidor, 4), (s1_classe, 6), (s2_estimar, 6), (s3_giro, 4)])),
    ]
    body = lesson(
        ["Um <b>ângulo</b> mostra uma mudança de direção, um giro. A volta inteira tem 360°; meia volta, 180°; um quarto de volta, 90°.",
         "Classificação: <b>agudo</b> (menos de 90°), <b>reto</b> (90°), <b>obtuso</b> (entre 90° e 180°), <b>raso</b> (180°).",
         "Com o <b>transferidor</b>: centro no vértice, um lado no 0 e leia na mesma escala em que está o 0.",
         "No relógio, de um número ao seguinte há 30°; o ponteiro dos minutos gira 6° por minuto."],
        [("3/4 de volta", ["360 ÷ 4 × 3"], "270°"),
         ("Ponteiros às 4h", ["4 × 30"], "120°")],
        [["Ler a escala errada", "Leia na escala que começa no 0 do seu lado."],
         ["Achar que lados maiores dão ângulo maior", "O ângulo é a abertura, não o tamanho dos lados."],
         ["Dizer que 1/4 de volta tem 25°", "1/4 de 360° = 90°."]],
        ang_svg(90, 120))
    faq = [("Como usar o transferidor?", "Coloque o centro do transferidor no vértice do ângulo, alinhe um lado com o 0 e leia a medida onde passa o outro lado, na mesma escala em que está o 0."),
           ("O que a BNCC pede no 6º ano?", "Reconhecer a abertura do ângulo como grandeza associada às figuras geométricas (EF06MA25), resolver problemas que envolvam a noção de ângulo em diferentes contextos e em situações reais, como ângulo de visão (EF06MA26), e determinar medidas da abertura de ângulos, por meio de transferidor e/ou tecnologias digitais (EF06MA27).")]
    unit(R, "angulos", "G", ["EF06MA25", "EF06MA26", "EF06MA27"],
         "Reconhecer a abertura do ângulo como grandeza associada às figuras geométricas; resolver problemas que envolvam a noção de ângulo em diferentes contextos e em situações reais, como ângulo de visão; determinar medidas da abertura de ângulos, por meio de transferidor e/ou tecnologias digitais",
         "Ângulos: giros, classificação e transferidor", "Ângulos",
         "Atividades de matemática para o 6º ano sobre ângulos: giros e frações de volta, ângulos agudo, reto, obtuso e raso, uso do transferidor e ângulos no relógio. 100 exercícios com gabarito.",
         "Volta inteira: 360°. Ângulo reto: 90°.", "Leia o transferidor na escala que começa no 0.",
         body, faq, sets, 18, grade="6-ano")


if __name__ == "__main__":
    main()
