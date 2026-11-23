# -*- coding: utf-8 -*-
"""
Brasil Matemática 7º ano: Volume de blocos retangulares (Grandezas e medidas, EF07MA29, EF07MA30)
  python3 tools/gen_br_matematica_7_volume_de_blocos_retangulares.py
Volume do bloco retangular (comprimento × largura × altura) e do cubo; cubinhos de 1 cm³; unidades cm³, dm³, m³ e relação com
litros (1 dm³ = 1 L, 1 m³ = 1.000 L); achar uma aresta a partir do volume; problemas com caixas, aquários e caixas d’água.
Usa geradores do 9º ano (volume) e do 5º ano (volume com cubinhos) com outro sorteio.
Erros: somar as arestas, achar que 1 m³ = 100 L, esquecer de converter cm em dm.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, use
from br_9 import M, d, bank, unit

R = random.Random(87017)
v_paral, v_cubo, v_litros = use("gen_br_matematica_9_volume_de_prismas_e_cilindros", 87917, "s1_paral", "s1_cubo_altura", "s4_litros")
c_contar, c_camada = use("gen_br_matematica_5_volume", 87918, "s1_contar", "s1_camada")


def s1_conv():
    k = R.choice(["dm3L", "m3L", "cm3mL", "Lcm3", "m3dm3"])
    n = R.randint(2, 90)
    if k == "dm3L":
        return M("Quantos litros cabem em %d dm³?" % n, "%d L" % n, ["%d L" % (n * 10), "%d L" % (n * 1000), "%s L" % d(F(n, 10))], "1 dm³ = 1 L: <b>%d L</b>." % n)
    if k == "m3L":
        return M("Quantos litros cabem em %d m³?" % n, "%s L" % d(n * 1000), ["%s L" % d(n * 100), "%d L" % n, "%s L" % d(n * 10)], "1 m³ = 1.000 L: <b>%s L</b>." % d(n * 1000))
    if k == "cm3mL":
        n = R.randint(20, 900)
        return M("Quantos mL cabem em %d cm³?" % n, "%d mL" % n, ["%s mL" % d(n * 10), "%s mL" % d(F(n, 10)), "%s mL" % d(n * 1000)], "1 cm³ = 1 mL: <b>%d mL</b>." % n)
    if k == "Lcm3":
        n = R.choice([F(1, 2), 1, 2, F(3, 2), 5, F(5, 2), 10])
        return M("Quantos cm³ há em %s L?" % d(n), "%s cm³" % d(n * 1000), ["%s cm³" % d(n * 100), "%s cm³" % d(n * 10), "%s cm³" % d(n * 10 ** 6)], "1 L = 1 dm³ = 1.000 cm³: <b>%s cm³</b>." % d(n * 1000))
    return M("Quantos dm³ há em %d m³?" % n, "%s dm³" % d(n * 1000), ["%s dm³" % d(n * 100), "%s dm³" % d(n * 10), "%d dm³" % n], "1 m³ = 1.000 dm³ (10 × 10 × 10): <b>%s dm³</b>." % d(n * 1000))


def s2_aresta():
    k = R.choice(["cubo", "alt"])
    if k == "cubo":
        a = R.randint(2, 10)
        return M("Um cubo tem volume de %s cm³. Quanto mede a aresta?" % d(a ** 3), "%d cm" % a, ["%s cm" % d(F(a ** 3, 3), 1) if (F(a ** 3, 3) * 10).denominator == 1 else "%d cm" % (a * a), "%d cm" % (a * a), "%d cm" % (a + 1)],
                     "Que número multiplicado 3 vezes por ele mesmo dá %s? %d × %d × %d: <b>%d cm</b>." % (d(a ** 3), a, a, a, a))
    c, l, h = R.randint(4, 20), R.randint(3, 12), R.randint(2, 15)
    return M("Uma caixa tem %d cm de comprimento, %d cm de largura e volume de %s cm³. Qual é a altura?" % (c, l, d(c * l * h)), "%d cm" % h, ["%s cm" % d(c * l * h - c * l), "%d cm" % (c * l), "%d cm" % (h + 2)],
             "%s ÷ (%d × %d) = %s ÷ %d = <b>%d cm</b>." % (d(c * l * h), c, l, d(c * l * h), c * l, h))


def s3_problemas():
    k = R.choice(["caixa_dagua", "piscina", "areia", "caixas"])
    if k == "caixa_dagua":
        c, l, h = R.choice([(2, 1, 1), (1, 1, 1), (3, 2, 1), (2, 2, 1), (4, 2, 1)])
        return M("Uma caixa d’água em forma de bloco mede %d m × %d m × %d m. Quantos litros cabem nela?" % (c, l, h), "%s L" % d(c * l * h * 1000), ["%s L" % d(c * l * h * 100), "%d L" % (c * l * h), "%s L" % d((c + l + h) * 1000)],
                 "%d × %d × %d = %d m³ = <b>%s L</b>." % (c, l, h, c * l * h, d(c * l * h * 1000)))
    if k == "piscina":
        c, l, p = R.choice([(8, 4, F(3, 2)), (10, 5, 2), (6, 3, 1), (12, 6, F(3, 2)), (5, 4, F(6, 5))])
        V = c * l * p
        return M("Uma piscina tem %d m de comprimento, %d m de largura e %s m de profundidade. Qual é o seu volume?" % (c, l, d(p)), "%s m³" % d(V), ["%s m³" % d(c * l), "%s m³" % d(c + l + p), "%s m³" % d(V * 1000)],
                 "%d × %d × %s = <b>%s m³</b>." % (c, l, d(p), d(V)))
    if k == "areia":
        c, l, h = R.randint(2, 6), R.randint(1, 4), F(R.randint(1, 5), 10)
        V = c * l * h
        return M("Uma caçamba retangular mede %d m × %d m e está cheia de areia até %s m de altura. Quantos m³ de areia há?" % (c, l, d(h)), "%s m³" % d(V), ["%d m³" % (c * l), "%s m³" % d(V * 10), "%s m³" % d(c + l + h)],
                 "%d × %d × %s = <b>%s m³</b>." % (c, l, d(h), d(V)))
    a = R.choice([10, 20, 25, 50])
    c, l, h = R.choice([(100, 50, 50), (200, 100, 50), (100, 100, 100), (50, 50, 50)])
    if c % a or l % a or h % a:
        return None
    n = (c // a) * (l // a) * (h // a)
    return M("Quantas caixas cúbicas de %d cm de aresta cabem num baú de %d cm × %d cm × %d cm?" % (a, c, l, h), d(n), [d(c * l * h // a), d((c + l + h) // a), d(n // 2)],
             "%d × %d × %d = <b>%s caixas</b>." % (c // a, l // a, h // a, d(n)))


def main():
    seen = set()
    sets = [
        ("Contar cubinhos", mix(R, seen, [(c_contar, 12), (c_camada, 8)])),
        ("Volume do bloco e do cubo", mix(R, seen, [(v_paral, 12), (v_cubo, 8)])),
        ("Unidades de volume e capacidade", mix(R, seen, [(s1_conv, 20)])),
        ("Achar uma aresta", mix(R, seen, [(s2_aresta, 20)])),
        ("Problemas", mix(R, seen, [(s3_problemas, 14), (v_litros, 6)])),
    ]
    body = lesson(
        ["O <b>volume</b> mede o espaço ocupado. Um cubinho de 1 cm de aresta tem 1 cm³.",
         "Bloco retangular: V = comprimento × largura × altura. Cubo: V = a × a × a = a³.",
         "Capacidade: 1 cm³ = 1 mL; 1 dm³ = 1 L; 1 m³ = 1.000 L."],
        [("Caixa de 20 cm × 10 cm × 5 cm", ["20 × 10 × 5"], "1.000 cm³ = 1 L"),
         ("Caixa d’água de 2 m × 1 m × 1 m", ["2 m³"], "2.000 L")],
        [["Somar as arestas", "Volume é produto: c × l × h."],
         ["Achar que 1 m³ = 100 L", "1 m³ = 1.000 L."],
         ["Misturar unidades", "Use todas as medidas na mesma unidade."]])
    faq = [("Quantos litros cabem em 1 m³?", "1.000 litros, porque 1 m³ = 10 dm × 10 dm × 10 dm = 1.000 dm³, e cada dm³ é 1 litro."),
           ("O que a BNCC pede no 7º ano?", "Resolver e elaborar problemas que envolvam medidas de grandezas inseridos em contextos oriundos de situações cotidianas (EF07MA29) e resolver e elaborar problemas de cálculo de medida do volume de blocos retangulares, envolvendo as unidades usuais (EF07MA30).")]
    unit(R, "volume-de-blocos-retangulares", "M", ["EF07MA29", "EF07MA30"],
         "Resolver e elaborar problemas que envolvam medidas de grandezas inseridos em contextos oriundos de situações cotidianas ou de outras áreas do conhecimento; resolver e elaborar problemas de cálculo de medida do volume de blocos retangulares, envolvendo as unidades usuais (metro cúbico, decímetro cúbico e centímetro cúbico)",
         "Volume de blocos retangulares e capacidade", "Volume de blocos retangulares",
         "Atividades de matemática para o 7º ano sobre volume de blocos retangulares e cubos: cubinhos, unidades cm³, dm³ e m³, litros, achar uma aresta e problemas com caixas e piscinas. 100 exercícios com gabarito.",
         "V = comprimento × largura × altura", "1 dm³ = 1 L; 1 m³ = 1.000 L",
         body, faq, sets, 17, grade="7-ano")


if __name__ == "__main__":
    main()
