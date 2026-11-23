# -*- coding: utf-8 -*-
"""
Brasil Matemática 6º ano: Números naturais e sistema de numeração decimal (Números, EF06MA01, EF06MA02)
  python3 tools/gen_br_matematica_6_numeros_naturais_e_sistema_de_numeracao.py
Valor posicional até bilhões; ler e escrever (milhões, mil); compor e decompor; comparar e ordenar; antecessor e sucessor;
números romanos; características do sistema decimal (base 10, posicional, zero) comparadas com os sistemas egípcio e romano.
Erros: confundir valor absoluto e valor relativo, esquecer o zero numa ordem vazia, ler 3.040.000 como «três milhões e quatrocentos mil».
"""
import random
from br_common import lesson, mix
from br_9 import M, d, bank, unit

R = random.Random(86001)
ORD = ["unidades", "dezenas", "centenas", "unidades de milhar", "dezenas de milhar", "centenas de milhar", "unidades de milhão", "dezenas de milhão", "centenas de milhão", "unidades de bilhão"]


def rnum(k):
    n = R.randint(10 ** (k - 1), 10 ** k - 1)
    s = list(str(n))
    for i in R.sample(range(1, k), min(2, k - 1)):
        if R.random() < 0.4:
            s[i] = "0"
    return int("".join(s))


def s1_valor():
    n = rnum(R.randint(6, 10))
    s = str(n)
    i = R.choice([j for j in range(len(s)) if s[j] != "0"])
    pos = len(s) - 1 - i
    v = int(s[i]) * 10 ** pos
    if R.random() < 0.5:
        return M("No número %s, qual é o valor do algarismo da ordem das <b>%s</b>?" % (d(n), ORD[pos]), d(v),
                 [s[i], d(v * 10), d(v // 10) if pos else d(v * 100), d(int(s[i]) * 10 ** (pos + 2))], "O algarismo %s está nas %s: vale %s · %s = <b>%s</b>." % (s[i], ORD[pos], s[i], d(10 ** pos), d(v)))
    return M("No número %s, em que ordem está o algarismo que vale %s?" % (d(n), d(v)), ORD[pos], [ORD[p] for p in (pos - 1, pos + 1, pos + 2) if 0 <= p < len(ORD)] + [ORD[0] if pos > 2 else ORD[5]],
             "%s = %s · %s: ordem das <b>%s</b>." % (d(v), s[i], d(10 ** pos), ORD[pos]))


def palavras(n):
    bi, r = divmod(n, 10 ** 9)
    mi, r = divmod(r, 10 ** 6)
    mil, u = divmod(r, 1000)
    p = []
    if bi:
        p.append("%d %s" % (bi, "bilhão" if bi == 1 else "bilhões"))
    if mi:
        p.append("%d %s" % (mi, "milhão" if mi == 1 else "milhões"))
    if mil:
        p.append("%d mil" % mil)
    if u:
        p.append(str(u))
    return ", ".join(p[:-1]) + " e " + p[-1] if len(p) > 1 else p[0]


def s2_ler():
    k = R.choice([7, 8, 9, 10])
    n = R.randint(1, 9) * 10 ** (k - 1) + R.choice([0, R.randint(1, 999) * 1000]) + R.choice([0, R.randint(1, 999)])
    n += R.choice([0, R.randint(1, 99) * 10 ** 6]) if k >= 9 else 0
    if n % 10 ** (k - 1) == 0:
        return None
    w = palavras(n)
    mi, r = divmod(n, 10 ** 6)
    wr = [d(n * 10), d(n // 10), d(n + 9 * 10 ** (k - 2)), d(n - 10 ** (k - 1) // 10 * 9)]
    if R.random() < 0.5:
        return M("Como se escreve com algarismos o número «%s»?" % w, d(n), wr, "«%s» = <b>%s</b>." % (w, d(n)))
    return M("Como se lê o número %s?" % d(n), w, [palavras(n * 10), palavras(n // 10), palavras(n + 10 ** 6 if n % 10 ** 9 < 9 * 10 ** 8 else n - 10 ** 6)],
             "Separe as classes: %s = <b>%s</b>." % (d(n), w))


def s3_decompor():
    n = rnum(R.randint(6, 9))
    s = str(n)
    parts = [int(c) * 10 ** (len(s) - 1 - i) for i, c in enumerate(s) if c != "0"]
    if R.random() < 0.5:
        return M("Qual número é %s?" % " + ".join(d(p) for p in parts), d(n), [d(int("".join(c for c in s if c != "0"))), d(n * 10), d(sum(int(c) for c in s)), d(n // 10), d(n + 10 ** (len(s) - 2))],
                 "Juntando as ordens: <b>%s</b>." % d(n))
    return M("Qual é a decomposição de %s?" % d(n), " + ".join(d(p) for p in parts), [" + ".join(d(p * 10) for p in parts), " + ".join(d(p // 10) if p >= 10 else d(p) for p in parts), " + ".join(c for c in s if c != "0")],
             "Cada algarismo vezes o valor da sua ordem: <b>%s</b>." % " + ".join(d(p) for p in parts))


def s4_comparar():
    base = rnum(R.randint(7, 9))
    xs = sorted({base + R.choice([-1, 1]) * R.choice([10 ** R.randint(2, 6), 9 * 10 ** R.randint(1, 4)]) for _ in range(4)} | {base})
    if len(xs) < 4:
        return None
    xs = xs[:4]
    k = R.choice(["maior", "menor", "ordem", "suc"])
    sh = xs[:]
    R.shuffle(sh)
    if k == "maior":
        return M("Qual é o maior número: %s?" % "; ".join(d(x) for x in sh), d(xs[-1]), [d(x) for x in xs[:-1]], "Compare da ordem mais alta para a mais baixa: <b>%s</b>." % d(xs[-1]))
    if k == "menor":
        return M("Qual é o menor número: %s?" % "; ".join(d(x) for x in sh), d(xs[0]), [d(x) for x in xs[1:]], "<b>%s</b> é o menor." % d(xs[0]))
    if k == "ordem":
        ok = " &lt; ".join(d(x) for x in xs)
        return M("Qual é a ordem crescente de %s?" % "; ".join(d(x) for x in sh), ok, [" &lt; ".join(d(x) for x in [xs[1], xs[0], xs[2], xs[3]]), " &lt; ".join(d(x) for x in xs[::-1]), " &lt; ".join(d(x) for x in [xs[0], xs[2], xs[1], xs[3]])],
                 "Do menor para o maior: <b>%s</b>." % ok)
    n = R.choice([10 ** 6, 10 ** 7, 3 * 10 ** 6, 10 ** 9, 2 * 10 ** 8]) + R.choice([0, -0])
    if R.random() < 0.5:
        return M("Qual é o antecessor de %s?" % d(n), d(n - 1), [d(n + 1), d(n - 10), d(n - 1000)], "Antecessor: %s − 1 = <b>%s</b>." % (d(n), d(n - 1)))
    m = n - 1
    return M("Qual é o sucessor de %s?" % d(m), d(n), [d(m - 1), d(m + 10), d(m * 10 + 1)], "Sucessor: %s + 1 = <b>%s</b>." % (d(m), d(n)))


ROM = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


def rom(n):
    s = ""
    for v, l in ROM:
        while n >= v:
            s += l
            n -= v
    return s


def s5_romanos():
    n = R.choice([R.randint(14, 99), R.randint(100, 999), R.randint(1000, 3999), R.choice([4, 9, 14, 19, 40, 49, 90, 99, 400, 444, 900, 1999, 2024, 2026])])
    wrong_r = [rom(n).replace("IV", "IIII").replace("IX", "VIIII") if ("IV" in rom(n) or "IX" in rom(n)) else rom(n + 1), rom(n + 10) if n < 3990 else rom(n - 10), rom(n - 1) if n > 1 else "II", rom(n + 100) if n < 3800 else rom(n - 100)]
    if R.random() < 0.5:
        return M("Qual número o numeral romano <b>%s</b> representa?" % rom(n), d(n), [d(n + 10), d(n - 1), d(n + 2) if n % 10 != 8 else d(n - 2), d(n + 100)],
                 "Leia da esquerda para a direita; um símbolo menor antes de um maior subtrai: <b>%s = %s</b>." % (rom(n), d(n)))
    return M("Como se escreve %s em algarismos romanos?" % d(n), rom(n), wrong_r, "%s = <b>%s</b>." % (d(n), rom(n)))


s6_sistemas = bank(R, [
    ("No sistema de numeração decimal, cada ordem vale…", "10 vezes a ordem à sua direita", ["2 vezes a ordem à sua direita", "100 vezes a ordem à sua direita", "o mesmo que a ordem à sua direita"]),
    ("O nosso sistema é <b>posicional</b>. Isso quer dizer que…", "o valor do algarismo depende da posição", ["cada símbolo vale sempre o mesmo", "não existe o zero", "os números são escritos com letras"]),
    ("No sistema egípcio antigo, o símbolo do 10 repetido 3 vezes valia 30. Esse sistema era…", "aditivo e não posicional", ["posicional, como o nosso", "de base 2", "igual ao romano em tudo"]),
    ("Qual é a função do zero no sistema decimal?", "marcar uma ordem vazia", ["valer 10", "separar as classes", "indicar número negativo"]),
    ("Com quantos algarismos diferentes escrevemos qualquer número natural no sistema decimal?", "10", ["9", "100", "infinitos"]),
    ("No sistema romano, não existe símbolo para…", "o zero", ["o mil", "o cinco", "o cem"]),
    ("Quantas ordens tem a classe dos milhões?", "3", ["2", "4", "6"]),
    ("Em 4.507.000, quantas unidades de milhar há ao todo?", "4.507", ["507", "4", "4.507.000"]),
    ("Em 3.600.000, quantas centenas de milhar há ao todo?", "36", ["6", "3", "360"]),
    ("Um número de 10 algarismos começa na ordem das…", "unidades de bilhão", ["centenas de milhão", "dezenas de bilhão", "unidades de milhão"]),
    ("Qual é o menor número natural de 7 algarismos?", "1.000.000", ["9.999.999", "1.000.001", "100.000"]),
    ("Qual é o maior número natural de 6 algarismos diferentes?", "987.654", ["999.999", "987.650", "123.456"]),
    ("No numeral romano, um símbolo menor à esquerda de um maior…", "é subtraído", ["é somado", "é multiplicado", "não vale nada"]),
    ("No numeral romano, um mesmo símbolo pode se repetir seguido no máximo…", "3 vezes", ["2 vezes", "4 vezes", "quantas vezes quiser"]),
], "s6_sistemas")


def main():
    seen = set()
    sets = [
        ("Valor posicional", mix(R, seen, [(s1_valor, 20)])),
        ("Ler, escrever e decompor", mix(R, seen, [(s2_ler, 10), (s3_decompor, 10)])),
        ("Comparar e ordenar", mix(R, seen, [(s4_comparar, 20)])),
        ("Números romanos", mix(R, seen, [(s5_romanos, 20)])),
        ("O sistema de numeração", mix(R, seen, [(s6_sistemas, 12), (s1_valor, 4), (s3_decompor, 4)])),
    ]
    body = lesson(
        ["O sistema de numeração decimal tem <b>base 10</b>: dez unidades de uma ordem formam uma unidade da ordem seguinte.",
         "Ele é <b>posicional</b>: o 5 de 503 vale 500, e o 5 de 35 vale 5. O zero marca uma ordem vazia.",
         "As ordens se agrupam em classes de 3: unidades simples, milhares, milhões, bilhões. Para ler, separe as classes com o ponto.",
         "Para comparar, conte os algarismos; se forem iguais, compare da esquerda para a direita."],
        [("4.025.300", ["4 milhões", "25 mil", "300"], "4 milhões, 25 mil e 300"),
         ("MCMXCIX", ["M = 1.000", "CM = 900", "XC = 90", "IX = 9"], "1.999")],
        [["Confundir valor absoluto e posicional", "O 7 de 70.000 vale 70.000."],
         ["Esquecer o zero de uma ordem vazia", "Três milhões e quarenta mil = 3.040.000."],
         ["Somar sempre no romano", "IX = 10 − 1 = 9."]],
        "")
    faq = [("O que o 6º ano estuda sobre o sistema de numeração?", "Ler, escrever, comparar e ordenar números naturais grandes, reconhecer o valor posicional e comparar o sistema decimal com outros sistemas, como o romano e o egípcio (EF06MA01 e EF06MA02)."),
           ("Por que o sistema decimal é posicional?", "Porque o valor de cada algarismo depende da posição em que ele está: cada ordem vale 10 vezes a ordem à sua direita.")]
    unit(R, "numeros-naturais-e-sistema-de-numeracao", "N", ["EF06MA01", "EF06MA02"],
         "Comparar, ordenar, ler e escrever números naturais e números racionais cuja representação decimal é finita; reconhecer o sistema de numeração decimal, como o que prevaleceu no mundo ocidental, e destacar semelhanças e diferenças com outros sistemas",
         "Números naturais e sistema de numeração decimal", "Números naturais",
         "Atividades de matemática para o 6º ano sobre números naturais: valor posicional até bilhões, leitura e escrita, decomposição, comparar e ordenar, números romanos e sistemas de numeração. 100 exercícios com gabarito.",
         "Cada ordem vale 10 vezes a da direita.", "O valor do algarismo depende da posição.",
         body, faq, sets, 1, grade="6-ano")


if __name__ == "__main__":
    main()
