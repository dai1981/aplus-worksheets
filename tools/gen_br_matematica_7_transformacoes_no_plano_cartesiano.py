# -*- coding: utf-8 -*-
"""
Brasil Matemática 7º ano: Transformações no plano cartesiano e simetrias (Geometria, EF07MA19, EF07MA20, EF07MA21)
  python3 tools/gen_br_matematica_7_transformacoes_no_plano_cartesiano.py
Multiplicar as coordenadas dos vértices por um número (ampliação/redução a partir da origem); multiplicar por −1 (simetria em
relação à origem); simetria em relação aos eixos (reflexão); translação; figuras com simetria; ladrilhamentos.
Erros: trocar x e y na reflexão, mudar o sinal das duas coordenadas na reflexão em um eixo, somar em vez de multiplicar.
"""
import random
from br_common import lesson, mix
from br_9 import M, bank, kosy, unit

R = random.Random(87011)


def P(x, y):
    return "(%s, %s)" % (str(x).replace("-", "−"), str(y).replace("-", "−"))


def s1_mult():
    x, y = R.randint(-4, 4), R.randint(-4, 4)
    if x == 0 or y == 0:
        return None
    k = R.choice([2, 3, -1, -2])
    ok = P(k * x, k * y)
    return M("Multiplicando as coordenadas do ponto A%s por %s, que ponto obtemos?" % (P(x, y), str(k).replace("-", "−")), ok, [P(x + k, y + k), P(k * x, y), P(-k * x, -k * y)],
             "Multiplique x e y por %s: <b>%s</b>." % (str(k).replace("-", "−"), ok))


def s2_reflexao():
    x, y = R.randint(-5, 5), R.randint(-5, 5)
    if x == 0 or y == 0 or abs(x) == abs(y):
        return None
    k = R.choice(["x", "y", "o"])
    ok = {"x": P(x, -y), "y": P(-x, y), "o": P(-x, -y)}[k]
    nm = {"x": "ao eixo x", "y": "ao eixo y", "o": "à origem"}[k]
    alts = [P(x, -y), P(-x, y), P(-x, -y), P(y, x)]
    pic = kosy(pts=[(x, y, "A")])
    return M(pic + "Qual é o simétrico do ponto A%s em relação %s?" % (P(x, y), nm), ok, [a for a in alts if a != ok],
             {"x": "Na reflexão no eixo x, só o y muda de sinal", "y": "Na reflexão no eixo y, só o x muda de sinal", "o": "Na simetria em relação à origem, os dois mudam de sinal (multiplicar por −1)"}[k] + ": <b>%s</b>." % ok)


def s3_translacao():
    x, y = R.randint(-4, 4), R.randint(-4, 4)
    dx, dy = R.choice([-4, -3, -2, 2, 3, 4]), R.choice([-3, -2, -1, 1, 2, 3])
    ok = P(x + dx, y + dy)
    t = "%d unidades para a %s e %d para %s" % (abs(dx), "direita" if dx > 0 else "esquerda", abs(dy), "cima" if dy > 0 else "baixo")
    return M("O triângulo com vértice A%s foi transladado %s. Onde fica a imagem de A?" % (P(x, y), t), ok, [P(x + dy, y + dx) if dx != dy else P(x - dx, y + dy), P(x - dx, y - dy), P(x * dx, y * dy) if P(x * dx, y * dy) != ok else P(x + dx + 1, y + dy)],
             "Some %s ao x e %s ao y: <b>%s</b>." % (str(dx).replace("-", "−"), str(dy).replace("-", "−"), ok))


def s4_figura():
    w, h = R.randint(1, 3), R.randint(1, 3)
    x, y = R.randint(0, 2), R.randint(0, 2)
    k = R.choice([2, 3])
    V = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    if max(max(a, b) for a, b in V) * k > 5:
        return None
    q = R.choice(["per", "area", "vert"])
    pts = [(a * k, b * k, n) for (a, b), n in zip(V, "ABCD")]
    pic = kosy(pts=[(a, b, n.lower()) for (a, b), n in zip(V, "ABCD")] + pts, lo=-1, hi=6)
    if q == "vert":
        a, b = V[2]
        return M(pic + "O retângulo abcd teve as coordenadas multiplicadas por %d, formando ABCD. Se c = %s, quais são as coordenadas de C?" % (k, P(a, b)), P(a * k, b * k), [P(a + k, b + k), P(a * k, b), P(a * k * k, b * k * k)],
                 "Multiplique as duas coordenadas por %d: <b>%s</b>." % (k, P(a * k, b * k)))
    if q == "per":
        return M(pic + "O retângulo abcd (lados %d e %d) teve as coordenadas multiplicadas por %d. O perímetro da nova figura é quantas vezes o original?" % (w, h, k), "%d vezes" % k, ["%d vezes" % (k * k), "%d vezes" % (k + 1), "igual"],
                 "Cada lado fica %d vezes maior, então o perímetro também: <b>%d vezes</b>." % (k, k))
    return M(pic + "O retângulo abcd teve as coordenadas multiplicadas por %d. A área da nova figura é quantas vezes a original?" % k, "%d vezes" % (k * k), ["%d vezes" % k, "%d vezes" % (2 * k), "igual"],
             "Comprimento e largura ficam %d vezes maiores: área × %d × %d = <b>%d vezes</b>." % (k, k, k, k * k))


s5_simetria = bank(R, [
    ("Quantos eixos de simetria tem um quadrado?", "4", ["2", "1", "8"]),
    ("Quantos eixos de simetria tem um retângulo que não é quadrado?", "2", ["4", "1", "0"]),
    ("Quantos eixos de simetria tem um triângulo equilátero?", "3", ["1", "2", "6"]),
    ("Quantos eixos de simetria tem um triângulo isósceles que não é equilátero?", "1", ["2", "3", "0"]),
    ("Quantos eixos de simetria tem um círculo?", "infinitos", ["1", "2", "4"]),
    ("Quantos eixos de simetria tem um hexágono regular?", "6", ["3", "2", "12"]),
    ("Na reflexão, a figura e a imagem são…", "congruentes (mesma forma e tamanho)", ["de tamanhos diferentes", "sempre iguais em posição", "semelhantes com razão 2"]),
    ("Na translação, a figura…", "desliza sem girar nem mudar de tamanho", ["gira em torno de um ponto", "é espelhada", "dobra de tamanho"]),
    ("Multiplicar as coordenadas por 2 faz a figura…", "ficar ampliada, com lados 2 vezes maiores", ["deslizar 2 unidades", "girar 2 vezes", "ficar igual"]),
    ("Multiplicar as coordenadas por −1 produz…", "a figura simétrica em relação à origem", ["a mesma figura", "a reflexão no eixo x", "uma ampliação"]),
    ("Um ladrilhamento com quadrados funciona porque…", "4 ângulos de 90° completam 360°", ["os quadrados são grandes", "3 ângulos de 90° completam 360°", "os quadrados têm 4 lados"]),
    ("Com pentágonos regulares sozinhos, é possível ladrilhar um piso sem buracos?", "não, 108° não divide 360°", ["sim, sempre", "sim, com 3 pentágonos", "só com pentágonos grandes"]),
], "s5_simetria")


def main():
    seen = set()
    sets = [
        ("Multiplicar as coordenadas", mix(R, seen, [(s1_mult, 20)])),
        ("Reflexões", mix(R, seen, [(s2_reflexao, 20)])),
        ("Translações", mix(R, seen, [(s3_translacao, 20)])),
        ("Ampliação no plano", mix(R, seen, [(s4_figura, 20)])),
        ("Simetria e ladrilhamentos", mix(R, seen, [(s5_simetria, 12), (s2_reflexao, 8)])),
    ]
    body = lesson(
        ["Multiplicar as coordenadas dos vértices por k (k &gt; 1) amplia a figura a partir da origem; por um número entre 0 e 1, reduz.",
         "Multiplicar por −1 dá a figura simétrica em relação à origem: (x, y) → (−x, −y).",
         "Reflexão no eixo x: (x, y) → (x, −y). No eixo y: (x, y) → (−x, y). Translação: some o mesmo valor a todos os x e/ou a todos os y.",
         "Reflexão, translação e rotação não mudam a forma nem o tamanho."],
        [("A(2, −3) refletido no eixo y", ["muda o sinal do x"], "(−2, −3)"),
         ("A(1, 2) com coordenadas × 3", ["(3, 6)"], "lados 3 vezes maiores")],
        [["Trocar x e y", "(2, 5) e (5, 2) são pontos diferentes."],
         ["Mudar os dois sinais na reflexão num eixo", "No eixo x só o y muda."],
         ["Somar em vez de multiplicar", "Ampliar é multiplicar as coordenadas."]],
        kosy(pts=[(2, 3, "A"), (-2, 3, "A'")]))
    faq = [("Como achar o simétrico de um ponto em relação aos eixos?", "Em relação ao eixo x, troque o sinal do y; em relação ao eixo y, troque o sinal do x; em relação à origem, troque os dois."),
           ("O que a BNCC pede no 7º ano?", "Realizar transformações de polígonos representados no plano cartesiano, decorrentes da multiplicação das coordenadas de seus vértices por um número inteiro (EF07MA19), reconhecer e representar as transformações de figuras planas por simetrias de translação, rotação e reflexão (EF07MA20) e reconhecer e construir figuras obtidas por simetrias (EF07MA21).")]
    unit(R, "transformacoes-no-plano-cartesiano", "G", ["EF07MA19", "EF07MA20", "EF07MA21"],
         "Realizar transformações de polígonos representados no plano cartesiano, decorrentes da multiplicação das coordenadas de seus vértices por um número inteiro; reconhecer e representar, no plano cartesiano, o simétrico de figuras em relação aos eixos e à origem; reconhecer e construir figuras obtidas por simetrias de translação, rotação e reflexão",
         "Transformações no plano cartesiano e simetrias", "Transformações e simetrias",
         "Atividades de matemática para o 7º ano sobre transformações no plano cartesiano: multiplicar coordenadas, reflexões nos eixos, simetria em relação à origem, translações, ampliação e simetria de figuras. 100 exercícios com gabarito.",
         "Eixo x: muda o y. Eixo y: muda o x.", "Coordenadas × k: figura ampliada.",
         body, faq, sets, 11, grade="7-ano")


if __name__ == "__main__":
    main()
