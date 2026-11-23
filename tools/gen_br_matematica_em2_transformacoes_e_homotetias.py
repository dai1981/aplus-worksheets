# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 2ª série: Transformações isométricas e homotetias (EM13MAT105)
  python3 tools/gen_br_matematica_em2_transformacoes_e_homotetias.py
Reflexão, translação e rotação no plano cartesiano (coordenadas), composição de transformações;
homotetia de centro O e razão k: coordenadas da imagem, perímetro × |k|, área × k², razão negativa; isometrias na arte e na natureza.
Usa geradores do 7º ano (reflexão, translação) e do 8º ano (rotação, composição) com outro sorteio.
Erros: multiplicar a área por k, esquecer que k negativo inverte a figura, trocar o sinal da coordenada errada na reflexão.
"""
import random
from fractions import Fraction as F
from br_em import M, d, fq, bank, mix, lesson, use, unit, kosy

R = random.Random(92005)
t_refl, t_trans = use("gen_br_matematica_7_transformacoes_no_plano_cartesiano", 92902, "s2_reflexao", "s3_translacao")
t_rot, t_comp = use("gen_br_matematica_8_transformacoes_geometricas", 92903, "s1_rotacao", "s2_composicao")


def P(x, y):
    return "(%s, %s)" % (d(x), d(y))


def s1_homot():
    k = R.choice([2, 3, F(1, 2), -1, -2, F(3, 2)])
    x, y = R.randint(-4, 5), R.randint(-4, 5)
    if (x == 0 and y == 0) or (x * k).denominator != 1 or (y * k).denominator != 1:
        return None
    q = R.choice(["origem", "centro"])
    if q == "origem":
        return M("Uma homotetia de centro na origem e razão %s leva o ponto A%s em qual ponto?" % (fq(k), P(x, y)), P(k * x, k * y), [P(x + k, y + k), P(-k * x, -k * y), P(k * x, y) if k * y != y else P(x, k * y + 1)],
                 "Multiplique as coordenadas por %s: <b>%s</b>." % (fq(k), P(k * x, k * y)))
    cx, cy = R.randint(-2, 2), R.randint(-2, 2)
    if (cx, cy) == (0, 0) or k < 0:
        return None
    nx, ny = cx + k * (x - cx), cy + k * (y - cy)
    return M("Uma homotetia de centro O%s e razão %s leva o ponto A%s em qual ponto?" % (P(cx, cy), fq(k), P(x, y)), P(nx, ny), [P(k * x, k * y), P(x + k, y + k), P(cx + k * x, cy + k * y)],
             "A′ = O + %s · (A − O) = %s + %s · %s = <b>%s</b>." % (fq(k), P(cx, cy), fq(k), P(x - cx, y - cy), P(nx, ny)))


def s2_medidas():
    k = R.choice([2, 3, 4, F(1, 2), F(1, 3), -2])
    q = R.choice(["per", "area", "area", "vol"])
    if q == "per":
        p = R.choice([12, 18, 24, 30, 36])
        return M("Uma figura de perímetro %d cm sofre uma homotetia de razão %s. Qual é o novo perímetro?" % (p, fq(k)), "%s cm" % d(abs(k) * p), ["%s cm" % d(k * k * p), "%s cm" % d(p + abs(k)), "%s cm" % d(p)],
                 "O perímetro fica multiplicado por |k| = %s: <b>%s cm</b>." % (fq(abs(k)), d(abs(k) * p)))
    if q == "area":
        A = R.choice([9, 12, 18, 36, 48, 72])
        if (A * k * k).denominator != 1:
            return None
        return M("Uma figura de área %d cm² sofre uma homotetia de razão %s. Qual é a nova área?" % (A, fq(k)), "%s cm²" % d(k * k * A), ["%s cm²" % d(abs(k) * A), "%s cm²" % d(A), "%s cm²" % d(k * k * k * A) if k * k * k * A > 0 else "%s cm²" % d(2 * k * k * A)],
                 "A área fica multiplicada por k² = %s: <b>%s cm²</b>." % (fq(k * k), d(k * k * A)))
    if k < 0 or k < 1:
        return None
    V = R.choice([5, 8, 10, 12])
    return M("Um cubo de volume %d cm³ é ampliado com todas as arestas multiplicadas por %s. Qual é o novo volume?" % (V, d(k)), "%s cm³" % d(k ** 3 * V), ["%s cm³" % d(k * V), "%s cm³" % d(k * k * V), "%s cm³" % d(V + k ** 3)],
             "O volume fica multiplicado por k³ = %s: <b>%s cm³</b>." % (d(k ** 3), d(k ** 3 * V)))


s3_tipo = bank(R, [
    ("Uma transformação que conserva as distâncias (a figura não muda de forma nem de tamanho) é uma…", "isometria", ["homotetia de razão 2", "ampliação", "redução"]),
    ("Reflexão, translação e rotação são…", "isometrias", ["homotetias", "ampliações", "projeções"]),
    ("Uma homotetia de razão 3…", "amplia a figura, mantendo a forma", ["mantém o tamanho", "reduz a figura", "muda a forma"]),
    ("Uma homotetia de razão 1/2…", "reduz a figura à metade das medidas", ["dobra a figura", "não muda a figura", "inverte a figura sem reduzir"]),
    ("Uma homotetia de razão −1 equivale a…", "uma rotação de 180° em torno do centro", ["uma translação", "uma reflexão num eixo", "uma ampliação"]),
    ("Na homotetia, uma figura e sua imagem são…", "semelhantes", ["sempre congruentes", "sem relação", "sempre do mesmo tamanho"]),
    ("O desenho de uma borboleta, igual dos dois lados, tem simetria de…", "reflexão", ["translação", "homotetia", "rotação de 90°"]),
    ("Um ladrilho repetido numa calçada, sempre na mesma direção, mostra…", "translações", ["homotetias", "reflexões em um ponto", "ampliações"]),
    ("As pás de um ventilador, iguais a cada giro de 120°, mostram simetria de…", "rotação", ["translação", "reflexão", "homotetia"]),
    ("Uma fotografia ampliada de 10 × 15 cm para 20 × 30 cm é uma homotetia de razão…", "2", ["4", "10", "1/2"]),
    ("Na homotetia de razão k, os ângulos da figura…", "não mudam", ["ficam multiplicados por k", "ficam multiplicados por k²", "mudam de sinal"]),
], "s3_tipo")


def s4_figura():
    k = R.choice([2, -1, F(1, 2)])
    pts = [(1, 1), (2, 1), (1, 2)] if k != F(1, 2) else [(2, 2), (4, 2), (2, 4)]
    if k == 2:
        pts = [(1, 0), (2, 1), (0, 2)]
    img = [(k * x, k * y) for x, y in pts]
    g = kosy(pts=[(pts[0][0], pts[0][1], ""), (img[0][0], img[0][1], "")], lo=-5, hi=5, label="triângulo ABC (azul) e sua imagem A′B′C′ (vermelha)")
    u, x0, y0 = 24, 20 + 5 * 24, 20 + 5 * 24
    tris = "".join("<polygon points='%s' fill='%s' fill-opacity='0.18' stroke='%s' stroke-width='2.2'/>" % (" ".join("%.1f,%.1f" % (x0 + float(x) * u, y0 - float(y) * u) for x, y in t), c, c, ) for t, c in ((pts, "#1f5fbf"), (img, "#c0392b")))
    i = g.index("<circle")
    g = g[:i] + tris + g[i:]
    return M(g + "O triângulo vermelho é a imagem do triângulo azul por uma homotetia de centro na origem (os pontos marcados se correspondem). Qual é a razão?", fq(k), [fq(-k), fq(1 / F(k)) if abs(k) != 1 else "2", fq(k * k) if k * k != k else "3"],
             "O ponto %s vai para %s: as coordenadas foram multiplicadas por <b>%s</b>." % (P(*pts[0]), P(*img[0]), fq(k)))


def main():
    seen = set()
    sets = [
        ("Reflexão e translação", mix(R, seen, [(t_refl, 10), (t_trans, 10)])),
        ("Rotação e composição", mix(R, seen, [(t_rot, 12), (t_comp, 8)])),
        ("Homotetia: coordenadas", mix(R, seen, [(s1_homot, 17), (s4_figura, 3)])),
        ("Homotetia: perímetro, área e volume", mix(R, seen, [(s2_medidas, 20)])),
        ("Isometrias e homotetias no dia a dia", mix(R, seen, [(s3_tipo, 11), (s1_homot, 5), (s2_medidas, 4)])),
    ]
    body = lesson(
        ["<b>Isometrias</b> conservam distâncias: reflexão (espelho), translação (deslizar), rotação (girar). A figura não muda de forma nem de tamanho.",
         "<b>Homotetia</b> de centro O e razão k: cada ponto A vai para A′ com OA′ = k · OA. Com centro na origem, (x, y) → (kx, ky).",
         "Na homotetia, as figuras são semelhantes: comprimentos × |k|, áreas × k², volumes × |k|³. Se k &lt; 0, a imagem fica do outro lado do centro.",
         "Isometrias e homotetias aparecem em mosaicos, logotipos, fotos ampliadas e na natureza."],
        [("Homotetia de centro (0, 0) e razão 3 do ponto (2, −1)", ["(3 · 2, 3 · (−1))"], "(6, −3)"),
         ("Área 10 cm², razão 3", ["10 · 3²"], "90 cm²")],
        [["Multiplicar a área por k", "Área: multiplique por k²."],
         ["Ignorar o sinal de k", "k negativo leva a figura para o lado oposto do centro."],
         ["Trocar a coordenada na reflexão", "Reflexão no eixo x muda o sinal de y; no eixo y, o de x."]])
    faq = [("O que é uma homotetia?", "É uma transformação que amplia ou reduz uma figura a partir de um centro, multiplicando as distâncias ao centro por uma razão k. A imagem é semelhante à figura original."),
           ("O que a BNCC pede?", "Utilizar as noções de transformações isométricas (translação, reflexão, rotação e composições destas) e transformações homotéticas para construir figuras e analisar elementos da natureza e diferentes produções humanas (fractais, construções civis, obras de arte, entre outras) (EM13MAT105).")]
    unit(R, "transformacoes-isometricas-e-homotetias", "G", ["EM13MAT105"],
         "Utilizar as noções de transformações isométricas (translação, reflexão, rotação e composições destas) e transformações homotéticas para construir figuras e analisar elementos da natureza e diferentes produções humanas (fractais, construções civis, obras de arte, entre outras)",
         "Transformações isométricas e homotetias", "Isometrias e homotetias",
         "Atividades de matemática para a 2ª série do Ensino Médio sobre transformações: reflexão, translação, rotação, composição, homotetia, efeito no perímetro, na área e no volume. 100 exercícios com gabarito.",
         "Homotetia de razão k: áreas × k²", "Isometrias não mudam o tamanho.",
         body, faq, sets, 5, grade="2-serie")


if __name__ == "__main__":
    main()
