# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 2ª série: Lei dos senos e lei dos cossenos (EM13MAT308)
  python3 tools/gen_br_matematica_em2_leis_dos_senos_e_dos_cossenos.py
Lei dos cossenos (calcular um lado ou um ângulo), lei dos senos (lados, ângulos e raio da circunferência circunscrita),
área de um triângulo por (a · b · sen C) ÷ 2, problemas (distâncias inacessíveis, terrenos, navegação).
Erros: esquecer o «− 2bc cos A», usar cos 120° positivo, aplicar a lei dos senos com o lado que não é oposto ao ângulo.
"""
import random
from fractions import Fraction as F
from br_em import M, d, fq, bank, mix, lesson, unit, tri, sq

R = random.Random(92002)
COS = {60: F(1, 2), 120: F(-1, 2), 90: F(0)}
ANG = [(7, 3, 8, 60), (7, 5, 8, 60), (7, 3, 5, 120), (13, 7, 15, 60), (13, 8, 15, 60), (5, 3, 4, 90), (13, 5, 12, 90), (14, 6, 10, 120)]


def s1_lado():
    A = R.choice([60, 120, 90, 60])
    b, c = R.sample(range(2, 11), 2)
    a2 = b * b + c * c - 2 * b * c * COS[A]
    if a2.denominator != 1 or a2 <= 0:
        return None
    a2 = int(a2)
    ans = sq(a2)
    wrong = [sq(b * b + c * c) if A != 90 else sq(b * b + c * c + b * c), sq(int(b * b + c * c + 2 * b * c * COS[A])) if A != 90 else str(b + c), str(b + c)]
    import math
    g = tri(math.sqrt(a2), b, c, [("A", "B", str(c)), ("C", "A", str(b)), ("B", "C", "a")], [("A", "%d°" % A)], label="triângulo com dois lados e o ângulo entre eles")
    return M(g + "Quanto mede o lado a?", ans, wrong,
             "a² = %d² + %d² − 2 · %d · %d · cos %d° = %d %s %s = %d; a = <b>%s</b>." % (b, c, b, c, A, b * b + c * c, "−" if COS[A] >= 0 else "+", d(abs(2 * b * c * COS[A])), a2, ans))


def s2_angulo():
    a, b, c, A = R.choice(ANG)
    g = tri(a, b, c, [("A", "B", str(c)), ("C", "A", str(b)), ("B", "C", str(a))], [("A", "?")], label="triângulo com os três lados conhecidos")
    cosA = F(b * b + c * c - a * a, 2 * b * c)
    return M(g + "Quanto mede o ângulo Â?", "%d°" % A, [x for x in ("30°", "45°", "60°", "90°", "120°", "150°") if x != "%d°" % A][:4],
             "cos Â = (%d² + %d² − %d²) ÷ (2 · %d · %d) = %s ⇒ <b>Â = %d°</b>." % (b, c, a, b, c, fq(cosA), A))


SIN = {30: "1/2", 45: "√2/2", 60: "√3/2", 90: "1", 120: "√3/2", 135: "√2/2", 150: "1/2"}
RATIO = {(30, 45): "√2", (30, 60): "√3", (45, 60): "√6/2", (30, 90): "2", (45, 90): "√2", (60, 90): "2√3/3", (45, 30): "√2/2", (60, 30): "√3/3", (60, 45): "√6/3", (30, 120): "√3", (45, 120): "√6/2", (30, 135): "√2"}


def mul(k, r):
    """k · razão como texto"""
    if r == "2":
        return str(2 * k)
    if "/" in r:
        num_, den = r.split("/")
        coef = 1 if num_.startswith("√") else int(num_.split("√")[0])
        rad = num_[num_.index("√"):] if "√" in num_ else ""
        v = F(k * coef, int(den))
        if v.denominator == 1:
            return ("%d%s" % (v.numerator, rad)) if v != 1 else rad
        return None
    return ("%d%s" % (k, r)) if k != 1 else r


def s3_senos():
    A, B = R.choice(list(RATIO))
    k = R.choice([2, 4, 6, 8, 10, 12])
    ans = mul(k, RATIO[(A, B)])
    if not ans:
        return None
    C = 180 - A - B
    if C <= 0:
        return None
    w = [mul(k, RATIO[(B, A)]) if (B, A) in RATIO else str(k + 1), str(k), mul(k, "√2") if "√2" not in ans else mul(k, "√3")]
    import math
    a, b = math.sin(math.radians(A)), math.sin(math.radians(B))
    g = tri(a, b, math.sin(math.radians(C)), [("B", "C", str(k)), ("C", "A", "x")], [("A", "%d°" % A), ("B", "%d°" % B)], label="triângulo com dois ângulos e um lado")
    return M(g + "Pela lei dos senos, quanto mede x?", ans, [x for x in w if x],
             "x ÷ sen %d° = %d ÷ sen %d° ⇒ x = %d · (%s) ÷ (%s) = <b>%s</b>." % (B, k, A, k, SIN[B], SIN[A], ans))


def s4_area_raio():
    k = R.choice(["area", "area", "raio"])
    if k == "area":
        a, b = R.randint(2, 12), R.randint(2, 12)
        C = R.choice([30, 90, 150, 60, 45])
        if C in (30, 150, 90):
            v = F(a * b, 4) if C != 90 else F(a * b, 2)
            ans = d(v)
        else:
            v = F(a * b, 4)
            ans = (d(v) if v != 1 else "") + ("√3" if C == 60 else "√2")
        return M("Dois lados de um triângulo medem %d cm e %d cm e formam um ângulo de %d°. Qual é a área? (sen %d° = %s)" % (a, b, C, C, SIN[C]), ans + " cm²", [d(a * b) + " cm²", d(F(a * b, 2)) + " cm²" if C != 90 else d(F(a * b, 4)) + " cm²", d(a + b) + " cm²"],
                 "A = %d · %d · sen %d° ÷ 2 = <b>%s cm²</b>." % (a, b, C, ans))
    A = R.choice([30, 90, 150])
    a = R.choice([4, 6, 8, 10, 12])
    Rr = F(a, 2) / (F(1, 2) if A != 90 else 1)
    return M("Num triângulo, o lado oposto ao ângulo de %d° mede %d cm. Qual é o raio da circunferência circunscrita?" % (A, a), "%s cm" % d(Rr), ["%s cm" % d(2 * Rr), "%s cm" % d(F(a, 4)), "%s cm" % d(Rr + 1)],
             "a ÷ sen Â = 2R ⇒ %d ÷ %s = 2R ⇒ <b>R = %s cm</b>." % (a, SIN[A], d(Rr)))


s5_problemas = bank(R, [
    ("De um ponto, dois postes estão a 30 m e 50 m, e o ângulo entre as direções é 60°. Qual é a distância entre os postes?", "√1.900 m ≈ 43,6 m", ["80 m", "√3.400 m ≈ 58,3 m", "20 m"]),
    ("Um terreno triangular tem lados de 40 m e 30 m formando 90°. Qual é a área?", "600 m²", ["1.200 m²", "70 m²", "300 m²"]),
    ("Dois barcos saem do mesmo porto em direções que formam 120°: um navega 3 km e o outro 5 km. Qual a distância entre eles?", "7 km", ["8 km", "√19 km", "2 km"]),
    ("Num triângulo, Â = 30°, B̂ = 45° e o lado oposto a Â mede 10 m. Quanto mede o lado oposto a B̂?", "10√2 m", ["10 m", "5√2 m", "20 m"]),
    ("A lei dos cossenos, para um ângulo de 90°, vira…", "o teorema de Pitágoras", ["a lei dos senos", "a fórmula da área", "a soma dos ângulos"]),
    ("Para usar a lei dos senos é preciso conhecer…", "um lado e o ângulo oposto a ele (mais um dado)", ["só os três ângulos", "só um lado", "a área"]),
    ("Se num triângulo a² &gt; b² + c², o ângulo Â é…", "obtuso", ["agudo", "reto", "nulo"]),
    ("cos 120° vale…", "−1/2", ["1/2", "√3/2", "−√3/2"]),
    ("Os lados de um triângulo medem 5, 7 e 8. O maior ângulo fica oposto ao lado de medida…", "8", ["5", "7", "todos são iguais"]),
], "s5_problemas")


def main():
    seen = set()
    sets = [
        ("Lei dos cossenos: lados", mix(R, seen, [(s1_lado, 20)])),
        ("Lei dos cossenos: ângulos", mix(R, seen, [(s2_angulo, 8), (s1_lado, 12)])),
        ("Lei dos senos", mix(R, seen, [(s3_senos, 20)])),
        ("Área e raio da circunscrita", mix(R, seen, [(s4_area_raio, 20)])),
        ("Problemas", mix(R, seen, [(s5_problemas, 9), (s3_senos, 5), (s1_lado, 6)])),
    ]
    body = lesson(
        ["Servem para <b>qualquer triângulo</b>, não só o retângulo. Nomeie: lado a oposto a Â, b oposto a B̂, c oposto a Ĉ.",
         "<b>Lei dos cossenos</b>: a² = b² + c² − 2bc · cos Â. Use quando souber dois lados e o ângulo entre eles, ou os três lados.",
         "<b>Lei dos senos</b>: a ÷ sen Â = b ÷ sen B̂ = c ÷ sen Ĉ = 2R (R: raio da circunferência circunscrita). Use com dois ângulos e um lado.",
         "<b>Área</b>: A = a · b · sen Ĉ ÷ 2. Lembre: cos 120° = −1/2, sen 120° = √3/2, sen 150° = 1/2."],
        [("b = 3, c = 5, Â = 120°", ["a² = 9 + 25 − 2 · 3 · 5 · (−1/2) = 34 + 15"], "a = 7"),
         ("Â = 30°, B̂ = 45°, a = 6", ["b = 6 · (√2/2) ÷ (1/2)"], "b = 6√2")],
        [["Esquecer o «− 2bc cos Â»", "Sem esse termo, é Pitágoras, que só vale com 90°."],
         ["Usar cos 120° = 1/2", "Ângulo obtuso: cosseno negativo."],
         ["Pareamento errado na lei dos senos", "Cada lado vai com o ângulo oposto a ele."]])
    faq = [("Quando usar a lei dos senos e quando usar a dos cossenos?", "Lei dos cossenos: dois lados e o ângulo entre eles, ou três lados. Lei dos senos: dois ângulos e um lado, ou dois lados e o ângulo oposto a um deles."),
           ("O que a BNCC pede?", "Aplicar as relações métricas, incluindo as leis do seno e do cosseno ou as noções de congruência e semelhança, para resolver e elaborar problemas que envolvem triângulos, em variados contextos (EM13MAT308).")]
    unit(R, "leis-dos-senos-e-dos-cossenos", "G", ["EM13MAT308"],
         "Aplicar as relações métricas, incluindo as leis do seno e do cosseno ou as noções de congruência e semelhança, para resolver e elaborar problemas que envolvem triângulos, em variados contextos",
         "Lei dos senos e lei dos cossenos", "Leis dos senos e dos cossenos",
         "Atividades de matemática para a 2ª série do Ensino Médio sobre a lei dos senos e a lei dos cossenos: calcular lados e ângulos de qualquer triângulo, área com o seno, raio da circunferência circunscrita e problemas. 100 exercícios com gabarito.",
         "a² = b² + c² − 2bc · cos Â", "a ÷ sen Â = b ÷ sen B̂ = 2R.",
         body, faq, sets, 2, grade="2-serie")


if __name__ == "__main__":
    main()
