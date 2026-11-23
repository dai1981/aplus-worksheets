# -*- coding: utf-8 -*-
"""
Brasil Matemática 5º ano: Polígonos (Geometria, EF05MA17)
  python3 tools/gen_br_matematica_5_poligonos.py
Reconhecer polígonos (figura plana fechada de lados retos); nomes pelo número de lados (triângulo … decágono);
lados, vértices e ângulos; ângulos retos, agudos e obtusos; polígonos regulares; triângulos e quadriláteros; desenhar com régua e esquadro.
Erros: chamar o círculo de polígono, achar que todo hexágono é regular, confundir número de lados e de diagonais.
"""
import math
import random
from br_common import mcq, lesson, make_unit, mix, wrap, line, text, INK, GREEN, RED

R = random.Random(80516)
NOMES = {3: "triângulo", 4: "quadrilátero", 5: "pentágono", 6: "hexágono", 7: "heptágono", 8: "octógono", 9: "eneágono", 10: "decágono"}
COL = ["#cfe6d6", "#f6d6a8", "#c9dcf2", "#f2c6d0", "#e8e0a8"]


def poly_pts(n, regular, cx=90, cy=90, r=70):
    rot = R.uniform(0, 2 * math.pi)
    pts = []
    for i in range(n):
        ang = rot + 2 * math.pi * i / n + (0 if regular else R.uniform(-0.25, 0.25) * 2 * math.pi / n)
        rr = r if regular else r * R.uniform(0.7, 1.0)
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    return pts


def poly_svg(pts, col=None, label="polígono"):
    body = "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.4'/>" % (" ".join("%.1f,%.1f" % p for p in pts), col or R.choice(COL), INK)
    return wrap(180, 180, body, label)


def s1_nome():
    n = R.randint(3, 10)
    reg = R.random() < 0.5
    pic = poly_svg(poly_pts(n, reg), label="polígono")
    near = sorted([m for m in NOMES if m != n], key=lambda m: (abs(m - n), R.random()))[:3]
    return mcq(pic + "Como se chama este polígono?", NOMES[n], [NOMES[m] for m in near],
               "Conte os lados: são %d. Um polígono de %d lados é um <b>%s</b>." % (n, n, NOMES[n]))


def s1_lados():
    n = R.randint(3, 10)
    k = R.choice(["lados", "vértices", "ângulos", "nome"])
    if k == "nome":
        near = sorted([m for m in NOMES if m != n], key=lambda m: (abs(m - n), R.random()))[:3]
        return mcq("Como se chama o polígono que tem %d lados?" % n, NOMES[n], [NOMES[m] for m in near], "%d lados: <b>%s</b>." % (n, NOMES[n]))
    return mcq("Quantos %s tem um %s?" % (k, NOMES[n]), str(n), [str(n + 1), str(n - 1), str(2 * n)],
               "Num polígono, o número de lados, de vértices e de ângulos é o mesmo: <b>%d</b>." % n)


FIG = [("circulo", False, "o contorno é curvo"), ("aberta", False, "a figura não é fechada"), ("curva", False, "tem um lado curvo"),
       ("estrela", True, "é fechada e tem só lados retos"), ("seta", True, "é fechada e tem só lados retos"), ("cruzada", False, "os lados se cruzam")]


def fig_svg(kind):
    if kind == "circulo":
        b = "<ellipse cx='90' cy='90' rx='%d' ry='%d' fill='%s' stroke='%s' stroke-width='2.4'/>" % (R.randint(50, 70), R.randint(40, 70), R.choice(COL), INK)
    elif kind == "aberta":
        pts = poly_pts(R.randint(4, 6), False)
        b = "<polyline points='%s' fill='none' stroke='%s' stroke-width='2.4'/>" % (" ".join("%.1f,%.1f" % p for p in pts), INK)
    elif kind == "curva":
        b = "<path d='M30 140 L150 140 L150 60 Q90 10 30 60 Z' fill='%s' stroke='%s' stroke-width='2.4'/>" % (R.choice(COL), INK)
    elif kind == "estrela":
        k = R.choice([5, 6])
        pts = []
        for i in range(2 * k):
            r = 75 if i % 2 == 0 else 32
            a = -math.pi / 2 + math.pi * i / k
            pts.append((90 + r * math.cos(a), 92 + r * math.sin(a)))
        b = "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.4'/>" % (" ".join("%.1f,%.1f" % p for p in pts), R.choice(COL), INK)
    elif kind == "seta":
        b = "<polygon points='20,70 100,70 100,40 160,90 100,140 100,110 20,110' fill='%s' stroke='%s' stroke-width='2.4'/>" % (R.choice(COL), INK)
    else:
        b = "<polygon points='30,40 150,140 150,40 30,140' fill='none' stroke='%s' stroke-width='2.4'/>" % INK
    return wrap(180, 180, b, "figura plana")


def s2_eh():
    kind, ok, why = R.choice(FIG)
    return mcq(fig_svg(kind) + "Esta figura é um polígono?", "Sim" if ok else "Não", ["Não" if ok else "Sim", "Só se for colorida", "Só se tiver 4 lados"] if ok else ["Sim", "Só se for colorida", "Só se tiver 4 lados"],
               "Polígono é uma figura plana fechada, formada só por segmentos de reta que não se cruzam. Aqui %s: <b>%s</b>." % (why, "é polígono" if ok else "não é polígono"))


DEF = [("O que é um polígono?", "uma figura plana fechada formada por segmentos de reta", ["qualquer figura com cantos", "uma figura plana com lados curvos", "uma figura espacial"]),
       ("O que é o vértice de um polígono?", "o ponto onde dois lados se encontram", ["o meio de um lado", "o lado maior", "a parte de dentro"]),
       ("O que é um polígono regular?", "um polígono com todos os lados e todos os ângulos iguais", ["um polígono com 4 lados", "um polígono grande", "um polígono com lados curvos"]),
       ("Qual destas figuras é um polígono regular?", "o quadrado", ["o retângulo comprido", "o losango que não é quadrado", "o trapézio"]),
       ("Qual destas figuras não é um polígono?", "o círculo", ["o triângulo", "o hexágono", "o retângulo"]),
       ("Quantos lados tem o menor polígono que existe?", "3", ["2", "4", "1"]),
       ("Um polígono com 8 ângulos tem quantos lados?", "8", ["4", "16", "7"]),
       ("Que nome tem um quadrilátero com 4 ângulos retos e 4 lados iguais?", "quadrado", ["retângulo", "losango", "trapézio"]),
       ("Que nome tem um quadrilátero com só um par de lados paralelos?", "trapézio", ["paralelogramo", "retângulo", "losango"]),
       ("Que nome tem um quadrilátero com 4 lados iguais e sem ângulos retos?", "losango", ["quadrado", "retângulo", "trapézio"])]


def s2_def():
    q, a, w = R.choice(DEF)
    return mcq(q, a, w, "Resposta: <b>%s</b>." % a)


def angulo_svg(g):
    cx, cy = 100, 130
    a = math.radians(g)
    s = [line(cx, cy, cx + 130, cy, INK, 2.6), line(cx, cy, cx + 110 * math.cos(-a), cy + 110 * math.sin(-a), INK, 2.6)]
    if g == 90:
        s.append("<path d='M%d %d h18 v-18 h-18' fill='none' stroke='%s' stroke-width='1.6'/>" % (cx, cy, RED))
    else:
        r = 26
        s.append("<path d='M%.1f %.1f A%d %d 0 0 0 %.1f %.1f' fill='none' stroke='%s' stroke-width='1.6'/>" % (cx + r, cy, r, r, cx + r * math.cos(-a), cy + r * math.sin(-a), RED))
    return wrap(240, 145, "".join(s), "ângulo")


def s3_angulo():
    t = R.choice(["agudo", "reto", "obtuso"])
    g = {"agudo": R.randint(25, 70), "reto": 90, "obtuso": R.randint(110, 160)}[t]
    return mcq(angulo_svg(g) + "Este ângulo é agudo, reto ou obtuso?", t, [x for x in ["agudo", "reto", "obtuso", "raso"] if x != t],
               "Compare com o canto de uma folha (ângulo reto, 90°): %s. É <b>%s</b>." % ({"agudo": "é menor", "reto": "é igual", "obtuso": "é maior"}[t], t))


ANG = [("Quantos ângulos retos tem um retângulo?", "4", ["2", "0", "1"]), ("Quantos ângulos retos pode ter um triângulo, no máximo?", "1", ["2", "3", "0"]),
       ("Um ângulo menor que o canto de uma folha de papel é…", "agudo", ["reto", "obtuso", "raso"]), ("Um ângulo maior que um ângulo reto e menor que meia-volta é…", "obtuso", ["agudo", "reto", "raso"]),
       ("Que instrumento ajuda a desenhar ângulos retos?", "o esquadro", ["o compasso", "a balança", "a fita métrica"]),
       ("Os ponteiros de um relógio às 3h formam um ângulo…", "reto", ["agudo", "obtuso", "raso"]), ("Os ponteiros de um relógio à 1h formam um ângulo…", "agudo", ["reto", "obtuso", "raso"]),
       ("Os ponteiros de um relógio às 5h formam um ângulo…", "obtuso", ["agudo", "reto", "raso"]), ("Quantos ângulos tem um hexágono?", "6", ["5", "8", "12"]),
       ("Num quadrado, todos os ângulos são…", "retos", ["agudos", "obtusos", "diferentes"]), ("Num triângulo equilátero, os ângulos são…", "agudos e iguais", ["retos", "obtusos", "diferentes"])]


def s3_quiz():
    q, a, w = R.choice(ANG)
    return mcq(q, a, w, "Resposta: <b>%s</b>." % a)


def s4_regular():
    n = R.randint(3, 8)
    reg = R.random() < 0.5
    pic = poly_svg(poly_pts(n, reg, r=72), label="polígono")
    ans = "regular" if reg else "não regular"
    return mcq(pic + "Este %s é regular ou não regular?" % NOMES[n], ans, ["não regular" if reg else "regular", "não é polígono", "depende da cor"],
               "%s <b>%s</b>." % ("Todos os lados e ângulos são iguais:" if reg else "Os lados não são todos iguais:", ans))


def s4_triangulos():
    k = R.choice(["equi", "iso", "esc", "ret"])
    if k == "ret":
        a, b = R.randint(50, 110), R.randint(50, 110)
        pts = [(30, 150), (30 + a, 150), (30, 150 - b)]
        extra = "<path d='M30 150 h14 v-14 h-14' fill='none' stroke='%s' stroke-width='1.6'/>" % RED
        ans, why = "triângulo retângulo", "tem um ângulo reto"
    elif k == "equi":
        L = R.randint(90, 130)
        pts = [(25, 150), (25 + L, 150), (25 + L / 2, 150 - L * 0.866)]
        extra = ""
        ans, why = "triângulo equilátero", "tem os 3 lados iguais"
    elif k == "iso":
        L, h = R.randint(70, 110), R.randint(100, 135)
        pts = [(25, 150), (25 + L, 150), (25 + L / 2, 150 - h)]
        extra = ""
        ans, why = "triângulo isósceles", "tem 2 lados iguais"
    else:
        pts = [(20, 150), (160, 150), (R.randint(40, 70), R.randint(50, 80))]
        extra = ""
        ans, why = "triângulo escaleno", "tem os 3 lados diferentes"
    body = "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.4'/>%s" % (" ".join("%.1f,%.1f" % p for p in pts), R.choice(COL), INK, extra)
    marks = ""
    if k in ("equi", "iso"):
        sides = [(pts[0], pts[2]), (pts[1], pts[2])] + ([(pts[0], pts[1])] if k == "equi" else [])
        for p1, p2 in sides:
            mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
            dx, dy = p2[0] - p1[0], p2[1] - p1[1]
            d = math.hypot(dx, dy)
            nx, ny = -dy / d * 7, dx / d * 7
            marks += line(mx - nx, my - ny, mx + nx, my + ny, RED, 2)
    pic = wrap(180, 160, body + marks, "triângulo")
    opts = ["triângulo retângulo", "triângulo equilátero", "triângulo isósceles", "triângulo escaleno"]
    return mcq(pic + "Que triângulo é este? (Os risquinhos vermelhos marcam lados iguais.)", ans, [o for o in opts if o != ans],
               "Ele %s: <b>%s</b>." % (why, ans))


def s5_problema():
    k = R.choice(["vert", "soma", "palitos", "regular", "lados2", "diag"])
    if k == "vert":
        a, b = R.sample(range(3, 11), 2)
        return mcq("Juntando os vértices de um %s e de um %s, quantos vértices temos ao todo?" % (NOMES[a], NOMES[b]), str(a + b), [str(a * b), str(a + b + 2), str(abs(a - b))],
                   "%s: %d vértices; %s: %d vértices. %d + %d = <b>%d</b>." % (NOMES[a], a, NOMES[b], b, a, b, a + b))
    if k == "palitos":
        n = R.randint(3, 10)
        m = R.randint(2, 5)
        return mcq("Com palitos iguais, %s montou %d %ss separados. Quantos palitos usou?" % (R.choice(["Lucas", "Maria", "Davi", "Júlia"]), m, NOMES[n]), str(n * m),
                   [str(n + m), str(n * m + m), str(n)], "Cada %s usa %d palitos: %d × %d = <b>%d</b>." % (NOMES[n], n, m, n, n * m))
    if k == "regular":
        n = R.randint(3, 8)
        L = R.randint(3, 15)
        return mcq("Um %s regular tem lados de %d cm. Quanto mede o contorno dele?" % (NOMES[n], L), "%d cm" % (n * L), ["%d cm" % x for x in (n + L, L * 4 if n != 4 else L * 3, (n - 1) * L)],
                   "Todos os %d lados medem %d cm: %d × %d = <b>%d cm</b>." % (n, L, n, L, n * L))
    if k == "lados2":
        a, b = R.sample(range(3, 11), 2)
        return mcq("Quantos lados um %s tem a mais que um %s?" % (NOMES[max(a, b)], NOMES[min(a, b)]), str(abs(a - b)), [str(a + b), str(max(a, b)), str(abs(a - b) + 1)],
                   "%d − %d = <b>%d</b>." % (max(a, b), min(a, b), abs(a - b)))
    if k == "soma":
        q, ans, w, e = R.choice([
            ("Uma placa de trânsito «PARE» tem a forma de um polígono com 8 lados. Como se chama esse polígono?", "octógono", ["hexágono", "decágono", "heptágono"], "8 lados: <b>octógono</b>."),
            ("Um favo de mel é formado por células com 6 lados iguais. Que polígono elas lembram?", "hexágono regular", ["pentágono regular", "octógono", "quadrado"], "6 lados iguais: <b>hexágono regular</b>."),
            ("Uma bola de futebol tradicional tem gomos com 5 lados. Que polígono eles lembram?", "pentágono", ["hexágono", "quadrilátero", "heptágono"], "5 lados: <b>pentágono</b>."),
            ("Uma placa de «dê a preferência» tem a forma de um polígono com 3 lados iguais. Que polígono é?", "triângulo equilátero", ["triângulo retângulo", "quadrado", "triângulo escaleno"], "3 lados iguais: <b>triângulo equilátero</b>.")])
        return mcq(q, ans, w, e)
    n = R.randint(4, 6)
    d = n * (n - 3) // 2
    return mcq("Uma diagonal liga dois vértices que não são vizinhos. Quantas diagonais tem um %s?" % NOMES[n], str(d), [str(n), str(n * (n - 3)), str(d + 1)],
               "De cada vértice saem %d diagonais; %d × %d = %d, mas cada diagonal foi contada 2 vezes: %d ÷ 2 = <b>%d</b>." % (n - 3, n, n - 3, n * (n - 3), n * (n - 3), d))


def main():
    seen = set()
    sets = [
        ("Nomes dos polígonos", mix(R, seen, [(s1_nome, 12), (s1_lados, 8)])),
        ("O que é um polígono", mix(R, seen, [(s2_eh, 10), (s2_def, 10)])),
        ("Ângulos", mix(R, seen, [(s3_angulo, 12), (s3_quiz, 8)])),
        ("Regulares e triângulos", mix(R, seen, [(s4_regular, 10), (s4_triangulos, 10)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Um <b>polígono</b> é uma figura plana fechada, formada só por segmentos de reta (lados) que não se cruzam. O círculo não é polígono.",
         "O nome depende do número de lados: 3 triângulo, 4 quadrilátero, 5 pentágono, 6 hexágono, 7 heptágono, 8 octógono, 9 eneágono, 10 decágono.",
         "Todo polígono tem o mesmo número de lados, vértices e ângulos.",
         "Ângulo <b>reto</b> = canto de uma folha (90°); <b>agudo</b> é menor; <b>obtuso</b> é maior.",
         "Um polígono é <b>regular</b> quando tem todos os lados e todos os ângulos iguais."],
        [("Quantos vértices tem um octógono?", ["octógono = 8 lados", "lados = vértices"], "8"),
         ("Um retângulo comprido é um polígono regular?", ["os ângulos são iguais", "mas os lados não são todos iguais"], "não")],
        [["Chamar o círculo de polígono", "O círculo não tem lados retos."],
         ["Achar que todo hexágono é regular", "Um hexágono pode ter lados diferentes; regular é só quando todos são iguais."],
         ["Confundir ângulo obtuso com reto", "Use o canto de uma folha para comparar."]],
        poly_svg(poly_pts(6, True), COL[0], "hexágono regular"))
    faq = [("O que o 5º ano aprende sobre polígonos?", "A BNCC pede reconhecer, nomear e comparar polígonos considerando lados, vértices e ângulos, e desenhá-los com régua, esquadro ou softwares de geometria."),
           ("Qual é a diferença entre polígono regular e irregular?", "No regular, todos os lados e ângulos são iguais (quadrado, triângulo equilátero). No irregular, não.")]
    make_unit(R, "poligonos", "G", ["EF05MA17"],
              "Reconhecer, nomear e comparar polígonos, considerando lados, vértices e ângulos, e desenhá-los, utilizando material de desenho ou tecnologias digitais",
              "Polígonos: lados, vértices e ângulos", "Polígonos",
              "Atividades de matemática para o 5º ano sobre polígonos: nomes pelo número de lados, lados, vértices e ângulos, ângulos retos, agudos e obtusos, polígonos regulares e triângulos. 100 exercícios com gabarito.",
              "Polígono: figura plana fechada de lados retos.", "Lados = vértices = ângulos.",
              body, faq, sets, 16, grade="5-ano")


if __name__ == "__main__":
    main()
