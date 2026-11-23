# -*- coding: utf-8 -*-
"""
Brasil Matemática 7º ano: Operações com números inteiros (Números, EF07MA04)
  python3 tools/gen_br_matematica_7_operacoes_com_numeros_inteiros.py
Adição e subtração (sinais iguais e diferentes; subtrair é somar o oposto); multiplicação e divisão (regra dos sinais);
potências de base negativa; expressões numéricas com inteiros; problemas (saldo, temperatura, pontos, altitude).
Erros: −5 − 3 = −2, (−4) × (−3) = −12, (−2)² = −4, confundir −2² com (−2)².
"""
import random
from br_common import lesson, mix
from br_9 import M, d, par, unit

R = random.Random(87003)


def nz(lo=-20, hi=20):
    return R.choice([x for x in range(lo, hi + 1) if x])


def s1_soma():
    a, b = nz(), nz()
    k = R.choice(["+", "−"])
    if k == "+":
        r = a + b
        return M("Calcule %s + %s." % (d(a), par(b)), d(r), [d(-r) if r else "1", d(abs(a) + abs(b)) if abs(a) + abs(b) != r else d(r + 2), d(a - b) if a - b != r else d(r - 2)],
                 ("Sinais iguais: some os módulos e mantenha o sinal" if (a > 0) == (b > 0) else "Sinais diferentes: subtraia os módulos e fique com o sinal do maior módulo") + ": <b>%s</b>." % d(r))
    r = a - b
    return M("Calcule %s − %s." % (d(a), par(b)), d(r), [d(a + b) if a + b != r else d(r + 1), d(-r) if r else "1", d(abs(a) - abs(b)) if abs(a) - abs(b) != r else d(r - 2)],
             "Subtrair é somar o oposto: %s + %s = <b>%s</b>." % (d(a), par(-b), d(r)))


def s2_multdiv():
    a, b = nz(-12, 12), nz(-12, 12)
    if R.random() < 0.5:
        return M("Calcule %s × %s." % (par(a), par(b)), d(a * b), [d(-a * b), d(a + b) if a + b != a * b else d(a * b + 1), d(abs(a * b) + 1)],
                 "Sinais %s: resultado %s. %d × %d = %d → <b>%s</b>." % ("iguais" if (a > 0) == (b > 0) else "diferentes", "positivo" if a * b > 0 else "negativo", abs(a), abs(b), abs(a * b), d(a * b)))
    p = a * b
    return M("Calcule %s ÷ %s." % (par(p), par(b)), d(a), [d(-a), d(p - b) if p - b != a else d(a + 1), d(b) if b != a else d(a * 2)],
             "Sinais %s: resultado %s: <b>%s</b>." % ("iguais" if (p > 0) == (b > 0) else "diferentes", "positivo" if a > 0 else "negativo", d(a)))


def s3_potencia():
    b = R.choice([-1, -2, -3, -4, -5, -10])
    e = R.randint(2, 4) if abs(b) < 10 else R.randint(2, 3)
    k = R.choice(["par", "sem"])
    if k == "par":
        v = b ** e
        return M("Calcule (%s)%s." % (d(b), "²³⁴"[e - 2]), d(v), [d(-v), d(b * e), d(abs(b) * e)],
                 "Expoente %s: resultado %s. <b>%s</b>." % ("par" if e % 2 == 0 else "ímpar", "positivo" if v > 0 else "negativo", d(v)))
    v = -(abs(b) ** 2)
    return M("Calcule −%d² (sem parênteses)." % abs(b), d(v), [d(-v), d(-2 * abs(b)), d(2 * abs(b))], "Sem parênteses, o expoente vale só para o %d: −(%d²) = <b>%s</b>." % (abs(b), abs(b), d(v)))


def s4_expressao():
    a, b, c, e = nz(-9, 9), nz(-9, 9), nz(-6, 6), nz(-5, 5)
    t = R.randint(0, 3)
    if t == 0:
        q, v = "%s + %s × %s" % (d(a), par(b), par(c)), a + b * c
        w = (a + b) * c
    elif t == 1:
        q, v = "(%s − %s) × %s" % (d(a), par(b), par(c)), (a - b) * c
        w = a - b * c
    elif t == 2:
        q, v = "%s × %s − %s × %s" % (par(a), par(b), par(c), par(e)), a * b - c * e
        w = a * b + c * e
    else:
        q, v = "%s ÷ %s + %s" % (par(a * c), par(c), par(b)), a + b
        w = a - b
    if w == v:
        return None
    return M("Calcule %s." % q, d(v), [d(w), d(-v) if v else "1", d(v + 2)], "Primeiro parênteses, depois × e ÷, por fim + e −, com a regra dos sinais: <b>%s</b>." % d(v))


def s5_problemas():
    k = R.choice(["temp", "saldo", "pontos", "mergulho", "historia"])
    if k == "temp":
        a, b, c = R.randint(-8, 4), R.randint(3, 12), R.randint(2, 15)
        r = a + b - c
        return M("A temperatura era %s °C. Subiu %d °C e, à noite, caiu %d °C. Qual é a temperatura final?" % (d(a), b, c), "%s °C" % d(r), ["%s °C" % d(a - b + c), "%s °C" % d(-r) if r else "1 °C", "%s °C" % d(a + b + c)],
                 "%s + %d − %d = <b>%s °C</b>." % (d(a), b, c, d(r)))
    if k == "saldo":
        s = R.randint(-200, 100)
        dp, gs = R.randint(50, 300), R.randint(100, 500)
        r = s + dp - gs
        return M("O saldo de Ana era %s reais. Ela depositou %d reais e gastou %d reais. Qual é o saldo agora?" % (d(s), dp, gs), "%s reais" % d(r), ["%s reais" % d(-r) if r else "1 real", "%s reais" % d(s - dp + gs), "%s reais" % d(dp - gs)],
                 "%s + %d − %d = <b>%s reais</b>." % (d(s), dp, gs, d(r)))
    if k == "pontos":
        c, e = R.randint(5, 15), R.randint(2, 12)
        pc, pe = R.choice([3, 4, 5]), R.choice([-1, -2])
        r = c * pc + e * pe
        return M("Num jogo, cada acerto vale +%d pontos e cada erro vale %s pontos. Bia acertou %d e errou %d. Quantos pontos ela fez?" % (pc, d(pe), c, e), d(r), [d(c * pc + e * abs(pe)), d(c * pc), d(c * pc - e)] if pe == -2 else [d(c * pc + e), d(c * pc), d(c * pc - 2 * e)],
                 "%d × %d + %d × (%s) = %d − %d = <b>%s</b>." % (c, pc, e, d(pe), c * pc, e * abs(pe), d(r)))
    if k == "mergulho":
        p, sub = R.randint(10, 40), R.randint(3, 9)
        return M("Um mergulhador está a %s m (abaixo do nível do mar). Ele sobe %d m. Em que posição fica?" % (d(-p), sub), "%s m" % d(-p + sub), ["%s m" % d(-p - sub), "%s m" % d(p - sub), "%s m" % d(p + sub)], "%s + %d = <b>%s m</b>." % (d(-p), sub, d(-p + sub)))
    a, b = R.randint(100, 500), R.randint(1500, 2026)
    return M("Arquimedes nasceu por volta de %d a.C. (ano −%d). Quantos anos se passaram até %d d.C.?" % (a, a, b), "%s anos" % d(a + b - 1), ["%s anos" % d(b - a), "%s anos" % d(a + b + 1), "%s anos" % d(b)],
             "Como não existe ano zero, de −%d até %d passam %d + %d − 1 = <b>%s anos</b>." % (a, b, a, b, d(a + b - 1)))


def main():
    seen = set()
    sets = [
        ("Adição e subtração", mix(R, seen, [(s1_soma, 20)])),
        ("Multiplicação e divisão", mix(R, seen, [(s2_multdiv, 20)])),
        ("Potências e sinais", mix(R, seen, [(s3_potencia, 10), (s2_multdiv, 10)])),
        ("Expressões numéricas", mix(R, seen, [(s4_expressao, 20)])),
        ("Problemas", mix(R, seen, [(s5_problemas, 20)])),
    ]
    body = lesson(
        ["Adição: sinais iguais, some os módulos e mantenha o sinal (−3 + (−5) = −8); sinais diferentes, subtraia os módulos e use o sinal do maior (−7 + 4 = −3).",
         "Subtração: some o oposto. 5 − (−3) = 5 + 3 = 8.",
         "Multiplicação e divisão: sinais iguais dão resultado positivo; sinais diferentes, negativo.",
         "Potência de base negativa: expoente par dá positivo, ímpar dá negativo. (−2)² = 4, mas −2² = −4."],
        [("−6 − (−9)", ["−6 + 9"], "3"),
         ("(−3) × (−4) ÷ (−2)", ["12 ÷ (−2)"], "−6")],
        [["−5 − 3 = −2", "−5 − 3 = −5 + (−3) = −8."],
         ["(−4) × (−3) = −12", "Sinais iguais: +12."],
         ["(−2)² = −4", "(−2) × (−2) = 4."]])
    faq = [("Qual é a regra dos sinais?", "Na multiplicação e na divisão, sinais iguais dão resultado positivo e sinais diferentes dão resultado negativo. Na adição, compare os módulos."),
           ("O que a BNCC pede no 7º ano?", "Resolver e elaborar problemas que envolvam operações com números inteiros (EF07MA04).")]
    unit(R, "operacoes-com-numeros-inteiros", "N", ["EF07MA04"],
         "Resolver e elaborar problemas que envolvam operações com números inteiros",
         "Operações com números inteiros: regra dos sinais", "Operações com inteiros",
         "Atividades de matemática para o 7º ano sobre operações com números inteiros: adição, subtração, multiplicação, divisão, potências, regra dos sinais, expressões e problemas. 100 exercícios com gabarito.",
         "Sinais iguais: +. Sinais diferentes: −.", "Subtrair é somar o oposto.",
         body, faq, sets, 3, grade="7-ano")


if __name__ == "__main__":
    main()
