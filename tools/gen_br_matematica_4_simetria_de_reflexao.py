# -*- coding: utf-8 -*-
"""
Brasil Matemática 4º ano: Simetria de reflexão (Geometria, EF04MA19)
  python3 tools/gen_br_matematica_4_simetria_de_reflexao.py
Reconhecer figuras simétricas e o eixo de simetria na malha quadriculada; completar figuras por simetria; distância ao eixo;
letras e números com eixos de simetria; quantos eixos têm as figuras; a figura refletida é congruente à original.
Usa os desenhos da malha do gerador alemão (Klasse 3, Achsensymmetrie) com textos em português.
Erros: copiar a figura sem espelhar (deslocar), contar a distância errada até o eixo, achar que o retângulo tem eixos nas diagonais.
"""
import random
import gen_de_mathe_k3_achsensymmetrie as DE
from br_common import mcq, lesson, make_unit, mix, wrap, text, GREEN

R = random.Random(80415)
DE.R = random.Random(80956)
COLS, ROWS, Q = DE.COLS, DE.ROWS, DE.Q
L4 = "ABCD"


def four(figs):
    s = []
    for i, c in enumerate(figs):
        ox = 10 + i * 112
        s.append(DE.grid(ox, 10, c, True))
        s.append(text(ox + COLS * Q / 2.0, 10 + ROWS * Q + 24, L4[i], 16, col=GREEN))
    return wrap(10 + 4 * 112, 10 + ROWS * Q + 32, "".join(s), "quatro figuras A, B, C e D na malha quadriculada", lg=True)


def s1_qual():
    hs = [DE.half() for _ in range(4)]
    if not all(hs):
        return None
    good = DE.mirror(hs[0])
    bads = [DE.broken(DE.mirror(hs[1])), DE.shifted(hs[2]), DE.broken(DE.mirror(hs[3]))]
    if not all(bads) or any(b == DE.mirror({(x, y) for x, y in b if x < 3}) for b in bads):
        return None
    figs = bads + [good]
    R.shuffle(figs)
    k = figs.index(good)
    return mcq(four(figs) + "Qual figura é simétrica em relação à linha vermelha?", L4[k], [L4[i] for i in range(4) if i != k],
               "Só na figura <b>%s</b> os quadradinhos estão à mesma distância do eixo, dos dois lados: dobrando a folha na linha, as duas metades coincidem." % L4[k])


def s2_completar():
    h = DE.half()
    if not h:
        return None
    good = DE.mirror(h)
    sh = DE.shifted(h)
    near = DE.broken(good)
    flipped = set(h) | {(COLS - 1 - x, ROWS - 1 - y) for x, y in h}
    opts = [good, sh, near, flipped]
    if not near or len({frozenset(o) for o in opts}) < 4:
        return None
    pic = wrap(COLS * Q + 20, ROWS * Q + 20, DE.grid(10, 10, h), "metade de uma figura e o eixo de simetria")
    R.shuffle(opts)
    k = opts.index(good)
    return mcq(pic + "Esta é a metade esquerda de uma figura. Qual desenho mostra a figura completada por simetria?" + four(opts), L4[k], [L4[i] for i in range(4) if i != k],
               "Cada quadradinho vai para o outro lado do eixo, à mesma distância. É o desenho <b>%s</b>." % L4[k])


def qd(n):
    return "%d quadradinho%s" % (n, "" if n == 1 else "s")


def s2_distancia():
    if R.random() < 0.5:
        n = R.randint(2, 6)
        side, other = R.choice([("à esquerda", "à direita"), ("à direita", "à esquerda")])
        ans = "%s %s do eixo" % (qd(n), other)
        return mcq("Um ponto está a %s %s de um eixo de simetria vertical. Onde fica o seu simétrico?" % (qd(n), side), ans,
                   ["%s %s do eixo" % (qd(n), side), "%s %s do eixo" % (qd(n + 1), other), "%s %s do eixo" % (qd(2 * n), other)],
                   "O simétrico fica à mesma distância, do outro lado: <b>%s</b>." % ans)
    n = R.randint(1, 7)
    return mcq("Um ponto está a %s do eixo. Quantos quadradinhos há entre o ponto e o seu simétrico?" % qd(n), qd(2 * n), [qd(n), qd(n + 1), qd(2 * n + 2)],
               "%d até o eixo e mais %d do outro lado: <b>%s</b>." % (n, n, qd(2 * n)))


VERT = list("AHIMOTUVWXY")
HORI = list("BCDEHIKOX")
NONE = list("FGJLNPQRSZ")


def s3_letras():
    kind = R.choice(["v", "v", "h", "n"])
    if kind == "v":
        a, w = R.choice(VERT), R.sample(NONE, 3)
        q = "Qual letra tem um eixo de simetria <b>vertical</b>: %s?" % ", ".join(sorted([a] + w))
        e = "Dobrando %s numa linha vertical no meio, as duas metades coincidem: <b>%s</b>." % (a, a)
    elif kind == "h":
        a, w = R.choice([x for x in HORI if x not in VERT]), R.sample(NONE, 3)
        q = "Qual letra tem um eixo de simetria <b>horizontal</b>: %s?" % ", ".join(sorted([a] + w))
        e = "Em %s, a metade de cima e a de baixo coincidem: <b>%s</b>." % (a, a)
    else:
        a, w = R.choice(NONE), R.sample(VERT + [x for x in HORI if x not in VERT], 3)
        q = "Qual letra <b>não</b> tem eixo de simetria: %s?" % ", ".join(sorted([a] + w))
        e = "%s não tem eixo de simetria; as outras letras podem ser dobradas em duas metades iguais: <b>%s</b>." % (a, a)
    return mcq(q, a, w, e)


EIXOS = [("um quadrado", "4"), ("um retângulo (que não é quadrado)", "2"), ("um triângulo com os 3 lados iguais", "3"), ("um círculo", "infinitos"),
         ("um coração", "1"), ("uma borboleta", "1"), ("um hexágono regular", "6"), ("a letra H", "2"), ("a letra A", "1"), ("a letra F", "nenhum"),
         ("o número 8", "2"), ("o número 3", "1"), ("um losango (que não é quadrado)", "2"), ("a letra X", "2")]


def s3_eixos():
    thing, ans = R.choice(EIXOS)
    near = {"4": ["2", "8"], "2": ["4", "1"], "3": ["1", "6"], "infinitos": ["1", "4"], "1": ["2", "nenhum"], "6": ["3", "12"], "nenhum": ["1", "2"]}[ans]
    rest = [x for x in ["nenhum", "1", "2", "3", "4", "6", "infinitos"] if x != ans and x not in near]
    R.shuffle(rest)
    return mcq("Quantos eixos de simetria tem %s?" % thing, ans, near + rest,
               "%s tem <b>%s</b> %s de simetria." % (thing[0].upper() + thing[1:], ans, "eixo" if ans in ("1", "nenhum") else "eixos"))


IDEIAS = [("Uma figura e o seu reflexo num eixo de simetria são…", "congruentes (iguais em forma e tamanho)", ["de tamanhos diferentes", "sempre de cores diferentes", "uma maior que a outra"]),
          ("Para verificar se uma figura é simétrica, podemos…", "dobrar a folha no eixo e ver se as metades coincidem", ["medir só um lado", "contar as cores", "girar a folha"]),
          ("Num espelho, a sua mão direita aparece…", "do lado esquerdo da imagem", ["do lado direito da imagem", "em cima", "embaixo"]),
          ("O eixo de simetria divide a figura em…", "duas partes iguais que se encaixam ao dobrar", ["duas partes de tamanhos diferentes", "quatro partes sempre", "três partes"]),
          ("Um ponto que está em cima do eixo de simetria, no reflexo, fica…", "no mesmo lugar", ["1 quadradinho ao lado", "do outro lado da folha", "longe do eixo"]),
          ("A diagonal de um retângulo comprido é um eixo de simetria?", "Não: dobrando na diagonal, as metades não coincidem", ["Sim, sempre", "Sim, se for colorido", "Só às vezes"]),
          ("Qual destas imagens costuma ser simétrica?", "o rosto de frente de um gato", ["uma mão vista de lado", "uma árvore torta", "uma nuvem"]),
          ("Ao refletir uma figura, o que muda?", "o lado para onde ela está virada", ["o tamanho", "a forma", "o número de lados"])]


def s4_ideia():
    q, a, w = R.choice(IDEIAS)
    return mcq(q, a, w, "Na simetria de reflexão, a figura «se vira» como num espelho, mas continua com a mesma forma e o mesmo tamanho. Resposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Qual figura é simétrica?", mix(R, seen, [(s1_qual, 20)])),
        ("Completar por simetria", mix(R, seen, [(s2_completar, 14), (s2_distancia, 6)])),
        ("Distância até o eixo", mix(R, seen, [(s2_distancia, 8), (s4_ideia, 8), (s2_completar, 4)])),
        ("Letras e números simétricos", mix(R, seen, [(s3_letras, 20)])),
        ("Eixos de simetria", mix(R, seen, [(s3_eixos, 12), (s1_qual, 8)])),
    ]
    body = lesson(
        ["Uma figura tem <b>simetria de reflexão</b> quando, dobrando-a numa linha (o <b>eixo de simetria</b>), as duas metades coincidem.",
         "Na malha quadriculada, cada quadradinho tem um simétrico do outro lado do eixo, <b>à mesma distância</b>.",
         "A figura refletida é <b>congruente</b> à original: tem a mesma forma e o mesmo tamanho, só que virada, como num espelho.",
         "Algumas figuras têm vários eixos: o quadrado tem 4; o retângulo comprido tem 2; o círculo tem infinitos."],
        [("Um quadradinho está a 3 casas à esquerda do eixo. Onde fica o simétrico?", ["mesma distância", "do outro lado"], "3 casas à direita do eixo"),
         ("Quantos eixos de simetria tem a letra H?", ["um vertical", "um horizontal"], "2")],
        [["Copiar a metade sem espelhar (deslocar)", "O que está perto do eixo continua perto do eixo do outro lado."],
         ["Contar a distância a partir da borda", "Conte sempre a partir do eixo."],
         ["Achar que as diagonais do retângulo são eixos", "Dobre e confira: as metades não coincidem."]])
    faq = [("O que é simetria de reflexão?", "É quando uma figura pode ser dobrada numa linha e as duas metades coincidem, como a imagem num espelho. A linha é o eixo de simetria."),
           ("Por que usar malha quadriculada?", "A malha ajuda a contar a distância de cada parte até o eixo e a desenhar o simétrico no lugar certo, como a BNCC indica para o 4º ano.")]
    make_unit(R, "simetria-de-reflexao", "G", ["EF04MA19"],
              "Reconhecer simetria de reflexão em figuras e em pares de figuras geométricas planas e utilizá-la na construção de figuras congruentes, com o uso de malhas quadriculadas e de softwares de geometria",
              "Simetria de reflexão: eixos e figuras simétricas", "Simetria",
              "Atividades de matemática para o 4º ano sobre simetria de reflexão: figuras simétricas na malha quadriculada, completar por simetria, eixos de simetria, letras e números simétricos. 100 exercícios com gabarito.",
              "Dobrando no eixo, as duas metades coincidem.", "O simétrico fica à mesma distância do eixo.",
              body, faq, sets, 15, grade="4-ano")


if __name__ == "__main__":
    main()
