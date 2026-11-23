# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 2ª série: Cilindros, cones e esferas (EM13MAT309)
  python3 tools/gen_br_matematica_em2_cilindros_cones_e_esferas.py
Cilindro: área lateral 2πrh, área total, volume πr²h; cone: geratriz g² = h² + r², área lateral πrg, volume πr²h ÷ 3;
esfera: área 4πr², volume 4πr³ ÷ 3; problemas (latas, casquinhas, caixas-d’água, bolas). Respostas com π ou com π = 3,14.
Usa geradores do 9º ano (volume do cilindro) com outro sorteio.
Erros: usar o diâmetro como raio, esquecer o ÷ 3 no cone, usar a altura no lugar da geratriz na área lateral do cone.
"""
import random
from fractions import Fraction as F
from br_em import M, d, bank, mix, lesson, use, unit, num

R = random.Random(92009)
v_cil = use("gen_br_matematica_9_volume_de_prismas_e_cilindros", 92908, "s3_cil")


def pi(v, un):
    v = F(v)
    if v == 1:
        return ("π " + un).strip()
    if v.denominator != 1:
        return ("%sπ/%d %s" % (num(v.numerator), v.denominator, un)).strip()
    return ("%sπ %s" % (d(v), un)).strip()


def s1_cilindro():
    r, h = R.randint(1, 10), R.randint(2, 15)
    k = R.choice(["lat", "tot", "vol"])
    if k == "lat":
        return M("Qual é a área lateral de um cilindro de raio %d cm e altura %d cm?" % (r, h), pi(2 * r * h, "cm²"), [pi(r * h, "cm²"), pi(r * r * h, "cm²"), pi(2 * r * h + 2 * r * r, "cm²")], "2πrh = 2π · %d · %d = <b>%s</b>." % (r, h, pi(2 * r * h, "cm²")))
    if k == "tot":
        return M("Qual é a área total de um cilindro de raio %d cm e altura %d cm?" % (r, h), pi(2 * r * h + 2 * r * r, "cm²"), [pi(2 * r * h, "cm²"), pi(2 * r * h + r * r, "cm²"), pi(r * r * h, "cm²")], "2πrh + 2πr² = %s + %s = <b>%s</b>." % (pi(2 * r * h, ""), pi(2 * r * r, ""), pi(2 * r * h + 2 * r * r, "cm²")))
    return M("Qual é o volume de um cilindro de raio %d cm e altura %d cm?" % (r, h), pi(r * r * h, "cm³"), [pi(2 * r * h, "cm³"), pi(r * h, "cm³"), pi(F(r * r * h, 3), "cm³")], "πr²h = π · %d · %d = <b>%s</b>." % (r * r, h, pi(r * r * h, "cm³")))


def s2_cone():
    r, h, g = R.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 6, 10), (9, 12, 15), (8, 15, 17), (12, 5, 13), (4, 3, 5)])
    k = R.choice(["g", "lat", "tot", "vol", "vol"])
    if k == "g":
        return M("Um cone tem raio %d cm e altura %d cm. Quanto mede a geratriz?" % (r, h), "%d cm" % g, ["%d cm" % (r + h), "%d cm" % (h - r) if h > r else "%d cm" % (r - h + 10), "%d cm" % (2 * r)], "g² = %d² + %d² = %d ⇒ <b>%d cm</b>." % (h, r, g * g, g))
    if k == "lat":
        return M("Um cone tem raio %d cm e geratriz %d cm. Qual é a área lateral?" % (r, g), pi(r * g, "cm²"), [pi(r * h, "cm²"), pi(2 * r * g, "cm²"), pi(r * g + r * r, "cm²")], "πrg = π · %d · %d = <b>%s</b>." % (r, g, pi(r * g, "cm²")))
    if k == "tot":
        return M("Um cone tem raio %d cm e geratriz %d cm. Qual é a área total?" % (r, g), pi(r * g + r * r, "cm²"), [pi(r * g, "cm²"), pi(2 * r * g + r * r, "cm²"), pi(r * g + 2 * r * r, "cm²")], "πrg + πr² = <b>%s</b>." % pi(r * g + r * r, "cm²"))
    return M("Um cone tem raio %d cm e altura %d cm. Qual é o volume?" % (r, h), pi(F(r * r * h, 3), "cm³"), [pi(r * r * h, "cm³"), pi(F(r * r * g, 3), "cm³"), pi(F(r * h, 3), "cm³")], "πr²h ÷ 3 = π · %d · %d ÷ 3 = <b>%s</b>." % (r * r, h, pi(F(r * r * h, 3), "cm³")))


def s3_esfera():
    r = R.randint(1, 12)
    k = R.choice(["area", "vol", "vol", "diam"])
    if k == "area":
        return M("Qual é a área da superfície de uma esfera de raio %d cm?" % r, pi(4 * r * r, "cm²"), [pi(r * r, "cm²"), pi(2 * r * r, "cm²"), pi(F(4 * r ** 3, 3), "cm²"), pi(4 * r, "cm²"), pi(8 * r * r, "cm²")], "4πr² = 4π · %d = <b>%s</b>." % (r * r, pi(4 * r * r, "cm²")))
    if k == "vol":
        return M("Qual é o volume de uma esfera de raio %d cm?" % r, pi(F(4 * r ** 3, 3), "cm³"), [pi(4 * r * r, "cm³"), pi(r ** 3, "cm³"), pi(F(4 * r * r, 3), "cm³"), pi(2 * r ** 3, "cm³"), pi(4 * r ** 3, "cm³")], "4πr³ ÷ 3 = 4π · %d ÷ 3 = <b>%s</b>." % (r ** 3, pi(F(4 * r ** 3, 3), "cm³")))
    D = 2 * r
    return M("Uma bola tem %d cm de diâmetro. Qual é a área da sua superfície?" % D, pi(4 * r * r, "cm²"), [pi(4 * D * D, "cm²"), pi(r * r, "cm²"), pi(D * D, "cm²") if D * D != 4 * r * r else pi(2 * D, "cm²")], "Raio = %d; 4π · %d² = <b>%s</b>." % (r, r, pi(4 * r * r, "cm²")))


def s4_problemas():
    P = F(314, 100)
    k = R.choice(["lata", "casquinha", "caixa", "bolas", "derreter"])
    if k == "lata":
        r, h = R.choice([(3, 10), (4, 12), (5, 10), (3, 12), (4, 10), (5, 12), (2, 10), (6, 10)])
        V = P * r * r * h
        return M("Uma lata cilíndrica tem %d cm de raio e %d cm de altura. Quantos mililitros cabem nela, aproximadamente? (π = 3,14)" % (r, h), "%s mL" % d(V), ["%s mL" % d(2 * P * r * h), "%s mL" % d(P * r * h), "%s mL" % d(V / 3)], "3,14 · %d · %d = %s cm³ = <b>%s mL</b>." % (r * r, h, d(V), d(V)))
    if k == "casquinha":
        r, h = R.choice([(3, 9), (3, 10), (2, 12), (4, 9), (3, 12), (2, 9), (4, 12), (5, 12)])
        V = P * r * r * h / 3
        return M("Uma casquinha de sorvete é um cone de raio %d cm e altura %d cm. Qual é o volume da casquinha? (π = 3,14)" % (r, h), "%s cm³" % d(V, 2), ["%s cm³" % d(V * 3, 2), "%s cm³" % d(P * r * h, 2), "%s cm³" % d(V / 2, 2)], "3,14 · %d · %d ÷ 3 = <b>%s cm³</b>." % (r * r, h, d(V, 2)))
    if k == "caixa":
        r, h = R.choice([(1, 1), (1, 2), (2, 1), (1, 3)])
        V = P * r * r * h
        return M("Uma caixa-d’água cilíndrica tem %d m de raio e %d m de altura. Qual é a capacidade em litros? (π = 3,14)" % (r, h), "%s L" % d(V * 1000), ["%s L" % d(V * 100), "%s L" % d(V), "%s L" % d(2 * P * r * h * 1000)], "%s m³ = <b>%s L</b> (1 m³ = 1.000 L)." % (d(V), d(V * 1000)))
    if k == "bolas":
        r = R.choice([2, 3, 4])
        return M("Três bolas de raio %d cm cabem exatamente num cilindro (raio %d cm, altura %d cm). Qual é o volume vazio dentro do cilindro? (Deixe com π.)" % (r, r, 6 * r), pi(6 * r ** 3 - 4 * r ** 3, "cm³"), [pi(6 * r ** 3, "cm³"), pi(4 * r ** 3, "cm³"), pi(6 * r ** 3 - F(4 * r ** 3, 3), "cm³")],
                 "Cilindro: π · %d · %d = %s; bolas: 3 · 4π · %d ÷ 3 = %s; vazio = <b>%s</b>." % (r * r, 6 * r, pi(6 * r ** 3, ""), r ** 3, pi(4 * r ** 3, ""), pi(2 * r ** 3, "cm³")))
    r = R.choice([3, 6, 9, 12])
    return M("Uma esfera de metal de raio %d cm é derretida e moldada num cilindro de raio %d cm. Qual é a altura do cilindro?" % (r, r), "%s cm" % d(F(4 * r, 3)), ["%d cm" % (4 * r), "%d cm" % (2 * r), "%d cm" % r], "πr²h = 4πr³ ÷ 3 ⇒ h = 4r ÷ 3 = <b>%s cm</b>." % d(F(4 * r, 3)))


def main():
    seen = set()
    sets = [
        ("Cilindro", mix(R, seen, [(s1_cilindro, 14), (v_cil, 6)])),
        ("Cone", mix(R, seen, [(s2_cone, 20)])),
        ("Esfera", mix(R, seen, [(s3_esfera, 20)])),
        ("Problemas com corpos redondos", mix(R, seen, [(s4_problemas, 20)])),
        ("Revisão", mix(R, seen, [(s1_cilindro, 7), (s2_cone, 7), (s3_esfera, 6)])),
    ]
    body = lesson(
        ["<b>Cilindro</b>: área lateral 2πrh (um retângulo enrolado); área total 2πrh + 2πr²; volume πr²h.",
         "<b>Cone</b>: geratriz g² = h² + r²; área lateral πrg; área total πrg + πr²; volume πr²h ÷ 3.",
         "<b>Esfera</b>: área 4πr²; volume 4πr³ ÷ 3.",
         "Capacidade: 1 cm³ = 1 mL e 1 m³ = 1.000 L."],
        [("Cone com r = 3 e h = 4", ["g = √(16 + 9) = 5", "Al = π · 3 · 5", "V = π · 9 · 4 ÷ 3"], "Al = 15π cm², V = 12π cm³"),
         ("Esfera de raio 3 cm", ["4π · 27 ÷ 3"], "36π cm³")],
        [["Usar o diâmetro como raio", "Divida o diâmetro por 2."],
         ["Esquecer o ÷ 3 no cone", "O cone é 1/3 do cilindro de mesma base e altura."],
         ["Usar a altura na área do cone", "A área lateral usa a geratriz g."]])
    faq = [("Qual é a fórmula do volume da esfera?", "V = 4πr³ ÷ 3. Para r = 3 cm, V = 4π · 27 ÷ 3 = 36π cm³ ≈ 113 cm³."),
           ("O que a BNCC pede?", "Resolver e elaborar problemas que envolvem o cálculo de áreas totais e de volumes de prismas, pirâmides e corpos redondos em situações reais (EM13MAT309).")]
    unit(R, "cilindros-cones-e-esferas", "M", ["EM13MAT309"],
         "Resolver e elaborar problemas que envolvem o cálculo de áreas totais e de volumes de prismas, pirâmides e corpos redondos em situações reais (como o cálculo do gasto de material para revestimento ou pinturas de objetos cujos formatos sejam composições dos sólidos estudados), com ou sem apoio de tecnologias digitais",
         "Cilindros, cones e esferas: áreas e volumes", "Cilindros, cones e esferas",
         "Atividades de matemática para a 2ª série do Ensino Médio sobre corpos redondos: área e volume do cilindro, geratriz, área e volume do cone, área e volume da esfera e problemas. 100 exercícios com gabarito.",
         "Esfera: V = 4πr³ ÷ 3", "Cone: V = πr²h ÷ 3; g² = h² + r².",
         body, faq, sets, 9, grade="2-serie")


if __name__ == "__main__":
    main()
