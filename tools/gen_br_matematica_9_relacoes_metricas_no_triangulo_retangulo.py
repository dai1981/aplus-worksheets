# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: Relações métricas no triângulo retângulo (Geometria, EF09MA13)
  python3 tools/gen_br_matematica_9_relacoes_metricas_no_triangulo_retangulo.py
Altura relativa à hipotenusa: a = m + n, h² = m · n, cateto² = hipotenusa · projeção, b · c = a · h; elementos do triângulo
retângulo (hipotenusa, catetos, projeções); a demonstração do teorema de Pitágoras pela semelhança.
Erros: usar a projeção errada para o cateto, esquecer a raiz quadrada, chamar de hipotenusa um cateto.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix
from br_9 import M, d, formas, unit

R = random.Random(89013)
# (m, n): projeções de AB e AC sobre a hipotenusa BC
TRI = [(F(9), F(16)), (F(16), F(9)), (F(18), F(32)), (F(32), F(18)), (F(36, 10), F(64, 10)), (F(64, 10), F(36, 10)), (F(27), F(48)), (F(48), F(27)),
       (F(18, 10), F(32, 10)), (F(32, 10), F(18, 10)), (F(25), F(144)), (F(144), F(25)), (F(54, 10), F(96, 10)), (F(96, 10), F(54, 10)), (F(4), F(1)), (F(1), F(4)),
       (F(8), F(2)), (F(2), F(8)), (F(12), F(3)), (F(3), F(12))]


def isq(x):
    """raiz exata de um Fraction (ou None)"""
    from math import isqrt
    p, q = x.numerator, x.denominator
    a, b = isqrt(p), isqrt(q)
    return F(a, b) if a * a == p and b * b == q else None


def elems(m, n):
    a = m + n
    h = isq(m * n)
    c = isq(a * m)
    b = isq(a * n)
    return a, h, c, b


def pic(m, n, lab):
    """lab: {'m','n','h','c','b'} → texto"""
    a = m + n
    h = isq(m * n) or (m * n) ** 0.5
    sc = 340.0 / float(a)
    sc = min(sc, 150.0 / float(h))
    W = int(float(a) * sc) + 70
    B, C = (35, 190), (35 + float(a) * sc, 190)
    Hh = (35 + float(m) * sc, 190)
    A = (Hh[0], 190 - float(h) * sc)
    sides = []
    for key, (p, q) in {"m": ("B", "H"), "n": ("H", "C"), "h": ("A", "H"), "c": ("A", "B"), "b": ("A", "C")}.items():
        if key in lab:
            sides.append((p, q, lab[key]))
    sh = {"pts": {"A": A, "B": B, "C": C, "H": Hh}, "poly": "ABC", "segs": [("A", "H")], "right": [("A", "B", "C"), ("H", "A", "C")], "sides": sides, "ref": (Hh[0], 150)}
    if "h" in lab:
        sh["sides"] = [s for s in sides if s[2] != lab["h"]] 
        ex = "<text x='%.1f' y='%.1f' font-size='14' fill='%s' font-weight='700' font-family='sans-serif'>%s</text>" % (Hh[0] + 6, (A[1] + 190) / 2 + 5, "#c0392b" if lab["h"].startswith("x") else "#1f5fbf", lab["h"])
    else:
        ex = ""
    return formas([sh], W=max(W, 300), H=220, label="triângulo retângulo ABC com a altura AH relativa à hipotenusa", extra=ex)


def s1_h():
    m, n = R.choice(TRI)
    a, h, c, b = elems(m, n)
    k = R.choice(["h", "m"])
    if k == "h":
        return M(pic(m, n, {"m": d(m), "n": d(n), "h": "x"}) + "No triângulo retângulo ABC, AH é a altura relativa à hipotenusa (medidas em cm). Quanto mede x?", "%s cm" % d(h),
                 ["%s cm" % d(m * n), "%s cm" % d((m + n) / 2), "%s cm" % d(abs(n - m)) if n != m else "1 cm", "%s cm" % d(h + 1)],
                 "h² = m · n = %s · %s = %s → <b>h = %s cm</b>." % (d(m), d(n), d(m * n), d(h)))
    return M(pic(m, n, {"m": "x", "n": d(n), "h": d(h)}) + "No triângulo retângulo ABC, AH é a altura relativa à hipotenusa (medidas em cm). Quanto mede x?", "%s cm" % d(m),
             ["%s cm" % d(h * h * n), "%s cm" % d(n - h) if n > h else "%s cm" % d(h - n), "%s cm" % d(F(n, h)) if (F(n, h) * 100).denominator == 1 else "%s cm" % d(m + 2), "%s cm" % d(m + 1)],
             "h² = m · n → %s = x · %s → <b>x = %s cm</b>." % (d(h * h), d(n), d(m)))


def s2_cateto():
    m, n = R.choice(TRI)
    a, h, c, b = elems(m, n)
    if c is None:
        return None
    k = R.choice(["c", "proj"])
    if k == "c":
        return M(pic(m, n, {"m": d(m), "n": d(n), "c": "x"}) + "No triângulo retângulo ABC, AH é a altura (medidas em cm). Quanto mede o cateto x = AB?", "%s cm" % d(c),
                 ["%s cm" % d(isq(a * n)) if isq(a * n) else "%s cm" % d(a), "%s cm" % d(a * m), "%s cm" % d(isq(m * n)), "%s cm" % d(c + 1)],
                 "c² = a · m (hipotenusa vezes a projeção de AB) = %s · %s = %s → <b>x = %s cm</b>." % (d(a), d(m), d(a * m), d(c)))
    return M(pic(m, n, {"m": "x", "c": d(c)}) + "No triângulo retângulo ABC, a hipotenusa BC mede %s cm e AH é a altura. Quanto mede a projeção x = BH?" % d(a), "%s cm" % d(m),
             ["%s cm" % d(n), "%s cm" % d(c * c / a + 1), "%s cm" % d(a - c), "%s cm" % d(a * c, 1) if (a * c * 10).denominator == 1 else "%s cm" % d(m + 2)],
             "c² = a · m → %s = %s · x → <b>x = %s cm</b>." % (d(c * c), d(a), d(m)))


def s3_bc_ah():
    m, n = R.choice(TRI)
    a, h, c, b = elems(m, n)
    if None in (b, c):
        return None
    return M(pic(m, n, {"c": d(c), "b": d(b), "h": "x"}) + "No triângulo retângulo ABC, os catetos medem %s cm e %s cm, e a hipotenusa mede %s cm. Quanto mede a altura x relativa à hipotenusa?" % (d(c), d(b), d(a)), "%s cm" % d(h),
             ["%s cm" % d(c * b / 2), "%s cm" % d((c + b) / 2), "%s cm" % d(a - b), "%s cm" % d(h + 2)],
             "b · c = a · h → %s · %s = %s · x → <b>x = %s cm</b>." % (d(b), d(c), d(a), d(h)))


def s4_hip():
    m, n = R.choice(TRI)
    a, h, c, b = elems(m, n)
    k = R.choice(["a", "n"])
    if k == "a":
        return M("No triângulo retângulo ABC, as projeções dos catetos sobre a hipotenusa medem %s cm e %s cm. Quanto mede a hipotenusa?" % (d(m), d(n)), "%s cm" % d(a), ["%s cm" % d(m * n), "%s cm" % d(isq(m * n)), "%s cm" % d(abs(n - m)) if m != n else "1 cm", "%s cm" % d(a * 2)],
                 "a = m + n = %s + %s = <b>%s cm</b>." % (d(m), d(n), d(a)))
    return M("A hipotenusa de um triângulo retângulo mede %s cm, e a projeção de um cateto sobre ela mede %s cm. Quanto mede a projeção do outro cateto?" % (d(a), d(m)), "%s cm" % d(n), ["%s cm" % d(a + m), "%s cm" % d(m), "%s cm" % d(a * m), "%s cm" % d(n + 1)],
             "m + n = a → n = %s − %s = <b>%s cm</b>." % (d(a), d(m), d(n)))


def s5_teoria():
    q, a, w = R.choice([
        ("No triângulo retângulo, a hipotenusa é…", "o lado oposto ao ângulo reto", ["o maior cateto", "a altura relativa a um cateto", "o lado adjacente ao ângulo reto"]),
        ("A altura relativa à hipotenusa divide o triângulo retângulo em dois triângulos…", "semelhantes ao triângulo original", ["congruentes entre si sempre", "equiláteros", "sem relação com o original"]),
        ("Qual relação liga a altura h às projeções m e n?", "h² = m · n", ["h = m + n", "h² = m + n", "h = m · n"]),
        ("Qual relação liga o cateto b, a hipotenusa a e a projeção n de b?", "b² = a · n", ["b = a · n", "b² = a + n", "b² = m · n"]),
        ("Somando b² = a · n e c² = a · m, obtemos…", "b² + c² = a², o teorema de Pitágoras", ["b + c = a", "b² · c² = a²", "h² = m · n"]),
        ("Qual relação liga os catetos b e c, a hipotenusa a e a altura h?", "b · c = a · h", ["b + c = a + h", "b · c = h²", "b² = a · h"]),
        ("As projeções dos catetos sobre a hipotenusa somam…", "a hipotenusa", ["a altura", "o maior cateto", "180°"]),
        ("No triângulo retângulo, o maior lado é sempre…", "a hipotenusa", ["um cateto", "a altura", "a projeção maior"]),
    ])
    return M(q, a, w, "Resposta: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Elementos e projeções", mix(R, seen, [(s4_hip, 14), (s5_teoria, 6)])),
        ("Altura: h² = m · n", mix(R, seen, [(s1_h, 20)])),
        ("Catetos: c² = a · m", mix(R, seen, [(s2_cateto, 20)])),
        ("b · c = a · h", mix(R, seen, [(s3_bc_ah, 10), (s1_h, 6), (s4_hip, 4)])),
        ("Revisão das relações métricas", mix(R, seen, [(s2_cateto, 6), (s1_h, 6), (s4_hip, 6), (s5_teoria, 2)])),
    ]
    body = lesson(
        ["No triângulo retângulo ABC (ângulo reto em A), BC = a é a <b>hipotenusa</b>, AB = c e AC = b são os <b>catetos</b>.",
         "A altura AH = h divide a hipotenusa nas <b>projeções</b> m (de AB) e n (de AC). Os três triângulos formados são semelhantes.",
         "Da semelhança saem: a = m + n; h² = m · n; c² = a · m; b² = a · n; b · c = a · h.",
         "Somando c² = a · m e b² = a · n: b² + c² = a(m + n) = a². É o <b>teorema de Pitágoras</b>."],
        [("m = 9, n = 16", ["h² = 9 · 16 = 144"], "h = 12"),
         ("a = 25, m = 9", ["c² = 25 · 9 = 225"], "c = 15")],
        [["Usar a projeção errada", "Cada cateto vai com a projeção que fica ao lado dele."],
         ["Esquecer a raiz quadrada", "h² = 144 dá h = 12, não 144."],
         ["Chamar um cateto de hipotenusa", "A hipotenusa fica em frente ao ângulo reto."]],
        pic(F(9), F(16), {"m": "m", "n": "n", "h": "h", "c": "c", "b": "b"}))
    faq = [("Quais são as relações métricas no triângulo retângulo?", "a = m + n, h² = m · n, b² = a · n, c² = a · m e b · c = a · h, em que a é a hipotenusa, b e c os catetos, h a altura relativa à hipotenusa e m e n as projeções."),
           ("O que a BNCC pede no 9º ano?", "Demonstrar relações métricas do triângulo retângulo, entre elas o teorema de Pitágoras, utilizando inclusive a semelhança de triângulos (EF09MA13).")]
    unit(R, "relacoes-metricas-no-triangulo-retangulo", "G", ["EF09MA13"],
         "Demonstrar relações métricas do triângulo retângulo, entre elas o teorema de Pitágoras, utilizando, inclusive, a semelhança de triângulos",
         "Relações métricas no triângulo retângulo", "Relações métricas",
         "Atividades de matemática para o 9º ano sobre relações métricas no triângulo retângulo: hipotenusa, catetos, projeções, altura, h² = m · n, c² = a · m e b · c = a · h. 100 exercícios com gabarito.",
         "h² = m · n e c² = a · m", "Tudo vem da semelhança dos triângulos formados pela altura.",
         body, faq, sets, 13)


if __name__ == "__main__":
    main()
