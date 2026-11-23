# -*- coding: utf-8 -*-
"""
Brasil Matemática 5º ano: Porcentagem (Números, EF05MA06)
  python3 tools/gen_br_matematica_5_porcentagem.py
10%, 25%, 50%, 75% e 100% com figuras (quadrado de 100 partes); porcentagem e fração (1/10, 1/4, 1/2, 3/4, 1);
calcular a porcentagem de uma quantidade com cálculo mental; descontos e educação financeira; problemas.
Erros: 25% de 80 = 25, 10% = dividir por 100, confundir o desconto com o preço final.
"""
import random
import gen_br_matematica_5_numeros_decimais as DEC
from br_common import mcq, num, lesson, make_unit, mix, fr, reais, disco, Kids

R = random.Random(80506)
K = Kids(R)
P = {10: (1, 10), 25: (1, 4), 50: (1, 2), 75: (3, 4), 100: (1, 1)}
PL = [10, 25, 50, 75, 100]


def pct(p):
    return "%d%%" % p


def frp(p):
    a, b = P[p]
    return "1 inteiro" if b == 1 else fr(a, b)


def grade(p):
    """quadrado de 100 partes com p partes pintadas em lugares variados (linhas inteiras e partes soltas)"""
    from br_common import wrap, INK
    cells = list(range(100))
    if R.random() < 0.5:
        on = set(R.sample(cells, p))
    else:
        rows = R.sample(range(10), p // 10)
        on = {r * 10 + c for r in rows for c in range(10)}
        rest = [x for x in cells if x not in on]
        on |= set(R.sample(rest, p % 10))
    c, out = 16, []
    for i in cells:
        x, y = 6 + (i % 10) * c, 6 + (i // 10) * c
        out.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='0.8'/>" % (x, y, c, c, "#7cc68f" if i in on else "#fff", INK))
    out.append("<rect x='6' y='6' width='160' height='160' fill='none' stroke='%s' stroke-width='2'/>" % INK)
    return wrap(172, 172, "".join(out), "quadrado dividido em 100 partes iguais, %d pintadas" % p)


def s1_figura():
    p = R.choice([10, 20, 25, 30, 35, 40, 45, 50, 60, 70, 75, 80, 90, 15, 5])
    return mcq(grade(p) + "Que porcentagem do quadrado está pintada?", pct(p), [pct(x) for x in (100 - p, p // 10 if p % 10 == 0 else p + 5, p + 10 if p < 90 else p - 20, p * 2 if p < 50 else p - 10, 5 if p != 5 else 50) if x != p],
               "O quadrado tem 100 partes e %d estão pintadas: %d em 100 = <b>%d%%</b>." % (p, p, p))


def s1_disco():
    d = R.choice([2, 4, 4, 10, 10])
    k = R.randint(1, d)
    p = 100 * k // d
    return mcq(disco(d, k) + "Que porcentagem do círculo está pintada?", pct(p), [pct(x) for x in (100 - p, k, d, p + 10 if d == 10 else 25, 50, 75) if x != p and 0 < x <= 100],
               "O círculo tem %d partes iguais e %d %s: %s = %s = <b>%d%%</b>." % (d, k, "está pintada" if k == 1 else "estão pintadas", fr(k, d), fr(p, 100), p))


def frx(p):
    from fractions import Fraction
    f = Fraction(p, 100)
    return "1 inteiro" if f == 1 else fr(f.numerator, f.denominator)


PF = [10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90, 100]


def s2_fracao():
    p = R.choice(PF)
    near = sorted([x for x in PF if x != p], key=lambda x: abs(x - p))
    if R.random() < 0.5:
        return mcq("Qual fração é igual a %s?" % pct(p), frx(p), [frx(x) for x in near[:2]] + [fr(1, p // 10) if p % 10 == 0 and p < 100 and p > 10 else fr(1, 100), fr(p // 10 if p % 10 == 0 else p, 10) if p < 100 else fr(1, 10)],
                   "%s = %s = <b>%s</b>." % (pct(p), fr(p, 100), frx(p)))
    return mcq("Que porcentagem é igual a %s?" % frx(p), pct(p), [pct(x) for x in near[:3]],
               "%s = %s = <b>%s</b>." % (frx(p), fr(p, 100), pct(p)))


def s2_decimal():
    p = R.choice([10, 20, 25, 50, 75, 100, 5, 30])
    dd = {10: "0,1", 20: "0,2", 25: "0,25", 50: "0,5", 75: "0,75", 100: "1", 5: "0,05", 30: "0,3"}
    wr = {10: ["0,01", "10", "1,0"], 20: ["0,02", "2,0", "20"], 25: ["2,5", "0,025", "0,4"], 50: ["0,05", "5,0", "0,2"], 75: ["7,5", "0,075", "0,34"],
          100: ["0,1", "100", "10"], 5: ["0,5", "5", "0,005"], 30: ["0,03", "3,0", "30"]}
    return mcq("Que número decimal é igual a %s?" % pct(p), dd[p], wr[p], "%s = %s = <b>%s</b>." % (pct(p), fr(p, 100), dd[p]))


def calc(p, n):
    a, b = P[p]
    return n // b * a


def s3_calcular():
    p = R.choice(PL)
    a, b = P[p]
    n = R.choice([x for x in range(20, 1001, 20) if x % b == 0 and x % 10 == 0])
    ans = calc(p, n)
    how = {10: "10%% = %s: %s ÷ 10 = %s" % (fr(1, 10), num(n), num(ans)), 25: "25%% = %s: %s ÷ 4 = %s" % (fr(1, 4), num(n), num(ans)),
           50: "50%% = metade: %s ÷ 2 = %s" % (num(n), num(ans)), 75: "75%% = %s: %s ÷ 4 = %s e %s × 3 = %s" % (fr(3, 4), num(n), num(n // 4), num(n // 4), num(ans)),
           100: "100%% é o inteiro: %s" % num(n)}[p]
    w = [num(x) for x in (p, n // 10 if p != 10 else n // 100, n - ans, n // 4 if p != 25 else n // 2, n * 2, ans + 10) if x > 0 and x != ans]
    return mcq("Quanto é %s de %s?" % (pct(p), num(n)), num(ans), w, how + ". Resposta: <b>%s</b>." % num(ans))


def s3_quanto():
    n = R.choice([40, 60, 80, 120, 200, 400, 240, 160, 300, 500])
    p = R.choice([10, 25, 50, 75])
    ans = calc(p, n)
    if n % P[p][1]:
        return None
    return mcq("%s é quanto por cento de %s?" % (num(ans), num(n)), pct(p), [pct(x) for x in (10, 25, 50, 75, 100) if x != p],
               "%s ÷ %s = %s, e %s = <b>%s</b>." % (num(ans), num(n), frp(p), frp(p), pct(p)))


ITENS = [("uma bicicleta", 400, 1200), ("um tênis", 120, 400), ("uma mochila", 80, 240), ("um jogo de tabuleiro", 60, 200), ("uma camiseta", 40, 120),
         ("um livro", 40, 100), ("uma bola", 40, 160), ("um patinete", 200, 600), ("um fone de ouvido", 80, 320), ("uma lancheira", 40, 120)]


def s4_desconto():
    obj, lo, hi = R.choice(ITENS)
    p = R.choice([10, 25, 50, 10, 25])
    pr = R.choice([x for x in range(lo, hi + 1, 20) if x % P[p][1] == 0 and (x // P[p][1]) % 1 == 0])
    d = calc(p, pr)
    if R.random() < 0.5:
        return mcq("%s custa %s. A loja dá %s de desconto. De quanto é o desconto?" % (obj[0].upper() + obj[1:], reais(pr * 100), pct(p)), reais(d * 100),
                   [reais((pr - d) * 100), reais(p * 100), reais(d * 200), reais(pr * 10)],
                   "%s de %s = %s." % (pct(p), reais(pr * 100), "<b>%s</b>" % reais(d * 100)))
    return mcq("%s custa %s. Com %s de desconto, quanto vai custar?" % (obj[0].upper() + obj[1:], reais(pr * 100), pct(p)), reais((pr - d) * 100),
               [reais(d * 100), reais((pr - p) * 100), reais((pr + d) * 100), reais(pr * 100), reais((pr - 2 * d) * 100)],
               "Desconto: %s de %s = %s. Preço: %s − %s = <b>%s</b>." % (pct(p), reais(pr * 100), reais(d * 100), reais(pr * 100), reais(d * 100), reais((pr - d) * 100)))


def s4_poupar():
    p, g = K.next()
    m = R.choice([20, 40, 60, 80, 100, 120, 200])
    pc = R.choice([10, 25, 50])
    if m % P[pc][1]:
        return None
    k = R.choice(["guarda", "gasta"])
    s = calc(pc, m)
    if k == "guarda":
        return mcq("%s ganhou %s de mesada e guardou %s no cofrinho. Quanto %s guardou?" % (p, reais(m * 100), pct(pc), g), reais(s * 100),
                   [reais((m - s) * 100), reais(pc * 100), reais(s * 200), reais(m * 100), reais(s * 300)], "%s de %s = <b>%s</b>." % (pct(pc), reais(m * 100), reais(s * 100)))
    return mcq("%s tinha %s e gastou %s. Quanto sobrou?" % (p, reais(m * 100), pct(pc)), reais((m - s) * 100),
               [reais(s * 100), reais((m - pc) * 100), reais(m * 100)], "Gastou %s de %s = %s. Sobrou %s − %s = <b>%s</b>." % (pct(pc), reais(m * 100), reais(s * 100), reais(m * 100), reais(s * 100), reais((m - s) * 100)))


def s5_problema():
    k = R.choice(["turma", "pesquisa", "jogo", "comparar", "garrafa", "dobro"])
    if k == "turma":
        n = R.choice([20, 24, 28, 32, 36, 40])
        p = R.choice([25, 50, 75])
        a = calc(p, n)
        return mcq("Numa turma de %d alunos, %s vão para a escola a pé. Quantos alunos vão a pé?" % (n, pct(p)), str(a), [str(n - a), str(p), str(n // 10)],
                   "%s de %d = %d. <b>%d alunos</b>." % (pct(p), n, a, a))
    if k == "pesquisa":
        n = R.choice([40, 80, 120, 200, 400])
        p = R.choice([10, 25, 50, 75])
        a = calc(p, n)
        sp = R.choice(["futebol", "vôlei", "natação", "basquete", "judô"])
        return mcq("Numa pesquisa com %d crianças, %s preferem %s. Quantas crianças preferem %s?" % (n, pct(p), sp, sp), str(a), [str(n - a), str(p), str(a * 2) if a * 2 != n - a else str(a + 10)],
                   "%s de %d = <b>%d</b>." % (pct(p), n, a))
    if k == "jogo":
        n = R.choice([20, 40, 60, 80])
        a = calc(R.choice([25, 50, 75]), n)
        p, g = K.next()
        pc = a * 100 // n
        return mcq("%s fez %d arremessos e acertou %d. Que porcentagem dos arremessos %s acertou?" % (p, n, a, g), pct(pc), [pct(x) for x in (10, 25, 50, 75, 100, a) if x != pc],
                   "%d de %d = %s = <b>%s</b>." % (a, n, frp(pc), pct(pc)))
    if k == "comparar":
        a = R.choice([40, 80, 120, 200])
        b = R.choice([40, 80, 120, 200])
        if a == b:
            return None
        x, y = calc(50, a), calc(25, b)
        if x == y:
            return None
        return mcq("O que é maior: 50%% de %d ou 25%% de %d?" % (a, b), "50%% de %d (= %d)" % (a, x) if x > y else "25%% de %d (= %d)" % (b, y),
                   ["50%% de %d (= %d)" % (a, x) if x < y else "25%% de %d (= %d)" % (b, y), "São iguais", "Não dá para saber"],
                   "50%% de %d = %d e 25%% de %d = %d. <b>%s</b>." % (a, x, b, y, "50% de " + str(a) if x > y else "25% de " + str(b)))
    if k == "garrafa":
        L = R.choice([1000, 2000, 500])
        p = R.choice([25, 50, 75])
        a = calc(p, L)
        return mcq("Uma garrafa de %s mL estava cheia. Bebemos %s da água. Quantos mililitros bebemos?" % (num(L), pct(p)), "%s mL" % num(a),
                   ["%s mL" % num(x) for x in (L - a, p, L // 10, L, L // 4) if x != a], "%s de %s mL = <b>%s mL</b>." % (pct(p), num(L), num(a)))
    n = R.choice([30, 50, 70, 90, 110, 130])
    return mcq("Quanto é 10%% de %d e quanto é 20%% de %d?" % (n * 10, n * 10), "%d e %d" % (n, 2 * n), ["%d e %d" % (n * 10 // 100, n * 2 * 10 // 100), "%d e %d" % (10, 20), "%d e %d" % (n, n + 10)],
               "10%% de %d = %d ÷ 10 = %d. 20%% é o dobro de 10%%: %d. <b>%d e %d</b>." % (n * 10, n * 10, n, 2 * n, n, 2 * n))


def main():
    seen = set()
    sets = [
        ("Porcentagem nas figuras", mix(R, seen, [(s1_figura, 14), (s1_disco, 6)])),
        ("Porcentagem, fração e decimal", mix(R, seen, [(s2_fracao, 12), (s2_decimal, 8)])),
        ("Calcular porcentagens", mix(R, seen, [(s3_calcular, 14), (s3_quanto, 6)])),
        ("Descontos e dinheiro", mix(R, seen, [(s4_desconto, 12), (s4_poupar, 8)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["<b>Por cento</b> (%) quer dizer «em cada 100». 30% = 30 em 100 = " + fr(30, 100) + ".",
         "Lembre: 10% = " + fr(1, 10) + ", 25% = " + fr(1, 4) + ", 50% = " + fr(1, 2) + " (metade), 75% = " + fr(3, 4) + " e 100% = o inteiro.",
         "Para calcular: 10% → divida por 10; 50% → divida por 2; 25% → divida por 4; 75% → divida por 4 e multiplique por 3.",
         "Num <b>desconto</b>, calcule quanto vale a porcentagem e subtraia do preço."],
        [("Quanto é 25% de 160?", ["25% = " + fr(1, 4), "160 ÷ 4 = 40"], "40"),
         ("Um tênis custa R$ 120,00 e tem 10% de desconto. Quanto vai custar?", ["10% de 120 = 12", "120 − 12 = 108"], "R$ 108,00")],
        [["25% de 80 = 25", "25% não é o número 25: é " + fr(1, 4) + ". 80 ÷ 4 = 20."],
         ["10% = dividir por 100", "10% = " + fr(10, 100) + " = " + fr(1, 10) + ": divida por 10."],
         ["Responder o desconto quando a pergunta é o preço final", "Depois de achar o desconto, subtraia do preço."]],
        DEC.grade100(25))
    faq = [("Quais porcentagens o 5º ano estuda?", "A BNCC pede associar 10%, 25%, 50%, 75% e 100% a décima parte, quarta parte, metade, três quartos e um inteiro, e calcular com cálculo mental, também em situações de educação financeira."),
           ("Como calcular 75% de um número de cabeça?", "Divida o número por 4 (isso é 25%) e multiplique por 3. Exemplo: 75% de 40 = 40 ÷ 4 × 3 = 30.")]
    make_unit(R, "porcentagem", "N", ["EF05MA06"],
              "Associar as representações 10%, 25%, 50%, 75% e 100% respectivamente à décima parte, quarta parte, metade, três quartos e um inteiro, para calcular porcentagens, utilizando estratégias pessoais, cálculo mental e calculadora, em contextos de educação financeira, entre outros",
              "Porcentagem: 10%, 25%, 50%, 75% e 100%", "Porcentagem",
              "Atividades de matemática para o 5º ano sobre porcentagem: 10%, 25%, 50%, 75% e 100%, porcentagem e fração, cálculo mental, descontos e educação financeira. 100 exercícios com gabarito.",
              "% quer dizer «em cada 100».", "10% = 1/10, 25% = 1/4, 50% = 1/2, 75% = 3/4, 100% = 1 inteiro.",
              body, faq, sets, 6, grade="5-ano")


if __name__ == "__main__":
    main()
