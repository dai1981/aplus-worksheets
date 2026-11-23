# -*- coding: utf-8 -*-
"""
Brasil Matemática 8º ano: Transformações geométricas e composições (Geometria, EF08MA18)
  python3 tools/gen_br_matematica_8_transformacoes_geometricas.py
Translação, reflexão e rotação no plano cartesiano; rotação de 90° e 180° em torno da origem; composição de transformações
(duas reflexões = rotação; duas translações = uma translação); o que muda e o que se conserva (forma, tamanho, orientação).
Usa geradores do 7º ano (reflexões e translações) com outro sorteio.
Erros: girar no sentido errado, aplicar a segunda transformação ao ponto original, achar que a reflexão mantém a orientação.
"""
import random
from br_common import lesson, mix, use
from br_9 import M, bank, kosy, unit

R = random.Random(88014)
t_refl, t_trans = use("gen_br_matematica_7_transformacoes_no_plano_cartesiano", 88914, "s2_reflexao", "s3_translacao")


def P(x, y):
    return "(%s, %s)" % (str(x).replace("-", "−"), str(y).replace("-", "−"))


def s1_rotacao():
    x, y = R.randint(-5, 5), R.randint(-5, 5)
    if x == 0 or y == 0 or abs(x) == abs(y):
        return None
    k = R.choice(["90a", "90h", "180"])
    r = {"90a": (-y, x), "90h": (y, -x), "180": (-x, -y)}[k]
    nm = {"90a": "90° no sentido anti-horário", "90h": "90° no sentido horário", "180": "180°"}[k]
    alts = [(-y, x), (y, -x), (-x, -y), (y, x), (x, -y)]
    return M(kosy(pts=[(x, y, "A")]) + "Girando o ponto A%s %s em torno da origem, onde ele chega?" % (P(x, y), nm), P(*r), [P(*a) for a in alts if a != r][:3],
             {"90a": "Rotação de 90° anti-horária: (x, y) → (−y, x)", "90h": "Rotação de 90° horária: (x, y) → (y, −x)", "180": "Rotação de 180°: (x, y) → (−x, −y)"}[k] + ": <b>%s</b>." % P(*r))


def s2_composicao():
    x, y = R.randint(-5, 5), R.randint(-5, 5)
    if x == 0 or y == 0 or abs(x) == abs(y):
        return None
    k = R.choice(["xy", "tt", "rt"])
    if k == "xy":
        r = (-x, -y)
        return M("O ponto A%s é refletido no eixo x e, depois, a imagem é refletida no eixo y. Onde ele termina?" % P(x, y), P(*r), [P(x, -y), P(-x, y), P(y, x)], "(x, y) → (x, −y) → (−x, −y): <b>%s</b>, o mesmo que girar 180°." % P(*r))
    if k == "tt":
        a, b, c, e = [R.choice([-3, -2, -1, 1, 2, 3]) for _ in range(4)]
        r = (x + a + c, y + b + e)
        return M("O ponto A%s é transladado %s e, depois, %s. Onde ele termina?" % (P(x, y), "(%s, %s)" % (str(a).replace("-", "−"), str(b).replace("-", "−")), "(%s, %s)" % (str(c).replace("-", "−"), str(e).replace("-", "−"))), P(*r),
                 [P(x + c, y + e), P(x + a * c, y + b * e) if (x + a * c, y + b * e) != r else P(r[0] + 1, r[1]), P(x - a - c, y - b - e)],
                 "Duas translações equivalem a uma só: some (%s, %s) a A: <b>%s</b>." % (str(a + c).replace("-", "−"), str(b + e).replace("-", "−"), P(*r)))
    a = R.choice([-3, -2, 2, 3])
    r = (-(x + a), y)
    return M("O ponto A%s é transladado %d unidades para a %s e, depois, refletido no eixo y. Onde ele termina?" % (P(x, y), abs(a), "direita" if a > 0 else "esquerda"), P(*r), [P(-x + a, y), P(x + a, -y), P(-x, y)],
             "Translação: %s; reflexão no eixo y: <b>%s</b>." % (P(x + a, y), P(*r)))


s3_conceitos = bank(R, [
    ("Translação, reflexão e rotação conservam…", "a forma e o tamanho da figura", ["só a forma", "só a posição", "nada"]),
    ("Qual transformação muda a orientação (a figura fica «espelhada»)?", "a reflexão", ["a translação", "a rotação", "nenhuma"]),
    ("Duas reflexões seguidas, em retas perpendiculares, equivalem a…", "uma rotação de 180°", ["uma translação", "uma reflexão", "nenhuma mudança"]),
    ("Duas reflexões seguidas, em retas paralelas, equivalem a…", "uma translação", ["uma rotação de 90°", "uma reflexão", "uma ampliação"]),
    ("Duas rotações de 90° no mesmo sentido, em torno do mesmo ponto, equivalem a…", "uma rotação de 180°", ["uma translação", "uma reflexão", "nenhuma mudança"]),
    ("Na rotação de 180° em torno da origem, (x, y) vira…", "(−x, −y)", ["(y, x)", "(−y, x)", "(x, −y)"]),
    ("Na reflexão em relação à reta y = x, (3, 1) vira…", "(1, 3)", ["(−3, 1)", "(3, −1)", "(−1, −3)"]),
    ("Uma translação de (2, −1) seguida de uma de (−2, 1) leva o ponto…", "de volta à posição inicial", ["ao dobro da distância", "à origem sempre", "para longe"]),
    ("Na rotação, o ponto que não se move é…", "o centro de rotação", ["o ponto mais distante", "todos os pontos", "nenhum"]),
], "s3_conceitos")


def main():
    seen = set()
    sets = [
        ("Translações", mix(R, seen, [(t_trans, 20)])),
        ("Reflexões", mix(R, seen, [(t_refl, 20)])),
        ("Rotações", mix(R, seen, [(s1_rotacao, 20)])),
        ("Composição de transformações", mix(R, seen, [(s2_composicao, 20)])),
        ("O que se conserva?", mix(R, seen, [(s3_conceitos, 9), (s1_rotacao, 6), (s2_composicao, 5)])),
    ]
    body = lesson(
        ["<b>Translação</b>: desliza a figura (soma valores às coordenadas). <b>Reflexão</b>: espelha em relação a uma reta. <b>Rotação</b>: gira em torno de um ponto.",
         "Em torno da origem: 90° anti-horário (x, y) → (−y, x); 90° horário (x, y) → (y, −x); 180° (x, y) → (−x, −y).",
         "<b>Composição</b>: aplique uma transformação depois da outra, sempre sobre a imagem. Duas reflexões em eixos perpendiculares dão uma rotação de 180°.",
         "As três transformações conservam a forma e o tamanho; só a reflexão inverte a orientação."],
        [("A(2, 3) girado 90° anti-horário", ["(−3, 2)"], "(−3, 2)"),
         ("A(2, 3): reflexão no eixo x e depois no eixo y", ["(2, −3)", "(−2, −3)"], "(−2, −3)")],
        [["Girar no sentido errado", "Anti-horário é o contrário dos ponteiros do relógio."],
         ["Aplicar a 2ª transformação ao ponto original", "Use a imagem da 1ª."],
         ["Achar que a reflexão mantém a orientação", "A imagem fica espelhada."]],
        kosy(pts=[(2, 3, "A"), (-3, 2, "A'")]))
    faq = [("Como girar um ponto 90° em torno da origem?", "No sentido anti-horário, (x, y) vira (−y, x). No sentido horário, (x, y) vira (y, −x)."),
           ("O que a BNCC pede no 8º ano?", "Reconhecer e construir figuras obtidas por composições de transformações geométricas (translação, reflexão e rotação), com o uso de instrumentos de desenho ou de softwares de geometria dinâmica (EF08MA18).")]
    unit(R, "transformacoes-geometricas", "G", ["EF08MA18"],
         "Reconhecer e construir figuras obtidas por composições de transformações geométricas (translação, reflexão e rotação), com o uso de instrumentos de desenho ou de softwares de geometria dinâmica",
         "Transformações geométricas: translação, reflexão e rotação", "Transformações geométricas",
         "Atividades de matemática para o 8º ano sobre transformações geométricas no plano cartesiano: translação, reflexão, rotação de 90° e 180°, composição de transformações e o que se conserva. 100 exercícios com gabarito.",
         "Rotação de 180°: (x, y) → (−x, −y)", "Translação, reflexão e rotação conservam forma e tamanho.",
         body, faq, sets, 14, grade="8-ano")


if __name__ == "__main__":
    main()
