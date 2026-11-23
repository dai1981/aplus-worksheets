# -*- coding: utf-8 -*-
"""
Brasil Matemática 3º ano: Igualdade e sentenças matemáticas (Álgebra, EF03MA11)
  python3 tools/gen_br_matematica_3_igualdade.py
Ideia de igualdade (o sinal = como equilíbrio), diferentes adições e subtrações com o mesmo resultado, verdadeiro ou falso,
número que falta dos dois lados (8 + 5 = ___ + 6), balança em equilíbrio, compensação (+ 1 e − 1).
Erros: ler o = como «dá o resultado» (8 + 5 = 13 + 6 = 19), achar que 15 − 7 = 16 − 6, mexer só num dos lados.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, wrap, text, line, INK, GREEN, FILL, reais

R = random.Random(80312)


def s1_mesma_soma():
    a, b = R.randint(6, 40), R.randint(6, 40)
    s = a + b
    k = R.randint(1, 5)
    ok = "%d + %d" % (a + k, b - k)
    return mcq("Qual adição tem o mesmo resultado que %d + %d?" % (a, b), ok,
               ["%d + %d" % (a + k, b + k), "%d + %d" % (a - k, b - k) if a > k and b > k else "%d + %d" % (a, b + k), "%d − %d" % (s + k, k + 1)],
               "%d + %d = %d e %s = %d. Quando uma parcela ganha %d e a outra perde %d, a soma não muda: <b>%s</b>." % (a, b, s, ok, s, k, k, ok))


def s1_mesma_dif():
    a = R.randint(20, 90)
    b = R.randint(5, a - 5)
    k = R.randint(1, 9)
    ok = "%d − %d" % (a + k, b + k)
    return mcq("Qual subtração tem o mesmo resultado que %d − %d?" % (a, b), ok,
               ["%d − %d" % (a + k, b - k) if b > k else "%d − %d" % (a + k, b), "%d − %d" % (a - k, b + k) if a - k > b + k else "%d − %d" % (a + 2 * k, b), "%d + %d" % (a - b - k, k + 1)],
               "%d − %d = %d. Se os dois números aumentam %d, a diferença não muda: %s = %d. <b>%s</b>." % (a, b, a - b, k, ok, a - b, ok))


def s2_vf():
    a, b = R.randint(5, 30), R.randint(5, 30)
    s = a + b
    k = R.choice(["v1", "f1", "v2", "f2"])
    if k == "v1":
        c = R.randint(2, s - 2)
        frase = "%d + %d = %d + %d" % (a, b, c, s - c)
        ans = "verdadeira"
    elif k == "f1":
        c = R.randint(2, s - 2)
        frase = "%d + %d = %d + %d" % (a, b, c, s - c + R.choice([1, 2, -1]))
        ans = "falsa"
    elif k == "v2":
        c = R.randint(1, 9)
        frase = "%d − %d = %d − %d" % (s, a, s + c, a + c)
        ans = "verdadeira"
    else:
        c = R.randint(1, 9)
        frase = "%d − %d = %d − %d" % (s, a, s + c, a - c if a > c else a + 2 * c)
        ans = "falsa"
    L, Rr = [p.strip() for p in frase.split("=")]
    vl, vr = eval(L.replace("−", "-")), eval(Rr.replace("−", "-"))
    return mcq("A igualdade %s é verdadeira ou falsa?" % frase, ans, ["falsa" if ans == "verdadeira" else "verdadeira", "depende da ordem", "não dá para saber"],
               "%s = %d e %s = %d. Os dois lados %s: <b>%s</b>." % (L, vl, Rr, vr, "valem o mesmo" if vl == vr else "são diferentes", ans))


def s2_falta():
    a, b = R.randint(5, 40), R.randint(5, 40)
    c = R.randint(2, a + b - 2)
    x = a + b - c
    if x <= 0 or c in (a, b):
        return None
    w = [a + b, a + b + c, c - a if c > a else a + b - c + 1]
    return mcq("Que número completa a igualdade? %d + %d = %d + ___" % (a, b, c), str(x), [str(v) for v in w if v != x and v > 0] + [str(x + 1)],
               "%d + %d = %d. Para o outro lado também dar %d: %d + <b>%d</b>. (Não é %d: o sinal = não quer dizer «o resultado é».)" % (a, b, a + b, a + b, c, x, a + b))


def balanca(left, right):
    s = [line(150, 120, 150, 40, INK, 3), line(60, 40, 240, 40, INK, 3),
         "<polygon points='130,128 170,128 150,112' fill='%s'/>" % INK,
         line(60, 40, 60, 62, INK, 1.5), line(240, 40, 240, 62, INK, 1.5),
         "<rect x='20' y='62' width='80' height='10' fill='%s' stroke='%s'/>" % (FILL, GREEN),
         "<rect x='200' y='62' width='80' height='10' fill='%s' stroke='%s'/>" % (FILL, GREEN)]
    for i, v in enumerate(left):
        s.append("<rect x='%d' y='%d' width='34' height='24' rx='4' fill='#fff3c4' stroke='%s'/>" % (22 + (i % 2) * 40, 36 - (i // 2) * 26, INK) + text(39 + (i % 2) * 40, 53 - (i // 2) * 26, v, 13))
    for i, v in enumerate(right):
        s.append("<rect x='%d' y='%d' width='34' height='24' rx='4' fill='#fff3c4' stroke='%s'/>" % (202 + (i % 2) * 40, 36 - (i // 2) * 26, INK) + text(219 + (i % 2) * 40, 53 - (i // 2) * 26, v, 13))
    return wrap(300, 132, "".join(s), "balança em equilíbrio com caixas numeradas")


def s3_balanca():
    a, b, c = R.randint(3, 20), R.randint(3, 20), R.randint(3, 20)
    x = a + b - c
    if x <= 0 or x == c:
        return None
    return mcq(balanca([str(a), str(b)], [str(c), "?"]) + "A balança está em equilíbrio. Que número deve estar na caixa «?»", str(x),
               [str(a + b), str(a + b + c), str(x + 1)],
               "Os dois pratos valem o mesmo: %d + %d = %d, e %d + <b>%d</b> = %d." % (a, b, a + b, c, x, a + b))


def s3_compensa():
    a = R.randint(28, 89)
    b = R.choice([9, 19, 29, 39, 49, 99]) if a > 40 else R.choice([9, 19])
    k = R.choice(["+", "−"])
    if k == "+":
        return mcq("%d + %d é igual a qual conta mais fácil?" % (a, b), "%d + %d" % (a - 1, b + 1),
                   ["%d + %d" % (a + 1, b + 1), "%d + %d" % (a, b + 1), "%d − %d" % (a + b + 1, 1)],
                   "Tirando 1 de um e dando 1 ao outro, a soma não muda: %d + %d = %d + %d = <b>%d</b>." % (a, b, a - 1, b + 1, a + b))
    if b >= a:
        return None
    return mcq("%d − %d é igual a qual conta mais fácil?" % (a, b), "%d − %d" % (a + 1, b + 1),
               ["%d − %d" % (a - 1, b + 1), "%d − %d" % (a, b + 1), "%d − %d" % (a + 1, b)],
               "Somando 1 aos dois números, a diferença não muda: %d − %d = %d − %d = <b>%d</b>." % (a, b, a + 1, b + 1, a - b))


def s4_varias():
    r = R.randint(12, 40)
    pairs = [(a, r - a) for a in range(2, r - 1)]
    a, b = R.choice(pairs)
    c, d = R.choice([p for p in pairs if p != (a, b)])
    e = R.randint(r + 2, r + 30)
    ok = "%d + %d, %d + %d e %d − %d" % (a, b, c, d, e, e - r)
    return mcq("Quais contas têm resultado %d?" % r, ok,
               ["%d + %d, %d + %d e %d − %d" % (a, b + 1, c, d, e, e - r), "%d + %d, %d + %d e %d − %d" % (a, b, c, d + 1, e, e - r),
                "%d + %d, %d + %d e %d − %d" % (a, b, c, d, e, e - r + 1)],
               "Confira cada conta: todas dão %d. <b>%s</b>." % (r, ok))


def s5_problema():
    k = R.choice(["figurinhas", "dinheiro", "times", "potes"])
    if k == "figurinhas":
        a, b = R.randint(12, 30), R.randint(12, 30)
        c = R.randint(10, 30)
        x = a + b - c
        if x <= 0:
            return None
        return mcq("Ana tem %d figurinhas azuis e %d verdes. Bia tem %d figurinhas azuis. Quantas verdes Bia precisa ter para as duas terem o mesmo total?" % (a, b, c), str(x),
                   [str(a + b), str(b), str(x + 1)],
                   "Ana tem %d + %d = %d. Bia: %d + ___ = %d, então <b>%d</b>." % (a, b, a + b, c, a + b, x))
    if k == "dinheiro":
        a, b = R.randint(10, 40), R.randint(10, 40)
        c = R.randint(10, a + b - 5)
        x = a + b - c
        return mcq("Num cofre há %s em cédulas e %s em moedas. Noutro cofre há %s. Quanto falta pôr no segundo cofre para os dois terem o mesmo valor?" % (reais(a * 100), reais(b * 100), reais(c * 100)),
                   reais(x * 100), [reais((a + b) * 100), reais((x + 10) * 100), reais((c - a) * 100) if c > a else reais((x + 1) * 100)],
                   "Primeiro cofre: %d + %d = %d. %d + ___ = %d: falta <b>%s</b>." % (a, b, a + b, c, a + b, reais(x * 100)))
    if k == "times":
        a, b = R.randint(8, 15), R.randint(8, 15)
        c = R.randint(5, 12)
        x = a + b - c
        return mcq("No time Azul há %d meninas e %d meninos. No time Verde há %d meninas. Quantos meninos o time Verde precisa ter para os times ficarem iguais em número?" % (a, b, c), str(x),
                   [str(b), str(a + b), str(x - 1)],
                   "Azul: %d + %d = %d. Verde: %d + <b>%d</b> = %d." % (a, b, a + b, c, x, a + b))
    a, b = R.randint(20, 60), R.randint(5, 15)
    c = R.randint(a + 3, a + 25)
    x = c - (a - b)
    return mcq("Um pote tinha %d balas e saíram %d. Outro pote tinha %d balas. Quantas balas devem sair do segundo pote para os dois ficarem com o mesmo número?" % (a, b, c), str(x),
               [str(b), str(c - a), str(x + 1)],
               "Primeiro pote: %d − %d = %d. Segundo: %d − ___ = %d, então <b>%d</b>." % (a, b, a - b, c, a - b, x))


def main():
    seen = set()
    sets = [
        ("Contas com o mesmo resultado", mix(R, seen, [(s1_mesma_soma, 10), (s1_mesma_dif, 10)])),
        ("Verdadeira ou falsa? Número que falta", mix(R, seen, [(s2_vf, 10), (s2_falta, 10)])),
        ("Balança e compensação", mix(R, seen, [(s3_balanca, 10), (s3_compensa, 10)])),
        ("Várias contas, um resultado", mix(R, seen, [(s4_varias, 10), (s2_falta, 10)])),
        ("Problemas de igualdade", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["O sinal <b>=</b> quer dizer que os dois lados <b>valem o mesmo</b>, como uma balança em equilíbrio. Não quer dizer só «o resultado é».",
         "Várias contas podem ter o mesmo resultado: 8 + 5 = 10 + 3 = 20 − 7 = 13.",
         "Na adição, se uma parcela ganha 2 e a outra perde 2, a soma não muda: 38 + 25 = 40 + 23.",
         "Na subtração, se os dois números aumentam (ou diminuem) o mesmo tanto, a diferença não muda: 52 − 19 = 53 − 20."],
        [("8 + 5 = ___ + 6", ["8 + 5 = 13", "___ + 6 = 13"], "7"),
         ("46 + 29 é igual a qual conta mais fácil?", ["46 − 1 = 45; 29 + 1 = 30"], "45 + 30")],
        [["8 + 5 = 13 + 6 → escrever 13", "O 13 é o valor da esquerda. Do lado direito falta 7, porque 7 + 6 = 13."],
         ["Achar que 15 − 7 = 16 − 6", "15 − 7 = 8 e 16 − 6 = 10: na subtração, os dois números aumentam o mesmo tanto."],
         ["Mudar só um lado da balança", "Para continuar em equilíbrio, os dois lados precisam ter o mesmo valor."]],
        balanca(["8", "5"], ["7", "6"]))
    faq = [("Por que trabalhar a igualdade no 3º ano?", "Muitas crianças leem o sinal = como «dá». Entender que = significa «vale o mesmo» é a base para as equações dos anos seguintes."),
           ("Como explicar com materiais?", "Use uma balança de pratos ou desenhe uma: coloque tampinhas dos dois lados e peça para equilibrar trocando as quantidades.")]
    make_unit(R, "igualdade", "A", ["EF03MA11"],
              "Compreender a ideia de igualdade para escrever diferentes sentenças de adições ou de subtrações de dois números naturais que resultem na mesma soma ou diferença",
              "Igualdade: contas com o mesmo resultado", "Igualdade",
              "Atividades de matemática para o 3º ano sobre igualdade: sentenças com a mesma soma ou diferença, verdadeiro ou falso, número que falta, balança em equilíbrio e compensação. 100 exercícios com gabarito.",
              "O sinal = quer dizer «vale o mesmo».", "38 + 25 = 40 + 23: uma parcela ganha, a outra perde.",
              body, faq, sets, 12)


if __name__ == "__main__":
    main()
