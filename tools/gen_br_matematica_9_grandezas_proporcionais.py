# -*- coding: utf-8 -*-
"""
Brasil Matemática 9º ano: Grandezas diretamente e inversamente proporcionais (Números, EF09MA08)
  python3 tools/gen_br_matematica_9_grandezas_proporcionais.py
Identificar proporção direta, inversa ou nenhuma; regra de três simples direta e inversa; divisão em partes diretamente
proporcionais; escalas e receitas; problemas de economia (câmbio, impostos simples).
Erros: usar regra de três direta quando é inversa, achar que toda grandeza que aumenta junto é proporcional (idade e altura).
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix, reais
from br_9 import M, d, unit

R = random.Random(89007)


def s1_tipo():
    q, a = R.choice([
        ("o número de pães comprados e o valor pago (mesmo preço por pão)", "diretamente proporcionais"),
        ("o número de pedreiros e o tempo para levantar o mesmo muro", "inversamente proporcionais"),
        ("a velocidade de um carro e o tempo para fazer o mesmo percurso", "inversamente proporcionais"),
        ("a quantidade de gasolina e a distância percorrida (mesmo consumo)", "diretamente proporcionais"),
        ("a idade e a altura de uma pessoa", "não são proporcionais"),
        ("o lado de um quadrado e o seu perímetro", "diretamente proporcionais"),
        ("o lado de um quadrado e a sua área", "não são proporcionais"),
        ("o número de torneiras iguais abertas e o tempo para encher um tanque", "inversamente proporcionais"),
        ("as horas trabalhadas e o salário de quem ganha por hora", "diretamente proporcionais"),
        ("o número de pessoas que dividem uma pizza e o tamanho de cada pedaço", "inversamente proporcionais"),
        ("a temperatura em °C e a temperatura em °F", "não são proporcionais"),
        ("a massa de farinha e o número de bolos da mesma receita", "diretamente proporcionais"),
        ("o número de máquinas iguais e o tempo para produzir 1.000 peças", "inversamente proporcionais"),
        ("o número de convidados e o tempo de duração da festa", "não são proporcionais"),
    ])
    return M("Como são as grandezas: %s?" % q, a, [x for x in ["diretamente proporcionais", "inversamente proporcionais", "não são proporcionais", "sempre iguais"] if x != a],
             "Resposta: <b>%s</b>." % a)


def s1_tabela():
    k = R.choice(["dir", "inv", "nada"])
    x = [1, 2, 3, 4, 6]
    xs = R.sample(x, 4)
    xs.sort()
    c = R.choice([12, 24, 36, 48, 60])
    if k == "dir":
        ys = [c // 12 * 3 * v for v in xs]
        ans = "diretamente proporcionais"
        why = "y ÷ x é sempre %d" % (c // 12 * 3)
    elif k == "inv":
        ys = [c // v for v in xs]
        ans = "inversamente proporcionais"
        why = "x · y é sempre %d" % c
    else:
        b = R.randint(2, 5)
        ys = [3 * v + b for v in xs]
        ans = "não são proporcionais"
        why = "nem y ÷ x nem x · y é constante"
    tb = "<table class='sn-table' style='width:auto'><tbody><tr><th>x</th>%s</tr><tr><th>y</th>%s</tr></tbody></table>" % ("".join("<td>%d</td>" % v for v in xs), "".join("<td>%d</td>" % v for v in ys))
    return M(tb + "As grandezas x e y da tabela são…", ans, [z for z in ["diretamente proporcionais", "inversamente proporcionais", "não são proporcionais"] if z != ans] + ["proporcionais só no começo"],
             "%s: <b>%s</b>." % (why[0].upper() + why[1:], ans))


def s2_direta():
    k = R.choice(["pao", "tinta", "receita", "km"])
    if k == "pao":
        n1, p = R.choice([4, 5, 6, 8]), R.choice([75, 80, 90, 120])
        n2 = R.choice([v for v in [10, 12, 15, 20, 24] if v != n1])
        return M("%d pães custam %s. Quanto custam %d pães iguais?" % (n1, reais(n1 * p), n2), reais(n2 * p), [reais(n1 * p + n2 - n1), reais(n1 * p * n2), reais(F(n1 * p * n1, n2))if (n1 * p * n1) % n2 == 0 else reais(n1 * p + 100)],
                 "Um pão custa %s; %d · %s = <b>%s</b>." % (reais(p), n2, reais(p), reais(n2 * p)))
    if k == "tinta":
        L, m2 = R.choice([(2, 18), (3, 24), (4, 30), (5, 40)])
        L2 = R.choice([v for v in [6, 8, 9, 10, 12] if v != L])
        y = F(m2 * L2, L)
        if y.denominator != 1:
            return None
        return M("Com %d litros de tinta pintam-se %d m² de parede. Quantos m² se pintam com %d litros?" % (L, m2, L2), "%s m²" % d(y), ["%s m²" % d(F(m2 * L, L2), 1), "%d m²" % (m2 + L2 - L), "%d m²" % (m2 * L2)],
                 "Regra de três direta: %d/%d = x/%d → x = <b>%s m²</b>." % (L, m2, L2, d(y)))
    if k == "receita":
        o, f, p2 = R.choice([(3, 240, 5), (2, 300, 3), (4, 500, 6), (3, 360, 4)])
        y = F(f * p2, o)
        return M("Uma receita usa %d ovos para %d g de farinha. Com %d ovos, quanto de farinha se usa?" % (o, f, p2), "%s g" % d(y), ["%s g" % d(F(f * o, p2), 1), "%d g" % (f + p2 - o), "%d g" % (f * p2)],
                 "%d ÷ %d = %s g por ovo; · %d = <b>%s g</b>." % (f, o, d(F(f, o), 1), p2, d(y)))
    km, L = R.choice([(120, 10), (150, 12), (90, 6), (210, 15)])
    km2 = R.choice([300, 360, 420, 480])
    y = F(L * km2, km)
    if y.denominator != 1:
        return None
    return M("Um carro gasta %d litros para %d km. Quantos litros gasta para %d km?" % (L, km, km2), "%s L" % d(y), ["%s L" % d(F(L * km, km2), 1), "%d L" % (L + 10), "%d L" % (km2 // 10)],
             "Direta: %d/%d = x/%d → x = <b>%s L</b>." % (L, km, km2, d(y)))


def s3_inversa():
    k = R.choice(["pedreiro", "vel", "torneira", "racao"])
    if k == "pedreiro":
        a, t = R.choice([(4, 12), (6, 10), (3, 20), (5, 12), (8, 9)])
        b = R.choice([v for v in [2, 3, 4, 6, 8, 10, 12] if v != a and (a * t) % v == 0])
        y = a * t // b
        return M("%d pedreiros levantam um muro em %d dias. Em quantos dias %d pedreiros, no mesmo ritmo, levantam o mesmo muro?" % (a, t, b), "%d dias" % y,
                 ["%s dias" % d(F(t * b, a), 1), "%d dias" % (t + a - b) if t + a - b > 0 else "%d dias" % (t + 1), "%d dias" % (a * t)],
                 "Inversa: %d · %d = %d · x → x = <b>%d dias</b>." % (a, t, b, y))
    if k == "vel":
        v, t = R.choice([(60, 4), (80, 3), (90, 2), (75, 4), (100, 3)])
        v2 = R.choice([w for w in [40, 50, 60, 80, 100, 120, 150] if w != v and (v * t * 10) % w == 0])
        y = F(v * t, v2)
        return M("A %d km/h, uma viagem dura %d horas. Quanto dura a %d km/h?" % (v, t, v2), "%s h" % d(y), ["%s h" % d(F(t * v2, v), 2), "%s h" % d(t + 1), "%d h" % (t * 2)],
                 "Inversa: %d · %d = %d · x → x = <b>%s h</b>." % (v, t, v2, d(y)))
    if k == "torneira":
        n, t = R.choice([(2, 6), (3, 8), (4, 9), (2, 12)])
        n2 = R.choice([w for w in [1, 3, 4, 6, 8] if w != n and (n * t) % w == 0])
        y = n * t // n2
        return M("%d torneiras iguais enchem um tanque em %d horas. Em quanto tempo %d %s enche%s o tanque?" % (n, t, n2, "torneira" if n2 == 1 else "torneiras", "" if n2 == 1 else "m"), "%d h" % y,
                 ["%s h" % d(F(t * n2, n), 1), "%d h" % (t + 1), "%d h" % (n * t + 1)], "Inversa: %d · %d = %d · x → x = <b>%d h</b>." % (n, t, n2, y))
    a, dias = R.choice([(10, 30), (12, 20), (15, 24), (8, 45)])
    b = R.choice([w for w in [5, 6, 12, 15, 18, 20, 24] if w != a and (a * dias) % w == 0])
    y = a * dias // b
    return M("Uma ração alimenta %d cavalos por %d dias. Para quantos dias dá se forem %d cavalos?" % (a, dias, b), "%d dias" % y, ["%s dias" % d(F(dias * b, a), 1), "%d dias" % (dias + a - b) if dias + a - b > 0 else "%d dias" % (dias + 2), "%d dias" % (a * dias)],
             "Inversa: %d · %d = %d · x → x = <b>%d dias</b>." % (a, dias, b, y))


def s4_partes():
    ps = R.choice([(2, 3), (1, 4), (3, 5), (2, 3, 5), (1, 2, 3), (3, 4), (2, 5)])
    tot = sum(ps) * R.choice([50, 100, 120, 150, 200, 300])
    u = tot // sum(ps)
    nm = R.sample(["Ana", "Bruno", "Caio", "Duda", "Elisa"], len(ps))
    i = R.randrange(len(ps))
    k = R.choice(["dinheiro", "premio"])
    what = "%s foram divididos entre %s em partes diretamente proporcionais a %s" % (reais(tot * 100), ", ".join(nm[:-1]) + " e " + nm[-1], ", ".join(map(str, ps[:-1])) + " e " + str(ps[-1]))
    if k == "premio":
        what = "Um prêmio de " + what[0].lower() + what[1:]
        what = what.replace("foram divididos", "foi dividido")
    return M("%s. Quanto recebe %s?" % (what[0].upper() + what[1:], nm[i]), reais(u * ps[i] * 100), [reais(tot * 100 // len(ps)) if tot % len(ps) == 0 else reais(tot * 50), reais(u * 100), reais(u * (sum(ps) - ps[i]) * 100), reais(u * (ps[i] + 1) * 100), reais(tot * ps[i] * 10)],
             "%s ÷ %d partes = %s por parte; %d · %s = <b>%s</b>." % (reais(tot * 100), sum(ps), reais(u * 100), ps[i], reais(u * 100), reais(u * ps[i] * 100)))


def s5_economia():
    k = R.choice(["cambio", "imposto", "prestacao"])
    if k == "cambio":
        c = R.choice([F(5), F(11, 2), F(6), F(27, 5)])
        us = R.choice([20, 50, 80, 100, 150, 200])
        y = c * us
        return M("Suponha que 1 dólar custe %s. Quantos reais são necessários para comprar %d dólares?" % (reais(int(c * 100)), us), reais(int(y * 100)), [reais(int(F(us * 100) / c)) if (F(us) / c * 100).denominator == 1 else reais(us * 100), reais(int((c + us) * 100)), reais(int(y * 10))],
                 "Direta: %d · %s = <b>%s</b>." % (us, reais(int(c * 100)), reais(int(y * 100))))
    if k == "imposto":
        p, t = R.choice([(200, 10), (500, 8), (300, 15), (800, 5), (1200, 6)])
        y = F(p * t, 100)
        return M("Uma taxa é proporcional ao valor: %d%% do preço. Qual é a taxa sobre uma compra de %s?" % (t, reais(p * 100)), reais(int(y * 100)), [reais(t * 100), reais(int(y * 1000)), reais(int((p - y) * 100))],
                 "%d%% de %d = %s · %d = <b>%s</b>." % (t, p, d(F(t, 100)), p, reais(int(y * 100))))
    n, v = R.choice([(10, 120), (12, 85), (8, 150), (6, 230)])
    n2 = R.choice([w for w in [4, 5, 15, 20, 24] if (n * v) % w == 0])
    y = n * v // n2
    return M("Uma compra foi dividida em %d parcelas iguais de %s. Se fosse dividida em %d parcelas iguais (sem juros), qual seria cada parcela?" % (n, reais(v * 100), n2), reais(y * 100),
             [reais(v * n2 // n * 100) if (v * n2) % n == 0 else reais((v + 10) * 100), reais(n * v * 100), reais((v + n - n2) * 100)], "Total %s; ÷ %d = <b>%s</b> (inversa)." % (reais(n * v * 100), n2, reais(y * 100)))


def main():
    seen = set()
    sets = [
        ("Direta, inversa ou nenhuma?", mix(R, seen, [(s1_tipo, 10), (s1_tabela, 10)])),
        ("Regra de três direta", mix(R, seen, [(s2_direta, 20)])),
        ("Regra de três inversa", mix(R, seen, [(s3_inversa, 20)])),
        ("Divisão em partes proporcionais", mix(R, seen, [(s4_partes, 20)])),
        ("Problemas de economia", mix(R, seen, [(s5_economia, 12), (s2_direta, 4), (s3_inversa, 4)])),
    ]
    body = lesson(
        ["Duas grandezas são <b>diretamente proporcionais</b> quando, se uma dobra, a outra também dobra: y ÷ x é constante.",
         "São <b>inversamente proporcionais</b> quando, se uma dobra, a outra fica pela metade: x · y é constante.",
         "Na regra de três direta, multiplique em cruz. Na inversa, o produto x · y fica igual: 4 pedreiros · 12 dias = 6 pedreiros · x.",
         "Para dividir em partes proporcionais a 2 e 3, divida o total por 2 + 3 = 5 e multiplique cada parte."],
        [("4 pedreiros, 12 dias; 6 pedreiros?", ["4 · 12 = 6 · x", "48 = 6x"], "8 dias"),
         ("R$ 500,00 em partes 2 e 3", ["500 ÷ 5 = 100"], "R$ 200,00 e R$ 300,00")],
        [["Usar a regra direta quando é inversa", "Pergunte: se uma aumenta, a outra aumenta ou diminui?"],
         ["Achar que tudo que cresce junto é proporcional", "Idade e altura crescem juntas, mas não são proporcionais."],
         ["Dividir pelo número de pessoas, não de partes", "Some as partes: 2 + 3 = 5."]])
    faq = [("Como saber se a proporção é direta ou inversa?", "Pense no que acontece quando uma grandeza dobra. Se a outra também dobra, é direta; se cai pela metade, é inversa. Se não acontece nenhum dos dois, as grandezas não são proporcionais."),
           ("O que a BNCC pede no 9º ano?", "Resolver e elaborar problemas com grandezas diretamente e inversamente proporcionais, incluindo divisão em partes proporcionais e situações de economia.")]
    unit(R, "grandezas-proporcionais", "N", ["EF09MA08"],
         "Resolver e elaborar problemas que envolvam relações de proporcionalidade direta e inversa entre duas ou mais grandezas, inclusive escalas, divisão em partes proporcionais e taxa de variação, em contextos socioculturais, ambientais e de outras áreas",
         "Grandezas diretamente e inversamente proporcionais", "Grandezas proporcionais",
         "Atividades de matemática para o 9º ano sobre grandezas diretamente e inversamente proporcionais: regra de três direta e inversa, divisão em partes proporcionais e problemas de economia. 100 exercícios com gabarito.",
         "Direta: y ÷ x fica igual. Inversa: x · y fica igual.", "Se uma dobra e a outra dobra, é direta; se cai pela metade, é inversa.",
         body, faq, sets, 7)


if __name__ == "__main__":
    main()
