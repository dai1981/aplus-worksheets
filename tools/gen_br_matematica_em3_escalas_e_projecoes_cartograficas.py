# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 3ª série: Escalas e projeções cartográficas (EM13MAT509)
  python3 tools/gen_br_matematica_em3_escalas_e_projecoes_cartograficas.py
Escala numérica (1 : 50.000) e conversões; áreas no mapa (escala ao quadrado); comprimento de um paralelo
(2πR · cos da latitude); projeções cilíndrica (Mercator), cônica e azimutal: o que cada uma conserva e o que deforma.
Erros: esquecer de converter cm em km, usar a escala sem elevar ao quadrado nas áreas, achar que o mapa de Mercator mostra áreas corretas.
"""
import random
import math
from fractions import Fraction as F
from br_em import M, d, bank, mix, lesson, unit, num

R = random.Random(93010)
ESC = [10000, 20000, 25000, 50000, 100000, 200000, 250000, 500000, 1000000, 5000000]


def s1_escala():
    e = R.choice(ESC)
    k = R.choice(["real", "mapa", "qual"])
    if k == "real":
        c = R.choice([2, 3, 4, 5, F(5, 2), 6, 8, 12])
        real_cm = c * e
        km = real_cm / 100000
        return M("Num mapa de escala 1 : %s, dois pontos estão a %s cm. Qual é a distância real?" % (num(e), d(c)), "%s km" % d(km), ["%s km" % d(km * 10), "%s km" % d(km / 10), "%s m" % d(km)],
                 "%s × %s = %s cm = <b>%s km</b>." % (d(c), num(e), num(real_cm) if F(real_cm).denominator == 1 else d(real_cm), d(km)))
    if k == "mapa":
        km = R.choice([1, 2, 5, 10, 20, 50, 100])
        c = F(km * 100000, e)
        if (c * 10).denominator != 1 or c > 50 or c < F(1, 2):
            return None
        return M("Num mapa de escala 1 : %s, quantos centímetros representam %s km reais?" % (num(e), d(km)), "%s cm" % d(c), ["%s cm" % d(c * 10), "%s cm" % d(c / 10), "%s cm" % d(km)],
                 "%s km = %s cm; ÷ %s = <b>%s cm</b>." % (d(km), num(km * 100000), num(e), d(c)))
    c = R.choice([2, 4, 5, 8, 10])
    km = R.choice([1, 2, 5, 10, 20, 40, 100])
    esc = F(km * 100000, c)
    if esc.denominator != 1:
        return None
    return M("Num mapa, %d cm correspondem a %d km. Qual é a escala?" % (c, km), "1 : %s" % num(esc), ["1 : %s" % num(esc / 100), "1 : %s" % num(esc * 10), "1 : %s" % num(F(km, c))], "%d km = %s cm; %s ÷ %d = <b>1 : %s</b>." % (km, num(km * 100000), num(km * 100000), c, num(esc)))


def s2_area():
    e = R.choice([500, 1000, 2000, 5000, 10000, 20000, 25000, 50000, 100000])
    k = R.choice(["mapa2real", "mapa2real", "ampliar"])
    if k == "mapa2real":
        a = R.choice([1, 2, 4, 5, 10])
        real_m2 = a * (e // 100) ** 2
        km2 = F(real_m2) / 10 ** 6
        txt = ("%s m²" % num(real_m2)) if real_m2 < 10 ** 6 else ("%s km²" % d(km2))
        wrong = ("%s m²" % num(a * e // 100)) if a * e // 100 < 10 ** 6 else "%s km²" % d(F(a * e, 100) / 10 ** 6)
        return M("Num mapa de escala 1 : %s, um terreno ocupa %d cm². Qual é a área real?" % (num(e), a), txt, [wrong, ("%s m²" % num(real_m2 * 100)) if real_m2 * 100 < 10 ** 6 else "%s km²" % d(km2 * 100), ("%s m²" % num(real_m2 // 100)) if real_m2 // 100 else "1 m²"],
                 "1 cm = %s m, então 1 cm² = %s m²; × %d = <b>%s</b>." % (num(e // 100), num((e // 100) ** 2), a, txt))
    f = R.choice([2, 3, 4, 10])
    return M("Se a escala de um mapa é aumentada %d vezes (o mapa fica %d vezes maior em cada direção), a área desenhada de um país fica…" % (f, f), "%d vezes maior" % (f * f), ["%d vezes maior" % f, "%d vezes maior" % (2 * f) if 2 * f != f * f else "%d vezes maior" % (f ** 3), "igual"], "Áreas mudam com o quadrado da escala: <b>%d vezes</b>." % (f * f))


def s3_paralelo():
    lat = R.choice([0, 30, 45, 60, 90])
    Rt = 6400
    c = {0: "1", 30: "√3/2", 45: "√2/2", 60: "1/2", 90: "0"}[lat]
    k = R.choice(["frac", "km"])
    if k == "frac" or lat in (30, 45):
        ans = {0: "igual ao Equador", 30: "cerca de 87% do Equador", 45: "cerca de 71% do Equador", 60: "metade do Equador", 90: "zero (é um ponto, o polo)"}[lat]
        return M("O comprimento de um paralelo é o comprimento do Equador × cos(latitude). O paralelo de %d° tem comprimento…" % lat, ans, [x for x in ("igual ao Equador", "metade do Equador", "cerca de 87% do Equador", "zero (é um ponto, o polo)", "o dobro do Equador") if x != ans][:3],
                 "cos %d° = %s: <b>%s</b>." % (lat, c, ans))
    eq = F(2 * 314 * Rt, 100)
    v = eq * {0: 1, 60: F(1, 2), 90: 0}[lat]
    return M("Usando raio da Terra 6.400 km e π = 3,14, qual é o comprimento aproximado do paralelo de latitude %d°? (cos %d° = %s)" % (lat, lat, c), "%s km" % d(v), ["%s km" % d(eq), "%s km" % d(eq / 4), "%s km" % d(v + 1000)] if lat else ["%s km" % d(eq / 2), "%s km" % d(eq * 2), "%s km" % d(F(314 * Rt, 100))],
             "2 · 3,14 · 6.400 · %s = <b>%s km</b>." % (c, d(v)))


s4_projecoes = bank(R, [
    ("Na projeção de Mercator (cilíndrica), as regiões perto dos polos aparecem…", "muito maiores do que são", ["menores do que são", "com a área correta", "invisíveis"]),
    ("No mapa de Mercator, a Groenlândia parece do tamanho da África, mas na verdade é…", "cerca de 14 vezes menor", ["do mesmo tamanho", "maior", "2 vezes maior"]),
    ("A projeção de Mercator conserva…", "os ângulos (formas locais), útil para navegação", ["as áreas", "as distâncias em todo o mapa", "nada"]),
    ("Uma projeção que conserva as áreas, mas deforma as formas, é chamada…", "equivalente", ["conforme", "azimutal", "plana"]),
    ("Uma projeção que conserva os ângulos é chamada…", "conforme", ["equivalente", "equidistante", "afilática"]),
    ("A projeção azimutal (plana) é feita num plano tangente à esfera e é muito usada para…", "mapas das regiões polares", ["mapas do Equador", "plantas de casas", "gráficos de setores"]),
    ("Nenhum mapa plano representa a Terra sem deformações porque…", "a superfície de uma esfera não pode ser planificada sem esticar ou cortar", ["a Terra é plana", "faltam satélites", "os mapas são pequenos"]),
    ("Na projeção cônica, a deformação é menor…", "nas latitudes médias, perto do paralelo de contato", ["nos polos", "no Equador", "em todo o mapa igualmente"]),
    ("Numa escala 1 : 100.000, 1 cm no mapa corresponde a…", "1 km", ["100 m", "10 km", "100 km"]),
    ("Um mapa de escala 1 : 10.000 tem ___ detalhes que um de 1 : 1.000.000.", "mais", ["menos", "os mesmos", "nenhum"]),
], "s4_projecoes")


def main():
    seen = set()
    sets = [
        ("Escala: distância real", mix(R, seen, [(s1_escala, 20)])),
        ("Escala: no mapa e qual escala", mix(R, seen, [(s1_escala, 20)])),
        ("Áreas em mapas", mix(R, seen, [(s2_area, 20)])),
        ("Paralelos e deformações", mix(R, seen, [(s3_paralelo, 6), (s4_projecoes, 10), (s1_escala, 4)])),
        ("Revisão", mix(R, seen, [(s1_escala, 10), (s2_area, 10)])),
    ]
    body = lesson(
        ["<b>Escala</b> 1 : 50.000 significa que 1 cm no mapa vale 50.000 cm (500 m) no real. Lembre: 1 km = 100.000 cm.",
         "Para <b>áreas</b>, a escala entra ao quadrado: se 1 cm vale 500 m, 1 cm² vale 500² = 250.000 m².",
         "Os paralelos diminuem até os polos: comprimento = comprimento do Equador × cos(latitude).",
         "Toda <b>projeção</b> deforma algo. Mercator (cilíndrica, conforme) conserva ângulos e aumenta as áreas perto dos polos; projeções equivalentes conservam áreas; a azimutal é boa para os polos."],
        [("Escala 1 : 200.000, distância de 3,5 cm", ["3,5 × 200.000 = 700.000 cm"], "7 km"),
         ("Escala 1 : 10.000, terreno de 4 cm²", ["1 cm² = 100² m² = 10.000 m²"], "40.000 m²")],
        [["Esquecer de converter cm em km", "Divida por 100.000."],
         ["Usar a escala simples para áreas", "Eleve a escala ao quadrado."],
         ["Confiar nas áreas do mapa de Mercator", "Perto dos polos tudo parece maior."]])
    faq = [("Por que a Groenlândia parece tão grande nos mapas?", "Porque a projeção de Mercator estica as regiões perto dos polos para conservar os ângulos. Na realidade, a África é cerca de 14 vezes maior que a Groenlândia."),
           ("O que a BNCC pede?", "Investigar a deformação de ângulos e áreas provocada pelas diferentes projeções usadas em cartografia (como a cilíndrica e a cônica), com ou sem suporte de tecnologia digital (EM13MAT509).")]
    unit(R, "escalas-e-projecoes-cartograficas", "M", ["EM13MAT509"],
         "Investigar a deformação de ângulos e áreas provocada pelas diferentes projeções usadas em cartografia (como a cilíndrica e a cônica), com ou sem suporte de tecnologia digital",
         "Escalas e projeções cartográficas", "Escalas e projeções cartográficas",
         "Atividades de matemática para a 3ª série do Ensino Médio sobre cartografia: escala numérica, distâncias e áreas em mapas, comprimento dos paralelos e deformações das projeções de Mercator, cônica e azimutal. 100 exercícios com gabarito.",
         "Escala de áreas = escala ao quadrado", "Toda projeção plana deforma algo.",
         body, faq, sets, 10, grade="3-serie")


if __name__ == "__main__":
    main()
