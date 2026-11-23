# -*- coding: utf-8 -*-
"""
Brasil Matemática 7º ano: Números racionais (Números, EF07MA10, EF07MA11, EF07MA12)
  python3 tools/gen_br_matematica_7_numeros_racionais.py
Racionais positivos e negativos nas formas fracionária e decimal; reta numérica; comparar e ordenar; as quatro operações com
racionais (regra dos sinais com frações e decimais); inverso; problemas.
Erros: achar que −0,5 &lt; −0,25 é falso, esquecer o sinal na fração, somar numeradores e denominadores.
"""
import random
from fractions import Fraction as F
from br_common import lesson, mix
from br_9 import M, d, fq, bank, unit

R = random.Random(87005)


def rq():
    if R.random() < 0.5:
        return F(R.choice([-1, 1]) * R.randint(1, 9), R.choice([2, 3, 4, 5, 6, 8]))
    return F(R.choice([-1, 1]) * R.randint(1, 99), R.choice([10, 100]))


def show(x, frac):
    return fq(x) if frac else d(x)


def s1_comparar():
    frac = R.random() < 0.5
    xs = set()
    while len(xs) < 4:
        x = rq() if not frac else F(R.choice([-1, 1]) * R.randint(1, 9), R.choice([2, 3, 4, 5, 6]))
        if frac or (x * 100).denominator == 1:
            xs.add(x)
    xs = sorted(xs)
    sh = xs[:]
    R.shuffle(sh)
    k = R.choice(["maior", "menor", "ordem"])
    if k == "ordem":
        ok = " &lt; ".join(show(x, frac) for x in xs)
        return M("Qual é a ordem crescente de %s?" % "; ".join(show(x, frac) for x in sh), ok, [" &lt; ".join(show(x, frac) for x in xs[::-1]), " &lt; ".join(show(x, frac) for x in sorted(xs, key=abs)) if sorted(xs, key=abs) != xs else " &lt; ".join(show(x, frac) for x in [xs[1], xs[0], xs[2], xs[3]]), " &lt; ".join(show(x, frac) for x in [xs[0], xs[2], xs[1], xs[3]])],
                 "Negativos à esquerda do zero; entre negativos, o de maior módulo é o menor: <b>%s</b>." % ok)
    t = xs[-1] if k == "maior" else xs[0]
    return M("Qual é o %s número: %s?" % (k, "; ".join(show(x, frac) for x in sh)), show(t, frac), [show(x, frac) for x in xs if x != t], "Na reta, o %s fica mais à %s: <b>%s</b>." % (k, "direita" if k == "maior" else "esquerda", show(t, frac)))


def s2_formas():
    x = F(R.choice([-1, 1]) * R.choice([1, 3, 5, 7, 9, 11]), R.choice([2, 4, 5, 8, 20, 25]))
    if R.random() < 0.5:
        return M("Escreva %s na forma decimal." % fq(x), d(x), [d(-x), d(x * 10), "%s%d,%d" % ("−" if x < 0 else "", abs(x.numerator), x.denominator)], "%d ÷ %d = %s; o sinal se mantém: <b>%s</b>." % (abs(x.numerator), x.denominator, d(abs(x)), d(x)))
    return M("Escreva %s como fração irredutível." % d(x), fq(x), [fq(-x), fq(F(x.numerator, x.denominator * 10)), fq(1 / x)], "%s = %s: <b>%s</b>." % (d(x), fq(x), fq(x)))


def s3_operacoes():
    frac = R.random() < 0.55
    if frac:
        a = F(R.choice([-1, 1]) * R.randint(1, 7), R.choice([2, 3, 4, 5, 6]))
        b = F(R.choice([-1, 1]) * R.randint(1, 7), R.choice([2, 3, 4, 5, 6]))
    else:
        a = F(R.choice([-1, 1]) * R.randint(1, 60), 10)
        b = F(R.choice([-1, 1]) * R.randint(1, 60), 10)
    op = R.choice(["+", "−", "×", "÷"])
    r = {"+": a + b, "−": a - b, "×": a * b, "÷": a / b}[op]
    if not frac and op == "÷" and (r * 100).denominator != 1:
        return None
    if not frac and (r * 100).denominator != 1:
        return None
    sb = ("(%s)" % show(b, frac)) if b < 0 else show(b, frac)
    w = {"+": a - b, "−": a + b, "×": -a * b, "÷": -a / b}[op]
    w2 = -r
    ws = [show(w, frac) if (frac or (w * 100).denominator == 1) else show(r + 1, frac), show(w2, frac) if r else "1", show(r + F(1, 2), frac)]
    return M("Calcule %s %s %s." % (show(a, frac), op, sb), show(r, frac), ws, "Use a regra dos sinais%s: <b>%s</b>." % (" e o mesmo denominador" if frac and op in "+−" else "", show(r, frac)))


def s4_problemas():
    k = R.choice(["temp", "bolsa", "receita", "saldo"])
    if k == "temp":
        a = F(R.randint(-80, -5), 10)
        b = F(R.randint(10, 90), 10)
        return M("A temperatura passou de %s °C para %s °C. Qual foi a variação?" % (d(a), d(a + b)), "%s °C" % d(b), ["%s °C" % d(2 * a + b), "%s °C" % d(-b), "%s °C" % d(abs(a) - abs(a + b)) if abs(a) != abs(a + b) else "%s °C" % d(b + 1)],
                 "Final − inicial: %s − (%s) = <b>%s °C</b>." % (d(a + b), d(a), d(b)))
    if k == "bolsa":
        xs = [F(R.choice([-1, 1]) * R.randint(5, 40), 10) for _ in range(3)]
        s = sum(xs)
        return M("Uma ação variou %s em três dias. Qual foi a variação total?" % "; ".join(("+" if x > 0 else "") + d(x) + "%" for x in xs), ("+" if s > 0 else "") + d(s) + "%", [("+" if -s > 0 else "") + d(-s) + "%" if s else "+1%", "+" + d(sum(abs(x) for x in xs)) + "%", ("+" if s + 1 > 0 else "") + d(s + 1) + "%"],
                 "%s = <b>%s%%</b>." % (" + ".join("(%s)" % d(x) for x in xs), ("+" if s > 0 else "") + d(s)))
    if k == "receita":
        f, n = R.choice([F(3, 4), F(2, 3), F(1, 2), F(5, 4)]), R.randint(2, 6)
        return M("Uma receita leva %s de xícara de leite. Para metade da receita, quanto leite vai?" % fq(f), fq(f / 2) + " de xícara", [fq(f * 2) + " de xícara", fq(f - F(1, 2)) + " de xícara" if f > F(1, 2) else fq(f + F(1, 2)) + " de xícara", fq(F(f.numerator, f.denominator + 2)) + " de xícara"],
                 "%s ÷ 2 = <b>%s</b>." % (fq(f), fq(f / 2)))
    s, g = F(R.randint(-500, 300), 1) + F(R.randint(0, 99), 100), F(R.randint(100, 900), 1) + F(R.choice([0, 50, 90]), 100)
    r = s - g
    return M("O saldo era de %s reais e foi debitado %s reais. Qual é o novo saldo?" % (d(s), d(g)), "%s reais" % d(r), ["%s reais" % d(s + g), "%s reais" % d(-r), "%s reais" % d(g - abs(s))],
             "%s − %s = <b>%s reais</b>." % (d(s), d(g), d(r)))


s5_conceitos = bank(R, [
    ("Todo número inteiro é também um número…", "racional", ["natural", "irracional", "decimal infinito"]),
    ("Qual é maior: −0,5 ou −0,25?", "−0,25", ["−0,5", "são iguais", "não dá para comparar"]),
    ("O inverso de −2/3 é…", "−3/2", ["3/2", "2/3", "−2/3"]),
    ("O oposto de −2/3 é…", "2/3", ["−3/2", "3/2", "−2/3"]),
    ("−3/4 é igual a…", "−0,75", ["0,75", "−0,34", "−3,4"]),
    ("Entre −1 e 0 há…", "infinitos números racionais", ["nenhum número", "só −0,5", "10 números"]),
    ("A fração −6/8 simplificada é…", "−3/4", ["3/4", "−6/4", "−2/3"]),
    ("O produto de dois racionais negativos é…", "positivo", ["negativo", "zero", "depende dos números"]),
], "s5_conceitos")


def main():
    seen = set()
    sets = [
        ("Fração e decimal", mix(R, seen, [(s2_formas, 20)])),
        ("Comparar e ordenar", mix(R, seen, [(s1_comparar, 20)])),
        ("Operações com racionais", mix(R, seen, [(s3_operacoes, 20)])),
        ("Problemas", mix(R, seen, [(s4_problemas, 20)])),
        ("Revisão", mix(R, seen, [(s5_conceitos, 8), (s3_operacoes, 6), (s1_comparar, 6)])),
    ]
    body = lesson(
        ["Os <b>números racionais</b> podem ser escritos como fração de inteiros: 3/4, −2/5, 0,7, −1,25 e todos os inteiros.",
         "Na reta, os negativos ficam à esquerda do zero: −0,25 &gt; −0,5.",
         "As operações seguem as mesmas regras de sinais dos inteiros; com frações, use o mesmo denominador para somar e subtrair.",
         "Inverso de a/b é b/a (o produto dá 1); oposto de a/b é −a/b (a soma dá 0)."],
        [("−1/2 + 3/4", ["−2/4 + 3/4"], "1/4"),
         ("(−1,5) × (−0,4)", ["sinais iguais", "1,5 × 0,4 = 0,6"], "0,6")],
        [["Achar −0,5 &gt; −0,25", "Mais longe do zero à esquerda é menor."],
         ["Perder o sinal", "−3/4 = −0,75."],
         ["Somar numeradores e denominadores", "Iguale os denominadores antes."]])
    faq = [("O que são números racionais?", "São os números que podem ser escritos como a/b, com a e b inteiros e b diferente de zero. Incluem os inteiros, as frações e os decimais finitos e periódicos, positivos e negativos."),
           ("O que a BNCC pede no 7º ano?", "Comparar e ordenar números racionais em diferentes contextos e associá-los a pontos da reta numérica (EF07MA10), compreender e utilizar a multiplicação e a divisão de números racionais (EF07MA11) e resolver e elaborar problemas que envolvam as operações com números racionais (EF07MA12).")]
    unit(R, "numeros-racionais", "N", ["EF07MA10", "EF07MA11", "EF07MA12"],
         "Comparar e ordenar números racionais em diferentes contextos e associá-los a pontos da reta numérica; compreender e utilizar a multiplicação e a divisão de números racionais, a relação entre elas e suas propriedades operatórias; resolver e elaborar problemas que envolvam as operações com números racionais",
         "Números racionais: comparar, ordenar e operar", "Números racionais",
         "Atividades de matemática para o 7º ano sobre números racionais positivos e negativos: frações e decimais, comparar e ordenar, as quatro operações, inverso, oposto e problemas. 100 exercícios com gabarito.",
         "Racional = fração de inteiros.", "Mesmas regras de sinais dos inteiros.",
         body, faq, sets, 5, grade="7-ano")


if __name__ == "__main__":
    main()
