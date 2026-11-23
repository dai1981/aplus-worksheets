# -*- coding: utf-8 -*-
"""
Brasil Matemática 4º ano: Ângulos retos e não retos (Geometria, EF04MA18)
  python3 tools/gen_br_matematica_4_angulos_retos_e_nao_retos.py
Reconhecer ângulos retos (como o canto de uma folha ou do esquadro) e não retos (agudos e obtusos); contar os ângulos retos de polígonos;
giros de 1/4 de volta (ângulo reto), meia-volta e volta inteira; ângulos dos ponteiros do relógio.
Erros: achar que o ângulo muda de tipo quando a figura gira, confundir o tamanho do lado com o tamanho do ângulo, achar que todo quadrilátero tem 4 ângulos retos.
"""
import random
from br_common import mcq, lesson, make_unit, mix, wrap, line, text, INK, RED, relogio, use

R = random.Random(80414)
M = "gen_br_matematica_5_poligonos"
s_ang, s_quiz = use(M, 80955, "s3_angulo", "s3_quiz")
COLS = ["#cfe6d6", "#f6d6a8", "#c9dcf2", "#f2c6d0", "#e8e0a8"]
SHAPES = {
    "retângulo": ([(0, 0), (6, 0), (6, 3), (0, 3)], 4),
    "quadrado": ([(0, 0), (4, 0), (4, 4), (0, 4)], 4),
    "triângulo retângulo": ([(0, 0), (5, 0), (0, 4)], 1),
    "trapézio retângulo": ([(0, 0), (6, 0), (4, 3), (0, 3)], 2),
    "figura em L": ([(0, 0), (6, 0), (6, 2), (2, 2), (2, 5), (0, 5)], 5),
    "paralelogramo": ([(0, 0), (5, 0), (7, 3), (2, 3)], 0),
    "losango": ([(3, 0), (6, 2), (3, 4), (0, 2)], 0),
    "triângulo": ([(0, 0), (6, 0), (2, 4)], 0),
    "pentágono da casinha": ([(0, 0), (5, 0), (5, 3), (2.5, 5), (0, 3)], 2),
    "trapézio": ([(1, 0), (5, 0), (6, 3), (0, 3)], 0),
}


def is_right(p0, p1, p2):
    ax, ay = p0[0] - p1[0], p0[1] - p1[1]
    bx, by = p2[0] - p1[0], p2[1] - p1[1]
    return abs(ax * bx + ay * by) < 1e-9


def figura(pts):
    c = 26
    ang = R.choice([0, 90, 180, 270])
    # girar a figura para mostrar que o ângulo não depende da posição
    import math
    a = math.radians(ang)
    P = [(x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)) for x, y in pts]
    mx, my = min(x for x, _ in P), min(y for _, y in P)
    P = [(20 + (x - mx) * c, 20 + (y - my) * c) for x, y in P]
    W = int(max(x for x, _ in P) + 20)
    H = int(max(y for _, y in P) + 20)
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.4'/>" % (" ".join("%.1f,%.1f" % p for p in P), R.choice(COLS), INK)]
    n = len(P)
    area = sum(P[i][0] * P[(i + 1) % n][1] - P[(i + 1) % n][0] * P[i][1] for i in range(n))
    for i in range(n):
        p0, p1, p2 = P[i - 1], P[i], P[(i + 1) % n]
        cross = (p1[0] - p0[0]) * (p2[1] - p1[1]) - (p1[1] - p0[1]) * (p2[0] - p1[0])
        if is_right(p0, p1, p2) and cross * area > 0:
            lu = math.hypot(p0[0] - p1[0], p0[1] - p1[1])
            lv = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
            ux, uy = (p0[0] - p1[0]) / lu * 12, (p0[1] - p1[1]) / lu * 12
            vx, vy = (p2[0] - p1[0]) / lv * 12, (p2[1] - p1[1]) / lv * 12
            s.append("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='1.6'/>" % (p1[0] + ux, p1[1] + uy, p1[0] + ux + vx, p1[1] + uy + vy, p1[0] + vx, p1[1] + vy, RED))
    return wrap(max(W, 120), max(H, 100), "".join(s), "polígono")


def s2_contar():
    nome = R.choice(sorted(SHAPES))
    pts, n = SHAPES[nome]
    marcar = R.random() < 0.5
    pic = figura(pts) if marcar else figura(pts).replace("stroke='%s' stroke-width='1.6'" % RED, "stroke='none' stroke-width='0'")
    return mcq(pic + "Quantos ângulos retos tem esta figura (%s)?%s" % (nome, " Os quadradinhos vermelhos marcam os ângulos retos." if marcar else " Use o canto de uma folha para conferir."),
               str(n), [str(x) for x in (n + 1, n - 1 if n else 2, len(pts), 4 if n != 4 else 2)],
               "Confira cada canto com o canto de uma folha (ou o esquadro): <b>%d</b> ângulo%s reto%s." % (n, "" if n == 1 else "s", "" if n == 1 else "s"))


def s2_qual():
    com = sorted(k for k, (_, n) in SHAPES.items() if n > 0)
    sem = sorted(k for k, (_, n) in SHAPES.items() if n == 0)
    if R.random() < 0.5:
        a, w = R.choice(com), R.sample(sem, 3)
        q = "Qual destas figuras tem pelo menos um ângulo reto: %s?"
        e = "O %s tem %d ângulo%s reto%s: <b>%s</b>." % (a, SHAPES[a][1], "" if SHAPES[a][1] == 1 else "s", "" if SHAPES[a][1] == 1 else "s", a)
    else:
        a, w = R.choice(sem), R.sample(com, 3)
        q = "Qual destas figuras <b>não</b> tem nenhum ângulo reto: %s?"
        e = "Os ângulos do %s são agudos ou obtusos: <b>%s</b>." % (a, a)
    opts = sorted([a] + w)
    return mcq(q % (", ".join(opts[:-1]) + " ou " + opts[-1]), a, w, e)


def s3_giro():
    q, a, w = R.choice([("Quando giramos 1/4 de volta, formamos um ângulo…", "reto", ["agudo", "obtuso", "raso"]),
                        ("Quantos ângulos retos há numa volta inteira?", "4", ["2", "1", "3"]),
                        ("Quantos ângulos retos há em meia-volta?", "2", ["1", "4", "3"]),
                        ("Uma pessoa de frente para o norte gira 1/4 de volta para a direita. Fica de frente para o…", "leste", ["oeste", "sul", "norte"]),
                        ("Uma pessoa de frente para o norte dá meia-volta. Fica de frente para o…", "sul", ["leste", "oeste", "norte"]),
                        ("Que instrumento usamos para conferir um ângulo reto?", "o esquadro", ["o compasso", "a balança", "o termômetro"]),
                        ("Dobrando uma folha ao meio duas vezes, o canto formado é um ângulo…", "reto", ["agudo", "obtuso", "raso"]),
                        ("Um ângulo menor que o reto é chamado…", "agudo", ["obtuso", "raso", "reto"]),
                        ("Um ângulo maior que o reto (e menor que meia-volta) é chamado…", "obtuso", ["agudo", "reto", "nulo"]),
                        ("Se giramos um quadrado, os ângulos dele…", "continuam retos", ["ficam agudos", "ficam obtusos", "somem"])])
    return mcq(q, a, w, "Ângulo reto = 1/4 de volta, como o canto de uma folha. Resposta: <b>%s</b>." % a)


def s3_relogio():
    h = R.choice([3, 9, 1, 2, 4, 5, 7, 8, 10, 11, 6, 12])
    t = "reto" if h in (3, 9) else "agudo" if h in (1, 2, 10, 11, 12) else "obtuso" if h in (4, 5, 7, 8) else "raso (meia-volta)"
    if h == 12:
        return None
    return mcq(relogio(h, 0) + "Que ângulo os ponteiros formam às %dh?" % h, t, [x for x in ["reto", "agudo", "obtuso", "raso (meia-volta)"] if x != t],
               "Compare com o canto de uma folha (3h e 9h formam ângulo reto): <b>%s</b>." % t)


def main():
    seen = set()
    sets = [
        ("Ângulo reto ou não?", mix(R, seen, [(s_ang, 20)])),
        ("Ângulos retos nos polígonos", mix(R, seen, [(s2_contar, 14), (s2_qual, 6)])),
        ("Giros e ângulos", mix(R, seen, [(s3_giro, 10), (s_quiz, 10)])),
        ("Ângulos no relógio", mix(R, seen, [(s3_relogio, 10), (s_ang, 10)])),
        ("Desafios", mix(R, seen, [(s2_contar, 16), (s2_qual, 4)])),
    ]
    body = lesson(
        ["Um <b>ângulo reto</b> tem a abertura do canto de uma folha de papel ou de um esquadro: é 1/4 de volta.",
         "Ângulos <b>não retos</b> são menores (agudos) ou maiores (obtusos) que o reto.",
         "Para conferir, encoste o canto de uma folha dobrada no ângulo.",
         "Girar a figura não muda os ângulos: o quadrado continua com 4 ângulos retos."],
        [("Quantos ângulos retos tem um retângulo?", ["os 4 cantos são como o canto da folha"], "4"),
         ("Às 3h, os ponteiros formam que ângulo?", ["1/4 de volta"], "reto")],
        [["Achar que o ângulo muda quando a figura gira", "Os ângulos ficam iguais em qualquer posição."],
         ["Achar que o ângulo é maior porque os lados são compridos", "O tamanho do ângulo é a abertura, não o comprimento dos lados."],
         ["Achar que todo quadrilátero tem ângulos retos", "O losango e o paralelogramo podem não ter nenhum."]])
    faq = [("Como o 4º ano reconhece ângulos retos?", "A BNCC pede reconhecer ângulos retos e não retos em figuras poligonais, usando dobraduras, esquadros ou softwares de geometria."),
           ("Como fazer um «medidor» de ângulo reto?", "Dobre uma folha ao meio e depois ao meio de novo: o canto da dobra é um ângulo reto perfeito.")]
    make_unit(R, "angulos-retos-e-nao-retos", "G", ["EF04MA18"],
              "Reconhecer ângulos retos e não retos em figuras poligonais com o uso de dobraduras, esquadros ou softwares de geometria",
              "Ângulos retos e não retos", "Ângulos retos",
              "Atividades de matemática para o 4º ano sobre ângulos retos e não retos: canto da folha e esquadro, ângulos nos polígonos, giros de 1/4 de volta e ângulos dos ponteiros do relógio. 100 exercícios com gabarito.",
              "Ângulo reto: o canto de uma folha (1/4 de volta).", "Girar a figura não muda os ângulos.",
              body, faq, sets, 14, grade="4-ano")


if __name__ == "__main__":
    main()
