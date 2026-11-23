# -*- coding: utf-8 -*-
"""
Brasil Matemática 6º ano: Ampliação e redução de figuras (Geometria, EF06MA21)
  python3 tools/gen_br_matematica_6_ampliacao_e_reducao.py
Ampliar e reduzir figuras em malhas quadriculadas; fator de ampliação ou redução; os ângulos não mudam; o perímetro muda na mesma
razão e a área muda pelo quadrado da razão; escalas de desenhos e mapas; fotos e telas.
Usa desenhos do 5º ano (ampliação e redução) com outro sorteio.
Erros: somar um número a cada lado em vez de multiplicar, achar que a área dobra quando os lados dobram, mudar os ângulos.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, use
from br_9 import M, d, bank, unit

R = random.Random(86015)
a_lado, a_reduzir, a_qual, a_perim = use("gen_br_matematica_5_ampliacao_e_reducao", 86915, "s1_lado", "s1_reduzir", "s2_qual", "s4_perimetro")


def s1_fator():
    k = R.choice([F(2), F(3), F(4), F(1, 2), F(1, 3), F(3, 2), F(5, 2)])
    L = R.randint(2, 12) * 2
    if (L * k).denominator != 1:
        return None
    q = R.choice(["Um retângulo tem um lado de %d cm. Depois de %s, esse lado passou a medir %s cm. Qual é o fator?" % (L, "ampliado" if k > 1 else "reduzido", d(L * k))])
    return M(q, d(k) if k.denominator == 1 else ("%s" % d(k) if (k * 10).denominator == 1 else "1/%d" % k.denominator), [d(L * k - L) if k > 1 else d(L - L * k), d(1 / k) if (1 / k).denominator == 1 else "1/%d" % (1 / k).denominator, d(k * 2) if k > 1 else "1/%d" % (k.denominator * 2)],
             "Fator = nova medida ÷ medida original = %s ÷ %d = <b>%s</b>." % (d(L * k), L, d(k) if (k * 10).denominator == 1 else "1/%d" % k.denominator))


def s2_area():
    k = R.choice([2, 3, 4, F(1, 2), F(1, 3)])
    k = F(k)
    A = R.choice([6, 8, 9, 12, 18, 24, 36, 48])
    if (A * k * k).denominator != 1:
        return None
    w = "ampliada com fator %s" % d(k) if k > 1 else "reduzida à %s" % {F(1, 2): "metade", F(1, 3): "terça parte"}[k]
    return M("Uma figura de área %d cm² foi %s (todos os lados). Qual é a nova área?" % (A, w), "%s cm²" % d(A * k * k), ["%s cm²" % d(A * k), "%s cm²" % d(A + k) if k > 1 else "%s cm²" % d(A - 1), "%s cm²" % d(A * k * k * k) if (A * k ** 3).denominator == 1 else "%s cm²" % d(A * 2)],
             "Lados × %s, área × %s² = %s: %d × %s = <b>%s cm²</b>." % (d(k) if k > 1 else "1/%d" % k.denominator, d(k) if k > 1 else "(1/%d)" % k.denominator, d(k * k) if k > 1 else "1/%d" % (k * k).denominator, A, d(k * k) if k > 1 else "1/%d" % (k * k).denominator, d(A * k * k)))


def s3_escala():
    e = R.choice([50, 100, 200, 500, 1000])
    cm = R.randint(2, 15)
    real = cm * e
    k = R.choice(["real", "desenho"])
    real_txt = "%s m" % d(F(real, 100)) if real >= 100 else "%d cm" % real
    if k == "real":
        return M("Numa planta na escala 1 : %s, uma parede mede %d cm. Qual é o comprimento real?" % (d(e), cm), real_txt, ["%s m" % d(F(real, 10)), "%s m" % d(F(real, 1000), 3), "%d cm" % (cm + e)],
                 "%d cm × %s = %s cm = <b>%s</b>." % (cm, d(e), d(real), real_txt))
    return M("Numa planta na escala 1 : %s, qual medida terá no desenho uma parede de %s?" % (d(e), real_txt), "%d cm" % cm, ["%d cm" % (cm * 10), "%s cm" % d(F(cm, 10)), "%d cm" % real],
             "%s cm ÷ %s = <b>%d cm</b>." % (d(real), d(e), cm))


s4_conceitos = bank(R, [
    ("Ao ampliar uma figura com fator 2, os ângulos…", "continuam iguais", ["dobram", "caem pela metade", "ficam retos"]),
    ("Ao ampliar uma figura com fator 3, o perímetro…", "fica 3 vezes maior", ["fica 9 vezes maior", "não muda", "aumenta 3 cm"]),
    ("Ao ampliar uma figura com fator 2, a área…", "fica 4 vezes maior", ["fica 2 vezes maior", "não muda", "fica 8 vezes maior"]),
    ("Somar 2 cm a todos os lados de um retângulo 4 cm × 2 cm dá uma figura…", "que não é ampliação (fica deformada)", ["ampliada com fator 2", "igual à original", "reduzida"]),
    ("Um fator de ampliação menor que 1 indica…", "uma redução", ["uma ampliação", "a figura igual", "um erro"]),
    ("Na escala 1 : 100, 1 cm no desenho representa…", "1 m no real", ["10 cm no real", "100 m no real", "1 cm no real"]),
    ("Uma foto 10 cm × 15 cm ampliada sem deformar pode ficar…", "20 cm × 30 cm", ["20 cm × 25 cm", "12 cm × 17 cm", "15 cm × 15 cm"]),
    ("Duas figuras são uma ampliação da outra quando…", "os lados são proporcionais e os ângulos iguais", ["têm a mesma área", "têm o mesmo perímetro", "têm a mesma cor"]),
    ("Um quadrado de lado 3 cm reduzido à terça parte fica com lado…", "1 cm", ["2 cm", "0,3 cm", "9 cm"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Ampliar na malha", mix(R, seen, [(a_lado, 10), (a_qual, 10)])),
        ("Reduzir e o fator", mix(R, seen, [(a_reduzir, 10), (s1_fator, 10)])),
        ("Perímetro e área", mix(R, seen, [(a_perim, 8), (s2_area, 12)])),
        ("Escalas", mix(R, seen, [(s3_escala, 20)])),
        ("Revisão", mix(R, seen, [(s4_conceitos, 9), (s2_area, 5), (s1_fator, 6)])),
    ]
    body = lesson(
        ["<b>Ampliar</b> ou <b>reduzir</b> uma figura sem deformar é multiplicar todos os lados pelo mesmo número, o <b>fator</b>.",
         "Os ângulos não mudam. O perímetro é multiplicado pelo fator; a área, pelo fator ao quadrado.",
         "Numa escala 1 : 100, cada 1 cm do desenho vale 100 cm (1 m) de verdade."],
        [("Retângulo 3 cm × 2 cm, fator 3", ["9 cm × 6 cm", "área: 6 → 54"], "área 9 vezes maior"),
         ("Escala 1 : 200, parede de 4 cm", ["4 × 200 = 800 cm"], "8 m")],
        [["Somar em vez de multiplicar", "Todos os lados são multiplicados pelo fator."],
         ["Achar que a área dobra com fator 2", "Ela fica 4 vezes maior."],
         ["Mudar os ângulos", "Na ampliação, os ângulos ficam iguais."]])
    faq = [("O que acontece com a área quando ampliamos uma figura?", "Se os lados são multiplicados por k, a área é multiplicada por k × k. Com fator 2, a área fica 4 vezes maior."),
           ("O que a BNCC pede no 6º ano?", "Construir figuras planas semelhantes em situações de ampliação e de redução, com o uso de malhas quadriculadas, plano cartesiano ou tecnologias digitais (EF06MA21).")]
    unit(R, "ampliacao-e-reducao", "G", ["EF06MA21"],
         "Construir figuras planas semelhantes em situações de ampliação e de redução, com o uso de malhas quadriculadas, plano cartesiano ou tecnologias digitais",
         "Ampliação e redução de figuras", "Ampliação e redução",
         "Atividades de matemática para o 6º ano sobre ampliação e redução de figuras: malha quadriculada, fator de ampliação, perímetro e área, ângulos e escalas. 100 exercícios com gabarito.",
         "Multiplique todos os lados pelo mesmo fator.", "Área × fator²; ângulos iguais.",
         body, faq, sets, 15, grade="6-ano")


if __name__ == "__main__":
    main()
