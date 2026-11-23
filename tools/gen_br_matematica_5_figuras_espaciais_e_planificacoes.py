# -*- coding: utf-8 -*-
"""
Brasil Matemática 5º ano: Figuras espaciais e planificações (Geometria, EF05MA16)
  python3 tools/gen_br_matematica_5_figuras_espaciais_e_planificacoes.py
Prismas e pirâmides de base triangular, quadrada, pentagonal e hexagonal; cilindro e cone; nome pela base;
faces, arestas e vértices (prisma: n + 2, 3n, 2n; pirâmide: n + 1, 2n, n + 1); planificações; comparar prismas e pirâmides.
Erros: chamar todo prisma de cubo, contar só as faces laterais, confundir cone com pirâmide, esquecer as arestas escondidas.
"""
import math
import random
import gen_br_matematica_3_figuras_geometricas_espaciais as BR3
from br_common import mcq, lesson, make_unit, mix, wrap, line, INK, GREEN, table

R = random.Random(80515)
BR3.R = random.Random(80915)
BR3.DE.R = random.Random(80916)
BASE = {3: ("triangular", "triângulo"), 4: ("quadrangular", "quadrilátero"), 5: ("pentagonal", "pentágono"), 6: ("hexagonal", "hexágono")}
COL = ["#cfe6d6", "#f6d6a8", "#c9dcf2", "#f2c6d0", "#e8e0a8"]


def nome(kind, n):
    return "%s de base %s" % ("prisma" if kind == "prisma" else "pirâmide", BASE[n][0])


def art(kind, n):
    return ("o " if kind == "prisma" else "a ") + nome(kind, n)


def fav(kind, n):
    return (n + 2, 3 * n, 2 * n) if kind == "prisma" else (n + 1, 2 * n, n + 1)


def solido(kind, n, col):
    """prisma ou pirâmide em perspectiva; arestas escondidas tracejadas"""
    cx, cy, rx, ry, h = 110, 150, 78, 26, 110
    rot = R.uniform(0.1, 0.5)
    base = [(cx + rx * math.cos(2 * math.pi * i / n + rot), cy + ry * math.sin(2 * math.pi * i / n + rot)) for i in range(n)]
    back = [math.sin(2 * math.pi * i / n + rot) < -0.05 for i in range(n)]
    s = []
    dash = " stroke-dasharray='5 4'"
    if kind == "prisma":
        top = [(x, y - h) for x, y in base]
        s.append("<polygon points='%s' fill='%s' stroke='none'/>" % (" ".join("%.1f,%.1f" % p for p in top), col))
        for i in range(n):
            j = (i + 1) % n
            hid = back[i] and back[j]
            s.append(line(base[i][0], base[i][1], base[j][0], base[j][1], INK, 2, dash if hid else ""))
            s.append(line(top[i][0], top[i][1], top[j][0], top[j][1], INK, 2))
            s.append(line(base[i][0], base[i][1], top[i][0], top[i][1], INK, 2, dash if back[i] else ""))
    else:
        ap = (cx, cy - h - 10)
        for i in range(n):
            j = (i + 1) % n
            hid = back[i] and back[j]
            s.append(line(base[i][0], base[i][1], base[j][0], base[j][1], INK, 2, dash if hid else ""))
            s.append(line(base[i][0], base[i][1], ap[0], ap[1], INK, 2, dash if back[i] else ""))
    return wrap(220, 186, "".join(s), "figura geométrica espacial")


def poly(cx, cy, r, n, rot=-math.pi / 2):
    return [(cx + r * math.cos(rot + 2 * math.pi * i / n), cy + r * math.sin(rot + 2 * math.pi * i / n)) for i in range(n)]


def pg(pts, col):
    return "<polygon points='%s' fill='%s' stroke='%s' stroke-width='1.6'/>" % (" ".join("%.1f,%.1f" % p for p in pts), col, INK)


def planif(kind, n, col):
    """planificação de um prisma (n retângulos + 2 bases) ou de uma pirâmide (base + n triângulos)"""
    s = []
    if kind == "prisma":
        a, h = 40, 60

        def walk(x, y, sign):
            pts, th = [], 0.0
            for _ in range(n):
                pts.append((x, y))
                x, y = x + a * math.cos(th), y + a * math.sin(th)
                th += sign * 2 * math.pi / n
            return pts
        top = walk(0, 0, -1)
        bot = walk(0, h, 1)
        ys = [y for _, y in top + bot]
        y_off = 8 - min(ys)
        x0 = 10
        for i in range(n):
            s.append(pg([(x0 + i * a, y_off), (x0 + (i + 1) * a, y_off), (x0 + (i + 1) * a, y_off + h), (x0 + i * a, y_off + h)], col))
        s.append(pg([(x0 + x, y_off + y) for x, y in top], col))
        s.append(pg([(x0 + x, y_off + y) for x, y in bot], col))
        return wrap(x0 * 2 + n * a, int(y_off + max(ys) + 8), "".join(s), "planificação de uma figura espacial")
    a = 50
    r = a / (2 * math.sin(math.pi / n))
    cx = cy = 120
    P = poly(cx, cy, r, n)
    s.append(pg(P, col))
    for i in range(n):
        p1, p2 = P[i], P[(i + 1) % n]
        mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        dx, dy = mx - cx, my - cy
        d = math.hypot(dx, dy)
        tip = (mx + dx / d * 52, my + dy / d * 52)
        s.append(pg([p1, p2, tip], "#fff"))
    return wrap(240, 240, "".join(s), "planificação de uma figura espacial")


def s1_nome():
    kind = R.choice(["prisma", "piramide"])
    n = R.choice([3, 4, 5, 6])
    ans = nome(kind, n)
    w = [nome("piramide" if kind == "prisma" else "prisma", n)] + [nome(kind, m) for m in sorted(BASE, key=lambda m: abs(m - n)) if m != n][:2]
    return mcq(solido(kind, n, R.choice(COL)) + "Qual é o nome desta figura?", ans, w,
               "%s A base é um %s: é %s." % ("Tem duas bases iguais e faces laterais retangulares." if kind == "prisma" else "Tem uma base e faces laterais triangulares que se encontram num vértice.",
                                              BASE[n][1], "<b>%s</b>" % art(kind, n)))


def s1_base():
    kind = R.choice(["prisma", "piramide"])
    n = R.choice([3, 4, 5, 6])
    k = R.choice(["base", "lat"])
    if k == "base":
        return mcq("Que forma tem a base %s?" % ("do " + nome(kind, n) if kind == "prisma" else "da " + nome(kind, n)), BASE[n][1], [BASE[m][1] for m in BASE if m != n],
                   "O nome diz a base: %s → <b>%s</b>." % (BASE[n][0], BASE[n][1]))
    ans = "retângulos" if kind == "prisma" else "triângulos"
    return mcq("Que forma têm as faces laterais %s?" % ("do " + nome(kind, n) if kind == "prisma" else "da " + nome(kind, n)), ans,
               ["triângulos" if kind == "prisma" else "retângulos", BASE[n][1] + "s", "círculos", "hexágonos"],
               "Num prisma, as faces laterais são retângulos; numa pirâmide, são triângulos. <b>%s</b>." % ans)


def s2_contar():
    kind = R.choice(["prisma", "piramide"])
    n = R.choice([3, 4, 5, 6])
    i = R.randrange(3)
    word = ["faces", "arestas", "vértices"][i]
    F, A, V = fav(kind, n)
    v = (F, A, V)[i]
    pic = solido(kind, n, R.choice(COL)) if R.random() < 0.6 else ""
    others = [F, A, V, v + 1, v - 1, (n if i == 0 else n * 2 if i == 1 else n)]
    return mcq(pic + "Quant%s %s tem %s?" % ("as" if i < 2 else "os", word, art(kind, n)), str(v), [str(x) for x in others if x != v and x > 0],
               "%s tem %d faces, %d arestas e %d vértices. <b>%d %s</b>." % (art(kind, n)[0].upper() + art(kind, n)[1:], F, A, V, v, word))


def s2_qual():
    kind = R.choice(["prisma", "piramide"])
    n = R.choice([3, 4, 5, 6])
    F, A, V = fav(kind, n)
    q = "Que figura tem %d faces, %d arestas e %d vértices?" % (F, A, V)
    cands = [art(k, m) for k in ("prisma", "piramide") for m in (3, 4, 5, 6) if (k, m) != (kind, n)]
    near = sorted(cands, key=lambda c: (abs(int(fav("prisma" if c.startswith("o ") else "piramide", [m for m in BASE if BASE[m][0] in c][0])[1]) - A), R.random()))
    return mcq(q, art(kind, n), near[:3], "%s: %d faces, %d arestas e %d vértices. <b>%s</b>." % (art(kind, n)[0].upper() + art(kind, n)[1:], F, A, V, art(kind, n)))


def s3_planif():
    kind = R.choice(["prisma", "piramide"])
    n = R.choice([3, 4, 5, 6])
    if kind == "prisma" and n == 4 and R.random() < 0.5:
        return None
    pic = planif(kind, n, R.choice(COL))
    ans = art(kind, n)
    w = [art("piramide" if kind == "prisma" else "prisma", n)] + [art(kind, m) for m in sorted(BASE, key=lambda m: abs(m - n)) if m != n][:2]
    return mcq(pic + "Que figura espacial se forma ao dobrar esta planificação?", ans, w,
               "%s → <b>%s</b>." % ("%d retângulos e 2 %ss" % (n, BASE[n][1]) if kind == "prisma" else "1 %s e %d triângulos" % (BASE[n][1], n), ans))


def s3_texto():
    it = BR3.s3_plan() if R.random() < 0.5 else BR3.s3_cubo()
    return it


def s4_comparar():
    k = R.choice(range(8))
    if k == 0:
        return mcq("O que um prisma tem e uma pirâmide não tem?", "duas bases iguais e paralelas", ["faces planas", "arestas", "vértices"],
                   "O prisma tem duas bases iguais; a pirâmide tem uma base e um vértice no alto. Resposta: <b>duas bases iguais e paralelas</b>.")
    if k == 1:
        return mcq("Qual é a diferença entre o cone e a pirâmide?", "a base do cone é um círculo", ["o cone tem duas bases", "a pirâmide não tem vértice", "a pirâmide rola"],
                   "Os dois têm um vértice no alto, mas o cone tem base redonda e superfície curva. Resposta: <b>a base do cone é um círculo</b>.")
    if k == 2:
        return mcq("O cubo é um tipo de…", "prisma de base quadrada", ["pirâmide de base quadrada", "cilindro", "cone"],
                   "O cubo tem duas bases quadradas iguais e faces laterais quadradas: é um <b>prisma de base quadrada</b>.")
    if k == 3:
        return mcq("Qual figura é um <b>corpo redondo</b>?", "o cilindro", ["o prisma de base hexagonal", "a pirâmide de base triangular", "o cubo"],
                   "Corpos redondos têm superfície curva: esfera, cone e <b>cilindro</b>.")
    if k == 4:
        n = R.choice([3, 4, 5, 6])
        return mcq("Num prisma de base %s, quantas faces são laterais?" % BASE[n][0], str(n), [str(n + 2), str(n * 2), str(n - 1)],
                   "Cada lado da base forma uma face lateral: <b>%d</b>." % n)
    if k == 5:
        n = R.choice([3, 4, 5, 6])
        return mcq("Numa pirâmide de base %s, quantos triângulos há?" % BASE[n][0], str(n), [str(n + 1), str(n * 2), str(3)] if n != 3 else ["4", "6", "2"],
                   "Cada lado da base forma uma face triangular: <b>%d</b>." % n)
    if k == 6:
        return mcq("Que objeto tem a forma de um prisma de base hexagonal?", "um lápis sextavado", ["uma bola", "uma casquinha de sorvete", "uma lata de refrigerante"],
                   "O lápis sextavado tem duas bases hexagonais e 6 faces laterais: <b>um lápis sextavado</b>.")
    return mcq("Que objeto tem a forma de uma pirâmide de base quadrada?", "o telhado de uma barraca de 4 lados", ["um tijolo", "uma lata", "um dado"],
               "Base quadrada e 4 triângulos que se encontram no alto: <b>o telhado de uma barraca de 4 lados</b>.")


def s4_tabela():
    kind = R.choice(["prisma", "piramide"])
    ns = [3, 4, 5, 6]
    rows = [[BASE[n][0]] + [str(x) for x in fav(kind, n)] for n in ns]
    hide = R.choice(ns[1:])
    col = R.randrange(3)
    v = fav(kind, hide)[col]
    rows[ns.index(hide)][col + 1] = "?"
    tb = table(["Base", "Faces", "Arestas", "Vértices"], rows)
    return mcq(tb + "A tabela mostra %s. Que número falta?" % ("prismas" if kind == "prisma" else "pirâmides"), str(v), [str(x) for x in (v + 1, v - 1, fav(kind, hide - 1)[col], v + 2) if x != v],
               "Veja o padrão: %s. Para a base %s: <b>%d</b>." % ("faces = n + 2, arestas = 3 × n, vértices = 2 × n" if kind == "prisma" else "faces = n + 1, arestas = 2 × n, vértices = n + 1", BASE[hide][0], v))


def s5_problema():
    kind = R.choice(["prisma", "piramide"])
    n = R.randint(7, 10)
    k = R.randrange(3)
    F, A, V = fav(kind, n)
    word = ["faces", "arestas", "vértices"][k]
    v = (F, A, V)[k]
    if R.random() < 0.5:
        return mcq("A base de %s tem %d lados. Quant%s %s tem essa figura?" % ("um prisma" if kind == "prisma" else "uma pirâmide", n, "as" if k < 2 else "os", word), str(v),
                   [str(x) for x in (F, A, V, v + 1, n) if x != v],
                   "%s com base de %d lados: %s. <b>%d %s</b>." % ("Prisma" if kind == "prisma" else "Pirâmide", n,
                                                                   "faces = %d + 2, arestas = 3 × %d, vértices = 2 × %d" % (n, n, n) if kind == "prisma" else "faces = %d + 1, arestas = 2 × %d, vértices = %d + 1" % (n, n, n), v, word))
    m = R.randint(3, 8)
    F, A, V = fav(kind, m)
    return mcq("Para montar o esqueleto de %s com palitos, cada aresta usa 1 palito. Quantos palitos são necessários?" % art(kind, m).replace("o prisma", "um prisma").replace("a pirâmide", "uma pirâmide"),
               str(A), [str(x) for x in (F, V, A + m, A - m) if x != A], "Cada aresta é um palito: %s tem <b>%d arestas</b>." % (art(kind, m), A)) if m <= 6 else None


def main():
    seen = set()
    sets = [
        ("Prismas e pirâmides", mix(R, seen, [(s1_nome, 12), (s1_base, 8)])),
        ("Faces, arestas e vértices", mix(R, seen, [(s2_contar, 14), (s2_qual, 6)])),
        ("Planificações", mix(R, seen, [(s3_planif, 12), (s3_texto, 8)])),
        ("Comparar figuras", mix(R, seen, [(s4_comparar, 8), (s4_tabela, 12)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Um <b>prisma</b> tem duas bases iguais e faces laterais retangulares. Uma <b>pirâmide</b> tem uma base e faces laterais triangulares que se encontram num vértice.",
         "O nome vem da base: prisma de base triangular, pirâmide de base pentagonal…",
         "Se a base tem n lados: o prisma tem n + 2 faces, 3 × n arestas e 2 × n vértices; a pirâmide tem n + 1 faces, 2 × n arestas e n + 1 vértices.",
         "A <b>planificação</b> é a figura aberta sobre o papel: um prisma dá n retângulos e 2 bases; uma pirâmide dá 1 base e n triângulos."],
        [("Quantas arestas tem um prisma de base pentagonal?", ["a base tem 5 lados", "5 arestas embaixo, 5 em cima, 5 laterais", "3 × 5"], "15"),
         ("Que figura forma uma planificação com 1 hexágono e 6 triângulos?", ["1 base", "faces triangulares"], "pirâmide de base hexagonal")],
        [["Contar só as faces laterais", "Some também as bases: prisma de base triangular = 3 + 2 = 5 faces."],
         ["Esquecer as arestas escondidas", "As linhas tracejadas também são arestas."],
         ["Confundir cone e pirâmide", "O cone tem base redonda; a pirâmide tem base de polígono."]],
        solido("prisma", 5, COL[0]) + solido("piramide", 5, COL[2]))
    faq = [("O que o 5º ano estuda sobre figuras espaciais?", "A BNCC pede associar figuras espaciais (prismas, pirâmides, cilindros e cones) às suas planificações e analisar, nomear e comparar seus atributos."),
           ("Existe uma regra para faces, arestas e vértices?", "Sim. Nos prismas e pirâmides, vértices + faces = arestas + 2 (relação de Euler). No 5º ano, basta perceber o padrão na tabela.")]
    make_unit(R, "figuras-espaciais-e-planificacoes", "G", ["EF05MA16"],
              "Associar figuras espaciais a suas planificações (prismas, pirâmides, cilindros e cones) e analisar, nomear e comparar seus atributos",
              "Figuras espaciais e planificações: prismas e pirâmides", "Figuras espaciais",
              "Atividades de matemática para o 5º ano sobre figuras espaciais: prismas e pirâmides, faces, arestas e vértices, planificações, cilindro e cone. 100 exercícios com gabarito.",
              "Prisma: 2 bases e faces retangulares. Pirâmide: 1 base e faces triangulares.", "O nome vem da forma da base.",
              body, faq, sets, 15, grade="5-ano")


if __name__ == "__main__":
    main()
