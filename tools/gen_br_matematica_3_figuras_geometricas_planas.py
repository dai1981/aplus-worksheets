# -*- coding: utf-8 -*-
"""
Brasil Matemática 3º ano: Figuras geométricas planas (Geometria, EF03MA15, EF03MA16)
  python3 tools/gen_br_matematica_3_figuras_geometricas_planas.py
Triângulo, quadrado, retângulo, trapézio, paralelogramo (e losango, pentágono, hexágono); lados e vértices;
lados paralelos e de mesmo comprimento; classificar e comparar; figuras congruentes na malha quadriculada.
Erros: achar que o quadrado girado vira losango, contar vértices e lados diferentes, achar que figuras do mesmo
tipo são sempre congruentes.
"""
import math
import random
import gen_fr_maths_ce2_figures_planes_et_angles_droits as FRF
from br_common import mcq, lesson, make_unit, mix, wrap, line, INK, GREEN, FILL, relabel, text

R = random.Random(80315)
FRF.R = random.Random(80915)
PT = {"carré": "quadrado", "rectangle": "retângulo", "losange": "losango", "triangle rectangle": "triângulo retângulo", "triangle": "triângulo",
      "pentagone": "pentágono", "hexagone": "hexágono", "trapeze": "trapézio", "para": "paralelogramo"}
ART = {n: "um " + n for n in PT.values()}
CONF = {"quadrado": ["um losango", "um retângulo"], "retângulo": ["um quadrado", "um paralelogramo"], "losango": ["um quadrado", "um trapézio"],
        "triângulo retângulo": ["um triângulo", "um retângulo"], "triângulo": ["um triângulo retângulo", "um trapézio"],
        "pentágono": ["um hexágono", "um quadrado"], "hexágono": ["um pentágono", "um losango"],
        "trapézio": ["um paralelogramo", "um retângulo"], "paralelogramo": ["um retângulo", "um trapézio"]}
WHY = {"quadrado": "4 lados iguais e 4 cantos retos", "retângulo": "4 cantos retos e os lados opostos iguais", "losango": "4 lados iguais, sem cantos retos",
       "triângulo retângulo": "3 lados e um canto reto", "triângulo": "3 lados", "pentágono": "5 lados", "hexágono": "6 lados",
       "trapézio": "4 lados e só um par de lados paralelos", "paralelogramo": "4 lados, com os lados opostos paralelos e iguais, sem cantos retos"}
NL = {"quadrado": 4, "retângulo": 4, "losango": 4, "triângulo retângulo": 3, "triângulo": 3, "pentágono": 5, "hexágono": 6, "trapézio": 4, "paralelogramo": 4}


def shape(k):
    if k == "trapeze":
        b, t, h = R.randint(150, 190), R.randint(60, 100), R.randint(60, 90)
        off = R.randint(10, b - t - 10)
        p = [(0, h), (b, h), (off + t, 0), (off, 0)]
        s = FRF.poly(FRF.rot(p, R.choice([0, 0, 0.3, -0.3])), "x")
    elif k == "para":
        b, h, off = R.randint(110, 150), R.randint(55, 85), R.randint(35, 60)
        p = [(0, h), (b, h), (b + off, 0), (off, 0)]
        s = FRF.poly(FRF.rot(p, R.choice([0, 0, 0.25, -0.25])), "x")
    else:
        s = FRF.shape(k)
    return relabel(s, "uma figura plana")


def s1_nome():
    k = R.choice(sorted(PT))
    n = PT[k]
    w = CONF[n] + [ART[x] for x in sorted(ART) if ART[x] not in CONF[n] and x != n]
    return mcq(shape(k) + "Qual é o nome desta figura?", ART[n], w, "Esta figura tem %s: é <b>%s</b>." % (WHY[n], ART[n]))


def s1_conta():
    k = R.choice(sorted(PT))
    n = PT[k]
    v = NL[n]
    word = R.choice(["lados", "vértices"])
    return mcq(shape(k) + "Quantos %s tem esta figura?" % word, str(v), [str(x) for x in (v - 1, v + 1, v + 2, 2 * v) if x != v and x > 0],
               "Conte os %s: <b>%d</b>. Um polígono tem o mesmo número de lados e de vértices." % (word, v))


PROP = [("Quantos lados tem um pentágono?", "5", ["6", "4", "8"]), ("Quantos lados tem um hexágono?", "6", ["5", "8", "4"]),
        ("Quantos vértices tem um triângulo?", "3", ["4", "2", "6"]), ("Quantos vértices tem um trapézio?", "4", ["3", "5", "6"]),
        ("Que figura tem 4 lados iguais e 4 cantos retos?", "o quadrado", ["o losango", "o retângulo", "o trapézio"]),
        ("Que figura tem 4 lados iguais, mas nenhum canto reto?", "o losango", ["o quadrado", "o retângulo", "o trapézio"]),
        ("Que figura tem 4 cantos retos, dois lados compridos e dois curtos?", "o retângulo", ["o quadrado", "o losango", "o trapézio"]),
        ("Que figura de 4 lados tem só um par de lados paralelos?", "o trapézio", ["o paralelogramo", "o retângulo", "o quadrado"]),
        ("Que figura tem os lados opostos paralelos e iguais, mas não tem cantos retos?", "o paralelogramo", ["o trapézio", "o retângulo", "o quadrado"]),
        ("Como se chama uma figura fechada formada só por segmentos de reta?", "polígono", ["círculo", "reta", "sólido"]),
        ("O círculo é um polígono?", "não, o contorno dele é curvo", ["sim, tem muitos lados", "sim, é uma figura fechada", "só se for grande"]),
        ("O quadrado também é um retângulo?", "sim, tem 4 cantos retos", ["não, nunca", "só se for grande", "sim, porque tem 3 lados"]),
        ("Como se chama um polígono de 3 lados?", "triângulo", ["quadrilátero", "pentágono", "hexágono"]),
        ("Como se chama o ponto onde dois lados se encontram?", "vértice", ["centro", "aresta", "face"]),
        ("A placa de PARE tem a forma de um…", "octógono (8 lados)", ["hexágono", "pentágono", "quadrado"]),
        ("Os favos de mel das abelhas têm a forma de um…", "hexágono", ["pentágono", "quadrado", "triângulo"]),
        ("Quantos lados têm juntos 2 triângulos e 1 quadrado?", "10", ["7", "9", "12"]),
        ("Um quadrilátero é qualquer figura com…", "4 lados", ["4 cantos retos", "4 lados iguais", "3 lados"])]


def s2_prop():
    q, a, w = R.choice(PROP)
    return mcq(q, a, w, "Resposta: <b>%s</b>." % a)


def lista(xs):
    xs = list(xs)
    R.shuffle(xs)
    return ", ".join(xs[:-1]) + " ou " + xs[-1]


def s2_classifica():
    k = R.choice(["4l", "3l", "paral", "reto"])
    if k == "4l":
        good = R.choice(["quadrado", "retângulo", "trapézio", "paralelogramo", "losango"])
        bad = R.sample(["triângulo", "pentágono", "hexágono", "triângulo retângulo"], 3)
        why = "O %s tem 4 lados: <b>é um quadrilátero</b>." % good
        q = "Qual destas figuras é um quadrilátero (tem 4 lados): %s?"
    elif k == "3l":
        good = R.choice(["triângulo", "triângulo retângulo"])
        bad = R.sample(["quadrado", "pentágono", "trapézio", "losango", "hexágono"], 3)
        why = "Os triângulos têm 3 lados e 3 vértices: <b>o %s</b>." % good
        q = "Qual destas figuras tem exatamente 3 vértices: %s?"
    elif k == "paral":
        good = R.choice(["retângulo", "quadrado", "paralelogramo", "losango"])
        bad = R.sample(["trapézio", "triângulo", "pentágono", "triângulo retângulo"], 3)
        why = "O %s tem os lados opostos paralelos (dois pares). O trapézio tem só um par: <b>o %s</b>." % (good, good)
        q = "Qual destas figuras tem dois pares de lados paralelos: %s?"
    else:
        good = R.choice(["retângulo", "quadrado"])
        bad = R.sample(["losango", "paralelogramo", "trapézio", "pentágono", "triângulo"], 3)
        why = "Quadrado e retângulo têm 4 cantos retos: <b>o %s</b>." % good
        q = "Qual destas figuras tem 4 cantos retos: %s?"
    opts = ["o " + x for x in [good] + bad]
    return mcq(q % lista(opts), opts[0], opts[1:], why)


CELL = 18


def malha(polys, W, H, labels):
    s = []
    for x in range(W + 1):
        s.append(line(6 + x * CELL, 6, 6 + x * CELL, 6 + H * CELL, "#d0dbe6", 1))
    for y in range(H + 1):
        s.append(line(6, 6 + y * CELL, 6 + W * CELL, 6 + y * CELL, "#d0dbe6", 1))
    for (pts, lab) in zip(polys, labels):
        s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (" ".join("%d,%d" % (6 + x * CELL, 6 + y * CELL) for x, y in pts), FILL, GREEN))
        cx = sum(x for x, _ in pts) / float(len(pts))
        cy = sum(y for _, y in pts) / float(len(pts))
        s.append(text(6 + cx * CELL, 6 + cy * CELL + 5, lab, 14, col=INK))
    return wrap(W * CELL + 12, H * CELL + 12, "".join(s), "figuras na malha quadriculada", lg=True)


def base_shape():
    k = R.choice(["ret", "tri", "trap", "L"])
    if k == "ret":
        w, h = R.randint(2, 4), R.randint(2, 3)
        return [(0, 0), (w, 0), (w, h), (0, h)]
    if k == "tri":
        w, h = R.randint(2, 4), R.randint(2, 3)
        return [(0, h), (w, h), (0, 0)]
    if k == "trap":
        return [(0, 2), (4, 2), (3, 0), (1, 0)]
    return [(0, 0), (2, 0), (2, 1), (3, 1), (3, 3), (0, 3)]


def variants(p):
    w = max(x for x, _ in p)
    h = max(y for _, y in p)
    flip = [(w - x, y) for x, y in p]
    rot = [(h - y, x) for x, y in p]
    big = [(2 * x, 2 * y) for x, y in p]
    stretch = [(x + (1 if x == w else 0), y) for x, y in p]
    taller = [(x, y + (1 if y == h else 0)) for x, y in p]
    return flip, rot, big, stretch, taller


def place(polys):
    out, ox = [], 1
    for pts in polys:
        out.append([(x + ox, y + 1) for x, y in pts])
        ox += max(x for x, _ in pts) + 2
    return out, ox, max(max(y for _, y in p) for p in polys) + 2


def s3_congruente():
    p = base_shape()
    flip, rot, big, stretch, taller = variants(p)
    good = R.choice([flip, rot, list(p)])
    bad = R.sample([big, stretch, taller], 2)
    if max(max(x for x, _ in q) for q in [big]) > 8:
        bad = [stretch, taller]
    cands = [good] + bad
    order = R.sample(range(3), 3)
    shown = [p] + [cands[i] for i in order]
    pls, W, H = place(shown)
    labs = ["M", "A", "B", "C"]
    k = labs[1 + order.index(0)]
    return mcq(malha(pls, W, H, labs) + "Qual figura é congruente à figura M (mesma forma e mesmo tamanho, mesmo que esteja virada)?", "a figura %s" % k,
               ["a figura %s" % x for x in "ABC" if x != k] + ["nenhuma"],
               "Recorte M e coloque por cima: só %s se encaixa perfeitamente (girar ou virar não muda o tamanho). Resposta: <b>a figura %s</b>." % (k, k))


def s3_lados():
    k = R.choice(["ret", "quad", "tri", "trap"])
    if k == "ret":
        a, b = R.randint(3, 9), R.randint(2, 6)
        if a == b:
            return None
        return mcq("Um retângulo tem um lado de %d cm e outro de %d cm. Quanto medem os outros dois lados?" % (a, b), "%d cm e %d cm" % (a, b),
                   ["%d cm e %d cm" % (a, a), "%d cm e %d cm" % (b, b), "%d cm e %d cm" % (a + b, a + b)],
                   "No retângulo, os lados opostos são iguais: <b>%d cm e %d cm</b>." % (a, b))
    if k == "quad":
        a = R.randint(2, 12)
        return mcq("Um lado de um quadrado mede %d cm. Quanto medem os outros lados?" % a, "%d cm cada um" % a,
                   ["%d cm cada um" % (2 * a), "%d cm cada um" % (a + 1), "não dá para saber"],
                   "No quadrado, os 4 lados são iguais: <b>%d cm cada um</b>." % a)
    if k == "tri":
        a = R.randint(3, 9)
        return mcq("Um triângulo tem os 3 lados iguais e um deles mede %d cm. Quanto mede o contorno?" % a, "%d cm" % (3 * a),
                   ["%d cm" % a, "%d cm" % (4 * a), "%d cm" % (2 * a)], "%d + %d + %d = <b>%d cm</b>." % (a, a, a, 3 * a))
    a, b, c = R.randint(8, 14), R.randint(3, 6), R.randint(4, 7)
    return mcq("Um trapézio tem lados de %d cm, %d cm, %d cm e %d cm. Quanto mede o contorno?" % (a, c, b, c), "%d cm" % (a + b + 2 * c),
               ["%d cm" % (a + b + c), "%d cm" % (a + b), "%d cm" % (a + b + 2 * c + 1)],
               "%d + %d + %d + %d = <b>%d cm</b>." % (a, c, b, c, a + b + 2 * c))


def s4_compor():
    T = [("Juntando 2 triângulos retângulos iguais pelo lado maior, que figura se pode formar?", "um retângulo", ["um pentágono", "um círculo", "um hexágono"]),
         ("Cortando um quadrado ao meio, de um canto ao canto oposto, que figuras se formam?", "2 triângulos", ["2 quadrados", "2 retângulos", "4 triângulos"]),
         ("Cortando um retângulo ao meio, pela linha do meio, que figuras se formam?", "2 retângulos", ["2 triângulos", "2 losangos", "2 hexágonos"]),
         ("Juntando 2 quadrados iguais lado a lado, que figura se forma?", "um retângulo", ["um quadrado maior", "um losango", "um trapézio"]),
         ("Quantos triângulos iguais formam um hexágono como o dos favos de mel?", "6", ["3", "4", "8"]),
         ("Juntando 3 triângulos iguais lado a lado, de ponta para cima e para baixo, que figura se forma?", "um trapézio", ["um quadrado", "um círculo", "um pentágono"]),
         ("Juntando 4 quadrados iguais em 2 linhas de 2, que figura se forma?", "um quadrado maior", ["um retângulo comprido", "um losango", "um triângulo"]),
         ("Juntando 2 trapézios iguais pela base maior, que figura se pode formar?", "um hexágono", ["um quadrado", "um triângulo", "um círculo"])]
    q, a, w = R.choice(T)
    return mcq(q, a, w, "Desenhe na malha ou recorte papel para ver: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Nome das figuras planas", mix(R, seen, [(s1_nome, 14), (s1_conta, 6)])),
        ("Lados e vértices", mix(R, seen, [(s1_conta, 8), (s2_prop, 12)])),
        ("Classificar e comparar", mix(R, seen, [(s2_classifica, 12), (s3_lados, 8)])),
        ("Figuras congruentes", mix(R, seen, [(s3_congruente, 14), (s2_prop, 6)])),
        ("Compor e decompor figuras", mix(R, seen, [(s4_compor, 8), (s3_lados, 8), (s1_nome, 4)])),
    ]
    body = lesson(
        ["Um <b>polígono</b> é uma figura plana fechada feita de segmentos de reta. Ele tem o mesmo número de <b>lados</b> e de <b>vértices</b>.",
         "Quadriláteros têm 4 lados: <b>quadrado</b> (4 lados iguais e 4 cantos retos), <b>retângulo</b> (4 cantos retos), <b>paralelogramo</b> (lados opostos paralelos), <b>trapézio</b> (só um par de lados paralelos).",
         "Girar ou virar uma figura não muda o nome dela: um quadrado inclinado continua sendo quadrado.",
         "Figuras <b>congruentes</b> têm a mesma forma e o mesmo tamanho: uma se encaixa perfeitamente na outra."],
        [("Um retângulo tem lados de 6 cm e 3 cm. E os outros?", ["Lados opostos iguais"], "6 cm e 3 cm"),
         ("Trapézio ou paralelogramo?", ["Só um par de lados paralelos"], "trapézio")],
        [["Achar que o quadrado girado é losango", "Se tem 4 cantos retos e 4 lados iguais, é quadrado em qualquer posição."],
         ["Achar que todos os triângulos são congruentes", "Congruentes precisam ter também o mesmo tamanho."],
         ["Confundir trapézio e paralelogramo", "O paralelogramo tem dois pares de lados paralelos; o trapézio, só um."]])
    faq = [("Quais figuras planas a BNCC pede no 3º ano?", "Triângulo, quadrado, retângulo, trapézio e paralelogramo, classificados e comparados pelos lados (quantidade, posição e comprimento) e pelos vértices."),
           ("O que são figuras congruentes?", "São figuras com a mesma forma e o mesmo tamanho. Para conferir, recorte uma e veja se ela cobre a outra exatamente, mesmo que precise girar ou virar.")]
    make_unit(R, "figuras-geometricas-planas", "G", ["EF03MA15", "EF03MA16"],
              "Classificar e comparar figuras planas (triângulo, quadrado, retângulo, trapézio e paralelogramo) em relação a seus lados (quantidade, posições relativas e comprimento) e vértices; reconhecer figuras congruentes, usando sobreposição e desenhos em malhas quadriculadas ou triangulares",
              "Figuras geométricas planas: lados, vértices e congruência", "Figuras geométricas planas",
              "Atividades de matemática para o 3º ano sobre figuras geométricas planas: triângulo, quadrado, retângulo, trapézio e paralelogramo, lados e vértices, classificar, figuras congruentes na malha quadriculada. 100 exercícios com gabarito.",
              "Polígono: mesmo número de lados e de vértices.", "Congruentes: mesma forma e mesmo tamanho.",
              body, faq, sets, 15)


if __name__ == "__main__":
    main()
