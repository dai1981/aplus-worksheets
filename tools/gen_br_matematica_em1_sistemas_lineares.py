# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio 1ª série: Sistemas de equações lineares (EM13MAT301)
  python3 tools/gen_br_matematica_em1_sistemas_lineares.py
Sistemas 2 × 2 (adição, substituição, gráfico), classificação (possível e determinado, possível e indeterminado, impossível),
sistemas 3 × 3 por escalonamento simples, problemas (ingressos, misturas, idades, compras).
Usa geradores do 8º ano (adição, gráfico, problemas) com outro sorteio.
Erros: somar as equações sem igualar coeficientes, achar que retas paralelas têm solução, parar depois de achar só uma incógnita.
"""
import random
from fractions import Fraction as F
from br_em import M, d, fq, par, expr, bank, mix, lesson, use, unit, R2, num

R = random.Random(91013)
s_adic, s_graf, s_prob = use("gen_br_matematica_8_sistemas_de_equacoes", 91906, "s3_adicao", "s4_grafico", "s5_problemas")


def sys_(rows):
    return "<span class='sys'>%s</span>" % "<br>".join(rows)


def eq(cs, vs, rhs):
    return "%s = %s" % (expr(list(zip(cs, vs))), d(rhs))


def s1_classif():
    a, b = R.choice([(1, 2), (2, 1), (1, -1), (3, 1), (2, 3), (1, 3)])
    c = R.randint(-6, 8)
    k = R.choice(["spd", "spi", "si"])
    m = R.choice([2, 3, -1])
    if k == "spd":
        e2 = (a + R.choice([1, 2]), b - R.choice([1, 2, 3]))
        if e2[0] * b == e2[1] * a:
            return None
        rows = [eq([a, b], ["x", "y"], c), eq(list(e2), ["x", "y"], R.randint(-5, 9))]
        ans = "possível e determinado (uma solução)"
        exp = "Os coeficientes não são proporcionais: as retas se cortam num ponto."
    elif k == "spi":
        rows = [eq([a, b], ["x", "y"], c), eq([m * a, m * b], ["x", "y"], m * c)]
        ans = "possível e indeterminado (infinitas soluções)"
        exp = "A 2ª equação é a 1ª multiplicada por %s: as retas coincidem." % d(m)
    else:
        rows = [eq([a, b], ["x", "y"], c), eq([m * a, m * b], ["x", "y"], m * c + R.choice([1, 2, 3]))]
        ans = "impossível (nenhuma solução)"
        exp = "Os coeficientes são proporcionais, mas os termos independentes não: as retas são paralelas."
    opts = ["possível e determinado (uma solução)", "possível e indeterminado (infinitas soluções)", "impossível (nenhuma solução)", "possível e determinado com x = y = 0"]
    return M(sys_(rows) + "<br>Como se classifica esse sistema?", ans, [o for o in opts if o != ans], exp + " Resposta: <b>%s</b>." % ans)


def s2_resolver():
    x, y = R.randint(-4, 6), R.randint(-4, 6)
    while True:
        a1, b1, a2, b2 = [R.choice([x_ for x_ in range(-4, 6) if x_]) for _ in range(4)]
        if a1 * b2 - a2 * b1 != 0:
            break
    c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
    rows = [eq([a1, b1], ["x", "y"], c1), eq([a2, b2], ["x", "y"], c2)]
    k = R.choice(["par", "soma"])
    if k == "par":
        return M(sys_(rows) + "<br>Qual é a solução do sistema?", "(%s, %s)" % (d(x), d(y)), ["(%s, %s)" % (d(y), d(x)) if x != y else "(%s, %s)" % (d(x), d(y + 1)), "(%s, %s)" % (d(-x), d(y)) if x else "(1, %s)" % d(y), "(%s, %s)" % (d(x), d(-y)) if y else "(%s, 1)" % d(x)],
                     "Resolvendo (por adição ou substituição): x = %s e y = %s. Confira nas duas equações. <b>(%s, %s)</b>." % (d(x), d(y), d(x), d(y)))
    return M(sys_(rows) + "<br>Quanto vale x + y?", d(x + y), [d(x - y), d(x * y), d(x + y + 1)], "Solução: x = %s e y = %s; x + y = <b>%s</b>." % (d(x), d(y), d(x + y)))


def s3_tres():
    x, y, z = R.randint(-3, 5), R.randint(-3, 5), R.randint(-3, 5)
    k = R.choice(["escada", "soma"])
    if k == "escada":
        a, b = R.choice([1, 2, -1]), R.choice([1, 2, 3, -1])
        c = R.choice([1, 2, -2])
        rows = ["x + %s = %s" % (expr([(a, "y"), (b, "z")]), d(x + a * y + b * z)), "%s = %s" % (expr([(1, "y"), (c, "z")]), d(y + c * z)), "z = %s" % d(z)]
        rows[0] = rows[0].replace("x + −", "x − ")
        return M(sys_(rows) + "<br>Qual é a solução (x, y, z)?", "(%s, %s, %s)" % (d(x), d(y), d(z)), ["(%s, %s, %s)" % (d(z), d(y), d(x)) if x != z else "(%s, %s, %s)" % (d(x + 1), d(y), d(z)), "(%s, %s, %s)" % (d(x), d(y + c * z), d(z)) if c * z else "(%s, %s, %s)" % (d(x), d(y - 1), d(z)), "(%s, %s, %s)" % (d(-x), d(y), d(z)) if x else "(1, %s, %s)" % (d(y), d(z))],
                 "Já temos z = %s. Na 2ª: y = %s. Na 1ª: x = %s. <b>(%s, %s, %s)</b>." % (d(z), d(y), d(x), d(x), d(y), d(z)))
    rows = ["x + y + z = %s" % d(x + y + z), "x − y = %s" % d(x - y), "y + z = %s" % d(y + z)]
    return M(sys_(rows) + "<br>Qual é o valor de x?", d(x), [d(y), d(z), d(x + y + z)], "Da 1ª e da 3ª: x = (x + y + z) − (y + z) = %s − %s = <b>%s</b>." % (d(x + y + z), par(y + z), d(x)))


def s4_prob():
    k = R.choice(["ingressos", "moedas", "lanche", "idades", "tres"])
    if k == "ingressos":
        pi, pm = R.choice([(40, 20), (30, 15), (50, 25), (60, 30)])
        i, m = R.randint(20, 80), R.randint(10, 60)
        return M("Um show vendeu %d ingressos, inteiras a R$ %d e meias a R$ %d, arrecadando R$ %s. Quantas meias foram vendidas?" % (i + m, pi, pm, num(pi * i + pm * m)), str(m), [str(i), str((i + m) // 2), str(m + 5)],
                 "x + y = %d e %dx + %dy = %s ⇒ y = <b>%d</b>." % (i + m, pi, pm, num(pi * i + pm * m), m))
    if k == "moedas":
        a, b = R.randint(5, 30), R.randint(5, 30)
        return M("Um cofre tem %d moedas, só de R$ 0,50 e de R$ 1,00, num total de R$ %s. Quantas moedas de R$ 1,00 há?" % (a + b, d(F(a, 2) + b, 2, keep=True)), str(b), [str(a), str((a + b) // 2), str(b + 2)],
                 "x + y = %d e 0,5x + y = %s ⇒ <b>%d</b> moedas de R$ 1,00." % (a + b, d(F(a, 2) + b), b))
    if k == "lanche":
        s, r = R.choice([(8, 5), (10, 6), (12, 4), (9, 5), (7, 3)])
        a1, b1 = R.choice([(2, 3), (3, 1), (1, 2)])
        a2, b2 = R.choice([(1, 4), (2, 1), (4, 1)])
        if a1 * b2 == a2 * b1:
            return None
        return M("%d sanduíches e %d sucos custam R$ %d; %d %s e %d sucos custam R$ %d. Quanto custa um suco?" % (a1, b1, a1 * s + b1 * r, a2, "sanduíche" if a2 == 1 else "sanduíches", b2, a2 * s + b2 * r) if b1 > 1 and b2 > 1 else
                 "%d %s e %d %s custam R$ %d; %d %s e %d %s custam R$ %d. Quanto custa um suco?" % (a1, "sanduíche" if a1 == 1 else "sanduíches", b1, "suco" if b1 == 1 else "sucos", a1 * s + b1 * r, a2, "sanduíche" if a2 == 1 else "sanduíches", b2, "suco" if b2 == 1 else "sucos", a2 * s + b2 * r),
                 R2(r), [R2(s), R2(s + r), R2(abs(s - r))], "Resolvendo o sistema: sanduíche R$ %d e suco <b>%s</b>." % (s, R2(r)))
    if k == "idades":
        a, b = R.randint(20, 45), R.randint(5, 18)
        return M("A soma das idades de mãe e filho é %d anos, e a diferença é %d anos. Quantos anos tem o filho?" % (a + b, a - b), str(b), [str(a), str((a + b) // 2), str(a - b)], "x + y = %d e x − y = %d ⇒ x = %d, <b>y = %d</b>." % (a + b, a - b, a, b))
    p1, p2, p3 = R.randint(2, 6), R.randint(3, 8), R.randint(4, 10)
    return M("Caneta, lápis e borracha: caneta + lápis = R$ %d; lápis + borracha = R$ %d; caneta + borracha = R$ %d. Quanto custa o lápis?" % (p3 + p1, p1 + p2, p3 + p2), R2(p1), [R2(p2), R2(p3), R2(F(p1 + p2 + p3, 3))],
             "Somando: 2(c + ℓ + b) = %d ⇒ c + ℓ + b = %d; ℓ = %d − %d = <b>%s</b>." % (2 * (p1 + p2 + p3), p1 + p2 + p3, p1 + p2 + p3, p2 + p3, R2(p1)))


def main():
    seen = set()
    sets = [
        ("Resolver sistemas 2 × 2", mix(R, seen, [(s2_resolver, 12), (s_adic, 8)])),
        ("Interpretação gráfica", mix(R, seen, [(s_graf, 20)])),
        ("Classificação", mix(R, seen, [(s1_classif, 20)])),
        ("Sistemas 3 × 3", mix(R, seen, [(s3_tres, 20)])),
        ("Problemas", mix(R, seen, [(s4_prob, 14), (s_prob, 6)])),
    ]
    body = lesson(
        ["Um <b>sistema linear</b> pede valores que satisfaçam todas as equações ao mesmo tempo.",
         "<b>Adição</b>: multiplique para igualar coeficientes de uma incógnita e some ou subtraia as equações. <b>Substituição</b>: isole uma incógnita e substitua na outra.",
         "Cada equação de 2 incógnitas é uma reta. Retas que se cortam: <b>uma solução</b> (SPD). Retas iguais: <b>infinitas</b> (SPI). Retas paralelas: <b>nenhuma</b> (SI).",
         "Sistemas 3 × 3: escalone (deixe em forma de escada) e resolva de baixo para cima."],
        [("x + y = 10 e x − y = 4", ["somando: 2x = 14"], "x = 7, y = 3"),
         ("2x + 4y = 6 e x + 2y = 5", ["1ª ÷ 2: x + 2y = 3, diferente de 5"], "impossível")],
        [["Somar sem igualar os coeficientes", "Prepare as equações para que uma incógnita desapareça."],
         ["Achar solução em retas paralelas", "Paralelas não se cruzam: sistema impossível."],
         ["Parar depois da 1ª incógnita", "Substitua para achar as outras."]])
    faq = [("Como saber se um sistema é impossível?", "Num sistema 2 × 2, se os coeficientes de x e y são proporcionais mas os termos independentes não, as retas são paralelas e não há solução."),
           ("O que a BNCC pede?", "Resolver e elaborar problemas do cotidiano, da Matemática e de outras áreas do conhecimento, que envolvem equações lineares simultâneas, usando técnicas algébricas e gráficas, com ou sem apoio de tecnologias digitais (EM13MAT301).")]
    unit(R, "sistemas-lineares", "A", ["EM13MAT301"],
         "Resolver e elaborar problemas do cotidiano, da Matemática e de outras áreas do conhecimento, que envolvem equações lineares simultâneas, usando técnicas algébricas e gráficas, com ou sem apoio de tecnologias digitais",
         "Sistemas de equações lineares", "Sistemas lineares",
         "Atividades de matemática para a 1ª série do Ensino Médio sobre sistemas lineares: método da adição e da substituição, interpretação gráfica, classificação (SPD, SPI, SI), sistemas 3 × 3 e problemas. 100 exercícios com gabarito.",
         "Retas que se cortam: uma solução", "Paralelas: nenhuma; coincidentes: infinitas.",
         body, faq, sets, 13, grade="1-serie")


if __name__ == "__main__":
    main()
