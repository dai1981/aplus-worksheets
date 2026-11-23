# -*- coding: utf-8 -*-
"""
Brasil Matemática 3º ano: Tabuada (Números, EF03MA03, EF03MA07)
  python3 tools/gen_br_matematica_3_tabuada.py
Tabuada do 2, 3, 4, 5 e 10 (BNCC) e também do 6 ao 9 para revisão; adição de parcelas iguais, dobro e triplo,
fator que falta, sequência da tabuada, propriedade comutativa (3 × 4 = 4 × 3).
Erros: somar em vez de multiplicar (4 × 3 = 7), errar a contagem de 2 em 2 ou de 5 em 5, confundir dobro e metade.
"""
import random
from br_common import mcq, num, lesson, make_unit, mix, arranjo, grupos, KINDS, coisas, COISAS

R = random.Random(80307)
BASE = [2, 3, 4, 5, 10]


def near(a, b):
    p = a * b
    return [str(x) for x in (a + b, p + a, p - a, p + b, p - b, (a + 1) * b) if x != p and x > 0]


def s1_basica():
    a = R.choice(BASE)
    b = R.randint(1, 10)
    if R.random() < 0.5:
        a, b = b, a
    return mcq("Quanto é %d × %d?" % (a, b), str(a * b), near(a, b), "%d × %d = <b>%d</b>." % (a, b, a * b))


def s1_parcelas():
    a = R.choice(BASE)
    b = R.randint(2, 6)
    soma = " + ".join([str(a)] * b)
    return mcq("Que multiplicação é igual a %s?" % soma, "%d × %d" % (b, a), ["%d × %d" % (a, a), "%d + %d" % (b, a), "%d × %d" % (b, a * b)],
               "São %d parcelas iguais a %d: <b>%d × %d</b> = %d." % (b, a, b, a, a * b))


def s2_figura():
    a = R.choice([2, 3, 4, 5])
    b = R.randint(2, 6)
    kind = R.choice(KINDS)
    if R.random() < 0.5:
        return mcq(arranjo(a, b, kind) + "Quantos objetos há? Escolha a multiplicação certa.", "%d × %d = %d" % (a, b, a * b),
                   ["%d + %d = %d" % (a, b, a + b), "%d × %d = %d" % (a, b, a * b + b), "%d × %d = %d" % (a, a, a * a) if a != b else "%d × %d = %d" % (b, b + 1, b * (b + 1))],
                   "São %d linhas com %d em cada: <b>%d × %d = %d</b>." % (a, b, a, b, a * b))
    nome = coisas(kind, 2).split(" ", 1)[1]
    return mcq(grupos(a, b, kind) + "%s %s há ao todo?" % ("Quantas" if COISAS[kind][2] == "f" else "Quantos", nome), str(a * b),
               near(a, b), "São %d grupos de %d: %d × %d = <b>%d</b>." % (a, b, a, b, a * b))


def s2_dobro():
    n = R.randint(3, 50)
    k = R.choice(["dobro", "triplo", "quadruplo"])
    f = {"dobro": 2, "triplo": 3, "quadruplo": 4}[k]
    if f > 2 and n > 30:
        return None
    nome = {"dobro": "o dobro", "triplo": "o triplo", "quadruplo": "o quádruplo"}[k]
    return mcq("Qual é %s de %d?" % (nome, n), str(f * n), [str(n + f), str(f * n + f), str(n // 2) if n % 2 == 0 and f == 2 else str((f + 1) * n)],
               "%s é %d × %d = <b>%d</b>." % (nome[0].upper() + nome[1:], f, n, f * n))


def s3_falta():
    a = R.choice(BASE + [6, 7, 8, 9])
    b = R.randint(2, 10)
    p = a * b
    if R.random() < 0.5:
        return mcq("Que número falta? %d × ___ = %d" % (a, p), str(b), [str(p - a), str(b + 1), str(b - 1), str(a)],
                   "Pense: %d vezes quanto dá %d? %d × %d = %d. Resposta: <b>%d</b>." % (a, p, a, b, p, b))
    return mcq("Que número falta? ___ × %d = %d" % (b, p), str(a), [str(p - b), str(a + 1), str(a - 1), str(b)],
               "%d × %d = %d. Resposta: <b>%d</b>." % (a, b, p, a))


def s3_revisao():
    a = R.randint(6, 9)
    b = R.randint(2, 9)
    if R.random() < 0.5:
        a, b = b, a
    return mcq("Quanto é %d × %d?" % (a, b), str(a * b), near(a, b), "%d × %d = <b>%d</b>." % (a, b, a * b))


def s4_seq():
    a = R.choice([2, 3, 4, 5, 6, 10])
    st = R.randint(1, 5)
    seq = [a * (st + i) for i in range(5)]
    miss = R.randint(1, 4)
    shown = [str(x) if i != miss else "___" for i, x in enumerate(seq)]
    return mcq("Complete a sequência da tabuada do %d: %s." % (a, ", ".join(shown)), str(seq[miss]),
               [str(seq[miss] + 1), str(seq[miss] - 1), str(seq[miss] + a), str(seq[miss] - a)],
               "A sequência vai de %d em %d: <b>%d</b>." % (a, a, seq[miss]))


def s4_comut():
    a, b = R.randint(2, 9), R.randint(2, 9)
    if a == b:
        return None
    k = R.choice(["com", "comp"])
    if k == "com":
        return mcq("Sabendo que %d × %d = %d, quanto é %d × %d?" % (a, b, a * b, b, a), str(a * b), [str(a * b + 1), str(a + b), str(a * (b + 1))],
                   "A ordem dos fatores não altera o produto: <b>%d</b>." % (a * b))
    x, y = (a, b) if a * b != (a + 1) * (b - 1) else (a, b + 1)
    p = x * y
    o1 = "&gt;" if p > (x + 1) * (y - 1) else ("&lt;" if p < (x + 1) * (y - 1) else "=")
    L, Rr = "%d × %d" % (x, y), "%d × %d" % (x + 1, y - 1)
    ok = "%s %s %s" % (L, o1, Rr)
    return mcq("Compare %s e %s. Qual frase está certa?" % (L, Rr), ok, ["%s %s %s" % (L, c, Rr) for c in ("&gt;", "&lt;", "=") if c != o1] + ["%s %s %s" % (Rr, o1, L)],
               "%s = %d e %s = %d: <b>%s</b>." % (L, p, Rr, (x + 1) * (y - 1), ok))


def s5_problema():
    k = R.choice(["rodas", "pernas", "dedos", "caixas", "pacotes", "semanas", "notas"])
    n = R.randint(2, 10)
    T = {"rodas": ("Quantas rodas têm %d bicicletas?", 2, "Cada bicicleta tem 2 rodas"),
         "pernas": ("Quantas patas têm %d cachorros?", 4, "Cada cachorro tem 4 patas"),
         "dedos": ("Quantos dedos há em %d mãos?", 5, "Cada mão tem 5 dedos"),
         "caixas": ("Uma caixa tem 10 ovos. Quantos ovos há em %d caixas?", 10, "Cada caixa tem 10 ovos"),
         "pacotes": ("Um pacote tem 3 iogurtes. Quantos iogurtes há em %d pacotes?", 3, "Cada pacote tem 3 iogurtes"),
         "semanas": ("Quantos dias há em %d semanas?", 7, "Cada semana tem 7 dias"),
         "notas": ("Quantos reais há em %d cédulas de R$ 5?", 5, "Cada cédula vale R$ 5")}
    q, f, why = T[k]
    if k in ("semanas",) and n > 4:
        return None
    return mcq(q % n, str(n * f), [str(n + f), str(n * f + f), str(n * f - f), str(n * (f + 1))],
               "%s: %d × %d = <b>%d</b>." % (why, n, f, n * f))


def main():
    seen = set()
    sets = [
        ("Tabuada do 2, 3, 4, 5 e 10", mix(R, seen, [(s1_basica, 14), (s1_parcelas, 6)])),
        ("Multiplicação com figuras, dobro e triplo", mix(R, seen, [(s2_figura, 12), (s2_dobro, 8)])),
        ("Fator que falta e tabuada do 6 ao 9", mix(R, seen, [(s3_falta, 10), (s3_revisao, 10)])),
        ("Sequências e ordem dos fatores", mix(R, seen, [(s4_seq, 12), (s4_comut, 8)])),
        ("Problemas com a tabuada", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Multiplicar é somar <b>parcelas iguais</b>: 4 + 4 + 4 = 3 × 4 = 12.",
         "Na tabuada do 2 conte de 2 em 2; na do 5, de 5 em 5; na do 10, de 10 em 10. A tabuada do 4 é o dobro da do 2.",
         "O <b>dobro</b> é × 2 e o <b>triplo</b> é × 3.",
         "A ordem dos fatores não altera o produto: 3 × 4 = 4 × 3. Assim, quem sabe 3 × 8 também sabe 8 × 3."],
        [("5 × 7", ["Conte de 5 em 5 sete vezes: 5, 10, 15, 20, 25, 30, 35"], "35"),
         ("4 × 6", ["2 × 6 = 12", "o dobro de 12 é 24"], "24")],
        [["4 × 3 = 7", "Isso é 4 + 3. Multiplicar é 3 + 3 + 3 + 3 = 12."],
         ["Pular um número na contagem de 5 em 5", "Use os dedos para contar quantas vezes já somou."],
         ["Achar que o dobro de 8 é 4", "Dobro é × 2 (16). Metade é ÷ 2 (4)."]],
        arranjo(3, 4, "apple"))
    faq = [("Que tabuadas a BNCC pede no 3º ano?", "A BNCC indica problemas de multiplicação por 2, 3, 4, 5 e 10 no 3º ano. As tabuadas do 6 ao 9 costumam ser completadas no 4º ano, mas aparecem aqui para revisão."),
           ("Como decorar a tabuada sem sofrimento?", "Comece pelas mais fáceis (2, 5 e 10), use a ordem dos fatores para aprender metade das contas e pratique poucos minutos todos os dias.")]
    make_unit(R, "tabuada", "N", ["EF03MA03", "EF03MA07"],
              "Construir e utilizar fatos básicos da adição e da multiplicação para o cálculo mental ou escrito; resolver e elaborar problemas de multiplicação (por 2, 3, 4, 5 e 10) com os significados de adição de parcelas iguais e elementos apresentados em disposição retangular",
              "Tabuada do 2, 3, 4, 5 e 10", "Tabuada",
              "Atividades de matemática para o 3º ano sobre a tabuada: tabuada do 2, 3, 4, 5 e 10, adição de parcelas iguais, dobro e triplo, fator que falta, sequências e problemas. 100 exercícios com gabarito.",
              "Multiplicar é somar parcelas iguais.", "3 × 4 = 4 × 3: a ordem não muda o produto.",
              body, faq, sets, 7)


if __name__ == "__main__":
    main()
