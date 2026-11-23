# -*- coding: utf-8 -*-
"""
Brasil Matemática 8º ano: Volume e capacidade (Grandezas e medidas, EF08MA20, EF08MA21)
  python3 tools/gen_br_matematica_8_volume_e_capacidade.py
Relação entre litro e decímetro cúbico (1 L = 1 dm³, 1 mL = 1 cm³, 1 m³ = 1.000 L); volume de blocos retangulares e cilindros;
volume de recipientes por deslocamento de água; quantos copos, garrafas ou caixas cabem.
Usa geradores do 7º ano (unidades de volume) e do 9º ano (paralelepípedo, cilindro, litros) com outro sorteio.
Erros: 1 m³ = 100 L, usar o diâmetro como raio, esquecer de converter as unidades antes de dividir.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, use
from br_9 import M, d, bank, unit
from br_common import num

R = random.Random(88016)
v_conv = use("gen_br_matematica_7_volume_de_blocos_retangulares", 88916, "s1_conv")
v_paral, v_cil, v_litros, v_prob = use("gen_br_matematica_9_volume_de_prismas_e_cilindros", 88926, "s1_paral", "s3_cil", "s4_litros", "s5_problemas")
import gen_br_matematica_9_volume_de_prismas_e_cilindros as V9
PI = F(314, 100)


def s1_desloc():
    c, l = R.choice([(20, 10), (30, 20), (25, 20), (40, 30), (20, 15)])
    sobe = R.choice([1, 2, 3, 4, 5])
    v = c * l * sobe
    obj = R.choice(["uma pedra", "uma bola de ferro", "um enfeite de vidro", "um peso de metal"])
    return M("Um aquário tem base retangular de %d cm por %d cm. Ao colocar %s dentro, a água subiu %d cm. Qual é o volume do objeto?" % (c, l, obj, sobe),
             "%s cm³" % num(v), ["%s cm³" % num(c * l), "%s cm³" % num((c + l) * sobe), "%s cm³" % num(v * 10)],
             "O volume do objeto é o volume da água que subiu: %d × %d × %d = <b>%s cm³</b> (%s mL)." % (c, l, sobe, num(v), num(v)))


def s2_quantos():
    k = R.choice(["copos", "garrafas", "caixa"])
    if k == "copos":
        L = R.choice([2, 3, 5, 6])
        ml = R.choice([200, 250, 300])
        n = L * 1000 // ml
        if L * 1000 % ml:
            return None
        return M("Quantos copos de %d mL é possível encher com %d L de suco?" % (ml, L), str(n), [str(n * 10), str(L * 100 // ml) if L * 100 // ml else str(n // 2), str(n + 2)],
                 "%d L = %s mL; %s ÷ %d = <b>%d copos</b>." % (L, num(L * 1000), num(L * 1000), ml, n))
    if k == "garrafas":
        c, l, a = R.choice([(50, 40, 30), (100, 50, 40), (60, 50, 40), (80, 50, 50)])
        V = c * l * a // 1000
        g = R.choice([2, 5])
        if V % g:
            return None
        return M("Um tanque tem %d cm × %d cm × %d cm. Quantas garrafas de %d L são necessárias para enchê-lo?" % (c, l, a, g), num(V // g), [num(V), num(c * l * a // g), num(V * g)],
                 "V = %s cm³ = %d L; %d ÷ %d = <b>%d garrafas</b>." % (num(c * l * a), V, V, g, V // g))
    a = R.choice([1, 2, 5])
    b = R.choice([10, 20, 25, 50])
    n = (a * 100 // b) ** 3
    return M("Quantos cubinhos de %d cm de aresta cabem numa caixa cúbica de %d m de aresta?" % (b, a), num(n), [num(a * 100 // b), num((a * 100 // b) ** 2), num(n * 10)],
             "%d m = %d cm; %d ÷ %d = %d por aresta; %d³ = <b>%s</b>." % (a, a * 100, a * 100, b, a * 100 // b, a * 100 // b, num(n)))


def s3_cil_litros():
    r = R.choice([5, 10, 20, 30, 50])
    h = R.choice([10, 20, 40, 50, 100])
    V = PI * r * r * h
    return M("Uma lata cilíndrica tem raio %d cm e altura %d cm. Quantos litros cabem nela? (π = 3,14)" % (r, h), "%s L" % d(V / 1000), ["%s L" % d(V / 100), "%s L" % d(V), "%s L" % d(PI * 4 * r * r * h / 1000)],
             "V = 3,14 · %d² · %d = %s cm³; ÷ 1.000 = <b>%s L</b>." % (r, h, num(V) if V.denominator == 1 else d(V), d(V / 1000)))


s4_conceitos = bank(R, [
    ("1 litro equivale a…", "1 dm³", ["1 m³", "1 cm³", "10 cm³"]),
    ("1 m³ equivale a…", "1.000 L", ["100 L", "10 L", "1 L"]),
    ("1 mL equivale a…", "1 cm³", ["1 dm³", "10 cm³", "1 m³"]),
    ("Uma caixa d’água de 1 m × 1 m × 1 m tem capacidade de…", "1.000 L", ["100 L", "1 L", "10.000 L"]),
    ("Se dobramos o raio de um cilindro e mantemos a altura, o volume…", "fica 4 vezes maior", ["dobra", "não muda", "fica 8 vezes maior"]),
    ("Se dobramos as três arestas de um bloco, o volume…", "fica 8 vezes maior", ["dobra", "fica 4 vezes maior", "fica 6 vezes maior"]),
    ("Capacidade é…", "o volume que cabe dentro de um recipiente", ["a área da base", "o peso do recipiente", "o perímetro da tampa"]),
], "s4_conceitos")


def main():
    seen = set()
    sets = [
        ("Litros e decímetros cúbicos", mix(R, seen, [(v_conv, 14), (s4_conceitos, 6)])),
        ("Volume do bloco retangular", mix(R, seen, [(v_paral, 12), (v_litros, 8)])),
        ("Volume do cilindro", mix(R, seen, [(v_cil, 12), (s3_cil_litros, 8)])),
        ("Deslocamento de água e recipientes", mix(R, seen, [(s1_desloc, 10), (s2_quantos, 10)])),
        ("Problemas", mix(R, seen, [(v_prob, 12), (s2_quantos, 4), (v_litros, 4)])),
    ]
    body = lesson(
        ["<b>Capacidade</b> é o volume que cabe num recipiente. 1 L = 1 dm³, 1 mL = 1 cm³ e 1 m³ = 1.000 L.",
         "Bloco retangular: V = c · l · a. Cilindro: V = π · r² · h.",
         "Para medir o volume de um objeto irregular, mergulhe-o na água: o volume de água que sobe é o volume do objeto.",
         "Converta as unidades antes de comparar ou dividir."],
        [("Caixa de 50 cm × 40 cm × 30 cm", ["60.000 cm³ = 60 dm³"], "60 L"),
         ("Aquário 30 cm × 20 cm, água sobe 2 cm", ["30 × 20 × 2"], "1.200 cm³")],
        [["Pensar que 1 m³ = 100 L", "1 m³ = 10 dm × 10 dm × 10 dm = 1.000 dm³ = 1.000 L."],
         ["Usar o diâmetro como raio", "O raio é a metade do diâmetro."],
         ["Dividir sem converter", "Passe tudo para a mesma unidade (mL ou L) antes."]],
        V9.cil(5, 10))
    faq = [("Quantos litros tem 1 m³?", "1 m³ tem 1.000 litros, porque 1 m³ = 1.000 dm³ e 1 dm³ = 1 L."),
           ("O que a BNCC pede no 8º ano?", "Reconhecer a relação entre um litro e um decímetro cúbico e a relação entre litro e metro cúbico, para resolver problemas de cálculo de capacidade de recipientes (EF08MA20), e resolver e elaborar problemas que envolvam o cálculo do volume de recipiente cujo formato é o de um bloco retangular (EF08MA21).")]
    unit(R, "volume-e-capacidade", "M", ["EF08MA20", "EF08MA21"],
         "Reconhecer a relação entre um litro e um decímetro cúbico e a relação entre litro e metro cúbico, para resolver problemas de cálculo de capacidade de recipientes; resolver e elaborar problemas que envolvam o cálculo do volume de recipiente cujo formato é o de um bloco retangular",
         "Volume e capacidade", "Volume e capacidade",
         "Atividades de matemática para o 8º ano sobre volume e capacidade: litro e decímetro cúbico, metro cúbico, blocos retangulares, cilindros, deslocamento de água e problemas. 100 exercícios com gabarito.",
         "1 L = 1 dm³ e 1 m³ = 1.000 L", "Converta antes de calcular.",
         body, faq, sets, 16, grade="8-ano")


if __name__ == "__main__":
    main()
