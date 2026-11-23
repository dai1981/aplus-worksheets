# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 2ª série: Polígonos regulares e ladrilhamentos (EM13MAT505, EM13MAT506)
  python3 tools/gen_br_matematica_em2_poligonos_regulares_e_ladrilhamentos.py
Ângulos internos de polígonos regulares; quais polígonos regulares ladrilham o plano (ângulos que somam 360° num vértice);
combinações de polígonos num vértice; área do triângulo equilátero e do hexágono regular;
perímetro e área em função do lado (função linear e quadrática).
Usa geradores do 9º ano (ângulos de polígonos regulares) com outro sorteio.
Erros: achar que o pentágono regular ladrilha, achar que a área dobra quando o lado dobra, usar a fórmula do quadrado no hexágono.
"""
import random
from fractions import Fraction as F
from br_em import M, d, bank, mix, lesson, use, unit, curva, num

R = random.Random(92007)
p_ang, p_inv = use("gen_br_matematica_9_poligonos_regulares", 92905, "s1_angulos", "s2_inverso")
NOMES = {3: "triângulo equilátero", 4: "quadrado", 5: "pentágono regular", 6: "hexágono regular", 8: "octógono regular", 10: "decágono regular", 12: "dodecágono regular"}


def ai(n):
    return F(180 * (n - 2), n)


def s1_ladrilho():
    k = R.choice(["um", "um", "falta", "combo"])
    if k == "um":
        n = R.choice([3, 4, 5, 6, 8, 10, 12])
        ok = 360 % ai(n) == 0 if ai(n).denominator == 1 else False
        ans = "sim, %s cabem em cada vértice" % num(360 / ai(n)) if ok else "não, porque %s° não divide 360°" % d(ai(n))
        w = ["não, porque %s° não divide 360°" % d(ai(n)), "sim, porque todo polígono regular ladrilha", "sim, porque tem lados iguais"] if ok else ["sim, porque todo polígono regular ladrilha", "sim, porque tem lados iguais", "sim, %s cabem em cada vértice" % num(int(360 / ai(n)))]
        return M("É possível ladrilhar o plano usando só %ss iguais?" % NOMES[n] if n != 4 else "É possível ladrilhar o plano usando só quadrados iguais?", ans, w,
                 "Ângulo interno %s°; 360 ÷ %s = %s: <b>%s</b>." % (d(ai(n)), d(ai(n)), d(360 / ai(n), 2), "sim" if ok else "não"))
    if k == "falta":
        combos = [([8, 8], 4), ([12, 12], 3), ([6, 6], 6), ([3, 3, 3, 3], 6), ([4, 4, 4], 4), ([3, 3, 4], 4), ([3, 12], 12), ([4, 6], 12), ([3, 3, 6], 6), ([3, 4, 4], 6)]
        have, miss = R.choice(combos)
        s = sum(ai(n) for n in have)
        nomes = " e ".join(NOMES[n] for n in have) if len(set(have)) == len(have) else ", ".join(NOMES[n] for n in have)
        return M("Num vértice de um ladrilhamento já há: %s. Que polígono regular completa os 360°?" % nomes, NOMES[miss], [NOMES[x] for x in (3, 4, 5, 6, 8, 12) if x != miss][:4],
                 "Ângulos: %s = %s°; faltam %s°, o ângulo do <b>%s</b>." % (" + ".join(d(ai(n)) + "°" for n in have), d(s), d(360 - s), NOMES[miss]))
    ok_combos = [(3, 3, 3, 4, 4), (3, 3, 4, 3, 4), (3, 6, 3, 6), (4, 8, 8), (3, 12, 12), (4, 6, 12), (3, 3, 3, 3, 6)]
    bad = [(5, 5, 5), (4, 5, 6), (3, 3, 5), (4, 4, 5), (3, 8, 8)]
    if R.random() < 0.5:
        c = R.choice(ok_combos)
        return M("Os polígonos regulares %s podem se encontrar num mesmo vértice, sem sobrar espaço?" % ", ".join(NOMES[n] for n in c), "sim, os ângulos somam 360°", ["não, os ângulos somam mais de 360°", "não, os ângulos somam menos de 360°", "só se forem do mesmo tamanho de lado diferente"],
                 "%s = 360°: <b>sim</b>." % " + ".join(d(ai(n)) + "°" for n in c))
    c = R.choice(bad)
    s = sum(ai(n) for n in c)
    ans = "não, os ângulos somam %s°" % d(s)
    return M("Os polígonos regulares %s podem se encontrar num mesmo vértice, sem sobrar espaço?" % ", ".join(NOMES[n] for n in c), ans, ["sim, os ângulos somam 360°", "sim, porque são regulares", "não, os ângulos somam 180°"],
             "%s = %s° ≠ 360°: <b>não</b>." % (" + ".join(d(ai(n)) + "°" for n in c), d(s)))


def s2_area():
    k = R.choice(["tri", "hexa", "hexa_per"])
    l = R.randint(2, 12)
    if k == "tri":
        v = F(l * l, 4)
        return M("Qual é a área de um triângulo equilátero de lado %d cm?" % l, "%s√3 cm²" % d(v) if v != 1 else "√3 cm²", ["%s√3 cm²" % d(F(l * l, 2)), "%s cm²" % d(F(l * l, 2)), "%s√2 cm²" % d(v)],
                 "A = ℓ²√3 ÷ 4 = %d · √3 ÷ 4 = <b>%s√3 cm²</b>." % (l * l, d(v)))
    if k == "hexa":
        v = F(6 * l * l, 4)
        return M("Qual é a área de um hexágono regular de lado %d cm?" % l, "%s√3 cm²" % d(v), ["%s√3 cm²" % d(F(l * l, 4)), "%d cm²" % (6 * l * l), "%s√3 cm²" % d(6 * l * l)],
                 "6 triângulos equiláteros: 6 · %d²√3 ÷ 4 = <b>%s√3 cm²</b>." % (l, d(v)))
    return M("Um hexágono regular tem perímetro %d cm. Qual é a área?" % (6 * l), "%s√3 cm²" % d(F(6 * l * l, 4)), ["%s√3 cm²" % d(F(36 * l * l, 4)), "%s√3 cm²" % d(F(l * l, 4)), "%d cm²" % (6 * l * l)],
             "Lado = %d ÷ 6 = %d; A = 6 · %d²√3 ÷ 4 = <b>%s√3 cm²</b>." % (6 * l, l, l, d(F(6 * l * l, 4))))


def s3_funcao():
    k = R.choice(["perlei", "arealei", "dobra", "graf"])
    n = R.choice([3, 4, 5, 6, 8])
    if k == "perlei":
        return M("O perímetro P de um %s, em função do lado ℓ, é…" % NOMES[n], "P(ℓ) = %dℓ, uma função linear" % n, ["P(ℓ) = ℓ%s, uma função quadrática" % "²", "P(ℓ) = %d + ℓ, uma função afim não linear" % n, "P(ℓ) = %dℓ², uma função quadrática" % n],
                 "Há %d lados iguais: <b>P = %dℓ</b>, proporcional ao lado." % (n, n))
    if k == "arealei":
        lei = {4: "A(ℓ) = ℓ²", 3: "A(ℓ) = (√3/4)ℓ²", 6: "A(ℓ) = (3√3/2)ℓ²"}
        if n not in lei:
            return None
        return M("A área de um %s, em função do lado ℓ, é…" % NOMES[n], lei[n] + ", uma função quadrática", ["A(ℓ) = %dℓ, uma função linear" % n, "A(ℓ) = ℓ + %d, uma função afim" % n, "A(ℓ) = 2ℓ, uma função linear"],
                 "A área é proporcional ao quadrado do lado: <b>%s</b>." % lei[n])
    if k == "dobra":
        m = R.choice([2, 3, 4])
        q = R.choice(["per", "area"])
        if q == "per":
            return M("Se o lado de um %s é multiplicado por %d, o perímetro fica multiplicado por…" % (NOMES[n], m), str(m), [str(m * m), str(m + n), str(n)], "P = %dℓ é linear: <b>%d</b>." % (n, m))
        return M("Se o lado de um %s é multiplicado por %d, a área fica multiplicada por…" % (NOMES[n], m), str(m * m), [str(m), str(2 * m) if 2 * m != m * m else str(m ** 3), str(m * n)], "A área é proporcional a ℓ²: <b>%d</b>." % (m * m))
    g = curva([(lambda x: 4 * x, "P"), (lambda x: x * x, "A")], (0, 6, 1), (0, 24, 4), label="perímetro P e área A de um quadrado em função do lado ℓ")
    q = R.choice(["igual", "qual"])
    if q == "igual":
        return M(g + "O gráfico mostra P(ℓ) = 4ℓ e A(ℓ) = ℓ² para um quadrado. Para qual lado o perímetro e a área têm o mesmo valor numérico?", "ℓ = 4", ["ℓ = 2", "ℓ = 0 e ℓ = 2", "ℓ = 16"], "4ℓ = ℓ² ⇒ <b>ℓ = 4</b> (ℓ &gt; 0).")
    return M(g + "O gráfico mostra P(ℓ) = 4ℓ e A(ℓ) = ℓ² para um quadrado. Qual curva é uma parábola?", "a da área A", ["a do perímetro P", "as duas", "nenhuma"], "A(ℓ) = ℓ² é uma função quadrática: <b>a da área</b>.")


def main():
    seen = set()
    sets = [
        ("Ângulos de polígonos regulares", mix(R, seen, [(p_ang, 12), (p_inv, 8)])),
        ("Ladrilhamentos com um polígono", mix(R, seen, [(s1_ladrilho, 20)])),
        ("Áreas de polígonos regulares", mix(R, seen, [(s2_area, 20)])),
        ("Perímetro e área em função do lado", mix(R, seen, [(s3_funcao, 18), (s2_area, 2)])),
        ("Revisão", mix(R, seen, [(p_ang, 6), (s1_ladrilho, 6), (s2_area, 8)])),
    ]
    body = lesson(
        ["Ângulo interno de um polígono regular de n lados: 180° · (n − 2) ÷ n. Triângulo 60°, quadrado 90°, pentágono 108°, hexágono 120°, octógono 135°, dodecágono 150°.",
         "Polígonos <b>ladrilham o plano</b> quando os ângulos que se encontram num vértice somam exatamente 360°. Só três polígonos regulares ladrilham sozinhos: triângulo, quadrado e hexágono.",
         "Área do triângulo equilátero: ℓ²√3 ÷ 4. O hexágono regular é formado por 6 deles: 6ℓ²√3 ÷ 4.",
         "Em função do lado, o perímetro é uma função <b>linear</b> (P = nℓ) e a área, uma função <b>quadrática</b> (A = kℓ²)."],
        [("Octógonos e quadrados num vértice", ["135° + 135° + 90° = 360°"], "ladrilham juntos"),
         ("Hexágono regular de lado 4 cm", ["6 · 16√3 ÷ 4"], "24√3 cm²")],
        [["Achar que o pentágono regular ladrilha", "108° não divide 360°."],
         ["Área dobra quando o lado dobra", "A área fica 4 vezes maior."],
         ["Usar ℓ² no hexágono", "Divida em 6 triângulos equiláteros."]])
    faq = [("Quais polígonos regulares ladrilham o plano sozinhos?", "Só o triângulo equilátero (6 por vértice), o quadrado (4 por vértice) e o hexágono regular (3 por vértice), porque seus ângulos internos dividem 360°."),
           ("O que a BNCC pede?", "Resolver problemas sobre ladrilhamentos do plano, com ou sem apoio de aplicativos de geometria dinâmica, para conjecturar a respeito dos tipos ou composição de polígonos que podem ser utilizados (EM13MAT505), e representar graficamente a variação da área e do perímetro de um polígono regular quando os comprimentos de seus lados variam, analisando e classificando as funções envolvidas (EM13MAT506).")]
    unit(R, "poligonos-regulares-e-ladrilhamentos", "G", ["EM13MAT505", "EM13MAT506"],
         "Resolver problemas sobre ladrilhamentos do plano, com ou sem apoio de aplicativos de geometria dinâmica, para conjecturar a respeito dos tipos ou composição de polígonos que podem ser utilizados em ladrilhamento, generalizando padrões observados; representar graficamente a variação da área e do perímetro de um polígono regular quando os comprimentos de seus lados variam, analisando e classificando as funções envolvidas",
         "Polígonos regulares e ladrilhamentos", "Polígonos regulares e ladrilhamentos",
         "Atividades de matemática para a 2ª série do Ensino Médio sobre polígonos regulares: ângulos internos, ladrilhamentos do plano, área do triângulo equilátero e do hexágono, perímetro e área em função do lado. 100 exercícios com gabarito.",
         "Ladrilham: os ângulos somam 360°", "Só triângulo, quadrado e hexágono regulares ladrilham sozinhos.",
         body, faq, sets, 7, grade="2-serie")


if __name__ == "__main__":
    main()
