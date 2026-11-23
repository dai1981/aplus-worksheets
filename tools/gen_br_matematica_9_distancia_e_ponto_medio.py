# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: Distância entre pontos e ponto médio no plano cartesiano (Geometria, EF09MA16)
  python3 tools/gen_br_matematica_9_distancia_e_ponto_medio.py
Ponto médio de um segmento; distância entre dois pontos (Pitágoras); pontos na mesma horizontal ou vertical;
achar a outra extremidade a partir do ponto médio; perímetro e área de polígonos com vértices no plano.
Erros: subtrair no ponto médio (é a média), esquecer de elevar ao quadrado, misturar x com y.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix
from br_9 import M, d, fq, sq, kosy, unit

R = random.Random(89016)
TR = [(3, 4, 5), (4, 3, 5), (6, 8, 10), (8, 6, 10), (5, 12, 13), (12, 5, 13)]


def P(x, y):
    return "(%s, %s)" % (fq(x), fq(y))


def s1_medio():
    x1, y1, x2, y2 = [R.randint(-8, 9) for _ in range(4)]
    if (x1, y1) == (x2, y2) or x1 == x2 and y1 == y2:
        return None
    mx, my = F(x1 + x2, 2), F(y1 + y2, 2)
    return M("Qual é o ponto médio do segmento de A%s a B%s?" % (P(x1, y1), P(x2, y2)), P(mx, my),
             [P(F(x2 - x1, 2), F(y2 - y1, 2)), P(x1 + x2, y1 + y2), P(my, mx) if mx != my else P(mx + 1, my), P(F(x1 + y1, 2), F(x2 + y2, 2))],
             "M = ((%s + %s) ÷ 2, (%s + %s) ÷ 2) = <b>%s</b>." % (d(x1), d(x2) if x2 >= 0 else "(%s)" % d(x2), d(y1), d(y2) if y2 >= 0 else "(%s)" % d(y2), P(mx, my)))


def s2_extremo():
    x1, y1, mx, my = [R.randint(-6, 6) for _ in range(4)]
    if (x1, y1) == (mx, my):
        return None
    x2, y2 = 2 * mx - x1, 2 * my - y1
    return M("M%s é o ponto médio do segmento AB, com A%s. Quais são as coordenadas de B?" % (P(mx, my), P(x1, y1)), P(x2, y2),
             [P(F(mx + x1, 2), F(my + y1, 2)), P(mx - x1, my - y1), P(x1 - 2 * mx, y1 - 2 * my), P(x2 + 1, y2)],
             "B = (2 · %s − %s, 2 · %s − %s) = <b>%s</b>." % (d(mx), d(x1) if x1 >= 0 else "(%s)" % d(x1), d(my), d(y1) if y1 >= 0 else "(%s)" % d(y1), P(x2, y2)))


def s3_dist():
    a, b, c = R.choice(TR)
    x1, y1 = R.randint(-4, 1), R.randint(-4, 1)
    sx, sy = R.choice([1, -1]), R.choice([1, -1])
    if c > 5:
        x1, y1 = R.randint(-6, 6), R.randint(-6, 6)
    x2, y2 = x1 + sx * a, y1 + sy * b
    pic = kosy(pts=[(x1, y1, "A"), (x2, y2, "B")], lo=-5, hi=5) if max(abs(v) for v in (x1, y1, x2, y2)) <= 5 else ""
    return M(pic + "Qual é a distância entre A%s e B%s?" % (P(x1, y1), P(x2, y2)), d(c), [d(a + b), d(c * c), d(abs(a - b)) if a != b else d(c + 1), d(c + 2)],
             "Δx = %d, Δy = %d; d² = %d² + %d² = %d → <b>d = %d</b>." % (a, b, a, b, c * c, c))


def s4_dist_irr():
    k = R.choice(["hv", "irr"])
    if k == "hv":
        x, y1, y2 = R.randint(-6, 6), R.randint(-7, 0), R.randint(1, 8)
        if R.random() < 0.5:
            return M("Qual é a distância entre A%s e B%s?" % (P(x, y1), P(x, y2)), d(y2 - y1), [d(y2 + y1) if y2 + y1 != y2 - y1 else d(y2), d(abs(x)) if abs(x) != y2 - y1 else d(y2 - y1 + 1), d((y2 - y1) ** 2)],
                     "Mesma abscissa: d = %s − %s = <b>%s</b>." % (d(y2), "(%s)" % d(y1) if y1 < 0 else d(y1), d(y2 - y1)))
        return M("Qual é a distância entre A%s e B%s?" % (P(y1, x), P(y2, x)), d(y2 - y1), [d(y2 + y1) if y2 + y1 != y2 - y1 else d(y2), d(abs(x)) if abs(x) != y2 - y1 else d(y2 - y1 + 1), d((y2 - y1) ** 2)],
                 "Mesma ordenada: d = %s − %s = <b>%s</b>." % (d(y2), "(%s)" % d(y1) if y1 < 0 else d(y1), d(y2 - y1)))
    dx, dy = R.choice([(1, 1), (1, 2), (2, 2), (1, 3), (2, 3), (3, 3), (2, 4), (1, 4), (3, 5), (4, 4), (2, 6)])
    x1, y1 = R.randint(-5, 3), R.randint(-5, 3)
    x2, y2 = x1 + dx, y1 + dy
    n = dx * dx + dy * dy
    return M("Qual é a distância entre A%s e B%s? (Deixe a raiz simplificada.)" % (P(x1, y1), P(x2, y2)), sq(n), [d(dx + dy), d(n), sq(abs(dy * dy - dx * dx)) if dx != dy else d(2 * dx), "√%d" % (dx + dy)],
             "d² = %d² + %d² = %d → <b>d = %s</b>." % (dx, dy, n, sq(n)))


def s5_poligono():
    k = R.choice(["ret", "tri", "per_tri"])
    if k == "ret":
        x1, y1 = R.randint(-4, 0), R.randint(-4, 0)
        w, h = R.randint(2, 5), R.randint(2, 4)
        pts = [(x1, y1, "A"), (x1 + w, y1, "B"), (x1 + w, y1 + h, "C"), (x1, y1 + h, "D")]
        q = R.choice(["área", "perímetro"])
        ans = w * h if q == "área" else 2 * (w + h)
        return M(kosy(pts=pts) + "ABCD é um retângulo com A%s e C%s. Qual é a %s?" % (P(x1, y1), P(x1 + w, y1 + h), q), d(ans) + (" unidades de área" if q == "área" else " unidades"),
                 [d(2 * (w + h) if q == "área" else w * h) + (" unidades de área" if q == "área" else " unidades"), d(w + h) + (" unidades de área" if q == "área" else " unidades"), d(ans + 2) + (" unidades de área" if q == "área" else " unidades")],
                 "Lados %d e %d: %s = <b>%s</b>." % (w, h, "%d · %d" % (w, h) if q == "área" else "2 · (%d + %d)" % (w, h), d(ans)))
    if k == "tri":
        x1, y1 = R.randint(-5, 0), R.randint(-4, 0)
        b, h = R.randint(3, 6), R.randint(2, 5)
        t = R.randint(0, b)
        if x1 + b > 5:
            return None
        pts = [(x1, y1, "A"), (x1 + b, y1, "B"), (x1 + t, y1 + h, "C")]
        A = F(b * h, 2)
        return M(kosy(pts=pts) + "Qual é a área do triângulo de vértices A%s, B%s e C%s?" % (P(x1, y1), P(x1 + b, y1), P(x1 + t, y1 + h)), d(A), [d(b * h), d(b + h), d(A + h)],
                 "Base AB = %d, altura = %d: %d · %d ÷ 2 = <b>%s</b>." % (b, h, b, h, d(A)))
    a, b, c = R.choice([(3, 4, 5), (4, 3, 5), (6, 8, 10)])
    x1, y1 = R.randint(-5, -1), R.randint(-5, -2)
    if x1 + a > 5 or y1 + b > 5:
        return None
    pts = [(x1, y1, "A"), (x1 + a, y1, "B"), (x1 + a, y1 + b, "C")]
    return M(kosy(pts=pts) + "Qual é o perímetro do triângulo de vértices A%s, B%s e C%s?" % (P(x1, y1), P(x1 + a, y1), P(x1 + a, y1 + b)), d(a + b + c), [d(a + b), d(a + b + a + b), d(a * b), d(a + b + c + 1)],
             "AB = %d, BC = %d e AC = √(%d² + %d²) = %d: %d + %d + %d = <b>%d</b>." % (a, b, a, b, c, a, b, c, a + b + c))


def main():
    seen = set()
    sets = [
        ("Ponto médio", mix(R, seen, [(s1_medio, 20)])),
        ("A outra extremidade", mix(R, seen, [(s2_extremo, 14), (s1_medio, 6)])),
        ("Distância entre dois pontos", mix(R, seen, [(s3_dist, 20)])),
        ("Distâncias com raízes e na mesma reta", mix(R, seen, [(s4_dist_irr, 20)])),
        ("Polígonos no plano cartesiano", mix(R, seen, [(s5_poligono, 20)])),
    ]
    body = lesson(
        ["O <b>ponto médio</b> de AB é a média das coordenadas: M = ((x₁ + x₂) ÷ 2, (y₁ + y₂) ÷ 2).",
         "A <b>distância</b> entre dois pontos vem do teorema de Pitágoras: d² = (x₂ − x₁)² + (y₂ − y₁)².",
         "Se os pontos estão na mesma horizontal ou vertical, basta subtrair as coordenadas que mudam."],
        [("A(1, 2) e B(7, 10)", ["M = (8 ÷ 2, 12 ÷ 2)", "d² = 6² + 8² = 100"], "M(4, 6) e d = 10"),
         ("M(2, 3), A(−1, 5)", ["B = (2 · 2 + 1, 2 · 3 − 5)"], "B(5, 1)")],
        [["Subtrair no ponto médio", "O ponto médio é a soma dividida por 2."],
         ["Esquecer de elevar ao quadrado", "d² = Δx² + Δy²; depois tire a raiz."],
         ["Misturar x com y", "Some x com x e y com y."]],
        kosy(pts=[(1, 1, "A"), (4, 5, "B")]))
    faq = [("Como calcular a distância entre dois pontos no plano cartesiano?", "Calcule a diferença dos x e a diferença dos y, eleve as duas ao quadrado, some e tire a raiz quadrada: é o teorema de Pitágoras."),
           ("O que a BNCC pede no 9º ano?", "Determinar o ponto médio de um segmento de reta e a distância entre dois pontos quaisquer, dadas as coordenadas desses pontos no plano cartesiano, sem o uso de fórmulas, e utilizar esse conhecimento para calcular, por exemplo, medidas de perímetros e áreas de figuras planas construídas no plano (EF09MA16).")]
    unit(R, "distancia-e-ponto-medio", "G", ["EF09MA16"],
         "Determinar o ponto médio de um segmento de reta e a distância entre dois pontos quaisquer, dadas as coordenadas desses pontos no plano cartesiano, sem o uso de fórmulas, e utilizar esse conhecimento para calcular, por exemplo, medidas de perímetros e áreas de figuras planas construídas no plano",
         "Distância entre pontos e ponto médio no plano cartesiano", "Distância e ponto médio",
         "Atividades de matemática para o 9º ano sobre o plano cartesiano: ponto médio, distância entre dois pontos com o teorema de Pitágoras, extremidade do segmento, perímetro e área de polígonos. 100 exercícios com gabarito.",
         "Ponto médio: média das coordenadas.", "Distância: Pitágoras com Δx e Δy.",
         body, faq, sets, 16)


if __name__ == "__main__":
    main()
