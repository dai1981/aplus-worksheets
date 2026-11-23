# -*- coding: utf-8 -*-
"""
Brasil Matemática 6º ano: Polígonos, triângulos e quadriláteros (Geometria, EF06MA18, EF06MA19, EF06MA20)
  python3 tools/gen_br_matematica_6_poligonos_triangulos_e_quadrilateros.py
Polígonos (nome pelo número de lados, regulares e não regulares, convexos); triângulos quanto aos lados e aos ângulos;
soma dos ângulos internos do triângulo (180°); quadriláteros: paralelogramo, retângulo, losango, quadrado, trapézio e suas propriedades;
inclusão de classes (todo quadrado é retângulo e losango).
Usa desenhos do 5º ano (polígonos) com outro sorteio.
Erros: achar que quadrado não é retângulo, classificar o triângulo só pelos lados quando pedem os ângulos, somar 360° no triângulo.
"""
import random
from br_common import lesson, mix, use
from br_9 import M, bank, unit

R = random.Random(86014)
p_nome, p_eh, p_tri = use("gen_br_matematica_5_poligonos", 86914, "s1_nome", "s2_eh", "s4_triangulos")
NOMES = {3: "triângulo", 4: "quadrilátero", 5: "pentágono", 6: "hexágono", 7: "heptágono", 8: "octógono", 9: "eneágono", 10: "decágono", 11: "undecágono", 12: "dodecágono"}


def s1_lados():
    n = R.choice(sorted(NOMES))
    if R.random() < 0.5:
        return M("Quantos lados tem um %s?" % NOMES[n], str(n), [str(n + 1), str(n - 1), str(n + 2)], "Um %s tem <b>%d lados</b> (e %d vértices e %d ângulos)." % (NOMES[n], n, n, n))
    return M("Como se chama o polígono de %d lados?" % n, NOMES[n], [NOMES[m] for m in sorted(NOMES) if m != n and abs(m - n) <= 3][:3], "<b>%s</b>." % NOMES[n].capitalize())


def s2_angulos():
    k = R.choice(["terceiro", "classe", "classe"])
    a, b = R.randint(20, 100), R.randint(20, 100)
    c = 180 - a - b
    if c <= 5:
        return None
    if k == "terceiro":
        return M("Dois ângulos de um triângulo medem %d° e %d°. Quanto mede o terceiro?" % (a, b), "%d°" % c, ["%d°" % (360 - a - b), "%d°" % (a + b), "%d°" % (180 - a)], "A soma dos ângulos é 180°: 180 − %d − %d = <b>%d°</b>." % (a, b, c))
    mx = max(a, b, c)
    ans = "acutângulo" if mx < 90 else ("retângulo" if mx == 90 else "obtusângulo")
    return M("Um triângulo tem ângulos de %d°, %d° e %d°. Quanto aos ângulos, ele é…" % (a, b, c), ans, [x for x in ["acutângulo", "retângulo", "obtusângulo", "equilátero"] if x != ans],
             "O maior ângulo mede %d°: %s. <b>%s</b>." % (mx, "menor que 90°" if mx < 90 else ("90°" if mx == 90 else "maior que 90°"), ans.capitalize()))


def s3_lados_tri():
    k = R.choice(["equi", "iso", "esc", "exist"])
    if k == "exist":
        a, b, c = sorted(R.sample(range(2, 15), 3))
        ok = a + b > c
        ans = "sim" if ok else "não"
        return M("É possível construir um triângulo com lados de %d cm, %d cm e %d cm?" % (a, b, c), ans, ["não" if ok else "sim", "só se for retângulo", "sempre é possível"],
                 "Os dois menores lados somam %d, que é %s %d: <b>%s</b>." % (a + b, "maior que" if ok else "menor ou igual a", c, ans))
    if k == "equi":
        L = R.randint(3, 15)
        s = (L, L, L)
    elif k == "iso":
        L, m = R.sample(range(3, 15), 2)
        if 2 * L <= m:
            return None
        s = (L, L, m)
    else:
        s = tuple(R.sample(range(3, 15), 3))
        if sum(s) - max(s) <= max(s):
            return None
    ans = {"equi": "equilátero", "iso": "isósceles", "esc": "escaleno"}[k]
    return M("Um triângulo tem lados de %d cm, %d cm e %d cm. Quanto aos lados, ele é…" % s, ans, [x for x in ["equilátero", "isósceles", "escaleno", "retângulo"] if x != ans],
             "Lados iguais: %s. <b>%s</b>." % ({"equi": "os três", "iso": "dois", "esc": "nenhum"}[k], ans.capitalize()))


s4_quad = bank(R, [
    ("Um quadrilátero com dois pares de lados paralelos é um…", "paralelogramo", ["trapézio", "triângulo", "pentágono"]),
    ("Um quadrilátero com apenas um par de lados paralelos é um…", "trapézio", ["paralelogramo", "losango", "retângulo"]),
    ("Um paralelogramo com os quatro ângulos retos é um…", "retângulo", ["losango", "trapézio", "pentágono"]),
    ("Um paralelogramo com os quatro lados iguais é um…", "losango", ["retângulo", "trapézio", "triângulo"]),
    ("Um quadrilátero com quatro lados iguais e quatro ângulos retos é um…", "quadrado", ["losango que não é retângulo", "trapézio", "retângulo que não é losango"]),
    ("Todo quadrado é também…", "retângulo e losango", ["trapézio isósceles", "só losango", "só retângulo"]),
    ("Todo retângulo é um quadrado?", "não, só quando os lados são iguais", ["sim, sempre", "sim, porque tem ângulos retos", "não, porque não tem lados paralelos"]),
    ("A soma dos ângulos internos de um quadrilátero é…", "360°", ["180°", "540°", "90°"]),
    ("As diagonais de um retângulo são…", "iguais", ["perpendiculares sempre", "diferentes", "paralelas"]),
    ("As diagonais de um losango são…", "perpendiculares", ["iguais sempre", "paralelas", "inexistentes"]),
    ("Num paralelogramo, os lados opostos são…", "paralelos e iguais", ["perpendiculares", "diferentes", "sempre iguais aos outros"]),
    ("Um trapézio com os lados não paralelos iguais chama-se…", "trapézio isósceles", ["trapézio retângulo", "losango", "paralelogramo"]),
    ("Um polígono regular tem…", "todos os lados e todos os ângulos iguais", ["só os lados iguais", "só os ângulos iguais", "lados paralelos"]),
    ("Um losango que não é quadrado é um polígono regular?", "não", ["sim", "só se tiver lados iguais", "só se for grande"]),
    ("Num quadrilátero, três ângulos medem 90°, 90° e 70°. O quarto mede…", "110°", ["90°", "70°", "180°"]),
    ("Um triângulo pode ter dois ângulos retos?", "não, a soma passaria de 180°", ["sim", "só se for isósceles", "só se for equilátero"]),
    ("Cada ângulo de um triângulo equilátero mede…", "60°", ["90°", "45°", "180°"]),
    ("Um triângulo retângulo isósceles tem ângulos de…", "90°, 45° e 45°", ["90°, 60° e 30°", "60°, 60° e 60°", "90°, 90° e 0°"]),
], "s4_quad")


def main():
    seen = set()
    sets = [
        ("Polígonos", mix(R, seen, [(p_nome, 8), (s1_lados, 8), (p_eh, 4)])),
        ("Triângulos quanto aos lados", mix(R, seen, [(p_tri, 8), (s3_lados_tri, 12)])),
        ("Ângulos do triângulo", mix(R, seen, [(s2_angulos, 20)])),
        ("Quadriláteros", mix(R, seen, [(s4_quad, 18), (s1_lados, 2)])),
        ("Revisão", mix(R, seen, [(s2_angulos, 8), (s3_lados_tri, 8), (p_tri, 4)])),
    ]
    body = lesson(
        ["<b>Polígonos</b> são figuras planas fechadas formadas por segmentos. O nome vem do número de lados: triângulo, quadrilátero, pentágono, hexágono…",
         "Triângulos — pelos lados: equilátero (3 iguais), isósceles (2 iguais), escaleno (nenhum igual). Pelos ângulos: acutângulo, retângulo (um de 90°), obtusângulo (um maior que 90°). A soma dos ângulos é 180°.",
         "Quadriláteros: <b>paralelogramos</b> (2 pares de lados paralelos: retângulo, losango, quadrado) e <b>trapézios</b> (1 par). O quadrado é retângulo e losango ao mesmo tempo.",
         "Para existir triângulo, a soma dos dois lados menores precisa ser maior que o maior lado."],
        [("Ângulos 50° e 70°", ["180 − 50 − 70"], "o terceiro mede 60°"),
         ("Lados 3, 4 e 8", ["3 + 4 = 7 &lt; 8"], "não forma triângulo")],
        [["Achar que quadrado não é retângulo", "Ele tem 4 ângulos retos: é retângulo."],
         ["Confundir classificação por lados e por ângulos", "Leia se pedem lados ou ângulos."],
         ["Usar 360° no triângulo", "Triângulo: 180°. Quadrilátero: 360°."]])
    faq = [("Todo quadrado é retângulo?", "Sim. O retângulo é o quadrilátero com 4 ângulos retos; o quadrado tem 4 ângulos retos e ainda os 4 lados iguais, então é um retângulo especial (e também um losango)."),
           ("O que a BNCC pede no 6º ano?", "Reconhecer, nomear e comparar polígonos (EF06MA18), identificar características dos triângulos e classificá-los em relação às medidas dos lados e dos ângulos (EF06MA19) e identificar características dos quadriláteros, classificá-los e reconhecer a inclusão e a intersecção de classes (EF06MA20).")]
    unit(R, "poligonos-triangulos-e-quadrilateros", "G", ["EF06MA18", "EF06MA19", "EF06MA20"],
         "Reconhecer, nomear e comparar polígonos, considerando lados, vértices e ângulos, e classificá-los em regulares e não regulares; identificar características dos triângulos e classificá-los em relação às medidas dos lados e dos ângulos; identificar características dos quadriláteros, classificá-los em relação a lados e a ângulos e reconhecer a inclusão e a intersecção de classes entre eles",
         "Polígonos, triângulos e quadriláteros", "Polígonos, triângulos e quadriláteros",
         "Atividades de matemática para o 6º ano sobre polígonos, triângulos e quadriláteros: nomes, classificação dos triângulos por lados e ângulos, soma dos ângulos, condição de existência e propriedades dos quadriláteros. 100 exercícios com gabarito.",
         "Triângulo: 180°. Quadrilátero: 360°.", "Todo quadrado é retângulo e losango.",
         body, faq, sets, 14, grade="6-ano")


if __name__ == "__main__":
    main()
