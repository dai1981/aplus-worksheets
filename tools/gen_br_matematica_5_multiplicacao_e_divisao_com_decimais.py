# -*- coding: utf-8 -*-
"""
Brasil Matemática 5º ano: Multiplicação e divisão com decimais (Números, EF05MA08)
  python3 tools/gen_br_matematica_5_multiplicacao_e_divisao_com_decimais.py
Multiplicar e dividir decimais por 10, 100 e 1.000 (a vírgula anda); decimal × número natural; decimal ÷ número natural;
divisão de naturais com quociente decimal (7 ÷ 2 = 3,5); dinheiro; problemas com medidas.
Erros: 2,5 × 4 = 8,20 (multiplicar as partes separadas), contar errado as casas decimais, andar a vírgula para o lado errado.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, dz, reais, armada, Kids

R = random.Random(80510)
K = Kids(R)


def s1_potencias():
    k = R.choice([1, 2, 2, 3])
    a = R.randint(11, 9999)
    if a % 10 == 0:
        return None
    m = R.choice([10, 100, 1000])
    z = len(str(m)) - 1
    if R.random() < 0.5:
        # a / 10^k × m
        res, rk = a * m, k
        ans = dz(res, rk)
        w = [dz(a, k + z), dz(a * 10, k) if z > 1 else dz(a * 100, k), dz(a, k) + "0" * z if "," in dz(a, k) else dz(a, k - 1), dz(res, rk + 1)]
        return mcq("Calcule %s × %s." % (dz(a, k), dz(m, 0)), ans, w,
                   "Multiplicar por %s: a vírgula anda %d casa%s para a <b>direita</b>. Resposta: <b>%s</b>." % (dz(m, 0), z, "" if z == 1 else "s", ans))
    ans = dz(a, k + z)
    w = [dz(a * m * m, k + z) if k + z < 6 else None, dz(a * m, k), dz(a, k + z + 1), dz(a, k + z - 1)]
    return mcq("Calcule %s ÷ %s." % (dz(a, k), dz(m, 0)), ans, w,
               "Dividir por %s: a vírgula anda %d casa%s para a <b>esquerda</b>. Resposta: <b>%s</b>." % (dz(m, 0), z, "" if z == 1 else "s", ans))


def s1_converter():
    k = R.choice(["m_cm", "cm_m", "kg_g", "L_mL"])
    if k == "m_cm":
        a = R.randint(11, 999)
        return mcq("Quantos centímetros são %s m? (1 m = 100 cm)" % dz(a, 2), dz(a, 0) + " cm", [dz(a, 1) + " cm", dz(a * 10, 0) + " cm", dz(a, 2) + " cm"],
                   "%s × 100 = <b>%s cm</b>." % (dz(a, 2), dz(a, 0)))
    if k == "cm_m":
        a = R.randint(11, 999)
        return mcq("Quantos metros são %d cm?" % a, dz(a, 2) + " m", [dz(a, 1) + " m", dz(a, 3) + " m", "%s m" % num(a * 100)],
                   "%d ÷ 100 = <b>%s m</b>." % (a, dz(a, 2)))
    if k == "kg_g":
        a = R.randint(11, 9999)
        return mcq("Quantos gramas são %s kg? (1 kg = 1.000 g)" % dz(a, 3), dz(a, 0) + " g", [dz(a, 1) + " g", dz(a, 2) + " g", dz(a * 10, 0) + " g"],
                   "%s × 1.000 = <b>%s g</b>." % (dz(a, 3), dz(a, 0)))
    a = R.randint(11, 9999)
    return mcq("Quantos litros são %s mL? (1 L = 1.000 mL)" % dz(a, 0), dz(a, 3) + " L", [dz(a, 2) + " L", dz(a, 1) + " L", dz(a * 1000, 0) + " L"],
               "%s ÷ 1.000 = <b>%s L</b>." % (dz(a, 0), dz(a, 3)))


def sep_wrong(a, k, n):
    """2,5 × 4 → 8,20 (multiplica inteiros e decimais separados)"""
    ip, fp_ = divmod(a, 10 ** k)
    return "%d,%d" % (ip * n, fp_ * n)


def s2_vezes():
    k = R.choice([1, 1, 2])
    a = R.randint(11, 99 * 10 ** (k - 1) + 9)
    if a % 10 == 0:
        return None
    n = R.randint(2, 9) if R.random() < 0.7 else R.randint(11, 25)
    res = a * n
    pic = armada([dz(a, k), str(n)], "×") if R.random() < 0.4 else ""
    w = [sep_wrong(a, k, n), dz(res, k + 1), dz(res, k - 1) if k > 1 else dz(res, 0), dz(res + 10 ** k, k)]
    return mcq(pic + "Calcule %s × %d." % (dz(a, k), n), dz(res, k), w,
               "Multiplique sem a vírgula: %s × %d = %s. O fator tem %d %s, então o produto também: <b>%s</b>." % (num(a), n, num(res), k, "casa decimal" if k == 1 else "casas decimais", dz(res, k)))


def s2_cabeca():
    a, n = R.choice([(25, 4), (5, 2), (25, 8), (125, 8), (75, 4), (15, 2), (5, 6), (25, 6), (5, 12), (125, 4), (35, 2), (45, 2), (25, 12)])
    k = 1 if a < 100 else 2
    res = a * n
    return mcq("Calcule de cabeça: %s × %d." % (dz(a, k), n), dz(res, k), [sep_wrong(a, k, n), dz(res, k + 1), dz(res, k - 1) if k > 1 else dz(res * 10, k), dz(res + 10 ** k, k)],
               "%s × %d = %s. Resposta: <b>%s</b>." % (dz(a, k), n, dz(res, k), dz(res, k)))


def s3_dividir():
    n = R.randint(2, 9)
    k = R.choice([1, 2])
    q = R.randint(11, 99 * 10 ** (k - 1) + 9)
    if q % 10 == 0:
        return None
    a = q * n
    w = [dz(q, k + 1), dz(q * 10, k), dz(q + 10 ** (k - 1), k), dz(a // n // 10, k) if a // n // 10 else None]
    return mcq("Calcule %s ÷ %d." % (dz(a, k), n), dz(q, k), w,
               "%s ÷ %d: divida como se fosse %s ÷ %d = %s e mantenha %d %s. Prova: %s × %d = %s. Resposta: <b>%s</b>." % (
                   dz(a, k), n, num(a), n, num(q), k, "casa decimal" if k == 1 else "casas decimais", dz(q, k), n, dz(a, k), dz(q, k)))


def s3_quociente():
    d = R.choice([2, 4, 5, 8, 10, 20, 25])
    n = R.randint(3, 99)
    if n % d == 0:
        return None
    q10 = n * 1000 // d
    if n * 1000 % d:
        return None
    ans = dz(q10, 3)
    w = ["%d e resto %d" % (n // d, n % d), dz(q10 * 10, 3), dz(q10, 4), "%d,%d" % (n // d, n % d) if dz(q10, 3) != "%d,%d" % (n // d, n % d) else dz(q10 + 100, 3)]
    return mcq("Calcule %d ÷ %d até não sobrar resto." % (n, d), ans, w,
               "%d ÷ %d = %d e resto %d. Continue: coloque a vírgula no quociente e um zero no resto. Resposta: <b>%s</b>." % (n, d, n // d, n % d, ans))


def s4_dinheiro():
    k = R.choice(["vezes", "vezes", "div", "div"])
    p, g = K.next()
    if k == "vezes":
        pr = R.randint(1, 30) * 100 + R.choice([25, 50, 75, 90, 40, 60, 99, 45])
        n = R.randint(2, 9)
        obj = R.choice(["cadernos", "sorvetes", "pastéis", "ingressos", "canetas", "pacotes de biscoito", "garrafas de suco"])
        return mcq("%s comprou %d %s de %s cada. Quanto gastou?" % (p, n, obj, reais(pr)), reais(pr * n),
                   [reais(x) for x in (pr * n // 10 * 10 + 10 if pr * n % 10 else pr * n + 100, pr * (n - 1), pr * n + 100, (pr // 100 * n) * 100 + pr % 100 * n % 100) if x != pr * n],
                   "%d × %s = <b>%s</b>." % (n, reais(pr), reais(pr * n)))
    n = R.randint(2, 8)
    each = R.randint(3, 40) * 100 + R.choice([0, 50, 25, 75, 20, 40, 60, 80])
    tot = each * n
    return mcq("%s e mais %d amigos dividiram igualmente uma conta de %s. Quanto cada um pagou?" % (p, n - 1, reais(tot)), reais(each),
               [reais(x) for x in (tot // (n - 1) if n > 2 and tot % (n - 1) == 0 else each + 100, each * 10 if each < 1000 else each // 10, each + 50, each - 100) if x != each and x > 0],
               "São %d pessoas: %s ÷ %d = <b>%s</b>." % (n, reais(tot), n, reais(each)))


def s5_problema():
    k = R.choice(["fita", "corrida", "garrafas", "tabua", "gasolina", "receita", "peso"])
    p, g = K.next()
    if k == "fita":
        a = R.randint(11, 99)
        n = R.randint(3, 8)
        return mcq("%s cortou uma fita de %s m em %d pedaços iguais. Quanto mede cada pedaço?" % (p, dz(a * n, 1), n), dz(a, 1) + " m",
                   [dz(a, 2) + " m", dz(a * 10, 1) + " m", dz(a + 1, 1) + " m"], "%s ÷ %d = <b>%s m</b>." % (dz(a * n, 1), n, dz(a, 1)))
    if k == "corrida":
        a = R.randint(15, 95)
        if a % 10 == 0:
            return None
        n = R.randint(3, 7)
        return mcq("%s corre %s km por dia. Quantos quilômetros corre em %d dias?" % (p, dz(a, 1), n), dz(a * n, 1) + " km",
                   [sep_wrong(a, 1, n) + " km", dz(a * n, 2) + " km", dz(a * n + 10, 1) + " km", dz(a * n - 10, 1) + " km"], "%d × %s = <b>%s km</b>." % (n, dz(a, 1), dz(a * n, 1)))
    if k == "garrafas":
        a = R.choice([15, 25, 35, 5, 75])
        n = R.randint(4, 12)
        k2 = 1 if a < 10 else 2
        return mcq("Uma garrafa tem %s L de água. Quantos litros há em %d garrafas?" % (dz(a, k2), n), dz(a * n, k2) + " L",
                   [sep_wrong(a, k2, n) + " L", dz(a * n, k2 + 1) + " L", dz(a * n + 10 ** k2, k2) + " L", dz(a * n + 10 ** (k2 - 1), k2) + " L", dz(a * n - 10 ** (k2 - 1), k2) + " L"], "%d × %s = <b>%s L</b>." % (n, dz(a, k2), dz(a * n, k2)))
    if k == "tabua":
        a = R.randint(125, 480)
        m = R.choice([10, 100])
        return mcq("Uma peça de tecido mede %s m. Quanto medem %s peças iguais?" % (dz(a, 2), dz(m, 0)), dz(a * m, 2) + " m",
                   [dz(a, 2 + len(str(m)) - 1) + " m", dz(a * m * 10, 2) + " m", dz(a * m, 3) + " m"], "Multiplicar por %s: a vírgula anda %d casa%s para a direita. <b>%s m</b>." % (dz(m, 0), len(str(m)) - 1, "" if m == 10 else "s", dz(a * m, 2)))
    if k == "gasolina":
        pl = R.randint(550, 690)
        n = R.randint(10, 40)
        return mcq("O litro da gasolina custa %s. Quanto custam %d litros?" % (reais(pl), n), reais(pl * n),
                   [reais(x) for x in (pl * n + 100, pl * (n - 1), pl * n + 1000, pl * n - 10) if x != pl * n], "%d × %s = <b>%s</b>." % (n, reais(pl), reais(pl * n)))
    if k == "receita":
        a = R.choice([25, 5, 75, 15])
        k2 = 2 if a > 9 else 1
        n = R.choice([2, 3, 4])
        return mcq("Uma receita usa %s kg de farinha. Para fazer %d receitas, quantos quilos são necessários?" % (dz(a, k2), n), dz(a * n, k2) + " kg",
                   [sep_wrong(a, k2, n) + " kg", dz(a * n, k2 + 1) + " kg", dz(a + n, k2) + " kg", dz(a * n + 10 ** (k2 - 1), k2) + " kg"], "%d × %s = <b>%s kg</b>." % (n, dz(a, k2), dz(a * n, k2)))
    q = R.randint(11, 99)
    if q % 10 == 0:
        return None
    n = R.choice([4, 5, 6, 8])
    return mcq("%d pacotes iguais de arroz têm, juntos, %s kg. Quantos quilos tem cada pacote?" % (n, dz(q * n, 1)), dz(q, 1) + " kg",
               [dz(q, 2) + " kg", dz(q * 10, 1) + " kg", dz(q + 10, 1) + " kg"], "%s ÷ %d = <b>%s kg</b>." % (dz(q * n, 1), n, dz(q, 1)))


def main():
    seen = set()
    sets = [
        ("× e ÷ por 10, 100 e 1.000", mix(R, seen, [(s1_potencias, 14), (s1_converter, 6)])),
        ("Decimal × número natural", mix(R, seen, [(s2_vezes, 14), (s2_cabeca, 6)])),
        ("Decimal ÷ número natural", mix(R, seen, [(s3_dividir, 14), (s3_quociente, 6)])),
        ("Dinheiro", mix(R, seen, [(s4_dinheiro, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Multiplicar por 10, 100 ou 1.000: a vírgula anda 1, 2 ou 3 casas para a <b>direita</b> (3,25 × 100 = 325).",
         "Dividir por 10, 100 ou 1.000: a vírgula anda para a <b>esquerda</b> (3,25 ÷ 10 = 0,325).",
         "Decimal × natural: multiplique sem a vírgula e dê ao produto o <b>mesmo número de casas decimais</b> (2,35 × 4 → 235 × 4 = 940 → 9,40 = 9,4).",
         "Decimal ÷ natural: divida normalmente e coloque a vírgula no quociente quando chegar à vírgula do dividendo."],
        [("Calcule 1,25 × 6.", ["125 × 6 = 750", "2 casas decimais: 7,50"], "7,5"),
         ("Calcule 7 ÷ 4.", ["7 ÷ 4 = 1 e resto 3", "3 = 30 décimos: 30 ÷ 4 = 7 e resto 2", "2 décimos = 20 centésimos: 20 ÷ 4 = 5"], "1,75")],
        [["2,5 × 4 = 8,20 (multiplicar inteiro e decimal separados)", "Multiplique o número todo: 25 × 4 = 100 → 10,0 = 10."],
         ["Contar errado as casas: 1,25 × 6 = 75,0", "O fator 1,25 tem 2 casas: o produto também tem 2 casas (7,50)."],
         ["Andar a vírgula para o lado errado", "× 10 deixa o número maior (vai para a direita); ÷ 10 deixa menor."]],
        armada(["1,25", "6"], "×", result="7,50"))
    faq = [("O 5º ano multiplica decimal por decimal?", "Não. A BNCC do 5º ano pede multiplicação com multiplicador natural e divisão com divisor natural. Decimal × decimal vem no 6º ano."),
           ("Por que a vírgula anda quando multiplicamos por 10?", "Cada ordem fica 10 vezes maior: os décimos viram unidades, os centésimos viram décimos. Por isso cada algarismo passa uma casa para a esquerda da vírgula.")]
    make_unit(R, "multiplicacao-e-divisao-com-decimais", "N", ["EF05MA08"],
              "Resolver e elaborar problemas de multiplicação e divisão com números naturais e com números racionais cuja representação decimal é finita (com multiplicador natural e divisor natural e diferente de zero), utilizando estratégias diversas, como cálculo por estimativa, cálculo mental e algoritmos",
              "Multiplicação e divisão com números decimais", "× e ÷ com decimais",
              "Atividades de matemática para o 5º ano sobre multiplicação e divisão com números decimais: por 10, 100 e 1.000, decimal × número natural, decimal ÷ número natural, dinheiro e medidas. 100 exercícios com gabarito.",
              "× 10: a vírgula anda para a direita. ÷ 10: para a esquerda.", "Decimal × natural: o produto tem as mesmas casas decimais.",
              body, faq, sets, 10, grade="5-ano")


if __name__ == "__main__":
    main()
