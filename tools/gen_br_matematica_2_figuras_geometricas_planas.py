# -*- coding: utf-8 -*-
"""
Brasil Matemática 2º ano: Figuras geométricas planas (Geometria, EF02MA15)
  python3 tools/gen_br_matematica_2_figuras_geometricas_planas.py
Círculo, quadrado, retângulo e triângulo: nome, em posições diferentes (girados), lados e cantos (vértices),
contar figuras num desenho, contorno das faces de sólidos (carimbo), comparar quadrado e retângulo.
Erros: achar que um quadrado girado deixa de ser quadrado, achar que o triângulo só é triângulo «de ponta para cima», confundir quadrado com retângulo.
"""
import random
import k_pics
from br_common import mcq, lesson, make_unit, mix, fig, relabel, text, INK, wrap
from br_2 import FORMAS, CORES

R = random.Random(80214)
K4 = ["circle", "square", "rectangle", "triangle"]
ART = {"circle": "o círculo", "square": "o quadrado", "rectangle": "o retângulo", "triangle": "o triângulo"}
LADOS = {"circle": 0, "square": 4, "rectangle": 4, "triangle": 3}


def nm(k):
    return FORMAS[k][0]


def tri_svg(color):
    """triângulo com lados diferentes, em qualquer posição"""
    import math
    pts = []
    for a0 in sorted(R.sample(range(0, 360, 15), 3)):
        r = R.uniform(28, 46)
        pts.append((60 + r * math.cos(math.radians(a0)), 60 + r * math.sin(math.radians(a0))))
    (x1, y1), (x2, y2), (x3, y3) = pts
    area = abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / 2
    if area < 700:
        return None
    f, st = k_pics.SHAPE_COL[color]
    return "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 120' width='120' height='120' role='img' aria-label='uma figura plana'><polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/></svg>" % (
        " ".join("%.1f,%.1f" % p for p in pts), f, st)


def uma(k, color=None, rot=None):
    color = color or R.choice(sorted(CORES))
    rot = R.choice([0, 0, 20, 35, 45, 70, 90, 120, 160]) if rot is None and k != "circle" else (rot or 0)
    if k == "triangle" and R.random() < 0.5:
        t = tri_svg(color)
        if t:
            return fig(t)
    return fig(relabel(k_pics.one_shape_svg(k, color, 36, rot), "uma figura plana"))


def s1_nome():
    k = R.choice(K4)
    # o quadrado também é um retângulo: não usar «retângulo» como resposta errada do quadrado
    wr = [nm(x) for x in K4 if x != k and not (k == "square" and x == "rectangle")] + (["hexágono"] if k == "square" else [])
    return mcq(uma(k) + "Que figura é esta?", nm(k), wr,
               "%s%s. Resposta: <b>%s</b>." % ({"circle": "Contorno redondo, sem lados retos", "square": "4 lados iguais e 4 cantos retos", "rectangle": "4 lados e 4 cantos retos, dois lados mais compridos", "triangle": "3 lados e 3 cantos"}[k],
                                               ", mesmo girada" if k != "circle" else "", nm(k)))


def s1_letras():
    ks = R.sample(K4, 4)
    alvo = R.choice(ks)
    if alvo == "rectangle":  # sem quadrado: o quadrado também é um retângulo
        ks = ["triangle" if x == "square" else x for x in ks]
    items = [(k, R.choice(sorted(CORES))) for k in ks]
    pic = fig(relabel(k_pics.lettered_shapes_svg(items), "figuras A, B, C e D"))
    i = ks.index(alvo)
    return mcq(pic + "Qual letra mostra %s?" % ART[alvo], "ABCD"[i], [x for x in "ABCD" if x != "ABCD"[i]], "%s está na letra <b>%s</b>." % (ART[alvo].capitalize(), "ABCD"[i]))


def s2_lados():
    k = R.choice(K4)
    t = R.choice(["lados", "cantos"])
    n = LADOS[k]
    if k == "circle":
        return mcq("Quantos %s retos tem o círculo?" % ("lados" if t == "lados" else "cantos"), "nenhum", ["1", "2", "4"], "O círculo tem o contorno curvo: <b>nenhum</b>.")
    return mcq(uma(k) + "Quantos %s tem esta figura?" % ("lados" if t == "lados" else "cantos (vértices)"), str(n), [str(x) for x in (3, 4, 5, 2) if x != n],
               "%s tem <b>%d %s</b>." % (ART[k].capitalize(), n, "lados" if t == "lados" else "cantos"))


PROP = [("Que figura tem 3 lados?", "triângulo", ["quadrado", "retângulo", "círculo"]),
        ("Que figura não tem lados retos nem cantos?", "círculo", ["triângulo", "quadrado", "retângulo"]),
        ("Que figura tem 4 lados todos do mesmo tamanho?", "quadrado", ["retângulo", "triângulo", "círculo"]),
        ("Que figura tem 4 lados, com dois lados compridos e dois curtos?", "retângulo", ["quadrado", "triângulo", "círculo"]),
        ("O quadrado e o retângulo têm quantos lados cada um?", "4", ["3", "5", "0"]),
        ("Quantos lados têm juntos 1 triângulo e 1 quadrado?", "7", ["6", "8", "4"]),
        ("Quantos cantos têm juntos 2 triângulos?", "6", ["3", "5", "8"]),
        ("Quantos lados têm juntos 2 quadrados?", "8", ["4", "6", "16"]),
        ("Quantos lados têm juntos 1 retângulo e 1 círculo?", "4", ["5", "8", "0"]),
        ("Um triângulo girado de cabeça para baixo continua sendo…", "um triângulo", ["um quadrado", "um círculo", "outra figura"]),
        ("Um quadrado girado, apoiado num canto, continua sendo…", "um quadrado", ["um triângulo", "um círculo", "um retângulo comprido"]),
        ("Qual figura tem mais lados: o triângulo ou o retângulo?", "o retângulo", ["o triângulo", "os dois têm o mesmo", "o círculo"])]


def s2_prop():
    q, a, w = R.choice(PROP)
    return mcq(q, a, w, "Resposta: <b>%s</b>." % a)


def s3_contar():
    alvo = R.choice(K4)
    n = R.randint(2, 6)
    others = [x for x in K4 if x != alvo and not (alvo == "rectangle" and x == "square")]
    items = [(alvo, R.choice(sorted(CORES))) for _ in range(n)] + [(R.choice(others), R.choice(sorted(CORES))) for _ in range(R.randint(4, 8))]
    R.shuffle(items)
    if len(items) > 15:
        return None
    pic = fig(relabel(k_pics.shapes_mix_svg(items, R.randint(1, 99999)), "figuras planas misturadas"))
    return mcq(pic + "Quantos %s há no desenho?" % FORMAS[alvo][1], str(n), [str(n + 1), str(n - 1), str(len(items))], "Conte só os %s: <b>%d</b>." % (FORMAS[alvo][1], n))


def s3_cor():
    alvo = R.choice(K4)
    cor = R.choice(sorted(CORES))
    pool = [x for x in K4 if not (alvo == "rectangle" and x == "square")]
    items = [(R.choice(pool), R.choice(sorted(CORES))) for _ in range(R.randint(8, 13))]
    n = sum(1 for x in items if x == (alvo, cor))
    if n < 1:
        return None
    pic = fig(relabel(k_pics.shapes_mix_svg(items, R.randint(1, 99999)), "figuras planas de várias cores"))
    nome = "%s %s" % (FORMAS[alvo][1], {"red": "vermelhos", "blue": "azuis", "yellow": "amarelos", "green": "verdes"}[cor])
    tot = sum(1 for x in items if x[0] == alvo)
    return mcq(pic + "Quantos %s há?" % nome, str(n), [str(tot) if tot != n else str(n + 2), str(n + 1), str(sum(1 for x in items if x[1] == cor)) if sum(1 for x in items if x[1] == cor) != n else str(n + 3)],
               "Conte só a forma e a cor pedidas: <b>%d</b>." % n)


CARIMBO = [("Se você passar tinta numa face de um dado (cubo) e carimbar no papel, que figura aparece?", "quadrado", ["círculo", "triângulo", "retângulo comprido"]),
           ("Se você contornar com lápis o fundo de uma lata (cilindro), que figura desenha?", "círculo", ["quadrado", "triângulo", "retângulo"]),
           ("Contornando a face maior de uma caixa de sapatos (bloco retangular), que figura aparece?", "retângulo", ["círculo", "triângulo", "quadrado de lados iguais"]),
           ("Carimbando uma face lateral de uma pirâmide, que figura aparece?", "triângulo", ["círculo", "quadrado", "retângulo"]),
           ("Contornando a base de um chapéu de festa (cone), que figura aparece?", "círculo", ["triângulo", "quadrado", "retângulo"]),
           ("Que figura plana você consegue carimbar com a base de uma pirâmide de base quadrada?", "quadrado", ["círculo", "retângulo comprido", "nenhuma"]),
           ("Uma bola (esfera) pode carimbar qual figura plana inteira?", "nenhuma, ela só toca o papel num ponto", ["círculo grande", "quadrado", "triângulo"])]


def s4_carimbo():
    q, a, w = R.choice(CARIMBO)
    return mcq(q, a, w, "A face que toca o papel deixa a sua forma. Resposta: <b>%s</b>." % a)


def ret_svg(w, h):
    return wrap(w + 20, h + 20, "<rect x='10' y='10' width='%d' height='%d' fill='#bfe0f5' stroke='%s' stroke-width='2'/>" % (w, h, INK), "uma figura de 4 lados")


def s4_qr():
    if R.random() < 0.5:
        w = h = R.choice([50, 60, 70, 80])
        ans = "quadrado"
    else:
        w, h = R.choice([(100, 50), (120, 60), (60, 110), (90, 40), (40, 90), (130, 70)])
        ans = "retângulo"
    return mcq(ret_svg(w, h) + "Esta figura tem 4 cantos retos. Os lados são %s. Ela é um quadrado ou um retângulo?" % ("todos do mesmo tamanho" if ans == "quadrado" else "dois mais compridos e dois mais curtos"), ans,
               ["quadrado" if ans == "retângulo" else "retângulo", "triângulo", "círculo"], "Resposta: <b>%s</b>." % ans)


OBJ = [("Uma pizza inteira vista de cima tem a forma de um…", "círculo", ["quadrado", "triângulo", "retângulo"]),
       ("A porta da sala de aula tem a forma de um…", "retângulo", ["círculo", "triângulo", "quadrado de lados iguais"]),
       ("Uma fatia de pizza tem a forma parecida com um…", "triângulo", ["quadrado", "círculo", "retângulo"]),
       ("Uma casa do jogo da velha tem a forma de um…", "quadrado", ["círculo", "triângulo", "retângulo comprido"]),
       ("Uma moeda tem a forma de um…", "círculo", ["quadrado", "triângulo", "retângulo"]),
       ("A tela de um celular tem a forma de um…", "retângulo", ["círculo", "triângulo", "quadrado de lados iguais"]),
       ("Uma placa de «dê a preferência» no trânsito tem a forma de um…", "triângulo", ["quadrado", "círculo", "retângulo"]),
       ("O telhado de uma casa desenhada na frente costuma ser um…", "triângulo", ["círculo", "quadrado", "retângulo"]),
       ("Um ladrilho de chão com 4 lados iguais tem a forma de um…", "quadrado", ["triângulo", "círculo", "retângulo comprido"]),
       ("O relógio de parede da escola costuma ter a forma de um…", "círculo", ["triângulo", "retângulo", "quadrado"])]


def s5_objeto():
    q, a, w = R.choice(OBJ)
    return mcq(q, a, w, "Resposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Nome das figuras planas", mix(R, seen, [(s1_nome, 12), (s1_letras, 8)])),
        ("Lados e cantos", mix(R, seen, [(s2_lados, 10), (s2_prop, 10)])),
        ("Contar figuras", mix(R, seen, [(s3_contar, 12), (s3_cor, 8)])),
        ("Faces dos sólidos e quadrado ou retângulo", mix(R, seen, [(s4_carimbo, 7), (s4_qr, 8), (s1_nome, 5)])),
        ("Figuras no dia a dia", mix(R, seen, [(s5_objeto, 10), (s2_prop, 2), (s1_letras, 8)])),
    ]
    body = lesson(
        ["O <b>círculo</b> é redondo: não tem lados retos nem cantos.",
         "O <b>triângulo</b> tem 3 lados e 3 cantos (vértices).",
         "O <b>quadrado</b> tem 4 lados iguais e 4 cantos retos. O <b>retângulo</b> tem 4 cantos retos e dois lados mais compridos.",
         "Girar a figura não muda o nome dela: um triângulo de ponta para baixo continua sendo triângulo."],
        [("Figura com 3 lados, de ponta para baixo", ["conte os lados: 3"], "triângulo"),
         ("Contorno da face de um dado", ["face quadrada"], "quadrado")],
        [["Achar que o quadrado girado vira outra figura", "Conte os lados e veja se são iguais."],
         ["Achar que só é triângulo se a ponta estiver para cima", "Qualquer figura fechada com 3 lados é triângulo."],
         ["Confundir quadrado e retângulo", "No quadrado, os 4 lados são iguais."]],
        fig(relabel(k_pics.lettered_shapes_svg([("circle", "red"), ("triangle", "yellow"), ("square", "blue"), ("rectangle", "green")]), "círculo, triângulo, quadrado e retângulo")))
    faq = [("Que figuras planas o 2º ano estuda?", "A BNCC pede reconhecer, comparar e nomear círculo, quadrado, retângulo e triângulo, em diferentes posições e também nos contornos das faces de sólidos."),
           ("Como praticar em casa?", "Carimbe com tinta as faces de caixas, latas e dados, ou contorne-as com lápis. Depois procure essas figuras em objetos da casa.")]
    make_unit(R, "figuras-geometricas-planas", "G", ["EF02MA15"],
              "Reconhecer, comparar e nomear figuras planas (círculo, quadrado, retângulo e triângulo), por meio de características comuns, em desenhos apresentados em diferentes disposições ou em contornos de faces de sólidos geométricos",
              "Figuras planas: círculo, quadrado, retângulo e triângulo", "Figuras planas",
              "Atividades de matemática para o 2º ano sobre figuras planas: círculo, quadrado, retângulo e triângulo, em posições diferentes, lados e cantos, contornos das faces de sólidos. 100 exercícios com gabarito.",
              "Triângulo: 3 lados. Quadrado e retângulo: 4 lados.", "Girar não muda o nome da figura.",
              body, faq, sets, 14, grade="2-ano")


if __name__ == "__main__":
    main()
